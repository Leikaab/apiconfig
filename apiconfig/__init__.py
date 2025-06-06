# -*- coding: utf-8 -*-
"""
apiconfig: A library for flexible API configuration and authentication.

This library provides components for managing API client configurations
(like base URLs, timeouts, retries) and handling various authentication
strategies (Basic, Bearer, API Key, etc.).
"""

import importlib.metadata
import logging

# Core components re-exported for easier access
from .auth.base import AuthStrategy
from .auth.strategies import ApiKeyAuth, BasicAuth, BearerAuth, CustomAuth
from .config.base import ClientConfig
from .config.manager import ConfigManager
from .config.providers import EnvProvider, FileProvider, MemoryProvider
from .exceptions.auth import (
    AuthenticationError,
    AuthStrategyError,
    ExpiredTokenError,
    InvalidCredentialsError,
    MissingCredentialsError,
    TokenRefreshError,
)
from .exceptions.base import APIConfigError, ConfigurationError
from .exceptions.config import (
    ConfigLoadError,
    ConfigProviderError,
    InvalidConfigError,
    MissingConfigError,
)
from .types import (
    AuthCredentials,
    ConfigDict,
    DataType,
    HeadersType,
    JsonObject,
    JsonValue,
    QueryParamType,
    TokenRefreshCallable,
    TokenStorageStrategy,
)

try:
    __version__: str = importlib.metadata.version("apiconfig")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover - fallback for local use
    __version__ = "0.0.0"

# Define public API
__all__: list[str] = [
    # Config
    "ClientConfig",
    "ConfigManager",
    "EnvProvider",
    "FileProvider",
    "MemoryProvider",
    # Auth
    "AuthStrategy",
    "BasicAuth",
    "BearerAuth",
    "ApiKeyAuth",
    "CustomAuth",
    # Exceptions
    "APIConfigError",
    "ConfigurationError",
    "MissingConfigError",
    "InvalidConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
    "AuthenticationError",
    "MissingCredentialsError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "TokenRefreshError",
    "AuthStrategyError",
    # Types
    "HeadersType",
    "QueryParamType",
    "DataType",
    "ConfigDict",
    "AuthCredentials",
    "TokenStorageStrategy",
    "TokenRefreshCallable",
    "JsonValue",
    "JsonObject",
]

# Configure null handler for library logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
