import logging
from typing import Dict

from apiconfig.auth.base import AuthStrategy

log = logging.getLogger(__name__)


class BearerAuth(AuthStrategy):
    def __init__(self, token: str) -> None:
        self.token = token

    def prepare_request_headers(self) -> Dict[str, str]:
        log.debug("[BearerAuth] Injecting Bearer token into Authorization header.")
        return {"Authorization": f"Bearer {self.token}"}

    def prepare_request_params(self) -> Dict[str, str]:
        return {}
