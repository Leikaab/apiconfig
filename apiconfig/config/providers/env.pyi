from typing import Any, Dict, Optional, Type, TypeVar

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
        """
        Initializes the provider with a specific prefix.

        Args:
            prefix: The prefix to look for in environment variable names.
                   Defaults to "APICONFIG_".
        """
        ...

    def _is_digit(self, value: str) -> bool:
        """Helper method to check if a string contains only digits."""
        ...

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration from environment variables matching the prefix.

        Performs automatic type inference for common data types:
        - Strings containing only digits are converted to integers
        - "true" and "false" (case-insensitive) are converted to boolean values
        - Strings that can be parsed as floats are converted to float values
        - All other values remain as strings

        Returns:
            A dictionary containing the loaded configuration key-value pairs.
            Keys maintain their original case after the prefix is removed.

        Raises:
            InvalidConfigError: If a value identified as an integer (via isdigit())
                               cannot be parsed as an integer.
        """
        ...

    def get(self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None) -> Any:
        """
        Get a configuration value from environment variables.

        Args:
            key: The configuration key to get (without the prefix).
            default: The default value to return if the key is not found.
            expected_type: The expected type of the value. If provided, the value
                will be coerced to this type.

        Returns:
            The configuration value, or the default if not found.
            If expected_type is provided, the value will be coerced to that type.

        Raises:
            ConfigValueError: If the value cannot be coerced to the expected type.

        Notes:
            For boolean conversion, the following string values are recognized:
            - True: "true", "1", "yes", "y", "on" (case-insensitive)
            - False: "false", "0", "no", "n", "off" (case-insensitive)
            Any other string will raise a ConfigValueError when converting to bool.
        """
        ...
