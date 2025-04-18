"""
Exceptions for the apiconfig library.

This module re-exports all core exception classes for convenient access.
"""

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
]
