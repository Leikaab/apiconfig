import json
import re
from typing import Any, Optional, Pattern, Union

import pytest

from apiconfig.utils.redaction.body import (
    DEFAULT_SENSITIVE_KEYS_PATTERN,
    REDACTED_BODY_PLACEHOLDER,
    redact_body,
)
from apiconfig.utils.redaction.headers import REDACTED_VALUE  # Import from headers

# --- Test Data ---

SENSITIVE_KEY_PATTERN = DEFAULT_SENSITIVE_KEYS_PATTERN
SENSITIVE_VALUE_PATTERN_EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
SENSITIVE_VALUE_PATTERN_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)


# --- Test Cases ---


@pytest.mark.parametrize(
    "body, content_type, key_pattern, value_pattern, expected_output",
    [
        # --- JSON Redaction (Keys Only - Default) ---
        (
            '{"password": "secret123", "username": "user"}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            None,
            f'{{"password": "{REDACTED_VALUE}", "username": "user"}}',
        ),
        (
            '{"data": {"session_token": "abc", "value": 1}}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            None,
            f'{{"data": {{"session_token": "{REDACTED_VALUE}", "value": 1}}}}',
        ),
        (
            '[{"user_key": "xyz"}, {"id": 1}]',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            None,
            f'[{{"user_key": "{REDACTED_VALUE}"}}, {{"id": 1}}]',
        ),
        (
            '{"normal": "value"}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            None,
            '{"normal": "value"}',
        ),
        # --- Form Redaction (Keys Only - Default) ---
        (
            "password=secret123&username=user",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            None,
            "password=%5BREDACTED%5D&username=user",  # Use URL encoded value
        ),
        (
            "data.session_token=abc&data.value=1",  # Note: parse_qs doesn't handle nested keys well
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            None,
            "data.session_token=%5BREDACTED%5D&data.value=1",  # Use URL encoded value
        ),
        (
            "user_key=xyz&id=1",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            None,
            "user_key=%5BREDACTED%5D&id=1",  # Use URL encoded value
        ),
        (
            "normal=value&another=test",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            None,
            "normal=value&another=test",
        ),
        # --- JSON Redaction (Value Pattern - Email) ---
        (
            '{"email": "test@example.com", "user_id": 1}',
            "application/json",
            SENSITIVE_KEY_PATTERN,  # No sensitive keys
            SENSITIVE_VALUE_PATTERN_EMAIL,
            f'{{"email": "{REDACTED_VALUE}", "user_id": 1}}',  # Value redacted
        ),
        (
            '{"contact": {"primary_email": "info@test.dev"}, "secondary": "other@domain.org"}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            f'{{"contact": {{"primary_email": "{REDACTED_VALUE}"}}, "secondary": "{REDACTED_VALUE}"}}',
        ),
        (
            '{"password": "secret", "email": "admin@example.com"}',  # Both key and value sensitive
            "application/json",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            f'{{"password": "{REDACTED_VALUE}", "email": "{REDACTED_VALUE}"}}',  # Key redaction takes precedence, value also matches
        ),
        (
            '{"message": "This is not an email"}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            '{"message": "This is not an email"}',  # No value match
        ),
        # --- Form Redaction (Value Pattern - Email) ---
        (
            "email=test@example.com&user_id=1",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,  # No sensitive keys
            SENSITIVE_VALUE_PATTERN_EMAIL,
            "email=%5BREDACTED%5D&user_id=1",  # Use URL encoded value
        ),
        (
            "primary_email=info@test.dev&secondary=other@domain.org",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            "primary_email=%5BREDACTED%5D&secondary=%5BREDACTED%5D",  # Use URL encoded value
        ),
        (
            "password=secret&email=admin@example.com",  # Both key and value sensitive - Remove f-string
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            "password=%5BREDACTED%5D&email=%5BREDACTED%5D",  # Use URL encoded value
        ),
        (
            "message=This+is+not+an+email",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            "message=This+is+not+an+email",  # No value match
        ),
        # --- JSON Redaction (Value Pattern - UUID) ---
        (
            '{"request_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "status": "ok"}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_UUID,
            f'{{"request_id": "{REDACTED_VALUE}", "status": "ok"}}',
        ),
        # --- Form Redaction (Value Pattern - UUID) ---
        (
            "request_id=a1b2c3d4-e5f6-7890-1234-567890abcdef&status=ok",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_UUID,
            "request_id=%5BREDACTED%5D&status=ok",  # Use URL encoded value
        ),
        # --- Edge Cases ---
        (None, "application/json", SENSITIVE_KEY_PATTERN, None, None),
        ("", "application/json", SENSITIVE_KEY_PATTERN, None, ""),
        ("{}", "application/json", SENSITIVE_KEY_PATTERN, None, "{}"),
        ("[]", "application/json", SENSITIVE_KEY_PATTERN, None, "[]"),
        ("", "application/x-www-form-urlencoded", SENSITIVE_KEY_PATTERN, None, ""),
        (
            b'{"password": "secret"}',
            "application/json",
            SENSITIVE_KEY_PATTERN,
            None,
            f'{{"password": "{REDACTED_VALUE}"}}'.encode("utf-8"),
        ),
        (
            b"password=secret",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            None,
            "password=%5BREDACTED%5D".encode("utf-8"),
        ),  # Use URL encoded value
        (
            b"\x80abc",
            None,
            SENSITIVE_KEY_PATTERN,
            None,
            REDACTED_BODY_PLACEHOLDER,
        ),  # Binary data
        (
            "not json",
            "application/json",
            SENSITIVE_KEY_PATTERN,
            None,
            "not json",
        ),  # Unparseable JSON
        (
            "a=b=c",
            "application/x-www-form-urlencoded",
            SENSITIVE_KEY_PATTERN,
            None,
            "a=b%3Dc",
        ),  # Unparseable form (sort of)
        (
            {"password": "secret", "user": "test"},
            None,
            SENSITIVE_KEY_PATTERN,
            None,
            {"password": REDACTED_VALUE, "user": "test"},
        ),  # Already parsed dict
        (
            [{"auth_token": "abc"}],
            None,
            SENSITIVE_KEY_PATTERN,
            None,
            [{"auth_token": REDACTED_VALUE}],
        ),  # Already parsed list
        (
            {"email": "test@example.com"},
            None,
            SENSITIVE_KEY_PATTERN,
            SENSITIVE_VALUE_PATTERN_EMAIL,
            {"email": REDACTED_VALUE},
        ),  # Already parsed dict with value pattern
        (
            123,
            None,
            SENSITIVE_KEY_PATTERN,
            None,
            123,
        ),  # Non-string/bytes/dict/list body
    ],
)
def test_redact_body(
    body: Union[str, bytes, Any],
    content_type: Optional[str],
    key_pattern: Pattern[str],
    value_pattern: Optional[Pattern[str]],
    expected_output: Union[str, bytes, Any],
) -> None:
    """Tests the redact_body function with various inputs and patterns."""
    result = redact_body(
        body=body,
        content_type=content_type,
        sensitive_keys_pattern=key_pattern,
        sensitive_value_pattern=value_pattern,
    )

    # Handle comparison for JSON strings where key order might differ
    if isinstance(expected_output, str) and content_type == "application/json" and expected_output.startswith(("{", "[")):
        try:
            assert json.loads(result) == json.loads(expected_output)
        except (json.JSONDecodeError, TypeError):
            pytest.fail(f"Failed to compare JSON: result={result!r}, expected={expected_output!r}")  # Should not happen if expected is valid JSON
    # Handle comparison for form-urlencoded strings where param order might differ
    elif isinstance(expected_output, str) and content_type == "application/x-www-form-urlencoded":
        # Simple comparison works if urlencode produces consistent order,
        # otherwise more complex parsing/comparison might be needed.
        # For these tests, direct string comparison should suffice.
        assert result == expected_output
    # Handle bytes comparison - result might be string if decoded and redacted
    elif isinstance(expected_output, bytes):
        if isinstance(result, str):
            # Compare decoded expected output with string result
            try:
                assert result == expected_output.decode("utf-8")
            except UnicodeDecodeError:
                pytest.fail(f"Could not decode expected bytes for comparison: {expected_output!r}")
        elif isinstance(result, bytes):
            # If result is still bytes (e.g., binary data placeholder), compare directly
            assert result == expected_output
        else:
            # Should not happen based on function logic
            pytest.fail(f"Unexpected result type {type(result)} when expecting bytes.")
    # Handle already parsed data (dicts/lists)
    elif isinstance(expected_output, (dict, list)):
        assert result == expected_output
    # Handle None or other types
    else:
        assert result == expected_output


def test_redact_body_defaults() -> None:
    """Tests redact_body uses default key pattern."""
    body = '{"password": "secret", "user": "test"}'
    content_type = "application/json"
    expected = f'{{"password": "{REDACTED_VALUE}", "user": "test"}}'
    result = redact_body(body=body, content_type=content_type)
    assert json.loads(result) == json.loads(expected)


def test_redact_body_no_content_type_json_like() -> None:
    """Tests redaction when body is dict/list and content_type is None."""
    body = {"session_token": "abc", "data": [1, 2]}
    expected = {"session_token": REDACTED_VALUE, "data": [1, 2]}
    result = redact_body(body=body, content_type=None)  # Should assume JSON
    assert result == expected


def test_redact_body_no_content_type_string() -> None:
    """Tests no redaction when body is string and content_type is None."""
    body = '{"password": "secret"}'  # Looks like JSON, but no content type
    expected = '{"password": "secret"}'
    result = redact_body(body=body, content_type=None)
    assert result == expected
