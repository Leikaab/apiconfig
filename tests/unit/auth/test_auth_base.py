"""Unit tests for the AuthStrategy base class."""

from typing import Dict, Optional
from unittest.mock import Mock

import pytest

from apiconfig.auth.base import AuthStrategy
from apiconfig.types import HttpRequestCallable, QueryParamType, TokenRefreshResult


class ConcreteAuthStrategy(AuthStrategy):
    """Concrete implementation of AuthStrategy for testing."""

    def __init__(self, http_request_callable: Optional[HttpRequestCallable] = None) -> None:
        super().__init__(http_request_callable)

    def prepare_request_headers(self) -> Dict[str, str]:
        """Test implementation."""
        return {"Authorization": "Bearer test-token"}

    def prepare_request_params(self) -> Optional[QueryParamType]:
        """Test implementation."""
        return None


class RefreshableAuthStrategy(AuthStrategy):
    """Concrete implementation that supports refresh for testing."""

    def __init__(self, http_request_callable: Optional[HttpRequestCallable] = None) -> None:
        super().__init__(http_request_callable)
        self._can_refresh = True

    def prepare_request_headers(self) -> Dict[str, str]:
        """Test implementation."""
        return {"Authorization": "Bearer test-token"}

    def prepare_request_params(self) -> Optional[QueryParamType]:
        """Test implementation."""
        return None

    def can_refresh(self) -> bool:
        """Override to return True for testing."""
        return self._can_refresh and self._http_request_callable is not None

    def refresh(self) -> Optional[TokenRefreshResult]:
        """Override with test implementation."""
        if not self.can_refresh():
            raise NotImplementedError("This auth strategy does not support refresh")
        return {
            "token_data": {
                "access_token": "new-token",
                "expires_in": 3600,
            }
        }


class TestAuthStrategy:
    """Test cases for the AuthStrategy base class."""

    def test_init_without_http_request_callable(self) -> None:
        """Test initialization without http_request_callable."""
        strategy = ConcreteAuthStrategy()
        assert strategy._http_request_callable is None  # pyright: ignore[reportPrivateUsage]

    def test_init_with_http_request_callable(self) -> None:
        """Test initialization with http_request_callable."""
        mock_callable = Mock()
        strategy = ConcreteAuthStrategy(http_request_callable=mock_callable)
        assert strategy._http_request_callable is mock_callable  # pyright: ignore[reportPrivateUsage]

    def test_can_refresh_default_implementation(self) -> None:
        """Test that can_refresh returns False by default."""
        strategy = ConcreteAuthStrategy()
        assert strategy.can_refresh() is False

    def test_refresh_default_implementation_raises_not_implemented(self) -> None:
        """Test that refresh raises NotImplementedError by default."""
        strategy = ConcreteAuthStrategy()
        with pytest.raises(NotImplementedError, match="This auth strategy does not support refresh"):
            strategy.refresh()

    def test_is_expired_default_implementation(self) -> None:
        """Test that is_expired returns False by default."""
        strategy = ConcreteAuthStrategy()
        assert strategy.is_expired() is False

    def test_get_refresh_callback_returns_none_when_cannot_refresh(self) -> None:
        """Test that get_refresh_callback returns None when can_refresh is False."""
        strategy = ConcreteAuthStrategy()
        callback = strategy.get_refresh_callback()
        assert callback is None

    def test_get_refresh_callback_returns_callable_when_can_refresh(self) -> None:
        """Test that get_refresh_callback returns a callable when can_refresh is True."""
        mock_callable = Mock()
        strategy = RefreshableAuthStrategy(http_request_callable=mock_callable)
        callback = strategy.get_refresh_callback()

        assert callback is not None
        assert callable(callback)

    def test_get_refresh_callback_calls_refresh_when_invoked(self) -> None:
        """Test that the callback returned by get_refresh_callback calls refresh."""
        mock_callable = Mock()
        strategy = RefreshableAuthStrategy(http_request_callable=mock_callable)

        # Create a mock for the refresh method
        refresh_mock = Mock(
            return_value={
                "token_data": {
                    "access_token": "new-token",
                    "expires_in": 3600,
                }
            }
        )

        # Replace the refresh method with our mock
        original_refresh = strategy.refresh
        strategy.refresh = refresh_mock  # type: ignore

        callback = strategy.get_refresh_callback()
        assert callback is not None

        # Call the callback
        callback()

        # Verify refresh was called
        refresh_mock.assert_called_once()

        # Restore original method
        strategy.refresh = original_refresh  # type: ignore

    def test_refreshable_strategy_can_refresh_with_http_callable(self) -> None:
        """Test that RefreshableAuthStrategy can refresh when http_request_callable is provided."""
        mock_callable = Mock()
        strategy = RefreshableAuthStrategy(http_request_callable=mock_callable)
        assert strategy.can_refresh() is True

    def test_refreshable_strategy_cannot_refresh_without_http_callable(self) -> None:
        """Test that RefreshableAuthStrategy cannot refresh without http_request_callable."""
        strategy = RefreshableAuthStrategy()
        assert strategy.can_refresh() is False

    def test_refreshable_strategy_refresh_returns_token_data(self) -> None:
        """Test that RefreshableAuthStrategy.refresh returns expected token data."""
        mock_callable = Mock()
        strategy = RefreshableAuthStrategy(http_request_callable=mock_callable)

        result = strategy.refresh()

        assert result is not None
        assert "token_data" in result
        token_data = result.get("token_data")
        assert token_data is not None
        assert token_data.get("access_token") == "new-token"
        assert token_data.get("expires_in") == 3600

    def test_refreshable_strategy_refresh_raises_when_cannot_refresh(self) -> None:
        """Test that RefreshableAuthStrategy.refresh raises NotImplementedError when cannot refresh."""
        strategy = RefreshableAuthStrategy()  # No http_request_callable

        with pytest.raises(NotImplementedError, match="This auth strategy does not support refresh"):
            strategy.refresh()
