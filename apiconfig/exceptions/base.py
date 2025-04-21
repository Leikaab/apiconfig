__all__ = [
    "APIConfigError",
    "ConfigurationError",
    "AuthenticationError",
]


class APIConfigError(Exception):
    pass


class ConfigurationError(APIConfigError):
    pass


class AuthenticationError(APIConfigError):
    pass
