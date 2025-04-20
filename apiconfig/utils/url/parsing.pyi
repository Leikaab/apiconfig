import urllib.parse
from typing import Any, Dict, List, Union


def parse_url(url: str) -> urllib.parse.ParseResult:
    """
    Parses a URL string into its components using urllib.parse.urlparse.

    Handles URLs potentially missing a scheme by defaulting to 'https://'.
    This is only applied if the URL appears to be a domain name (contains a dot)
    and doesn't start with a slash. Simple filenames (like file.txt) are not
    treated as domains and don't get a scheme added.

    Preserves multiple leading slashes in paths, which is important for certain
    URL patterns where the number of slashes is semantically significant.
    The function specifically detects and preserves paths with multiple leading
    slashes (e.g., "///path") which would otherwise be collapsed by urlparse.

    Args:
        url: The URL string to parse.

    Returns:
        A ParseResult object containing the URL components (scheme, netloc,
        path, params, query, fragment).

    Examples:
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
    ...


def get_query_params(url: str) -> Dict[str, Union[str, List[str]]]:
    """
    Extracts query parameters from a URL string into a dictionary.

    Handles multiple values for the same parameter key by returning a list
    for that key. Single values are returned as strings. Blank values are
    preserved.

    Args:
        url: The URL string from which to extract query parameters.

    Returns:
        A dictionary where keys are parameter names and values are either
        strings (for single occurrences) or lists of strings (for multiple
        occurrences).

    Examples:
        >>> get_query_params("https://example.com/path?a=1&b=2")
        {'a': '1', 'b': '2'}
        >>> get_query_params("https://example.com/path?a=1&a=2")
        {'a': ['1', '2']}
        >>> get_query_params("https://example.com/path?key=")
        {'key': ''}
    """
    ...


def add_query_params(
    url: str, params_to_add: Dict[str, Any]
) -> str:
    """
    Adds or updates query parameters in a URL string.

    If a parameter key exists, its value is updated. If it doesn't exist,
    it's added. If the value provided for a key is None, the parameter
    is removed from the URL. Handles list values for parameters with
    multiple occurrences.

    Args:
        url: The original URL string.
        params_to_add: A dictionary of parameters to add or update.
                      Keys are parameter names. Values can be strings,
                      lists of strings, dictionaries, or any other type
                      (which will be converted to strings), or None
                      (to remove the parameter).

    Returns:
        A new URL string with the updated query parameters.

    Raises:
        ValueError: If the URL is empty.

    Examples:
        >>> add_query_params("https://example.com/path", {"a": "1"})
        'https://example.com/path?a=1'
        >>> add_query_params("https://example.com/path?a=1", {"a": "2"})
        'https://example.com/path?a=2'
        >>> add_query_params("https://example.com/path?a=1", {"a": None})
        'https://example.com/path'
        >>> add_query_params("https://example.com/path", {"a": ["1", "2"]})
        'https://example.com/path?a=1&a=2'
    """
    ...
