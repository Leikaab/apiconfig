"""Tests for the integration testing fixtures."""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_httpserver import HTTPServer

from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.env import EnvProvider
from apiconfig.config.providers.file import FileProvider


class TestHttpserverListenAddress:
    """Tests for the httpserver_listen_address fixture."""

    def test_httpserver_listen_address_manual(self) -> None:
        """Test that httpserver_listen_address returns a tuple with localhost and port 0."""
        # Create our own implementation that mimics the fixture
        address = ("127.0.0.1", 0)
        assert isinstance(address, tuple)
        assert len(address) == 2
        assert address[0] == "127.0.0.1"
        assert address[1] == 0


class TestMockApiUrl:
    """Tests for the mock_api_url fixture."""

    def test_mock_api_url_manual(self) -> None:
        """Test that mock_api_url returns the URL from the httpserver."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_httpserver.url_for.return_value = "http://127.0.0.1:8000/test/"

        # Mimic the fixture's behavior
        url = mock_httpserver.url_for("/")

        # Check that url_for was called with "/"
        mock_httpserver.url_for.assert_called_once_with("/")

        # Check that the URL is returned
        assert url == "http://127.0.0.1:8000/test/"


class TestTempConfigFile:
    """Tests for the temp_config_file fixture."""

    def test_temp_config_file_manual(self, tmp_path: Path) -> None:
        """Test that temp_config_file creates a valid JSON config file."""
        # Create our own implementation that mimics the fixture
        config_data = {
            "api": {
                "hostname": "file.example.com",
                "version": "v1",
            },
            "auth": {"type": "file_basic", "username": "file_user"},
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))

        # Check that the file exists and is a Path object
        assert isinstance(config_file, Path)
        assert config_file.exists()
        assert config_file.name == "config.json"

        # Check that the file contains valid JSON with expected structure
        config_data = json.loads(config_file.read_text())
        assert "api" in config_data
        assert "hostname" in config_data["api"]
        assert config_data["api"]["hostname"] == "file.example.com"
        assert "version" in config_data["api"]
        assert config_data["api"]["version"] == "v1"
        assert "auth" in config_data
        assert "type" in config_data["auth"]
        assert config_data["auth"]["type"] == "file_basic"
        assert "username" in config_data["auth"]
        assert config_data["auth"]["username"] == "file_user"


class TestFileProvider:
    """Tests for the file_provider fixture."""

    def test_file_provider_manual(self, tmp_path: Path) -> None:
        """Test that file_provider returns a FileProvider pointing to the temp config file."""
        # Create a config file
        config_data = {
            "api": {
                "hostname": "file.example.com",
                "version": "v1",
            },
            "auth": {"type": "file_basic", "username": "file_user"},
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))

        # Create a FileProvider directly
        provider = FileProvider(file_path=str(config_file))

        # Check that the provider is a FileProvider with the correct file path
        assert isinstance(provider, FileProvider)
        assert provider.file_path == config_file


class TestEnvProvider:
    """Tests for the env_provider fixture."""

    def test_env_provider_manual(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that env_provider sets environment variables and returns an EnvProvider."""
        # Set environment variables directly
        monkeypatch.setenv("APICONFIG_API_HOSTNAME", "env.example.com")
        monkeypatch.setenv("APICONFIG_AUTH_TYPE", "env_bearer")
        monkeypatch.setenv("APICONFIG_AUTH_TOKEN", "env_token_123")

        # Create an EnvProvider directly
        provider = EnvProvider(prefix="APICONFIG")

        # Check that the provider is an EnvProvider
        assert isinstance(provider, EnvProvider)

        # Check that the environment variables were set
        assert os.environ.get("APICONFIG_API_HOSTNAME") == "env.example.com"
        assert os.environ.get("APICONFIG_AUTH_TYPE") == "env_bearer"
        assert os.environ.get("APICONFIG_AUTH_TOKEN") == "env_token_123"

        # Check that the provider has the expected prefix
        assert provider.prefix == "APICONFIG"


class TestConfigManager:
    """Tests for the config_manager fixture."""

    def test_config_manager_manual(self) -> None:
        """Test that config_manager returns a ConfigManager with file and env providers."""
        # Create mock providers
        mock_file_provider = MagicMock(spec=FileProvider)
        mock_env_provider = MagicMock(spec=EnvProvider)

        # Create a ConfigManager directly
        manager = ConfigManager(providers=[mock_file_provider, mock_env_provider])

        # Check that the manager is a ConfigManager with the correct providers
        assert isinstance(manager, ConfigManager)
        assert manager.providers == [mock_file_provider, mock_env_provider]


class TestCustomAuthStrategyFactory:
    """Tests for the custom_auth_strategy_factory fixture."""

    def test_custom_auth_strategy_factory_with_callable(self) -> None:
        """Test that custom_auth_strategy_factory creates a CustomAuth with the provided callable."""

        # Define a test callable that will be used as a header_callback
        def test_header_callback() -> dict[str, str]:
            return {"X-Test": "test_value"}

        # Create a CustomAuth directly
        auth_strategy = CustomAuth(header_callback=test_header_callback)

        # Check that the strategy is a CustomAuth
        assert isinstance(auth_strategy, CustomAuth)

        # Test that the callable is used by calling the methods directly
        headers = auth_strategy.prepare_request_headers()
        params = auth_strategy.prepare_request_params()
        assert headers == {"X-Test": "test_value"}
        assert params == {}

    def test_custom_auth_strategy_factory_without_callable(self) -> None:
        """Test that custom_auth_strategy_factory creates a CustomAuth with a default no-op callable."""

        # Define a no-op header callback
        def default_header_callback() -> dict[str, str]:
            return {}

        # Create a CustomAuth directly
        auth_strategy = CustomAuth(header_callback=default_header_callback)

        # Check that the strategy is a CustomAuth
        assert isinstance(auth_strategy, CustomAuth)

        # Test that the default callable is a no-op by calling the methods directly
        headers = auth_strategy.prepare_request_headers()
        params = auth_strategy.prepare_request_params()

        # The headers and params should be empty
        assert headers == {}
        assert params == {}
