from typing import Dict, List, Union  # Add missing imports
from urllib.parse import ParseResult

import pytest

from apiconfig.utils.url import add_query_params, get_query_params, parse_url


# --- Tests for parse_url ---
@pytest.mark.parametrize(
    "url_in, expected_scheme, expected_netloc, expected_path",
    [
        ("https://example.com/path?q=1", "https", "example.com", "/path"),
        ("http://user:pass@host.com:8080", "http", "user:pass@host.com:8080", ""),
        ("example.com/api/v1", "https", "example.com", "/api/v1"),  # Default scheme
        ("ftp://ftp.example.com/", "ftp", "ftp.example.com", "/"),
        (
            "//cdn.example.com/script.js",
            "",
            "cdn.example.com",
            "/script.js",
        ),  # urlparse leaves scheme empty for //
        ("/relative/path", "", "", "/relative/path"),  # Relative path
    ],
)
def test_parse_url(
    url_in: str, expected_scheme: str, expected_netloc: str, expected_path: str
) -> None:
    """Tests basic URL parsing and scheme defaulting."""
    result: ParseResult = parse_url(url_in)
    assert isinstance(result, ParseResult)
    assert result.scheme == expected_scheme
    assert result.netloc == expected_netloc
    assert result.path == expected_path


# --- Tests for get_query_params ---
@pytest.mark.parametrize(
    "url_in, expected_params",
    [
        ("https://example.com/path", {}),
        ("https://example.com/path?a=1&b=hello", {"a": "1", "b": "hello"}),
        ("https://example.com/path?a=1&a=2&b=3", {"a": ["1", "2"], "b": "3"}),
        ("https://example.com/path?key=", {"key": ""}),
        ("https://example.com/path?key=&b=val", {"key": "", "b": "val"}),
        ("https://example.com/path?a=1&a=", {"a": ["1", ""]}),
        ("example.com?encoded=%20%26%3D", {"encoded": " &="}),  # Handles decoding
    ],
)
def test_get_query_params(
    url_in: str, expected_params: Dict[str, Union[str, List[str]]]
) -> None:
    """Tests extraction of query parameters."""
    result: Dict[str, Union[str, List[str]]] = get_query_params(url_in)
    assert result == expected_params


# --- Tests for add_query_params ---
@pytest.mark.parametrize(
    "url_in, params_to_add, expected_url_out",
    [
        # Add to URL with no params
        ("https://example.com/path", {"a": "1"}, "https://example.com/path?a=1"),
        # Add to URL with existing params (no overlap)
        (
            "https://example.com/path?a=1",
            {"b": "2"},
            "https://example.com/path?a=1&b=2",
        ),
        # Update existing param
        (
            "https://example.com/path?a=1",
            {"a": "new"},
            "https://example.com/path?a=new",
        ),
        # Add multi-value param
        (
            "https://example.com/path",
            {"a": ["1", "2"]},
            "https://example.com/path?a=1&a=2",
        ),
        # Update with multi-value param
        (
            "https://example.com/path?a=old",
            {"a": ["1", "2"]},
            "https://example.com/path?a=1&a=2",
        ),
        # Add param with special chars
        (
            "https://example.com/path",
            {"q": "a b&c=d"},
            "https://example.com/path?q=a+b%26c%3Dd",
        ),
        # Remove existing param using None
        (
            "https://example.com/path?a=1&b=2",
            {"a": None},
            "https://example.com/path?b=2",
        ),
        # Try removing non-existent param
        ("https://example.com/path?b=2", {"a": None}, "https://example.com/path?b=2"),
        # Add, update, and remove
        (
            "https://example.com/path?a=1&b=2",
            {"a": "new", "c": "3", "b": None},
            "https://example.com/path?a=new&c=3",
        ),
        # Add blank value
        ("https://example.com/path", {"a": ""}, "https://example.com/path?a="),
        # Update to blank value
        ("https://example.com/path?a=1", {"a": ""}, "https://example.com/path?a="),
        # Remove last param
        ("https://example.com/path?a=1", {"a": None}, "https://example.com/path"),
        # Handle URL without scheme
        ("example.com/path?a=1", {"b": "2"}, "https://example.com/path?a=1&b=2"),
    ],
)
def test_add_query_params(
    url_in: str,
    params_to_add: Dict[str, Union[str, List[str], None]],
    expected_url_out: str,
) -> None:
    """Tests adding, updating, and removing query parameters."""
    result: str = add_query_params(url_in, params_to_add)
    # Compare parsed results to ignore scheme/domain case differences if default added
    parsed_result: ParseResult = parse_url(result)
    parsed_expected: ParseResult = parse_url(expected_url_out)
    assert parsed_result.path == parsed_expected.path
    assert get_query_params(result) == get_query_params(expected_url_out)
    # Also check netloc if it was present in the input or expected output
    if parsed_expected.netloc or parse_url(url_in).netloc:
        assert parsed_result.netloc == parsed_expected.netloc
