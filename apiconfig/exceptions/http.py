"""HTTP-related exceptions for the apiconfig library.

This module defines exceptions raised by HTTP utility functions and HTTP API
client operations, with clear relationships to Python's native json library
exceptions where applicable.
"""

import json
from typing import Dict, List, Optional, Type, final

from apiconfig.types import HttpRequestProtocol, HttpResponseProtocol

from .base import APIConfigError, AuthenticationError, HttpContextMixin

__all__ = [
    "HTTPUtilsError",
    "JSONDecodeError",
    "JSONEncodeError",
    "PayloadTooLargeError",
    "ApiClientError",
    "ApiClientBadRequestError",
    "ApiClientUnauthorizedError",
    "ApiClientForbiddenError",
    "ApiClientNotFoundError",
    "ApiClientConflictError",
    "ApiClientUnprocessableEntityError",
    "ApiClientRateLimitError",
    "ApiClientInternalServerError",
    "create_api_client_error",
]


class HTTPUtilsError(APIConfigError):
    """Base exception for errors raised by HTTP utilities."""


@final
class JSONDecodeError(HTTPUtilsError, json.JSONDecodeError):
    """Raised when JSON decoding of an HTTP response body fails.

    Inherits from both HTTPUtilsError (for apiconfig exception hierarchy)
    and json.JSONDecodeError (for compatibility with native json exceptions).
    This allows catching either the specific apiconfig exception or the
    broader native json exception.
    """

    def __init__(self, msg: str, doc: str = "", pos: int = 0) -> None:
        """Initialize the JSONDecodeError.

        Parameters
        ----------
        msg : str
            The error message
        doc : str, optional
            The JSON document being parsed
        pos : int, optional
            The position in the document where parsing failed
        """
        # Initialize both parent classes
        HTTPUtilsError.__init__(self, msg)
        json.JSONDecodeError.__init__(self, msg, doc, pos)


@final
class JSONEncodeError(HTTPUtilsError, ValueError):
    """Raised when JSON encoding of data fails.

    Inherits from both HTTPUtilsError (for apiconfig exception hierarchy)
    and ValueError (following Python's convention for encoding errors).
    Python's json module doesn't have a specific JSONEncodeError,
    so we inherit from ValueError which is what json.dumps() raises.
    """


@final
class PayloadTooLargeError(HTTPUtilsError):
    """Raised when a payload exceeds the maximum allowed size for processing."""


# HTTP API Client Error Hierarchy


class ApiClientError(APIConfigError, HttpContextMixin):
    """
    Base exception for errors during HTTP API client operations.

    This exception provides a foundation for handling HTTP-related errors
    with rich context information for debugging and error handling.

    Parameters
    ----------
    message : str
        Error message describing the API client failure
    status_code : Optional[int]
        HTTP status code associated with the error
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        """
        Initialize API client error with HTTP context.

        Parameters
        ----------
        message : str
            Error message describing the API client failure
        status_code : Optional[int]
            HTTP status code associated with the error
        request : Optional[HttpRequestProtocol]
            HTTP request object
        response : Optional[HttpResponseProtocol]
            HTTP response object
        """
        super().__init__(message)
        self._init_http_context(request=request, response=response, status_code=status_code)

    def __str__(self) -> str:
        """Return string representation with HTTP context."""
        # Get the base message directly from Exception to avoid multiple inheritance issues
        base_message = Exception.__str__(self)

        context_parts: List[str] = []
        if self.status_code:
            context_parts.append(f"HTTP {self.status_code}")

        if self.method and self.url:
            context_parts.append(f"{self.method} {self.url}")

        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"

        return base_message


class ApiClientBadRequestError(ApiClientError):
    """
    HTTP 400 Bad Request from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the bad request (default: "Bad Request")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Bad Request",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=400, request=request, response=response)


class ApiClientUnauthorizedError(ApiClientError, AuthenticationError):
    """
    HTTP 401 Unauthorized from an API client operation.

    Indicates an authentication failure during an HTTP call.
    This class uses multiple inheritance to be both an API client error
    and an authentication error.

    Parameters
    ----------
    message : str
        Error message describing the unauthorized access (default: "Unauthorized")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Unauthorized",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        # Only call ApiClientError.__init__ since it already handles HTTP context initialization
        ApiClientError.__init__(self, message, status_code=401, request=request, response=response)

    def __str__(self) -> str:
        """Return string representation using ApiClientError's format."""
        # Use ApiClientError's __str__ method explicitly to avoid AuthenticationError's format
        return ApiClientError.__str__(self)


class ApiClientForbiddenError(ApiClientError):
    """
    HTTP 403 Forbidden from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the forbidden access (default: "Forbidden")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Forbidden",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=403, request=request, response=response)


class ApiClientNotFoundError(ApiClientError):
    """
    HTTP 404 Not Found from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the not found resource (default: "Not Found")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Not Found",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=404, request=request, response=response)


class ApiClientConflictError(ApiClientError):
    """
    HTTP 409 Conflict from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the conflict (default: "Conflict")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Conflict",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=409, request=request, response=response)


class ApiClientUnprocessableEntityError(ApiClientError):
    """
    HTTP 422 Unprocessable Entity from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the unprocessable entity (default: "Unprocessable Entity")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Unprocessable Entity",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=422, request=request, response=response)


class ApiClientRateLimitError(ApiClientError):
    """
    HTTP 429 Too Many Requests from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the rate limit (default: "Rate Limit Exceeded")
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Rate Limit Exceeded",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=429, request=request, response=response)


class ApiClientInternalServerError(ApiClientError):
    """
    HTTP 5xx Server Error from an API client operation.

    Parameters
    ----------
    message : str
        Error message describing the server error (default: "Internal Server Error")
    status_code : int
        HTTP status code (default: 500)
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object
    """

    def __init__(
        self,
        message: str = "Internal Server Error",
        status_code: int = 500,
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, status_code=status_code, request=request, response=response)


def create_api_client_error(
    status_code: int,
    message: Optional[str] = None,
    *,
    request: Optional[HttpRequestProtocol] = None,
    response: Optional[HttpResponseProtocol] = None,
) -> ApiClientError:
    """
    Create appropriate ApiClientError subclass based on HTTP status code.

    This utility function maps HTTP status codes to their corresponding
    exception classes, providing a convenient way to create the most
    specific exception type for a given status code.

    Parameters
    ----------
    status_code : int
        HTTP status code
    message : Optional[str]
        Custom error message (uses default if not provided)
    request : Optional[HttpRequestProtocol]
        HTTP request object
    response : Optional[HttpResponseProtocol]
        HTTP response object

    Returns
    -------
    ApiClientError
        Appropriate exception subclass for the status code

    Examples
    --------
    >>> error = create_api_client_error(404, "Resource not found")
    >>> isinstance(error, ApiClientNotFoundError)
    True
    >>> error = create_api_client_error(500)
    >>> isinstance(error, ApiClientInternalServerError)
    True
    """
    error_classes: Dict[int, Type[ApiClientError]] = {
        400: ApiClientBadRequestError,
        401: ApiClientUnauthorizedError,
        403: ApiClientForbiddenError,
        404: ApiClientNotFoundError,
        409: ApiClientConflictError,
        422: ApiClientUnprocessableEntityError,
        429: ApiClientRateLimitError,
    }

    if status_code in error_classes:
        error_class = error_classes[status_code]
        if message is not None:
            return error_class(message, request=request, response=response)
        else:
            # All subclasses have default message values, so we can call without message
            # mypy doesn't understand this, so we use type: ignore
            return error_class(request=request, response=response)  # type: ignore[call-arg]
    elif 500 <= status_code < 600:
        if message:
            return ApiClientInternalServerError(message, status_code=status_code, request=request, response=response)
        elif status_code == 500:
            return ApiClientInternalServerError(request=request, response=response)
        else:
            return ApiClientInternalServerError(f"Server Error (HTTP {status_code})", status_code=status_code, request=request, response=response)
    else:
        return ApiClientError(message or f"HTTP Error {status_code}", status_code=status_code, request=request, response=response)
