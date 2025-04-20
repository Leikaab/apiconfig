import re
from typing import Dict, Set, Tuple

import pytest

from apiconfig.utils.redaction.headers import DEFAULT_SENSITIVE_HEADER_PREFIXES, DEFAULT_SENSITIVE_HEADERS, REDACTED_VALUE, redact_headers

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
            {"Cookie": REDACTED_VALUE, "Accept": "text/html"},
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
