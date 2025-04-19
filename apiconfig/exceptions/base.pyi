"""Base exception classes for the apiconfig library."""

class APIConfigError(Exception):
    """Base exception for all apiconfig errors."""

class ConfigurationError(APIConfigError):
    """Base exception for configuration-related errors."""

class AuthenticationError(APIConfigError):
    """Base exception for authentication-related errors."""
