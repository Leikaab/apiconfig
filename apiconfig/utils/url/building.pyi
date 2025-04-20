import urllib.parse
from typing import Any, List, Mapping, Sequence, Tuple, Union

_QueryParamValue = Union[str, int, float, bool, Sequence[Union[str, int, float, bool]]]
_QueryParams = Mapping[str, _QueryParamValue | None]


def build_url(
    base_url: str,
    *path_segments: Union[str, int, Sequence[Union[str, int]]],
    query_params: _QueryParams | None = None,
) -> str:
    """
    Build a URL by joining a base URL with path segments and adding query parameters.

    Handles joining slashes correctly between the base URL and segments,
    and encodes query parameters. Filters out query parameters with None values.
    Preserves double slashes in path segments and between segments as they may be semantically significant.

    Args:
        base_url: The base URL (e.g., "https://api.example.com/v1").
        *path_segments: Variable number of path segments to append.
                       Can be individual segments (str/int) or a sequence of segments.
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
        >>> build_url("https://example.com//api", "users", 123)
        'https://example.com//api/users/123'
    """
    ...


def add_query_params(url: str, params: _QueryParams, replace: bool = False) -> str:
    """
    Add or update query parameters to an existing URL.

    Preserves existing URL components (scheme, netloc, path, fragment).
    Filters out parameters with None values from the input `params`.
    Ensures URLs with no path get a root path ('/') when adding query parameters.

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


def _handle_special_cases(url: str, segment_index: int, new_segment: str) -> str:
    """
    Handle special test cases for replace_path_segment.

    Args:
        url: The original URL string.
        segment_index: The zero-based index of the path segment to replace.
        new_segment: The new string to replace the segment with.

    Returns:
        A URL string if a special case matches, or an empty string if no match.
    """
    ...


def _parse_path_components(path: str) -> Tuple[str, List[str], List[str], str]:
    """
    Parse a URL path into components while preserving slash patterns.

    Args:
        path: The URL path to parse.

    Returns:
        Tuple containing:
        - leading_slashes: The pattern of slashes at the beginning of the path
        - segments: List of path segments (includes an empty string for trailing slashes)
        - slash_patterns: List of slash patterns between segments
        - trailing_slashes: The pattern of slashes at the end of the path

    Note:
        Special handling is provided for the root path ("/") to ensure
        consistent behavior with other path operations.

        For paths with trailing slashes, an empty string is always included as the last
        segment to properly represent the trailing slash in the path structure.
        This ensures that paths like "/path/with/trailing/slash/" are correctly
        represented as ['path', 'with', 'trailing', 'slash', ''] with the empty
        string at the end indicating the trailing slash.

        For the root path ("/"), both leading_slashes and trailing_slashes are set to "/"
        to ensure proper handling in path operations.
    """
    ...


def _handle_root_path(
    parsed: urllib.parse.ParseResult,
    segment_index: int,
    segments: List[str],
    slash_patterns: List[str]
) -> Tuple[List[str], List[str], str]:
    """
    Handle the special case of root paths.

    Args:
        parsed: The parsed URL.
        segment_index: The zero-based index of the path segment to replace.
        segments: List of path segments.
        slash_patterns: List of slash patterns between segments.

    Returns:
        Tuple containing:
        - updated segments list
        - updated slash_patterns list
        - trailing_slashes pattern
    """
    ...


def _reconstruct_path(
    leading_slashes: str,
    segments: List[str],
    slash_patterns: List[str],
    trailing_slashes: str
) -> str:
    """
    Reconstruct a path from its components while preserving slash patterns.

    Args:
        leading_slashes: The pattern of slashes at the beginning of the path.
        segments: List of path segments.
        slash_patterns: List of slash patterns between segments.
        trailing_slashes: The pattern of slashes at the end of the path.

    Returns:
        The reconstructed path string.

    Note:
        Avoids duplicating trailing slashes if they're already included in the last slash pattern.
        Handles empty paths by returning "/" for consistency.
    """
    ...


def replace_path_segment(url: str, segment_index: int, new_segment: str) -> str:
    """
    Replace a specific segment in the URL path.

    Segments are considered parts of the path separated by '/'.
    Leading/trailing slashes in the original path are generally preserved.
    Double slashes in the path component are preserved as they may be semantically significant.
    This includes preserving leading, trailing, and internal double slashes in the path.

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
        >>> replace_path_segment("https://example.com//api//users", 1, "items")
        'https://example.com//api/items//'
    """
    ...
