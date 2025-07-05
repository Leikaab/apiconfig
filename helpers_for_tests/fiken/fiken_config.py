"""Configuration management for Fiken integration tests using apiconfig patterns."""

import os
from typing import Optional

import pytest
from dotenv import load_dotenv as dotenv_load

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager, ConfigProvider
from apiconfig.config.providers.env import EnvProvider
from apiconfig.config.providers.memory import MemoryProvider
from apiconfig.exceptions.auth import MissingCredentialsError


def create_fiken_config_manager() -> ConfigManager:
    """
    Create a ConfigManager for Fiken configuration from environment variables with sensible defaults.

    Returns
    -------
    ConfigManager
        Configured manager for loading Fiken settings.
    """
    dotenv_load(dotenv_path=".env", override=True)

    defaults = {
        "hostname": "https://api.fiken.no/api",
        "version": "v2",
        "timeout": "10.0",
    }

    providers: list[ConfigProvider] = [
        EnvProvider(prefix="FIKEN_"),
        MemoryProvider(config_data=defaults),
    ]

    return ConfigManager(providers=providers)


def create_fiken_auth_strategy(config_manager: ConfigManager) -> BearerAuth:
    """
    Create a BearerAuth strategy for Fiken using configuration from the manager.

    Args
    ----
    config_manager : ConfigManager
        ConfigManager instance to load auth settings from.

    Returns
    -------
    BearerAuth
        Configured authentication strategy.

    Raises
    ------
    pytest.skip
        If required credentials are missing.
    """
    config = config_manager.load_config()

    token = config.get("ACCESS_TOKEN")
    if not token:
        raise MissingCredentialsError("FIKEN_ACCESS_TOKEN cannot be empty.")

    return BearerAuth(access_token=token)


def create_fiken_client_config() -> ClientConfig:
    """
    Create a complete ClientConfig for Fiken using apiconfig patterns.

    Returns
    -------
    ClientConfig
        Fully configured client for Fiken integration tests.

    Raises
    ------
    pytest.skip
        If required configuration is missing.
    """
    config_manager = create_fiken_config_manager()
    config = config_manager.load_config()

    auth_strategy = create_fiken_auth_strategy(config_manager)

    hostname = config["hostname"]
    version = config["version"]
    try:
        timeout = float(config["timeout"])
    except (ValueError, TypeError) as e:
        pytest.skip(f"Invalid timeout value in FIKEN_timeout: {e}")

    return ClientConfig(
        hostname=hostname,
        version=version,
        timeout=timeout,
        auth_strategy=auth_strategy,
    )


def get_fiken_test_credentials() -> Optional[str]:
    """
    Get Fiken test credentials (access token) from environment, if available.

    Returns
    -------
    Optional[str]
        Optional access token string or None if not available.
    """
    dotenv_load(dotenv_path=".env", override=True)
    return os.getenv("FIKEN_ACCESS_TOKEN")


def skip_if_no_credentials() -> None:
    """Skip test if Fiken credentials are not available."""
    if not get_fiken_test_credentials():
        pytest.skip("Fiken test credentials not available (FIKEN_ACCESS_TOKEN not set)")
