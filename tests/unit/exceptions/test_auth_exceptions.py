"""Unit tests for authentication exception classes."""

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
from apiconfig.types import HttpRequestContext, HttpResponseContext


class TestAuthenticationError:
    """Test cases for the base AuthenticationError class."""

    def test_basic_initialization(self) -> None:
        """Test basic initialization without context."""
        error = AuthenticationError("Test error message")
        assert str(error) == "Test error message"
        assert error.request_context is None
        assert error.response_context is None

    def test_initialization_with_request_context(self) -> None:
        """Test initialization with request context."""
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/token",
        }
        error = AuthenticationError("Test error", request_context=request_context)
        assert error.request_context == request_context
        assert error.response_context is None

    def test_initialization_with_response_context(self) -> None:
        """Test initialization with response context."""
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Unauthorized",
        }
        error = AuthenticationError("Test error", response_context=response_context)
        assert error.request_context is None
        assert error.response_context == response_context

    def test_initialization_with_both_contexts(self) -> None:
        """Test initialization with both request and response contexts."""
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/token",
        }
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Unauthorized",
        }
        error = AuthenticationError(
            "Test error",
            request_context=request_context,
            response_context=response_context,
        )
        assert error.request_context == request_context
        assert error.response_context == response_context

    def test_str_without_context(self) -> None:
        """Test string representation without context."""
        error = AuthenticationError("Simple error message")
        assert str(error) == "Simple error message"

    def test_str_with_request_context_only(self) -> None:
        """Test string representation with request context only."""
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/token",
        }
        error = AuthenticationError("Auth failed", request_context=request_context)
        expected = "Auth failed (Request: POST https://api.example.com/token)"
        assert str(error) == expected

    def test_str_with_response_context_only(self) -> None:
        """Test string representation with response context only."""
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Unauthorized",
        }
        error = AuthenticationError("Auth failed", response_context=response_context)
        expected = "Auth failed (Response: 401 Unauthorized)"
        assert str(error) == expected

    def test_str_with_both_contexts(self) -> None:
        """Test string representation with both contexts."""
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/token",
        }
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Unauthorized",
        }
        error = AuthenticationError(
            "Auth failed",
            request_context=request_context,
            response_context=response_context,
        )
        expected = "Auth failed (Request: POST https://api.example.com/token, Response: 401 Unauthorized)"
        assert str(error) == expected

    def test_str_with_partial_request_context(self) -> None:
        """Test string representation with partial request context."""
        request_context: HttpRequestContext = {
            "method": "POST",
            # Missing URL
        }
        error = AuthenticationError("Auth failed", request_context=request_context)
        expected = "Auth failed (Request: POST UNKNOWN)"
        assert str(error) == expected

    def test_str_with_partial_response_context(self) -> None:
        """Test string representation with partial response context."""
        response_context: HttpResponseContext = {
            "status_code": 401,
            # Missing reason
        }
        error = AuthenticationError("Auth failed", response_context=response_context)
        expected = "Auth failed (Response: 401)"
        assert str(error) == expected

    def test_str_with_empty_contexts(self) -> None:
        """Test string representation with empty contexts."""
        request_context: HttpRequestContext = {}
        response_context: HttpResponseContext = {}
        error = AuthenticationError(
            "Auth failed",
            request_context=request_context,
            response_context=response_context,
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
        request_context: HttpRequestContext = {
            "method": "GET",
            "url": "https://api.example.com/data",
        }
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Token Expired",
        }
        error = ExpiredTokenError(
            request_context=request_context,
            response_context=response_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/oauth/token",
        }
        response_context: HttpResponseContext = {
            "status_code": 400,
            "reason": "Bad Request",
        }
        error = TokenRefreshError(
            request_context=request_context,
            response_context=response_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/auth",
        }
        response_context: HttpResponseContext = {
            "status_code": 500,
            "reason": "Internal Server Error",
        }
        error = AuthStrategyError(
            request_context=request_context,
            response_context=response_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/login",
        }
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Unauthorized",
        }
        error = InvalidCredentialsError(
            request_context=request_context,
            response_context=response_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "GET",
            "url": "https://api.example.com/protected",
        }
        response_context: HttpResponseContext = {
            "status_code": 401,
            "reason": "Unauthorized",
        }
        error = MissingCredentialsError(
            request_context=request_context,
            response_context=response_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/oauth/token",
        }
        response_context: HttpResponseContext = {
            "status_code": 200,
            "reason": "OK",
        }
        error = TokenRefreshJsonError(
            request_context=request_context,
            response_context=response_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/oauth/token",
        }
        error = TokenRefreshTimeoutError(
            request_context=request_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": "https://api.example.com/oauth/token",
        }
        error = TokenRefreshNetworkError(
            request_context=request_context,
        )
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
        request_context: HttpRequestContext = {
            "method": "POST",
            "url": None,  # type: ignore
        }
        response_context: HttpResponseContext = {
            "status_code": None,  # type: ignore
            "reason": "OK",
        }
        error = AuthenticationError(
            "Test error",
            request_context=request_context,
            response_context=response_context,
        )
        # Should handle None gracefully
        result = str(error)
        assert "Test error" in result

    def test_missing_keys_in_context(self) -> None:
        """Test handling when expected keys are missing from context."""
        request_context: HttpRequestContext = {}  # Empty context
        response_context: HttpResponseContext = {}  # Empty context
        error = AuthenticationError(
            "Test error",
            request_context=request_context,
            response_context=response_context,
        )
        # Empty contexts should not add context information
        expected = "Test error"
        assert str(error) == expected

    def test_context_with_unknown_values(self) -> None:
        """Test handling when context has keys but with None/missing values."""
        request_context: HttpRequestContext = {
            "method": "POST",
            # Missing URL - should show UNKNOWN
        }
        response_context: HttpResponseContext = {
            "status_code": 401,
            # Missing reason - should show just status code
        }
        error = AuthenticationError(
            "Test error",
            request_context=request_context,
            response_context=response_context,
        )
        expected = "Test error (Request: POST UNKNOWN, Response: 401)"
        assert str(error) == expected

    def test_extra_keys_in_context(self) -> None:
        """Test that extra keys in context don't break functionality."""
        request_context = {
            "method": "POST",
            "url": "https://api.example.com/token",
            "extra_field": "should_be_ignored",
        }
        response_context = {
            "status_code": 401,
            "reason": "Unauthorized",
            "extra_field": "should_be_ignored",
        }
        error = AuthenticationError(
            "Test error",
            request_context=request_context,  # type: ignore
            response_context=response_context,  # type: ignore
        )
        expected = "Test error (Request: POST https://api.example.com/token, Response: 401 Unauthorized)"
        assert str(error) == expected
