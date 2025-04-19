# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/__init__.pyi
"""
Unit testing utilities for apiconfig.

This module re-exports utilities from submodules like mocks, factories, and assertions.
"""

from .assertions import (
    assert_auth_header_correct as assert_auth_header_correct,
    assert_client_config_valid as assert_client_config_valid,
    assert_provider_loads as assert_provider_loads,
)
from .factories import (
    create_auth_credentials as create_auth_credentials,
    create_invalid_client_config as create_invalid_client_config,
    create_provider_dict as create_provider_dict,
    create_valid_client_config as create_valid_client_config,
)
from .mocks import (
    MockConfigManager as MockConfigManager,
    MockConfigProvider as MockConfigProvider,
    create_mock_client_config as create_mock_client_config,
)

__all__: list[str] = [
    # Assertions
    "assert_auth_header_correct",
    "assert_client_config_valid",
    "assert_provider_loads",
    # Factories
    "create_auth_credentials",
    "create_invalid_client_config",
    "create_provider_dict",
    "create_valid_client_config",
    # Mocks
    "MockConfigProvider",
    "create_mock_client_config",
    "MockConfigManager",
]
