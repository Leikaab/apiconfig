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


def test_get_effective_settings_various_cases() -> None:
    cfg = ClientConfig(timeout=5.0, retries=2)
    cases = [
        (None, None, cfg, (5.0, 2)),
        (7.0, 4, cfg, (7.0, 4)),
        (None, 1, cfg, (5.0, 1)),
        (8.0, None, None, (8.0, 3)),
        (None, None, None, (10.0, 3)),
    ]
    for timeout, retries, config, expected in cases:
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
