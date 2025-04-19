from typing import Any

import pytest

from apiconfig.exceptions.base import APIConfigError
from apiconfig.utils.http import (
    HTTPUtilsError,
    JSONDecodeError,
    get_header_value,
    is_client_error,
    is_redirect,
    is_server_error,
    is_success,
    normalize_header_name,
    safe_json_decode,
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
    assert normalize_header_name(name) == expected


# --- Get Header Value Tests ---
@pytest.mark.parametrize(
    "headers, name, default, expected",
    [
        ({"Content-Type": "application/json"}, "content-type", None, "application/json"),
        ({"content-length": "100"}, "Content-Length", None, "100"),
        ({"X-API-Key": "123"}, "x-api-key", None, "123"),
        ({"Auth": "Bearer token"}, "AUTH", None, "Bearer token"),
        ({"Header1": "Value1"}, "header1", None, "Value1"),
        ({"Header1": "Value1"}, "NonExistent", "default_val", "default_val"),
        ({}, "AnyHeader", None, None),
        ({"Multi-Part-Header": "value"}, "multi-part-header", None, "value"),
    ],
)
def test_get_header_value(
    headers: dict[str, str], name: str, default: str | None, expected: str | None
) -> None:
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
def test_safe_json_decode_success(
    content: str | bytes, encoding: str | None, expected: dict[str, Any] | None
) -> None:
    assert safe_json_decode(content, encoding=encoding) == expected


@pytest.mark.parametrize(
    "content, encoding, expected_exception, match",
    [
        ("{invalid json", None, JSONDecodeError, "Failed to decode JSON"),
        (b"\x80abc", "utf-8", JSONDecodeError, "Failed to decode response body"),  # Invalid UTF-8 start byte
        # Removed problematic test case: (b'{"key": "value"}', "ascii", JSONDecodeError, "Failed to decode response body"),
        (123, None, HTTPUtilsError, "An unexpected error occurred"),  # Invalid input type
    ],
)
def test_safe_json_decode_failure(
    content: Any, encoding: str | None, expected_exception: type[APIConfigError], match: str
) -> None:
    with pytest.raises(expected_exception, match=match):
        safe_json_decode(content, encoding=encoding)
