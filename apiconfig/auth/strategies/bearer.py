"""Implements Bearer Token authentication strategy."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError, ExpiredTokenError
from apiconfig.types import (
    HttpRequestCallable,
    QueryParamType,
    TokenRefreshResult,
)

log = logging.getLogger(__name__)


class BearerAuth(AuthStrategy):
    """
    Implements Bearer Token authentication with refresh capabilities.

    This strategy adds an 'Authorization: Bearer <token>' header to requests,
    following the OAuth 2.0 Bearer Token specification (RFC 6750).

    Bearer tokens are typically used for accessing protected resources in APIs
    that implement OAuth 2.0 or similar authentication flows. This enhanced
    version supports token expiration checking and refresh capabilities.
    """

    access_token: str
    _expires_at: Optional[datetime]

    def __init__(
        self,
        access_token: str,
        expires_at: Optional[datetime] = None,
        http_request_callable: Optional[HttpRequestCallable] = None,
    ) -> None:
        """
        Initialize the BearerAuth strategy with refresh capabilities.

        Parameters
        ----------
        access_token : str
            The bearer token to use for authentication. Must be a non-empty string.
        expires_at : Optional[datetime], optional
            Optional expiration timestamp for the access token. Should be timezone-aware.
        http_request_callable : Optional[HttpRequestCallable], optional
            Optional HTTP callable for refresh operations. Required for refresh functionality.

        Raises
        ------
        AuthStrategyError
            If the access_token is empty or contains only whitespace. This validation
            ensures that authentication attempts are not made with invalid credentials.
        """
        super().__init__(http_request_callable)

        # Validate token is not empty or whitespace
        if not access_token or access_token.strip() == "":
            raise AuthStrategyError("Bearer token cannot be empty or whitespace")

        self.access_token = access_token
        self._expires_at = expires_at

    def can_refresh(self) -> bool:
        """
        Check if this Bearer auth strategy can perform refresh operations.

        Returns
        -------
        bool
            True if refresh is possible (has HTTP callable for custom refresh logic).
        """
        return self._http_request_callable is not None

    def is_expired(self) -> bool:
        """
        Check if the current access token is expired or close to expiring.

        Returns
        -------
        bool
            True if token is expired or expires within 5 minutes, False otherwise.
            Returns False if expiration time is not known.
        """
        if self._expires_at is None:
            return False  # Cannot determine expiry, assume valid

        # Consider token expired if it expires within 5 minutes
        buffer_time = timedelta(minutes=5)
        return datetime.now(timezone.utc) >= (self._expires_at - buffer_time)

    def refresh(self) -> Optional[TokenRefreshResult]:
        """
        Refresh the access token using custom refresh logic.

        This method provides a basic framework for token refresh. Concrete implementations
        should override this method to provide specific refresh logic for their use case.

        Returns
        -------
        Optional[TokenRefreshResult]
            New token data and any config updates.

        Raises
        ------
        AuthStrategyError
            If strategy is not configured for refresh.
        NotImplementedError
            If no custom refresh logic is provided.
        """
        if not self.can_refresh():
            raise AuthStrategyError("Bearer auth strategy is not configured for refresh")

        # This is a basic implementation that should be overridden by subclasses
        # or enhanced with specific refresh logic for the use case
        raise NotImplementedError(
            "Bearer auth refresh requires custom implementation. " "Override this method or use a specialized auth strategy for your token type."
        )

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepare the 'Authorization' header with the bearer token.

        Adds an 'Authorization' header with the format 'Bearer {token}'
        to be included in the HTTP request.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the 'Authorization' header with the bearer token value.

        Raises
        ------
        ExpiredTokenError
            If token is expired and cannot be refreshed.
        """
        if self.is_expired() and not self.can_refresh():
            raise ExpiredTokenError("Bearer token is expired and cannot be refreshed")

        log.debug("[BearerAuth] Injecting Bearer token into Authorization header.")
        return {"Authorization": f"Bearer {self.access_token}"}

    def prepare_request_params(self) -> Optional[QueryParamType]:
        """
        Bearer authentication does not modify query parameters.

        This method is implemented to satisfy the AuthStrategy interface,
        but Bearer authentication only uses headers, not query parameters.

        Returns
        -------
        Optional[QueryParamType]
            An empty dictionary, as Bearer authentication does not use query parameters.
        """
        return {}
