from .base import AuthenticationError

__all__: list[str] = [
    "AuthenticationError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "TokenRefreshJsonError",
    "TokenRefreshTimeoutError",
    "TokenRefreshNetworkError",
    "AuthStrategyError",
]


class InvalidCredentialsError(AuthenticationError):
    pass


class ExpiredTokenError(AuthenticationError):
    pass


class MissingCredentialsError(AuthenticationError):
    pass


class TokenRefreshError(AuthenticationError):
    pass


class TokenRefreshJsonError(TokenRefreshError):
    pass


class TokenRefreshTimeoutError(TokenRefreshError):
    pass


class TokenRefreshNetworkError(TokenRefreshError):
    pass


class AuthStrategyError(AuthenticationError):
    pass
