from typing import Any, Dict

from apiconfig.config.base import ClientConfig


def create_valid_client_config(**overrides: Any) -> ClientConfig:
    """
    Creates a valid ClientConfig instance with default values.

    Args:
        **overrides: Keyword arguments to override default configuration values.

    Returns:
        A valid ClientConfig instance.
    """
    ...


def create_invalid_client_config(reason: str, **overrides: Any) -> Dict[str, Any]:
    """
    Creates a dictionary representing potentially invalid ClientConfig data.

    This returns a dictionary because ClientConfig validation might prevent
    instantiation with invalid data directly. The consuming test should
    handle the expected validation error.

    Args:
        reason: A string indicating the reason for invalidity (e.g., "missing_hostname").
                Used to generate specific invalid configurations.
        **overrides: Keyword arguments to override default or invalid values.

    Returns:
        A dictionary containing potentially invalid configuration data.
    """
    ...


def create_auth_credentials(auth_type: str) -> Dict[str, Any]:
    """
    Generates a dictionary of sample authentication credentials.

    Args:
        auth_type: The type of authentication (e.g., "basic", "bearer", "api_key").

    Returns:
        A dictionary containing sample credentials for the specified type.
    """
    ...


def create_provider_dict(source: str) -> Dict[str, Any]:
    """
    Generates a sample configuration dictionary for a specific provider type.

    Args:
        source: The type of configuration source (e.g., "env", "file", "memory").

    Returns:
        A dictionary containing sample configuration data for the specified source.
    """
    ...
