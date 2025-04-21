# -*- coding: utf-8 -*-
"""Factory functions for creating test data."""

from typing import Any, Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig


def create_valid_client_config(**overrides: Any) -> ClientConfig:
    """Create a valid ClientConfig instance with default values.

    Parameters
    ----------
    **overrides : Any
        Keyword arguments to override default configuration values.

    Returns
    -------
    ClientConfig
        A valid ClientConfig instance.
    """
    defaults = {
        "hostname": "https://api.example.com",
        "version": "v1",
        "timeout": 30.0,
        "retries": 3,
        # "headers": {},  # Optionally add headers if needed
        # "auth_strategy": None,  # Optionally add auth_strategy if needed
        # "log_request_body": False,
        # "log_response_body": False,
    }
    # Only keep keys that are valid for ClientConfig
    valid_keys = {
        "hostname",
        "version",
        "headers",
        "timeout",
        "retries",
        "auth_strategy",
        "log_request_body",
        "log_response_body",
    }
    # Merge overrides, but only allow valid keys
    for k, v in overrides.items():
        if k in valid_keys:
            defaults[k] = v
    # Explicitly pass each argument to ClientConfig with correct type
    hostname: str = str(defaults.get("hostname", "https://api.example.com"))
    version: str = str(defaults.get("version", "v1"))
    timeout_val = defaults.get("timeout", 30.0)
    timeout: float = float(timeout_val) if isinstance(timeout_val, (int, float, str)) else 30.0
    retries_val = defaults.get("retries", 3)
    retries: int = int(retries_val) if isinstance(retries_val, (int, float, str)) else 3
    headers_val = defaults.get("headers")
    headers: Optional[Dict[str, str]] = dict(headers_val) if isinstance(headers_val, dict) else None
    auth_strategy_val = defaults.get("auth_strategy")
    auth_strategy: Optional[AuthStrategy] = auth_strategy_val if isinstance(auth_strategy_val, AuthStrategy) or auth_strategy_val is None else None
    log_request_body_val = defaults.get("log_request_body")
    log_request_body: Optional[bool] = bool(log_request_body_val) if log_request_body_val is not None else None
    log_response_body_val = defaults.get("log_response_body")
    log_response_body: Optional[bool] = bool(log_response_body_val) if log_response_body_val is not None else None

    return ClientConfig(
        hostname=hostname,
        version=version,
        timeout=timeout,
        retries=retries,
        headers=headers,
        auth_strategy=auth_strategy,
        log_request_body=log_request_body,
        log_response_body=log_response_body,
    )


def create_invalid_client_config(reason: str, **overrides: Any) -> Dict[str, Any]:
    """Create a dictionary representing potentially invalid ClientConfig data.

    This returns a dictionary because ClientConfig validation might prevent
    instantiation with invalid data directly. The consuming test should
    handle the expected validation error.

    Parameters
    ----------
    reason : str
        A string indicating the reason for invalidity (e.g., "missing_hostname").
        Used to generate specific invalid configurations.
    **overrides : Any
        Keyword arguments to override default or invalid values.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing potentially invalid configuration data.
    """
    # This function returns a dict because ClientConfig validation
    # might prevent instantiation with invalid data.
    # The 'reason' parameter is currently unused but kept for potential future use
    # in generating specific invalid configurations.
    config_data = {
        "hostname": "https://api.example.com",
        "api_version": "v1",
        "timeout": 30,
        "max_retries": 3,
        "user_agent": "TestClient/1.0",
    }
    config_data.update(overrides)
    # Example invalid modification based on a hypothetical reason
    if reason == "missing_hostname":
        del config_data["hostname"]
    elif reason == "invalid_timeout":
        config_data["timeout"] = -10
    # Add more specific invalid cases as needed
    return config_data


def create_auth_credentials(auth_type: str) -> Dict[str, Any]:
    """Generate a dictionary of sample authentication credentials.

    Parameters
    ----------
    auth_type : str
        The type of authentication (e.g., "basic", "bearer", "api_key").

    Returns
    -------
    Dict[str, Any]
        A dictionary containing sample credentials for the specified type.
    """
    if auth_type == "basic":
        return {"username": "testuser", "password": "testpassword"}
    elif auth_type == "bearer":
        return {"token": "testbearertoken"}
    elif auth_type == "api_key":
        return {"api_key": "testapikey", "header_name": "X-API-Key"}
    # Add more auth types as needed
    return {}


def create_provider_dict(source: str) -> Dict[str, Any]:
    """Generate a sample configuration dictionary for a specific provider type.

    Parameters
    ----------
    source : str
        The type of configuration source (e.g., "env", "file", "memory").

    Returns
    -------
    Dict[str, Any]
        A dictionary containing sample configuration data for the specified source.
    """
    if source == "env":
        # Example structure for env provider (keys might be prefixed)
        return {
            "APICONFIG_HOSTNAME": "env.example.com",
            "APICONFIG_TIMEOUT": "60",
        }
    elif source == "file":
        # Example structure for file provider
        return {
            "hostname": "file.example.com",
            "max_retries": 5,
            "auth": {"type": "basic", "username": "fileuser"},
        }
    elif source == "memory":
        # Example structure for memory provider
        return {
            "hostname": "memory.example.com",
            "api_version": "v2",
            "user_agent": "MemoryClient/2.0",
        }
    # Add more source types as needed
    return {}
