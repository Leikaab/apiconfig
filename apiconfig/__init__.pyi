# -*- coding: utf-8 -*-
"""
apiconfig: A library for flexible API configuration and authentication (stub).

This library provides components for managing API client configurations
(like base URLs, timeouts, retries) and handling various authentication
strategies (Basic, Bearer, API Key, etc.).
"""

from typing import List

# Core components re-exported for easier access
from .auth.base import AuthStrategy as AuthStrategy
from .auth.strategies import (
    ApiKeyAuth as ApiKeyAuth,
    BasicAuth as BasicAuth,
    BearerAuth as BearerAuth,
    CustomAuth as CustomAuth,
)
from .config.base import ClientConfig as ClientConfig
from .config.manager import ConfigManager as ConfigManager
from .config.providers import (
    EnvProvider as EnvProvider,
    FileProvider as FileProvider,
    MemoryProvider as MemoryProvider,
)
from .exceptions.auth import (
    AuthenticationError as AuthenticationError,
    AuthStrategyError as AuthStrategyError,
    ExpiredTokenError as ExpiredTokenError,
    InvalidCredentialsError as InvalidCredentialsError,
    MissingCredentialsError as MissingCredentialsError,
    TokenRefreshError as TokenRefreshError,
)
from .exceptions.base import APIConfigError as APIConfigError, ConfigurationError as ConfigurationError  # Import ConfigurationError from base
from .exceptions.config import (
    ConfigLoadError as ConfigLoadError,
    ConfigProviderError as ConfigProviderError,
    InvalidConfigError as InvalidConfigError,
    MissingConfigError as MissingConfigError,
)  # Remove ConfigurationError import from config
from .types import (
    AuthCredentials as AuthCredentials,
    ConfigDict as ConfigDict,
    DataType as DataType,
    HeadersType as HeadersType,
    JsonObject as JsonObject,
    JsonValue as JsonValue,
    ParamsType as ParamsType,
    TokenRefreshCallable as TokenRefreshCallable,
    TokenStorageStrategy as TokenStorageStrategy,
)

__version__: str
__all__: List[str] = [
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
    "ParamsType",
    "DataType",
    "ConfigDict",
    "AuthCredentials",
    "TokenStorageStrategy",
    "TokenRefreshCallable",
    "JsonValue",
    "JsonObject",
]
