import base64
import logging
from typing import Dict

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError

log = logging.getLogger(__name__)


class BasicAuth(AuthStrategy):

    def __init__(self, username: str, password: str) -> None:
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
        log.debug("[BasicAuth] Adding Basic Authentication header to request")
        auth_string = f"{self.username}:{self.password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        return {"Authorization": f"Basic {encoded_auth}"}

    def prepare_request_params(self) -> Dict[str, str]:
        return {}
