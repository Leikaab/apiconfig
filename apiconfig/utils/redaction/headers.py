import re
from collections.abc import Mapping
from typing import Dict, Optional, Set, Tuple

# Default set of sensitive header keys (lowercase)
DEFAULT_SENSITIVE_HEADERS: Set[str] = {
    "authorization",
    "cookie",
    "set-cookie",
    "proxy-authorization",
}

# Default tuple of sensitive header prefixes (lowercase)
DEFAULT_SENSITIVE_HEADER_PREFIXES: Tuple[str, ...] = (
    "x-api-key",
    "x-auth-token",
)

# Placeholder value for redacted headers
REDACTED_VALUE: str = "[REDACTED]"


def redact_headers(
    headers: Mapping[str, str],
    sensitive_keys: Set[str] = DEFAULT_SENSITIVE_HEADERS,
    sensitive_prefixes: Tuple[str, ...] = DEFAULT_SENSITIVE_HEADER_PREFIXES,
    sensitive_name_pattern: Optional[re.Pattern] = None,
) -> Dict[str, str]:
    redacted_headers: Dict[str, str] = {}
    if not headers:
        return redacted_headers

    for name, value in headers.items():
        lower_name = name.lower()
        is_sensitive_by_key = lower_name in sensitive_keys
        is_sensitive_by_prefix = lower_name.startswith(sensitive_prefixes)
        is_sensitive_by_pattern = bool(
            sensitive_name_pattern and sensitive_name_pattern.search(name)
        )

        is_sensitive = (
            is_sensitive_by_key or is_sensitive_by_prefix or is_sensitive_by_pattern
        )

        # Ensure value is treated as a string for consistency
        redacted_headers[name] = REDACTED_VALUE if is_sensitive else str(value)
    return redacted_headers
