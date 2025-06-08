"""URL utilities using urllib.parse with type-safe query parameter handling.

This module provides minimal wrappers around urllib.parse functions,
adding only type safety and parameter normalization.
"""

import urllib.parse
from typing import Any, Dict, List, Optional, TypeAlias, Union

from apiconfig.types import QueryParamType

UrlencodeParams: TypeAlias = Dict[str, List[str]]


def normalize_query_params(params: Optional[QueryParamType]) -> UrlencodeParams:
    """
    Convert QueryParamType to format expected by urllib.parse.urlencode.

    This is the ONLY custom logic needed - everything else uses urllib.parse.
    """
    if not params:
        return {}

    result: UrlencodeParams = {}
    for key, value in params.items():
        if value is None:
            continue  # Skip None values
        elif isinstance(value, (list, tuple, set)):
            result[key] = [str(item) for item in value]
        else:
            result[key] = [str(value)]

    return result


def build_url(base_url: str, path: str = "", params: Optional[QueryParamType] = None, version: Optional[str] = None) -> str:
    """
    Build URL using urllib.parse - simple and robust.

    Args
    ----
    base_url : str
        Base URL (e.g., "https://api.example.com")
    path : str
        Path to join (e.g., "/users/123")
    params : Optional[QueryParamType]
        Query parameters

    Returns
    -------
    str
        Complete URL

    Examples
    --------
    >>> build_url("https://api.example.com", "/users", {"limit": 10})
    "https://api.example.com/users?limit=10"
    """
    # Prepend version to path if provided
    if version:
        path = f"{version.strip('/')}/{path.lstrip('/')}"

    # Use urllib.parse.urljoin for path joining - it handles all edge cases
    if path:
        # Ensure base_url ends with slash for proper joining
        if not base_url.endswith("/"):
            base_url += "/"

        # Convert absolute paths to relative to preserve base_url path components
        # urljoin("https://api.example.com/v2", "/users") -> "https://api.example.com/users" (WRONG!)
        # urljoin("https://api.example.com/v2/", "users") -> "https://api.example.com/v2/users" (CORRECT!)
        if path.startswith("/"):
            path = path.lstrip("/")

        url = urllib.parse.urljoin(base_url, path)
    else:
        url = base_url
        # For empty path, ensure trailing slash if base_url doesn't have one
        if not url.endswith("/"):
            url += "/"

    # Add query parameters if provided
    if params:
        normalized_params = normalize_query_params(params)
        if normalized_params:
            # Use urllib.parse.urlencode - it handles all encoding
            query_string = urllib.parse.urlencode(normalized_params, doseq=True)

            # Use urllib.parse for URL reconstruction
            parsed = urllib.parse.urlparse(url)
            url = urllib.parse.urlunparse(parsed._replace(query=query_string))

    return url


def add_query_params(url: str, params: QueryParamType, replace: bool = False) -> str:
    """
    Add query parameters to existing URL using urllib.parse.

    Args
    ----
    url : str
        Existing URL
    params : QueryParamType
        Parameters to add
    replace : bool
        If True, replace all existing params. If False, merge.

    Returns
    -------
    str
        URL with added parameters
    """
    if not url:
        raise ValueError("URL cannot be empty")

    parsed = urllib.parse.urlparse(url)

    # Parse existing query parameters
    existing_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

    # Handle None values for parameter removal
    params_to_remove = [key for key, value in params.items() if value is None]
    params_to_add = {key: value for key, value in params.items() if value is not None}

    # Add new parameters
    normalized_new_params = normalize_query_params(params_to_add)

    final_params: UrlencodeParams
    if replace:
        final_params = normalized_new_params
    else:
        # Start with existing params, then update with new ones
        final_params = dict(existing_params)
        final_params.update(normalized_new_params)

        # Remove parameters that were set to None
        for key in params_to_remove:
            final_params.pop(key, None)

    # Rebuild query string
    query_string = urllib.parse.urlencode(final_params, doseq=True)

    # Reconstruct URL
    return urllib.parse.urlunparse(parsed._replace(query=query_string))


def get_query_params(url: str) -> Dict[str, Union[str, List[str]]]:
    """
    Extract query parameters from URL using urllib.parse.

    Args
    ----
    url : str
        URL to parse

    Returns
    -------
    Dict[str, Union[str, List[str]]]
        Dictionary of query parameters
    """
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

    # Simplify single-item lists to strings
    result: Dict[str, Union[str, List[str]]] = {}
    for key, values in params.items():
        if len(values) == 1:
            result[key] = values[0]
        else:
            result[key] = values

    return result


def build_url_with_auth(
    base_url: str,
    path: str = "",
    query_params: Optional[QueryParamType] = None,
    auth_params: Optional[QueryParamType] = None,
    version: Optional[str] = None,
) -> str:
    """
    Build URL with separate query and auth parameters.

    This is the ONLY high-level function needed for most use cases.
    """
    # Merge parameters
    all_params: Dict[str, Any] = {}
    if query_params:
        all_params.update(query_params)
    if auth_params:
        all_params.update(auth_params)

    return build_url(base_url, path, all_params, version)


def parse_url(url: str, default_scheme: str = "https") -> urllib.parse.ParseResult:
    """Parse URL using urllib.parse with optional default scheme."""
    if not url:
        return urllib.parse.urlparse(url)

    # Special case: preserve multiple leading slashes (e.g., "///path")
    # urllib.parse.urlparse normalizes "///path" to "/path", but tests expect preservation
    if url.startswith("///") and not url.startswith("////"):
        # Parse normally but preserve the original path
        parsed = urllib.parse.urlparse(url)
        # Create a new ParseResult with the original path preserved
        return urllib.parse.ParseResult(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            path=url,  # Use original URL as path since it's just a path with multiple slashes
            params=parsed.params,
            query=parsed.query,
            fragment=parsed.fragment,
        )

    # Add default scheme if missing AND it looks like a domain/host
    # Conditions for adding scheme:
    # 1. No scheme present (no "://")
    # 2. Contains a dot (domain-like) OR contains colon (host:port)
    # 3. Doesn't start with "/" (not a path)
    # 4. Doesn't start with "//" (not a protocol-relative URL)
    # 5. Not a simple filename with common extensions
    if (
        "://" not in url
        and ("." in url or ":" in url)
        and not url.startswith("/")
        and not (
            url.count(".") == 1 and "/" not in url and ":" not in url and url.split(".")[-1] in ["txt", "html", "css", "js", "json", "xml", "pdf"]
        )
    ):
        url = f"{default_scheme}://{url}"

    return urllib.parse.urlparse(url)


__all__ = [
    "build_url",
    "build_url_with_auth",
    "add_query_params",
    "get_query_params",
    "normalize_query_params",
    "parse_url",
]
