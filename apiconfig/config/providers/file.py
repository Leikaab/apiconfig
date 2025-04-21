import json
import pathlib
from typing import Any, Dict, Optional, Type, TypeVar, Union

from apiconfig.exceptions.config import ConfigLoadError, ConfigValueError

T = TypeVar("T")


class FileProvider:
    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        self._file_path = pathlib.Path(file_path)

    def load(self) -> Dict[str, Any]:
        if self._file_path.suffix.lower() != ".json":
            # TODO: Add support for YAML later if needed
            raise ConfigLoadError(f"Unsupported file type: {self._file_path.suffix}. " "Only .json is currently supported.")

        try:
            with self._file_path.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
            if not isinstance(config_data, dict):
                raise ConfigLoadError(f"Configuration file '{self._file_path}' must contain a JSON object (dict).")
            return config_data
        except FileNotFoundError as e:
            raise ConfigLoadError(f"Configuration file not found: {self._file_path}") from e
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Error decoding JSON from configuration file: {self._file_path}") from e
        except OSError as e:
            raise ConfigLoadError(f"Error reading configuration file: {self._file_path}") from e

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
