import base64
import logging
from typing import Dict

from apiconfig.auth.base import AuthStrategy

log: logging.Logger

class BasicAuth(AuthStrategy):
    """
    Implements HTTP Basic Authentication.

    This strategy adds the 'Authorization' header with Basic credentials
    (base64-encoded username:password) to the request.
    """

    username: str
    password: str

    def __init__(self, username: str, password: str) -> None:
        """
        Initializes the BasicAuth strategy.

        Args:
            username: The username for authentication.
            password: The password for authentication.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Generates the 'Authorization' header for Basic Authentication.

        Returns:
            A dictionary containing the 'Authorization' header.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Returns an empty dictionary as Basic Auth uses headers, not params.

        Returns:
            An empty dictionary.
        """
        ...
