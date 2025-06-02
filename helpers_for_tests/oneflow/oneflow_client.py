"""Simplified OneFlow client using apiconfig patterns and utilities."""

from typing import Optional, Union

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.config.base import ClientConfig
from apiconfig.types import HttpMethod, JsonList, JsonObject, QueryParamType
from helpers_for_tests.common.base_client import BaseClient


class OneFlowClient(BaseClient):
    """
    A streamlined client for interacting with the OneFlow API.

    This client demonstrates proper use of apiconfig utilities:
    - Uses apiconfig.utils.http for status checking and JSON handling
    - Uses apiconfig.utils.url for URL construction
    - Uses httpx for modern HTTP client capabilities
    - Leverages ClientConfig for centralized configuration
    """

    def __init__(self, client_config: ClientConfig):
        """
        Initialize the OneFlowClient with a configured ClientConfig.

        Args
        ----
        client_config : ClientConfig
            Pre-configured ClientConfig with ApiKeyAuth.

        Raises
        ------
        ValueError
            If auth_strategy is not ApiKeyAuth.
        """
        super().__init__(client_config)
        if not isinstance(self.config.auth_strategy, ApiKeyAuth):
            raise ValueError("ClientConfig.auth_strategy must be an instance of ApiKeyAuth.")

    def list_users(self, params: Optional[QueryParamType] = None) -> Union[JsonObject, JsonList]:
        """
        List users from OneFlow API.

        Args
        ----
        params : Optional[QueryParamType]
            Optional query parameters for filtering/sorting.

        Returns
        -------
        Union[JsonObject, JsonList]
            JSON response containing user data.
        """
        return self._request(HttpMethod.GET, "/users", params=params)

    def list_contracts(self, params: Optional[QueryParamType] = None) -> Union[JsonObject, JsonList]:
        """
        List contracts from OneFlow API.

        Args
        ----
        params : Optional[QueryParamType]
            Optional query parameters for filtering/sorting.

        Returns
        -------
        Union[JsonObject, JsonList]
            JSON response containing contract data.
        """
        return self._request(HttpMethod.GET, "/contracts", params=params)
