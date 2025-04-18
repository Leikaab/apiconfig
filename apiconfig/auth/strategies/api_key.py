from typing import Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError


class ApiKeyAuth(AuthStrategy):

    def __init__(self, api_key: str, header_name: Optional[str] = None, param_name: Optional[str] = None):
        self.api_key = api_key
        self.header_name = header_name
        self.param_name = param_name

        # Validate that at least one of header_name or param_name is provided
        if header_name is None and param_name is None:
            raise AuthStrategyError("One of header_name or param_name must be provided for ApiKeyAuth")

        # Validate that only one of header_name or param_name is provided
        if header_name is not None and param_name is not None:
            raise AuthStrategyError("Only one of header_name or param_name should be provided for ApiKeyAuth")

    def prepare_request_headers(self) -> Dict[str, str]:
        if self.header_name is not None:
            return {self.header_name: self.api_key}
        return {}

    def prepare_request_params(self) -> Dict[str, str]:
        if self.param_name is not None:
            return {self.param_name: self.api_key}
        return {}
