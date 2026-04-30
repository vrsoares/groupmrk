"""Unit tests for URL verifier module."""

import pytest
from unittest.mock import patch, MagicMock
from groupmrk.verifier import (
    verify_url,
    verify_batch,
    _extract_host,
    _is_local_or_private,
)
from groupmrk.models import URLVerificationResult


class TestVerifyURL:
    """Tests for verify_url function."""

    def test_verify_url_with_successful_response(self):
        """Test verification of reachable URL."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com")

            assert result.is_reachable is True
            assert result.status_code == 200
            assert result.verification_skipped is False

    def test_verify_url_with_redirect_response(self):
        """Test verification of redirect URL (3xx is reachable)."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 301
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/redirect")

            assert result.is_reachable is True
            assert result.status_code == 301
            assert result.verification_skipped is False

    def test_verify_url_with_client_error(self):
        """Test verification of URL with client error (4xx not reachable)."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/notfound")

            assert result.is_reachable is False
            assert result.status_code == 404
            assert result.verification_skipped is False

    def test_verify_url_with_server_error(self):
        """Test verification of URL with server error (5xx not reachable)."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/error")

            assert result.is_reachable is False
            assert result.status_code == 500

    def test_verify_url_timeout(self):
        """Test handling of timeout errors."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            import httpx
            mock_client = MagicMock()
            mock_client.head.side_effect = httpx.TimeoutException("Timeout")
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/slow")

            assert result.is_reachable is False
            assert result.error_type == "timeout"
            assert result.verification_skipped is False

    def test_verify_url_connection_error(self):
        """Test handling of connection errors."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            import httpx
            mock_client = MagicMock()
            mock_client.head.side_effect = httpx.ConnectError("Connection refused")
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/unreachable")

            assert result.is_reachable is False
            assert result.error_type == "connection"
            assert result.verification_skipped is False

    def test_verify_url_catches_generic_exceptions(self):
        """Test that generic exceptions are handled as unknown."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            # Generic Exception that is not specifically caught
            mock_client.head.side_effect = Exception("Generic error")
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/error")

            assert result.is_reachable is False
            assert result.error_type == "unknown"
            assert result.verification_skipped is False


class TestLocalURLVerification:
    """Tests for local URL verification skipping."""

    def test_verify_url_skips_localhost(self):
        """Test that localhost URLs are skipped."""
        result = verify_url("http://localhost")
        assert result.verification_skipped is True
        assert result.error_type == "none"

    def test_verify_url_skips_127_0_0_1(self):
        """Test that 127.0.0.1 URLs without port are skipped."""
        result = verify_url("http://127.0.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_192_168(self):
        """Test that 192.168.x.x URLs are skipped."""
        result = verify_url("http://192.168.1.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_10(self):
        """Test that 10.x.x.x URLs are skipped."""
        result = verify_url("http://10.0.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_172_16(self):
        """Test that 172.16.x.x URLs are skipped."""
        result = verify_url("http://172.16.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_172_17(self):
        """Test that 172.17.x.x URLs are skipped."""
        result = verify_url("http://172.17.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_172_18(self):
        """Test that 172.18.x.x URLs are skipped."""
        result = verify_url("http://172.18.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_172_19(self):
        """Test that 172.19.x.x URLs are skipped."""
        result = verify_url("http://172.19.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_172_30(self):
        """Test that 172.30.x.x URLs are skipped."""
        result = verify_url("http://172.30.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_private_network_172_31(self):
        """Test that 172.31.x.x URLs are skipped."""
        result = verify_url("http://172.31.0.1")
        assert result.verification_skipped is True

    def test_verify_url_skips_dot_local_domain(self):
        """Test that .local mDNS domain URLs are skipped."""
        result = verify_url("http://myserver.local")
        assert result.verification_skipped is True


class TestVerifyBatch:
    """Tests for batch URL verification."""

    def test_verify_batch_single_url(self):
        """Test batch verification with single URL."""
        with patch("groupmrk.verifier.verify_url") as mock_verify:
            mock_verify.return_value = URLVerificationResult(
                status_code=200,
                is_reachable=True,
                error_type="none",
                verification_skipped=False,
            )
            results = verify_batch(["https://example.com"])

            assert len(results) == 1
            assert "https://example.com" in results

    def test_verify_batch_multiple_urls(self):
        """Test batch verification with multiple URLs."""
        with patch("groupmrk.verifier.verify_url") as mock_verify:
            mock_verify.return_value = URLVerificationResult(
                status_code=200,
                is_reachable=True,
                error_type="none",
                verification_skipped=False,
            )
            urls = [
                "https://example.com",
                "https://example.org",
                "https://example.net",
            ]
            results = verify_batch(urls)

            assert len(results) == 3
            for url in urls:
                assert url in results

    def test_verify_batch_empty_list(self):
        """Test batch verification with empty list."""
        results = verify_batch([])
        assert results == {}

    def test_verify_batch_returns_dict(self):
        """Test that batch returns dictionary."""
        with patch("groupmrk.verifier.verify_url") as mock_verify:
            mock_verify.return_value = URLVerificationResult(
                status_code=0,
                is_reachable=False,
                error_type="none",
                verification_skipped=True,
            )
            results = verify_batch(["https://example.com"])

            assert isinstance(results, dict)
            assert isinstance(results["https://example.com"], URLVerificationResult)


class TestExtractHost:
    """Tests for host extraction from URLs."""

    def test_extract_host_from_https(self):
        """Test host extraction from HTTPS URL."""
        host = _extract_host("https://example.com/path")
        assert host == "example.com"

    def test_extract_host_from_http_with_port(self):
        """Test host extraction from HTTP URL with port."""
        host = _extract_host("http://example.com:8080/path")
        assert host == "example.com:8080"

    def test_extract_host_from_ip(self):
        """Test host extraction from IP URL."""
        host = _extract_host("http://192.168.1.1/page")
        assert host == "192.168.1.1"

    def test_extract_host_from_local_path(self):
        """Test host extraction from local path."""
        host = _extract_host("file:///path/to/file")
        assert host == "/path/to/file"

    def test_extract_host_handles_non_standard_url(self):
        """Test host extraction from non-standard URL."""
        # Non-standard URL returns original string
        host = _extract_host("not a url")
        assert host == "not a url"

    def test_extract_host_handles_empty_string(self):
        """Test host extraction from empty string."""
        host = _extract_host("")
        assert host == ""


class TestIsLocalOrPrivate:
    """Tests for local/private network detection."""

    def test_is_local_or_private_localhost(self):
        """Test localhost detection."""
        assert _is_local_or_private("localhost") is True
        assert _is_local_or_private("127.0.0.1") is True
        assert _is_local_or_private("::1") is True

    def test_is_local_or_private_192_168(self):
        """Test 192.168.x.x detection."""
        assert _is_local_or_private("192.168.0.1") is True
        assert _is_local_or_private("192.168.1.1") is True
        assert _is_local_or_private("192.168.255.255") is True

    def test_is_local_or_private_10(self):
        """Test 10.x.x.x detection."""
        assert _is_local_or_private("10.0.0.1") is True
        assert _is_local_or_private("10.255.255.255") is True

    def test_is_local_or_private_172_16_31(self):
        """Test 172.16-31.x.x detection."""
        assert _is_local_or_private("172.16.0.1") is True
        assert _is_local_or_private("172.31.255.255") is True

    def test_is_local_or_private_dot_local(self):
        """Test .local mDNS domain detection."""
        assert _is_local_or_private("server.local") is True

    def test_is_local_or_private_rejects_public_ip(self):
        """Test that public IPs are rejected."""
        assert _is_local_or_private("8.8.8.8") is False
        assert _is_local_or_private("1.1.1.1") is False

    def test_is_local_or_private_rejects_public_domain(self):
        """Test that public domains are rejected."""
        assert _is_local_or_private("example.com") is False
        assert _is_local_or_private("google.com") is False

    def test_is_local_or_private_handles_empty_string(self):
        """Test handling of empty string."""
        assert _is_local_or_private("") is False


class TestTimeoutConfiguration:
    """Tests for timeout configuration."""

    def test_verify_url_uses_custom_timeout(self):
        """Test that custom timeout is passed to client."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            verify_url("https://example.com", timeout=10.0)

            call_kwargs = mock_client_class.call_args[1]
            assert call_kwargs["timeout"] == 10.0

    def test_verify_url_uses_default_timeout(self):
        """Test that default timeout is used when not specified."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            verify_url("https://example.com")

            call_kwargs = mock_client_class.call_args[1]
            assert call_kwargs["timeout"] == 5.0  # DEFAULT_TIMEOUT


class TestRedirectHandling:
    """Tests for redirect handling."""

    def test_verify_url_follows_redirects(self):
        """Test that redirects are followed."""
        with patch("groupmrk.verifier.httpx.Client") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 302
            mock_client = MagicMock()
            mock_client.head.return_value = mock_response
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client_class.return_value = mock_client

            result = verify_url("https://example.com/redirect")

            # Should be reachable since 302 is in 200-399 range
            assert result.is_reachable is True
            assert result.status_code == 302