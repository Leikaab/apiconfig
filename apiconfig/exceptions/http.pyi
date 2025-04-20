"""HTTP-related exceptions for the apiconfig library.

This module defines exceptions raised by HTTP utility functions.
"""

from .base import APIConfigError
from typing import final

__all__: list[str] = ["HTTPUtilsError", "JSONDecodeError"]


class HTTPUtilsError(APIConfigError):
    """Base exception for errors raised by HTTP utilities."""
    ...


@final
class JSONDecodeError(HTTPUtilsError):
    """Raised when JSON decoding of an HTTP response body fails."""
    ...
