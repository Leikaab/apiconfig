"""Integration tests for apiconfig with OneFlow API.

This test demonstrates comprehensive usage of apiconfig patterns:
- Configuration management with ConfigManager and multiple providers
- ApiKeyAuth authentication strategy with custom headers
- HTTP utilities for safe JSON handling and status checking
- URL utilities for proper parameter handling
- Modern HTTP client integration with proper error handling
"""

import os

import pytest

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
from apiconfig.exceptions.auth import AuthStrategyError
from apiconfig.exceptions.http import HTTPUtilsError
from apiconfig.types import HttpMethod
from helpers_for_tests.oneflow.oneflow_client import OneFlowClient
from helpers_for_tests.oneflow.oneflow_config import (
    create_oneflow_client_config,
    create_oneflow_config_manager,
    skip_if_no_credentials,
)


@pytest.fixture
def oneflow_config() -> ClientConfig:
    """Create OneFlow configuration using improved config management."""
    return create_oneflow_client_config()


@pytest.fixture
def oneflow_client(oneflow_config: ClientConfig) -> OneFlowClient:
    """Create a configured OneFlow client.

    Args:
        oneflow_config: Client configuration from oneflow_config fixture.

    Returns:
        OneFlowClient: Configured client instance using improved patterns.
    """
    return OneFlowClient(oneflow_config)


@pytest.fixture
def config_manager() -> ConfigManager:
    """Create a OneFlow configuration manager for advanced testing."""
    return create_oneflow_config_manager()


@pytest.mark.skipif(not os.getenv("ONEFLOW_API_KEY"), reason="OneFlow test credentials not available (ONEFLOW_API_KEY not set)")
class TestOneFlowIntegration:
    """Integration tests for OneFlow API using comprehensive apiconfig patterns."""

    def test_oneflow_apiconfig_setup(self, oneflow_config: ClientConfig) -> None:
        """
        Integration test: apiconfig config and auth for OneFlow.
        Asserts that config is set up correctly using ConfigManager and ApiKeyAuth.
        """
        # Assert base_url is set correctly
        assert oneflow_config.base_url is not None
        assert "oneflow" in oneflow_config.base_url.lower()

        # Auth strategy should be ApiKeyAuth and api_key should be present
        assert oneflow_config.auth_strategy is not None
        assert isinstance(oneflow_config.auth_strategy, ApiKeyAuth)
        assert oneflow_config.auth_strategy.api_key is not None
        assert len(oneflow_config.auth_strategy.api_key) > 0
        assert oneflow_config.auth_strategy.header_name == "x-oneflow-api-token"

        # Check for user email header if configured
        if oneflow_config.headers and "x-oneflow-user-email" in oneflow_config.headers:
            assert len(oneflow_config.headers["x-oneflow-user-email"]) > 0

    def test_oneflow_api_users(self, oneflow_client: OneFlowClient) -> None:
        """
        True integration test: Uses apiconfig to load config/auth and makes a real call to OneFlow API.
        Tests listing users using improved HTTP utilities.

        This test demonstrates enhanced apiconfig workflow:
        1. Configuration loading via ConfigManager with multiple providers
        2. Authentication via ApiKeyAuth with custom headers
        3. HTTP requests with safe JSON handling
        4. URL construction with parameter utilities
        """
        # List users using the improved client
        users = oneflow_client.list_users()

        # Verify response structure
        assert isinstance(users, dict), f"Unexpected response type: {type(users)}"
        assert "data" in users, f"Response dict missing 'data' key: {users.keys()}"
        user_list = users["data"]
        assert isinstance(user_list, list), f"'data' is not a list: {type(user_list)}"
        assert len(user_list) > 0, "No users returned in response."

        # Verify user structure
        first_user = user_list[0]
        assert isinstance(first_user, dict)
        assert "id" in first_user, "No user in response contains an 'id' field."

    def test_oneflow_api_users_with_parameters(self, oneflow_client: OneFlowClient) -> None:
        """Test listing users with query parameters using URL utilities."""
        # Test with query parameters to demonstrate URL utility usage
        params = {"limit": "10", "offset": "0"}
        users = oneflow_client.list_users(params=params)

        # Verify response structure
        assert isinstance(users, dict)
        assert "data" in users
        assert isinstance(users["data"], list)

    def test_list_contracts(self, oneflow_client: OneFlowClient) -> None:
        """Test listing contracts using the improved client."""
        contracts = oneflow_client.list_contracts()

        # OneFlow may return different structures, handle both cases
        if isinstance(contracts, dict):
            # Dict response with data key
            if "data" in contracts:
                assert isinstance(contracts["data"], list)
        elif isinstance(contracts, list):
            # Direct list response
            assert len(contracts) >= 0  # May be empty

    def test_configuration_validation(self) -> None:
        """Test that proper configuration validation occurs.

        This test verifies that the apiconfig components properly
        validate configuration and raise appropriate errors.
        """
        # Test missing credentials - should fail during auth strategy creation
        with pytest.raises(AuthStrategyError):
            ApiKeyAuth(api_key="", header_name="x-oneflow-api-token")

    def test_config_manager_layered_providers(self, config_manager: ConfigManager) -> None:
        """Test that ConfigManager properly loads configuration."""
        # Load configuration from all providers
        config = config_manager.load_config()

        # Test that we can access configuration values (from env or defaults)
        hostname = config.get("hostname")
        assert hostname is not None
        assert "oneflow" in hostname.lower()

        # Test that version is available
        version = config.get("version")
        assert version is not None

        # Test timeout configuration
        timeout = config.get("timeout")
        assert timeout is not None
        assert float(timeout) > 0

    def test_error_handling_with_http_utilities(self, oneflow_client: OneFlowClient) -> None:
        """Test that API errors are handled appropriately using HTTP utilities.

        This test verifies that the client properly handles
        HTTP errors using apiconfig's HTTP utilities and converts
        them to appropriate exceptions.
        """
        # Test with invalid endpoint to trigger error handling
        with pytest.raises(HTTPUtilsError) as exc_info:
            oneflow_client._request(HttpMethod.GET, "/nonexistent")

        # Verify we get proper apiconfig HTTP exceptions
        error_message = str(exc_info.value)
        assert "HTTP request" in error_message or "failed" in error_message.lower()

        # Verify it's not a raw HTTP library error
        assert not isinstance(exc_info.value, ImportError)
        assert not isinstance(exc_info.value, AttributeError)

    def test_client_repr(self, oneflow_client: OneFlowClient) -> None:
        """Test that the client has a useful string representation."""
        repr_str = repr(oneflow_client)
        assert "OneFlowClient" in repr_str
        assert "base_url" in repr_str
        assert "ApiKeyAuth" in repr_str


class TestOneFlowConfigurationPatterns:
    """Tests specifically for configuration management patterns."""

    def test_skip_if_no_credentials_utility(self) -> None:
        """Test the utility function for skipping tests without credentials."""
        # This should either skip or pass, depending on whether credentials are available
        skip_if_no_credentials()
        # If we get here, credentials are available

    def test_config_manager_creation(self) -> None:
        """Test that config manager can be created with proper providers."""
        config_manager = create_oneflow_config_manager()

        # Verify that we can load configuration
        config = config_manager.load_config()
        assert isinstance(config, dict)

        # Verify that we can get configuration values (from env or defaults)
        hostname = config.get("hostname")
        assert hostname is not None

        timeout = config.get("timeout")
        assert timeout is not None


@pytest.mark.skipif(not os.getenv("ONEFLOW_API_KEY"), reason="OneFlow test credentials not available (ONEFLOW_API_KEY not set)")
def test_oneflow_auth_and_list_users(oneflow_config: ClientConfig, oneflow_client: OneFlowClient) -> None:
    """
    Legacy test name preserved for backward compatibility.

    Tests API key authentication and listing users using improved apiconfig patterns.
    """
    # This test maintains the original test name for backward compatibility
    # but now uses the improved implementation

    # Test API key authentication setup
    auth_strategy = oneflow_client.config.auth_strategy
    assert isinstance(auth_strategy, ApiKeyAuth)

    api_key = auth_strategy.api_key
    assert api_key is not None
    assert isinstance(api_key, str)
    assert len(api_key) > 0

    # Test listing users with improved HTTP handling
    users = oneflow_client.list_users()
    assert isinstance(users, dict)
    assert "data" in users
    assert isinstance(users["data"], list)
    assert len(users["data"]) > 0

    # Basic check of user data structure
    first_user = users["data"][0]
    assert isinstance(first_user, dict)
    assert "id" in first_user
