"""Integration tests for apiconfig with Tripletex API.

This test demonstrates comprehensive usage of apiconfig patterns:
- Configuration management with ConfigManager and multiple providers
- Custom authentication strategies (TripletexSessionAuth)
- HTTP utilities for safe JSON handling and status checking
- URL utilities for proper parameter handling
- Modern HTTP client integration with proper error handling
"""

import pytest

from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
from apiconfig.exceptions.auth import MissingCredentialsError
from apiconfig.exceptions.http import HTTPUtilsError
from apiconfig.types import HttpMethod
from helpers_for_tests.tripletex.tripletex_auth import TripletexSessionAuth
from helpers_for_tests.tripletex.tripletex_client import TripletexClient
from helpers_for_tests.tripletex.tripletex_config import (
    create_tripletex_client_config,
    create_tripletex_config_manager,
    skip_if_no_credentials,
)


@pytest.fixture
def tripletex_config() -> ClientConfig:
    """Create Tripletex configuration using improved config management."""
    return create_tripletex_client_config()


@pytest.fixture
def tripletex_client(tripletex_config: ClientConfig) -> TripletexClient:
    """Create a configured Tripletex client.

    Args:
        tripletex_config: Client configuration from tripletex_config fixture.

    Returns:
        TripletexClient: Configured client instance using improved patterns.
    """
    return TripletexClient(tripletex_config)


@pytest.fixture
def config_manager() -> ConfigManager:
    """Create a Tripletex configuration manager for advanced testing."""
    return create_tripletex_config_manager()


class TestTripletexIntegration:
    """Integration tests for Tripletex API using comprehensive apiconfig patterns."""

    def test_session_token_creation(self, tripletex_client: TripletexClient) -> None:
        """Test that session token can be created successfully.

        This test verifies that the TripletexSessionAuth strategy
        can successfully authenticate and obtain a session token.
        """
        # Access the auth strategy to trigger token creation
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        # Verify that session token was created
        session_token = auth_strategy.get_session_token()
        assert session_token is not None
        assert isinstance(session_token, str)
        assert len(session_token) > 0

    def test_list_countries(self, tripletex_client: TripletexClient) -> None:
        """Test listing countries using improved HTTP utilities.

        This test demonstrates enhanced apiconfig workflow:
        1. Configuration loading via ConfigManager with multiple providers
        2. Authentication via TripletexSessionAuth
        3. HTTP requests with safe JSON handling
        4. URL construction with parameter utilities
        """
        # List countries using the improved client
        countries = tripletex_client.list_countries()

        # Verify response structure
        assert isinstance(countries, dict)
        assert "values" in countries
        assert isinstance(countries["values"], list)

        # Verify we got some countries
        country_list = countries["values"]
        assert len(country_list) > 0

        # Verify country structure
        first_country = country_list[0]
        assert isinstance(first_country, dict)
        assert "id" in first_country
        assert "displayName" in first_country
        assert "isoAlpha2Code" in first_country

        # Verify specific expected countries exist
        country_codes = {country["isoAlpha2Code"] for country in country_list}
        expected_codes = {"NO", "SE", "DK", "US", "DE"}
        assert expected_codes.issubset(country_codes), f"Expected country codes {expected_codes} not found in {country_codes}"

    def test_list_countries_with_parameters(self, tripletex_client: TripletexClient) -> None:
        """Test listing countries with query parameters using URL utilities."""
        # Test with query parameters to demonstrate URL utility usage
        params = {"count": "10", "from": "0"}
        countries = tripletex_client.list_countries(params=params)

        # Verify response structure
        assert isinstance(countries, dict)
        assert "values" in countries
        assert isinstance(countries["values"], list)

    def test_get_session_info(self, tripletex_client: TripletexClient) -> None:
        """Test getting session information to verify authentication works."""
        # This tests the new method that wasn't in the original client
        session_info = tripletex_client.get_session_info()

        assert isinstance(session_info, dict)
        # The response structure may vary, but we should get some data
        assert "value" in session_info or "values" in session_info or len(session_info) > 0

    def test_list_currencies(self, tripletex_client: TripletexClient) -> None:
        """Test listing currencies using the improved client."""
        currencies = tripletex_client.list_currencies()

        assert isinstance(currencies, dict)
        assert "values" in currencies
        assert isinstance(currencies["values"], list)

        if currencies["values"]:  # If we get currencies
            first_currency = currencies["values"][0]
            assert isinstance(first_currency, dict)
            assert "id" in first_currency

    def test_configuration_validation(self) -> None:
        """Test that proper configuration validation occurs.

        This test verifies that the apiconfig components properly
        validate configuration and raise appropriate errors.
        """
        # Test missing credentials - should fail during auth strategy creation
        with pytest.raises(MissingCredentialsError):
            TripletexSessionAuth(consumer_token="", employee_token="", company_id="0", session_token_hostname="https://api.tripletex.io")

    def test_config_manager_layered_providers(self, config_manager: ConfigManager) -> None:
        """Test that ConfigManager properly loads configuration."""
        # Load configuration from all providers
        config = config_manager.load_config()

        # Test that we can access configuration values (from env or defaults)
        hostname = config.get("hostname")
        assert hostname is not None
        assert "tripletex" in hostname.lower()

        # Test that version is available
        version = config.get("version")
        assert version is not None

        # Test timeout configuration
        timeout = config.get("timeout")
        assert timeout is not None
        assert float(timeout) > 0

    def test_error_handling_with_http_utilities(self, tripletex_client: TripletexClient) -> None:
        """Test that API errors are handled appropriately using HTTP utilities.

        This test verifies that the client properly handles
        HTTP errors using apiconfig's HTTP utilities and converts
        them to appropriate exceptions.
        """
        # Test with invalid endpoint to trigger error handling
        with pytest.raises(HTTPUtilsError) as exc_info:
            tripletex_client._request(HttpMethod.GET, "/nonexistent")

        # Verify we get proper apiconfig HTTP exceptions
        error_message = str(exc_info.value)
        assert "HTTP request" in error_message or "failed" in error_message.lower()

        # Verify it's not a raw HTTP library error
        assert not isinstance(exc_info.value, ImportError)
        assert not isinstance(exc_info.value, AttributeError)

    def test_client_repr(self, tripletex_client: TripletexClient) -> None:
        """Test that the client has a useful string representation."""
        repr_str = repr(tripletex_client)
        assert "TripletexClient" in repr_str
        assert "base_url" in repr_str
        assert "TripletexSessionAuth" in repr_str


class TestTripletexConfigurationPatterns:
    """Tests specifically for configuration management patterns."""

    def test_skip_if_no_credentials_utility(self) -> None:
        """Test the utility function for skipping tests without credentials."""
        # This should either skip or pass, depending on whether credentials are available
        skip_if_no_credentials()
        # If we get here, credentials are available

    def test_config_manager_creation(self) -> None:
        """Test that config manager can be created with proper providers."""
        config_manager = create_tripletex_config_manager()

        # Verify that we can load configuration
        config = config_manager.load_config()
        assert isinstance(config, dict)

        # Verify that we can get configuration values (from env or defaults)
        hostname = config.get("hostname")
        assert hostname is not None

        timeout = config.get("timeout")
        assert timeout is not None


def test_tripletex_auth_and_list_countries(tripletex_config: ClientConfig, tripletex_client: TripletexClient) -> None:
    """
    Legacy test name preserved for backward compatibility.

    Tests getting a session token and listing countries using improved apiconfig patterns.
    """
    # This test maintains the original test name for backward compatibility
    # but now uses the improved implementation

    # Test session token creation
    auth_strategy = tripletex_client.config.auth_strategy
    assert isinstance(auth_strategy, TripletexSessionAuth)

    session_token = auth_strategy.get_session_token()
    assert session_token is not None
    assert isinstance(session_token, str)
    assert len(session_token) > 0

    # Test listing countries with improved HTTP handling
    countries = tripletex_client.list_countries()
    assert isinstance(countries, dict)
    assert "values" in countries
    assert isinstance(countries["values"], list)
    assert len(countries["values"]) > 0

    # Basic check of country data structure
    first_country = countries["values"][0]
    assert isinstance(first_country, dict)
    assert "id" in first_country
    assert "displayName" in first_country
    assert "isoAlpha2Code" in first_country
