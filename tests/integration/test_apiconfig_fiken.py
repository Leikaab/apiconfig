import pytest

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
from apiconfig.exceptions.auth import AuthStrategyError
from apiconfig.exceptions.http import HTTPUtilsError
from apiconfig.types import HttpMethod
from helpers_for_tests.fiken.fiken_client import FikenClient
from helpers_for_tests.fiken.fiken_config import (
    create_fiken_client_config,
    create_fiken_config_manager,
    skip_if_no_credentials,
)


@pytest.fixture
def fiken_config() -> ClientConfig:
    """Create Fiken configuration using improved config management."""
    return create_fiken_client_config()


@pytest.fixture
def fiken_client(fiken_config: ClientConfig) -> FikenClient:
    """Create a configured Fiken client."""
    return FikenClient(fiken_config)


@pytest.fixture
def config_manager() -> ConfigManager:
    """Create a Fiken configuration manager for advanced testing."""
    return create_fiken_config_manager()


class TestFikenIntegration:
    """Integration tests for Fiken API using comprehensive apiconfig patterns."""

    def test_fiken_apiconfig_setup(self, fiken_config: ClientConfig) -> None:
        """
        Integration test: apiconfig config and auth for Fiken.
        Asserts that config is set up correctly using EnvProvider and BearerAuth.
        """
        # Assert base_url is set correctly
        assert fiken_config.base_url is not None
        assert "fiken" in fiken_config.base_url.lower()

        # Auth strategy should be BearerAuth and access_token should be present
        assert fiken_config.auth_strategy is not None
        assert isinstance(fiken_config.auth_strategy, BearerAuth)
        assert fiken_config.auth_strategy.access_token is not None
        assert len(fiken_config.auth_strategy.access_token) > 0

    def test_fiken_api_companies(self, fiken_client: FikenClient) -> None:
        """
        True integration test: Uses apiconfig to load config/auth and makes a real call to Fiken API.
        Skips if no token is set. Asserts on the real API response.
        """
        companies = fiken_client.list_companies()

        # Fiken returns a list of companies, so we expect a list or a dict with a key
        assert isinstance(companies, (list, dict)), f"Unexpected response type: {type(companies)}"
        # If dict, check for expected keys
        if isinstance(companies, dict):
            assert "companies" in companies or "data" in companies or "id" in companies, f"Response dict missing expected keys: {companies.keys()}"
        # If list, check at least one company object
        if isinstance(companies, list):
            assert len(companies) > 0, "No companies returned in response."
            assert isinstance(companies[0], dict), "Company object is not a dict."

    def test_configuration_validation(self) -> None:
        """Test that proper configuration validation occurs."""
        with pytest.raises(AuthStrategyError):
            BearerAuth(access_token="")

    def test_config_manager_layered_providers(self, config_manager: ConfigManager) -> None:
        """Test that ConfigManager properly loads configuration."""
        config = config_manager.load_config()

        hostname = config.get("hostname")
        assert hostname is not None
        assert "fiken" in hostname.lower()

        version = config.get("version")
        assert version is not None

        timeout = config.get("timeout")
        assert timeout is not None
        assert float(timeout) > 0

    def test_error_handling_with_http_utilities(self, fiken_client: FikenClient) -> None:
        """Test that API errors are handled appropriately using HTTP utilities."""
        with pytest.raises(HTTPUtilsError) as exc_info:
            fiken_client._request(HttpMethod.GET, "/nonexistent")

        error_message = str(exc_info.value)
        assert "HTTP request" in error_message or "failed" in error_message.lower()
        assert not isinstance(exc_info.value, ImportError)
        assert not isinstance(exc_info.value, AttributeError)

    def test_client_repr(self, fiken_client: FikenClient) -> None:
        """Test that the client has a useful string representation."""
        repr_str = repr(fiken_client)
        assert "FikenClient" in repr_str
        assert "base_url" in repr_str
        assert "BearerAuth" in repr_str


class TestFikenConfigurationPatterns:
    """Tests specifically for configuration management patterns."""

    def test_skip_if_no_credentials_utility(self) -> None:
        """Test the utility function for skipping tests without credentials."""
        skip_if_no_credentials()

    def test_config_manager_creation(self) -> None:
        """Test that config manager can be created with proper providers."""
        config_manager = create_fiken_config_manager()
        config = config_manager.load_config()
        assert isinstance(config, dict)

        hostname = config.get("hostname")
        assert hostname is not None

        timeout = config.get("timeout")
        assert timeout is not None
