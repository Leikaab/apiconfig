from typing import Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError


class ApiKeyAuth(AuthStrategy):

    def __init__(
        self,
        api_key: str,
        header_name: Optional[str] = None,
        param_name: Optional[str] = None,
    ):
        # Validate api_key is not empty or whitespace
        if not api_key or api_key.strip() == "":
            raise AuthStrategyError("API key cannot be empty or whitespace")

        # Validate that at least one of header_name or param_name is provided
        if header_name is None and param_name is None:
            raise AuthStrategyError("One of header_name or param_name must be provided for ApiKeyAuth")

        # Validate that only one of header_name or param_name is provided
        if header_name is not None and param_name is not None:
            raise AuthStrategyError("Only one of header_name or param_name should be provided for ApiKeyAuth")

        # Validate header_name and param_name are not empty or whitespace if provided
        if header_name is not None and header_name.strip() == "":
            raise AuthStrategyError("Header name cannot be empty or whitespace")

        if param_name is not None and param_name.strip() == "":
            raise AuthStrategyError("Parameter name cannot be empty or whitespace")

        self.api_key = api_key
        self.header_name = header_name
        self.param_name = param_name

    def prepare_request_headers(self) -> Dict[str, str]:
        if self.header_name is not None:
            return {self.header_name: self.api_key}
        return {}

    def prepare_request_params(self) -> Dict[str, str]:
        if self.param_name is not None:
            return {self.param_name: self.api_key}
        return {}
