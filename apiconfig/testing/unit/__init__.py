# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/__init__.py
"""Unit testing utilities for apiconfig."""

from .assertions import (
    assert_auth_header_correct,
    assert_client_config_valid,
    assert_provider_loads,
)
from .factories import (
    create_auth_credentials,
    create_invalid_client_config,
    create_provider_dict,
    create_valid_client_config,
)
from .mocks import (
    MockConfigManager,
    MockConfigProvider,
    create_mock_client_config,
)

__all__ = [
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
