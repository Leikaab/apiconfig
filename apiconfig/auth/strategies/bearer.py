import logging
from typing import Dict

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError

log = logging.getLogger(__name__)


class BearerAuth(AuthStrategy):
    def __init__(self, token: str) -> None:
        # Validate token is not empty or whitespace
        if not token or token.strip() == "":
            raise AuthStrategyError("Bearer token cannot be empty or whitespace")

        self.token = token

    def prepare_request_headers(self) -> Dict[str, str]:
        log.debug("[BearerAuth] Injecting Bearer token into Authorization header.")
        return {"Authorization": f"Bearer {self.token}"}

    def prepare_request_params(self) -> Dict[str, str]:
        return {}
