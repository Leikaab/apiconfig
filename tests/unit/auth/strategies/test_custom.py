"""Tests for the CustomAuth strategy."""

from typing import Dict, Optional
from unittest.mock import Mock

import pytest

import apiconfig.types as api_types
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.exceptions.auth import AuthStrategyError


class TestCustomAuth:
    """Tests for the CustomAuth strategy."""

    def test_init_requires_at_least_one_callback(self) -> None:
        """Test that CustomAuth requires at least one callback."""
        # Should raise when both callbacks are None
        with pytest.raises(AuthStrategyError, match="At least one callback"):
            CustomAuth(header_callback=None, param_callback=None)

        # Should not raise when header_callback is provided
        CustomAuth(header_callback=lambda: {})

        # Should not raise when param_callback is provided
        CustomAuth(param_callback=lambda: {})

        # Should not raise when both callbacks are provided
        CustomAuth(header_callback=lambda: {}, param_callback=lambda: {})

    def test_init_with_refresh_functions(self) -> None:
        """Test initialization with refresh-related functions."""
        refresh_func = Mock(return_value={"token_data": {"access_token": "new_token"}})
        can_refresh_func = Mock(return_value=True)
        is_expired_func = Mock(return_value=False)
        http_request_callable = Mock()

        auth = CustomAuth(
            header_callback=lambda: {"Authorization": "Bearer token"},
            refresh_func=refresh_func,
            can_refresh_func=can_refresh_func,
            is_expired_func=is_expired_func,
            http_request_callable=http_request_callable,
        )

        assert auth.refresh_func is refresh_func
        assert auth.can_refresh_func is can_refresh_func
        assert auth.is_expired_func is is_expired_func
        assert auth._http_request_callable is http_request_callable  # pyright: ignore[reportPrivateUsage]

    def test_can_refresh_with_can_refresh_func(self) -> None:
        """Test can_refresh when can_refresh_func is provided."""
        can_refresh_func = Mock(return_value=True)
        auth = CustomAuth(
            header_callback=lambda: {},
            can_refresh_func=can_refresh_func,
        )

        result = auth.can_refresh()
        assert result is True
        can_refresh_func.assert_called_once()

    def test_can_refresh_without_can_refresh_func_with_refresh_func(self) -> None:
        """Test can_refresh when only refresh_func is provided."""
        refresh_func = Mock()
        auth = CustomAuth(
            header_callback=lambda: {},
            refresh_func=refresh_func,
        )

        result = auth.can_refresh()
        assert result is True

    def test_can_refresh_without_refresh_functions(self) -> None:
        """Test can_refresh when no refresh functions are provided."""
        auth = CustomAuth(header_callback=lambda: {})

        result = auth.can_refresh()
        assert result is False

    def test_is_expired_with_is_expired_func(self) -> None:
        """Test is_expired when is_expired_func is provided."""
        is_expired_func = Mock(return_value=True)
        auth = CustomAuth(
            header_callback=lambda: {},
            is_expired_func=is_expired_func,
        )

        result = auth.is_expired()
        assert result is True
        is_expired_func.assert_called_once()

    def test_is_expired_without_is_expired_func(self) -> None:
        """Test is_expired when no is_expired_func is provided."""
        auth = CustomAuth(header_callback=lambda: {})

        result = auth.is_expired()
        assert result is False

    def test_refresh_with_refresh_func(self) -> None:
        """Test refresh when refresh_func is provided."""
        expected_result = {
            "token_data": {"access_token": "new_token"},
            "config_updates": None,
        }
        refresh_func = Mock(return_value=expected_result)
        auth = CustomAuth(
            header_callback=lambda: {},
            refresh_func=refresh_func,
        )

        result = auth.refresh()
        assert result == expected_result
        refresh_func.assert_called_once()

    def test_refresh_without_refresh_func(self) -> None:
        """Test refresh when no refresh_func is provided."""
        auth = CustomAuth(header_callback=lambda: {})

        with pytest.raises(AuthStrategyError, match="no refresh function configured"):
            auth.refresh()

    def test_refresh_with_failing_refresh_func(self) -> None:
        """Test refresh when refresh_func raises an exception."""
        refresh_func = Mock(side_effect=ValueError("Refresh failed"))
        auth = CustomAuth(
            header_callback=lambda: {},
            refresh_func=refresh_func,
        )

        with pytest.raises(AuthStrategyError, match="Custom auth refresh failed"):
            auth.refresh()

    def test_prepare_request_headers_with_valid_callback(self) -> None:
        """Test prepare_request_headers with a valid callback."""

        # Define a header callback that returns a valid dictionary
        def header_callback() -> Dict[str, str]:
            return {"X-Custom-Header": "test_value"}

        auth = CustomAuth(header_callback=header_callback)
        headers = auth.prepare_request_headers()

        assert headers == {"X-Custom-Header": "test_value"}

    def test_prepare_request_headers_with_invalid_callback_return(self) -> None:
        """Test prepare_request_headers with a callback that returns a non-dict."""

        # Define a header callback that returns a non-dict value
        def invalid_header_callback() -> str:
            return "not_a_dict"

        auth = CustomAuth(header_callback=invalid_header_callback)  # type: ignore[arg-type]

        with pytest.raises(AuthStrategyError, match="header callback failed"):
            auth.prepare_request_headers()

    def test_prepare_request_headers_with_raising_callback(self) -> None:
        """Test prepare_request_headers with a callback that raises an exception."""

        # Define a header callback that raises an exception
        def raising_header_callback() -> None:
            raise ValueError("Test error")

        auth = CustomAuth(header_callback=raising_header_callback)  # type: ignore[arg-type]

        with pytest.raises(AuthStrategyError, match="header callback failed"):
            auth.prepare_request_headers()

    def test_prepare_request_headers_with_no_callback(self) -> None:
        """Test prepare_request_headers with no header callback."""
        # Create CustomAuth with only param_callback
        auth = CustomAuth(param_callback=lambda: {})

        # Should return empty dict when no header_callback is provided
        assert auth.prepare_request_headers() == {}

    def test_prepare_request_params_with_valid_callback(self) -> None:
        """Test prepare_request_params with a valid callback."""

        # Define a param callback that returns a valid dictionary
        def param_callback() -> Dict[str, str]:
            return {"custom_param": "test_value"}

        auth = CustomAuth(param_callback=param_callback)
        params = auth.prepare_request_params()

        assert params == {"custom_param": "test_value"}

    def test_prepare_request_params_with_invalid_callback_return(self) -> None:
        """Test prepare_request_params with a callback that returns a non-dict."""

        # Define a param callback that returns a non-dict value
        def invalid_param_callback() -> str:
            return "not_a_dict"

        auth = CustomAuth(param_callback=invalid_param_callback)  # type: ignore[arg-type]

        with pytest.raises(AuthStrategyError, match="parameter callback failed"):
            auth.prepare_request_params()

    def test_prepare_request_params_with_raising_callback(self) -> None:
        """Test prepare_request_params with a callback that raises an exception."""

        # Define a param callback that raises an exception
        def raising_param_callback() -> None:
            raise ValueError("Test error")

        auth = CustomAuth(param_callback=raising_param_callback)  # type: ignore[arg-type]

        with pytest.raises(AuthStrategyError, match="parameter callback failed"):
            auth.prepare_request_params()

    def test_prepare_request_params_with_no_callback(self) -> None:
        """Test prepare_request_params with no param callback."""
        # Create CustomAuth with only header_callback
        auth = CustomAuth(header_callback=lambda: {})

        # Should return empty dict when no param_callback is provided
        assert auth.prepare_request_params() == {}

    def test_prepare_request_with_both_callbacks(self) -> None:
        """Test prepare_request with both callbacks."""

        def header_callback() -> Dict[str, str]:
            return {"X-Custom-Header": "header_value"}

        def param_callback() -> Dict[str, str]:
            return {"custom_param": "param_value"}

        auth = CustomAuth(header_callback=header_callback, param_callback=param_callback)

        headers, params = auth.prepare_request()

        assert headers == {"X-Custom-Header": "header_value"}
        assert params == {"custom_param": "param_value"}

    def test_prepare_request_merges_with_provided_values(self) -> None:
        """Test prepare_request merges with provided headers and params."""

        def header_callback() -> Dict[str, str]:
            return {"X-Custom-Header": "header_value"}

        def param_callback() -> Dict[str, str]:
            return {"custom_param": "param_value"}

        auth = CustomAuth(header_callback=header_callback, param_callback=param_callback)

        # Provide initial headers and params
        initial_headers = {"Content-Type": "application/json"}
        initial_params = {"page": "1"}

        headers, params = auth.prepare_request(headers=initial_headers, params=initial_params)

        # Check that the result contains both initial and callback values
        assert headers == {
            "Content-Type": "application/json",
            "X-Custom-Header": "header_value",
        }
        assert params == {"page": "1", "custom_param": "param_value"}

    def test_backward_compatibility(self) -> None:
        """Test that existing usage patterns still work."""

        # Test the original usage pattern without refresh functionality
        def header_callback() -> Dict[str, str]:
            return {"Authorization": "Bearer old-token"}

        auth = CustomAuth(header_callback=header_callback)

        # Should work as before
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Bearer old-token"}

        # Refresh methods should have default behavior
        assert auth.can_refresh() is False
        assert auth.is_expired() is False

        with pytest.raises(AuthStrategyError, match="no refresh function configured"):
            auth.refresh()


class TestCustomAuthFactoryMethods:
    """Tests for CustomAuth factory methods."""

    def test_create_api_key_custom(self) -> None:
        """Test create_api_key_custom factory method."""
        auth = CustomAuth.create_api_key_custom(api_key="test-key-123", header_name="X-API-Key")

        # Test that headers are set correctly
        headers = auth.prepare_request_headers()
        assert headers == {"X-API-Key": "test-key-123"}

        # Test that params are empty
        params = auth.prepare_request_params()
        assert params == {}

        # Test that refresh is not supported by default
        assert auth.can_refresh() is False

    def test_create_api_key_custom_with_custom_header_name(self) -> None:
        """Test create_api_key_custom with custom header name."""
        auth = CustomAuth.create_api_key_custom(api_key="secret-key", header_name="X-Custom-API-Key")

        headers = auth.prepare_request_headers()
        assert headers == {"X-Custom-API-Key": "secret-key"}

    def test_create_api_key_custom_with_http_request_callable(self) -> None:
        """Test create_api_key_custom with http_request_callable."""
        http_callable = Mock()
        auth = CustomAuth.create_api_key_custom(api_key="test-key", http_request_callable=http_callable)

        assert auth._http_request_callable is http_callable  # pyright: ignore[reportPrivateUsage]

    def test_create_session_token_custom(self) -> None:
        """Test create_session_token_custom factory method."""
        refresh_call_count = 0

        def mock_refresh_func() -> str:
            nonlocal refresh_call_count
            refresh_call_count += 1
            return f"refreshed-token-{refresh_call_count}"

        auth = CustomAuth.create_session_token_custom(
            session_token="initial-token", session_refresh_func=mock_refresh_func, header_name="Authorization", token_prefix="Session"
        )

        # Test initial headers
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Session initial-token"}

        # Test that refresh is supported
        assert auth.can_refresh() is True

        # Test refresh functionality
        result = auth.refresh()
        assert result is not None
        token_data = result.get("token_data")
        assert token_data is not None
        assert token_data.get("access_token") == "refreshed-token-1"
        assert token_data.get("token_type") == "session"
        assert result.get("config_updates") is None

        # Test that headers are updated after refresh
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Session refreshed-token-1"}

        # Test multiple refreshes
        auth.refresh()
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Session refreshed-token-2"}

    def test_create_session_token_custom_with_custom_settings(self) -> None:
        """Test create_session_token_custom with custom header name and prefix."""

        def mock_refresh_func() -> str:
            return "new-session-token"

        auth = CustomAuth.create_session_token_custom(
            session_token="initial-session", session_refresh_func=mock_refresh_func, header_name="X-Session-Token", token_prefix="Custom"
        )

        headers = auth.prepare_request_headers()
        assert headers == {"X-Session-Token": "Custom initial-session"}

        auth.refresh()
        headers = auth.prepare_request_headers()
        assert headers == {"X-Session-Token": "Custom new-session-token"}

    def test_create_session_token_custom_with_http_request_callable(self) -> None:
        """Test create_session_token_custom with http_request_callable."""
        http_callable = Mock()

        def mock_refresh_func() -> str:
            return "refreshed-token"

        auth = CustomAuth.create_session_token_custom(
            session_token="initial-token", session_refresh_func=mock_refresh_func, http_request_callable=http_callable
        )

        assert auth._http_request_callable is http_callable  # pyright: ignore[reportPrivateUsage]

    def test_factory_methods_return_correct_type(self) -> None:
        """Test that factory methods return CustomAuth instances."""
        api_key_auth = CustomAuth.create_api_key_custom("key")
        assert isinstance(api_key_auth, CustomAuth)

        session_auth = CustomAuth.create_session_token_custom("token", lambda: "new-token")
        assert isinstance(session_auth, CustomAuth)


class TestCustomAuthRefreshIntegration:
    """Integration tests for CustomAuth refresh functionality."""

    def test_custom_refresh_with_state_management(self) -> None:
        """Test custom refresh with proper state management."""
        # Simulate a token that expires and needs refresh
        token_state = {
            "access_token": "initial-token",
            "expires_at": 1000,
            "current_time": 500,
        }

        def header_callback() -> Dict[str, str]:
            return {"Authorization": f"Bearer {token_state['access_token']}"}

        def is_expired_callback() -> bool:
            current_time = token_state["current_time"]
            expires_at = token_state["expires_at"]
            assert isinstance(current_time, int)
            assert isinstance(expires_at, int)
            return current_time >= expires_at

        def refresh_callback() -> Optional[api_types.TokenRefreshResult]:
            # Simulate getting a new token
            token_state["access_token"] = "refreshed-token"
            current_time = token_state["current_time"]
            assert isinstance(current_time, int)
            token_state["expires_at"] = current_time + 1000
            access_token = token_state["access_token"]
            assert isinstance(access_token, str)
            return {
                "token_data": {
                    "access_token": access_token,
                    "expires_in": 1000,
                },
                "config_updates": None,
            }

        auth = CustomAuth(
            header_callback=header_callback,
            is_expired_func=is_expired_callback,
            refresh_func=refresh_callback,
            can_refresh_func=lambda: True,
        )

        # Initially not expired
        assert not auth.is_expired()
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Bearer initial-token"}

        # Simulate time passing and token expiring
        token_state["current_time"] = 1001
        assert auth.is_expired()

        # Refresh the token
        result = auth.refresh()
        assert result is not None
        token_data = result.get("token_data")
        assert token_data is not None
        assert token_data.get("access_token") == "refreshed-token"

        # Token should no longer be expired and headers should be updated
        assert not auth.is_expired()
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Bearer refreshed-token"}

    def test_custom_refresh_error_handling(self) -> None:
        """Test error handling in custom refresh scenarios."""

        def failing_refresh() -> Optional[api_types.TokenRefreshResult]:
            raise ConnectionError("Network error during refresh")

        auth = CustomAuth(
            header_callback=lambda: {"Authorization": "Bearer token"},
            refresh_func=failing_refresh,
        )

        with pytest.raises(AuthStrategyError, match="Custom auth refresh failed"):
            auth.refresh()
