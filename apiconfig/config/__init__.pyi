# -*- coding: utf-8 -*-
"""
Configuration handling for apiconfig (stub).

This module provides the base configuration class (`ClientConfig`),
configuration management (`ConfigManager`), and various configuration
providers (environment, file, memory).
"""

from typing import List

from .base import ClientConfig as ClientConfig
from .manager import ConfigManager as ConfigManager
from .providers import EnvProvider as EnvProvider
from .providers import FileProvider as FileProvider
from .providers import MemoryProvider as MemoryProvider

__all__: List[str] = [
    "ClientConfig",
    "ConfigManager",
    "EnvProvider",
    "FileProvider",
    "MemoryProvider",
]
