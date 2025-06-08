"""Configuration management for OneFlow integration tests using apiconfig patterns."""

import os
from typing import Optional

import pytest
from dotenv import load_dotenv

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager, ConfigProvider
from apiconfig.config.providers.env import EnvProvider
from apiconfig.config.providers.memory import MemoryProvider
from apiconfig.exceptions.auth import MissingCredentialsError


def create_oneflow_config_manager() -> ConfigManager:
    """
    Create a ConfigManager for OneFlow configuration from environment variables with sensible defaults.

    Returns
    -------
    ConfigManager
        Configured manager for loading OneFlow settings.
    """
    load_dotenv(dotenv_path=".env", override=True)

    defaults = {
        "hostname": "https://api.test.oneflow.com",
        "version": "v1",
        "timeout": "10.0",
    }

    providers: list[ConfigProvider] = [
        EnvProvider(prefix="ONEFLOW_"),
        MemoryProvider(config_data=defaults),
    ]

    return ConfigManager(providers=providers)


def create_oneflow_auth_strategy(config_manager: ConfigManager) -> ApiKeyAuth:
    """
    Create an ApiKeyAuth strategy for OneFlow using configuration from the manager.

    Args
    ----
    config_manager : ConfigManager
        ConfigManager instance to load auth settings from.

    Returns
    -------
    ApiKeyAuth
        Configured authentication strategy.

    Raises
    ------
    pytest.skip
        If required credentials are missing.
    """
    config = config_manager.load_config()

    api_key = config.get("API_KEY")
    if not api_key:
        raise MissingCredentialsError("ONEFLOW_API_KEY cannot be empty.")

    return ApiKeyAuth(api_key, header_name="x-oneflow-api-token")


def create_oneflow_client_config() -> ClientConfig:
    """
    Create a complete ClientConfig for OneFlow using apiconfig patterns.

    Returns
    -------
    ClientConfig
        Fully configured client for OneFlow integration tests.

    Raises
    ------
    pytest.skip
        If required configuration is missing.
    """
    config_manager = create_oneflow_config_manager()
    config = config_manager.load_config()

    auth_strategy = create_oneflow_auth_strategy(config_manager)

    hostname = config["hostname"]
    version = config["version"]
    try:
        timeout = float(config["timeout"])
    except (ValueError, TypeError) as e:
        pytest.skip(f"Invalid timeout value in ONEFLOW_timeout: {e}")

    # Handle user email header if provided
    headers = {}
    user_email = config.get("USER_EMAIL")
    if user_email:
        headers["x-oneflow-user-email"] = user_email

    return ClientConfig(
        hostname=hostname,
        version=version,
        timeout=timeout,
        auth_strategy=auth_strategy,
        headers=headers if headers else None,
    )


def get_oneflow_test_credentials() -> tuple[Optional[str], Optional[str]]:
    """
    Get OneFlow test credentials (API key and user email) from environment, if available.

    Returns
    -------
    tuple[Optional[str], Optional[str]]
        Tuple of (api_key, user_email) or (None, None) if not available.
    """
    load_dotenv(dotenv_path=".env", override=True)
    api_key = os.getenv("ONEFLOW_API_KEY")
    user_email = os.getenv("ONEFLOW_USER_EMAIL")
    return api_key, user_email


def skip_if_no_credentials() -> None:
    """Skip test if OneFlow credentials are not available."""
    api_key, user_email = get_oneflow_test_credentials()
    if not api_key:
        pytest.skip("OneFlow test credentials not available (ONEFLOW_API_KEY not set)")
    if not user_email:
        pytest.skip("OneFlow test credentials not available (ONEFLOW_USER_EMAIL not set)")
