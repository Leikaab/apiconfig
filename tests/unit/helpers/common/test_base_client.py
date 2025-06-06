import pytest
import httpx
from apiconfig.config.base import ClientConfig
from apiconfig.exceptions.http import HTTPUtilsError, JSONDecodeError
from apiconfig.types import HttpMethod, QueryParamType
from helpers_for_tests.common.base_client import BaseClient
from apiconfig.auth.base import AuthStrategy
from typing import Dict, Optional

class DummyAuthStrategy(AuthStrategy):
    def prepare_request_headers(self) -> Dict[str, str]:
        return {}
    def prepare_request_params(self) -> Optional[QueryParamType]:
        return None

class DummyClient(BaseClient):
    pass


def _make_client() -> DummyClient:
    config = ClientConfig(hostname="example.com", auth_strategy=DummyAuthStrategy())
    return DummyClient(config)

def test_handle_response_raises_on_error_status() -> None:
    client = _make_client()
    response = httpx.Response(status_code=404, text="not found")
    with pytest.raises(HTTPUtilsError):
        client._handle_response(response, HttpMethod.GET, "https://example.com/test")


def test_handle_response_parses_json() -> None:
    client = _make_client()
    response = httpx.Response(status_code=200, json={"ok": True})
    result = client._handle_response(response, HttpMethod.GET, "https://example.com/test")
    assert result == {"ok": True}


def test_handle_response_invalid_json() -> None:
    client = _make_client()
    response = httpx.Response(status_code=200, text="{invalid json")
    with pytest.raises(JSONDecodeError):
        client._handle_response(response, HttpMethod.GET, "https://example.com/test")

