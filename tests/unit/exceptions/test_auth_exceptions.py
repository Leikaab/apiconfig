"""Unit tests for authentication exception classes."""

from unittest.mock import Mock

import pytest

from apiconfig.exceptions.auth import (
    AuthenticationError,
    AuthStrategyError,
    ExpiredTokenError,
    InvalidCredentialsError,
    MissingCredentialsError,
    TokenRefreshError,
    TokenRefreshJsonError,
    TokenRefreshNetworkError,
    TokenRefreshTimeoutError,
)


class TestAuthenticationError:
    """Test cases for the base AuthenticationError class."""

    def test_basic_initialization(self) -> None:
        """Test basic initialization without context."""
        error = AuthenticationError("Test error message")
        assert str(error) == "Test error message"
        assert error.request is None
        assert error.response is None
        assert error.method is None
        assert error.url is None
        assert error.status_code is None
        assert error.reason is None

    def test_initialization_with_request_object(self) -> None:
        """Test initialization with request object."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/token"

        error = AuthenticationError("Test error", request=request)
        assert error.request is request
        assert error.response is None
        assert error.method == "POST"
        assert error.url == "https://api.example.com/token"

    def test_initialization_with_response_object(self) -> None:
        """Test initialization with response object."""
        response = Mock(spec=["status_code", "reason", "headers", "text"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""

        error = AuthenticationError("Test error", response=response)
        assert error.request is None
        assert error.response is response
        assert error.status_code == 401
        assert error.reason == "Unauthorized"

    def test_initialization_with_both_objects(self) -> None:
        """Test initialization with both request and response objects."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/token"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""
        response.request = request

        error = AuthenticationError("Test error", response=response)
        assert error.request is request
        assert error.response is response
        assert error.method == "POST"
        assert error.url == "https://api.example.com/token"
        assert error.status_code == 401
        assert error.reason == "Unauthorized"

    def test_str_without_context(self) -> None:
        """Test string representation without context."""
        error = AuthenticationError("Simple error message")
        assert str(error) == "Simple error message"

    def test_str_with_request_context_only(self) -> None:
        """Test string representation with request context only."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/token"

        error = AuthenticationError("Auth failed", request=request)
        expected = "Auth failed (Request: POST https://api.example.com/token)"
        assert str(error) == expected

    def test_str_with_response_context_only(self) -> None:
        """Test string representation with response context only."""
        response = Mock(spec=["status_code", "reason", "headers", "text"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""

        error = AuthenticationError("Auth failed", response=response)
        expected = "Auth failed (Response: 401 Unauthorized)"
        assert str(error) == expected

    def test_str_with_both_contexts(self) -> None:
        """Test string representation with both contexts."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/token"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""
        response.request = request

        error = AuthenticationError("Auth failed", response=response)
        expected = "Auth failed (Request: POST https://api.example.com/token, Response: 401 Unauthorized)"
        assert str(error) == expected

    def test_str_with_partial_request_context(self) -> None:
        """Test string representation with partial request context."""
        request = Mock(spec=["method"])
        request.method = "POST"
        # Missing URL attribute

        error = AuthenticationError("Auth failed", request=request)
        # Should only show "Auth failed" since URL is missing
        assert str(error) == "Auth failed"

    def test_str_with_partial_response_context(self) -> None:
        """Test string representation with partial response context."""
        response = Mock(spec=["status_code", "headers", "text"])
        response.status_code = 401
        response.headers = {}
        response.text = ""
        # Missing reason attribute

        error = AuthenticationError("Auth failed", response=response)
        expected = "Auth failed (Response: 401)"
        assert str(error) == expected

    def test_str_with_empty_contexts(self) -> None:
        """Test string representation with empty contexts."""
        request = Mock(spec=[])  # No attributes
        response = Mock(spec=[])  # No attributes

        error = AuthenticationError(
            "Auth failed",
            request=request,
            response=response,
        )
        # Empty contexts should not add context information
        expected = "Auth failed"
        assert str(error) == expected

    def test_inheritance_from_base_exception(self) -> None:
        """Test that AuthenticationError properly inherits from base exception."""
        error = AuthenticationError("Test error")
        assert isinstance(error, Exception)
        assert hasattr(error, "args")


class TestExpiredTokenError:
    """Test cases for ExpiredTokenError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = ExpiredTokenError()
        assert str(error) == "Authentication token has expired"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = ExpiredTokenError("Custom expiry message")
        assert str(error) == "Custom expiry message"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "GET"
        request.url = "https://api.example.com/data"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 401
        response.reason = "Token Expired"
        response.headers = {}
        response.text = ""
        response.request = request

        error = ExpiredTokenError(response=response)
        expected = "Authentication token has expired (Request: GET https://api.example.com/data, Response: 401 Token Expired)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from AuthenticationError."""
        error = ExpiredTokenError()
        assert isinstance(error, AuthenticationError)


class TestTokenRefreshError:
    """Test cases for TokenRefreshError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = TokenRefreshError()
        assert str(error) == "Failed to refresh authentication token"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = TokenRefreshError("Custom refresh error")
        assert str(error) == "Custom refresh error"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/oauth/token"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 400
        response.reason = "Bad Request"
        response.headers = {}
        response.text = ""
        response.request = request

        error = TokenRefreshError(response=response)
        expected = "Failed to refresh authentication token (Request: POST https://api.example.com/oauth/token, Response: 400 Bad Request)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from AuthenticationError."""
        error = TokenRefreshError()
        assert isinstance(error, AuthenticationError)


class TestAuthStrategyError:
    """Test cases for AuthStrategyError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = AuthStrategyError()
        assert str(error) == "Authentication strategy error"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = AuthStrategyError("Custom strategy error")
        assert str(error) == "Custom strategy error"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/auth"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 500
        response.reason = "Internal Server Error"
        response.headers = {}
        response.text = ""
        response.request = request

        error = AuthStrategyError(response=response)
        expected = "Authentication strategy error (Request: POST https://api.example.com/auth, Response: 500 Internal Server Error)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from AuthenticationError."""
        error = AuthStrategyError()
        assert isinstance(error, AuthenticationError)


class TestInvalidCredentialsError:
    """Test cases for InvalidCredentialsError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = InvalidCredentialsError()
        assert str(error) == "Invalid credentials provided"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = InvalidCredentialsError("Username or password incorrect")
        assert str(error) == "Username or password incorrect"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/login"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""
        response.request = request

        error = InvalidCredentialsError(response=response)
        expected = "Invalid credentials provided (Request: POST https://api.example.com/login, Response: 401 Unauthorized)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from AuthenticationError."""
        error = InvalidCredentialsError()
        assert isinstance(error, AuthenticationError)


class TestMissingCredentialsError:
    """Test cases for MissingCredentialsError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = MissingCredentialsError()
        assert str(error) == "Required credentials not provided"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = MissingCredentialsError("API key is required")
        assert str(error) == "API key is required"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "GET"
        request.url = "https://api.example.com/protected"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""
        response.request = request

        error = MissingCredentialsError(response=response)
        expected = "Required credentials not provided (Request: GET https://api.example.com/protected, Response: 401 Unauthorized)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from AuthenticationError."""
        error = MissingCredentialsError()
        assert isinstance(error, AuthenticationError)


class TestTokenRefreshJsonError:
    """Test cases for TokenRefreshJsonError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = TokenRefreshJsonError()
        assert str(error) == "Failed to decode JSON from token refresh response"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = TokenRefreshJsonError("Invalid JSON in response")
        assert str(error) == "Invalid JSON in response"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/oauth/token"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = 200
        response.reason = "OK"
        response.headers = {}
        response.text = ""
        response.request = request

        error = TokenRefreshJsonError(response=response)
        expected = "Failed to decode JSON from token refresh response (Request: POST https://api.example.com/oauth/token, Response: 200 OK)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from TokenRefreshError and AuthenticationError."""
        error = TokenRefreshJsonError()
        assert isinstance(error, TokenRefreshError)
        assert isinstance(error, AuthenticationError)


class TestTokenRefreshTimeoutError:
    """Test cases for TokenRefreshTimeoutError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = TokenRefreshTimeoutError()
        assert str(error) == "Token refresh request timed out"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = TokenRefreshTimeoutError("Request timeout after 30 seconds")
        assert str(error) == "Request timeout after 30 seconds"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/oauth/token"

        error = TokenRefreshTimeoutError(request=request)
        expected = "Token refresh request timed out (Request: POST https://api.example.com/oauth/token)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from TokenRefreshError and AuthenticationError."""
        error = TokenRefreshTimeoutError()
        assert isinstance(error, TokenRefreshError)
        assert isinstance(error, AuthenticationError)


class TestTokenRefreshNetworkError:
    """Test cases for TokenRefreshNetworkError."""

    def test_default_message(self) -> None:
        """Test default message when none provided."""
        error = TokenRefreshNetworkError()
        assert str(error) == "Token refresh request failed due to network issues"

    def test_custom_message(self) -> None:
        """Test custom message."""
        error = TokenRefreshNetworkError("Connection refused")
        assert str(error) == "Connection refused"

    def test_with_context(self) -> None:
        """Test with HTTP context."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = "https://api.example.com/oauth/token"

        error = TokenRefreshNetworkError(request=request)
        expected = "Token refresh request failed due to network issues (Request: POST https://api.example.com/oauth/token)"
        assert str(error) == expected

    def test_inheritance(self) -> None:
        """Test inheritance from TokenRefreshError and AuthenticationError."""
        error = TokenRefreshNetworkError()
        assert isinstance(error, TokenRefreshError)
        assert isinstance(error, AuthenticationError)


class TestBackwardCompatibility:
    """Test cases to ensure backward compatibility."""

    def test_simple_exception_raising(self) -> None:
        """Test that existing code patterns still work."""
        # These should all work without breaking existing code
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("Simple error")

        with pytest.raises(ExpiredTokenError):
            raise ExpiredTokenError()

        with pytest.raises(TokenRefreshError):
            raise TokenRefreshError("Custom message")

        with pytest.raises(AuthStrategyError):
            raise AuthStrategyError()

    def test_exception_args_and_kwargs(self) -> None:
        """Test that additional args are properly handled."""
        # Test basic message handling
        error = AuthenticationError("Test message")
        assert str(error) == "Test message"
        assert error.args[0] == "Test message"

    def test_exception_with_kwargs_compatibility(self) -> None:
        """Test that the exception works with positional arguments for backward compatibility."""
        # Test that we can pass positional arguments in the old style
        error = AuthenticationError("Test message")
        assert str(error) == "Test message"

        # Test that the exception can be created with just a message (backward compatibility)
        error = AuthenticationError("Simple error")
        assert isinstance(error, AuthenticationError)
        assert str(error) == "Simple error"

    def test_exception_chaining(self) -> None:
        """Test exception chaining works properly."""
        try:
            raise ValueError("Original error")
        except ValueError as e:
            error = AuthenticationError("Wrapped error")
            error.__cause__ = e
            assert error.__cause__ is e


class TestContextEdgeCases:
    """Test edge cases for context handling."""

    def test_none_values_in_context(self) -> None:
        """Test handling of None values in context dictionaries."""
        request = Mock(spec=["method", "url"])
        request.method = "POST"
        request.url = None  # None value

        response = Mock(spec=["status_code", "reason", "headers", "text", "request"])
        response.status_code = None  # None value
        response.reason = "OK"
        response.headers = {}
        response.text = ""
        response.request = request

        error = AuthenticationError("Test error", response=response)
        # Should handle None gracefully
        result = str(error)
        assert "Test error" in result

    def test_missing_keys_in_context(self) -> None:
        """Test handling when expected keys are missing from context."""
        request = Mock(spec=[])  # Empty context - no attributes
        response = Mock(spec=[])  # Empty context - no attributes

        error = AuthenticationError("Test error", request=request, response=response)
        # Empty contexts should not add context information
        expected = "Test error"
        assert str(error) == expected

    def test_context_with_unknown_values(self) -> None:
        """Test handling when context has keys but with None/missing values."""
        request = Mock(spec=["method"])  # Has method but no url
        request.method = "POST"

        response = Mock(spec=["status_code", "headers", "text"])  # Has status_code but no reason
        response.status_code = 401
        response.headers = {}
        response.text = ""

        error = AuthenticationError("Test error", request=request, response=response)
        # With new implementation, partial context is not shown if incomplete
        expected = "Test error (Response: 401)"
        assert str(error) == expected

    def test_extra_keys_in_context(self) -> None:
        """Test that extra keys in context don't break functionality."""
        request = Mock(spec=["method", "url", "extra_field"])
        request.method = "POST"
        request.url = "https://api.example.com/token"
        request.extra_field = "should_be_ignored"

        response = Mock(spec=["status_code", "reason", "headers", "text", "request", "extra_field"])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""
        response.request = request
        response.extra_field = "should_be_ignored"

        error = AuthenticationError("Test error", response=response)
        expected = "Test error (Request: POST https://api.example.com/token, Response: 401 Unauthorized)"
        assert str(error) == expected
