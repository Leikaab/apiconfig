"""Implement HTTP Basic Authentication according to RFC 7617.

It provides a strategy for adding the 'Authorization' header with Basic
credentials (base64-encoded username:password) to HTTP requests.
"""

import base64
import logging
from typing import Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError
from apiconfig.types import QueryParamType

log: logging.Logger = logging.getLogger(__name__)


class BasicAuth(AuthStrategy):
    """Implements HTTP Basic Authentication according to RFC 7617.

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
        """Initialize the BasicAuth strategy with username and password credentials.

        Parameters
        ----------
        username : str
            The username for authentication. Must not be empty or contain only whitespace.
        password : str
            The password for authentication. Must not be empty, but may contain only whitespace.

        Raises
        ------
        AuthStrategyError
            If the username is empty or contains only whitespace.
        AuthStrategyError
            If the password is empty (but may contain only whitespace).

        Notes
        -----
        While username is validated to reject whitespace-only values, password validation
        allows whitespace-only values as they might be legitimate passwords.

        """
        # Validate username is not empty or whitespace
        if not username or username.strip() == "":
            raise AuthStrategyError("Username cannot be empty or whitespace")

        # Validate password is not empty
        if not password:
            raise AuthStrategyError("Password cannot be empty")

        log.debug(
            "[BasicAuth] Initialized with username: %s (Password not logged)",
            username,
        )
        self.username = username
        self.password = password

    def prepare_request_headers(self) -> Dict[str, str]:
        """Generate the 'Authorization' header for Basic Authentication.

        Creates a header with the format 'Authorization: Basic <base64-encoded username:password>'.
        The username and password are combined with a colon, encoded in UTF-8, then base64 encoded.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the 'Authorization' header with the Basic authentication credentials.

        """
        log.debug("[BasicAuth] Adding Basic Authentication header to request")
        auth_string = f"{self.username}:{self.password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        return {"Authorization": f"Basic {encoded_auth}"}

    def prepare_request_params(self) -> Optional[QueryParamType]:
        """Return an empty dictionary as Basic Auth uses headers, not query parameters.

        Basic Authentication is implemented exclusively through the 'Authorization' header
        and does not use query parameters for security reasons (to avoid credentials
        appearing in logs, browser history, or URLs).

        Returns
        -------
        Optional[QueryParamType]
            An empty dictionary, as no query parameters are needed for Basic Authentication.

        """
        return {}
