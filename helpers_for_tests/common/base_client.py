"""Common base client for API interactions using apiconfig patterns."""

import json
from typing import Any, Dict, Optional, Union

import httpx

from apiconfig.config.base import ClientConfig
from apiconfig.exceptions.http import HTTPUtilsError, JSONDecodeError
from apiconfig.types import HttpMethod, JsonList, JsonObject, QueryParamType
from apiconfig.utils.http import is_success
from apiconfig.utils.url import build_url_with_auth


class BaseClient:
    """
    A base client providing common utilities for API interactions.

    This class encapsulates shared logic for handling HTTP responses,
    which can be reused by specific API clients like FikenClient or TripletexClient.
    """

    def __init__(self, client_config: ClientConfig):
        """
        Initialize the BaseClient with a configured ClientConfig.

        Args
        ----
        client_config : ClientConfig
            Pre-configured ClientConfig.

        Raises
        ------
        TypeError
            If client_config is not a ClientConfig instance.
        ValueError
            If auth_strategy is not configured.
        """
        if not isinstance(client_config, ClientConfig):
            raise TypeError("client_config must be an instance of ClientConfig.")
        if not client_config.auth_strategy:
            raise ValueError("ClientConfig.auth_strategy must be configured.")
        self.config = client_config

    def _build_url(self, endpoint: str, params: Optional[QueryParamType] = None) -> str:
        """
        Build the complete request URL using apiconfig URL utilities.

        Args
        ----
        endpoint : str
            The API endpoint path (e.g., "/companies").
        params : Optional[QueryParamType]
            Optional query parameters.

        Returns
        -------
        str
            Complete URL with query parameters.
        """
        auth_params = self.config.auth_strategy.prepare_request_params() if self.config.auth_strategy else None
        return build_url_with_auth(self.config.base_url, endpoint, params, auth_params)

    def _prepare_headers(self) -> Dict[str, str]:
        """
        Prepare request headers using ClientConfig and AuthStrategy.

        Returns
        -------
        Dict[str, str]
            Dictionary of headers for the request.
        """
        headers = self.config.headers.copy() if self.config.headers else {}
        if self.config.auth_strategy is not None:
            auth_headers = self.config.auth_strategy.prepare_request_headers()
            headers.update(auth_headers)
        return headers

    def _handle_response(self, response: httpx.Response, method: HttpMethod, url: str) -> Union[JsonObject, JsonList]:
        """
        Handle HTTP response using apiconfig utilities.

        Args
        ----
        response : httpx.Response
            The httpx Response object.
        method : HttpMethod
            The HTTP method used.
        url : str
            The request URL.

        Returns
        -------
        Union[JsonObject, JsonList]
            Parsed JSON response data as either an object or list.

        Raises
        ------
        HTTPUtilsError
            For non-2xx responses.
        JSONDecodeError
            If JSON parsing fails.
        """
        if not is_success(response.status_code):
            error_message = (
                f"HTTP request to {method.value} {url} failed with status {response.status_code}. " f"Response: '{response.text[:200]}...'"
            )
            raise HTTPUtilsError(error_message)

        if not response.text.strip():
            return {}

        try:
            # Parse JSON directly to handle both objects and arrays
            result = json.loads(response.text)
            return result if isinstance(result, (dict, list)) else {}  # Explicitly cast to expected types
        except json.JSONDecodeError as e:
            raise JSONDecodeError(
                f"Failed to decode JSON response from {method.value} {url}. "
                f"Status: {response.status_code}. JSON error: {e}. "
                f"Response: '{response.text[:200]}...'"
            ) from e
        except Exception as e:
            raise JSONDecodeError(
                f"Failed to decode JSON response from {method.value} {url}. "
                f"Status: {response.status_code}. Original error: {e}. "
                f"Response: '{response.text[:200]}...'"
            ) from e

    def _request(
        self,
        method: HttpMethod,
        endpoint: str,
        params: Optional[QueryParamType] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[JsonObject, JsonList]:
        """
        Make an authenticated request to the API using httpx.

        Args
        ----
        method : HttpMethod
            The HTTP method.
        endpoint : str
            The API endpoint path.
        params : Optional[QueryParamType]
            Optional query parameters.
        json_data : Optional[Dict[str, Any]]
            Optional JSON data for request body.
        **kwargs : Any
            Additional arguments passed to httpx.request.

        Returns
        -------
        Union[JsonObject, JsonList]
            The JSON response as either an object or list.

        Raises
        ------
        HTTPUtilsError
            For HTTP errors or network issues.
        JSONDecodeError
            If response JSON parsing fails.
        ValueError
            For invalid request configuration.
        """
        if not self.config.base_url:
            raise ValueError("ClientConfig.base_url is not configured.")

        url = self._build_url(endpoint, params)
        headers = self._prepare_headers()

        try:
            with httpx.Client(
                timeout=self.config.timeout,
                follow_redirects=True,
                verify=True,
            ) as client:
                response = client.request(
                    method=method.value,
                    url=url,
                    headers=headers,
                    json=json_data if json_data is not None else None,
                    **kwargs,
                )
                return self._handle_response(response, method, url)

        except httpx.RequestError as e:
            raise HTTPUtilsError(f"Request failed for {method.value} {url}: {e}") from e
        except httpx.HTTPStatusError as e:
            raise HTTPUtilsError(f"HTTP error {e.response.status_code} for {method.value} {url}: {e.response.text}") from e
        except Exception as e:
            raise HTTPUtilsError(f"Unexpected error during request to {method.value} {url}: {e}") from e

    def __repr__(self) -> str:
        """Return string representation of the client."""
        return (
            f"<{self.__class__.__name__} "
            f"base_url='{self.config.base_url if self.config else 'N/A'}' "
            f"auth='{type(self.config.auth_strategy).__name__ if self.config and self.config.auth_strategy else 'N/A'}'"
            ">"
        )
