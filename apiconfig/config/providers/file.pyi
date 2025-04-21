import pathlib
from typing import Any, Dict, Optional, Type, TypeVar, Union

T = TypeVar("T")


class FileProvider:
    """
    Loads configuration data from a file.

    Currently supports JSON files. The configuration file must contain a valid JSON object (dictionary).
    YAML support may be added in the future.

    The provider handles file path resolution, loading, and parsing of the configuration file.
    It also provides type coercion capabilities when retrieving values.
    """

    _file_path: pathlib.Path

    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        """
        Initializes the FileProvider.

        Args:
            file_path: The path to the configuration file. Can be provided as a string
                       or a pathlib.Path object. The path is converted to a Path object
                       internally.
        """
        ...

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration data from the specified file.

        Currently only JSON files (.json extension) are supported. The file must contain
        a valid JSON object (dictionary).

        Returns:
            A dictionary containing the configuration key-value pairs.

        Raises:
            ConfigLoadError: If the file cannot be found, read, or decoded;
                             if the file type is unsupported (non-JSON);
                             or if the file content is not a JSON object (dictionary).
        """
        ...

    def get(
        self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None
    ) -> Any:
        """
        Get a configuration value from the loaded configuration.

        This method supports dot notation for accessing nested keys in the configuration.
        For example, "api.hostname" will access the "hostname" key within the "api" object.

        If the key is not found, the default value is returned.

        Type coercion is performed when expected_type is provided:
        - For boolean values (expected_type=bool), string values like "true", "yes", "1", "on"
          are converted to True, and "false", "no", "0", "off" are converted to False
          (case-insensitive).
        - For other types, standard Python type conversion is attempted (e.g., int("42")).

        Args:
            key: The configuration key to get. Can use dot notation for nested keys
                 (e.g., "api.hostname").
            default: The default value to return if the key is not found.
            expected_type: The expected type of the value. If provided, the value
                will be coerced to this type.

        Returns:
            The configuration value (coerced to expected_type if specified),
            or the default if the key is not found.

        Raises:
            ConfigValueError: If the value cannot be coerced to the expected type.
            ConfigLoadError: If there's an error loading the configuration file.
        """
        ...
