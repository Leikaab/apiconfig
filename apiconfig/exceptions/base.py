"""Base exception classes for the apiconfig library."""

from typing import Any, List, Optional

from apiconfig.types import HttpRequestProtocol, HttpResponseProtocol

__all__: list[str] = [
    "APIConfigError",
    "ConfigurationError",
    "AuthenticationError",
    "HttpContextMixin",
]


class APIConfigError(Exception):
    """Base exception for all apiconfig errors."""


class ConfigurationError(APIConfigError):
    """Base exception for configuration-related errors."""


class HttpContextMixin:
    """Mixin to add HTTP context extraction capabilities to exceptions."""

    def _init_http_context(
        self, request: Optional[HttpRequestProtocol] = None, response: Optional[HttpResponseProtocol] = None, status_code: Optional[int] = None
    ) -> None:
        """Initialize HTTP context attributes from request/response objects."""
        # Initialize all attributes
        self.status_code = status_code
        self.method: Optional[str] = None
        self.url: Optional[str] = None
        self.reason: Optional[str] = None
        self.request = None  # Original request object
        self.response = None  # Original response object

        # Handle explicit request parameter first - it takes precedence
        if request is not None:
            self.request = request
            self._extract_from_request(request)

        # Handle response parameter
        if response is not None:
            self.response = response
            self._extract_from_response(response)

            # If no explicit request was provided, try to extract from response
            if request is None:
                try:
                    # Check if response has a request attribute
                    # Note: hasattr() would trigger the property getter in httpx, causing RuntimeError
                    req = getattr(response, "request", None)
                    if req is not None:
                        self.request = req
                        self._extract_from_request(req)
                except RuntimeError as e:
                    # httpx raises RuntimeError when accessing request on a Response
                    # created without a request. This is expected behavior.
                    # The error message is: "The request instance has not been set on this response."
                    if "request instance has not been set" in str(e):
                        # This is the expected httpx behavior - no request available
                        pass
                    else:
                        # This is an unexpected RuntimeError - re-raise it
                        raise

    def _extract_from_request(self, request: Any) -> None:
        """Extract attributes from protocol-compliant request object."""
        if hasattr(request, "method") and request.method is not None:
            self.method = str(request.method)

        if hasattr(request, "url") and request.url is not None:
            self.url = str(request.url)

    def _extract_from_response(self, response: Any) -> None:
        """Extract attributes from protocol-compliant response object."""
        if hasattr(response, "status_code") and response.status_code is not None:
            self.status_code = int(response.status_code)

        if hasattr(response, "reason"):
            self.reason = str(response.reason) if response.reason else None


class AuthenticationError(APIConfigError, HttpContextMixin):
    """Base exception for authentication-related errors.

    Parameters
    ----------
    message : str
        Error message describing the authentication failure
    request : Optional[HttpRequestProtocol]
        HTTP request object (optional)
    response : Optional[HttpResponseProtocol]
        HTTP response object (optional)
    *args : Any
        Additional positional arguments for base exception
    **kwargs : Any
        Additional keyword arguments for base exception
    """

    def __init__(
        self,
        message: str,
        *,
        request: Optional[HttpRequestProtocol] = None,
        response: Optional[HttpResponseProtocol] = None,
    ) -> None:
        """
        Initialize authentication error with optional HTTP context.

        Parameters
        ----------
        message : str
            Error message describing the authentication failure
        request : Optional[HttpRequestProtocol]
            HTTP request object (optional)
        response : Optional[HttpResponseProtocol]
            HTTP response object (optional)
        """
        super().__init__(message)
        self._init_http_context(request=request, response=response)

    def __str__(self) -> str:
        """Return string representation with context if available."""
        base_message = super().__str__()

        context_parts: List[str] = []

        if self.method and self.url:
            context_parts.append(f"Request: {self.method} {self.url}")

        if self.status_code is not None:
            status_info = f"{self.status_code}"
            if self.reason:
                status_info += f" {self.reason}"
            context_parts.append(f"Response: {status_info}")

        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"

        return base_message
