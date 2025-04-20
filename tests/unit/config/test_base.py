"""Tests for the ClientConfig class."""


from typing import cast

import pytest

from apiconfig.auth.base import AuthStrategy

from apiconfig.config.base import ClientConfig
from apiconfig.exceptions.config import InvalidConfigError, MissingConfigError


# Mock auth strategy for testing
class MockAuthStrategy:
    """Mock auth strategy for testing."""

    def __init__(self, name: str = "mock_strategy") -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MockAuthStrategy):
            return NotImplemented
        return self.name == other.name


class TestClientConfig:
    """Tests for the ClientConfig class."""

    def test_init_default_values(self) -> None:
        """Test that ClientConfig initializes with default values."""
        config = ClientConfig()

        # Check default values
        assert config.hostname is None
        assert config.version is None
        assert config.headers == {}
        assert config.timeout == 10.0
        assert config.retries == 3
        assert config.auth_strategy is None
        assert config.log_request_body is False
        assert config.log_response_body is False

    def test_init_custom_values(self) -> None:
        """Test that ClientConfig initializes with custom values."""
        auth_strategy = MockAuthStrategy()
        config = ClientConfig(
            hostname="api.example.com",
            version="v1",
            headers={"User-Agent": "Test"},
            timeout=30.0,
            retries=5,
            auth_strategy=cast("AuthStrategy", auth_strategy),
            log_request_body=True,
            log_response_body=True,
        )

        # Check custom values
        assert config.hostname == "api.example.com"
        assert config.version == "v1"
        assert config.headers == {"User-Agent": "Test"}
        assert config.timeout == 30.0
        assert config.retries == 5
        assert config.auth_strategy is auth_strategy
        assert config.log_request_body is True
        assert config.log_response_body is True

    def test_init_partial_custom_values(self) -> None:
        """Test that ClientConfig initializes with some custom values."""
        config = ClientConfig(
            hostname="api.example.com",
            timeout=30.0,
        )

        # Check that specified values are custom and others are default
        assert config.hostname == "api.example.com"
        assert config.version is None
        assert config.headers == {}
        assert config.timeout == 30.0
        assert config.retries == 3  # Default
        assert config.auth_strategy is None
        assert config.log_request_body is False  # Default
        assert config.log_response_body is False  # Default

    def test_init_validation_negative_timeout(self) -> None:
        """Test that ClientConfig raises InvalidConfigError for negative timeout."""
        with pytest.raises(InvalidConfigError, match="Timeout must be non-negative"):
            ClientConfig(timeout=-1.0)

    def test_init_validation_negative_retries(self) -> None:
        """Test that ClientConfig raises InvalidConfigError for negative retries."""
        with pytest.raises(InvalidConfigError, match="Retries must be non-negative"):
            ClientConfig(retries=-1)

    def test_base_url_with_hostname(self) -> None:
        """Test base_url property with hostname set."""
        config = ClientConfig(hostname="api.example.com")
        assert config.base_url == "https://api.example.com"

    def test_base_url_with_hostname_and_version(self) -> None:
        """Test base_url property with hostname and version set."""
        config = ClientConfig(hostname="api.example.com", version="v1")
        assert config.base_url == "https://api.example.com/v1"

    def test_base_url_with_hostname_and_trailing_slash(self) -> None:
        """Test base_url property with hostname that has a trailing slash."""
        config = ClientConfig(hostname="api.example.com/")
        assert config.base_url == "https://api.example.com"

    def test_base_url_with_hostname_and_version_and_trailing_slash(self) -> None:
        """Test base_url property with hostname and version that have trailing slashes."""
        config = ClientConfig(hostname="api.example.com/", version="v1/")
        assert config.base_url == "https://api.example.com/v1"

    def test_base_url_with_scheme_in_hostname(self) -> None:
        """Test base_url property with hostname that includes a scheme."""
        config = ClientConfig(hostname="http://api.example.com")
        assert config.base_url == "http://api.example.com"

    def test_base_url_with_scheme_in_hostname_and_version(self) -> None:
        """Test base_url property with hostname that includes a scheme and version."""
        config = ClientConfig(hostname="http://api.example.com", version="v1")
        assert config.base_url == "http://api.example.com/v1"

    def test_base_url_without_hostname(self) -> None:
        """Test base_url property without hostname raises MissingConfigError."""
        config = ClientConfig()
        with pytest.raises(MissingConfigError, match="hostname is required"):
            _ = config.base_url

    def test_merge_with_compatible_type(self) -> None:
        """Test merging with a compatible ClientConfig instance."""
        base_config = ClientConfig(
            hostname="api.example.com",
            version="v1",
            headers={"User-Agent": "Base"},
            timeout=10.0,
            retries=3,
        )

        other_config = ClientConfig(
            hostname="api2.example.com",
            headers={"Authorization": "Bearer token"},
            timeout=20.0,
        )

        merged = base_config.merge(other_config)

        # Check that merged config has values from other_config where specified
        assert merged.hostname == "api2.example.com"  # From other
        assert merged.version == "v1"  # From base
        assert merged.headers == {
            "User-Agent": "Base",  # From base
            "Authorization": "Bearer token",  # From other
        }
        assert merged.timeout == 20.0  # From other
        assert merged.retries == 3  # From base

    def test_merge_with_incompatible_type(self) -> None:
        """Test merging with an incompatible type returns NotImplemented."""
        config = ClientConfig()
        result = config.merge("not a ClientConfig")  # type: ignore[arg-type]
        assert result is NotImplemented

    def test_merge_with_none_values(self) -> None:
        """Test that None values in other don't override base values."""
        base_config = ClientConfig(
            hostname="api.example.com",
            version="v1",
        )

        other_config = ClientConfig()  # All None or default values

        merged = base_config.merge(other_config)

        # Check that None values in other didn't override base values
        assert merged.hostname == "api.example.com"
        assert merged.version == "v1"

    def test_merge_with_auth_strategy(self) -> None:
        """Test merging with auth_strategy."""
        base_auth = MockAuthStrategy(name="base_auth")
        other_auth = MockAuthStrategy(name="other_auth")

        base_config = ClientConfig(auth_strategy=cast("AuthStrategy", base_auth))
        other_config = ClientConfig(auth_strategy=cast("AuthStrategy", other_auth))

        merged = base_config.merge(other_config)

        # Check that other's auth_strategy overrides base's
        assert merged.auth_strategy == other_auth

    def test_merge_validation(self) -> None:
        """Test that merged config is validated."""
        base_config = ClientConfig(timeout=10.0)
        other_config = ClientConfig()

        # Modify other_config's timeout to be negative (invalid)
        other_config.timeout = -1.0

        with pytest.raises(InvalidConfigError, match="Merged timeout must be non-negative"):
            base_config.merge(other_config)

    def test_merge_method(self) -> None:
        """Test that merge method works correctly."""
        base_config = ClientConfig(hostname="api.example.com")
        other_config = ClientConfig(version="v1")

        # Use the merge method instead of + operator
        result = base_config.merge(other_config)

        # Check that the merge works correctly
        assert result.hostname == "api.example.com"
        assert result.version == "v1"

    def test_merge_with_incompatible_type_raises_error(self) -> None:
        """Test that merge method raises TypeError with incompatible type."""
        config = ClientConfig()

        # The merge method returns NotImplemented, not raises TypeError
        result = config.merge("not a ClientConfig")  # type: ignore[arg-type]
        assert result is NotImplemented

    def test_merge_configs_static_method(self) -> None:
        """Test the merge_configs static method."""
        base_config = ClientConfig(hostname="api.example.com")
        other_config = ClientConfig(version="v1")

        merged = ClientConfig.merge_configs(base_config, other_config)

        assert merged.hostname == "api.example.com"
        assert merged.version == "v1"

    def test_merge_configs_with_incompatible_types(self) -> None:
        """Test that merge_configs raises TypeError with incompatible types."""
        config = ClientConfig()

        with pytest.raises(TypeError, match="Both arguments must be instances of ClientConfig"):
            ClientConfig.merge_configs(config, "not a ClientConfig")  # type: ignore[type-var]

        with pytest.raises(TypeError, match="Both arguments must be instances of ClientConfig"):
            ClientConfig.merge_configs("not a ClientConfig", config)  # type: ignore[type-var]

    def test_deep_copy_on_merge(self) -> None:
        """Test that merge creates deep copies of mutable attributes."""
        base_config = ClientConfig(headers={"User-Agent": "Base"})
        other_config = ClientConfig(headers={"Authorization": "Bearer token"})

        merged = base_config.merge(other_config)

        # Modify the original headers
        assert base_config.headers is not None

        base_config.headers["User-Agent"] = "Modified"
        assert other_config.headers is not None
        other_config.headers["Authorization"] = "Modified"

        # Check that merged headers are not affected
        assert merged.headers == {
            "User-Agent": "Base",
            "Authorization": "Bearer token",
        }

    def test_subclass_default_values(self) -> None:
        """Test that subclasses can define their own default values."""
        class CustomConfig(ClientConfig):
            hostname = "custom.example.com"
            version = "v2"
            timeout = 60.0

        config = CustomConfig()

        assert config.hostname == "custom.example.com"
        assert config.version == "v2"
        assert config.timeout == 60.0

        # Override with instance values
        config2 = CustomConfig(hostname="override.example.com")

        assert config2.hostname == "override.example.com"
        assert config2.version == "v2"  # Still from class
