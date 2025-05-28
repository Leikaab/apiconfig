"""Base exception classes for the apiconfig library."""

from typing import Any, Optional

from apiconfig.types import HttpRequestContext, HttpResponseContext

__all__: list[str] = [
    "APIConfigError",
    "ConfigurationError",
    "AuthenticationError",
]


class APIConfigError(Exception):
    """Base exception for all apiconfig errors."""


class ConfigurationError(APIConfigError):
    """Base exception for configuration-related errors."""


class AuthenticationError(APIConfigError):
    """Base exception for authentication-related errors.

    Parameters
    ----------
    message : str
        Error message describing the authentication failure
    request_context : Optional[HttpRequestContext]
        HTTP request context for debugging (optional)
    response_context : Optional[HttpResponseContext]
        HTTP response context for debugging (optional)
    *args : Any
        Additional positional arguments for base exception
    **kwargs : Any
        Additional keyword arguments for base exception
    """

    def __init__(
        self,
        message: str,
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize authentication error with optional HTTP context.

        Parameters
        ----------
        message : str
            Error message describing the authentication failure
        request_context : Optional[HttpRequestContext]
            HTTP request context for debugging (optional)
        response_context : Optional[HttpResponseContext]
            HTTP response context for debugging (optional)
        *args : Any
            Additional positional arguments for base exception
        **kwargs : Any
            Additional keyword arguments for base exception
        """
        super().__init__(message, *args, **kwargs)
        self.request_context = request_context
        self.response_context = response_context

    def __str__(self) -> str:
        """Return string representation with context if available."""
        base_message = super().__str__()

        context_parts = []

        # Only add context if the context dict is not None and has meaningful content
        if self.request_context and (self.request_context.get("method") or self.request_context.get("url")):
            method = self.request_context.get("method", "UNKNOWN")
            url = self.request_context.get("url", "UNKNOWN")
            context_parts.append(f"Request: {method} {url}")

        if self.response_context and (self.response_context.get("status_code") is not None or self.response_context.get("reason")):
            status = self.response_context.get("status_code", "UNKNOWN")
            reason = self.response_context.get("reason", "")
            status_info = f"{status} {reason}".strip()
            context_parts.append(f"Response: {status_info}")

        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"

        return base_message
