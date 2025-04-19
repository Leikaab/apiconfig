from typing import Dict, Optional

from apiconfig.auth.base import AuthStrategy

class ApiKeyAuth(AuthStrategy):
    """
    Implements API Key authentication.

    The API key can be sent either in a request header or as a query parameter.

    Args:
        api_key: The API key string.
        header_name: The name of the HTTP header to use for the API key.
        param_name: The name of the query parameter to use for the API key.

    Raises:
        AuthStrategyError: If neither or both `header_name` and `param_name` are provided.
    """

    api_key: str
    header_name: Optional[str]
    param_name: Optional[str]

    def __init__(
        self,
        api_key: str,
        header_name: Optional[str] = None,
        param_name: Optional[str] = None,
    ) -> None: ...
    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepares headers for API key authentication if configured for headers.

        Returns:
            A dictionary containing the API key header, or an empty dictionary.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Prepares query parameters for API key authentication if configured for parameters.

        Returns:
            A dictionary containing the API key parameter, or an empty dictionary.
        """
        ...
