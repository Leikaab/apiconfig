# -*- coding: utf-8 -*-
"""
Authentication strategies and base classes for apiconfig.

This module provides the core components for handling API authentication,
including the base strategy class and common implementations.
"""

from .base import AuthStrategy
from .strategies import ApiKeyAuth, BasicAuth, BearerAuth, CustomAuth

__all__: list[str] = [
    "AuthStrategy",
    "BasicAuth",
    "BearerAuth",
    "ApiKeyAuth",
    "CustomAuth",
]
