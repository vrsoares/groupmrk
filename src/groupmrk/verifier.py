"""URL verification with HTTP response handling."""

import asyncio
import ipaddress
import logging
import re
import socket
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx

from .models import (
    ALLOWED_PORTS,
    DANGEROUS_SCHEMES,
    MAX_REQUESTS,
    PRIVATE_IP_RANGES,
    PRIVATE_IPV6_RANGES,
    SAFE_EXTENSIONS,
    SENSITIVE_PARAMS,
    VerificationOutcome,
    VerificationResult,
)

logger = logging.getLogger(__name__)


def redact_url(url: str) -> str:
    """Redact sensitive parameters from URL.

    Replaces sensitive query params with [REDACTED] and
    redacts long alphanumeric path segments (potential tokens).
    """
    parsed = urlparse(url)

    # Redact sensitive query parameters
    if parsed.query:
        params = parsed.query.split("&")
        redacted_params = []
        for param in params:
            if "=" in param:
                key, value = param.split("=", 1)
                if key.lower() in SENSITIVE_PARAMS:
                    redacted_params.append(f"{key}=[REDACTED]")
                else:
                    redacted_params.append(param)
            else:
                redacted_params.append(param)
        query = "&".join(redacted_params)
    else:
        query = ""

    # Redact path segments that look like tokens (long alphanumeric strings)
    path = re.sub(r"/[a-zA-Z0-9]{32,}/", "/[REDACTED]/", parsed.path)

    return parsed._replace(query=query, path=path).geturl()


def _sanitize_error(error: str) -> str:
    """Sanitize error message to remove sensitive data."""
    # Remove anything that looks like a URL with credentials
    error = re.sub(r"://[^@]+@", "://[REDACTED]@", error)
    # Remove long hex strings (potential tokens)
    error = re.sub(r"[a-fA-F0-9]{32,}", "[REDACTED]", error)
    return error


def has_safe_extension(url: str) -> bool:
    """Check if URL has a safe file extension for GET fallback."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in SAFE_EXTENSIONS)


def _normalize_url(url: str) -> str:
    """Normalize URL for comparison (lowercase scheme/host, strip trailing slash)."""
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower().rstrip("/")
    path = parsed.path.rstrip("/") or "/"
    return f"{scheme}://{netloc}{path}"


def _is_private_ip(ip_str: str) -> bool:
    """Check if an IP address is in a private/reserved range."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True  # Invalid IP = block

    # Check IPv4 ranges
    for range_str in PRIVATE_IP_RANGES:
        if ip in ipaddress.ip_network(range_str, strict=False):
            return True

    # Check IPv6 ranges
    if isinstance(ip, ipaddress.IPv6Address):
        for range_str in PRIVATE_IPV6_RANGES:
            if ip in ipaddress.ip_network(range_str, strict=False):
                return True

    return False


def _resolve_and_check_ip(hostname: str) -> Optional[str]:
    """Resolve hostname and check if IP is private.

    Returns the resolved IP if public, None if private.
    """
    try:
        result = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for family, _, _, _, sockaddr in result:
            ip_str = sockaddr[0]
            if not _is_private_ip(ip_str):
                return ip_str
        return None  # All resolved IPs are private
    except (socket.gaierror, OSError):
        return None


def _check_url_credentials(url: str) -> bool:
    """Check if URL contains credentials (user:pass@host)."""
    parsed = urlparse(url)
    return bool(parsed.username)


def _check_redirect_port(url: str) -> bool:
    """Check if redirect target port is allowed."""
    parsed = urlparse(url)
    port = parsed.port
    if port is None:
        # Default port based on scheme
        return True
    return port in ALLOWED_PORTS


class URLVerifier:
    """Handles HTTP verification of URLs."""

    def __init__(self, timeout: float = 10.0, max_redirects: int = 5):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.requests_made = 0
        self.get_fallback_attempts = 0
        self.get_fallback_successes = 0
        self._semaphore = asyncio.Semaphore(5)

    def _check_request_limit(self) -> bool:
        """Check if we've hit the request limit."""
        return self.requests_made < MAX_REQUESTS

    def _increment_requests(self) -> None:
        """Increment request counter."""
        self.requests_made += 1

    async def verify(self, url: str) -> VerificationResult:
        """Verify a single URL.

        Returns VerificationResult with outcome and details.
        """
        # Check URL length
        if len(url) > 2048:
            logger.warning("URL too long (%d chars): %s...", len(url), url[:50])
            return VerificationResult(
                outcome=VerificationOutcome.FILTERED_4XX,
                error="URL too long (>2048 chars)",
            )

        # Check for credentials
        if _check_url_credentials(url):
            logger.warning("Credential URL blocked: %s", redact_url(url))
            return VerificationResult(
                outcome=VerificationOutcome.FILTERED_CREDENTIAL_URL,
                error="URL contains credentials",
            )

        # Check if private IP (block on initial request too)
        parsed = urlparse(url)
        if parsed.hostname:
            resolved_ip = _resolve_and_check_ip(parsed.hostname)
            if resolved_ip is None:
                logger.warning("Private IP blocked: %s", parsed.hostname)
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_SSRF,
                    error=f"Private IP: {parsed.hostname}",
                )

        # Check request limit
        if not self._check_request_limit():
            return VerificationResult(
                outcome=VerificationOutcome.FILTERED_CONNECTION,
                error="Request limit reached",
            )

        # Perform HTTP verification
        return await self._verify_http(url)

    async def _verify_http(self, url: str) -> VerificationResult:
        """Perform actual HTTP verification."""
        redirect_chain = [url]
        current_url = url

        for hop in range(self.max_redirects + 1):
            if not self._check_request_limit():
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_CONNECTION,
                    redirect_chain=redirect_chain,
                    error="Request limit reached during redirect",
                )

            # Re-verify IP before each request (DNS rebinding protection)
            if hop > 0:
                parsed = urlparse(current_url)
                if parsed.hostname:
                    resolved_ip = _resolve_and_check_ip(parsed.hostname)
                    if resolved_ip is None:
                        logger.warning("Private IP detected before request: %s", parsed.hostname)
                        return VerificationResult(
                            outcome=VerificationOutcome.FILTERED_SSRF,
                            redirect_chain=redirect_chain,
                            error=f"Private IP detected: {parsed.hostname}",
                        )

            try:
                self._increment_requests()
                async with httpx.AsyncClient(
                    timeout=self.timeout,
                    follow_redirects=False,
                    headers={"User-Agent": "groupmrk/1.0"},
                ) as client:
                    response = await client.head(current_url)

                status = response.status_code

                # Handle 304 Not Modified (before general 3xx)
                if status == 304:
                    return VerificationResult(
                        outcome=VerificationOutcome.VALID,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                    )

                # Handle redirects (3xx)
                if 300 <= status < 400:
                    location = response.headers.get("location")
                    if not location:
                        # No location header - treat as error
                        return VerificationResult(
                            outcome=VerificationOutcome.FILTERED_4XX,
                            status_code=status,
                            redirect_chain=redirect_chain,
                            error="Redirect without Location header",
                        )

                    # Use urljoin for proper relative URL resolution
                    # Handles /path, //host, and full URLs correctly
                    location = urljoin(current_url, location)

                    # Check for dangerous schemes
                    loc_parsed = urlparse(location)
                    if loc_parsed.scheme.lower() in DANGEROUS_SCHEMES:
                        logger.warning("Blocked dangerous scheme: %s", location)
                        return VerificationResult(
                            outcome=VerificationOutcome.FILTERED_SSRF,
                            status_code=status,
                            redirect_chain=redirect_chain,
                            error=f"Dangerous scheme: {loc_parsed.scheme}",
                        )

                    # Check redirect port
                    if not _check_redirect_port(location):
                        logger.warning("Blocked non-standard port: %s", location)
                        return VerificationResult(
                            outcome=VerificationOutcome.FILTERED_PORT,
                            status_code=status,
                            redirect_chain=redirect_chain,
                            error=f"Non-standard port: {urlparse(location).port}",
                        )

                    # Check for private IP in redirect target
                    loc_parsed = urlparse(location)
                    if loc_parsed.hostname:
                        resolved_ip = _resolve_and_check_ip(loc_parsed.hostname)
                        if resolved_ip is None:
                            logger.warning("Private IP in redirect: %s", loc_parsed.hostname)
                            return VerificationResult(
                                outcome=VerificationOutcome.FILTERED_SSRF,
                                status_code=status,
                                redirect_chain=redirect_chain,
                                error=f"Private IP in redirect: {loc_parsed.hostname}",
                            )

                    # Detect redirect loops (normalized comparison)
                    normalized_location = _normalize_url(location)
                    normalized_chain = [_normalize_url(u) for u in redirect_chain]
                    if normalized_location in normalized_chain:
                        logger.warning("Redirect loop detected: %s", redact_url(location))
                        return VerificationResult(
                            outcome=VerificationOutcome.FILTERED_LOOP,
                            status_code=status,
                            redirect_chain=redirect_chain,
                            error="Redirect loop detected",
                        )

                    redirect_chain.append(location)
                    current_url = location
                    continue

                # Handle success (2xx)
                if 200 <= status < 300:
                    return VerificationResult(
                        outcome=VerificationOutcome.REDIRECT_FOLLOWED if len(redirect_chain) > 1 else VerificationOutcome.VALID,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                    )

                # Handle 401 Unauthorized - keep
                if status == 401:
                    return VerificationResult(
                        outcome=VerificationOutcome.KEEP_AUTH_REQUIRED,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                    )

                # Handle 403 Forbidden - check for auth requirement
                if status == 403:
                    # Check if it requires authentication
                    www_auth = response.headers.get("www-authenticate", "")
                    if www_auth:
                        return VerificationResult(
                            outcome=VerificationOutcome.KEEP_AUTH_REQUIRED,
                            status_code=status,
                            final_url=current_url,
                            redirect_chain=redirect_chain,
                        )

                    # Check for safe extension GET fallback
                    # Use current_url (after redirects) not original url
                    if has_safe_extension(current_url):
                        return await self._try_get_fallback(current_url, redirect_chain, status)

                    return VerificationResult(
                        outcome=VerificationOutcome.FILTERED_4XX,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                        error="403 Forbidden",
                    )

                # Handle 405 Method Not Allowed
                if status == 405:
                    # Try GET fallback for safe extensions (use current_url)
                    if has_safe_extension(current_url):
                        return await self._try_get_fallback(current_url, redirect_chain, status)

                    return VerificationResult(
                        outcome=VerificationOutcome.FILTERED_4XX,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                        error="405 Method Not Allowed",
                    )

                # Handle 404 Not Found
                if status == 404:
                    return VerificationResult(
                        outcome=VerificationOutcome.FILTERED_404,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                        error="404 Not Found",
                    )

                # Handle other 4xx
                if 400 <= status < 500:
                    return VerificationResult(
                        outcome=VerificationOutcome.FILTERED_4XX,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                        error=f"{status} Client Error",
                    )

                # Handle 5xx Server Error
                if 500 <= status < 600:
                    return VerificationResult(
                        outcome=VerificationOutcome.FILTERED_5XX,
                        status_code=status,
                        final_url=current_url,
                        redirect_chain=redirect_chain,
                        error=f"{status} Server Error",
                    )

                # Unknown status
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_4XX,
                    status_code=status,
                    final_url=current_url,
                    redirect_chain=redirect_chain,
                    error=f"Unknown status: {status}",
                )

            except httpx.TimeoutException:
                logger.warning("Timeout: %s", redact_url(current_url))
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_TIMEOUT,
                    redirect_chain=redirect_chain,
                    error="Request timeout",
                )
            except httpx.ConnectError as e:
                logger.warning("Connection error: %s", redact_url(current_url))
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_CONNECTION,
                    redirect_chain=redirect_chain,
                    error=_sanitize_error(f"Connection error: {e}"),
                )
            except Exception as e:
                logger.warning("Error verifying %s", redact_url(current_url))
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_CONNECTION,
                    redirect_chain=redirect_chain,
                    error=_sanitize_error(f"Error: {e}"),
                )

        # Exceeded max redirects
        return VerificationResult(
            outcome=VerificationOutcome.FILTERED_LOOP,
            redirect_chain=redirect_chain,
            error=f"Max redirects ({self.max_redirects}) exceeded",
        )

    async def _try_get_fallback(
        self, url: str, redirect_chain: list[str], head_status: int
    ) -> VerificationResult:
        """Try GET request as fallback for HEAD (check Content-Length only)."""
        self.get_fallback_attempts += 1

        if not self._check_request_limit():
            return VerificationResult(
                outcome=VerificationOutcome.FILTERED_CONNECTION,
                redirect_chain=redirect_chain,
                error="Request limit reached",
            )

        # Re-verify IP before GET fallback (DNS rebinding protection)
        parsed = urlparse(url)
        if parsed.hostname:
            resolved_ip = _resolve_and_check_ip(parsed.hostname)
            if resolved_ip is None:
                logger.warning("Private IP in GET fallback: %s", parsed.hostname)
                return VerificationResult(
                    outcome=VerificationOutcome.FILTERED_SSRF,
                    redirect_chain=redirect_chain,
                    error=f"Private IP in GET fallback: {parsed.hostname}",
                )

        try:
            self._increment_requests()
            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=False,
                headers={"User-Agent": "groupmrk/1.0"},
            ) as client:
                response = await client.get(url, stream=True)

            status = response.status_code

            # Check Content-Length header only (don't read body)
            content_length = response.headers.get("content-length")
            if content_length:
                try:
                    size = int(content_length)
                    if size > 1_000_000:  # 1MB limit
                        logger.warning("GET fallback: file too large (%d bytes): %s", size, redact_url(url))
                        await response.aclose()
                        return VerificationResult(
                            outcome=VerificationOutcome.FILTERED_4XX,
                            status_code=status,
                            final_url=url,
                            redirect_chain=redirect_chain,
                            error=f"File too large: {size} bytes",
                        )
                except ValueError:
                    pass  # Invalid Content-Length, continue

            # Close immediately without reading body
            await response.aclose()

            if 200 <= status < 300:
                self.get_fallback_successes += 1
                logger.info("GET fallback succeeded for %s (HEAD was %d)", redact_url(url), head_status)
                return VerificationResult(
                    outcome=VerificationOutcome.VALID,
                    status_code=status,
                    final_url=url,
                    redirect_chain=redirect_chain,
                )

            return VerificationResult(
                outcome=VerificationOutcome.FILTERED_4XX,
                status_code=status,
                final_url=url,
                redirect_chain=redirect_chain,
                error=f"GET fallback failed: {status}",
            )

        except Exception as e:
            logger.warning("GET fallback error: %s", redact_url(url))
            return VerificationResult(
                outcome=VerificationOutcome.FILTERED_CONNECTION,
                redirect_chain=redirect_chain,
                error=_sanitize_error(f"GET fallback error: {e}"),
            )

    async def verify_batch(self, urls: list[str]) -> list[VerificationResult]:
        """Verify multiple URLs with concurrency control."""
        results = []

        # Process in batches of 5
        for i in range(0, len(urls), 5):
            batch = urls[i:i + 5]
            batch_results = await asyncio.gather(
                *[self._verify_with_semaphore(url) for url in batch],
                return_exceptions=True,
            )
            for url, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.error("Unexpected error for %s", redact_url(url))
                    results.append(VerificationResult(
                        outcome=VerificationOutcome.FILTERED_CONNECTION,
                        error=_sanitize_error(f"Unexpected error: {result}"),
                    ))
                else:
                    results.append(result)

            # Delay between batches
            if i + 5 < len(urls):
                await asyncio.sleep(0.1)

        return results

    async def _verify_with_semaphore(self, url: str) -> VerificationResult:
        """Verify URL with semaphore for concurrency control."""
        async with self._semaphore:
            return await self.verify(url)
