import re
from collections.abc import Mapping
from typing import Dict, Final, Optional, Set, Tuple

# Default set of sensitive header keys (lowercase)
DEFAULT_SENSITIVE_HEADERS: Final[Set[str]]

# Default tuple of sensitive header prefixes (lowercase)
DEFAULT_SENSITIVE_HEADER_PREFIXES: Final[Tuple[str, ...]]

# Default set of sensitive cookie keys (lowercase)
DEFAULT_SENSITIVE_COOKIE_KEYS: Final[Set[str]]

# Placeholder value for redacted headers
REDACTED_VALUE: Final[str]

def redact_headers(
    headers: Mapping[str, str],
    sensitive_keys: Set[str] = ...,
    sensitive_prefixes: Tuple[str, ...] = ...,
    sensitive_name_pattern: Optional[re.Pattern[str]] = ...,
    sensitive_cookie_keys: Set[str] = ...,
) -> Dict[str, str]:
    """
    Redacts sensitive information from HTTP headers.

    Iterates through a mapping of headers, identifies sensitive headers based on
    predefined keys, prefixes (case-insensitive), or a regex pattern for the
    header name, and replaces their values with a placeholder string.

    Special handling is provided for multi-value headers like `Cookie` and `Set-Cookie`,
    where only the sensitive values within these headers are redacted while preserving
    the structure and non-sensitive parts.

    Args:
        headers: A mapping (e.g., dictionary) of header names to values.
        sensitive_keys: A set of lowercase header names to consider sensitive.
                        Defaults to `DEFAULT_SENSITIVE_HEADERS`.
        sensitive_prefixes: A tuple of lowercase header prefixes to consider sensitive.
                            Defaults to `DEFAULT_SENSITIVE_HEADER_PREFIXES`.
        sensitive_name_pattern: An optional compiled regex pattern. If provided,
                                header names matching this pattern (case-insensitive)
                                will also be redacted. Defaults to `None`.
        sensitive_cookie_keys: A set of lowercase cookie names to consider sensitive.
                               Defaults to `DEFAULT_SENSITIVE_COOKIE_KEYS`.

    Returns:
        A new dictionary containing the headers with sensitive values redacted.
        Returns an empty dictionary if the input `headers` is None or empty.
    """
    ...

def _redact_cookie_header(cookie_value: str, sensitive_keys: Set[str]) -> str:
    """
    Redacts sensitive values from a Cookie header while preserving its structure.

    Args:
        cookie_value: The value of the Cookie header (e.g., "name=value; other=value2").
        sensitive_keys: A set of lowercase cookie names to consider sensitive.

    Returns:
        A string with sensitive cookie values redacted.
    """
    ...

def _redact_set_cookie_header(set_cookie_value: str, sensitive_keys: Set[str]) -> str:
    """
    Redacts sensitive values from a Set-Cookie header while preserving its attributes.

    Args:
        set_cookie_value: The value of the Set-Cookie header
                         (e.g., "name=value; Path=/; HttpOnly").
        sensitive_keys: A set of lowercase cookie names to consider sensitive.

    Returns:
        A string with sensitive cookie values redacted but attributes preserved.
    """
    ...
