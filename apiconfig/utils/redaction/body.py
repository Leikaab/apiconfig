import json
import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlencode

from .headers import REDACTED_VALUE  # Use consistent placeholder

# Constants
# REDACTED_PLACEHOLDER = "[REDACTED]" # Replaced by REDACTED_VALUE from headers
DEFAULT_SENSITIVE_KEYS_PATTERN = re.compile(
    r"password|token|secret|key|auth", re.IGNORECASE
)
REDACTED_BODY_PLACEHOLDER = "[REDACTED BODY]"


def _redact_recursive(
    data: Any,
    key_pattern: re.Pattern,
    value_pattern: Optional[re.Pattern] = None,
) -> Any:
    """Recursively redact sensitive data in dictionaries and lists."""
    if isinstance(data, dict):
        redacted_dict = {}
        for key, value in data.items():
            if key_pattern.search(key):
                redacted_dict[key] = REDACTED_VALUE
            else:
                redacted_dict[key] = _redact_recursive(
                    value, key_pattern, value_pattern
                )
        return redacted_dict
    elif isinstance(data, list):
        return [_redact_recursive(item, key_pattern, value_pattern) for item in data]
    elif isinstance(data, str) and value_pattern and value_pattern.search(data):
        return REDACTED_VALUE
    else:
        # Not a dict, list, or sensitive string value
        return data


def redact_body(
    body: Union[str, bytes, Any],
    content_type: Optional[str] = None,
    sensitive_keys_pattern: re.Pattern = DEFAULT_SENSITIVE_KEYS_PATTERN,
    sensitive_value_pattern: Optional[re.Pattern] = None,
) -> Union[str, bytes, Any]:
    """
    Redacts sensitive information from request or response bodies.

    Attempts to parse JSON or form-urlencoded bodies and recursively redacts
    values associated with keys matching `sensitive_keys_pattern` or string
    values matching `sensitive_value_pattern`.

    Args:
        body: The request or response body (str, bytes, or already parsed).
        content_type: The Content-Type header value (e.g., 'application/json').
        sensitive_keys_pattern: A compiled regex pattern to identify sensitive keys.
        sensitive_value_pattern: An optional compiled regex pattern to identify
                                 sensitive string values.

    Returns:
        The body with sensitive information redacted, or the original body
        if parsing/redaction is not applicable or fails.
    """
    if body is None:
        return None

    parsed_body: Any = None
    is_json = False
    is_form = False
    body_str: Optional[str] = None

    # 1. Determine type and decode if necessary
    if isinstance(body, bytes):
        try:
            # Attempt decoding assuming UTF-8, common for JSON/forms
            body_str = body.decode("utf-8")
        except UnicodeDecodeError:
            # If decoding fails, it's likely binary data, return placeholder
            return REDACTED_BODY_PLACEHOLDER
    elif isinstance(body, str):
        body_str = body
    else:
        # Body is already parsed (e.g., a dict or list)
        parsed_body = body
        # Assume JSON if it's a dict or list and no content_type specified
        if content_type is None and isinstance(body, (dict, list)):
            is_json = True

    # 2. Check content type if body was string/bytes
    if body_str is not None and content_type:
        content_type_lower = content_type.lower()
        if "application/json" in content_type_lower:
            is_json = True
        elif "application/x-www-form-urlencoded" in content_type_lower:
            is_form = True

    # 3. Parse and Redact
    try:
        if is_json:
            if parsed_body is None and body_str is not None:
                parsed_body = json.loads(body_str)
            redacted_data = _redact_recursive(
                parsed_body, sensitive_keys_pattern, sensitive_value_pattern
            )
            # Return in original format (parsed dict/list or JSON string)
            return json.dumps(redacted_data) if body_str is not None else redacted_data
        elif is_form and body_str is not None:
            parsed_form = parse_qs(body_str, keep_blank_values=True)
            redacted_form: Dict[str, List[str]] = {}
            for key, values in parsed_form.items():
                if sensitive_keys_pattern.search(key):
                    redacted_form[key] = [REDACTED_VALUE] * len(values)
                else:
                    # Check individual values if a value pattern is provided
                    if sensitive_value_pattern:
                        redacted_values = [
                            REDACTED_VALUE if sensitive_value_pattern.search(v) else v
                            for v in values
                        ]
                        redacted_form[key] = redacted_values
                    else:
                        redacted_form[key] = values
            # Return re-encoded form data
            return urlencode(redacted_form, doseq=True)

    except (json.JSONDecodeError, TypeError, ValueError):
        # If parsing fails, return original string/bytes or placeholder
        return (
            body_str if body_str is not None else body
        )  # Or consider REDACTED_BODY_PLACEHOLDER

    # 4. If not JSON or form, or if parsing failed, return original/placeholder
    # If it was originally bytes but couldn't be decoded, placeholder was returned earlier.
    # If it was originally a string/bytes but not JSON/Form, return original.
    # If it was already parsed but not dict/list, return original.
    return body_str if body_str is not None else body
