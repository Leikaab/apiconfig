"""Unit tests for apiconfig.testing.unit.factories."""

from typing import Any, Dict

import pytest

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.testing.unit.factories import (
    create_auth_credentials,
    create_invalid_client_config,
    create_provider_dict,
    create_valid_client_config,
)


class DummyAuthStrategy(AuthStrategy):
    """Dummy AuthStrategy for testing."""

    def authenticate(self, request: Any) -> Any:
        return request

    def prepare_request_headers(self) -> Dict[str, str]:
        """Return empty headers for testing."""
        return {}

    def prepare_request_params(self) -> Dict[str, str]:
        """Return empty params for testing."""
        return {}


def test_create_valid_client_config_defaults() -> None:
    """
    Test create_valid_client_config with default parameters.
    """
    config = create_valid_client_config()
    assert isinstance(config, ClientConfig)
    assert config.hostname == "https://api.example.com"
    assert config.version == "v1"
    assert config.timeout == 30.0
    assert config.retries == 3
    assert config.headers == {}
    assert config.auth_strategy is None
    assert config.log_request_body is False


@pytest.mark.parametrize(
    "key,value,expected",
    [
        ("hostname", "https://override.com", "https://override.com"),
        ("version", "v2", "v2"),
        ("timeout", 45, 45.0),
        ("timeout", 12.5, 12.5),
        ("timeout", "99", 99.0),
        ("retries", 7, 7),
        ("retries", 2.0, 2),
        ("retries", "5", 5),
        ("headers", {"X-Test": "1"}, {"X-Test": "1"}),
        ("auth_strategy", DummyAuthStrategy(), DummyAuthStrategy),
        ("log_request_body", True, True),
        ("log_request_body", False, False),
        ("log_response_body", True, True),
        ("log_response_body", False, False),
    ],
)
def test_create_valid_client_config_overrides(key: str, value: Any, expected: Any) -> None:
    """
    Test create_valid_client_config with various valid overrides.
    """
    kwargs = {key: value}
    config = create_valid_client_config(**kwargs)
    if key == "auth_strategy":
        assert isinstance(config.auth_strategy, DummyAuthStrategy)
    elif key == "headers":
        assert config.headers == expected
    elif key == "log_request_body":
        assert config.log_request_body == expected
    elif key == "log_response_body":
        assert config.log_response_body == expected
    else:
        assert getattr(config, key) == expected


def test_create_valid_client_config_invalid_keys_ignored() -> None:
    """
    Test that invalid override keys are ignored in create_valid_client_config.
    """
    config = create_valid_client_config(foo="bar", hostname="h", version="v")
    assert not hasattr(config, "foo")
    assert config.hostname == "h"
    assert config.version == "v"


def test_create_valid_client_config_headers_non_dict() -> None:
    """
    Test that non-dict headers are ignored and set to None.
    """
    config = create_valid_client_config(headers="notadict")
    assert config.headers == {}


def test_create_valid_client_config_auth_strategy_invalid_type() -> None:
    """
    Test that non-AuthStrategy, non-None auth_strategy is set to None.
    """
    config = create_valid_client_config(auth_strategy="notastrategy")
    assert config.auth_strategy is None


def test_create_valid_client_config_log_flags_non_bool() -> None:
    """
    Test that log_request_body and log_response_body handle non-bool values.
    """
    config = create_valid_client_config(log_request_body="yes", log_response_body=1)
    assert config.log_request_body is True
    assert config.log_response_body is True
    config2 = create_valid_client_config(log_request_body=None, log_response_body=None)
    assert config2.log_request_body is False


@pytest.mark.parametrize(
    "reason,expected_mod",
    [
        ("missing_hostname", lambda d: "hostname" not in d),
        ("invalid_timeout", lambda d: d.get("timeout") == -10),
        ("unknown_reason", lambda d: "hostname" in d and d.get("timeout") == 30),
    ],
)
def test_create_invalid_client_config_reasons(reason: str, expected_mod: Any) -> None:
    """
    Test create_invalid_client_config for different reasons.
    """
    data = create_invalid_client_config(reason)
    assert isinstance(data, dict)
    assert expected_mod(data)


def test_create_invalid_client_config_overrides_applied() -> None:
    """
    Test that overrides are applied in create_invalid_client_config.
    """
    data = create_invalid_client_config("missing_hostname", foo="bar", timeout=123)
    assert data["foo"] == "bar"
    assert data["timeout"] == 123
    assert "hostname" not in data


@pytest.mark.parametrize(
    "auth_type,expected",
    [
        ("basic", {"username": "testuser", "password": "testpassword"}),
        ("bearer", {"token": "testbearertoken"}),
        ("api_key", {"api_key": "testapikey", "header_name": "X-API-Key"}),
        ("unknown", {}),
        ("", {}),
    ],
)
def test_create_auth_credentials(auth_type: str, expected: Dict[str, Any]) -> None:
    """
    Test create_auth_credentials for all defined and undefined types.
    """
    creds = create_auth_credentials(auth_type)
    assert creds == expected


@pytest.mark.parametrize(
    "source,expected_keys",
    [
        ("env", {"APICONFIG_HOSTNAME", "APICONFIG_TIMEOUT"}),
        ("file", {"hostname", "max_retries", "auth"}),
        ("memory", {"hostname", "api_version", "user_agent"}),
        ("unknown", set()),
        ("", set()),
    ],
)
def test_create_provider_dict(source: str, expected_keys: set[str]) -> None:
    """
    Test create_provider_dict for all defined and undefined sources.
    """
    provider = create_provider_dict(source)
    assert set(provider.keys()) == expected_keys
