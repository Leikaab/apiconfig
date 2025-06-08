# -*- coding: utf-8 -*-
"""Logging formatter that redacts sensitive information."""

from __future__ import annotations

import logging
import re
from typing import Any, Literal, Mapping, Optional, Set, Tuple

from apiconfig.utils.redaction.body import (
    DEFAULT_SENSITIVE_KEYS_PATTERN as DEFAULT_BODY_KEYS_PATTERN,
)
from apiconfig.utils.redaction.body import (
    redact_body,
)
from apiconfig.utils.redaction.headers import (
    DEFAULT_SENSITIVE_COOKIE_KEYS,
    DEFAULT_SENSITIVE_HEADER_PREFIXES,
    DEFAULT_SENSITIVE_HEADERS,
    REDACTED_VALUE,
    redact_headers,
)


class RedactingFormatter(logging.Formatter):
    """Automatically redact sensitive information from log messages and HTTP headers.

    Guarantees
    ----------
    - Applies redaction to structured log messages (JSON, dict, form-encoded) using the project's redaction utilities.
    - Redacts HTTP headers if present in the log record (as a dict) using the project's header redaction utility.
    - For plain string messages, redacts secrets matching the sensitive value pattern if provided.
    - All redacted output uses the REDACTED_VALUE constant.
    - No redaction logic is duplicated; always delegates to utility functions.

    Limitations
    -----------
    - Only redacts fields and values matching the configured patterns.
    - If a message cannot be parsed as structured data, only obvious secrets in plain strings are redacted.
    - Binary/unparsable data is replaced with a placeholder or left unchanged, per utility behavior.

    Configuration
    -------------
    - Sensitive key/value patterns for both body and headers can be customized via the constructor.
    - Defaults to the project's standard patterns.

    Args
    ----
    fmt
        Format string for the log message.
    datefmt
        Date format string.
    style
        Format style ('%', '{', or '$').
    validate
        Whether to validate the format string.
    body_sensitive_keys_pattern
        Regex pattern for sensitive keys in structured data.
    body_sensitive_value_pattern
        Regex pattern for sensitive values in structured data or plain strings.
    header_sensitive_keys
        Set of sensitive header keys (lowercase).
    header_sensitive_prefixes
        Tuple of sensitive header prefixes (lowercase).
    header_sensitive_name_pattern
        Regex pattern for sensitive header names.
    defaults
        Optional mapping of default values for format fields.

    Example
    -------
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
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        *,
        body_sensitive_keys_pattern: re.Pattern[str] = DEFAULT_BODY_KEYS_PATTERN,
        body_sensitive_value_pattern: Optional[re.Pattern[str]] = None,
        header_sensitive_keys: Set[str] = DEFAULT_SENSITIVE_HEADERS,
        header_sensitive_prefixes: Tuple[str, ...] = DEFAULT_SENSITIVE_HEADER_PREFIXES,
        header_sensitive_name_pattern: Optional[re.Pattern[str]] = None,
        header_sensitive_cookie_keys: Set[str] = DEFAULT_SENSITIVE_COOKIE_KEYS,
        defaults: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
            defaults=defaults,
        )
        self.body_sensitive_keys_pattern = body_sensitive_keys_pattern
        self.body_sensitive_value_pattern = body_sensitive_value_pattern
        self.header_sensitive_keys = header_sensitive_keys
        self.header_sensitive_prefixes = header_sensitive_prefixes
        self.header_sensitive_name_pattern = header_sensitive_name_pattern
        self.header_sensitive_cookie_keys = header_sensitive_cookie_keys
        # For testability: allow monkeypatching
        self._redact_body = redact_body
        self._redact_headers_func = redact_headers

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text, redacting sensitive data.

        Args
        ----
        record
            The log record to format.

        Returns
        -------
        str
            The formatted and redacted log record.
        """
        self._redact_headers(record)
        self._redact_message(record)
        return super().format(record)

    def _redact_headers(self, record: logging.LogRecord) -> None:
        headers: Mapping[str, str] | None = getattr(record, "headers", None)
        if headers is not None:
            try:
                redacted = self._redact_headers_func(
                    headers,
                    sensitive_keys=self.header_sensitive_keys,
                    sensitive_prefixes=self.header_sensitive_prefixes,
                    sensitive_name_pattern=self.header_sensitive_name_pattern,
                    sensitive_cookie_keys=self.header_sensitive_cookie_keys,
                )
                record.headers = redacted
            except Exception:
                pass

    def _redact_message(self, record: logging.LogRecord) -> None:
        """Redact the log message in-place on the record.

        Handles all input types robustly:
        - For bytes: always output '[REDACTED BODY]'
        - For dict/list: always output JSON string with only sensitive fields redacted
        - For string: if structured (JSON/form), redact and output JSON string; else, redact sensitive values in the string
        """
        # Prefer the original msg attribute for type checks
        orig_msg = getattr(record, "msg", None)
        msg = record.getMessage()
        content_type = getattr(record, "content_type", None)
        # Start with the original message so every branch updates ``redacted_msg``
        redacted_msg: Any = msg

        # 1. If the original message is bytes, always redact as '[REDACTED BODY]'
        if isinstance(orig_msg, bytes):
            redacted_msg = self._redact_binary(orig_msg)
        elif self._is_binary(msg):
            # msg is a str that is actually binary data, treat as redacted body
            redacted_msg = "[REDACTED BODY]"
        # 2. If the original message is dict or list, always redact and serialize to JSON
        elif isinstance(orig_msg, (dict, list)):
            redacted_msg = self._redact_structured(orig_msg, content_type)
        # 3. If the message is empty, redact as '[REDACTED]'
        elif self._is_empty(msg):
            redacted_msg = self._redact_empty(msg)
        # 4. If the message is structured (JSON/form), redact and output JSON string
        elif self._is_structured(msg, content_type):
            redacted_msg = self._redact_structured(msg, content_type)
        # 5. Otherwise treat it as a plain string and redact sensitive values
        else:
            redacted_msg = self._redact_plain_string(msg)
        # 6. Fallback: keep ``redacted_msg`` as the original message

        # Ensure the final message is always a string for logging
        # If _redact_structured returned a dict/list, always serialize to JSON
        if isinstance(redacted_msg, (dict, list)):
            import json

            record.msg = json.dumps(redacted_msg, ensure_ascii=False)
        else:
            record.msg = str(redacted_msg)
        record.args = ()

    def _is_binary(self, msg: Any) -> bool:
        return isinstance(msg, bytes)

    def _is_empty(self, msg: Any) -> bool:
        return msg == "" or msg is None

    def _is_structured(self, msg: Any, content_type: Any) -> bool:
        if isinstance(msg, (dict, list)):
            return True
        if isinstance(msg, str):
            if content_type and ("json" in str(content_type).lower() or "form" in str(content_type).lower()):
                return True
            stripped = msg.strip()
            if stripped.startswith("{") and stripped.endswith("}"):
                return True
            if stripped.startswith("[") and stripped.endswith("]"):
                return True
        return False

    def _redact_binary(self, msg: bytes) -> str:
        # Always redact binary data as '[REDACTED BODY]'
        return "[REDACTED BODY]"

    def _redact_empty(self, msg: Any) -> str:
        # Always output '[REDACTED]' for empty messages to ensure output is not empty
        return "[REDACTED]"

    def _redact_structured(self, msg: Any, content_type: Any) -> str:
        import json

        # If msg is a string and looks like JSON, always parse, redact, and serialize
        if isinstance(msg, str):
            stripped = msg.strip()
            is_json = (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]"))
            if is_json:
                try:
                    # Use redact_body directly on the string, which will parse, redact, and return a JSON string
                    redacted = self._redact_body(
                        msg,
                        content_type="application/json",
                        sensitive_keys_pattern=self.body_sensitive_keys_pattern,
                        sensitive_value_pattern=self.body_sensitive_value_pattern,
                    )
                    # If the result is a dict/list, serialize to JSON; if it's a string, return as is
                    if isinstance(redacted, (dict, list)):
                        return json.dumps(redacted, ensure_ascii=False)
                    return str(redacted)
                except Exception:
                    # If parsing or redaction fails, fallback to original string
                    return msg
        try:
            redacted = self._redact_body(
                msg,
                content_type=content_type,
                sensitive_keys_pattern=self.body_sensitive_keys_pattern,
                sensitive_value_pattern=self.body_sensitive_value_pattern,
            )

            # For dict/list input: always serialize to JSON
            if isinstance(msg, (dict, list)):
                return json.dumps(redacted, ensure_ascii=False)
            # For string input (e.g., form-encoded), return as string
            if isinstance(msg, str):
                # If redacted is a dict/list, serialize to JSON
                if isinstance(redacted, (dict, list)):
                    return json.dumps(redacted, ensure_ascii=False)
                # Otherwise, return as string
                return str(redacted)
            # Fallback: always return string
            return str(redacted)
        except Exception:
            # If redaction fails, fallback to original string for str input, '[REDACTED]' for dict/list
            if isinstance(msg, str):
                return msg
            return "[REDACTED]"

    def _redact_plain_string(self, msg: str) -> str:
        if self.body_sensitive_value_pattern:
            redacted = self.body_sensitive_value_pattern.sub(REDACTED_VALUE, msg)
            if "[REDACTED]" in redacted:
                return redacted
        return msg
