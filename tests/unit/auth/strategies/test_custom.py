"""Tests for the CustomAuth strategy."""

import pytest

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

    def test_prepare_request_headers_with_valid_callback(self) -> None:
        """Test prepare_request_headers with a valid callback."""
        # Define a header callback that returns a valid dictionary
        def header_callback():
            return {"X-Custom-Header": "test_value"}

        auth = CustomAuth(header_callback=header_callback)
        headers = auth.prepare_request_headers()

        assert headers == {"X-Custom-Header": "test_value"}

    def test_prepare_request_headers_with_invalid_callback_return(self) -> None:
        """Test prepare_request_headers with a callback that returns a non-dict."""
        # Define a header callback that returns a non-dict value
        def invalid_header_callback():
            return "not_a_dict"

        auth = CustomAuth(header_callback=invalid_header_callback)

        with pytest.raises(AuthStrategyError, match="must return a dictionary"):
            auth.prepare_request_headers()

    def test_prepare_request_headers_with_raising_callback(self) -> None:
        """Test prepare_request_headers with a callback that raises an exception."""
        # Define a header callback that raises an exception
        def raising_header_callback():
            raise ValueError("Test error")

        auth = CustomAuth(header_callback=raising_header_callback)

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
        def param_callback():
            return {"custom_param": "test_value"}

        auth = CustomAuth(param_callback=param_callback)
        params = auth.prepare_request_params()

        assert params == {"custom_param": "test_value"}

    def test_prepare_request_params_with_invalid_callback_return(self) -> None:
        """Test prepare_request_params with a callback that returns a non-dict."""
        # Define a param callback that returns a non-dict value
        def invalid_param_callback():
            return "not_a_dict"

        auth = CustomAuth(param_callback=invalid_param_callback)

        with pytest.raises(AuthStrategyError, match="must return a dictionary"):
            auth.prepare_request_params()

    def test_prepare_request_params_with_raising_callback(self) -> None:
        """Test prepare_request_params with a callback that raises an exception."""
        # Define a param callback that raises an exception
        def raising_param_callback():
            raise ValueError("Test error")

        auth = CustomAuth(param_callback=raising_param_callback)

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
        def header_callback():
            return {"X-Custom-Header": "header_value"}

        def param_callback():
            return {"custom_param": "param_value"}

        auth = CustomAuth(
            header_callback=header_callback,
            param_callback=param_callback
        )

        headers, params = auth.prepare_request()

        assert headers == {"X-Custom-Header": "header_value"}
        assert params == {"custom_param": "param_value"}

    def test_prepare_request_merges_with_provided_values(self) -> None:
        """Test prepare_request merges with provided headers and params."""
        def header_callback():
            return {"X-Custom-Header": "header_value"}

        def param_callback():
            return {"custom_param": "param_value"}

        auth = CustomAuth(
            header_callback=header_callback,
            param_callback=param_callback
        )

        # Provide initial headers and params
        initial_headers = {"Content-Type": "application/json"}
        initial_params = {"page": "1"}

        headers, params = auth.prepare_request(
            headers=initial_headers,
            params=initial_params
        )

        # Check that the result contains both initial and callback values
        assert headers == {
            "Content-Type": "application/json",
            "X-Custom-Header": "header_value"
        }
        assert params == {
            "page": "1",
            "custom_param": "param_value"
        }
