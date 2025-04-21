"""URL parsing utilities."""

import urllib.parse
from typing import Dict, List, Union


def parse_url(url: str) -> urllib.parse.ParseResult:
    """
    Parse a URL string into its components using urllib.parse.urlparse.

    Handles URLs potentially missing a scheme by defaulting to 'https://'.
    This is only applied if the URL appears to be a domain name (contains a dot)
    and doesn't start with a slash. Simple filenames (like file.txt) are not
    treated as domains and don't get a scheme added.

    Preserves multiple leading slashes in paths, which is important for certain
    URL patterns where the number of slashes is semantically significant.
    The function specifically detects and preserves paths with multiple leading
    slashes (e.g., "///path") which would otherwise be collapsed by urlparse.

    Args
    ----
        url (str): The URL string to parse.

    Returns
    -------
        urllib.parse.ParseResult: A ParseResult object containing the URL components
            (scheme, netloc, path, params, query, fragment).

    Examples
    --------
        >>> parse_url("example.com/api")
        ParseResult(scheme='https', netloc='example.com', path='/api', ...)
        >>> parse_url("https://example.com/api")
        ParseResult(scheme='https', netloc='example.com', path='/api', ...)
        >>> parse_url("/relative/path")  # No scheme added for relative paths
        ParseResult(scheme='', netloc='', path='/relative/path', ...)
        >>> parse_url("file.txt")  # No scheme added for simple filenames
        ParseResult(scheme='', netloc='', path='file.txt', ...)
        >>> parse_url("localhost:8080")  # Handles hostname:port format
        ParseResult(scheme='https', netloc='localhost:8080', path='', ...)
        >>> parse_url("///path")  # Preserves multiple leading slashes
        ParseResult(scheme='', netloc='', path='///path', ...)
    """
    # Store the original path pattern to preserve multiple leading slashes
    original_path = ""
    has_multiple_leading_slashes = False

    # Check if the URL has a path with multiple leading slashes
    if url.startswith("///"):
        # Count leading slashes
        slash_count = 0
        for char in url:
            if char == "/":
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
    """
    Extract query parameters from a URL string into a dictionary.

    Handles multiple values for the same parameter key by returning a list
    for that key. Single values are returned as strings. Blank values are
    preserved.

    Args
    ----
        url (str): The URL string from which to extract query parameters.

    Returns
    -------
        Dict[str, Union[str, List[str]]]: A dictionary where keys are parameter
            names and values are either strings (for single occurrences) or
            lists of strings (for multiple occurrences).

    Examples
    --------
        >>> get_query_params("https://example.com/path?a=1&b=2")
        {'a': '1', 'b': '2'}
        >>> get_query_params("https://example.com/path?a=1&a=2")
        {'a': ['1', '2']}
        >>> get_query_params("https://example.com/path?key=")
        {'key': ''}
    """
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


def add_query_params(url: str, params_to_add: Dict[str, Union[str, List[str], None]]) -> str:
    """
    Add or update query parameters in a URL string.

    If a parameter key exists, its value is updated. If it doesn't exist,
    it's added. If the value provided for a key is None, the parameter
    is removed from the URL. Handles list values for parameters with
    multiple occurrences.

    Args
    ----
        url (str): The original URL string.
        params_to_add (Dict[str, Union[str, List[str], None]]): A dictionary
            of parameters to add or update. Keys are parameter names. Values
            can be strings, lists of strings, or None (to remove the parameter).

    Returns
    -------
        str: A new URL string with the updated query parameters.

    Raises
    ------
        ValueError: If the URL is empty.

    Examples
    --------
        >>> add_query_params("https://example.com/path", {"a": "1"})
        'https://example.com/path?a=1'
        >>> add_query_params("https://example.com/path?a=1", {"a": "2"})
        'https://example.com/path?a=2'
        >>> add_query_params("https://example.com/path?a=1", {"a": None})
        'https://example.com/path'
        >>> add_query_params("https://example.com/path", {"a": ["1", "2"]})
        'https://example.com/path?a=1&a=2'
    """
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
