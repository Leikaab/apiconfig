# -*- coding: utf-8 -*-
"""
Authentication strategies and base classes for apiconfig (stub).

This module provides the core components for handling API authentication,
including the base strategy class and common implementations.
"""

from typing import List

from .base import AuthStrategy as AuthStrategy
from .strategies import ApiKeyAuth as ApiKeyAuth
from .strategies import BasicAuth as BasicAuth
from .strategies import BearerAuth as BearerAuth
from .strategies import CustomAuth as CustomAuth

__all__: List[str] = [
    "AuthStrategy",
    "BasicAuth",
    "BearerAuth",
    "ApiKeyAuth",
    "CustomAuth",
]
