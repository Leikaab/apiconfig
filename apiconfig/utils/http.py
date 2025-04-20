import json
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
    return 200 <= status_code <= 299


def is_redirect(status_code: int) -> bool:
    return 300 <= status_code <= 399


def is_client_error(status_code: int) -> bool:
    return 400 <= status_code <= 499


def is_server_error(status_code: int) -> bool:
    return 500 <= status_code <= 599


def normalize_header_name(name: str) -> str:
    # Normalize to title case as per common convention (e.g., 'Content-Type')
    return "-".join(part.capitalize() for part in name.split("-"))


def get_header_value(
    headers: Mapping[str, str], name: str, default: Optional[str] = None
) -> Optional[str]:
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
    try:
        if isinstance(response_text, bytes):
            # Check size before decoding bytes
            if len(response_text) > max_size_bytes:
                raise PayloadTooLargeError(
                    f"Payload size ({len(response_text)} bytes) exceeds maximum allowed size ({max_size_bytes} bytes)"
                )
            # Attempt to decode bytes using provided encoding or default (UTF-8)
            text_content = response_text.decode(encoding or "utf-8")
        else:
            # Check size for string (UTF-8 encoded size)
            encoded_size = len(response_text.encode("utf-8"))
            if encoded_size > max_size_bytes:
                raise PayloadTooLargeError(
                    f"Payload size ({encoded_size} bytes) exceeds maximum allowed size ({max_size_bytes} bytes)"
                )
            text_content = response_text

        # Strip whitespace before checking if empty
        stripped_content = text_content.strip()
        if not stripped_content:
            return None  # Return None for empty or whitespace-only content

        return json.loads(stripped_content)
    except json.JSONDecodeError as e:
        raise JSONDecodeError(f"Failed to decode JSON: {e}") from e
    except UnicodeDecodeError as e:
        raise JSONDecodeError(
            f"Failed to decode response body with encoding '{encoding or 'utf-8'}': {e}"
        ) from e
    except PayloadTooLargeError:
        # Re-raise PayloadTooLargeError directly without wrapping
        raise
    except Exception as e:
        # Catch other potential errors during processing
        raise HTTPUtilsError(
            f"An unexpected error occurred during JSON decoding: {e}"
        ) from e
