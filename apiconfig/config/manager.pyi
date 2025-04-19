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
    """

    _providers: Sequence[ConfigProvider]

    def __init__(self, providers: Sequence[ConfigProvider]) -> None:
        """
        Initializes the ConfigManager with a sequence of configuration providers.

        Args:
            providers: A sequence of configuration provider instances.
                       Providers will be loaded in the order they appear in the sequence,
                       with later providers overriding settings from earlier ones.
        """
        ...

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
        ...
