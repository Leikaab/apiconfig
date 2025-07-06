# -*- coding: utf-8 -*-
"""
Integration testing utilities for apiconfig.

This package provides tools for setting up and running integration tests,
including mock servers and test fixtures.
"""

import typing

import httpx

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager

from .helpers import make_request_with_config as _make_request_with_config
from .helpers import setup_multi_provider_manager as _setup_multi_provider_manager
from .servers import configure_mock_response

make_request_with_config: typing.Callable[
    [ClientConfig, AuthStrategy, str, str, str],
    httpx.Response,
] = _make_request_with_config

setup_multi_provider_manager: typing.Callable[
    [list[tuple[str, dict[str, typing.Any]]]],
    ConfigManager,
] = _setup_multi_provider_manager

__all__: list[str] = [
    "configure_mock_response",
    "make_request_with_config",
    "setup_multi_provider_manager",
]
