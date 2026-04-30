"""Tests for URL verifier."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from groupmrk.models import VerificationOutcome
from groupmrk.verifier import (
    URLVerifier,
    has_safe_extension,
    redact_url,
    _is_private_ip,
    _check_url_credentials,
    _check_redirect_port,
)


class TestRedactUrl:
    """Test URL redaction."""

    def test_redact_token_param(self):
        url = "https://example.com/page?token=abc123&other=test"
        result = redact_url(url)
        assert "token=[REDACTED]" in result
        assert "other=test" in result

    def test_redact_multiple_sensitive_params(self):
        url = "https://example.com?token=abc&session_id=xyz&password=secret"
        result = redact_url(url)
        assert "token=[REDACTED]" in result
        assert "session_id=[REDACTED]" in result
        assert "password=[REDACTED]" in result

    def test_redact_long_path_segments(self):
        url = "https://example.com/api/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6/resource"
        result = redact_url(url)
        assert "[REDACTED]" in result

    def test_no_redaction_needed(self):
        url = "https://example.com/page?q=search"
        result = redact_url(url)
        assert result == url

    def test_redact_api_key(self):
        url = "https://api.example.com/data?api_key=12345"
        result = redact_url(url)
        assert "api_key=[REDACTED]" in result


class TestHasSafeExtension:
    """Test safe extension detection."""

    def test_pdf_extension(self):
        assert has_safe_extension("https://example.com/file.pdf") is True

    def test_zip_extension(self):
        assert has_safe_extension("https://example.com/file.zip") is True

    def test_docx_extension(self):
        assert has_safe_extension("https://example.com/file.docx") is True

    def test_jpg_extension(self):
        assert has_safe_extension("https://example.com/image.jpg") is True

    def test_html_extension(self):
        assert has_safe_extension("https://example.com/page.html") is True

    def test_no_extension(self):
        assert has_safe_extension("https://example.com/page") is False

    def test_php_extension(self):
        assert has_safe_extension("https://example.com/page.php") is False

    def test_case_insensitive(self):
        assert has_safe_extension("https://example.com/file.PDF") is True


class TestIsPrivateIp:
    """Test private IP detection."""

    def test_private_10_range(self):
        assert _is_private_ip("10.0.0.1") is True

    def test_private_172_range(self):
        assert _is_private_ip("172.16.0.1") is True

    def test_private_192_range(self):
        assert _is_private_ip("192.168.1.1") is True

    def test_link_local(self):
        assert _is_private_ip("169.254.0.1") is True

    def test_loopback(self):
        assert _is_private_ip("127.0.0.1") is True

    def test_public_ip(self):
        assert _is_private_ip("8.8.8.8") is False

    def test_public_ip_2(self):
        assert _is_private_ip("1.1.1.1") is False

    def test_ipv6_loopback(self):
        assert _is_private_ip("::1") is True

    def test_ipv6_link_local(self):
        assert _is_private_ip("fe80::1") is True


class TestCheckUrlCredentials:
    """Test credential URL detection."""

    def test_url_with_credentials(self):
        assert _check_url_credentials("http://user:pass@example.com") is True

    def test_url_without_credentials(self):
        assert _check_url_credentials("http://example.com") is False

    def test_url_with_username_only(self):
        assert _check_url_credentials("http://user@example.com") is True


class TestCheckRedirectPort:
    """Test redirect port validation."""

    def test_standard_http_port(self):
        assert _check_redirect_port("http://example.com:80") is True

    def test_standard_https_port(self):
        assert _check_redirect_port("https://example.com:443") is True

    def test_no_port(self):
        assert _check_redirect_port("http://example.com") is True

    def test_non_standard_port(self):
        assert _check_redirect_port("http://example.com:8080") is False

    def test_ssh_port(self):
        assert _check_redirect_port("http://example.com:22") is False


class TestURLVerifier:
    """Test URLVerifier class."""

    @pytest.fixture
    def verifier(self):
        return URLVerifier(timeout=5.0, max_redirects=3)

    @pytest.mark.asyncio
    async def test_url_too_long(self, verifier):
        url = "https://example.com/" + "a" * 2050
        result = await verifier.verify(url)
        assert result.outcome == VerificationOutcome.FILTERED_4XX
        assert "too long" in result.error.lower()

    @pytest.mark.asyncio
    async def test_credential_url_blocked(self, verifier):
        url = "http://user:pass@example.com"
        result = await verifier.verify(url)
        assert result.outcome == VerificationOutcome.FILTERED_CREDENTIAL_URL

    @pytest.mark.asyncio
    async def test_private_ip_blocked(self, verifier):
        url = "http://192.168.1.1/admin"
        result = await verifier.verify(url)
        assert result.outcome == VerificationOutcome.FILTERED_SSRF

    @pytest.mark.asyncio
    async def test_private_ip_10_range(self, verifier):
        url = "http://10.0.0.1/test"
        result = await verifier.verify(url)
        assert result.outcome == VerificationOutcome.FILTERED_SSRF

    @pytest.mark.asyncio
    async def test_request_limit_check(self, verifier):
        verifier.requests_made = 5000
        url = "https://example.com"
        result = await verifier.verify(url)
        assert result.outcome == VerificationOutcome.FILTERED_CONNECTION
        assert "limit" in result.error.lower()
