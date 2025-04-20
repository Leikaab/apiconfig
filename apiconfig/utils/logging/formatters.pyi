import logging
import re
import types
from typing import Any, Mapping, Optional, Set, Tuple, Union

_FormatStyle = logging._FormatStyle

class DetailedFormatter(logging.Formatter):
    """
    A logging formatter that provides detailed, potentially multi-line output.

    Includes timestamp, level name, logger name, message, filename, and line number.
    Handles multi-line messages, exception information, and stack information
    with appropriate indentation.
    """

    def __init__(
        self,
        fmt: Optional[str] = ...,
        datefmt: Optional[str] = ...,
        style: Union[str, None] = ...,
        validate: bool = ...,
        *,
        defaults: Optional[Mapping[str, Any]] = ...,
    ) -> None: ...
    def format(self, record: logging.LogRecord) -> str: ...
    def formatException(
        self,
        ei: (
            tuple[type[BaseException], BaseException, types.TracebackType | None]
            | tuple[None, None, None]
        ),
    ) -> str: ...
    def formatStack(self, stack_info: str) -> str: ...

class RedactingFormatter(logging.Formatter):
    """
    A logging formatter that automatically redacts sensitive information from log messages and HTTP headers.

    Guarantees:
        - Applies redaction to structured log messages (JSON, dict, form-encoded) using the project's redaction utilities.
        - Redacts HTTP headers if present in the log record (as a dict) using the project's header redaction utility.
        - For plain string messages, redacts secrets matching the sensitive value pattern if provided.
        - All redacted output uses the REDACTED_VALUE constant.
        - No redaction logic is duplicated; always delegates to utility functions.

    Limitations:
        - Only redacts fields and values matching the configured patterns.
        - If a message cannot be parsed as structured data, only obvious secrets in plain strings are redacted.
        - Binary/unparsable data is replaced with a placeholder or left unchanged, per utility behavior.

    Configuration:
        - Sensitive key/value patterns for both body and headers can be customized via the constructor.
        - Defaults to the project's standard patterns.

    Args:
        fmt: Format string for the log message.
        datefmt: Date format string.
        style: Format style ('%', '{', or '$').
        validate: Whether to validate the format string.
        body_sensitive_keys_pattern: Regex pattern for sensitive keys in structured data.
        body_sensitive_value_pattern: Regex pattern for sensitive values in structured data or plain strings.
        header_sensitive_keys: Set of sensitive header keys (lowercase).
        header_sensitive_prefixes: Tuple of sensitive header prefixes (lowercase).
        header_sensitive_name_pattern: Regex pattern for sensitive header names.
        defaults: Optional mapping of default values for format fields.

    Example:
        >>> import logging
        >>> from apiconfig.utils.logging.formatters import RedactingFormatter
        >>> handler = logging.StreamHandler()
        >>> handler.setFormatter(RedactingFormatter())
        >>> logger = logging.getLogger("api")
        >>> logger.addHandler(handler)
        >>> logger.info({"token": "secret123", "data": "ok"})
        # Output: {"token": "[REDACTED]", "data": "ok"}
    """

    def __init__(
        self,
        fmt: Optional[str] = ...,
        datefmt: Optional[str] = ...,
        style: Union[str, None] = ...,
        validate: bool = ...,
        *,
        body_sensitive_keys_pattern: re.Pattern[str] = ...,
        body_sensitive_value_pattern: Optional[re.Pattern[str]] = ...,
        header_sensitive_keys: Set[str] = ...,
        header_sensitive_prefixes: Tuple[str, ...] = ...,
        header_sensitive_name_pattern: Optional[re.Pattern[str]] = ...,
        defaults: Optional[Mapping[str, Any]] = ...,
    ) -> None: ...
    def format(self, record: logging.LogRecord) -> str: ...
    def _redact_headers(self, record: logging.LogRecord) -> None: ...
    def _redact_message(self, record: logging.LogRecord) -> None: ...
    def _is_binary(self, msg: Any) -> bool: ...
    def _is_empty(self, msg: Any) -> bool: ...
    def _is_structured(self, msg: Any, content_type: Any) -> bool: ...
    def _redact_binary(self, msg: bytes) -> str: ...
    def _redact_empty(self, msg: Any) -> str: ...
    def _redact_structured(self, msg: Any, content_type: Any) -> str: ...
    def _redact_plain_string(self, msg: str) -> str: ...
