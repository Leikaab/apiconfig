"""Authentication-specific exception classes for the apiconfig library."""

from .base import AuthenticationError


class InvalidCredentialsError(AuthenticationError):
    """Raised when provided credentials are invalid."""


class ExpiredTokenError(AuthenticationError):
    """Raised when an authentication token has expired."""


class MissingCredentialsError(AuthenticationError):
    """Raised when required credentials are not provided."""


class TokenRefreshError(AuthenticationError):
    """Raised when an attempt to refresh a token fails."""


class AuthStrategyError(AuthenticationError):
    """Base exception for errors specific to an authentication strategy."""
