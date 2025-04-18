from collections.abc import Mapping
from typing import Dict, Set, Tuple

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
) -> Dict[str, str]:
    redacted_headers: Dict[str, str] = {}
    if not headers:
        return redacted_headers

    for name, value in headers.items():
        lower_name = name.lower()
        is_sensitive = lower_name in sensitive_keys or lower_name.startswith(
            sensitive_prefixes
        )
        # Ensure value is treated as a string for consistency
        redacted_headers[name] = REDACTED_VALUE if is_sensitive else str(value)
    return redacted_headers
