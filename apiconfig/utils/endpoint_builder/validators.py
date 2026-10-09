"""
Validation functions for endpoint path segments.

This module provides pure validation functions that can be used
independently to validate path segments before building endpoints.
"""

from typing import Optional, Union

# Type alias for path arguments
PathArgs = Optional[Union[str, int]]


def validate_path_segments(*args: PathArgs) -> None:
    """
    Validate that all path segments are of acceptable types and values.

    ``None`` and empty strings are accepted and skipped when the path is
    joined, so optional segments can be passed through unchanged.

    Parameters
    ----------
    *args : PathArgs
        Variable number of path segments (e.g., resource IDs, actions).

    Raises
    ------
    TypeError
        If any arg is not None, str, or int.
    ValueError
        If any path segment contains path traversal or leading/trailing slashes.

    Examples
    --------
    >>> validate_path_segments("users", 123, "edit")  # Valid
    >>> validate_path_segments("users", None, "")  # Valid, skipped when joined
    >>> validate_path_segments("users", [], "edit")
    Traceback (most recent call last):
    ...
    TypeError: Path segment must be string or integer, got list
    """
    for arg in args:
        if arg is None:
            continue

        if not isinstance(arg, (str, int)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Path segment must be string or integer, got {type(arg).__name__}")

        # Check for dangerous path traversal patterns
        if isinstance(arg, str) and (".." in arg or arg.startswith("/") or arg.endswith("/")):
            raise ValueError("Path segment contains potentially dangerous characters")
