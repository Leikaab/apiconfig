"""Unit tests for apiconfig.utils.http module."""

from typing import Any

import pytest

from apiconfig.exceptions.base import APIConfigError
from apiconfig.utils.http import (
    HTTPUtilsError,
    JSONDecodeError,
    JSONEncodeError,
    PayloadTooLargeError,
    get_header_value,
    is_client_error,
    is_redirect,
    is_server_error,
    is_success,
    normalize_header_name,
    safe_json_decode,
    safe_json_encode,
)


# --- Status Code Tests ---
@pytest.mark.parametrize(
    "code, expected",
    [
        (200, True),
        (201, True),
        (299, True),
        (199, False),
        (300, False),
        (400, False),
    ],
)
def test_is_success(code: int, expected: bool) -> None:
    """Verify the is_success function correctly identifies success status codes."""
    assert is_success(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        (300, True),
        (301, True),
        (308, True),
        (399, True),
        (299, False),
        (400, False),
    ],
)
def test_is_redirect(code: int, expected: bool) -> None:
    """Verify the is_redirect function correctly identifies redirect status codes."""
    assert is_redirect(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        (400, True),
        (404, True),
        (499, True),
        (399, False),
        (500, False),
        (200, False),
    ],
)
def test_is_client_error(code: int, expected: bool) -> None:
    """Verify the is_client_error function correctly identifies client error status codes."""
    assert is_client_error(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        (500, True),
        (503, True),
        (599, True),
        (499, False),
        (600, False),
        (200, False),
    ],
)
def test_is_server_error(code: int, expected: bool) -> None:
    """Verify the is_server_error function correctly identifies server error status codes."""
    assert is_server_error(code) == expected


# --- Header Normalization Tests ---
@pytest.mark.parametrize(
    "name, expected",
    [
        ("content-type", "Content-Type"),
        ("CONTENT-LENGTH", "Content-Length"),
        ("x-custom-header", "X-Custom-Header"),
        ("Authorization", "Authorization"),
        ("single", "Single"),
    ],
)
def test_normalize_header_name(name: str, expected: str) -> None:
    """Verify the normalize_header_name function correctly normalizes header names."""
    assert normalize_header_name(name) == expected


# --- Get Header Value Tests ---
@pytest.mark.parametrize(
    "headers, name, default, expected",
    [
        (
            {"Content-Type": "application/json"},
            "content-type",
            None,
            "application/json",
        ),
        ({"content-length": "100"}, "Content-Length", None, "100"),
        ({"X-API-Key": "123"}, "x-api-key", None, "123"),
        ({"Auth": "Bearer token"}, "AUTH", None, "Bearer token"),
        ({"Header1": "Value1"}, "header1", None, "Value1"),
        ({"Header1": "Value1"}, "NonExistent", "default_val", "default_val"),
        ({}, "AnyHeader", None, None),
        ({"Multi-Part-Header": "value"}, "multi-part-header", None, "value"),
    ],
)
def test_get_header_value(headers: dict[str, str], name: str, default: str | None, expected: str | None) -> None:
    """Verify the get_header_value function correctly retrieves header values, including handling case-insensitivity and defaults."""
    assert get_header_value(headers, name, default=default) == expected


# --- Safe JSON Decode Tests ---
@pytest.mark.parametrize(
    "content, encoding, expected",
    [
        ('{"key": "value"}', None, {"key": "value"}),
        (b'{"bytes": true}', None, {"bytes": True}),
        (b'{"enc": "\xc3\xa9"}', "utf-8", {"enc": "é"}),
        ("", None, None),
        (b"", None, None),
        ("   ", None, None),  # Test whitespace only
        ('{"nested": {"num": 1}}', None, {"nested": {"num": 1}}),
    ],
)
def test_safe_json_decode_success(content: str | bytes, encoding: str | None, expected: dict[str, Any] | None) -> None:
    """Verify the safe_json_decode function successfully decodes valid JSON content."""
    assert safe_json_decode(content, encoding=encoding) == expected


@pytest.mark.parametrize(
    "content, encoding, expected_exception, match",
    [
        ("{invalid json", None, JSONDecodeError, "Failed to decode JSON"),
        (
            b"\x80abc",
            "utf-8",
            JSONDecodeError,
            "Failed to decode response body",
        ),  # Invalid UTF-8 start byte
        # Removed problematic test case: (b'{"key": "value"}', "ascii", JSONDecodeError, "Failed to decode response body"),
        (
            123,
            None,
            HTTPUtilsError,
            "An unexpected error occurred",
        ),  # Invalid input type
    ],
)
def test_safe_json_decode_failure(
    content: Any,
    encoding: str | None,
    expected_exception: type[APIConfigError],
    match: str,
) -> None:
    """Verify the safe_json_decode function raises the correct exceptions for invalid input or decoding errors."""
    with pytest.raises(expected_exception, match=match):
        safe_json_decode(content, encoding=encoding)


# --- Payload Size Tests ---
def test_safe_json_decode_with_custom_max_size() -> None:
    """Test that safe_json_decode works with a custom max_size_bytes."""
    # Small payload with small limit should work
    small_payload = '{"key": "value"}'
    assert safe_json_decode(small_payload, max_size_bytes=100) == {"key": "value"}

    # Same for bytes
    small_payload_bytes = b'{"key": "value"}'
    assert safe_json_decode(small_payload_bytes, max_size_bytes=100) == {"key": "value"}


def test_safe_json_decode_at_size_limit() -> None:
    """Test that safe_json_decode works with a payload exactly at the size limit."""
    # Create a payload that's exactly 19 bytes when UTF-8 encoded
    payload = '{"x": "' + "a" * 10 + '"}'  # 19 bytes when UTF-8 encoded
    assert len(payload.encode("utf-8")) == 19

    # Should work with max_size_bytes=19
    assert safe_json_decode(payload, max_size_bytes=19) == {"x": "a" * 10}

    # Same for bytes
    payload_bytes = payload.encode("utf-8")
    assert len(payload_bytes) == 19
    assert safe_json_decode(payload_bytes, max_size_bytes=19) == {"x": "a" * 10}


def test_safe_json_decode_exceeds_size_limit_string() -> None:
    """Test that safe_json_decode raises PayloadTooLargeError for string payloads exceeding the limit."""
    # Create a payload that's larger than the limit
    large_payload = '{"large": "' + "a" * 100 + '"}'

    with pytest.raises(PayloadTooLargeError, match="Payload size .* exceeds maximum allowed size"):
        safe_json_decode(large_payload, max_size_bytes=50)


# --- Safe JSON Encode Tests ---
@pytest.mark.parametrize(
    "data, ensure_ascii, indent, expected",
    [
        ({"key": "value"}, False, None, '{"key": "value"}'),
        ({"number": 42}, False, None, '{"number": 42}'),
        ({"bool": True}, False, None, '{"bool": true}'),
        ({"null": None}, False, None, '{"null": null}'),
        ({"list": [1, 2, 3]}, False, None, '{"list": [1, 2, 3]}'),
        ({"nested": {"key": "value"}}, False, None, '{"nested": {"key": "value"}}'),
        ({"unicode": "café"}, False, None, '{"unicode": "café"}'),
        ({"unicode": "café"}, True, None, '{"unicode": "caf\\u00e9"}'),
        ({"key": "value"}, False, 2, '{\n  "key": "value"\n}'),
    ],
)
def test_safe_json_encode_success(data: Any, ensure_ascii: bool, indent: int | None, expected: str) -> None:
    """Verify the safe_json_encode function successfully encodes valid data."""
    result = safe_json_encode(data, ensure_ascii=ensure_ascii, indent=indent)
    assert result == expected


def test_safe_json_encode_with_custom_max_size() -> None:
    """Test that safe_json_encode works with a custom max_size_bytes."""
    # Small data with small limit should work
    small_data = {"key": "value"}
    result = safe_json_encode(small_data, max_size_bytes=100)
    assert result == '{"key": "value"}'


def test_safe_json_encode_at_size_limit() -> None:
    """Test that safe_json_encode works with output exactly at the size limit."""
    # Create data that results in exactly 13 bytes when encoded
    data = {"x": "test"}  # Results in '{"x": "test"}' which is 13 bytes
    result = safe_json_encode(data, max_size_bytes=13)
    assert result == '{"x": "test"}'
    assert len(result.encode("utf-8")) == 13


def test_safe_json_encode_exceeds_size_limit() -> None:
    """Test that safe_json_encode raises PayloadTooLargeError when output exceeds the limit."""
    # Create data that results in a large JSON string
    large_data = {"large": "a" * 100}

    with pytest.raises(PayloadTooLargeError, match="Encoded JSON size .* exceeds maximum allowed size"):
        safe_json_encode(large_data, max_size_bytes=50)


@pytest.mark.parametrize(
    "data, expected_exception, match",
    [
        (object(), JSONEncodeError, "Failed to encode data as JSON"),
        (set([1, 2, 3]), JSONEncodeError, "Failed to encode data as JSON"),
        (lambda x: x, JSONEncodeError, "Failed to encode data as JSON"),
    ],
)
def test_safe_json_encode_non_serializable(data: Any, expected_exception: type[APIConfigError], match: str) -> None:
    """Verify the safe_json_encode function raises JSONEncodeError for non-serializable objects."""
    with pytest.raises(expected_exception, match=match):
        safe_json_encode(data)


def test_safe_json_encode_unicode_handling() -> None:
    """Test that safe_json_encode properly handles unicode characters."""
    unicode_data = {"message": "Hello 世界", "emoji": "🚀"}

    # Without ensure_ascii (default)
    result_unicode = safe_json_encode(unicode_data, ensure_ascii=False)
    assert "世界" in result_unicode
    assert "🚀" in result_unicode

    # With ensure_ascii=True
    result_ascii = safe_json_encode(unicode_data, ensure_ascii=True)
    assert "世界" not in result_ascii
    assert "🚀" not in result_ascii
    assert "\\u" in result_ascii  # Should contain unicode escapes


def test_safe_json_encode_indentation() -> None:
    """Test that safe_json_encode properly handles indentation."""
    data = {"outer": {"inner": "value"}}

    # No indentation (compact)
    compact = safe_json_encode(data, indent=None)
    assert "\n" not in compact

    # With indentation
    indented = safe_json_encode(data, indent=2)
    assert "\n" in indented
    assert "  " in indented  # Should contain spaces for indentation


def test_safe_json_decode_exceeds_size_limit_bytes() -> None:
    """Test that safe_json_decode raises PayloadTooLargeError for bytes payloads exceeding the limit."""
    # Create a bytes payload that's larger than the limit
    large_payload = b'{"large": "' + b"a" * 100 + b'"}'

    with pytest.raises(PayloadTooLargeError, match="Payload size .* exceeds maximum allowed size"):
        safe_json_decode(large_payload, max_size_bytes=50)
