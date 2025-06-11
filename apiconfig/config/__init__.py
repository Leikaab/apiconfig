# -*- coding: utf-8 -*-
"""
Configuration handling for apiconfig.

This module provides the base configuration class (`ClientConfig`),
configuration management (`ConfigManager`), and various configuration
providers (environment, file, memory).
"""

from .base import ClientConfig
from .manager import ConfigManager
from .providers import EnvProvider, FileProvider, MemoryProvider

__all__: list[str] = [
    "ClientConfig",
    "ConfigManager",
    "EnvProvider",
    "FileProvider",
    "MemoryProvider",
]
