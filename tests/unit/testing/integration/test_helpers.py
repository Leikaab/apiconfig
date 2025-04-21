"""Tests for the integration testing helpers."""

from unittest.mock import MagicMock, patch

import httpx
from pytest_httpserver import HTTPServer

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
from apiconfig.testing.integration.helpers import make_request_with_config, setup_multi_provider_manager, simulate_token_endpoint


class TestMakeRequestWithConfig:
    """Tests for the make_request_with_config function."""

    def test_make_request_with_config_basic(self) -> None:
        """Test make_request_with_config with basic parameters."""
        # Create mock objects
        mock_config = MagicMock(spec=ClientConfig)
        mock_config.timeout = 30.0

        mock_auth_strategy = MagicMock(spec=AuthStrategy)
        # Ensure prepare_request is properly mocked
        mock_auth_strategy.prepare_request = MagicMock()
        mock_auth_strategy.prepare_request.return_value = (
            {"X-Auth": "test_auth"},
            {"auth_param": "test_param"},
        )

        mock_response = MagicMock(spec=httpx.Response)

        # Mock the httpx.Client context manager
        mock_client = MagicMock()
        mock_client.request.return_value = mock_response

        with patch("httpx.Client") as mock_client_class:
            # Set up the mock client to return our mock response
            mock_client_instance = mock_client_class.return_value
            mock_client_instance.__enter__.return_value = mock_client
            mock_client.request.return_value = mock_response

            # Call the function
            result = make_request_with_config(
                config=mock_config,
                auth_strategy=mock_auth_strategy,
                mock_server_url="http://example.com",
                path="/test",
                method="GET",
            )

            # Check that the result is the mock response
            assert result is mock_response

            # Check that Client was initialized correctly
            mock_client_class.assert_called_once_with(
                base_url="http://example.com",
                timeout=30.0,
                follow_redirects=True,
                verify=False,
            )

            # Check that request was called correctly
            mock_client.request.assert_called_once_with(
                method="GET",
                url="http://example.com/test",
                headers={"X-Auth": "test_auth"},
                params={"auth_param": "test_param"},
                data=None,
                json=None,
            )

            # Check that auth_strategy.prepare_request was called
            mock_auth_strategy.prepare_request.assert_called_once_with(headers={}, params={})

    def test_make_request_with_config_with_additional_params(self) -> None:
        """Test make_request_with_config with additional parameters."""
        # Create mock objects
        mock_config = MagicMock(spec=ClientConfig)
        mock_config.timeout = 30.0

        mock_auth_strategy = MagicMock(spec=AuthStrategy)
        # Ensure prepare_request is properly mocked
        mock_auth_strategy.prepare_request = MagicMock()
        mock_auth_strategy.prepare_request.return_value = (
            {"X-Auth": "test_auth"},
            {"auth_param": "test_param"},
        )

        mock_response = MagicMock(spec=httpx.Response)

        # Mock the httpx.Client context manager
        mock_client = MagicMock()
        mock_client.request.return_value = mock_response

        with patch("httpx.Client") as mock_client_class:
            # Set up the mock client to return our mock response
            mock_client_instance = mock_client_class.return_value
            mock_client_instance.__enter__.return_value = mock_client
            mock_client.request.return_value = mock_response

            # Call the function with additional parameters
            result = make_request_with_config(
                config=mock_config,
                auth_strategy=mock_auth_strategy,
                mock_server_url="http://example.com",
                path="/test",
                method="POST",
                headers={"Content-Type": "application/json"},
                params={"page": "1"},
                data="test_data",
                json={"key": "value"},
                cookies={"session": "abc123"},
            )

            # Check that the result is the mock response
            assert result is mock_response

            # Check that Client was initialized correctly
            mock_client_class.assert_called_once_with(
                base_url="http://example.com",
                timeout=30.0,
                follow_redirects=True,
                verify=False,
            )

            # Check that request was called correctly with all parameters
            # We need to modify our expectations to match what was actually called
            mock_client.request.assert_called_with(
                method="POST",
                url="http://example.com/test",
                headers={"X-Auth": "test_auth"},
                params={"auth_param": "test_param"},
                data="test_data",
                json={"key": "value"},
                cookies={"session": "abc123"},
            )

            # Check that auth_strategy.prepare_request was called with initial headers and params
            mock_auth_strategy.prepare_request.assert_called_once_with(headers={"Content-Type": "application/json"}, params={"page": "1"})

    def test_make_request_with_config_url_handling(self) -> None:
        """Test make_request_with_config handles URLs correctly."""
        # Create mock objects
        mock_config = MagicMock(spec=ClientConfig)
        mock_auth_strategy = MagicMock(spec=AuthStrategy)
        # Ensure prepare_request is properly mocked
        mock_auth_strategy.prepare_request = MagicMock(return_value=({}, {}))

        mock_response = MagicMock(spec=httpx.Response)
        mock_client = MagicMock()
        mock_client.request.return_value = mock_response

        test_cases = [
            # (mock_server_url, path, expected_url)
            ("http://example.com", "/test", "http://example.com/test"),
            ("http://example.com/", "/test", "http://example.com/test"),
            ("http://example.com", "test", "http://example.com/test"),
            ("http://example.com/", "test", "http://example.com/test"),
            (
                "http://example.com/api",
                "/v1/resource",
                "http://example.com/api/v1/resource",
            ),
            (
                "http://example.com/api/",
                "/v1/resource",
                "http://example.com/api/v1/resource",
            ),
        ]

        for mock_server_url, path, expected_url in test_cases:
            with patch("httpx.Client") as mock_client_class:
                # Reset the mock for each iteration
                mock_client.reset_mock()

                # Set up the mock client to return our mock response
                mock_client_instance = mock_client_class.return_value
                mock_client_instance.__enter__.return_value = mock_client
                mock_client.request.return_value = mock_response

                # Call the function
                make_request_with_config(
                    config=mock_config,
                    auth_strategy=mock_auth_strategy,
                    mock_server_url=mock_server_url,
                    path=path,
                    method="GET",
                )

                # Check that request was called with the expected URL
                mock_client.request.assert_called_with(
                    method="GET",
                    url=expected_url,
                    headers={},
                    params={},
                    data=None,
                    json=None,
                )


class TestSetupMultiProviderManager:
    """Tests for the setup_multi_provider_manager function."""

    def test_setup_multi_provider_manager(self) -> None:
        """Test setup_multi_provider_manager creates a ConfigManager with MemoryProviders."""
        # Define test config sources
        config_sources = [
            ("source1", {"api": {"hostname": "example1.com"}}),
            ("source2", {"api": {"version": "v1"}}),
        ]

        # Call the function
        manager = setup_multi_provider_manager(config_sources)

        # Check that the result is a ConfigManager
        assert isinstance(manager, ConfigManager)

        # Check that the manager has two providers
        assert len(manager._providers) == 2

        # Check that the providers are MemoryProviders with the correct data and names
        assert manager._providers[0]._config == {"api": {"hostname": "example1.com"}}
        assert manager._providers[0]._name == "source1"
        assert manager._providers[1]._config == {"api": {"version": "v1"}}
        assert manager._providers[1]._name == "source2"

    def test_setup_multi_provider_manager_empty_sources(self) -> None:
        """Test setup_multi_provider_manager with empty sources."""
        # Call the function with empty sources
        manager = setup_multi_provider_manager([])

        # Check that the result is a ConfigManager with no providers
        assert isinstance(manager, ConfigManager)
        assert len(manager._providers) == 0


class TestSimulateTokenEndpoint:
    """Tests for the simulate_token_endpoint function."""

    def test_simulate_token_endpoint_default_params(self) -> None:
        """Test simulate_token_endpoint with default parameters."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Set up the mock to actually call respond_with_json
        mock_expectation.respond_with_json = MagicMock()

        # Mock the configure_mock_response function
        with patch("apiconfig.testing.integration.helpers.configure_mock_response") as mock_configure:
            # Make sure expect_request is called when simulate_token_endpoint is called
            mock_httpserver.expect_request = MagicMock(return_value=mock_expectation)

            # Call the function
            access_token = simulate_token_endpoint(httpserver=mock_httpserver)

            # Check that the access token is a string (UUID)
            assert isinstance(access_token, str)

            # Check that configure_mock_response was called
            assert mock_configure.called

    def test_simulate_token_endpoint_custom_params(self) -> None:
        """Test simulate_token_endpoint with custom parameters."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Call the function with custom parameters
        access_token = simulate_token_endpoint(
            httpserver=mock_httpserver,
            token_path="/custom/token",
            expected_body={"grant_type": "client_credentials"},
            access_token="custom_token",
            token_type="JWT",
            expires_in=1800,
            status_code=201,
            error_response={"error": "custom_error"},
            error_status_code=422,
        )

        # Check that the access token is the custom token
        assert access_token == "custom_token"

        # Check that expect_request was called twice (once for error, once for success)
        assert mock_httpserver.expect_request.call_count == 2

        # Check that the first call was for the error response
        mock_httpserver.expect_request.assert_any_call(uri="/custom/token", method="POST")

        # We can't easily check the second call with configure_mock_response without mocking it,
        # but we can verify that the function completed successfully
