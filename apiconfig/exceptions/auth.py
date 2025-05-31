"""Authentication-specific exception classes for the apiconfig library."""

from typing import Optional

from apiconfig.types import HttpRequestProtocol, HttpResponseProtocol

from .base import AuthenticationError

__all__: list[str] = [
    "AuthenticationError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "TokenRefreshJsonError",
    "TokenRefreshTimeoutError",
    "TokenRefreshNetworkError",
    "AuthStrategyError",
]


class InvalidCredentialsError(AuthenticationError):
    """Raised when provided credentials are invalid.

    Parameters
    ----------
    message : str
        Error message describing the invalid credentials (default: "Invalid credentials provided")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Invalid credentials provided",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class ExpiredTokenError(AuthenticationError):
    """Raised when an authentication token has expired.

    Parameters
    ----------
    message : str
        Error message describing the token expiration (default: "Authentication token has expired")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Authentication token has expired",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class MissingCredentialsError(AuthenticationError):
    """Raised when required credentials are not provided.

    Parameters
    ----------
    message : str
        Error message describing the missing credentials (default: "Required credentials not provided")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Required credentials not provided",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class TokenRefreshError(AuthenticationError):
    """Raised when an attempt to refresh a token fails.

    Parameters
    ----------
    message : str
        Error message describing the token refresh failure (default: "Failed to refresh authentication token")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Failed to refresh authentication token",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class TokenRefreshJsonError(TokenRefreshError):
    """Raised when JSON decoding of a token refresh response fails.

    Parameters
    ----------
    message : str
        Error message describing the JSON decoding failure (default: "Failed to decode JSON from token refresh response")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Failed to decode JSON from token refresh response",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class TokenRefreshTimeoutError(TokenRefreshError):
    """Raised when a token refresh request times out.

    Parameters
    ----------
    message : str
        Error message describing the timeout (default: "Token refresh request timed out")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Token refresh request timed out",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class TokenRefreshNetworkError(TokenRefreshError):
    """Raised when a token refresh request fails due to network issues.

    Parameters
    ----------
    message : str
        Error message describing the network failure (default: "Token refresh request failed due to network issues")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Token refresh request failed due to network issues",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)


class AuthStrategyError(AuthenticationError):
    """Base exception for errors specific to an authentication strategy.

    Parameters
    ----------
    message : str
        Error message describing the authentication strategy error (default: "Authentication strategy error")
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    """

    def __init__(
        self,
        message: str = "Authentication strategy error",
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        super().__init__(message, request=request, response=response)
