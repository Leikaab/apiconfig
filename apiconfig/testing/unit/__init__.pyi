# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/__init__.pyi
"""
Unit testing utilities for apiconfig.

This module re-exports utilities from submodules like mocks, factories, and assertions.
"""

from .assertions import assert_client_config_valid as assert_client_config_valid
from .factories import create_auth_credentials as create_auth_credentials
from .factories import create_invalid_client_config as create_invalid_client_config
from .factories import create_provider_dict as create_provider_dict
from .factories import create_valid_client_config as create_valid_client_config
from .helpers import BaseAuthStrategyTest as BaseAuthStrategyTest
from .helpers import BaseConfigProviderTest as BaseConfigProviderTest
from .helpers import assert_auth_header_correct as assert_auth_header_correct
from .helpers import assert_provider_loads as assert_provider_loads
from .helpers import check_auth_strategy_interface as check_auth_strategy_interface
from .helpers import temp_config_file as temp_config_file
from .helpers import temp_env_vars as temp_env_vars
from .mocks import MockConfigManager as MockConfigManager
from .mocks import MockConfigProvider as MockConfigProvider
from .mocks import create_mock_client_config as create_mock_client_config

__all__: list[str] = [
    # Assertions (from assertions.py)
    "assert_client_config_valid",
    # Factories
    "create_auth_credentials",
    "create_invalid_client_config",
    "create_provider_dict",
    "create_valid_client_config",
    # Mocks
    "MockConfigProvider",
    "create_mock_client_config",
    "MockConfigManager",
    # Helpers (from helpers.py)
    "BaseAuthStrategyTest",
    "BaseConfigProviderTest",
    "assert_auth_header_correct",  # Re-exported from helpers
    "assert_provider_loads",  # Re-exported from helpers
    "check_auth_strategy_interface",
    "temp_config_file",
    "temp_env_vars",
]
