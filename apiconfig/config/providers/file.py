"""Provides a configuration provider that loads data from a file."""

import json
import pathlib
from typing import Any, Dict, Optional, Type, TypeVar, Union, cast

from apiconfig.exceptions.config import ConfigLoadError, ConfigValueError

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
        Initialize the FileProvider.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            The path to the configuration file. Can be provided as a string
            or a pathlib.Path object. The path is converted to a Path object internally.
        """
        self._file_path = pathlib.Path(file_path)

    def load(self) -> Dict[str, Any]:
        """
        Load configuration data from the specified file.

        Currently only JSON files (.json extension) are supported. The file must contain
        a valid JSON object (dictionary).

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the configuration key-value pairs.

        Raises
        ------
        ConfigLoadError
            If the file cannot be found, read, or decoded;
            if the file type is unsupported (non-JSON);
            or if the file content is not a JSON object (dictionary).
        """
        import os

        file_path_str = os.path.normpath(str(self._file_path))

        if self._file_path.suffix.lower() != ".json":
            # TODO: Add support for YAML later if needed
            raise ConfigLoadError(f"Unsupported file type: {self._file_path.suffix}. Only .json is currently supported.")

        try:
            try:
                with self._file_path.open("r", encoding="utf-8") as f:
                    config_data = json.load(f)
            except FileNotFoundError as e:
                raise ConfigLoadError(f"Configuration file not found: {file_path_str}") from e
            except json.JSONDecodeError as e:
                raise ConfigLoadError(f"Error decoding JSON in configuration file: {file_path_str}") from e
            except OSError as e:
                raise ConfigLoadError(f"Error reading configuration file: {file_path_str}") from e

            if not isinstance(config_data, dict):
                raise ConfigLoadError(f"Configuration file must contain a JSON object: {file_path_str}")
            config_data = cast(dict[str, Any], config_data)
            return config_data
        except ConfigLoadError:
            # Re-raise our own errors unchanged
            raise
        except Exception as e:
            # Catch-all for any other unexpected errors
            raise ConfigLoadError(f"Error reading configuration file: {file_path_str}") from e

    def get(self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None) -> Any:
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

        Parameters
        ----------
        key : str
            The configuration key to get. Can use dot notation for nested keys (e.g., "api.hostname").
        default : Any, optional
            The default value to return if the key is not found.
        expected_type : Optional[Type[T]], optional
            The expected type of the value. If provided, the value will be coerced to this type.

        Returns
        -------
        Any
            The configuration value (coerced to expected_type if specified), or the default if the key is not found.

        Raises
        ------
        ConfigValueError
            If the value cannot be coerced to the expected type.
        ConfigLoadError
            If there's an error loading the configuration file.
        """
        config: Dict[str, Any] = self.load()

        # Handle dot notation for nested keys
        parts = key.split(".")
        value: Any = config

        # Navigate through nested dictionaries
        for part in parts:
            if not isinstance(value, dict) or part not in value:
                return default
            value = cast(Dict[str, Any], value)[part]

        if expected_type is None or isinstance(value, expected_type):
            return value

        try:
            # Handle other types through standard conversion
            if expected_type is object or not callable(expected_type):
                return value
                # mypy: unreachable
            if expected_type is bool:
                # Special handling for boolean values
                try:
                    lower: str = cast(str, value).lower()
                    val_lower: str = lower
                    if val_lower in ("true", "1", "yes", "y", "on"):
                        return True
                    elif val_lower in ("false", "0", "no", "n", "off"):
                        return False
                    else:
                        raise ValueError(f"Cannot convert '{value}' to bool")
                except AttributeError:
                    return bool(value)
            return expected_type(value)  # type: ignore[call-arg]
        except (ValueError, TypeError) as e:
            raise ConfigValueError(f"Cannot convert configuration value for '{key}' ({value}) to {expected_type.__name__}: {str(e)}") from e
