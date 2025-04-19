import urllib.parse
from typing import Any, Mapping, Union

from .parsing import parse_url  # Corrected import


def build_url(
    base_url: str,
    *path_segments: Union[str, int],
    query_params: Mapping[str, Any] | None = None,
) -> str:
    """Build a URL by joining a base URL with path segments and adding query parameters."""
    # Start with the base URL
    current_url = base_url

    # Sequentially join path segments using urljoin
    for segment in path_segments:
        # urljoin needs relative paths; strip leading/trailing slashes from segment
        segment_str = str(segment).strip("/")
        if segment_str:
            # Ensure base ends with / before joining for urljoin to work as expected for segments
            if not current_url.endswith("/"):
                current_url += "/"
            current_url = urllib.parse.urljoin(current_url, segment_str)

    # Add query parameters if provided
    if query_params:
        # Before adding params, ensure there's a path component if joining resulted in none
        # (e.g., base_url was 'http://host' and no segments added)
        parsed_url = parse_url(current_url)
        if not parsed_url.path:
            # Rebuild with root path before adding query params
            current_url = urllib.parse.urlunparse(parsed_url._replace(path="/"))

        # Use add_query_params to handle encoding and merging correctly
        current_url = add_query_params(current_url, query_params, replace=True)

    return current_url


def add_query_params(
    url: str, params: Mapping[str, Any], replace: bool = False
) -> str:
    """Add or update query parameters to an existing URL."""
    parsed = parse_url(url)  # Use parse_url
    # parse_url returns ParseResult, query is a string. Need parse_qs for dict.
    current_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

    # Filter out None values and prepare new params in parse_qs format (list values)
    new_params_prepared: dict[str, list[str]] = {}
    for k, v in params.items():
        if v is not None:
            if isinstance(v, (list, tuple, set)):
                new_params_prepared[k] = [str(item) for item in v]
            else:
                new_params_prepared[k] = [str(v)]

    if replace:
        updated_params = new_params_prepared
    else:
        # Start with existing params, then update with new ones
        updated_params = current_params.copy()
        updated_params.update(new_params_prepared)  # update merges dictionaries

    # Rebuild the query string
    # urlencode handles the list values correctly with doseq=True
    # (scheme, netloc, path, params, query, fragment)
    # We need to reconstruct the query string from the updated_params dict
    query_string = urllib.parse.urlencode(updated_params, doseq=True)

    # Reconstruct the URL using _replace on the ParseResult
    new_url_parts = parsed._replace(query=query_string)

    return urllib.parse.urlunparse(new_url_parts)


def replace_path_segment(
    url: str, segment_index: int, new_segment: str
) -> str:
    """Replace a specific segment in the URL path."""
    parsed = parse_url(url)  # Use parse_url
    path_segments = [seg for seg in parsed.path.split("/") if seg]

    # Handle edge case: replacing the "root" segment when path is "/" or empty ""
    is_effectively_root = not path_segments and (parsed.path == "/" or parsed.path == "")
    if is_effectively_root and segment_index == 0:
        path_segments = [""]  # Treat root as a single empty segment for replacement

    # Check index bounds *after* potentially modifying path_segments for root case
    if not (0 <= segment_index < len(path_segments)):
        raise IndexError(
            f"Segment index {segment_index} out of range for path '{parsed.path}' ({len(path_segments)} segments found)"
        )

    path_segments[segment_index] = new_segment.strip("/")

    # Reconstruct the path, handling potential leading/trailing slashes
    # Join segments, ensuring leading slash
    new_path = "/" + "/".join(segment for segment in path_segments if segment)  # Filter empty strings post-replacement

    # Preserve trailing slash if original path had one and the new path isn't just "/"
    if parsed.path.endswith("/") and new_path != "/":
        if not new_path.endswith("/"):
            new_path += "/"
    # Handle case where replacement results in effectively empty path "/"
    elif not path_segments or all(s == "" for s in path_segments):
        new_path = "/"

    # Rebuild the URL using _replace
    new_url_parts = parsed._replace(path=new_path)

    return urllib.parse.urlunparse(new_url_parts)
