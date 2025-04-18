import json
import pathlib
from typing import Any, Dict, Union

from apiconfig.exceptions.config import ConfigLoadError


class FileProvider:
    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        self._file_path = pathlib.Path(file_path)

    def load(self) -> Dict[str, Any]:
        if self._file_path.suffix.lower() != ".json":
            # TODO: Add support for YAML later if needed
            raise ConfigLoadError(
                f"Unsupported file type: {self._file_path.suffix}. "
                "Only .json is currently supported."
            )

        try:
            with self._file_path.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
            if not isinstance(config_data, dict):
                raise ConfigLoadError(
                    f"Configuration file '{self._file_path}' must contain a JSON object (dict)."
                )
            return config_data
        except FileNotFoundError as e:
            raise ConfigLoadError(f"Configuration file not found: {self._file_path}") from e
        except json.JSONDecodeError as e:
            raise ConfigLoadError(
                f"Error decoding JSON from configuration file: {self._file_path}"
            ) from e
        except OSError as e:
            raise ConfigLoadError(
                f"Error reading configuration file: {self._file_path}"
            ) from e
