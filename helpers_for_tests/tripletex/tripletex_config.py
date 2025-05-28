"""Configuration management for Tripletex integration tests using apiconfig patterns."""

import os
from typing import Any, Optional

import pytest
from dotenv import load_dotenv

from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.env import EnvProvider
from apiconfig.config.providers.memory import MemoryProvider
from helpers_for_tests.tripletex.tripletex_auth import TripletexSessionAuth


def create_tripletex_config_manager() -> ConfigManager:
    """
    Create a ConfigManager for Tripletex configuration from environment variables with sensible defaults.

    Returns
    -------
    ConfigManager
        Configured manager for loading Tripletex settings.
    """
    # Load environment variables
    load_dotenv(dotenv_path=".env", override=True)

    # Sensible defaults for non-sensitive configuration values
    defaults = {
        "hostname": "https://api-test.tripletex.tech",
        "version": "v2",
        "timeout": "30.0",
        "company_id": "0",
    }

    # Create providers - environment variables first, then defaults
    providers = [
        EnvProvider(prefix="TRIPLETEX_TEST_"),
        MemoryProvider(config_data=defaults),
    ]

    return ConfigManager(providers=providers)


def create_tripletex_auth_strategy(config_manager: ConfigManager) -> TripletexSessionAuth:
    """
    Create a TripletexSessionAuth strategy using configuration from the manager.

    Args
    ----
    config_manager : ConfigManager
        ConfigManager instance to load auth settings from.

    Returns
    -------
    TripletexSessionAuth
        Configured authentication strategy.

    Raises
    ------
    pytest.skip
        If required credentials are missing.
    ConfigurationError
        If credentials are invalid.
    """
    # Load configuration from all providers
    config = config_manager.load_config()

    try:
        consumer_token = config["CONSUMER_TOKEN"]
        employee_token = config["EMPLOYEE_TOKEN"]
    except KeyError as e:
        pytest.skip(f"Missing required environment variable: TRIPLETEX_TEST_{e}")

    if not consumer_token or not employee_token:
        pytest.skip("TRIPLETEX_TEST_CONSUMER_TOKEN or TRIPLETEX_TEST_EMPLOYEE_TOKEN environment variables are empty")

    # Get additional configuration (defaults provided by config manager)
    hostname = config["hostname"]
    company_id = config["company_id"]
    version = config["version"]

    # Create a simple HTTP callable for refresh operations
    def http_request_callable(*args: Any, **kwargs: Any) -> None:
        """Make HTTP request for refresh operations."""
        # This is a placeholder - the actual refresh will use the existing _fetch_session_token method
        # which uses urllib.request internally

    return TripletexSessionAuth(
        consumer_token=consumer_token,
        employee_token=employee_token,
        company_id=company_id,
        session_token_hostname=hostname,
        token_api_version=version,
        http_request_callable=http_request_callable,
    )


def create_tripletex_client_config() -> ClientConfig:
    """
    Create a complete ClientConfig for Tripletex using apiconfig patterns.

    Returns
    -------
    ClientConfig
        Fully configured client for Tripletex integration tests.

    Raises
    ------
    pytest.skip
        If required configuration is missing.
    ConfigurationError
        If configuration is invalid.
    """
    # Create configuration manager
    config_manager = create_tripletex_config_manager()

    # Load configuration from all providers
    config = config_manager.load_config()

    # Create authentication strategy
    auth_strategy = create_tripletex_auth_strategy(config_manager)

    # Get client configuration (defaults provided by config manager)
    hostname = config["hostname"]
    version = config["version"]
    try:
        timeout = float(config["timeout"])
    except (ValueError, TypeError) as e:
        pytest.skip(f"Invalid timeout value in TRIPLETEX_TEST_timeout: {e}")

    # Create client configuration
    return ClientConfig(
        hostname=hostname,
        version=version,
        timeout=timeout,
        auth_strategy=auth_strategy,
    )


def get_tripletex_test_credentials() -> Optional[tuple[str, str]]:
    """
    Get Tripletex test credentials from environment, if available.

    Returns
    -------
    Optional[tuple[str, str]]
        Optional tuple of (consumer_token, employee_token) or None if not available.
    """
    load_dotenv(dotenv_path=".env", override=True)

    consumer_token = os.getenv("TRIPLETEX_TEST_CONSUMER_TOKEN")
    employee_token = os.getenv("TRIPLETEX_TEST_EMPLOYEE_TOKEN")

    if consumer_token and employee_token:
        return (consumer_token, employee_token)
    return None


def skip_if_no_credentials() -> None:
    """Skip test if Tripletex credentials are not available."""
    if not get_tripletex_test_credentials():
        pytest.skip("Tripletex test credentials not available")
