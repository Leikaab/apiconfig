# -*- coding: utf-8 -*-
# File: apiconfig/testing/__init__.pyi
"""
Testing utilities for apiconfig.

This module provides access to unit and integration testing helpers.
"""

from .unit import (
    BaseAuthStrategyTest as BaseAuthStrategyTest,
    BaseConfigProviderTest as BaseConfigProviderTest,
    MockConfigManager as MockConfigManager,
    MockConfigProvider as MockConfigProvider,
    assert_auth_header_correct as assert_auth_header_correct,
    assert_client_config_valid as assert_client_config_valid,
    assert_provider_loads as assert_provider_loads,
    check_auth_strategy_interface as check_auth_strategy_interface,
    create_auth_credentials as create_auth_credentials,
    create_invalid_client_config as create_invalid_client_config,
    create_mock_client_config as create_mock_client_config,
    create_provider_dict as create_provider_dict,
    create_valid_client_config as create_valid_client_config,
    temp_config_file as temp_config_file,
    temp_env_vars as temp_env_vars,
)

__all__: list[str] = [
    # Unit Testing Helpers
    "BaseAuthStrategyTest",
    "BaseConfigProviderTest",
    "MockConfigManager",
    "MockConfigProvider",
    "assert_auth_header_correct",
    "assert_client_config_valid",
    "assert_provider_loads",
    "check_auth_strategy_interface",
    "create_auth_credentials",
    "create_invalid_client_config",
    "create_mock_client_config",
    "create_provider_dict",
    "create_valid_client_config",
    "temp_config_file",
    "temp_env_vars",
    # Integration Testing (Placeholder - Add when implemented)
    # "integration", # Example
]
