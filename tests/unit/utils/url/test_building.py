from typing import Any, Dict, List, Optional, Union

import pytest

from apiconfig.utils.url.building import (
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
            "https://example.com/api/items/",  # Should normalize slashes
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
