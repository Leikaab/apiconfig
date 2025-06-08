# -*- coding: utf-8 -*-
"""Utilities for redacting sensitive data from HTTP headers."""

import re
from collections.abc import Mapping
from typing import Dict, Final, List, Optional, Set, Tuple

# Default set of sensitive header keys (lowercase)
DEFAULT_SENSITIVE_HEADERS: Final[Set[str]] = {
    "authorization",
    "cookie",
    "set-cookie",
    "proxy-authorization",
}

# Default tuple of sensitive header prefixes (lowercase)
DEFAULT_SENSITIVE_HEADER_PREFIXES: Final[Tuple[str, ...]] = (
    "x-api-key",
    "x-auth-token",
)

# Default set of sensitive cookie keys (lowercase)
DEFAULT_SENSITIVE_COOKIE_KEYS: Final[Set[str]] = {
    "session",
    "token",
    "auth",
    "key",
    "secret",
    "password",
    "credential",
    "jwt",
}

# Placeholder value for redacted headers
REDACTED_VALUE: Final[str] = "[REDACTED]"


def redact_headers(
    headers: Mapping[str, str],
    sensitive_keys: Set[str] = DEFAULT_SENSITIVE_HEADERS,
    sensitive_prefixes: Tuple[str, ...] = DEFAULT_SENSITIVE_HEADER_PREFIXES,
    sensitive_name_pattern: Optional[re.Pattern[str]] = None,
    sensitive_cookie_keys: Set[str] = DEFAULT_SENSITIVE_COOKIE_KEYS,
) -> Dict[str, str]:
    """Redact sensitive information from HTTP headers.

    Iterates through a mapping of headers, identifies sensitive headers based on
    predefined keys, prefixes (case-insensitive), or a regex pattern for the
    header name, and replaces their values with a placeholder string.

    Special handling is provided for multi-value headers like `Cookie` and `Set-Cookie`,
    where only the sensitive values within these headers are redacted while preserving
    the structure and non-sensitive parts.

    Args
    ----
    headers
        A mapping (e.g., dictionary) of header names to values.
    sensitive_keys
        A set of lowercase header names to consider sensitive.
        Defaults to `DEFAULT_SENSITIVE_HEADERS`.
    sensitive_prefixes
        A tuple of lowercase header prefixes to consider sensitive.
        Defaults to `DEFAULT_SENSITIVE_HEADER_PREFIXES`.
    sensitive_name_pattern
        An optional compiled regex pattern. If provided,
        header names matching this pattern (case-insensitive)
        will also be redacted. Defaults to `None`.
    sensitive_cookie_keys
        A set of lowercase cookie names to consider sensitive.
        Defaults to `DEFAULT_SENSITIVE_COOKIE_KEYS`.

    Returns
    -------
    Dict[str, str]
        A new dictionary containing the headers with sensitive values redacted.
        Returns an empty dictionary if the input `headers` is None or empty.
    """
    redacted_headers: Dict[str, str] = {}
    if not headers:
        return redacted_headers

    for name, value in headers.items():
        lower_name = name.lower()
        is_sensitive_by_key = lower_name in sensitive_keys
        is_sensitive_by_prefix = lower_name.startswith(sensitive_prefixes)
        is_sensitive_by_pattern = bool(sensitive_name_pattern and sensitive_name_pattern.search(name))

        is_sensitive = is_sensitive_by_key or is_sensitive_by_prefix or is_sensitive_by_pattern

        # Ensure value is treated as a string for consistency
        value_str = str(value)

        # Special handling for multi-value headers
        if is_sensitive and lower_name == "cookie":
            redacted_headers[name] = _redact_cookie_header(value_str, sensitive_cookie_keys)
        elif is_sensitive and lower_name == "set-cookie":
            redacted_headers[name] = _redact_set_cookie_header(value_str, sensitive_cookie_keys)
        else:
            redacted_headers[name] = REDACTED_VALUE if is_sensitive else value_str

    return redacted_headers


def _redact_cookie_header(cookie_value: str, sensitive_keys: Set[str]) -> str:
    """Redact sensitive values from a Cookie header while preserving its structure.

    Args
    ----
    cookie_value
        The value of the Cookie header (e.g., "name=value; other=value2").
    sensitive_keys
        A set of lowercase cookie names to consider sensitive.

    Returns
    -------
    str
        A string with sensitive cookie values redacted.
    """
    if not cookie_value:
        return cookie_value

    # Split the cookie string into individual cookies
    cookies: List[str] = cookie_value.split(";")
    redacted_cookies: List[str] = []

    for i, cookie in enumerate(cookies):
        # Skip empty segments
        if not cookie.strip():
            redacted_cookies.append(cookie)
            continue

        # Split each cookie into name and value
        parts = cookie.split("=", 1)
        if len(parts) < 2:
            # If there's no equals sign, just keep the cookie as is
            redacted_cookies.append(cookie)
            continue

        name, value = parts[0].strip(), parts[1]

        # Check if this cookie name is sensitive and value is not empty
        if (
            name.lower() in sensitive_keys or any(name.lower().startswith(prefix) for prefix in ["auth", "token", "key", "secret"])
        ) and value.strip():
            redacted_cookies.append(f"{name}={REDACTED_VALUE}")
        else:
            redacted_cookies.append(f"{name}={value}")

    # Join the cookies back together, preserving the original separators
    result = ""
    for i, cookie in enumerate(redacted_cookies):
        if i > 0:
            # Use the original separator (semicolon + original whitespace)
            original_separator = cookies[i]
            whitespace_prefix = ""
            for char in original_separator:
                if char.isspace():
                    whitespace_prefix += char
                else:
                    break
            result += ";" + whitespace_prefix
        result += cookie

    return result


def _redact_set_cookie_header(set_cookie_value: str, sensitive_keys: Set[str]) -> str:
    """Redact sensitive values from a Set-Cookie header while preserving its attributes.

    Args
    ----
    set_cookie_value
        The value of the Set-Cookie header
        (e.g., "name=value; Path=/; HttpOnly").
    sensitive_keys
        A set of lowercase cookie names to consider sensitive.

    Returns
    -------
    str
        A string with sensitive cookie values redacted but attributes preserved.
    """
    if not set_cookie_value:
        return set_cookie_value

    # Split the Set-Cookie value into the main cookie and its attributes
    parts = set_cookie_value.split(";", 1)
    main_cookie = parts[0].strip()
    attributes = parts[1].strip() if len(parts) > 1 else ""

    # Split the main cookie into name and value
    cookie_parts = main_cookie.split("=", 1)
    if len(cookie_parts) < 2:
        # If there's no equals sign, just return the original value
        return set_cookie_value

    name, value = cookie_parts[0].strip(), cookie_parts[1]

    # Check if this cookie name is sensitive and value is not empty
    if (name.lower() in sensitive_keys or any(name.lower().startswith(prefix) for prefix in ["auth", "token", "key", "secret"])) and value.strip():
        redacted_main_cookie = f"{name}={REDACTED_VALUE}"
    else:
        redacted_main_cookie = main_cookie

    # Reconstruct the Set-Cookie value with attributes
    if attributes:
        return f"{redacted_main_cookie}; {attributes}"
    else:
        return redacted_main_cookie
