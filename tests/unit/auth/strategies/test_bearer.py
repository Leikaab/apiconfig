"""Tests for the BearerAuth strategy."""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock as MockClass

import pytest

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.exceptions.auth import AuthStrategyError, ExpiredTokenError


class TestBearerAuth:
    """Tests for the BearerAuth strategy."""

    def test_init_with_valid_token_only(self) -> None:
        """Test initialization with a valid token only."""
        auth = BearerAuth(access_token="valid_token")
        assert auth.access_token == "valid_token"
        assert auth._expires_at is None  # pyright: ignore[reportPrivateUsage]
        assert auth._http_request_callable is None  # pyright: ignore[reportPrivateUsage]

    def test_init_with_all_parameters(self) -> None:
        """Test initialization with all parameters."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        http_callable = MockClass()

        auth = BearerAuth(access_token="valid_token", expires_at=expires_at, http_request_callable=http_callable)

        assert auth.access_token == "valid_token"
        assert auth._expires_at == expires_at  # pyright: ignore[reportPrivateUsage]
        assert auth._http_request_callable == http_callable  # pyright: ignore[reportPrivateUsage]

    def test_init_rejects_empty_token(self) -> None:
        """Test that BearerAuth rejects empty tokens."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="Bearer token cannot be empty or whitespace"):
            BearerAuth(access_token="")

        # Whitespace only
        with pytest.raises(AuthStrategyError, match="Bearer token cannot be empty or whitespace"):
            BearerAuth(access_token="   ")

    def test_can_refresh_without_http_callable(self) -> None:
        """Test can_refresh returns False when no HTTP callable is provided."""
        auth = BearerAuth(access_token="test_token")
        assert auth.can_refresh() is False

    def test_can_refresh_with_http_callable(self) -> None:
        """Test can_refresh returns True when HTTP callable is provided."""
        http_callable = MockClass()
        auth = BearerAuth(access_token="test_token", http_request_callable=http_callable)
        assert auth.can_refresh() is True

    def test_is_expired_without_expires_at(self) -> None:
        """Test is_expired returns False when no expiration time is set."""
        auth = BearerAuth(access_token="test_token")
        assert auth.is_expired() is False

    def test_is_expired_with_future_expiration(self) -> None:
        """Test is_expired returns False when token expires in the future (beyond buffer)."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        auth = BearerAuth(access_token="test_token", expires_at=expires_at)
        assert auth.is_expired() is False

    def test_is_expired_with_past_expiration(self) -> None:
        """Test is_expired returns True when token has already expired."""
        expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
        auth = BearerAuth(access_token="test_token", expires_at=expires_at)
        assert auth.is_expired() is True

    def test_is_expired_within_buffer_time(self) -> None:
        """Test is_expired returns True when token expires within 5-minute buffer."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=3)
        auth = BearerAuth(access_token="test_token", expires_at=expires_at)
        assert auth.is_expired() is True

    def test_is_expired_exactly_at_buffer_boundary(self) -> None:
        """Test is_expired behavior at the 5-minute buffer boundary."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        auth = BearerAuth(access_token="test_token", expires_at=expires_at)
        # Should be considered expired due to >= comparison
        assert auth.is_expired() is True

    def test_refresh_raises_error_when_not_refreshable(self) -> None:
        """Test refresh raises AuthStrategyError when strategy cannot refresh."""
        auth = BearerAuth(access_token="test_token")

        with pytest.raises(AuthStrategyError, match="Bearer auth strategy is not configured for refresh"):
            auth.refresh()

    def test_refresh_raises_not_implemented_when_refreshable(self) -> None:
        """Test refresh raises NotImplementedError when refreshable but no custom logic."""
        http_callable = MockClass()
        auth = BearerAuth(access_token="test_token", http_request_callable=http_callable)

        with pytest.raises(NotImplementedError, match="Bearer auth refresh requires custom implementation"):
            auth.refresh()

    def test_prepare_request_headers_with_valid_token(self) -> None:
        """Test prepare_request_headers generates the correct Authorization header."""
        auth = BearerAuth(access_token="test_token")
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Bearer test_token"}

    def test_prepare_request_headers_with_expired_non_refreshable_token(self) -> None:
        """Test prepare_request_headers raises ExpiredTokenError for expired non-refreshable token."""
        expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
        auth = BearerAuth(access_token="test_token", expires_at=expires_at)

        with pytest.raises(ExpiredTokenError, match="Bearer token is expired and cannot be refreshed"):
            auth.prepare_request_headers()

    def test_prepare_request_headers_with_expired_refreshable_token(self) -> None:
        """Test prepare_request_headers works with expired but refreshable token."""
        expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
        http_callable = MockClass()
        auth = BearerAuth(access_token="test_token", expires_at=expires_at, http_request_callable=http_callable)

        # Should not raise ExpiredTokenError since token can be refreshed
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Bearer test_token"}

    def test_prepare_request_params(self) -> None:
        """Test prepare_request_params returns an empty dictionary."""
        auth = BearerAuth(access_token="test_token")
        params = auth.prepare_request_params()
        assert params == {}

    def test_get_refresh_callback_without_refresh_capability(self) -> None:
        """Test get_refresh_callback returns None when refresh is not supported."""
        auth = BearerAuth(access_token="test_token")
        callback = auth.get_refresh_callback()
        assert callback is None

    def test_get_refresh_callback_with_refresh_capability(self) -> None:
        """Test get_refresh_callback returns a callable when refresh is supported."""
        http_callable = MockClass()
        auth = BearerAuth(access_token="test_token", http_request_callable=http_callable)
        callback = auth.get_refresh_callback()

        assert callback is not None
        assert callable(callback)

        # Test that calling the callback attempts to call refresh
        with pytest.raises(NotImplementedError):
            callback()
