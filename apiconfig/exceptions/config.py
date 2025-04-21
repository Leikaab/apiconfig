from .base import ConfigurationError


class InvalidConfigError(ConfigurationError):
    pass


class MissingConfigError(ConfigurationError):
    pass


class ConfigLoadError(ConfigurationError):
    pass


class ConfigProviderError(ConfigurationError):
    pass


class ConfigValueError(ConfigurationError):
    pass


__all__ = [
    "InvalidConfigError",
    "MissingConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
    "ConfigValueError",
]
