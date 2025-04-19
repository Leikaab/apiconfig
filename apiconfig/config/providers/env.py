import os
from typing import Any, Dict

from apiconfig.exceptions.config import InvalidConfigError


class EnvProvider:
    def __init__(self, prefix: str = "APICONFIG_") -> None:
        self._prefix = prefix

    def load(self) -> Dict[str, Any]:
        config: Dict[str, Any] = {}
        prefix_len = len(self._prefix)

        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                config_key = key[prefix_len:]  # Keep original case after removing prefix
                # Basic type inference (can be expanded later)
                if value.isdigit():
                    try:
                        config[config_key] = int(value)
                    except ValueError:
                        # Should not happen with isdigit, but safety first
                        raise InvalidConfigError(
                            f"Invalid integer value for env var {key}: {value}"
                        )
                elif value.lower() in ("true", "false"):
                    config[config_key] = value.lower() == "true"
                else:
                    try:
                        # Attempt float conversion
                        config[config_key] = float(value)
                    except ValueError:
                        # Keep as string if not clearly int, bool, or float
                        config[config_key] = value
        return config
