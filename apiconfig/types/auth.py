"""Authentication-related type definitions."""

from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Protocol,
    TypeAlias,
    TypedDict,
    runtime_checkable,
)

# Authentication Types
AuthCredentials: TypeAlias = Dict[str, Any]
"""Type alias for authentication credentials."""

# Token Types
TokenData: TypeAlias = Dict[str, Any]
"""Type alias for token data."""

RefreshedTokenData: TypeAlias = Dict[str, Any]
"""Type alias for refreshed token data."""


class TokenRefreshResult(TypedDict, total=False):
    """Type for token refresh operation results."""

    token_data: Optional[TokenData]
    config_updates: Optional[Dict[str, Any]]


# Callback Types
TokenRefreshCallable: TypeAlias = Callable[[], Optional[TokenRefreshResult]]
"""Type alias for a callable that refreshes tokens."""

AuthRefreshCallback: TypeAlias = Callable[[], None]
"""Type alias for authentication refresh callback."""

HttpRequestCallable: TypeAlias = Callable[[], Any]
"""Type alias for HTTP request callable."""

CustomAuthPrepareCallable: TypeAlias = Callable[[Any], Any]
"""Type alias for custom authentication preparation callable."""

# Storage Strategy Protocol


@runtime_checkable
class TokenStorageStrategy(Protocol):
    """Protocol for token storage strategies."""

    def store_token(self, key: str, token_data: TokenData) -> None:
        """Store token data."""
        ...

    def retrieve_token(self, key: str) -> Optional[TokenData]:
        """Retrieve token data."""
        ...

    def remove_token(self, key: str) -> None:
        """Remove token data."""
        ...


__all__ = [
    "AuthCredentials",
    "TokenData",
    "RefreshedTokenData",
    "TokenRefreshResult",
    "TokenRefreshCallable",
    "AuthRefreshCallback",
    "HttpRequestCallable",
    "CustomAuthPrepareCallable",
    "TokenStorageStrategy",
]
