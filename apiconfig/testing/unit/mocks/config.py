# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/mocks/config.py
"""Mock implementations for configuration components."""

from typing import Any, Dict, Optional, Type
from unittest.mock import MagicMock

from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager

# NOTE: No ConfigProvider base class found in current implementation.
# Providers seem to use duck typing (requiring a load() method).


class MockConfigProvider:
    """
    A mock ConfigProvider (duck-typed) that returns a predefined dictionary.

    Mimics the structure of existing providers like EnvProvider, which do not
    inherit from a formal base class but provide a `load()` method.
    """

    def __init__(self, config_data: Dict[str, Any]) -> None:
        self._config_data = config_data

    def load(self) -> Dict[str, Any]:
        """Return the predefined configuration dictionary."""
        return self._config_data


def create_mock_client_config(
    *,
    hostname: str = "mock.example.com",
    api_version: Optional[str] = "v1",
    timeout: int = 30,
    max_retries: int = 3,
    **kwargs: Any,
) -> ClientConfig:
    """Factory function to create ClientConfig instances with defaults."""
    config_data = {
        "hostname": hostname,
        "api_version": api_version,
        "timeout": timeout,
        "max_retries": max_retries,
        **kwargs,
    }
    return ClientConfig(**config_data)


class MockConfigManager(ConfigManager):
    """A mock ConfigManager."""

    def __init__(
        self,
        mock_config: Optional[ClientConfig] = None,
        providers: Optional[list[Any]] = None,  # Use Any since no base class
        config_class: Type[ClientConfig] = ClientConfig,
    ) -> None:
        # Initialize with MagicMock providers if none are given
        # Use a generic MagicMock since there's no specific provider base class
        if providers is None:
            # Create a mock object that has a load method for duck typing
            mock_provider = MagicMock()
            mock_provider.load.return_value = {}
            providers = [mock_provider]
        super().__init__(providers=providers, config_class=config_class)  # type: ignore[arg-type] # Manager expects Provider objs

        # Allow predefining the config to be returned by load_config
        self._mock_config = mock_config
        # Use MagicMock for load_config to allow spying/assertions
        self.load_config = MagicMock(spec=self.load_config)  # type: ignore[method-assign]

        if mock_config:
            self.load_config.return_value = mock_config
        else:
            # If no specific mock config, return a default one
            self.load_config.return_value = create_mock_client_config()
