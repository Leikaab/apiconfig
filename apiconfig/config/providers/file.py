import json
import pathlib
from typing import Any, Dict, Optional, Type, TypeVar, Union

from apiconfig.exceptions.config import ConfigLoadError, ConfigValueError

T = TypeVar("T")


class FileProvider:
    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        self._file_path = pathlib.Path(file_path)

    def load(self) -> Dict[str, Any]:
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
            return config_data
        except ConfigLoadError:
            # Re-raise our own errors unchanged
            raise
        except Exception as e:
            # Catch-all for any other unexpected errors
            raise ConfigLoadError(f"Error reading configuration file: {file_path_str}") from e

    def get(self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None) -> Any:
        config = self.load()

        # Handle dot notation for nested keys
        parts = key.split(".")
        value = config

        # Navigate through nested dictionaries
        for part in parts:
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]

        if expected_type is None or isinstance(value, expected_type):
            return value

        try:
            if expected_type is bool:
                # Special handling for boolean values
                if isinstance(value, str):
                    if value.lower() in ("true", "1", "yes", "y", "on"):
                        return True
                    if value.lower() in ("false", "0", "no", "n", "off"):
                        return False
                    raise ValueError(f"Cannot convert '{value}' to bool")
                return bool(value)

            # Handle other types through standard conversion
            return expected_type(value)
        except (ValueError, TypeError) as e:
            raise ConfigValueError(f"Cannot convert configuration value for '{key}' ({value}) to {expected_type.__name__}: {str(e)}") from e
