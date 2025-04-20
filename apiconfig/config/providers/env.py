import os
from typing import Any, Dict

from apiconfig.exceptions.config import ConfigValueError, InvalidConfigError


class EnvProvider:
    def __init__(self, prefix: str = "APICONFIG_") -> None:
        self._prefix = prefix

    def _is_digit(self, value: str) -> bool:
        """Helper method to check if a string contains only digits."""
        return value.isdigit()

    def load(self) -> Dict[str, Any]:
        config: Dict[str, Any] = {}
        prefix_len = len(self._prefix)

        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                config_key = key[
                    prefix_len:
                ]  # Keep original case after removing prefix
                # Basic type inference (can be expanded later)
                if self._is_digit(value):
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

    def get(self, key: str, default: Any = None, expected_type: type = None) -> Any:
        """Get a configuration value from environment variables.

        Args:
            key: The configuration key to get (without the prefix).
            default: The default value to return if the key is not found.
            expected_type: The expected type of the value. If provided, the value
                will be coerced to this type.

        Returns:
            The configuration value, or the default if not found.

        Raises:
            ConfigValueError: If the value cannot be coerced to the expected type.
        """
        env_key = f"{self._prefix}{key}"
        value = os.environ.get(env_key)

        if value is None:
            return default

        if expected_type is None:
            return value

        try:
            if expected_type is bool:
                # Special handling for boolean values
                if value.lower() in ("true", "1", "yes", "y", "on"):
                    return True
                if value.lower() in ("false", "0", "no", "n", "off"):
                    return False
                raise ValueError(f"Cannot convert '{value}' to bool")

            # Handle other types through standard conversion
            return expected_type(value)
        except (ValueError, TypeError) as e:
            raise ConfigValueError(
                f"Cannot convert environment variable {env_key}='{value}' to {expected_type.__name__}: {str(e)}"
            ) from e
