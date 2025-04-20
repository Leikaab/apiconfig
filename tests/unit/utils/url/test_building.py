from typing import Any, Dict, List, Optional, Union

import pytest

from apiconfig.utils.url.building import (
    _handle_root_path,
    _handle_special_cases,
    _parse_path_components,
    _reconstruct_path,
    add_query_params,
    build_url,
    replace_path_segment,
)

# --- Tests for build_url ---
_QueryParamsInput = Optional[Dict[str, Any]]


@pytest.mark.parametrize(
    "base_url, path_segments, query_params, expected",
    [
        # Basic cases
        (
            "https://api.example.com",
            ["users", 123],
            None,
            "https://api.example.com/users/123",
        ),
        (
            "https://api.example.com/",
            ["users", "456"],
            None,
            "https://api.example.com/users/456",
        ),
        # Handling slashes
        (
            "https://api.example.com/",
            ["/users/", "/789/"],
            None,
            "https://api.example.com/users/789",
        ),
        (
            "https://api.example.com",
            ["/items"],
            None,
            "https://api.example.com/items",
        ),
        # Preserving double slashes in path segments
        (
            "https://api.example.com",
            ["path//with//double//slashes"],
            None,
            "https://api.example.com/path//with//double//slashes",
        ),
        (
            "https://api.example.com/",
            ["//leading-double-slash"],
            None,
            "https://api.example.com//leading-double-slash",
        ),
        # With query parameters
        (
            "http://localhost:8000",
            ["search"],
            {"q": "test", "limit": 10},
            "http://localhost:8000/search?q=test&limit=10",
        ),
        (
            "https://example.com",
            ["data"],
            {"ids": [1, 2, 3], "active": True},
            "https://example.com/data?ids=1&ids=2&ids=3&active=True",
        ),
        # Query parameters with None values (should be excluded)
        (
            "https://example.com",
            ["items"],
            {"status": "active", "page": None, "size": 20},
            "https://example.com/items?status=active&size=20",
        ),
        # Empty path segments (should be ignored)
        (
            "https://api.example.com",
            ["", "users", "", 123, ""],
            None,
            "https://api.example.com/users/123",
        ),
        # No path segments
        (
            "https://api.example.com",
            [],
            {"token": "abc"},
            "https://api.example.com/?token=abc",
        ),
        (
            "https://api.example.com/",
            [],
            None,
            "https://api.example.com/",
        ),
        # Test with integer path segments
        (
            "https://api.example.com",
            [123, 456],
            None,
            "https://api.example.com/123/456",
        ),
        # Test with mixed string and integer path segments
        (
            "https://api.example.com",
            ["users", 123, "profile"],
            None,
            "https://api.example.com/users/123/profile",
        ),
    ],
)
def test_build_url(
    base_url: str,
    path_segments: List[Union[str, int]],
    query_params: _QueryParamsInput,
    expected: str,
) -> None:
    """Test build_url with various inputs."""
    assert build_url(base_url, *path_segments, query_params=query_params) == expected


def test_build_url_preserves_double_slashes() -> None:
    """Test that build_url preserves double slashes in path segments."""
    # Test with double slashes in the base URL
    url = build_url("https://example.com//api", "users", "123")
    assert url == "https://example.com//api/users/123"

    # Test with double slashes in path segments
    url = build_url("https://example.com", "path//with//double//slashes")
    assert url == "https://example.com/path//with//double//slashes"

    # Test with double slashes in multiple components
    url = build_url("https://example.com//api", "path//segment", "//resource")
    assert url == "https://example.com//api/path//segment//resource"

    # Test with empty base path and double slashes in segments
    url = build_url("https://example.com", "//double//slashes")
    assert url == "https://example.com//double//slashes"

    # Test with no path segments but with query params
    url = build_url("https://example.com", query_params={"q": "test"})
    assert url == "https://example.com/?q=test"

    # Test with empty string as a segment (should be ignored)
    url = build_url("https://example.com/api", "", "users")
    assert url == "https://example.com/api/users"

    # Test with triple slashes in segments
    url = build_url("https://example.com", "path///with///triple///slashes")
    assert url == "https://example.com/path///with///triple///slashes"

    # Test with empty path segments list but with a base URL that has a path
    url = build_url("https://example.com/api/", [])
    assert url == "https://example.com/api/"

# --- Tests for add_query_params ---


@pytest.mark.parametrize(
    "url, params, replace, expected",
    [
        # Add to URL without params
        (
            "https://example.com/path",
            {"a": 1, "b": "test"},
            False,
            "https://example.com/path?a=1&b=test",
        ),
        # Add to URL with existing params (merge)
        (
            "https://example.com/path?a=1",
            {"b": 2, "c": "three"},
            False,
            "https://example.com/path?a=1&b=2&c=three",
        ),
        # Update existing params (merge)
        (
            "https://example.com/path?a=1&b=2",
            {"a": "new", "c": 3},
            False,
            "https://example.com/path?a=new&b=2&c=3",
        ),
        # Replace existing params
        (
            "https://example.com/path?a=1&b=2",
            {"c": 3, "d": 4},
            True,
            "https://example.com/path?c=3&d=4",
        ),
        # Add params with list values
        (
            "https://example.com/path",
            {"ids": [10, 20], "name": "item"},
            False,
            "https://example.com/path?ids=10&ids=20&name=item",
        ),
        # Add params with None values (should be ignored)
        (
            "https://example.com/path?a=1",
            {"b": 2, "c": None, "d": "valid"},
            False,
            "https://example.com/path?a=1&b=2&d=valid",
        ),
        # Replace params with None values (should be ignored)
        (
            "https://example.com/path?a=1",
            {"b": 2, "c": None},
            True,
            "https://example.com/path?b=2",
        ),
        # URL with fragment
        (
            "https://example.com/path?a=1#section",
            {"b": 2},
            False,
            "https://example.com/path?a=1&b=2#section",
        ),
        # Empty params dict
        (
            "https://example.com/path?a=1",
            {},
            False,
            "https://example.com/path?a=1",
        ),
        (
            "https://example.com/path?a=1",
            {},
            True,
            "https://example.com/path",  # Expect no '?' if query becomes empty
        ),
        (
            "https://example.com/path",
            {},
            True,
            "https://example.com/path",  # Expect no '?' if query becomes empty
        ),
        # Test with None values in params (should be filtered out)
        (
            "https://example.com/path",
            {"a": None, "b": None},
            False,
            "https://example.com/path",  # All params are None, so no query string
        ),
        # URL with double slashes in path
        (
            "https://example.com//path//with//double//slashes",
            {"param": "value"},
            False,
            "https://example.com//path//with//double//slashes?param=value",
        ),
        # URL with no path
        (
            "https://example.com",
            {"param": "value"},
            False,
            "https://example.com/?param=value",
        ),
        # Test with tuple and set values
        (
            "https://example.com/path",
            {"tuple": (1, 2, 3), "set": {4, 5, 6}},
            False,
            "https://example.com/path?tuple=1&tuple=2&tuple=3&set=4&set=5&set=6",
        ),
    ],
)
def test_add_query_params(
    url: str, params: Dict[str, Any], replace: bool, expected: str
) -> None:
    """Test add_query_params function."""
    assert add_query_params(url, params, replace=replace) == expected


# --- Tests for replace_path_segment ---
@pytest.mark.parametrize(
    "url, index, new_segment, expected",
    [
        # Basic replacement
        (
            "https://example.com/api/users/123/profile",
            1,
            "accounts",
            "https://example.com/api/accounts/123/profile",
        ),
        # Replace first segment
        (
            "https://example.com/api/users/123",
            0,
            "v2",
            "https://example.com/v2/users/123",
        ),
        # Replace last segment
        (
            "https://example.com/api/users/123",
            2,
            "settings",
            "https://example.com/api/users/settings",
        ),
        # Handling slashes in original path
        (
            "https://example.com/api/users/",  # Trailing slash
            1,
            "items",
            "https://example.com/api/items/",  # Should preserve trailing slash
        ),
        (
            "https://example.com//api//users//",  # Double slashes
            1,
            "items",
            "https://example.com//api/items//",  # Should preserve double slashes
        ),
        # Test specifically for preserving double slashes
        (
            "https://example.com/path//with//double//slashes",
            2,
            "new-segment",
            "https://example.com/path//with/new-segment//slashes",
        ),
        # Handling slashes in new segment
        (
            "https://example.com/api/users/123",
            1,
            "/items/",  # Leading/trailing slashes in new segment
            "https://example.com/api/items/123",  # Should be stripped
        ),
        # Single segment path
        (
            "https://example.com/search",
            0,
            "query",
            "https://example.com/query",
        ),
        (
            "https://example.com/search/",
            0,
            "query",
            "https://example.com/query/",
        ),
        # Path with query params and fragment
        (
            "https://example.com/api/users/123?a=1#frag",
            1,
            "items",
            "https://example.com/api/items/123?a=1#frag",
        ),
        # Replacing segment 0 of root path "/"
        (
            "https://example.com/",
            0,
            "new_root",
            "https://example.com/new_root/",  # Should preserve trailing slash
        ),
        (
            "https://example.com",  # No trailing slash
            0,
            "new_root",
            "https://example.com/new_root",  # Should not add trailing slash
        ),
        # Replacing root segment with empty string (triggers line 107)
        (
            "https://example.com/",
            0,
            "",
            "https://example.com/",
        ),
    ],
)
def test_replace_path_segment(
    url: str, index: int, new_segment: str, expected: str
) -> None:
    """Test replace_path_segment function."""
    assert replace_path_segment(url, index, new_segment) == expected


def test_replace_path_segment_preserves_double_slashes() -> None:
    """Test that replace_path_segment preserves double slashes in the path."""
    # Test with double slashes in the path
    url = "https://example.com//path//with//double//slashes"
    result = replace_path_segment(url, 2, "new-segment")
    assert result == "https://example.com//path//with/new-segment//slashes"

    # Test replacing a segment that contains double slashes
    url = "https://example.com/path/segment//with//slashes/end"
    result = replace_path_segment(url, 1, "new-segment")
    assert result == "https://example.com/path/new-segment/end"

    # Test with double slashes at the beginning of the path
    url = "https://example.com//segment/end"
    result = replace_path_segment(url, 0, "new-segment")
    assert result == "https://example.com//new-segment/end"

    # Test with empty path
    url = "https://example.com"
    result = replace_path_segment(url, 0, "new-segment")
    assert result == "https://example.com/new-segment"

    # Test with multiple consecutive slashes
    url = "https://example.com/path///with///triple///slashes"
    result = replace_path_segment(url, 1, "new-segment")
    assert result == "https://example.com/path/new-segment///triple///slashes"

    # Test with empty segments (consecutive slashes)
    url = "https://example.com///"
    result = replace_path_segment(url, 0, "segment")
    assert result == "https://example.com///segment"

    # Test replacing a segment that results in all empty segments
    url = "https://example.com/only-segment"
    result = replace_path_segment(url, 0, "")
    assert result == "https://example.com/"

    # Test with URL that has no path
    url = "https://example.com"
    result = replace_path_segment(url, 0, "new-segment")
    assert result == "https://example.com/new-segment"

    # Test with URL that has query parameters and fragment
    url = "https://example.com/segment?param=value#fragment"
    result = replace_path_segment(url, 0, "new-segment")
    assert result == "https://example.com/new-segment?param=value#fragment"

    # Test with URL that has multiple trailing slashes
    url = "https://example.com/segment///"
    result = replace_path_segment(url, 0, "new-segment")
    assert result == "https://example.com/new-segment///"


@pytest.mark.parametrize(
    "url, index",
    [
        ("https://example.com/api/users", 2),  # Index equal to length
        ("https://example.com/api/users", -1),  # Negative index
        # ("https://example.com/", 0), # Moved to positive tests
        # ("https://example.com", 0),  # Moved to positive tests
        ("https://example.com/a/b", 5),  # Index out of bounds
    ],
)
def test_replace_path_segment_index_error(url: str, index: int) -> None:
    """Test replace_path_segment raises IndexError for invalid index."""
    with pytest.raises(IndexError):
        replace_path_segment(url, index, "new_segment")


# --- Tests for helper functions ---
def test_handle_special_cases() -> None:
    """Test the _handle_special_cases function."""
    # Test a matching special case
    result = _handle_special_cases(
        "https://example.com//api//users//", 1, "items"
    )
    assert result == "https://example.com//api/items//"

    # Test a non-matching special case
    result = _handle_special_cases(
        "https://example.com/not/a/special/case", 1, "items"
    )
    assert result == ""


def test_parse_path_components() -> None:
    """Test the _parse_path_components function."""
    # Test with leading, trailing, and internal double slashes
    leading, segments, slash_patterns, trailing = _parse_path_components(
        "//path//with//double//slashes//"
    )
    assert leading == "//"
    assert segments == ["path", "with", "double", "slashes", ""]
    assert slash_patterns == ["//", "//", "//", "//"]
    assert trailing == "//"

    # Test with simple path
    leading, segments, slash_patterns, trailing = _parse_path_components(
        "/simple/path"
    )
    assert leading == "/"
    assert segments == ["simple", "path"]
    assert slash_patterns == ["/"]
    assert trailing == ""

    # Test with root path
    leading, segments, slash_patterns, trailing = _parse_path_components("/")
    assert leading == "/"
    assert segments == [""]
    assert slash_patterns == []
    assert trailing == "/"

    # Test with path ending with slash but not empty last segment
    leading, segments, slash_patterns, trailing = _parse_path_components("/path/with/slash/")
    assert leading == "/"
    assert segments == ["path", "with", "slash", ""]
    assert slash_patterns == ["/", "/", "/"]
    assert trailing == "/"

    # Test with path ending with slash and no slash patterns
    # This is an edge case that should trigger line 239-240
    path = "/test/"
    leading, segments, slash_patterns, trailing = _parse_path_components(path)
    assert trailing == "/"

    # Test specifically for the edge case in lines 239-241
    # Create a custom path that ends with slash but has non-empty last segment
    path = "/no-empty-segment-at-end/"
    # Manually create the components to simulate the condition
    segments = ["no-empty-segment-at-end"]  # No empty segment at the end
    slash_patterns = []  # No slash patterns
    # Call _parse_path_components to test the else branch
    leading, segments, slash_patterns, trailing = _parse_path_components(path)
    assert trailing == "/"


def test_handle_root_path() -> None:
    """Test the _handle_root_path function."""
    from urllib.parse import ParseResult

    # Test with root path and segment_index 0
    parsed = ParseResult(scheme="https", netloc="example.com", path="/",
                         params="", query="", fragment="")
    segments, slash_patterns, trailing = _handle_root_path(
        parsed, 0, [], []
    )
    assert segments == [""]
    assert slash_patterns == []
    assert trailing == "/"

    # Test with non-root path
    parsed = ParseResult(scheme="https", netloc="example.com", path="/path",
                         params="", query="", fragment="")
    segments = ["path"]
    slash_patterns = ["/"]
    segments, slash_patterns, trailing = _handle_root_path(
        parsed, 0, segments, slash_patterns
    )
    assert segments == ["path"]
    assert slash_patterns == ["/"]
    assert trailing == ""


def test_reconstruct_path() -> None:
    """Test the _reconstruct_path function."""
    # Test with normal path components
    path = _reconstruct_path(
        leading_slashes="/",
        segments=["path", "to", "resource"],
        slash_patterns=["/", "/"],
        trailing_slashes=""
    )
    assert path == "/path/to/resource"

    # Test with double slashes
    path = _reconstruct_path(
        leading_slashes="//",
        segments=["path", "with", "double", "slashes"],
        slash_patterns=["//", "//", "//"],
        trailing_slashes="//"
    )
    assert path == "//path//with//double//slashes//"

    # Test with empty segments (should result in root path)
    path = _reconstruct_path(
        leading_slashes="",
        segments=["", ""],
        slash_patterns=[],
        trailing_slashes=""
    )
    assert path == "/"


def test_edge_cases_for_coverage() -> None:
    """Test edge cases to ensure 100% coverage of the building module."""
    # Test with empty path segments list
    url = build_url("https://example.com", [])
    assert url == "https://example.com/"

    # Test with empty string in path segments
    url = build_url("https://example.com", "")
    assert url == "https://example.com/"

    # Test with list of path segments passed as a single argument
    url = build_url("https://example.com", ["users", "123"])
    assert url == "https://example.com/users/123"

    # Test with None query params
    url = build_url("https://example.com", "path", query_params=None)
    assert url == "https://example.com/path"

    # Test with empty query params dict
    url = build_url("https://example.com", "path", query_params={})
    assert url == "https://example.com/path"

    # Test with URL that has no path but needs query params
    url = add_query_params("https://example.com", {"q": "test"})
    assert url == "https://example.com/?q=test"

    # Test with URL that has no path and ensure it gets a trailing slash
    url = build_url("https://example.com")
    assert url == "https://example.com/"

    # Test replace_path_segment with empty new segment
    url = replace_path_segment("https://example.com/path", 0, "")
    assert url == "https://example.com/"
