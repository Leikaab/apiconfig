from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar("T")

class EnvProvider:
    """
    Loads configuration values from environment variables.

    Looks for environment variables starting with a specific prefix (defaulting
    to "APICONFIG_"), strips the prefix, converts the remaining key to lowercase,
    and attempts basic type inference (int, bool, float, str).
    """

    _prefix: str

    def __init__(self, prefix: str = "APICONFIG_") -> None:
        """
        Initializes the provider with a specific prefix.

        Args:
            prefix: The prefix to look for in environment variable names.
        """
        ...

    def _is_digit(self, value: str) -> bool:
        """Helper method to check if a string contains only digits."""
        ...

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration from environment variables matching the prefix.

        Returns:
            A dictionary containing the loaded configuration key-value pairs.

        Raises:
            InvalidConfigError: If a value intended as an integer cannot be parsed.
        """
        ...

    def get(
        self, key: str, default: Any = None, expected_type: Optional[Type[T]] = None
    ) -> Any:
        """
        Get a configuration value from environment variables.

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
        ...
