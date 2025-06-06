from unittest.mock import MagicMock

import pytest

from apiconfig.auth.token.refresh import (
    _get_effective_settings,
    _prepare_auth_and_payload,
)
from apiconfig.config.base import ClientConfig


class DummyBasicClient:
    """HTTP client with a BasicAuth class attribute."""

    def __init__(self) -> None:
        self.BasicAuth = MagicMock(return_value="basic_auth_obj")


class DummyRequestsClient:
    """HTTP client exposing an auth callable like requests.Session."""

    def __init__(self) -> None:
        self.auth = MagicMock()


client_cfg = ClientConfig(timeout=5.0, retries=2)


@pytest.mark.parametrize(
    "timeout,retries,config,expected",
    [
        (None, None, client_cfg, (5.0, 2)),
        (7.0, 4, client_cfg, (7.0, 4)),
        (None, 1, client_cfg, (5.0, 1)),
        (8.0, None, None, (8.0, 3)),
        (None, None, None, (10.0, 3)),
    ],
)
def test_get_effective_settings_various_cases(
    timeout: float | None, retries: int | None, config: ClientConfig | None, expected: tuple[float, int]
) -> None:
    assert _get_effective_settings(timeout, retries, config) == expected


def test_prepare_auth_and_payload_basic_auth() -> None:
    client = DummyBasicClient()
    auth, payload = _prepare_auth_and_payload("id", "secret", "rt", None, client)
    assert auth == "basic_auth_obj"
    assert "client_id" not in payload and "client_secret" not in payload
    assert payload["refresh_token"] == "rt"
    client.BasicAuth.assert_called_once_with(username="id", password="secret")


def test_prepare_auth_and_payload_requests_style() -> None:
    client = DummyRequestsClient()
    auth, payload = _prepare_auth_and_payload("id", "secret", "rt", None, client)
    assert auth == ("id", "secret")
    assert "client_id" not in payload and "client_secret" not in payload
    client.auth.assert_not_called()


def test_prepare_auth_and_payload_no_client_keeps_credentials() -> None:
    auth, payload = _prepare_auth_and_payload("id", "secret", "rt", {"scope": "s"}, None)
    assert auth is None
    assert payload["client_id"] == "id" and payload["client_secret"] == "secret"
    assert payload["scope"] == "s"


@pytest.mark.parametrize("client_id,client_secret", [("id", None), (None, "sec")])
def test_prepare_auth_and_payload_partial_credentials(client_id: str | None, client_secret: str | None) -> None:
    client = DummyBasicClient()
    auth, payload = _prepare_auth_and_payload(client_id, client_secret, "rt", None, client)
    assert auth is None
    if client_id is not None:
        assert payload["client_id"] == client_id
    if client_secret is not None:
        assert payload["client_secret"] == client_secret
    client.BasicAuth.assert_not_called()


def test_prepare_auth_and_payload_extra_params_preserved() -> None:
    client = DummyBasicClient()
    auth, payload = _prepare_auth_and_payload(
        "id",
        "secret",
        "rt",
        {"scope": "s", "aud": "a"},
        client,
    )
    assert auth == "basic_auth_obj"
    assert payload == {"grant_type": "refresh_token", "refresh_token": "rt", "scope": "s", "aud": "a"}
