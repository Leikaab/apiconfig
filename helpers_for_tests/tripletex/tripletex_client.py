"""Simplified Tripletex client using apiconfig patterns and utilities."""

from typing import Optional, Union

from apiconfig.config.base import ClientConfig
from apiconfig.types import HttpMethod, JsonObject, QueryParamType
from helpers_for_tests.common.base_client import BaseClient
from helpers_for_tests.tripletex.tripletex_auth import TripletexSessionAuth


class TripletexClient(BaseClient):
    """
    A streamlined client for interacting with the Tripletex API.

    This client demonstrates proper use of apiconfig utilities:
    - Uses apiconfig.utils.http for status checking and JSON handling
    - Uses apiconfig.utils.url for URL construction
    - Uses httpx for modern HTTP client capabilities
    - Leverages ClientConfig for centralized configuration
    """

    def __init__(self, client_config: ClientConfig):
        """
        Initialize the TripletexClient with a configured ClientConfig.

        Args
        ----
        client_config : ClientConfig
            Pre-configured ClientConfig with TripletexSessionAuth.

        Raises
        ------
        ValueError
            If auth_strategy is not TripletexSessionAuth.
        """
        super().__init__(client_config)
        if not isinstance(self.config.auth_strategy, TripletexSessionAuth):
            raise ValueError("ClientConfig.auth_strategy must be an instance of TripletexSessionAuth.")

    def list_countries(self, params: Optional[QueryParamType] = None) -> JsonObject:
        """
        List countries from Tripletex API.

        Args
        ----
        params : Optional[QueryParamType]
            Optional query parameters for filtering/sorting.

        Returns
        -------
        JsonObject
            JSON response containing country data.
        """
        result = self._request(HttpMethod.GET, "/country", params=params)
        return result if isinstance(result, dict) else {}

    def get_company_info(self, company_id: Optional[Union[str, int]] = None) -> JsonObject:
        """
        Get company information from Tripletex API.

        Args
        ----
        company_id : Optional[Union[str, int]]
            Optional company ID. If not provided, uses authenticated company.

        Returns
        -------
        JsonObject
            JSON response containing company data.
        """
        endpoint = "/company"
        if company_id:
            endpoint = f"/company/{company_id}"
        result = self._request(HttpMethod.GET, endpoint)
        return result if isinstance(result, dict) else {}

    def list_currencies(self, params: Optional[QueryParamType] = None) -> JsonObject:
        """
        List currencies from Tripletex API.

        Args
        ----
        params : Optional[QueryParamType]
            Optional query parameters for filtering/sorting.

        Returns
        -------
        JsonObject
            JSON response containing currency data.
        """
        result = self._request(HttpMethod.GET, "/currency", params=params)
        return result if isinstance(result, dict) else {}

    def get_session_info(self) -> JsonObject:
        """
        Get session information to verify authentication.

        Returns
        -------
        JsonObject
            JSON response containing session data.
        """
        result = self._request(HttpMethod.GET, "/token/session/>whoAmI")
        return result if isinstance(result, dict) else {}
