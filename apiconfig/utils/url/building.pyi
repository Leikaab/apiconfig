import sys
from typing import Any, Mapping, Sequence, Union

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_QueryParamValue = Union[str, int, float, bool, Sequence[Union[str, int, float, bool]]]
_QueryParams = Mapping[str, _QueryParamValue | None]


def build_url(
    base_url: str,
    *path_segments: Union[str, int],
    query_params: _QueryParams | None = None,
) -> str:
    """
    Build a URL by joining a base URL with path segments and adding query parameters.

    Handles joining slashes correctly between the base URL and segments,
    and encodes query parameters. Filters out query parameters with None values.

    Args:
        base_url: The base URL (e.g., "https://api.example.com/v1").
        *path_segments: Variable number of path segments to append.
                        Segments will be joined with '/'. Leading/trailing
                        slashes in segments are handled. Empty segments are ignored.
        query_params: A dictionary of query parameters to add. Values can be
                      single values or sequences for repeated parameters.
                      Parameters with None values are excluded.

    Returns:
        The constructed URL string.

    Examples:
        >>> build_url("https://example.com/api", "users", 123)
        'https://example.com/api/users/123'
        >>> build_url("https://example.com/api/", "/users/", "/123/")
        'https://example.com/api/users/123'
        >>> build_url("https://example.com", "search", query_params={"q": "test", "limit": 10})
        'https://example.com/search?q=test&limit=10'
        >>> build_url("https://example.com", "items", query_params={"ids": [1, 2, 3], "status": None})
        'https://example.com/items?ids=1&ids=2&ids=3'
    """
    ...


def add_query_params(
    url: str, params: _QueryParams, replace: bool = False
) -> str:
    """
    Add or update query parameters to an existing URL.

    Preserves existing URL components (scheme, netloc, path, fragment).
    Filters out parameters with None values from the input `params`.

    Args:
        url: The original URL string.
        params: A dictionary of query parameters to add or update.
                Parameters with None values are ignored.
        replace: If True, existing query parameters are completely replaced
                 by `params`. If False (default), `params` are merged with
                 existing parameters, potentially overwriting values for
                 the same keys.

    Returns:
        The URL string with updated query parameters.

    Examples:
        >>> add_query_params("https://example.com/path?a=1", {"b": 2, "c": None})
        'https://example.com/path?a=1&b=2'
        >>> add_query_params("https://example.com/path?a=1", {"a": 2, "b": 3})
        'https://example.com/path?a=2&b=3'
        >>> add_query_params("https://example.com/path?a=1", {"b": 2}, replace=True)
        'https://example.com/path?b=2'
        >>> add_query_params("https://example.com/path#frag", {"q": "test"})
        'https://example.com/path?q=test#frag'
    """
    ...


def replace_path_segment(
    url: str, segment_index: int, new_segment: str
) -> str:
    """
    Replace a specific segment in the URL path.

    Segments are considered parts of the path separated by '/'.
    Leading/trailing slashes in the original path are generally preserved.

    Args:
        url: The original URL string.
        segment_index: The zero-based index of the path segment to replace.
                       Negative indices are not supported.
        new_segment: The new string to replace the segment with. Leading/trailing
                     slashes in the new segment are stripped.

    Returns:
        The URL string with the modified path.

    Raises:
        IndexError: If `segment_index` is out of range for the existing path segments.

    Examples:
        >>> replace_path_segment("https://example.com/api/users/123/profile", 1, "accounts")
        'https://example.com/api/accounts/123/profile'
        >>> replace_path_segment("https://example.com/api/users/", 1, "items")
        'https://example.com/api/items/'
        >>> replace_path_segment("https://example.com/search", 0, "query")
        'https://example.com/query'
    """
    ...
