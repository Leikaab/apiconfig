import re
from typing import Any, Optional, Pattern, Union

REDACTED_PLACEHOLDER: str
DEFAULT_SENSITIVE_KEYS_PATTERN: Pattern[str]
REDACTED_BODY_PLACEHOLDER: str


def redact_body(
    body: Union[str, bytes, Any],
    content_type: Optional[str] = ...,
    sensitive_keys_pattern: Pattern[str] = ...,
    sensitive_value_pattern: Optional[Pattern[str]] = ...,
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
                                Defaults to matching 'password', 'token', 'secret',
                                'key', 'auth' case-insensitively.
        sensitive_value_pattern: An optional compiled regex pattern to identify
                                 sensitive string values. Defaults to `None`.

    Returns:
        The body with sensitive information redacted, or the original body
        if parsing/redaction is not applicable or fails. Returns a generic
        placeholder if the body is bytes and cannot be decoded.
    """
    ...
