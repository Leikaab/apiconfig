import urllib.parse
from typing import Dict, List, Union


def parse_url(url: str) -> urllib.parse.ParseResult:
    """Parses a URL string into its components using urllib.parse.urlparse."""
    # Store the original path pattern to preserve multiple leading slashes
    original_path = ""
    has_multiple_leading_slashes = False

    # Check if the URL has a path with multiple leading slashes
    if url.startswith("///"):
        # Count leading slashes
        slash_count = 0
        for char in url:
            if char == '/':
                slash_count += 1
            else:
                break

        if slash_count > 2:
            has_multiple_leading_slashes = True
            original_path = "/" * slash_count + url[slash_count:]

    # Add a default scheme ONLY if it looks like a domain name is provided without one.
    # Do not add for relative paths or URLs starting with //.
    if "://" not in url and not url.startswith("//") and not url.startswith("/"):
        # Basic check: does it contain a dot and doesn't look like a simple filename?
        # This is imperfect but covers common cases like 'example.com/path'.
        # More robust domain detection could be added if needed.
        first_part = url.split("/")[0]

        # Check for hostname:port format (like localhost:8080)
        if ":" in first_part:
            # Only add scheme if it looks like a hostname:port, not a scheme:path
            host_part = first_part.split(":")[0]
            port_part = first_part.split(":")[1]
            # If port_part is numeric, it's likely a port number
            if port_part.isdigit() or host_part in ("localhost", "127.0.0.1"):
                url = f"https://{url}"
        elif "." in first_part and not first_part.endswith(".txt"):  # Don't add scheme to simple filenames
            url = f"https://{url}"

    # Parse the URL
    parsed = urllib.parse.urlparse(url)

    # If we detected multiple leading slashes, restore them in the path
    if has_multiple_leading_slashes:
        # Create a new ParseResult with the original path pattern
        parsed = parsed._replace(path=original_path)

    return parsed


def get_query_params(url: str) -> Dict[str, Union[str, List[str]]]:
    """Extracts query parameters from a URL into a dictionary."""
    parsed_url = parse_url(url)
    query_string = parsed_url.query
    params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
    # parse_qs returns list values, simplify single-item lists
    simple_params: Dict[str, Union[str, List[str]]] = {}
    for key, value in params.items():
        if len(value) == 1:
            simple_params[key] = value[0]
        else:
            simple_params[key] = value
    return simple_params


def add_query_params(
    url: str, params_to_add: Dict[str, Union[str, List[str], None]]
) -> str:
    """Adds or updates query parameters in a URL."""
    if not url:
        raise ValueError("URL cannot be empty")

    parsed_url = parse_url(url)
    existing_params = urllib.parse.parse_qs(parsed_url.query, keep_blank_values=True)

    # Update existing params with new ones
    for key, value in params_to_add.items():
        if value is None:
            # Remove parameter if value is None
            existing_params.pop(key, None)
        elif isinstance(value, list):
            existing_params[key] = [str(v) for v in value]
        else:
            existing_params[key] = [str(value)]

    # Rebuild the query string
    new_query_string = urllib.parse.urlencode(existing_params, doseq=True)

    # Reconstruct the URL
    # Use _replace which is the documented way to create a modified URL tuple
    new_url_parts = parsed_url._replace(query=new_query_string)
    return urllib.parse.urlunparse(new_url_parts)
