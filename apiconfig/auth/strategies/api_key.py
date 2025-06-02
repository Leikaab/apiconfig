"""
Implement API Key authentication strategy for the apiconfig library.

It allows sending the API key either in a request header or as a query parameter.
"""

from typing import Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError
from apiconfig.types import QueryParamType


class ApiKeyAuth(AuthStrategy):
    """
    Implements API Key authentication.

    The API key can be sent either in a request header or as a query parameter.
    You must provide exactly one of `header_name` or `param_name` to specify how
    the API key should be sent.

    Parameters
    ----------
    api_key : str
        The API key string.
    header_name : Optional[str]
        The name of the HTTP header to use for the API key.
    param_name : Optional[str]
        The name of the query parameter to use for the API key.

    Raises
    ------
    AuthStrategyError
        If the API key is empty or whitespace.
    AuthStrategyError
        If neither `header_name` nor `param_name` is provided.
    AuthStrategyError
        If both `header_name` and `param_name` are provided.
    AuthStrategyError
        If the provided `header_name` or `param_name` is empty or whitespace.
    """

    api_key: str
    header_name: Optional[str]
    param_name: Optional[str]

    def __init__(
        self,
        api_key: str,
        header_name: Optional[str] = None,
        param_name: Optional[str] = None,
    ) -> None:
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
        """
        Prepare headers for API key authentication if configured for headers.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the API key header, or an empty dictionary.
        """
        if self.header_name is not None:
            return {self.header_name: self.api_key}

        return {}

    def prepare_request_params(self) -> Optional[QueryParamType]:
        """
        Prepare query parameters for API key authentication if configured for parameters.

        Returns
        -------
        Optional[QueryParamType]
            A dictionary containing the API key parameter, or an empty dictionary.
        """
        if self.param_name is not None:
            return {self.param_name: self.api_key}

        return {}
