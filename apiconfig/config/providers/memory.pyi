from typing import Any, Mapping

class MemoryProvider:
    """
    A simple configuration provider that stores configuration in memory.
    """

    def __init__(self, config_data: Mapping[str, Any] | None = None) -> None:
        """
        Initializes the MemoryProvider.

        Args:
            config_data: An optional dictionary containing the initial
                         configuration data. If None, an empty dictionary
                         is used.
        """
        ...

    def get_config(self) -> Mapping[str, Any]:
        """
        Returns the configuration data stored in memory.

        Returns:
            A dictionary representing the configuration.
        """
        ...
