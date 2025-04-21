"""
Exceptions for the apiconfig library.

This module re-exports all core exception classes from the apiconfig.exceptions
submodules for convenient access. Import exceptions directly from this module
rather than from individual submodules for better maintainability.

The exceptions are organized into categories:
- Base exceptions: Core exception hierarchy
- Auth exceptions: Authentication and credential-related errors
- Config exceptions: Configuration loading and validation errors
- HTTP exceptions: HTTP request/response and JSON handling errors
"""

from .auth import AuthStrategyError as AuthStrategyError
from .auth import ExpiredTokenError as ExpiredTokenError
from .auth import InvalidCredentialsError as InvalidCredentialsError
from .auth import MissingCredentialsError as MissingCredentialsError
from .auth import TokenRefreshError as TokenRefreshError
from .base import APIConfigError as APIConfigError
from .base import AuthenticationError as AuthenticationError
from .base import ConfigurationError as ConfigurationError
from .config import ConfigLoadError as ConfigLoadError
from .config import ConfigProviderError as ConfigProviderError
from .config import InvalidConfigError as InvalidConfigError
from .config import MissingConfigError as MissingConfigError
from .http import HTTPUtilsError as HTTPUtilsError
from .http import JSONDecodeError as JSONDecodeError

__all__: list[str] = [
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
