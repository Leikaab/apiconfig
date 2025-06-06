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
from .http import (
    ApiClientBadRequestError,
    ApiClientConflictError,
    ApiClientError,
    ApiClientForbiddenError,
    ApiClientInternalServerError,
    ApiClientNotFoundError,
    ApiClientRateLimitError,
    ApiClientUnauthorizedError,
    ApiClientUnprocessableEntityError,
    HTTPUtilsError,
    JSONDecodeError,
    JSONEncodeError,
    PayloadTooLargeError,
    create_api_client_error,
)

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
    "JSONEncodeError",
    "PayloadTooLargeError",
    # API client exceptions
    "ApiClientError",
    "ApiClientBadRequestError",
    "ApiClientUnauthorizedError",
    "ApiClientForbiddenError",
    "ApiClientNotFoundError",
    "ApiClientConflictError",
    "ApiClientUnprocessableEntityError",
    "ApiClientRateLimitError",
    "ApiClientInternalServerError",
    "create_api_client_error",
]
