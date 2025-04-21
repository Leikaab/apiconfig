"""Internal implementation of exceptions package."""

from .auth import (
    AuthStrategyError,
    ExpiredTokenError,
    InvalidCredentialsError,
    MissingCredentialsError,
    TokenRefreshError,
)
from .base import APIConfigError, AuthenticationError, ConfigurationError
from .config import (
    ConfigLoadError,
    ConfigProviderError,
    InvalidConfigError,
    MissingConfigError,
)
from .http import HTTPUtilsError, JSONDecodeError

__all__ = [
    # Base exceptions
    "APIConfigError",
    "ConfigurationError",
    "AuthenticationError",
    # Auth exceptions
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "AuthStrategyError",
    # Config exceptions
    "InvalidConfigError",
    "MissingConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
    # HTTP exceptions
    "HTTPUtilsError",
    "JSONDecodeError",
]
