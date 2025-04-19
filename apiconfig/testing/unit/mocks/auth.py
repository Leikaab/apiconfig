# Implementation only, no docstrings or public type hints here
from typing import Any, Dict, Optional, Tuple

from apiconfig.auth.base import AuthStrategy
from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth


class MockAuthStrategy(AuthStrategy):
    def __init__(
        self,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        self.override_headers = override_headers if override_headers is not None else {}
        self.override_params = override_params if override_params is not None else {}
        self.raise_exception = raise_exception

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        if self.raise_exception:
            raise self.raise_exception

        final_headers = headers.copy() if headers else {}
        final_headers.update(self.override_headers)

        final_params = params.copy() if params else {}
        final_params.update(self.override_params)

        return final_headers, final_params

    # Add dummy implementations for abstract methods inherited from AuthStrategy
    # to make MockAuthStrategy concrete and instantiable for tests.
    # The actual mock logic is handled by the overridden prepare_request above.
    def prepare_request_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        # This method is required by AuthStrategy ABC.
        # Ensure it always returns Dict[str, str] as per the signature.
        # The actual mock logic uses the main prepare_request method.
        current_headers = headers if headers is not None else {}
        # In a real scenario, auth might be applied here. For the mock, just return.
        return current_headers

    def prepare_request_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # This method is required by AuthStrategy ABC.
        # Ensure it always returns Dict[str, Any] as per the signature.
        # The actual mock logic uses the main prepare_request method.
        current_params = params if params is not None else {}
        # In a real scenario, auth might be applied here. For the mock, just return.
        return current_params


class MockBasicAuth(MockAuthStrategy, BasicAuth):
    def __init__(
        self,
        username: str = "testuser",
        password: str = "testpass",
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        # Initialize the real strategy first for type checking etc.
        BasicAuth.__init__(self, username, password)
        # Initialize the mock behavior
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy


class MockBearerAuth(MockAuthStrategy, BearerAuth):
    def __init__(
        self,
        token: str = "testtoken",
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        BearerAuth.__init__(self, token)
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy


class MockApiKeyAuth(MockAuthStrategy, ApiKeyAuth):
    def __init__(
        self,
        api_key: str = "testapikey",
        header_name: str = "X-API-Key",
        param_name: Optional[str] = None,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        ApiKeyAuth.__init__(self, api_key, header_name, param_name)
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy


class MockCustomAuth(MockAuthStrategy, CustomAuth):
    def __init__(
        self,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ):
        # CustomAuth has no __init__, so just call MockAuthStrategy's
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy
