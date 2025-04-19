from collections.abc import Mapping
from typing import Dict, Final, Set, Tuple

# Default set of sensitive header keys (lowercase)
DEFAULT_SENSITIVE_HEADERS: Final[Set[str]]

# Default tuple of sensitive header prefixes (lowercase)
DEFAULT_SENSITIVE_HEADER_PREFIXES: Final[Tuple[str, ...]]

# Placeholder value for redacted headers
REDACTED_VALUE: Final[str]

def redact_headers(
    headers: Mapping[str, str],
    sensitive_keys: Set[str] = ...,
    sensitive_prefixes: Tuple[str, ...] = ...,
) -> Dict[str, str]:
    """
    Redacts sensitive information from HTTP headers.

    Iterates through a mapping of headers, identifies sensitive headers based on
    predefined keys and prefixes (case-insensitive), and replaces their values
    with a placeholder string.

    Args:
        headers: A mapping (e.g., dictionary) of header names to values.
        sensitive_keys: A set of lowercase header names to consider sensitive.
                        Defaults to `DEFAULT_SENSITIVE_HEADERS`.
        sensitive_prefixes: A tuple of lowercase header prefixes to consider sensitive.
                            Defaults to `DEFAULT_SENSITIVE_HEADER_PREFIXES`.

    Returns:
        A new dictionary containing the headers with sensitive values redacted.
        Returns an empty dictionary if the input `headers` is None or empty.
    """
    ...
