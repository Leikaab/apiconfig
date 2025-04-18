from typing import Callable, Dict, Optional

from apiconfig.auth.base import AuthStrategy


class CustomAuth(AuthStrategy):
    """
    Implements custom authentication logic using provided callback functions.

    This strategy allows users to define their own functions to generate
    authentication headers or parameters dynamically.
    """

    def __init__(
        self,
        header_callback: Optional[Callable[[], Dict[str, str]]] = None,
        param_callback: Optional[Callable[[], Dict[str, str]]] = None,
    ) -> None:
        """
        Initializes the CustomAuth strategy.

        Args:
            header_callback: A callable that returns a dictionary of headers
                             to add to the request.
            param_callback: A callable that returns a dictionary of parameters
                            to add to the request.

        Raises:
            AuthStrategyError: If neither header_callback nor param_callback
                               is provided.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Generates request headers using the header_callback, if provided.

        Returns:
            A dictionary of headers.

        Raises:
            AuthStrategyError: If the header_callback does not return a dictionary
                               or raises an exception.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Generates request parameters using the param_callback, if provided.

        Returns:
            A dictionary of parameters.

        Raises:
            AuthStrategyError: If the param_callback does not return a dictionary
                               or raises an exception.
        """
        ...
