"""HTTP-related exceptions for the apiconfig library.

This module defines exceptions raised by HTTP utility functions.
"""

from typing import final

from .base import APIConfigError

__all__ = ["HTTPUtilsError", "JSONDecodeError", "PayloadTooLargeError"]


class HTTPUtilsError(APIConfigError):
    """Base exception for errors raised by HTTP utilities."""


@final
class JSONDecodeError(HTTPUtilsError):
    """Raised when JSON decoding of an HTTP response body fails."""


@final
class PayloadTooLargeError(HTTPUtilsError):
    """Raised when a payload exceeds the maximum allowed size for processing."""
