import re
from typing import Dict, Set, Tuple

import pytest

from apiconfig.utils.redaction.headers import (
    DEFAULT_SENSITIVE_COOKIE_KEYS,
    DEFAULT_SENSITIVE_HEADER_PREFIXES,
    DEFAULT_SENSITIVE_HEADERS,
    REDACTED_VALUE,
    _redact_cookie_header,
    _redact_set_cookie_header,
    redact_headers,
)

# Test Cases for redact_headers


@pytest.mark.parametrize(
    "input_headers, expected_headers, sensitive_keys, sensitive_prefixes, sensitive_name_pattern",
    [
        # --- Default Behavior ---
        (
            {"Authorization": "Bearer 123", "Content-Type": "application/json"},
            {"Authorization": REDACTED_VALUE, "Content-Type": "application/json"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            None,
        ),
        (
            {"Cookie": "session=abc", "Accept": "text/html"},
            {"Cookie": "session=[REDACTED]", "Accept": "text/html"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            None,
        ),
        (
            {"X-API-Key": "secretkey", "User-Agent": "MyApp"},
            {"X-API-Key": REDACTED_VALUE, "User-Agent": "MyApp"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            None,
        ),
        (
            {"Normal-Header": "value1", "Another-Header": "value2"},
            {"Normal-Header": "value1", "Another-Header": "value2"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            None,
        ),
        ({}, {}, DEFAULT_SENSITIVE_HEADERS, DEFAULT_SENSITIVE_HEADER_PREFIXES, None),
        (None, {}, DEFAULT_SENSITIVE_HEADERS, DEFAULT_SENSITIVE_HEADER_PREFIXES, None),
        # --- Custom Keys/Prefixes ---
        (
            {"My-Secret": "123", "Public-Info": "abc"},
            {"My-Secret": REDACTED_VALUE, "Public-Info": "abc"},
            {"my-secret"},
            (),
            None,
        ),
        (
            {"Custom-Auth": "xyz", "Data": "123"},
            {"Custom-Auth": REDACTED_VALUE, "Data": "123"},
            set(),
            ("custom-",),
            None,
        ),
        # --- Case Insensitivity ---
        (
            {"authorization": "Bearer 123", "content-type": "application/json"},
            {"authorization": REDACTED_VALUE, "content-type": "application/json"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            None,
        ),
        (
            {"x-api-key": "secretkey", "user-agent": "MyApp"},
            {"x-api-key": REDACTED_VALUE, "user-agent": "MyApp"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            None,
        ),
        # --- New: Sensitive Name Pattern ---
        (
            {"Authorization": "Bearer 123", "X-Request-ID": "uuid-1"},
            {"Authorization": REDACTED_VALUE, "X-Request-ID": "uuid-1"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            re.compile(r"Session-ID", re.IGNORECASE),  # No match
        ),
        (
            {"Session-ID": "abc-123", "Content-Type": "application/json"},
            {"Session-ID": REDACTED_VALUE, "Content-Type": "application/json"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            re.compile(r"Session-ID", re.IGNORECASE),  # Match
        ),
        (
            {"session-id": "xyz-456", "Accept": "*/*"},
            {"session-id": REDACTED_VALUE, "Accept": "*/*"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            re.compile(r"Session-ID", re.IGNORECASE),  # Match (case-insensitive)
        ),
        (
            {"Authorization": "token", "My-Custom-Secret-Data": "value"},
            {"Authorization": REDACTED_VALUE, "My-Custom-Secret-Data": REDACTED_VALUE},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            re.compile(r"Secret", re.IGNORECASE),  # Match pattern
        ),
        (
            {"Authorization": "token", "My-Custom-Data": "value"},
            {"Authorization": REDACTED_VALUE, "My-Custom-Data": "value"},
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            re.compile(r"Secret", re.IGNORECASE),  # No pattern match
        ),
        # --- Combination ---
        (
            {
                "Authorization": "token",  # Default key
                "X-API-Key": "key",  # Default prefix
                "User-Secret-Token": "abc",  # Pattern match
                "Public-Data": "123",  # No match
            },
            {
                "Authorization": REDACTED_VALUE,
                "X-API-Key": REDACTED_VALUE,
                "User-Secret-Token": REDACTED_VALUE,
                "Public-Data": "123",
            },
            DEFAULT_SENSITIVE_HEADERS,
            DEFAULT_SENSITIVE_HEADER_PREFIXES,
            re.compile(r"Secret", re.IGNORECASE),
        ),
    ],
)
def test_redact_headers(
    input_headers: Dict[str, str],
    expected_headers: Dict[str, str],
    sensitive_keys: Set[str],
    sensitive_prefixes: Tuple[str, ...],
    sensitive_name_pattern: re.Pattern[str] | None,
) -> None:
    """Tests the redact_headers function with various inputs."""
    result = redact_headers(
        headers=input_headers,
        sensitive_keys=sensitive_keys,
        sensitive_prefixes=sensitive_prefixes,
        sensitive_name_pattern=sensitive_name_pattern,
    )
    assert result == expected_headers


# Test that defaults are used correctly


def test_redact_headers_defaults() -> None:
    """Tests that default sensitive keys and prefixes are used."""
    input_headers = {"Authorization": "Bearer 123", "X-API-Key": "secret"}
    expected_headers = {"Authorization": REDACTED_VALUE, "X-API-Key": REDACTED_VALUE}
    result = redact_headers(input_headers)
    assert result == expected_headers


# Test that input dictionary is not modified


def test_redact_headers_immutable() -> None:
    """Tests that the original headers dictionary is not modified."""
    input_headers = {"Authorization": "Bearer 123", "Content-Type": "application/json"}
    input_copy = input_headers.copy()
    redact_headers(input_headers)  # Call the function
    assert input_headers == input_copy  # Check if original is unchanged


# New tests for multi-value header redaction


@pytest.mark.parametrize(
    "cookie_value, expected_result",
    [
        # Simple cookie
        ("session=abc123", "session=[REDACTED]"),
        # Multiple cookies
        (
            "session=abc123; user=john; theme=dark",
            "session=[REDACTED]; user=john; theme=dark",
        ),
        # Multiple sensitive cookies
        (
            "session=abc123; token=xyz789; theme=dark",
            "session=[REDACTED]; token=[REDACTED]; theme=dark",
        ),
        # Cookies with spaces
        (
            "session=abc123;  token=xyz789;  theme=dark",
            "session=[REDACTED];  token=[REDACTED];  theme=dark",
        ),
        # Empty cookie value
        ("", ""),
        # Cookie without value
        ("session", "session"),
        # Cookie with empty value
        ("session=", "session="),
        # Cookie with special characters
        (
            "session=abc%20123; user=john@example.com",
            "session=[REDACTED]; user=john@example.com",
        ),
        # Custom sensitive cookie
        (
            "custom_secret=value; public=ok",
            "custom_secret=value; public=ok",
        ),
        # Cookie with prefix matching
        (
            "auth_token=value; public=ok",
            "auth_token=[REDACTED]; public=ok",
        ),
    ],
)
def test_redact_cookie_header(cookie_value: str, expected_result: str) -> None:
    """Tests the _redact_cookie_header function with various inputs."""
    result = _redact_cookie_header(cookie_value, DEFAULT_SENSITIVE_COOKIE_KEYS)
    assert result == expected_result


@pytest.mark.parametrize(
    "set_cookie_value, expected_result",
    [
        # Simple Set-Cookie
        ("session=abc123", "session=[REDACTED]"),
        # Set-Cookie with attributes
        (
            "session=abc123; Path=/; HttpOnly; Secure",
            "session=[REDACTED]; Path=/; HttpOnly; Secure",
        ),
        # Set-Cookie with Expires and Domain
        (
            "token=xyz789; Expires=Wed, 21 Oct 2025 07:28:00 GMT; Domain=example.com",
            "token=[REDACTED]; Expires=Wed, 21 Oct 2025 07:28:00 GMT; Domain=example.com",
        ),
        # Set-Cookie with Max-Age
        (
            "auth=secret; Max-Age=3600; Path=/api",
            "auth=[REDACTED]; Max-Age=3600; Path=/api",
        ),
        # Empty Set-Cookie value
        ("", ""),
        # Set-Cookie without value
        ("session", "session"),
        # Set-Cookie with empty value
        ("session=", "session="),
        # Set-Cookie with special characters
        (
            "session=abc%20123; Path=/",
            "session=[REDACTED]; Path=/",
        ),
        # Non-sensitive cookie
        (
            "theme=dark; Path=/; HttpOnly",
            "theme=dark; Path=/; HttpOnly",
        ),
        # Cookie with prefix matching
        (
            "auth_token=value; Path=/",
            "auth_token=[REDACTED]; Path=/",
        ),
    ],
)
def test_redact_set_cookie_header(set_cookie_value: str, expected_result: str) -> None:
    """Tests the _redact_set_cookie_header function with various inputs."""
    result = _redact_set_cookie_header(set_cookie_value, DEFAULT_SENSITIVE_COOKIE_KEYS)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_headers, expected_headers",
    [
        # Cookie header with multiple values
        (
            {"Cookie": "session=abc123; user=john; token=xyz789"},
            {"Cookie": "session=[REDACTED]; user=john; token=[REDACTED]"},
        ),
        # Set-Cookie header with attributes
        (
            {"Set-Cookie": "session=abc123; Path=/; HttpOnly; Secure"},
            {"Set-Cookie": "session=[REDACTED]; Path=/; HttpOnly; Secure"},
        ),
        # Multiple headers including Cookie and Set-Cookie
        (
            {
                "Authorization": "Bearer token123",
                "Cookie": "session=abc; theme=dark",
                "Set-Cookie": "token=xyz; Path=/",
                "Content-Type": "application/json",
            },
            {
                "Authorization": REDACTED_VALUE,
                "Cookie": "session=[REDACTED]; theme=dark",
                "Set-Cookie": "token=[REDACTED]; Path=/",
                "Content-Type": "application/json",
            },
        ),
        # Case insensitivity for header names
        (
            {
                "cookie": "session=abc; theme=dark",
                "set-cookie": "token=xyz; Path=/",
            },
            {
                "cookie": "session=[REDACTED]; theme=dark",
                "set-cookie": "token=[REDACTED]; Path=/",
            },
        ),
        # Custom sensitive cookie keys
        (
            {"Cookie": "custom=value; session=abc"},
            {"Cookie": "custom=value; session=[REDACTED]"},
        ),
    ],
)
def test_redact_headers_multi_value(
    input_headers: Dict[str, str], expected_headers: Dict[str, str]
) -> None:
    """Tests the redact_headers function with multi-value headers."""
    result = redact_headers(input_headers)
    assert result == expected_headers


def test_redact_headers_with_custom_cookie_keys() -> None:
    """Tests redact_headers with custom sensitive cookie keys."""
    input_headers = {"Cookie": "custom=value; session=abc"}
    custom_cookie_keys = {"custom"}
    expected_headers = {"Cookie": "custom=[REDACTED]; session=abc"}

    result = redact_headers(input_headers, sensitive_cookie_keys=custom_cookie_keys)
    assert result == expected_headers


def test_redact_cookie_header_with_custom_keys() -> None:
    """Tests _redact_cookie_header with custom sensitive keys."""
    cookie_value = "custom=value; public=ok"
    custom_keys = {"custom"}
    expected_result = "custom=[REDACTED]; public=ok"

    result = _redact_cookie_header(cookie_value, custom_keys)
    assert result == expected_result


def test_redact_set_cookie_header_with_custom_keys() -> None:
    """Tests _redact_set_cookie_header with custom sensitive keys."""
    set_cookie_value = "custom=value; Path=/"
    custom_keys = {"custom"}
    expected_result = "custom=[REDACTED]; Path=/"

    result = _redact_set_cookie_header(set_cookie_value, custom_keys)
    assert result == expected_result
