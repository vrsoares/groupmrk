"""URL verification module for HTTP HEAD requests.

This module checks if a website URL is working by sending a simple
HTTP HEAD request (which is like a quick "is this there?" message).

Simple language guide:
- verify_url: Check if a website is online and working
- verify_batch: Check many websites at once
- The system skips checking local/private networks (home WiFi addresses)
- All checks have a 5-second timeout to prevent hanging
"""

import logging
from urllib.parse import urlparse

import httpx

from .models import URLVerificationResult
from .validator import redact_sensitive_params

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT: float = 5.0
MAX_REDIRECTS: int = 1
MAX_CONCURRENT: int = 10


def verify_url(url_string: str, timeout: float = DEFAULT_TIMEOUT) -> URLVerificationResult:
    """Verify a URL is reachable via HTTP HEAD request."""
    if not url_string or not url_string.strip():
        return URLVerificationResult(
            status_code=0,
            is_reachable=False,
            error_type="invalid_input",
            verification_skipped=False,
        )

    parsed_url = _extract_host(url_string)

    if parsed_url and _is_local_or_private(parsed_url):
        safe_url = redact_sensitive_params(url_string)
        logger.debug(f"Skipping verification for local URL: {safe_url}")
        return URLVerificationResult(
            status_code=0,
            is_reachable=False,
            error_type="none",
            verification_skipped=True,
        )

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            max_redirects=MAX_REDIRECTS,
            verify=True,
        ) as client:
            response = client.head(url_string)
            is_reachable = 200 <= response.status_code < 400

            return URLVerificationResult(
                status_code=response.status_code,
                is_reachable=is_reachable,
                error_type="none",
                verification_skipped=False,
            )

    except httpx.TimeoutException:
        safe_url = redact_sensitive_params(url_string)
        logger.debug(f"Timeout verifying URL: {safe_url}")
        return URLVerificationResult(
            status_code=0,
            is_reachable=False,
            error_type="timeout",
            verification_skipped=False,
        )

    except httpx.ConnectError:
        safe_url = redact_sensitive_params(url_string)
        logger.debug(f"Connection error for URL: {safe_url}")
        return URLVerificationResult(
            status_code=0,
            is_reachable=False,
            error_type="connection",
            verification_skipped=False,
        )

    except Exception as e:
        error_str = str(e).lower()
        safe_url = redact_sensitive_params(url_string)
        if "ssl" in error_str or "tls" in error_str or "certificate" in error_str:
            logger.debug(f"SSL error for URL: {safe_url}")
            return URLVerificationResult(
                status_code=0,
                is_reachable=False,
                error_type="ssl",
                verification_skipped=False,
            )
        logger.debug(f"Error verifying URL {safe_url}: {e}")
        return URLVerificationResult(
            status_code=0,
            is_reachable=False,
            error_type="unknown",
            verification_skipped=False,
        )


def _extract_host(url_string: str) -> str:
    """Extract hostname from URL for local check."""
    try:
        parsed = urlparse(url_string)
        return parsed.netloc or parsed.path
    except Exception:
        return ""


def _is_local_or_private(host: str) -> bool:
    """Check if host is local or private network."""
    if not host:
        return False

    host_lower = host.lower()

    if host_lower in ("localhost", "127.0.0.1", "::1"):
        return True

    private_prefixes = (
        "10.",
        "192.168.",
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.2",
        "172.30.",
        "172.31.",
    )
    if any(host_lower.startswith(prefix) for prefix in private_prefixes):
        return True

    if host_lower.endswith(".local"):
        return True

    return False


def verify_batch(urls: list[str]) -> dict[str, URLVerificationResult]:
    """Verify multiple URLs with batch processing."""
    results = {}

    for url in urls:
        results[url] = verify_url(url)

    return results