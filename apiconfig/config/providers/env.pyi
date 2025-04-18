from typing import Any, Dict


class EnvProvider:
    """
    Loads configuration values from environment variables.

    Looks for environment variables starting with a specific prefix (defaulting
    to "APICONFIG_"), strips the prefix, converts the remaining key to lowercase,
    and attempts basic type inference (int, bool, float, str).
    """

    def __init__(self, prefix: str = "APICONFIG_") -> None:
        """
        Initializes the provider with a specific prefix.

        Args:
            prefix: The prefix to look for in environment variable names.
        """
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
