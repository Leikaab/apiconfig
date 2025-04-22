"""A configuration provider that stores data in memory."""

from typing import Any, Mapping, MutableMapping


class MemoryProvider:
    """A simple configuration provider that stores configuration in memory."""

    _config: MutableMapping[str, Any]

    def __init__(self, config_data: Mapping[str, Any] | None = None) -> None:
        """
        Initialize the MemoryProvider.

        Parameters
        ----------
        config_data : Mapping[str, Any] | None, optional
            An optional dictionary containing the initial configuration data.
            If None, an empty dictionary is used.
        """
        self._config = dict(config_data) if config_data is not None else {}

    def get_config(self) -> Mapping[str, Any]:
        """
        Return the configuration data stored in memory.

        Returns
        -------
        Mapping[str, Any]
            A dictionary representing the configuration.
        """
        return self._config

    # Potential future methods:
    # def set(self, key: str, value: Any) -> None:
    #     self._config[key] = value
    #
    # def update(self, data: Mapping[str, Any]) -> None:
    #     self._config.update(data)
