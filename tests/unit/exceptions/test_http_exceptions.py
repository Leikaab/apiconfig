"""Unit tests for HTTP exception classes."""

from unittest.mock import Mock

from apiconfig.exceptions.base import APIConfigError, AuthenticationError
from apiconfig.exceptions.http import (
    ApiClientBadRequestError,
    ApiClientConflictError,
    ApiClientError,
    ApiClientForbiddenError,
    ApiClientInternalServerError,
    ApiClientNotFoundError,
    ApiClientRateLimitError,
    ApiClientUnauthorizedError,
    ApiClientUnprocessableEntityError,
    create_api_client_error,
)


class TestApiClientError:
    """Test cases for the base ApiClientError class."""

    def test_basic_initialization(self) -> None:
        """Test basic initialization without context."""
        error = ApiClientError("Test error")
        assert str(error) == "Test error"
        assert error.status_code is None
        assert error.request is None
        assert error.response is None
        assert error.method is None
        assert error.url is None
        assert error.reason is None

    def test_initialization_with_status_code(self) -> None:
        """Test initialization with status code."""
        error = ApiClientError("Test error", status_code=500)
        assert str(error) == "Test error (HTTP 500)"
        assert error.status_code == 500

    def test_initialization_with_request_object(self) -> None:
        """Test initialization with request object."""
        request = Mock(spec=['method', 'url'])
        request.method = "GET"
        request.url = "https://api.example.com/users"

        error = ApiClientError("Test error", request=request)
        assert str(error) == "Test error (GET https://api.example.com/users)"
        assert error.request is request
        assert error.method == "GET"
        assert error.url == "https://api.example.com/users"

    def test_initialization_with_full_context(self) -> None:
        """Test initialization with both status code and request object."""
        request = Mock(spec=['method', 'url'])
        request.method = "POST"
        request.url = "https://api.example.com/users"

        error = ApiClientError("Test error", status_code=400, request=request)
        assert str(error) == "Test error (HTTP 400, POST https://api.example.com/users)"
        assert error.status_code == 400
        assert error.method == "POST"
        assert error.url == "https://api.example.com/users"

    def test_initialization_with_response_object(self) -> None:
        """Test initialization with response object that includes request."""
        # Create mock request
        request = Mock(spec=['method', 'url'])
        request.method = "DELETE"
        request.url = "https://api.example.com/item/123"

        # Create mock response with request
        response = Mock(spec=['status_code', 'reason', 'request', 'headers', 'text'])
        response.status_code = 404
        response.reason = "Not Found"
        response.request = request
        response.headers = {}
        response.text = ""

        error = ApiClientError("Resource not found", response=response)
        assert str(error) == "Resource not found (HTTP 404, DELETE https://api.example.com/item/123)"
        assert error.response is response
        assert error.request is request
        assert error.status_code == 404
        assert error.reason == "Not Found"
        assert error.method == "DELETE"
        assert error.url == "https://api.example.com/item/123"

    def test_str_with_partial_request_object(self) -> None:
        """Test string representation with partial request object."""
        # Only method
        request = Mock(spec=['method'])
        request.method = "GET"

        error = ApiClientError("Test error", request=request)
        assert str(error) == "Test error"  # URL is missing, so no context shown
        assert error.method == "GET"
        assert error.url is None

        # Only URL
        request = Mock(spec=['url'])
        request.url = "https://api.example.com/users"

        error = ApiClientError("Test error", request=request)
        assert str(error) == "Test error"  # Method is missing, so no context shown
        assert error.method is None
        assert error.url == "https://api.example.com/users"

    def test_str_with_empty_request_object(self) -> None:
        """Test string representation with empty request object."""
        request = Mock(spec=[])  # No attributes
        error = ApiClientError("Test error", request=request)
        assert str(error) == "Test error"
        assert error.method is None
        assert error.url is None

    def test_inheritance(self) -> None:
        """Test that ApiClientError inherits from APIConfigError."""
        error = ApiClientError("Test error")
        assert isinstance(error, APIConfigError)
        assert isinstance(error, Exception)


class TestApiClientBadRequestError:
    """Test cases for ApiClientBadRequestError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientBadRequestError()
        assert str(error) == "Bad Request (HTTP 400)"
        assert error.status_code == 400

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientBadRequestError("Invalid input data")
        assert str(error) == "Invalid input data (HTTP 400)"
        assert error.status_code == 400

    def test_with_context(self) -> None:
        """Test initialization with context."""
        request = Mock(spec=['method', 'url'])
        request.method = "POST"
        request.url = "https://api.example.com/users"

        error = ApiClientBadRequestError("Invalid input", request=request)
        assert str(error) == "Invalid input (HTTP 400, POST https://api.example.com/users)"
        assert error.request is request
        assert error.method == "POST"
        assert error.url == "https://api.example.com/users"

    def test_inheritance(self) -> None:
        """Test inheritance hierarchy."""
        error = ApiClientBadRequestError()
        assert isinstance(error, ApiClientError)
        assert isinstance(error, APIConfigError)


class TestApiClientUnauthorizedError:
    """Test cases for ApiClientUnauthorizedError with multiple inheritance."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientUnauthorizedError()
        assert str(error) == "Unauthorized (HTTP 401)"
        assert error.status_code == 401

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientUnauthorizedError("Invalid token")
        assert str(error) == "Invalid token (HTTP 401)"

    def test_multiple_inheritance(self) -> None:
        """Test that the class inherits from both ApiClientError and AuthenticationError."""
        error = ApiClientUnauthorizedError()
        assert isinstance(error, ApiClientError)
        assert isinstance(error, AuthenticationError)
        assert isinstance(error, APIConfigError)

    def test_with_context(self) -> None:
        """Test initialization with context."""
        request = Mock(spec=['method', 'url'])
        request.method = "GET"
        request.url = "https://api.example.com/protected"

        response = Mock(spec=['status_code', 'reason', 'headers', 'text', 'request'])
        response.status_code = 401
        response.reason = "Unauthorized"
        response.headers = {}
        response.text = ""
        response.request = request  # Link the request to the response

        error = ApiClientUnauthorizedError("Token expired", response=response)
        assert str(error) == "Token expired (HTTP 401, GET https://api.example.com/protected)"
        assert error.request is request
        assert error.response is response
        assert error.method == "GET"
        assert error.url == "https://api.example.com/protected"
        assert error.status_code == 401
        assert error.reason == "Unauthorized"

    def test_both_parent_init_called(self) -> None:
        """Test that both parent __init__ methods are called properly."""
        request = Mock(spec=['method', 'url'])
        request.method = "GET"
        request.url = "https://api.example.com/test"

        error = ApiClientUnauthorizedError("Test", request=request)

        # Should have ApiClientError attributes
        assert error.status_code == 401
        assert error.request is request
        assert error.method == "GET"
        assert error.url == "https://api.example.com/test"

        # Should also have attributes from HttpContextMixin
        assert hasattr(error, "request")
        assert hasattr(error, "response")
        assert hasattr(error, "method")
        assert hasattr(error, "url")
        assert hasattr(error, "reason")

    def test_str_without_context(self) -> None:
        """Test string representation without any context information."""
        error = ApiClientUnauthorizedError("Test message")
        assert str(error) == "Test message (HTTP 401)"

        # Test with empty request object
        empty_request = Mock(spec=[])
        error_empty_context = ApiClientUnauthorizedError("Test message", request=empty_request)
        assert str(error_empty_context) == "Test message (HTTP 401)"

        # Test with response but no request - should still get status from response
        response = Mock(spec=['status_code', 'headers', 'text'])
        response.status_code = 401
        response.headers = {}
        response.text = ""
        error_response_only = ApiClientUnauthorizedError("Test message", response=response)
        assert str(error_response_only) == "Test message (HTTP 401)"

        # Test by manually setting status_code to None to force the return base_message path
        error_no_status = ApiClientUnauthorizedError("Test message")
        error_no_status.status_code = None
        assert str(error_no_status) == "Test message"


class TestApiClientForbiddenError:
    """Test cases for ApiClientForbiddenError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientForbiddenError()
        assert str(error) == "Forbidden (HTTP 403)"
        assert error.status_code == 403

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientForbiddenError("Access denied")
        assert str(error) == "Access denied (HTTP 403)"


class TestApiClientNotFoundError:
    """Test cases for ApiClientNotFoundError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientNotFoundError()
        assert str(error) == "Not Found (HTTP 404)"
        assert error.status_code == 404

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientNotFoundError("User not found")
        assert str(error) == "User not found (HTTP 404)"


class TestApiClientConflictError:
    """Test cases for ApiClientConflictError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientConflictError()
        assert str(error) == "Conflict (HTTP 409)"
        assert error.status_code == 409

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientConflictError("Resource already exists")
        assert str(error) == "Resource already exists (HTTP 409)"


class TestApiClientUnprocessableEntityError:
    """Test cases for ApiClientUnprocessableEntityError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientUnprocessableEntityError()
        assert str(error) == "Unprocessable Entity (HTTP 422)"
        assert error.status_code == 422

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientUnprocessableEntityError("Validation failed")
        assert str(error) == "Validation failed (HTTP 422)"


class TestApiClientRateLimitError:
    """Test cases for ApiClientRateLimitError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientRateLimitError()
        assert str(error) == "Rate Limit Exceeded (HTTP 429)"
        assert error.status_code == 429

    def test_custom_message(self) -> None:
        """Test initialization with custom message."""
        error = ApiClientRateLimitError("Too many requests")
        assert str(error) == "Too many requests (HTTP 429)"


class TestApiClientInternalServerError:
    """Test cases for ApiClientInternalServerError."""

    def test_default_initialization(self) -> None:
        """Test default initialization."""
        error = ApiClientInternalServerError()
        assert str(error) == "Internal Server Error (HTTP 500)"
        assert error.status_code == 500

    def test_custom_status_code(self) -> None:
        """Test initialization with custom 5xx status code."""
        error = ApiClientInternalServerError("Service unavailable", status_code=503)
        assert str(error) == "Service unavailable (HTTP 503)"
        assert error.status_code == 503

    def test_custom_message_and_status(self) -> None:
        """Test initialization with custom message and status code."""
        error = ApiClientInternalServerError("Gateway timeout", status_code=504)
        assert str(error) == "Gateway timeout (HTTP 504)"
        assert error.status_code == 504


class TestCreateApiClientError:
    """Test cases for the create_api_client_error utility function."""

    def test_mapped_status_codes(self) -> None:
        """Test creation of specific exception types for mapped status codes."""
        # Test all mapped status codes
        test_cases = [
            (400, ApiClientBadRequestError),
            (401, ApiClientUnauthorizedError),
            (403, ApiClientForbiddenError),
            (404, ApiClientNotFoundError),
            (409, ApiClientConflictError),
            (422, ApiClientUnprocessableEntityError),
            (429, ApiClientRateLimitError),
        ]

        for status_code, expected_class in test_cases:
            error = create_api_client_error(status_code)
            assert isinstance(error, expected_class)
            assert error.status_code == status_code

    def test_mapped_status_codes_with_custom_message(self) -> None:
        """Test creation with custom messages for mapped status codes."""
        error = create_api_client_error(404, "Custom not found message")
        assert isinstance(error, ApiClientNotFoundError)
        assert str(error) == "Custom not found message (HTTP 404)"

    def test_5xx_status_codes(self) -> None:
        """Test creation of server error exceptions for 5xx status codes."""
        test_cases = [500, 501, 502, 503, 504, 505, 599]

        for status_code in test_cases:
            error = create_api_client_error(status_code)
            assert isinstance(error, ApiClientInternalServerError)
            assert error.status_code == status_code
            if status_code == 500:
                assert str(error) == "Internal Server Error (HTTP 500)"
            else:
                assert str(error) == f"Server Error (HTTP {status_code}) (HTTP {status_code})"

    def test_5xx_with_custom_message(self) -> None:
        """Test 5xx status codes with custom messages."""
        error = create_api_client_error(503, "Service temporarily unavailable")
        assert isinstance(error, ApiClientInternalServerError)
        assert error.status_code == 503
        assert str(error) == "Service temporarily unavailable (HTTP 503)"

    def test_unmapped_status_codes(self) -> None:
        """Test creation of generic ApiClientError for unmapped status codes."""
        test_cases = [100, 200, 201, 300, 301, 418, 451]

        for status_code in test_cases:
            error = create_api_client_error(status_code)
            assert isinstance(error, ApiClientError)
            assert not isinstance(
                error,
                (
                    ApiClientBadRequestError,
                    ApiClientUnauthorizedError,
                    ApiClientForbiddenError,
                    ApiClientNotFoundError,
                    ApiClientConflictError,
                    ApiClientUnprocessableEntityError,
                    ApiClientRateLimitError,
                    ApiClientInternalServerError,
                ),
            )
            assert error.status_code == status_code
            assert str(error) == f"HTTP Error {status_code} (HTTP {status_code})"

    def test_unmapped_with_custom_message(self) -> None:
        """Test unmapped status codes with custom messages."""
        error = create_api_client_error(418, "I'm a teapot")
        assert isinstance(error, ApiClientError)
        assert error.status_code == 418
        assert str(error) == "I'm a teapot (HTTP 418)"

    def test_with_context(self) -> None:
        """Test creation with request and response objects."""
        request = Mock(spec=['method', 'url'])
        request.method = "GET"
        request.url = "https://api.example.com/users"

        response = Mock(spec=['status_code', 'reason', 'request', 'headers', 'text'])
        response.status_code = 404
        response.reason = "Not Found"
        response.request = request
        response.headers = {}
        response.text = ""

        error = create_api_client_error(404, "User not found", request=request, response=response)

        assert isinstance(error, ApiClientNotFoundError)
        assert error.request is request
        assert error.response is response
        assert error.method == "GET"
        assert error.url == "https://api.example.com/users"
        assert error.status_code == 404
        assert error.reason == "Not Found"
        assert str(error) == "User not found (HTTP 404, GET https://api.example.com/users)"

    def test_default_messages_used(self) -> None:
        """Test that default messages are used when no custom message provided."""
        # Test a few key status codes
        error_400 = create_api_client_error(400)
        assert str(error_400) == "Bad Request (HTTP 400)"

        error_401 = create_api_client_error(401)
        assert str(error_401) == "Unauthorized (HTTP 401)"

        error_404 = create_api_client_error(404)
        assert str(error_404) == "Not Found (HTTP 404)"

    def test_edge_cases(self) -> None:
        """Test edge cases for status code boundaries."""
        # Test boundary of 5xx range
        error_499 = create_api_client_error(499)
        assert isinstance(error_499, ApiClientError)
        assert not isinstance(error_499, ApiClientInternalServerError)

        error_500 = create_api_client_error(500)
        assert isinstance(error_500, ApiClientInternalServerError)

        error_599 = create_api_client_error(599)
        assert isinstance(error_599, ApiClientInternalServerError)

        error_600 = create_api_client_error(600)
        assert isinstance(error_600, ApiClientError)
        assert not isinstance(error_600, ApiClientInternalServerError)


class TestHttpExceptionIntegration:
    """Integration tests for HTTP exception hierarchy."""

    def test_exception_catching_hierarchy(self) -> None:
        """Test that exceptions can be caught at different levels of the hierarchy."""
        error = ApiClientNotFoundError("Test error")

        # Should be catchable as specific type
        assert isinstance(error, ApiClientNotFoundError)

        # Should be catchable as base API client error
        assert isinstance(error, ApiClientError)

        # Should be catchable as base apiconfig error
        assert isinstance(error, APIConfigError)

        # Should be catchable as base exception
        assert isinstance(error, Exception)

    def test_unauthorized_error_multiple_inheritance_catching(self) -> None:
        """Test that ApiClientUnauthorizedError can be caught as both types."""
        error = ApiClientUnauthorizedError("Test error")

        # Should be catchable as API client error
        assert isinstance(error, ApiClientError)

        # Should be catchable as authentication error
        assert isinstance(error, AuthenticationError)

        # Should be catchable as base apiconfig error
        assert isinstance(error, APIConfigError)

    def test_context_preservation_through_factory(self) -> None:
        """Test that context is preserved when using the factory function."""
        request = Mock(spec=['method', 'url', 'headers'])
        request.method = "POST"
        request.url = "https://api.example.com/users"
        request.headers = {"Content-Type": "application/json"}

        response = Mock(spec=['status_code', 'headers', 'text', 'reason', 'request'])
        response.status_code = 422
        response.headers = {"Content-Type": "application/json"}
        response.text = '{"error": "validation failed"}'
        response.reason = "Unprocessable Entity"
        response.request = request

        error = create_api_client_error(422, "Validation failed", request=request, response=response)

        assert isinstance(error, ApiClientUnprocessableEntityError)
        assert error.request is request
        assert error.response is response
        assert error.status_code == 422
        assert error.method == "POST"
        assert error.url == "https://api.example.com/users"
        assert error.reason == "Unprocessable Entity"
