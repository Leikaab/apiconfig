import base64
import logging
from typing import Dict

from apiconfig.auth.base import AuthStrategy

log: logging.Logger

class BasicAuth(AuthStrategy):
    """
    Implements HTTP Basic Authentication according to RFC 7617.

    This strategy adds the 'Authorization' header with Basic credentials
    (base64-encoded username:password) to the request. The header format is:
    'Authorization: Basic <base64-encoded username:password>'.

    Basic Authentication is a simple authentication scheme built into the HTTP protocol.
    While simple to implement, it should only be used with HTTPS to ensure credentials
    are transmitted securely.
    """

    username: str
    password: str

    def __init__(self, username: str, password: str) -> None:
        """
        Initializes the BasicAuth strategy with username and password credentials.

        Args:
            username: The username for authentication. Must not be empty or contain only whitespace.
            password: The password for authentication. Must not be empty, but may contain only whitespace.

        Raises:
            AuthStrategyError: If the username is empty or contains only whitespace.
            AuthStrategyError: If the password is empty (but may contain only whitespace).

        Note:
            While username is validated to reject whitespace-only values, password validation
            allows whitespace-only values as they might be legitimate passwords.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Generates the 'Authorization' header for Basic Authentication.

        Creates a header with the format 'Authorization: Basic <base64-encoded username:password>'.
        The username and password are combined with a colon, encoded in UTF-8, then base64 encoded.

        Returns:
            A dictionary containing the 'Authorization' header with the Basic authentication credentials.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Returns an empty dictionary as Basic Auth uses headers, not query parameters.

        Basic Authentication is implemented exclusively through the 'Authorization' header
        and does not use query parameters for security reasons (to avoid credentials
        appearing in logs, browser history, or URLs).

        Returns:
            An empty dictionary, as no query parameters are needed for Basic Authentication.
        """
        ...
