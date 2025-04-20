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
from .auth.strategies import ApiKeyAuth as ApiKeyAuth
from .auth.strategies import BasicAuth as BasicAuth
from .auth.strategies import BearerAuth as BearerAuth
from .auth.strategies import CustomAuth as CustomAuth
from .config.base import ClientConfig as ClientConfig
from .config.manager import ConfigManager as ConfigManager
from .config.providers import EnvProvider as EnvProvider
from .config.providers import FileProvider as FileProvider
from .config.providers import MemoryProvider as MemoryProvider
from .exceptions.auth import AuthenticationError as AuthenticationError
from .exceptions.auth import AuthStrategyError as AuthStrategyError
from .exceptions.auth import ExpiredTokenError as ExpiredTokenError
from .exceptions.auth import InvalidCredentialsError as InvalidCredentialsError
from .exceptions.auth import MissingCredentialsError as MissingCredentialsError
from .exceptions.auth import TokenRefreshError as TokenRefreshError
from .exceptions.base import APIConfigError as APIConfigError
from .exceptions.base import ConfigurationError as ConfigurationError
from .exceptions.config import ConfigLoadError as ConfigLoadError
from .exceptions.config import ConfigProviderError as ConfigProviderError
from .exceptions.config import InvalidConfigError as InvalidConfigError
from .exceptions.config import MissingConfigError as MissingConfigError
from .types import AuthCredentials as AuthCredentials
from .types import ConfigDict as ConfigDict
from .types import DataType as DataType
from .types import HeadersType as HeadersType
from .types import JsonObject as JsonObject
from .types import JsonValue as JsonValue
from .types import ParamsType as ParamsType
from .types import TokenRefreshCallable as TokenRefreshCallable
from .types import TokenStorageStrategy as TokenStorageStrategy

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
