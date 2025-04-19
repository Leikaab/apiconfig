import logging
from typing import Any, Dict, Sequence

from apiconfig.exceptions.config import ConfigLoadError

# Placeholder for a potential future ConfigProvider protocol or base class
ConfigProvider = Any

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages loading configuration from multiple providers."""

    def __init__(self, providers: Sequence[ConfigProvider]) -> None:
        """
        Initializes the ConfigManager with a sequence of configuration providers.

        Args:
            providers: A sequence of configuration provider instances.
                       Providers will be loaded in the order they appear in the sequence,
                       with later providers overriding settings from earlier ones.
        """
        self._providers = providers

    def load_config(self) -> Dict[str, Any]:
        """
        Loads configuration by iterating through all registered providers.

        Configuration values from later providers in the sequence will override
        values from earlier providers.

        Returns:
            A dictionary containing the merged configuration.

        Raises:
            ConfigLoadError: If any provider fails to load its configuration.
        """
        merged_config: Dict[str, Any] = {}
        logger.debug("Loading configuration from %d providers...", len(self._providers))

        for provider in self._providers:
            provider_name = getattr(provider, "__class__", type(provider)).__name__
            try:
                logger.debug("Loading configuration from provider: %s", provider_name)
                # Assuming providers have a 'load' or 'get_config' method
                # Let's standardize on 'load' for now.
                # We might need a Protocol later.
                if hasattr(provider, "load"):
                    config_data = provider.load()
                elif hasattr(
                    provider, "get_config"
                ):  # Fallback for potential variations
                    config_data = provider.get_config()
                else:
                    raise AttributeError(
                        f"Provider {provider_name} lacks a 'load' or 'get_config' method."
                    )

                if config_data:
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
                raise ConfigLoadError(
                    f"Failed to load configuration from provider {provider_name}: {e}"
                ) from e

        logger.info("Configuration loaded successfully from all providers.")
        return merged_config
