"""Manages loading configuration from multiple providers."""

import logging
from typing import Any, Dict, Mapping, Protocol, Sequence, runtime_checkable

from apiconfig.exceptions.config import ConfigLoadError


@runtime_checkable
class _SupportsLoad(Protocol):
    """Protocol for providers implementing ``load``."""

    def load(self) -> Mapping[str, Any]: ...


@runtime_checkable
class _SupportsGetConfig(Protocol):
    """Protocol for providers implementing ``get_config``."""

    def get_config(self) -> Mapping[str, Any]: ...


ConfigProvider = _SupportsLoad | _SupportsGetConfig

logger: logging.Logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages loading configuration from multiple providers.

    This class orchestrates the process of gathering configuration settings
    from various sources (like environment variables, files, or in-memory dictionaries)
    and merging them into a single configuration dictionary.

    The ConfigManager follows a predictable merging strategy:
    1. Providers are processed in the order they were registered
    2. Each provider's configuration is merged into the result
    3. When keys conflict, later providers override earlier ones
    4. Providers must return dictionary-like objects or they will be skipped
    5. If a provider raises an exception, the entire loading process fails

    Providers must implement either a `load()` or `get_config()` method that
    returns a dictionary of configuration values.
    """

    def __init__(self, providers: Sequence[ConfigProvider]) -> None:
        """
        Initialize the ConfigManager with a sequence of configuration providers.

        Args
        ----
        providers: A sequence of configuration provider instances.
            Providers will be loaded in the order they appear in the sequence,
            with later providers overriding settings from earlier ones.
            Each provider must implement either a `load()` or `get_config()` method.
        """
        # Store providers as ``Any`` internally to avoid overly strict typing
        # that would leak into consumer code (e.g. tests accessing attributes
        # specific to concrete providers).
        self._providers: Sequence[Any] = list(providers)

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration by iterating through all registered providers.

        The method attempts to load configuration from each provider in sequence.
        For each provider, it:
        1. Attempts to call either `load()` or `get_config()` method
        2. Validates that the returned value is a dictionary
        3. Merges the dictionary into the accumulated configuration

        Configuration values from later providers in the sequence will override
        values from earlier providers when keys conflict. This allows for a layered
        configuration approach where default values can be overridden by more specific sources.

        Returns
        -------
        A dictionary containing the merged configuration from all providers.
            If no providers are registered or none return data, an empty dictionary is returned.

        Raises
        ------
        ConfigLoadError: If any provider fails to load its configuration or
            if a provider lacks both `load()` and `get_config()` methods.
        """
        merged_config: Dict[str, Any] = {}
        logger.debug("Loading configuration from %d providers...", len(self._providers))

        for provider in self._providers:
            provider_name = provider.__class__.__name__
            try:
                logger.debug("Loading configuration from provider: %s", provider_name)
                if isinstance(provider, _SupportsLoad):
                    config_data: Mapping[str, Any] = provider.load()
                elif isinstance(provider, _SupportsGetConfig):
                    config_data = provider.get_config()
                else:
                    raise AttributeError(f"Provider {provider_name} lacks a 'load' or 'get_config' method.")

                if config_data:
                    if not isinstance(config_data, dict):
                        logger.warning(
                            "Provider %s returned non-dict value: %r. Skipping.",
                            provider_name,
                            config_data,
                        )
                    else:
                        merged_config.update(config_data)
                        logger.debug("Merged config from %s", provider_name)
                else:
                    logger.debug("Provider %s returned no data.", provider_name)

            except Exception as e:
                logger.error(
                    "Failed to load configuration from provider %s: %s",
                    provider_name,
                    e,
                    exc_info=True,
                )
                # Wrap the original exception for context
                raise ConfigLoadError(f"Failed to load configuration from provider {provider_name}: {e}") from e

        logger.info("Configuration loaded successfully from all providers.")
        return merged_config
