from __future__ import annotations

from typing import Any, Dict, Optional  # pyright: ignore[reportShadowedImports]

import pytest

from apiconfig.utils.url import (
    add_query_params,
    build_url,
    build_url_with_auth,
    normalize_query_params,
)

# --- Tests for build_url ---
_QueryParamsInput = Optional[Dict[str, Any]]


@pytest.mark.parametrize(
    "base_url, path, query_params, expected",
    [
        # Basic cases
        (
            "https://api.example.com",
            "users/123",
            None,
            "https://api.example.com/users/123",
        ),
        (
            "https://api.example.com/",
            "users/456",
            None,
            "https://api.example.com/users/456",
        ),
        # With query parameters
        (
            "http://localhost:8000",
            "search",
            {"q": "test", "limit": 10},
            "http://localhost:8000/search?q=test&limit=10",
        ),
        (
            "https://example.com",
            "data",
            {"ids": [1, 2, 3], "active": True},
            "https://example.com/data?ids=1&ids=2&ids=3&active=True",
        ),
        # Query parameters with None values (should be excluded)
        (
            "https://example.com",
            "items",
            {"status": "active", "page": None, "size": 20},
            "https://example.com/items?status=active&size=20",
        ),
        # No path
        (
            "https://api.example.com",
            "",
            {"token": "abc"},
            "https://api.example.com/?token=abc",
        ),
        (
            "https://api.example.com/",
            "",
            None,
            "https://api.example.com/",
        ),
    ],
)
def test_build_url(
    base_url: str,
    path: str,
    query_params: _QueryParamsInput,
    expected: str,
) -> None:
    """Test build_url with various inputs."""
    assert build_url(base_url, path, query_params) == expected


def test_build_url_basic_functionality() -> None:
    """Test that build_url works with basic functionality."""
    # Test with path joining
    url = build_url("https://example.com/api", "users/123")
    assert url == "https://example.com/api/users/123"

    # Test with query params
    url = build_url("https://example.com", "search", {"q": "test"})
    assert url == "https://example.com/search?q=test"

    # Test with no path
    url = build_url("https://example.com", "", {"q": "test"})
    assert url == "https://example.com/?q=test"


# --- Tests for add_query_params ---


@pytest.mark.parametrize(
    "url, params, expected",
    [
        # Add to URL without params
        (
            "https://example.com/path",
            {"a": 1, "b": "test"},
            "https://example.com/path?a=1&b=test",
        ),
        # Add to URL with existing params (merge)
        (
            "https://example.com/path?a=1",
            {"b": 2, "c": "three"},
            "https://example.com/path?a=1&b=2&c=three",
        ),
        # Update existing params (merge)
        (
            "https://example.com/path?a=1&b=2",
            {"a": "new", "c": 3},
            "https://example.com/path?a=new&b=2&c=3",
        ),
        # Add params with list values
        (
            "https://example.com/path",
            {"ids": [10, 20], "name": "item"},
            "https://example.com/path?ids=10&ids=20&name=item",
        ),
        # Add params with None values (should be ignored)
        (
            "https://example.com/path?a=1",
            {"b": 2, "c": None, "d": "valid"},
            "https://example.com/path?a=1&b=2&d=valid",
        ),
        # URL with fragment
        (
            "https://example.com/path?a=1#section",
            {"b": 2},
            "https://example.com/path?a=1&b=2#section",
        ),
        # Empty params dict
        (
            "https://example.com/path?a=1",
            {},
            "https://example.com/path?a=1",
        ),
        # Test with None values in params (should be filtered out)
        (
            "https://example.com/path",
            {"a": None, "b": None},
            "https://example.com/path",  # All params are None, so no query string
        ),
        # Test with tuple values
        (
            "https://example.com/path",
            {"tuple": (1, 2, 3)},
            "https://example.com/path?tuple=1&tuple=2&tuple=3",
        ),
    ],
)
def test_add_query_params(url: str, params: Dict[str, Any], expected: str) -> None:
    """Test add_query_params function."""
    result = add_query_params(url, params)
    assert result == expected


# --- Tests for build_url_with_auth ---


def test_build_url_with_auth() -> None:
    """Test build_url_with_auth function."""
    # Test with both query and auth params
    url = build_url_with_auth("https://api.example.com", "users", query_params={"limit": 10}, auth_params={"api_key": "secret"})
    assert "limit=10" in url
    assert "api_key=secret" in url
    assert url.startswith("https://api.example.com/users?")

    # Test with only auth params
    url = build_url_with_auth("https://api.example.com", "users", auth_params={"token": "abc123"})
    assert url == "https://api.example.com/users?token=abc123"

    # Test with only query params
    url = build_url_with_auth("https://api.example.com", "users", query_params={"page": 1})
    assert url == "https://api.example.com/users?page=1"

    # Test with no params
    url = build_url_with_auth("https://api.example.com", "users")
    assert url == "https://api.example.com/users"


# --- Tests for normalize_query_params ---


def test_normalize_query_params() -> None:
    """Test normalize_query_params function."""
    # Test with None
    result = normalize_query_params(None)
    assert result == {}

    # Test with empty dict
    result = normalize_query_params({})
    assert result == {}

    # Test with simple params
    result = normalize_query_params({"a": "1", "b": 2})
    assert result == {"a": ["1"], "b": ["2"]}

    # Test with None values (should be filtered out)
    result = normalize_query_params({"a": "1", "b": None, "c": "3"})
    assert result == {"a": ["1"], "c": ["3"]}

    # Test with list values
    result = normalize_query_params({"ids": [1, 2, 3]})
    assert result == {"ids": ["1", "2", "3"]}

    # Test with tuple values
    result = normalize_query_params({"coords": (10.5, 20.3)})
    assert result == {"coords": ["10.5", "20.3"]}

    # Test with tuple values (sets are not supported in QueryParamType)
    result = normalize_query_params({"coords": (1, 2, 3)})
    assert result == {"coords": ["1", "2", "3"]}


def test_edge_cases_for_coverage() -> None:
    """Test edge cases to ensure coverage of the url module."""
    # Test with empty path
    url = build_url("https://example.com", "")
    assert url == "https://example.com/"

    # Test with None query params
    url = build_url("https://example.com", "path", None)
    assert url == "https://example.com/path"

    # Test with empty query params dict
    url = build_url("https://example.com", "path", {})
    assert url == "https://example.com/path"

    # Test add_query_params with empty normalized params
    url = add_query_params("https://example.com/path", {"a": None})
    assert url == "https://example.com/path"
