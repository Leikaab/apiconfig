from typing import Any, Dict

from apiconfig.config.base import ClientConfig


def create_valid_client_config(**overrides: Any) -> ClientConfig:
    defaults = {
        "hostname": "https://api.example.com",
        "api_version": "v1",
        "timeout": 30,
        "max_retries": 3,
        "user_agent": "TestClient/1.0",
    }
    defaults.update(overrides)
    return ClientConfig(**defaults)


def create_invalid_client_config(reason: str, **overrides: Any) -> Dict[str, Any]:
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
    if auth_type == "basic":
        return {"username": "testuser", "password": "testpassword"}
    elif auth_type == "bearer":
        return {"token": "testbearertoken"}
    elif auth_type == "api_key":
        return {"api_key": "testapikey", "header_name": "X-API-Key"}
    # Add more auth types as needed
    return {}


def create_provider_dict(source: str) -> Dict[str, Any]:
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
