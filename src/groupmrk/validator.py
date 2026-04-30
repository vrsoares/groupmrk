"""URL validation module for security checks.

This module validates URLs to ensure they are safe and properly formatted.
It checks for dangerous patterns like SQL injection, XSS attacks, and
ensures URLs don't point to internal private networks.

Simple language guide:
- validate_url: Check if a URL is safe to use
- is_local_url: Check if URL is from your private network (like home WiFi)
- is_ip_address: Check if URL uses numbers instead of a website name
- normalize_url: Clean up a URL so duplicates can be found
- redact_sensitive_params: Hide passwords/tokens in logs so they can't be seen
"""

from typing import Optional
from urllib.parse import urlparse

from .models import URL, ValidationResult


SUSPICIOUS_PATTERNS: list[str] = [
    "javascript:",
    "data:",
    "vbscript:",
]

REJECT_PATTERNS: list[str] = [
    "' OR '1'='1",
    "1=1",
    "--",
    "DROP TABLE",
    "<script",
    "onerror=",
    "onload=",
    "..%2F",
    "%2E%2E",
]


def validate_url(url_string: str) -> ValidationResult:
    """Validate a URL string for security issues."""
    if not url_string or not url_string.strip():
        return ValidationResult(
            is_valid=False,
            is_suspicious=False,
            reason="Empty or whitespace URL",
            patterns_found=[],
        )

    url_string = url_string.strip()
    patterns_found: list[str] = []

    for pattern in REJECT_PATTERNS:
        if pattern.lower() in url_string.lower():
            patterns_found.append(pattern)
            return ValidationResult(
                is_valid=False,
                is_suspicious=False,
                reason=f"Invalid characters detected: {pattern}",
                patterns_found=patterns_found,
            )

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.lower() in url_string.lower():
            patterns_found.append(pattern)

    try:
        parsed = urlparse(url_string)
    except Exception:
        return ValidationResult(
            is_valid=False,
            is_suspicious=False,
            reason="Invalid URL format",
            patterns_found=patterns_found,
        )

    if parsed.scheme and parsed.scheme.lower() not in ("http", "https", ""):
        return ValidationResult(
            is_valid=False,
            is_suspicious=False,
            reason=f"Invalid scheme: {parsed.scheme}",
            patterns_found=patterns_found,
        )

    if parsed.netloc:
        if is_non_routable_ip(parsed.netloc):
            return ValidationResult(
                is_valid=False,
                is_suspicious=False,
                reason="Non-routable IP address (link-local/reserved)",
                patterns_found=patterns_found,
            )

    if not parsed.netloc and not parsed.path:
        return ValidationResult(
            is_valid=False,
            is_suspicious=False,
            reason="No valid hostname or path found",
            patterns_found=patterns_found,
        )

    is_suspicious = len(patterns_found) > 0
    return ValidationResult(
        is_valid=True,
        is_suspicious=is_suspicious,
        reason="Valid" if not is_suspicious else f"Warning: {', '.join(patterns_found)}",
        patterns_found=patterns_found,
    )


def parse_url(url_string: str) -> Optional[URL]:
    """Parse a URL string into a URL value object."""
    if not url_string or not url_string.strip():
        return None

    url_string = url_string.strip()

    try:
        parsed = urlparse(url_string)
    except Exception:
        return None

    scheme = parsed.scheme.lower() if parsed.scheme else ""
    host = parsed.netloc or ""

    is_local = _is_local_network(host)
    is_ip = _is_ip_address(host)

    normalized = url_string.lower()
    if normalized.endswith("/"):
        normalized = normalized[:-1]

    return URL(
        original=url_string,
        normalized=normalized,
        scheme=scheme,
        host=host,
        is_local=is_local,
        is_ip=is_ip,
    )


def _is_local_network(host: str) -> bool:
    """Check if hostname is a local/private network address."""
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


def is_non_routable_ip(host: str) -> bool:
    """Check if hostname is a non-routable IP (non-RFC1918).

    These include link-local (169.254.x.x) and other reserved ranges.
    Should be rejected for security.

    RFC1918 (ALLOWED): 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
    NON-ROUTABLE (REJECT): 169.254.0.0/16, 0.0.0.0/8, 100.64.0.0/10, 224.0.0.0/4, etc.
    """
    if not host:
        return False

    parts = host.split(":")[0].split(".")
    if len(parts) != 4:
        return False

    try:
        first = int(parts[0])
        second = int(parts[1])

        if first == 169 and second == 254:
            return True

        if first == 0:
            return True

        if first == 100 and 64 <= second <= 127:
            return True

        if first >= 224:
            return True

        return False
    except (ValueError, IndexError):
        return False


def _is_ip_address(host: str) -> bool:
    """Check if hostname is an IP address."""
    if not host:
        return False

    return host.replace(".", "").isdigit()


def is_local_url(url_string: str) -> bool:
    """Check if URL is a local or private network URL."""
    try:
        parsed = urlparse(url_string)
        host = parsed.netloc or parsed.path
        return _is_local_network(host)
    except Exception:
        return False


def is_ip_address(url_string: str) -> bool:
    """Check if URL host is an IP address."""
    try:
        parsed = urlparse(url_string)
        host = parsed.netloc or parsed.path
        return _is_ip_address(host)
    except Exception:
        return False


def normalize_url(url_string: str) -> str:
    """Normalize URL for deduplication comparison."""
    if not url_string:
        return ""

    url_string = url_string.strip().lower()

    try:
        parsed = urlparse(url_string)

        scheme = parsed.scheme or "http"
        netloc = parsed.netloc.lower()

        if netloc.endswith(":80") and scheme == "http":
            netloc = netloc[:-4]
        elif netloc.endswith(":443") and scheme == "https":
            netloc = netloc[:-5]

        path = parsed.path
        if path.endswith("/") and len(path) > 1:
            path = path[:-1]

        path = path.replace("/./", "/").replace("//", "/")

        query = parsed.query

        normalized = f"{scheme}://{netloc}{path}"
        if query:
            normalized += f"?{query}"

        return normalized
    except Exception:
        return url_string.lower()


def detect_sql_injection(url_string: str) -> list[str]:
    """Detect SQL injection patterns in URL."""
    patterns = ["'", " OR ", " UNION ", " SELECT ", " DROP ", "--", "1=1"]
    found = []
    url_lower = url_string.lower()
    for pattern in patterns:
        if pattern.lower() in url_lower:
            found.append(pattern)
    return found


def detect_xss(url_string: str) -> list[str]:
    """Detect XSS patterns in URL."""
    patterns = ["<script", "javascript:", "onerror", "onload", "<img"]
    found = []
    url_lower = url_string.lower()
    for pattern in patterns:
        if pattern in url_lower:
            found.append(pattern)
    return found


def detect_path_traversal(url_string: str) -> list[str]:
    """Detect path traversal patterns in URL."""
    patterns = ["../", "..\\", "/etc/", "C:\\"]
    found = []
    for pattern in patterns:
        if pattern in url_string:
            found.append(pattern)
    return found


def detect_invalid_characters(url_string: str) -> list[str]:
    """Detect invalid characters in URL."""
    invalid_chars = ["<", ">", '"', ";"]
    found = []
    for char in invalid_chars:
        if char in url_string:
            found.append(char)
    return found


def redact_sensitive_params(url_string: str) -> str:
    """Redact sensitive query parameters from URL for logging."""
    sensitive_params = ["token", "password", "secret", "key", "auth", "api_key", "session"]

    try:
        parsed = urlparse(url_string)
        query_params = parsed.query.split("&") if parsed.query else []
        safe_params = []

        for param in query_params:
            param_lower = param.lower()
            is_sensitive = any(s in param_lower for s in sensitive_params)
            if is_sensitive and "=" in param:
                key = param.split("=")[0]
                safe_params.append(f"{key}=[REDACTED]")
            else:
                safe_params.append(param)

        safe_query = "&".join(safe_params)
        result = parsed._replace(query=safe_query).geturl()
        return result
    except Exception:
        return url_string