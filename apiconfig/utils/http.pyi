import sys
from typing import Any, Dict, Mapping, Optional, Union

from apiconfig.exceptions.http import HTTPUtilsError, JSONDecodeError, PayloadTooLargeError

__all__ = [
    "HTTPUtilsError",
    "JSONDecodeError",
    "PayloadTooLargeError",
    "is_success",
    "is_redirect",
    "is_client_error",
    "is_server_error",
    "normalize_header_name",
    "get_header_value",
    "safe_json_decode",
]

def is_success(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates success (2xx).

    Args:
        status_code: The HTTP status code.

    Returns:
        True if the status code is in the 200-299 range, False otherwise.
    """
    ...

def is_redirect(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates redirection (3xx).

    Args:
        status_code: The HTTP status code.

    Returns:
        True if the status code is in the 300-399 range, False otherwise.
    """
    ...

def is_client_error(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates a client error (4xx).

    Args:
        status_code: The HTTP status code.

    Returns:
        True if the status code is in the 400-499 range, False otherwise.
    """
    ...

def is_server_error(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates a server error (5xx).

    Args:
        status_code: The HTTP status code.

    Returns:
        True if the status code is in the 500-599 range, False otherwise.
    """
    ...

def normalize_header_name(name: str) -> str:
    """
    Normalize an HTTP header name to a canonical format (Title-Case).

    Example:
        'content-type' -> 'Content-Type'
        'X-CUSTOM-HEADER' -> 'X-Custom-Header'

    Args:
        name: The header name string.

    Returns:
        The normalized header name.
    """
    ...

def get_header_value(headers: Mapping[str, str], name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a header value from a mapping, case-insensitively.

    Normalizes both the provided header name and the keys in the mapping
    before comparison.

    Args:
        headers: A mapping (e.g., dictionary) of header names to values.
        name: The name of the header to retrieve (case-insensitive).
        default: The value to return if the header is not found.

    Returns:
        The header value if found, otherwise the default value.
    """
    ...

def safe_json_decode(
    response_text: Union[str, bytes],
    encoding: Optional[str] = None,
    max_size_bytes: int = 1 * 1024 * 1024,  # Default to 1MB
) -> Optional[Dict[str, Any]]:
    """
    Safely decode a JSON response body (string or bytes).

    Handles potential JSONDecodeError and UnicodeDecodeError.
    Returns None if the input content is empty.
    Checks payload size before decoding to prevent excessive memory usage.

    Args:
        response_text: The response body content as a string or bytes.
        encoding: The encoding to use if response_text is bytes. Defaults to 'utf-8'.
        max_size_bytes: Maximum allowed size of the payload in bytes. Defaults to 1MB.

    Returns:
        The decoded JSON dictionary, or None if the input was empty.

    Raises:
        PayloadTooLargeError: If the payload size exceeds max_size_bytes.
        JSONDecodeError: If JSON decoding fails or if byte decoding fails.
        HTTPUtilsError: For other unexpected errors during processing.
    """
    ...
