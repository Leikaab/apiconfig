# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/__init__.py
"""Unit testing utilities for apiconfig."""

from .assertions import assert_client_config_valid
from .factories import (
    create_auth_credentials,
    create_invalid_client_config,
    create_provider_dict,
    create_valid_client_config,
)
from .helpers import (
    BaseAuthStrategyTest,
    BaseConfigProviderTest,
    assert_auth_header_correct,
    assert_provider_loads,
    check_auth_strategy_interface,
    temp_config_file,
    temp_env_vars,
)
from .mocks import (
    MockConfigManager,
    MockConfigProvider,
    create_mock_client_config,
)

__all__ = [
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
