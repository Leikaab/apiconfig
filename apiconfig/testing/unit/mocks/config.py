# -*- coding: utf-8 -*-
# File: apiconfig/testing/unit/mocks/config.py
"""Mock implementations for configuration components."""

from typing import Any, Dict, Optional
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

    Parameters
    ----------
    config_data : Dict[str, Any]
        The dictionary that the `load` method should return.
    """

    def __init__(self, config_data: Dict[str, Any]) -> None:
        self._config_data = config_data

    def load(self) -> Dict[str, Any]:
        """
        Return the predefined configuration dictionary.

        Returns
        -------
        Dict[str, Any]
            The dictionary passed to the constructor.
        """
        return self._config_data


def create_mock_client_config(
    *,
    hostname: str = "mock.example.com",
    version: Optional[str] = "v1",
    timeout: int = 30,
    retries: int = 3,
    **kwargs: Any,
) -> ClientConfig:
    """Create ClientConfig instances with sensible defaults.

    This simplifies the creation of ClientConfig objects needed for tests,
    allowing specific attributes to be overridden via keyword arguments.

    Parameters
    ----------
    hostname : str, optional
        The mock hostname. Defaults to "mock.example.com".
    version : Optional[str], optional
        The mock API version. Defaults to "v1".
    timeout : int, optional
        The mock timeout. Defaults to 30.
    retries : int, optional
        The mock max retries. Defaults to 3.
    **kwargs : Any
        Additional keyword arguments to pass to the ClientConfig constructor,
        allowing overrides of defaults or setting other attributes.

    Returns
    -------
    ClientConfig
        A ClientConfig instance populated with the provided or default values.
    """
    config_data = {
        "hostname": hostname,
        "version": version,
        "timeout": timeout,
        "retries": retries,
        **kwargs,
    }
    return ClientConfig(**config_data)


class MockConfigManager(ConfigManager):
    """
    A mock ConfigManager for testing configuration loading logic.

    This mock allows tests to either:
    1. Predefine a specific `ClientConfig` instance that `load_config()` will return.
    2. Use `unittest.mock.MagicMock` to spy on calls to `load_config()` and
       assert how it was called, while still returning a default mock config.

    Parameters
    ----------
    mock_config : Optional[ClientConfig], optional
        An optional `ClientConfig` instance to be returned by
        `load_config()`. If None, `load_config()` will return a
        default config created by `create_mock_client_config()`.
    providers : Optional[list[Any]], optional
        An optional list of `ConfigProvider` instances. If None,
        a list containing a single `MagicMock` provider is used.
    """

    load_config: MagicMock  # Allow spying on this method

    def __init__(
        self,
        mock_config: Optional[ClientConfig] = None,
        providers: Optional[list[Any]] = None,  # Use Any since no base class
    ) -> None:
        """
        Initialize the MockConfigManager.

        Parameters
        ----------
        mock_config : Optional[ClientConfig], optional
            An optional `ClientConfig` instance to be returned by
            `load_config()`. If None, `load_config()` will return a
            default config created by `create_mock_client_config()`.
        providers : Optional[list[Any]], optional
            An optional list of `ConfigProvider` instances. If None,
            a list containing a single `MagicMock` provider is used.
        """
        # Initialize with MagicMock providers if none are given
        # Use a generic MagicMock since there's no specific provider base class
        if providers is None:
            # Create a mock object that has a load method for duck typing
            mock_provider = MagicMock()
            mock_provider.load.return_value = {}
            providers = [mock_provider]
        super().__init__(providers=providers)

        # Allow predefining the config to be returned by load_config
        self._mock_config = mock_config
        # Use MagicMock for load_config to allow spying/assertions
        # Don't use spec to allow arbitrary arguments for testing
        self.load_config = MagicMock()

        if mock_config:
            self.load_config.return_value = mock_config
        else:
            # If no specific mock config, return a default one
            self.load_config.return_value = create_mock_client_config()
