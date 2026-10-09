"""
Path manipulation utility functions for endpoint building.

This module provides pure functions for manipulating and joining
path segments in URL construction.
"""

from typing import List, Optional, Union

# Type alias for path arguments
PathArgs = Optional[Union[str, int]]


def join_path_segments(*args: PathArgs) -> str:
    """
    Join path segments into a properly formatted URL path.

    This function takes variable path segments, filters out None values,
    converts all values to strings, and joins them with forward slashes.
    The result does NOT start with a forward slash, so it can be appended
    to a base URL.

    Parameters
    ----------
    *args : PathArgs
        Variable number of path segments. Can be strings, integers, or None.
        None values and empty strings are filtered out before joining.

    Returns
    -------
    str
        The joined path string with forward slashes between segments.
        Returns empty string if no valid segments.

    Examples
    --------
    >>> join_path_segments("api", "v1", "users", 123)
    'api/v1/users/123'

    >>> join_path_segments("users", None, "posts")
    'users/posts'

    >>> join_path_segments()
    ''
    """
    # Filter out None values and empty strings, convert to strings and strip slashes
    segments: List[str] = []
    for arg in args:
        if arg is not None and str(arg).strip():
            # Strip leading and trailing slashes from each segment
            segment = str(arg).strip("/")
            if segment:  # Only add non-empty segments after stripping
                segments.append(segment)

    # If no segments, return empty string
    if not segments:
        return ""

    # Join with forward slash (no leading slash)
    return "/".join(segments)
