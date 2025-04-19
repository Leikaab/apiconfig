# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/mocks/config.pyi
"""Type hints and public interfaces for mock configuration components."""

from typing import Any, Dict, Optional, Type
from unittest.mock import MagicMock

from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
# NOTE: No ConfigProvider base class found in current implementation.
# Providers seem to use duck typing (requiring a load() method).


class MockConfigProvider:
    """
    A mock ConfigProvider (duck-typed) designed for testing purposes.

    Mimics the structure of existing providers like EnvProvider, which do not
    inherit from a formal base class but provide a `load()` method.

    This provider bypasses actual configuration sources (like files or environment
    variables) and instead returns a predefined dictionary provided during
    initialization. This allows tests to inject specific configuration scenarios
    easily.

    Args:
        config_data: The dictionary that the `load` method should return.
    """

    def __init__(self, config_data: Dict[str, Any]) -> None: ...

    def load(self) -> Dict[str, Any]:
        """
        Return the predefined configuration dictionary.

        Returns:
            The dictionary passed to the constructor.
        """
        ...


def create_mock_client_config(
    *,
    hostname: str = "mock.example.com",
    api_version: Optional[str] = "v1",
    timeout: int = 30,
    max_retries: int = 3,
    **kwargs: Any,
) -> ClientConfig:
    """
    Factory function to create ClientConfig instances with sensible defaults.

    This simplifies the creation of ClientConfig objects needed for tests,
    allowing specific attributes to be overridden via keyword arguments.

    Args:
        hostname: The mock hostname. Defaults to "mock.example.com".
        api_version: The mock API version. Defaults to "v1".
        timeout: The mock timeout. Defaults to 30.
        max_retries: The mock max retries. Defaults to 3.
        **kwargs: Additional keyword arguments to pass to the ClientConfig constructor,
                  allowing overrides of defaults or setting other attributes.

    Returns:
        A ClientConfig instance populated with the provided or default values.
    """
    ...


class MockConfigManager(ConfigManager):
    """
    A mock ConfigManager for testing configuration loading logic.

    This mock allows tests to either:
    1. Predefine a specific `ClientConfig` instance that `load_config()` will return.
    2. Use `unittest.mock.MagicMock` to spy on calls to `load_config()` and
       assert how it was called, while still returning a default mock config.

    Args:
        mock_config: An optional `ClientConfig` instance to be returned by
                     `load_config()`. If None, `load_config()` will return a
                     default config created by `create_mock_client_config()`.
        providers: An optional list of `ConfigProvider` instances. If None,
                   a list containing a single `MagicMock` provider is used.
        config_class: The configuration class to use. Defaults to `ClientConfig`.
    """
    load_config: MagicMock  # Allow spying on this method

    def __init__(
        self,
        mock_config: Optional[ClientConfig] = None,
        providers: Optional[list[Any]] = None,  # Use Any since no base class
        config_class: Type[ClientConfig] = ClientConfig,
    ) -> None: ...
