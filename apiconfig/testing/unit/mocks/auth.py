# Implementation only, no docstrings or public type hints here
from typing import Any, Dict, Optional, Tuple

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth


class MockBasicAuth(BasicAuth):
    def __init__(
        self,
        username: str = "testuser",
        password: str = "testpass",
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        super().__init__(username, password)
        self._return_headers = return_headers
        self._return_params = return_params
        self._raise_exception = raise_exception

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        if self._raise_exception:
            raise self._raise_exception

        base_headers, base_params = super().prepare_request(headers, params)

        final_headers = base_headers.copy()
        if self._return_headers is not None:
            final_headers.update(self._return_headers)  # Allow overriding/adding

        final_params = base_params.copy()
        if self._return_params is not None:
            final_params.update(self._return_params)  # Allow overriding/adding

        return final_headers, final_params


class MockBearerAuth(BearerAuth):
    def __init__(
        self,
        token: str = "testtoken",
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        super().__init__(token)
        self._return_headers = return_headers
        self._return_params = return_params
        self._raise_exception = raise_exception

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        if self._raise_exception:
            raise self._raise_exception

        base_headers, base_params = super().prepare_request(headers, params)

        final_headers = base_headers.copy()
        if self._return_headers is not None:
            final_headers.update(self._return_headers)

        final_params = base_params.copy()
        if self._return_params is not None:
            final_params.update(self._return_params)

        return final_headers, final_params


class MockApiKeyAuth(ApiKeyAuth):
    def __init__(
        self,
        api_key: str = "testapikey",
        header_name: str = "X-API-Key",
        param_name: Optional[str] = None,
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        super().__init__(api_key, header_name, param_name)
        self._return_headers = return_headers
        self._return_params = return_params
        self._raise_exception = raise_exception

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        if self._raise_exception:
            raise self._raise_exception

        base_headers, base_params = super().prepare_request(headers, params)

        final_headers = base_headers.copy()
        if self._return_headers is not None:
            final_headers.update(self._return_headers)

        final_params = base_params.copy()
        if self._return_params is not None:
            final_params.update(self._return_params)

        return final_headers, final_params


class MockCustomAuth(CustomAuth):
    def __init__(
        self,
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        self._return_headers = return_headers if return_headers is not None else {}
        self._return_params = return_params if return_params is not None else {}
        self._raise_exception = raise_exception

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        if self._raise_exception:
            raise self._raise_exception

        final_headers = headers.copy() if headers else {}
        final_headers.update(self._return_headers)

        final_params = params.copy() if params else {}
        final_params.update(self._return_params)

        return final_headers, final_params
