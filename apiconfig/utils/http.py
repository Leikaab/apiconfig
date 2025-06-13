# -*- coding: utf-8 -*-
"""HTTP related utility functions."""

import json
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Union, cast

if TYPE_CHECKING:  # pragma: no cover - imported only for type checking
    from apiconfig.exceptions.http import (
        HTTPUtilsError,
        JSONDecodeError,
        JSONEncodeError,
        PayloadTooLargeError,
    )

__all__ = [
    "HTTPUtilsError",
    "JSONDecodeError",
    "JSONEncodeError",
    "PayloadTooLargeError",
    "is_success",
    "is_redirect",
    "is_client_error",
    "is_server_error",
    "normalize_header_name",
    "get_header_value",
    "safe_json_decode",
    "safe_json_encode",
]


def __getattr__(name: str) -> Any:  # pragma: no cover - lazy attribute access
    if name in {
        "HTTPUtilsError",
        "JSONDecodeError",
        "JSONEncodeError",
        "PayloadTooLargeError",
    }:
        from apiconfig.exceptions.http import (
            HTTPUtilsError,
            JSONDecodeError,
            JSONEncodeError,
            PayloadTooLargeError,
        )

        return {
            "HTTPUtilsError": HTTPUtilsError,
            "JSONDecodeError": JSONDecodeError,
            "JSONEncodeError": JSONEncodeError,
            "PayloadTooLargeError": PayloadTooLargeError,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def is_success(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates success (2xx).

    Parameters
    ----------
    status_code : int
        The HTTP status code.

    Returns
    -------
    bool
        True if the status code is in the 200-299 range, False otherwise.
    """
    return 200 <= status_code <= 299


def is_redirect(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates redirection (3xx).

    Parameters
    ----------
    status_code : int
        The HTTP status code.

    Returns
    -------
    bool
        True if the status code is in the 300-399 range, False otherwise.
    """
    return 300 <= status_code <= 399


def is_client_error(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates a client error (4xx).

    Parameters
    ----------
    status_code : int
        The HTTP status code.

    Returns
    -------
    bool
        True if the status code is in the 400-499 range, False otherwise.
    """
    return 400 <= status_code <= 499


def is_server_error(status_code: int) -> bool:
    """
    Check if an HTTP status code indicates a server error (5xx).

    Parameters
    ----------
    status_code : int
        The HTTP status code.

    Returns
    -------
    bool
        True if the status code is in the 500-599 range, False otherwise.
    """
    return 500 <= status_code <= 599


def normalize_header_name(name: str) -> str:
    """
    Normalize an HTTP header name to a canonical format (Title-Case).

    Example
    -------
    'content-type' -> 'Content-Type'
    'X-CUSTOM-HEADER' -> 'X-Custom-Header'

    Parameters
    ----------
    name : str
        The header name string.

    Returns
    -------
    str
        The normalized header name.
    """
    return "-".join(part.capitalize() for part in name.split("-"))


def get_header_value(headers: Mapping[str, str], name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a header value from a mapping, case-insensitively.

    Normalizes both the provided header name and the keys in the mapping
    before comparison.

    Parameters
    ----------
    headers : Mapping[str, str]
        A mapping (e.g., dictionary) of header names to values.
    name : str
        The name of the header to retrieve (case-insensitive).
    default : Optional[str], optional
        The value to return if the header is not found.

    Returns
    -------
    Optional[str]
        The header value if found, otherwise the default value.
    """
    normalized_name = normalize_header_name(name)
    for key, value in headers.items():
        if normalize_header_name(key) == normalized_name:
            return value
    return default


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

    Parameters
    ----------
    response_text : Union[str, bytes]
        The response body content as a string or bytes.
    encoding : Optional[str], optional
        The encoding to use if response_text is bytes. Defaults to 'utf-8'.
    max_size_bytes : int, optional
        Maximum allowed size of the payload in bytes. Defaults to 1MB.

    Returns
    -------
    Optional[Dict[str, Any]]
        The decoded JSON dictionary, or None if the input was empty.

    Raises
    ------
    PayloadTooLargeError
        If the payload size exceeds max_size_bytes.
    JSONDecodeError
        If JSON decoding fails or if byte decoding fails.
    HTTPUtilsError
        For other unexpected errors during processing.
    """
    # Import exceptions lazily to avoid unnecessary runtime dependencies
    from apiconfig.exceptions.http import (
        HTTPUtilsError,
        JSONDecodeError,
        PayloadTooLargeError,
    )

    try:
        if isinstance(response_text, bytes):
            # Check size before decoding bytes
            if len(response_text) > max_size_bytes:
                raise PayloadTooLargeError(f"Payload size ({len(response_text)} bytes) exceeds maximum allowed size ({max_size_bytes} bytes)")
            # Attempt to decode bytes using provided encoding or default (UTF-8)
            text_content = response_text.decode(encoding or "utf-8")
        else:
            # Check size for string (UTF-8 encoded size)
            encoded_size = len(response_text.encode("utf-8"))
            if encoded_size > max_size_bytes:
                raise PayloadTooLargeError(f"Payload size ({encoded_size} bytes) exceeds maximum allowed size ({max_size_bytes} bytes)")
            text_content = response_text

        # Strip whitespace before checking if empty
        stripped_content = text_content.strip()
        if not stripped_content:
            return None  # Return None for empty or whitespace-only content

        result = json.loads(stripped_content)
        if not isinstance(result, dict):
            raise JSONDecodeError("Decoded JSON is not an object (dict).")
        result = cast(Dict[str, Any], result)
        return result
    except json.JSONDecodeError as e:
        raise JSONDecodeError(f"Failed to decode JSON: {e}") from e
    except UnicodeDecodeError as e:
        raise JSONDecodeError(f"Failed to decode response body with encoding '{encoding or 'utf-8'}': {e}") from e
    except PayloadTooLargeError:
        # Re-raise PayloadTooLargeError directly without wrapping
        raise
    except Exception as e:
        # Catch other potential errors during processing
        raise HTTPUtilsError(f"An unexpected error occurred during JSON decoding: {e}") from e


def safe_json_encode(
    data: Any,
    ensure_ascii: bool = False,
    indent: Optional[int] = None,
    max_size_bytes: int = 1 * 1024 * 1024,  # Default to 1MB
) -> str:
    """
    Safely encode data to a JSON string.

    Handles potential errors during JSON encoding and checks the resulting
    string size to prevent excessive memory usage.

    Parameters
    ----------
    data : Any
        The data to encode as JSON.
    ensure_ascii : bool, optional
        If True, escape non-ASCII characters. Defaults to False.
    indent : Optional[int], optional
        Number of spaces for indentation. None for compact output.
    max_size_bytes : int, optional
        Maximum allowed size of the resulting JSON string in bytes. Defaults to 1MB.

    Returns
    -------
    str
        The JSON-encoded string.

    Raises
    ------
    JSONEncodeError
        If JSON encoding fails or if the data is not serializable.
    PayloadTooLargeError
        If the resulting JSON string exceeds max_size_bytes.
    HTTPUtilsError
        For other unexpected errors during processing.
    """
    # Import exceptions lazily to avoid unnecessary runtime dependencies
    from apiconfig.exceptions.http import (
        HTTPUtilsError,
        JSONEncodeError,
        PayloadTooLargeError,
    )

    try:
        # Attempt to encode the data as JSON
        json_string = json.dumps(data, ensure_ascii=ensure_ascii, indent=indent)

        # Check the size of the resulting string
        encoded_size = len(json_string.encode("utf-8"))
        if encoded_size > max_size_bytes:
            raise PayloadTooLargeError(f"Encoded JSON size ({encoded_size} bytes) exceeds maximum allowed size ({max_size_bytes} bytes)")

        return json_string
    except TypeError as e:
        # json.dumps raises TypeError for non-serializable objects
        raise JSONEncodeError(f"Failed to encode data as JSON: {e}") from e
    except ValueError as e:
        # json.dumps can raise ValueError for certain edge cases
        raise JSONEncodeError(f"Failed to encode data as JSON: {e}") from e
    except PayloadTooLargeError:
        # Re-raise PayloadTooLargeError directly without wrapping
        raise
    except Exception as e:
        # Catch other potential errors during processing
        raise HTTPUtilsError(f"An unexpected error occurred during JSON encoding: {e}") from e
