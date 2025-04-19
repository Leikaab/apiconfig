import urllib.parse
from typing import Dict, List, Optional, Tuple, Union

def parse_url(url: str) -> urllib.parse.ParseResult:
    """
    Parses a URL string into its components using urllib.parse.urlparse.

    Handles URLs potentially missing a scheme by defaulting to 'https://'.

    Args:
        url: The URL string to parse.

    Returns:
        A ParseResult object containing the URL components (scheme, netloc,
        path, params, query, fragment).
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
    """
    ...

def add_query_params(
    url: str, params_to_add: Dict[str, Union[str, List[str], None]]
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
                       lists of strings, or None (to remove the parameter).

    Returns:
        A new URL string with the updated query parameters.
    """
    ...
