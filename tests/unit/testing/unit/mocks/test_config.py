"""Tests for the mock configuration components in apiconfig.testing.unit.mocks.config."""

from unittest.mock import MagicMock

from apiconfig.config.base import ClientConfig
from apiconfig.testing.unit.mocks.config import (
    MockConfigManager,
    MockConfigProvider,
    create_mock_client_config,
)


class TestMockConfigProvider:
    """Tests for the MockConfigProvider class."""

    def test_init(self) -> None:
        """Test that MockConfigProvider initializes correctly."""
        config_data = {"hostname": "test.example.com", "timeout": 30}
        provider = MockConfigProvider(config_data=config_data)
        assert provider._config_data == config_data

    def test_load(self) -> None:
        """Test that load() returns the config data provided during initialization."""
        config_data = {"hostname": "test.example.com", "timeout": 30}
        provider = MockConfigProvider(config_data=config_data)
        result = provider.load()
        assert result == config_data
        # Ensure we get the same object back, not a copy
        assert result is config_data


class TestCreateMockClientConfig:
    """Tests for the create_mock_client_config function."""

    def test_default_values(self) -> None:
        """Test that create_mock_client_config uses default values when no args provided."""
        config = create_mock_client_config()
        assert isinstance(config, ClientConfig)
        assert config.hostname == "mock.example.com"
        assert config.version == "v1"
        assert config.timeout == 30
        assert config.retries == 3

    def test_override_hostname(self) -> None:
        """Test overriding the hostname parameter."""
        config = create_mock_client_config(hostname="custom.example.org")
        assert config.hostname == "custom.example.org"
        # Other defaults should remain
        assert config.version == "v1"
        assert config.timeout == 30
        assert config.retries == 3

    def test_override_version(self) -> None:
        """Test overriding the version parameter."""
        config = create_mock_client_config(version="v2")
        assert config.version == "v2"
        # Other defaults should remain
        assert config.hostname == "mock.example.com"
        assert config.timeout == 30
        assert config.retries == 3

    def test_override_timeout(self) -> None:
        """Test overriding the timeout parameter."""
        config = create_mock_client_config(timeout=60)
        assert config.timeout == 60
        # Other defaults should remain
        assert config.hostname == "mock.example.com"
        assert config.version == "v1"
        assert config.retries == 3

    def test_override_retries(self) -> None:
        """Test overriding the retries parameter."""
        config = create_mock_client_config(retries=5)
        assert config.retries == 5
        # Other defaults should remain
        assert config.hostname == "mock.example.com"
        assert config.version == "v1"
        assert config.timeout == 30

    def test_additional_kwargs(self) -> None:
        """Test passing additional kwargs to create_mock_client_config."""
        headers = {"X-Test": "Value"}
        config = create_mock_client_config(headers=headers, log_request_body=True)
        assert config.headers == headers
        assert config.log_request_body is True
        # Default values should still be set
        assert config.hostname == "mock.example.com"
        assert config.version == "v1"

    def test_override_all_parameters(self) -> None:
        """Test overriding all parameters at once."""
        headers = {"X-Custom": "Header"}
        auth_strategy = MagicMock()
        config = create_mock_client_config(
            hostname="api.test.com",
            version="v3",
            timeout=45,
            retries=2,
            headers=headers,
            auth_strategy=auth_strategy,
            log_request_body=True,
            log_response_body=True,
        )
        assert config.hostname == "api.test.com"
        assert config.version == "v3"
        assert config.timeout == 45
        assert config.retries == 2
        assert config.headers == headers
        assert config.auth_strategy == auth_strategy
        assert config.log_request_body is True
        assert config.log_response_body is True


class TestMockConfigManager:
    """Tests for the MockConfigManager class."""

    def test_init_default_providers(self) -> None:
        """Test initialization with providers=None (should default to a MagicMock provider)."""
        manager = MockConfigManager()
        # Should have one provider that's a MagicMock
        assert len(manager._providers) == 1
        assert isinstance(manager._providers[0], MagicMock)
        # The mock provider should have a load method that returns an empty dict
        assert manager._providers[0].load.return_value == {}

    def test_init_with_explicit_providers(self) -> None:
        """Test initialization with explicit providers."""
        provider1 = MockConfigProvider(config_data={"key1": "value1"})
        provider2 = MockConfigProvider(config_data={"key2": "value2"})
        providers = [provider1, provider2]

        manager = MockConfigManager(providers=providers)

        assert manager._providers == providers

    def test_init_default_mock_config(self) -> None:
        """Test initialization with mock_config=None (should set a default ClientConfig)."""
        manager = MockConfigManager()

        # load_config should be a MagicMock
        assert isinstance(manager.load_config, MagicMock)

        # The return value should be a default ClientConfig
        result = manager.load_config()
        assert isinstance(result, ClientConfig)
        assert result.hostname == "mock.example.com"
        assert result.version == "v1"
        assert result.timeout == 30
        assert result.retries == 3

    def test_init_with_specific_mock_config(self) -> None:
        """Test initialization with a specific mock_config instance."""
        mock_config = ClientConfig(
            hostname="test.example.org",
            version="v2",
            timeout=45,
            retries=2,
        )

        manager = MockConfigManager(mock_config=mock_config)

        # load_config should return the provided mock_config
        assert manager.load_config.return_value == mock_config
        assert manager.load_config() == mock_config

    def test_load_config_is_magicmock(self) -> None:
        """Test that load_config is a MagicMock instance allowing spying."""
        manager = MockConfigManager()

        assert isinstance(manager.load_config, MagicMock)

        # Call the method and verify it was called
        manager.load_config()
        manager.load_config.assert_called_once()

        # Reset the mock to clear the call history
        manager.load_config.reset_mock()

        # Call with arguments and verify they were passed
        manager.load_config(arg1="test", arg2=123)
        # Use assert_called_once_with to ensure it was called exactly once with these args
        manager.load_config.assert_called_once_with(arg1="test", arg2=123)

    def test_load_config_with_custom_return_value(self) -> None:
        """Test setting a custom return value for load_config."""
        manager = MockConfigManager()
        custom_config = ClientConfig(hostname="custom.example.com")

        # Set a custom return value
        manager.load_config.return_value = custom_config

        # Verify the custom return value is used
        result = manager.load_config()
        assert result == custom_config
