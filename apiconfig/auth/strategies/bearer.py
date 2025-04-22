"""Implements Bearer Token authentication strategy."""

import logging
from typing import Dict

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError

log = logging.getLogger(__name__)


class BearerAuth(AuthStrategy):
    """
    Implements Bearer Token authentication.

    This strategy adds an 'Authorization: Bearer <token>' header to requests,
    following the OAuth 2.0 Bearer Token specification (RFC 6750).

    Bearer tokens are typically used for accessing protected resources in APIs
    that implement OAuth 2.0 or similar authentication flows.
    """

    token: str

    def __init__(self, token: str) -> None:
        """
        Initialize the BearerAuth strategy with the provided token.

        Parameters
        ----------
        token : str
            The bearer token to use for authentication. Must be a non-empty string.

        Raises
        ------
        AuthStrategyError
            If the token is empty or contains only whitespace. This validation ensures
            that authentication attempts are not made with invalid credentials.
        """
        # Validate token is not empty or whitespace
        if not token or token.strip() == "":
            raise AuthStrategyError("Bearer token cannot be empty or whitespace")

        self.token = token

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepare the 'Authorization' header with the bearer token.

        Adds an 'Authorization' header with the format 'Bearer {token}'
        to be included in the HTTP request.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the 'Authorization' header with the bearer token value.
        """
        log.debug("[BearerAuth] Injecting Bearer token into Authorization header.")
        return {"Authorization": f"Bearer {self.token}"}

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Bearer authentication does not modify query parameters.

        This method is implemented to satisfy the AuthStrategy interface,
        but Bearer authentication only uses headers, not query parameters.

        Returns
        -------
        Dict[str, str]
            An empty dictionary, as Bearer authentication does not use query parameters.
        """
        return {}
