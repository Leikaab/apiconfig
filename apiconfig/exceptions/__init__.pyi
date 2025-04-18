"""
Exceptions for the apiconfig library.

This module re-exports all core exception classes for convenient access.
"""

from .auth import (
    AuthStrategyError as AuthStrategyError,
    ExpiredTokenError as ExpiredTokenError,
    InvalidCredentialsError as InvalidCredentialsError,
    MissingCredentialsError as MissingCredentialsError,
    TokenRefreshError as TokenRefreshError,
)
from .base import (
    APIConfigError as APIConfigError,
    AuthenticationError as AuthenticationError,
    ConfigurationError as ConfigurationError,
)
from .config import (
    ConfigLoadError as ConfigLoadError,
    ConfigProviderError as ConfigProviderError,
    InvalidConfigError as InvalidConfigError,
    MissingConfigError as MissingConfigError,
)

__all__: list[str]
