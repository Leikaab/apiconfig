from typing import Dict

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError


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
        Initializes the BearerAuth strategy with the provided token.

        Args:
            token: The bearer token to use for authentication.
                  Must be a non-empty string.

        Raises:
            AuthStrategyError: If the token is empty or contains only whitespace.
                              This validation ensures that authentication attempts
                              are not made with invalid credentials.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepares the 'Authorization' header with the bearer token.

        Adds an 'Authorization' header with the format 'Bearer {token}'
        to be included in the HTTP request.

        Returns:
            A dictionary containing the 'Authorization' header with the
            bearer token value.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Bearer authentication does not modify query parameters.

        This method is implemented to satisfy the AuthStrategy interface,
        but Bearer authentication only uses headers, not query parameters.

        Returns:
            An empty dictionary, as Bearer authentication does not use
            query parameters.
        """
        ...
