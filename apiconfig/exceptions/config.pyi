"""Configuration-specific exception classes for the apiconfig library."""

from .base import ConfigurationError


class InvalidConfigError(ConfigurationError):
    """Raised when configuration values are invalid."""


class MissingConfigError(ConfigurationError):
    """Raised when required configuration values are missing."""


class ConfigLoadError(ConfigurationError):
    """Raised when configuration loading fails."""


class ConfigProviderError(ConfigurationError):
    """Raised for errors specific to a configuration provider."""


class ConfigValueError(ConfigurationError):
    """Raised when a configuration value cannot be coerced to the expected type."""


__all__ = [
    "InvalidConfigError",
    "MissingConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
    "ConfigValueError",
]
