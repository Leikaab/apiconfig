import pathlib
from typing import Any, Dict, Union, Optional, Type, TypeVar

T = TypeVar("T")


class FileProvider:
    """
    Loads configuration data from a file.

    Currently supports JSON files.
    """

    _file_path: pathlib.Path

    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        """
        Initializes the FileProvider.

        Args:
            file_path: The path to the configuration file (string or Path object).
        """
        ...

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration data from the specified file.

        Returns:
            A dictionary containing the configuration key-value pairs.

        Raises:
            ConfigLoadError: If the file cannot be found, read, decoded,
                             or if the file type is unsupported.
        """
        ...

    def get(self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None) -> Any:
        """
        Get a configuration value from the loaded configuration.

        Args:
            key: The configuration key to get. Can use dot notation for nested keys.
            default: The default value to return if the key is not found.
            expected_type: The expected type of the value. If provided, the value
                will be coerced to this type.

        Returns:
            The configuration value, or the default if not found.

        Raises:
            ConfigValueError: If the value cannot be coerced to the expected type.
            ConfigLoadError: If there's an error loading the configuration file.
        """
        ...
