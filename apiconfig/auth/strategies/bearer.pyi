from typing import Dict

from apiconfig.auth.base import AuthStrategy

class BearerAuth(AuthStrategy):
    """
    Implements Bearer Token authentication.

    This strategy adds an 'Authorization: Bearer <token>' header to requests.
    """

    token: str

    def __init__(self, token: str) -> None:
        """
        Initializes the BearerAuth strategy.

        Args:
            token: The bearer token to use for authentication.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepares the 'Authorization' header with the bearer token.

        Returns:
            A dictionary containing the 'Authorization' header.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Bearer authentication does not typically modify query parameters.

        Returns:
            An empty dictionary.
        """
        ...
