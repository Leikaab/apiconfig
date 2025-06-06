# -*- coding: utf-8 -*-
# File: apiconfig/testing/__init__.py
"""
Testing utilities for apiconfig.

This module provides access to unit and integration testing helpers.
"""

from .auth_verification import (
    AdvancedAuthVerification,
    AuthHeaderVerification,
    AuthTestHelpers,
)
from .unit import (
    BaseAuthStrategyTest,
    BaseConfigProviderTest,
    MockConfigManager,
    MockConfigProvider,
    assert_auth_header_correct,
    assert_client_config_valid,
    assert_provider_loads,
    check_auth_strategy_interface,
    create_auth_credentials,
    create_invalid_client_config,
    create_mock_client_config,
    create_provider_dict,
    create_valid_client_config,
    temp_config_file,
    temp_env_vars,
)

__all__: list[str] = [
    # Auth Verification Utilities
    "AdvancedAuthVerification",
    "AuthHeaderVerification",
    "AuthTestHelpers",
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
