import re
from collections.abc import Mapping
from typing import Dict, Final, Optional, Set, Tuple

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
    sensitive_name_pattern: Optional[re.Pattern[str]] = ...,
) -> Dict[str, str]:
    """
    Redacts sensitive information from HTTP headers.

    Iterates through a mapping of headers, identifies sensitive headers based on
    predefined keys, prefixes (case-insensitive), or a regex pattern for the
    header name, and replaces their values with a placeholder string.

    Args:
        headers: A mapping (e.g., dictionary) of header names to values.
        sensitive_keys: A set of lowercase header names to consider sensitive.
                        Defaults to `DEFAULT_SENSITIVE_HEADERS`.
        sensitive_prefixes: A tuple of lowercase header prefixes to consider sensitive.
                            Defaults to `DEFAULT_SENSITIVE_HEADER_PREFIXES`.
        sensitive_name_pattern: An optional compiled regex pattern. If provided,
                                header names matching this pattern (case-insensitive)
                                will also be redacted. Defaults to `None`.

    Returns:
        A new dictionary containing the headers with sensitive values redacted.
        Returns an empty dictionary if the input `headers` is None or empty.
    """
    ...
