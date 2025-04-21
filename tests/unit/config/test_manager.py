"""Tests for the ConfigManager class."""

import logging
from typing import Any, Dict, Optional

import pytest

from apiconfig.config.manager import ConfigManager
from apiconfig.exceptions.config import ConfigLoadError


# Mock provider classes for testing
class MockProvider:
    """Mock provider that returns a predefined config."""

    def __init__(
        self,
        config_data: Optional[Dict[str, Any]] = None,
        name: str = "MockProvider",
        raise_error: bool = False,
    ) -> None:
        self.config_data = config_data or {}
        self.name = name
        self.raise_error = raise_error
        self.load_called = False

    def load(self) -> Dict[str, Any]:
        """Mock load method."""
        self.load_called = True
        if self.raise_error:
            raise ValueError(f"Error in {self.name}")
        return self.config_data


class MockProviderWithGetConfig:
    """Mock provider that uses get_config instead of load."""

    def __init__(
        self,
        config_data: Optional[Dict[str, Any]] = None,
        name: str = "MockProviderWithGetConfig",
    ) -> None:
        self.config_data = config_data or {}
        self.name = name
        self.get_config_called = False

    def get_config(self) -> Dict[str, Any]:
        """Mock get_config method."""
        self.get_config_called = True
        return self.config_data


class MockProviderWithNoMethod:
    """Mock provider with neither load nor get_config methods."""

    def __init__(self, name: str = "MockProviderWithNoMethod") -> None:
        self.name = name


class TestConfigManager:
    """Tests for the ConfigManager class."""

    def test_init(self) -> None:
        """Test that ConfigManager initializes correctly."""
        providers = [MockProvider(), MockProvider()]
        manager = ConfigManager(providers=providers)
        assert manager._providers == providers

    def test_load_config_empty_providers(self) -> None:
        """Test loading config with no providers."""
        manager = ConfigManager(providers=[])
        config = manager.load_config()
        assert config == {}

    def test_load_config_single_provider(self) -> None:
        """Test loading config from a single provider."""
        provider = MockProvider(config_data={"api": {"hostname": "example.com"}})
        manager = ConfigManager(providers=[provider])

        config = manager.load_config()

        assert provider.load_called
        assert config == {"api": {"hostname": "example.com"}}

    def test_load_config_multiple_providers(self) -> None:
        """Test loading and merging config from multiple providers."""
        provider1 = MockProvider(
            config_data={"api": {"hostname": "example1.com"}, "timeout": 10},
            name="Provider1",
        )
        provider2 = MockProvider(
            config_data={"api": {"hostname": "example2.com"}, "retries": 3},
            name="Provider2",
        )

        manager = ConfigManager(providers=[provider1, provider2])
        config = manager.load_config()

        # Check that both providers were called
        assert provider1.load_called
        assert provider2.load_called

        # Check that the config was merged correctly with provider2 overriding provider1
        assert config == {
            "api": {"hostname": "example2.com"},  # Overridden by provider2
            "timeout": 10,  # From provider1
            "retries": 3,  # From provider2
        }

    def test_load_config_provider_with_get_config(self) -> None:
        """Test loading config from a provider with get_config method."""
        provider = MockProviderWithGetConfig(config_data={"api": {"hostname": "example.com"}})
        manager = ConfigManager(providers=[provider])

        config = manager.load_config()

        assert provider.get_config_called
        assert config == {"api": {"hostname": "example.com"}}

    def test_load_config_provider_with_no_method(self) -> None:
        """Test loading config from a provider with neither load nor get_config."""
        provider = MockProviderWithNoMethod()
        manager = ConfigManager(providers=[provider])

        with pytest.raises(ConfigLoadError, match="lacks a 'load' or 'get_config' method"):
            manager.load_config()

    def test_load_config_provider_returns_none(self) -> None:
        """Test loading config from a provider that returns None."""
        provider = MockProvider(config_data=None)
        manager = ConfigManager(providers=[provider])

        config = manager.load_config()

        assert provider.load_called
        assert config == {}

    def test_load_config_provider_returns_empty_dict(self) -> None:
        """Test loading config from a provider that returns an empty dict."""
        provider = MockProvider(config_data={})
        manager = ConfigManager(providers=[provider])

        config = manager.load_config()

        assert provider.load_called
        assert config == {}

    def test_load_config_provider_raises_error(self) -> None:
        """Test loading config when a provider raises an error."""
        provider = MockProvider(raise_error=True)
        manager = ConfigManager(providers=[provider])

        with pytest.raises(ConfigLoadError, match="Failed to load configuration"):
            manager.load_config()

    def test_load_config_first_provider_raises_error(self) -> None:
        """Test that if the first provider raises an error, the second is not called."""
        provider1 = MockProvider(raise_error=True, name="Provider1")
        provider2 = MockProvider(name="Provider2")

        manager = ConfigManager(providers=[provider1, provider2])

        with pytest.raises(ConfigLoadError):
            manager.load_config()

        assert provider1.load_called
        assert not provider2.load_called

    def test_load_config_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that ConfigManager logs appropriate messages."""
        caplog.set_level(logging.DEBUG)

        provider1 = MockProvider(config_data={"api": {"hostname": "example1.com"}}, name="Provider1")
        provider2 = MockProvider(config_data={"api": {"hostname": "example2.com"}}, name="Provider2")

        manager = ConfigManager(providers=[provider1, provider2])
        manager.load_config()

        # Check for expected log messages
        assert "Loading configuration from 2 providers" in caplog.text
        assert "Loading configuration from provider: MockProvider" in caplog.text
        assert "Merged config from MockProvider" in caplog.text
        assert "Configuration loaded successfully from all providers" in caplog.text

    def test_load_config_provider_returns_non_dict_value_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test loading config from a provider that returns a non-dict value logs a warning."""
        import logging

        caplog.set_level(logging.WARNING)

        # Create a provider that returns a non-dict value
        class BadProvider:
            def load(self) -> str:
                return "not a dict"

            def __str__(self) -> str:
                return "BadProvider"

        provider = BadProvider()
        manager = ConfigManager(providers=[provider])

        # This should not raise an error, but should log a warning
        config = manager.load_config()

        # The result should be an empty dict since the non-dict value was ignored
        assert config == {}

        # Check that a warning was logged
        assert "Provider returned non-dict value" in caplog.text
        assert "BadProvider" in caplog.text
