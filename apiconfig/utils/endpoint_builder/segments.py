"""
Segment building and joining functions for endpoint construction.

This module provides functions for building resource path segments
from various inputs.
"""

from typing import List, Optional, Union

# Type alias for path arguments
PathArgs = Optional[Union[str, int]]


def build_resource_segments(resource_path: Optional[str], *args: PathArgs) -> List[str]:
    """
    Build the resource path segments from a resource path and additional arguments.

    This function creates a list of path segments starting with the resource path
    (if provided) and then appending any additional non-None arguments as strings.

    Parameters
    ----------
    resource_path : Optional[str]
        The base resource path (e.g., "users", "posts"). Can be None.
    *args : PathArgs
        Additional path segments (e.g., resource IDs, sub-resources).
        None values are filtered out.

    Returns
    -------
    List[str]
        A list of path segment strings. Empty list if no valid segments.

    Examples
    --------
    >>> build_resource_segments("users", 123, "posts")
    ['users', '123', 'posts']

    >>> build_resource_segments("users", 123, None, "posts")
    ['users', '123', 'posts']

    >>> build_resource_segments(None, "posts", 456)
    ['posts', '456']

    >>> build_resource_segments(None)
    []
    """
    segments: List[str] = []

    # Add the resource path if it exists
    if resource_path:
        segments.append(resource_path)

    # Add any additional path segments from args, filtering out None values
    for arg in args:
        if arg is not None:
            segments.append(str(arg))

    return segments
