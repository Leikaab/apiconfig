"""Provides a configuration provider that loads values from environment variables."""

import os
from typing import Any, Dict, Optional, Type, TypeVar

from apiconfig.exceptions.config import ConfigValueError, InvalidConfigError

T = TypeVar("T")


class EnvProvider:
    """
    Loads configuration values from environment variables.

    Looks for environment variables starting with a specific prefix (defaulting
    to "APICONFIG_"), strips the prefix, preserves the original case of the key,
    and attempts basic type inference:
    - Strings containing only digits are converted to integers
    - "true" and "false" (case-insensitive) are converted to boolean values
    - Strings that can be parsed as floats are converted to float values
    - All other values remain as strings

    Type coercion is also available through the `get` method with the `expected_type`
    parameter, which supports special handling for boolean values.
    """

    _prefix: str

    def __init__(self, prefix: str = "APICONFIG_") -> None:
        """Initialize the provider with a specific prefix.

        Parameters
        ----------
        prefix : str, optional
            The prefix to look for in environment variable names. Defaults to "APICONFIG_".
        """
        self._prefix = prefix

    def _is_digit(self, value: str) -> bool:
        """Check if a string contains only digits.

        Parameters
        ----------
        value : str
            The string to check.

        Returns
        -------
        bool
            True if the string contains only digits, False otherwise.
        """
        return value.isdigit()

    def load(self) -> Dict[str, Any]:
        """Load configuration from environment variables matching the prefix.

        Performs automatic type inference for common data types:
        - Strings containing only digits are converted to integers
        - "true" and "false" (case-insensitive) are converted to boolean values
        - Strings that can be parsed as floats are converted to float values
        - All other values remain as strings

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the loaded configuration key-value pairs.
            Keys maintain their original case after the prefix is removed.

        Raises
        ------
        InvalidConfigError
            If a value identified as an integer (via isdigit()) cannot be parsed as an integer.
        """
        config: Dict[str, Any] = {}
        prefix_len = len(self._prefix)

        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                config_key = key[prefix_len:]  # Keep original case after removing prefix
                # Basic type inference (can be expanded later)
                if self._is_digit(value):
                    try:
                        config[config_key] = int(value)
                    except ValueError:
                        # Should not happen with isdigit, but safety first
                        raise InvalidConfigError(f"Invalid integer value for env var {key}: {value}")
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

    def get(self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None) -> Any:
        """Get a configuration value from environment variables.

        Parameters
        ----------
        key : str
            The configuration key to get (without the prefix).
        default : Any, optional
            The default value to return if the key is not found.
        expected_type : Optional[Type[T]], optional
            The expected type of the value. If provided, the value will be coerced to this type.

        Returns
        -------
        Any
            The configuration value, or the default if not found.
            If expected_type is provided, the value will be coerced to that type.

        Raises
        ------
        ConfigValueError
            If the value cannot be coerced to the expected type.

        Notes
        -----
        For boolean conversion, the following string values are recognized:
        - True: "true", "1", "yes", "y", "on" (case-insensitive)
        - False: "false", "0", "no", "n", "off" (case-insensitive)
        Any other string will raise a ConfigValueError when converting to bool.
        """
        env_key = f"{self._prefix}{key}"
        value = os.environ.get(env_key)

        if value is None:
            return default

        if expected_type is None:
            return value

        try:
            # Handle other types through standard conversion
            if expected_type is object or not callable(expected_type):
                return value
                # mypy: unreachable
            if expected_type is bool:
                # Special handling for boolean values
                try:
                    val_lower = value.lower()
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
            raise ConfigValueError(f"Cannot convert environment variable {env_key}='{value}' to {expected_type.__name__}: {str(e)}") from e
