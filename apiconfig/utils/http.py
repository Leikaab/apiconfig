import json
from typing import Any, Dict, Mapping, Optional, Union

from ..exceptions.base import APIConfigError


class HTTPUtilsError(APIConfigError):
    pass


class JSONDecodeError(HTTPUtilsError):
    pass


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
) -> Optional[Dict[str, Any]]:
    try:
        if isinstance(response_text, bytes):
            # Attempt to decode bytes using provided encoding or default (UTF-8)
            text_content = response_text.decode(encoding or "utf-8")
        else:
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
    except Exception as e:
        # Catch other potential errors during processing
        raise HTTPUtilsError(f"An unexpected error occurred during JSON decoding: {e}") from e
