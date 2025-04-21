from typing import Callable, Dict, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError


class CustomAuth(AuthStrategy):
    """Implements custom authentication logic using provided callback functions."""

    def __init__(
        self,
        header_callback: Optional[Callable[[], Dict[str, str]]] = None,
        param_callback: Optional[Callable[[], Dict[str, str]]] = None,
    ) -> None:
        if header_callback is None and param_callback is None:
            raise AuthStrategyError(
                "At least one callback (header or param) must be provided for CustomAuth."
            )
        self._header_callback = header_callback
        self._param_callback = param_callback

    def prepare_request_headers(self) -> Dict[str, str]:
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
        # Initialize headers and params if not provided
        headers = headers.copy() if headers else {}
        params = params.copy() if params else {}

        # Update with authentication headers and params
        headers.update(self.prepare_request_headers())
        params.update(self.prepare_request_params())

        return headers, params

    def prepare_request_params(self) -> Dict[str, str]:
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
