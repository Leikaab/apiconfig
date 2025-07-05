from typing import Dict, Optional

import httpx
import pytest

import apiconfig.types as api_types
from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.exceptions.http import HTTPUtilsError, JSONDecodeError
from helpers_for_tests.common.base_client import BaseClient


class DummyAuthStrategy(AuthStrategy):
    def prepare_request_headers(self) -> Dict[str, str]:
        return {}

    def prepare_request_params(self) -> Optional[api_types.QueryParamType]:
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
        client._handle_response(
            response,
            api_types.HttpMethod.GET,
            "https://example.com/test",
        )  # pyright: ignore[reportPrivateUsage]


def test_handle_response_parses_json() -> None:
    client = _make_client()
    response = httpx.Response(status_code=200, json={"ok": True})
    result = client._handle_response(
        response,
        api_types.HttpMethod.GET,
        "https://example.com/test",
    )  # pyright: ignore[reportPrivateUsage]
    assert result == {"ok": True}


def test_handle_response_invalid_json() -> None:
    client = _make_client()
    response = httpx.Response(status_code=200, text="{invalid json")
    with pytest.raises(JSONDecodeError):
        client._handle_response(
            response,
            api_types.HttpMethod.GET,
            "https://example.com/test",
        )  # pyright: ignore[reportPrivateUsage]


@pytest.mark.parametrize("body", ["", "null", "123", '"text"'])
def test_handle_response_empty_or_non_object_returns_empty_dict(body: str) -> None:
    """Non-object JSON bodies should result in an empty dict."""
    client = _make_client()
    response = httpx.Response(status_code=200, text=body)
    result = client._handle_response(
        response,
        api_types.HttpMethod.GET,
        "https://example.com/test",
    )  # pyright: ignore[reportPrivateUsage]
    assert result == {}
