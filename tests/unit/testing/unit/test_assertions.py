"""
Unit tests for apiconfig.testing.unit.assertions.

Covers all assertion helpers: assert_client_config_valid, assert_auth_header_correct, assert_provider_loads.
Ensures both success and failure (AssertionError) paths are tested for 100% coverage.
"""

from typing import Any, Dict

import pytest

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.exceptions.config import InvalidConfigError
from apiconfig.testing.unit import assertions


def test_type_checking_imports() -> None:
    """Test that TYPE_CHECKING imports are accessible."""
    # This test ensures the TYPE_CHECKING block is covered
    # by importing the module and checking that the types are available
    import apiconfig.testing.unit.assertions

    # The TYPE_CHECKING imports should be available for type hints
    # We can't directly test them since they're only available during type checking,
    # but we can ensure the module loads correctly
    assert hasattr(apiconfig.testing.unit.assertions, "assert_client_config_valid")
    assert hasattr(apiconfig.testing.unit.assertions, "assert_auth_header_correct")
    assert hasattr(apiconfig.testing.unit.assertions, "assert_provider_loads")


# --- Mocks for ClientConfig ---


class MockClientConfigValid(ClientConfig):
    """A valid mock ClientConfig."""

    hostname: str | None = "api.example.com"
    timeout: int | None = 10
    retries: int | None = 2

    @property
    def base_url(self) -> str:
        return f"https://{self.hostname}/"


class MockClientConfigNoHostname(MockClientConfigValid):
    hostname = ""


class MockClientConfigBaseUrlRaises(MockClientConfigValid):
    @property
    def base_url(self) -> str:
        raise ValueError("base_url error")


# --- Mocks for AuthStrategy ---


class MockAuthStrategyValid(AuthStrategy):
    """A valid mock AuthStrategy."""

    def prepare_request_headers(self) -> Dict[str, str]:
        return {"Authorization": "Bearer token123"}

    def prepare_request_params(self) -> Dict[str, str]:
        return {}


class MockAuthStrategyWrongHeaders(MockAuthStrategyValid):
    def prepare_request_headers(self) -> Dict[str, str]:
        return {"Authorization": "WRONG"}


# --- Mocks for ConfigProvider ---


class MockProviderValid:
    """A valid mock ConfigProvider."""

    def load(self) -> Dict[str, Any]:
        return {"key": "value"}


class MockProviderWrongDict(MockProviderValid):
    def load(self) -> Dict[str, Any]:
        return {"key": "wrong"}


class MockProviderNoLoad:
    pass


class MockProviderLoadNotCallable:
    load = "not a function"


# --- Tests for assert_client_config_valid ---


def test_assert_client_config_valid_success() -> None:
    """
    Test assert_client_config_valid passes for a valid ClientConfig.
    """
    config = MockClientConfigValid()
    assertions.assert_client_config_valid(config)


def test_assert_client_config_valid_wrong_type() -> None:
    """
    Test assert_client_config_valid fails if not a ClientConfig.
    """
    with pytest.raises(AttributeError):
        assertions.assert_client_config_valid(object())  # type: ignore[arg-type]


def test_assert_client_config_valid_empty_hostname() -> None:
    """
    Test assert_client_config_valid fails if hostname is empty.
    """
    config = MockClientConfigNoHostname()
    with pytest.raises(AssertionError, match="hostname cannot be empty"):
        assertions.assert_client_config_valid(config)


def test_assert_client_config_valid_negative_timeout() -> None:
    """
    Test assert_client_config_valid fails if timeout is negative.
    (Instantiation fails with InvalidConfigError, so assertion is never called.)
    """
    with pytest.raises(InvalidConfigError, match="Timeout must be non-negative"):
        MockClientConfigValid(timeout=-1)


def test_assert_client_config_valid_negative_retries() -> None:
    """
    Test assert_client_config_valid fails if retries is negative.
    (Instantiation fails with InvalidConfigError, so assertion is never called.)
    """
    with pytest.raises(InvalidConfigError, match="Retries must be non-negative"):
        MockClientConfigValid(retries=-1)


def test_assert_client_config_valid_base_url_raises() -> None:
    """
    Test assert_client_config_valid fails if base_url property raises.
    """
    config = MockClientConfigBaseUrlRaises()
    with pytest.raises(AssertionError, match="failed base_url construction"):
        assertions.assert_client_config_valid(config)


# --- Tests for assert_auth_header_correct ---


def test_assert_auth_header_correct_success() -> None:
    """
    Test assert_auth_header_correct passes for correct AuthStrategy and headers.
    """
    strategy = MockAuthStrategyValid()
    assertions.assert_auth_header_correct(strategy, {"Authorization": "Bearer token123"})


def test_assert_auth_header_correct_wrong_type() -> None:
    """
    Test assert_auth_header_correct fails if not an AuthStrategy.
    """
    with pytest.raises(AttributeError):
        assertions.assert_auth_header_correct(
            object(),  # type: ignore[arg-type]
            {"Authorization": "Bearer token123"},
        )


def test_assert_auth_header_correct_wrong_headers() -> None:
    """
    Test assert_auth_header_correct fails if headers do not match.
    """
    strategy = MockAuthStrategyWrongHeaders()
    with pytest.raises(AssertionError, match="Auth header mismatch"):
        assertions.assert_auth_header_correct(strategy, {"Authorization": "Bearer token123"})


# --- Tests for assert_provider_loads ---


def test_assert_provider_loads_success() -> None:
    """
    Test assert_provider_loads passes for correct provider and dict.
    """
    provider = MockProviderValid()
    assertions.assert_provider_loads(provider, {"key": "value"})


def test_assert_provider_loads_no_load() -> None:
    """
    Test assert_provider_loads fails if provider has no load method.
    """
    provider = MockProviderNoLoad()
    with pytest.raises(AssertionError, match="does not have a callable 'load' method"):
        assertions.assert_provider_loads(provider, {"key": "value"})


def test_assert_provider_loads_load_not_callable() -> None:
    """
    Test assert_provider_loads fails if load is not callable.
    """
    provider = MockProviderLoadNotCallable()
    with pytest.raises(AssertionError, match="does not have a callable 'load' method"):
        assertions.assert_provider_loads(provider, {"key": "value"})


def test_assert_provider_loads_wrong_dict() -> None:
    """
    Test assert_provider_loads fails if loaded dict does not match.
    """
    provider = MockProviderWrongDict()
    with pytest.raises(AssertionError, match="Provider load mismatch"):
        assertions.assert_provider_loads(provider, {"key": "value"})
