import logging
from typing import Any, Dict, Sequence

from apiconfig.exceptions.config import ConfigLoadError

# Placeholder for a potential future ConfigProvider protocol or base class
ConfigProvider = Any

logger: logging.Logger


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

    _providers: Sequence[ConfigProvider]

    def __init__(self, providers: Sequence[ConfigProvider]) -> None:
        """
        Initializes the ConfigManager with a sequence of configuration providers.

        Args:
            providers: A sequence of configuration provider instances.
                       Providers will be loaded in the order they appear in the sequence,
                       with later providers overriding settings from earlier ones.
                       Each provider must implement either a `load()` or `get_config()` method.
        """
        ...

    def load_config(self) -> Dict[str, Any]:
        """
        Loads configuration by iterating through all registered providers.

        The method attempts to load configuration from each provider in sequence.
        For each provider, it:
        1. Attempts to call either `load()` or `get_config()` method
        2. Validates that the returned value is a dictionary
        3. Merges the dictionary into the accumulated configuration

        Configuration values from later providers in the sequence will override
        values from earlier providers when keys conflict. This allows for a layered
        configuration approach where default values can be overridden by more specific sources.

        Returns:
            A dictionary containing the merged configuration from all providers.
            If no providers are registered or none return data, an empty dictionary is returned.

        Raises:
            ConfigLoadError: If any provider fails to load its configuration or
                             if a provider lacks both `load()` and `get_config()` methods.
        """
        ...
