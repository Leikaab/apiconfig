from typing import Any, Dict, List, Union  # Add missing imports
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
        ("file.txt", "", "", "file.txt"),  # Simple filename (no scheme added)
        ("domain.com", "https", "domain.com", ""),  # Domain with dot gets scheme
        ("domain.com/path?q=1#frag", "https", "domain.com", "/path"),  # Domain with path, query, fragment
        ("sub.domain.co.uk/path", "https", "sub.domain.co.uk", "/path"),  # Subdomain
        ("localhost:8080", "https", "localhost:8080", ""),  # localhost with port
        ("127.0.0.1:8000/api", "https", "127.0.0.1:8000", "/api"),  # IP address with port
        ("https://[2001:db8::1]/path", "https", "[2001:db8::1]", "/path"),  # IPv6
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


def test_parse_url_complete() -> None:
    """Test parse_url with all URL components."""
    url = "https://user:pass@example.com:8080/path/to/resource?a=1&b=2#section"
    result = parse_url(url)

    assert result.scheme == "https"
    assert result.netloc == "user:pass@example.com:8080"
    assert result.path == "/path/to/resource"
    assert result.params == ""
    assert result.query == "a=1&b=2"
    assert result.fragment == "section"


def test_parse_url_edge_cases() -> None:
    """Test parse_url with edge cases."""
    # Empty string
    result = parse_url("")
    assert result.scheme == ""
    assert result.netloc == ""
    assert result.path == ""

    # Just a slash
    result = parse_url("/")
    assert result.scheme == ""
    assert result.netloc == ""
    assert result.path == "/"

    # Multiple slashes (not a protocol)
    result = parse_url("///path")
    assert result.scheme == ""
    assert result.netloc == ""
    assert result.path == "///path"

    # URL with params component (rarely used)
    result = parse_url("https://example.com/path;param1=value1?query=value#frag")
    assert result.scheme == "https"
    assert result.netloc == "example.com"
    assert result.path == "/path"
    assert result.params == "param1=value1"
    assert result.query == "query=value"
    assert result.fragment == "frag"


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
        # Additional test cases for full coverage
        ("https://example.com/path?a=1&a=1", {"a": ["1", "1"]}),  # Duplicate values
        ("https://example.com/path?", {}),  # Empty query string
        ("https://example.com/path?&&", {}),  # Query string with only separators
        ("https://example.com/path?a&b&c", {"a": "", "b": "", "c": ""}),  # Params without values
        ("https://example.com/path?a=1+2", {"a": "1 2"}),  # Plus as space
        ("https://example.com/path?a=true&b=false", {"a": "true", "b": "false"}),  # Boolean-like values
        ("https://example.com/path?arr[]=1&arr[]=2", {"arr[]": ["1", "2"]}),  # Array-like notation
    ],
)
def test_get_query_params(
    url_in: str, expected_params: Dict[str, Union[str, List[str]]]
) -> None:
    """Tests extraction of query parameters."""
    result: Dict[str, Union[str, List[str]]] = get_query_params(url_in)
    assert result == expected_params


def test_get_query_params_with_complex_values() -> None:
    """Test get_query_params with complex query string values."""
    # URL with complex query parameters
    url = "https://example.com/search?q=complex+query+%28with+parentheses%29&filters[]=price:10-20&filters[]=color:red"
    result = get_query_params(url)

    assert result["q"] == "complex query (with parentheses)"
    assert result["filters[]"] == ["price:10-20", "color:red"]


def test_get_query_params_with_special_chars() -> None:
    """Test get_query_params with special characters in query parameters."""
    # URL with special characters in query parameters
    url = "https://example.com/path?special=!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~"
    result = get_query_params(url)

    assert "special" in result
    # The exact value depends on URL encoding, but it should contain most of the special chars


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
        # Additional test cases for full coverage
        # URL with fragment
        (
            "https://example.com/path?a=1#section",
            {"b": "2"},
            "https://example.com/path?a=1&b=2#section",
        ),
        # URL with params component
        (
            "https://example.com/path;param=value?a=1",
            {"b": "2"},
            "https://example.com/path;param=value?a=1&b=2",
        ),
        # URL with complex path
        (
            "https://example.com/path/to/resource",
            {"a": "1"},
            "https://example.com/path/to/resource?a=1",
        ),
        # URL with username and password
        (
            "https://user:pass@example.com/path",
            {"a": "1"},
            "https://user:pass@example.com/path?a=1",
        ),
        # URL with port
        (
            "https://example.com:8080/path",
            {"a": "1"},
            "https://example.com:8080/path?a=1",
        ),
        # URL with IPv6 address
        (
            "https://[2001:db8::1]/path",
            {"a": "1"},
            "https://[2001:db8::1]/path?a=1",
        ),
        # Add boolean-like values
        (
            "https://example.com/path",
            {"a": True, "b": False},
            "https://example.com/path?a=True&b=False",
        ),
        # Add numeric values
        (
            "https://example.com/path",
            {"a": 123, "b": 45.67},
            "https://example.com/path?a=123&b=45.67",
        ),
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


def test_add_query_params_with_complex_values() -> None:
    """Test add_query_params with complex values."""
    # Test with mixed types in lists
    url = "https://example.com/path"
    # Use type annotation to help mypy understand this is intentional
    params: Dict[str, Any] = {"mixed": [1, "two", 3.0, True]}
    result = add_query_params(url, params)

    assert get_query_params(result)["mixed"] == ["1", "two", "3.0", "True"]

    # Test with nested structures (will be converted to strings)
    url2 = "https://example.com/path"
    # Use type annotation to help mypy understand this is intentional
    params2: Dict[str, Any] = {"complex": {"a": 1, "b": 2}}
    result = add_query_params(url2, params2)

    # The exact string representation might vary, but it should contain the key
    assert "complex" in get_query_params(result)


def test_add_query_params_edge_cases() -> None:
    """Test add_query_params with edge cases."""
    # Empty URL
    with pytest.raises(ValueError):
        add_query_params("", {"a": "1"})

    # URL with only scheme
    result = add_query_params("https://", {"a": "1"})
    assert get_query_params(result)["a"] == "1"

    # URL with very long query parameter
    long_value = "x" * 1000  # 1000 character string
    result = add_query_params("https://example.com", {"long": long_value})
    assert get_query_params(result)["long"] == long_value
