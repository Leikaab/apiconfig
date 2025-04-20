from typing import Callable, Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError


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
        if header_callback is None and param_callback is None:
            raise AuthStrategyError(
                "At least one callback (header or param) must be provided for CustomAuth."
            )
        self._header_callback = header_callback
        self._param_callback = param_callback

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Generates request headers using the header_callback, if provided.

        Returns:
            A dictionary of headers.

        Raises:
            AuthStrategyError: If the header_callback does not return a dictionary.
        """
        if self._header_callback:
            try:
                result = self._header_callback()
                if not isinstance(result, dict):
                    raise AuthStrategyError(
                        "CustomAuth header callback must return a dictionary."
                    )
                return result
            except Exception as e:
                raise AuthStrategyError(
                    f"CustomAuth header callback failed: {e}"
                ) from e
        return {}

    def prepare_request(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> tuple[Dict[str, str], Dict[str, str]]:
        """
        Prepare authentication headers and parameters for an HTTP request.

        Args:
            headers: Optional initial headers dictionary to update.
            params: Optional initial parameters dictionary to update.

        Returns:
            A tuple of (headers, params) dictionaries with authentication data.
        """
        # Initialize headers and params if not provided
        headers = headers.copy() if headers else {}
        params = params.copy() if params else {}

        # Update with authentication headers and params
        headers.update(self.prepare_request_headers())
        params.update(self.prepare_request_params())

        return headers, params

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Generates request parameters using the param_callback, if provided.

        Returns:
            A dictionary of parameters.

        Raises:
            AuthStrategyError: If the param_callback does not return a dictionary.
        """
        if self._param_callback:
            try:
                result = self._param_callback()
                if not isinstance(result, dict):
                    raise AuthStrategyError(
                        "CustomAuth parameter callback must return a dictionary."
                    )
                return result
            except Exception as e:
                raise AuthStrategyError(
                    f"CustomAuth parameter callback failed: {e}"
                ) from e
        return {}
