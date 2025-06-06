"""Simplified Fiken client using apiconfig patterns and utilities."""

from typing import Optional, Union

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.config.base import ClientConfig
from apiconfig.types import HttpMethod, JsonList, JsonObject, QueryParamType
from helpers_for_tests.common.base_client import BaseClient


class FikenClient(BaseClient):
    """
    A streamlined client for interacting with the Fiken API.

    This client demonstrates proper use of apiconfig utilities:
    - Uses apiconfig.utils.http for status checking and JSON handling
    - Uses apiconfig.utils.url for URL construction
    - Uses httpx for modern HTTP client capabilities
    - Leverages ClientConfig for centralized configuration
    """

    def __init__(self, client_config: ClientConfig):
        """
        Initialize the FikenClient with a configured ClientConfig.

        Args
        ----
        client_config : ClientConfig
            Pre-configured ClientConfig with BearerAuth.

        Raises
        ------
        ValueError
            If auth_strategy is not BearerAuth.
        """
        super().__init__(client_config)
        if not isinstance(self.config.auth_strategy, BearerAuth):
            raise ValueError("ClientConfig.auth_strategy must be an instance of BearerAuth.")

    def list_companies(self, params: Optional[QueryParamType] = None) -> Union[JsonObject, JsonList]:
        """
        List companies from Fiken API.

        Args
        ----
        params : Optional[QueryParamType]
            Optional query parameters for filtering/sorting.

        Returns
        -------
        Union[JsonObject, JsonList]
            JSON response containing company data (typically a list of companies).
        """
        return self._request(HttpMethod.GET, "/companies", params=params)
