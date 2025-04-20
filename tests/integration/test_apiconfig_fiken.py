import os
from typing import Any

import httpx
import pytest

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.config.base import ClientConfig
from apiconfig.config.providers.env import EnvProvider


@pytest.fixture
def fiken_config() -> tuple[ClientConfig, str | None, str]:
    """
    Fixture to create a Fiken API config using apiconfig's EnvProvider and BearerAuth.
    Loads FIKEN_ACCESS_TOKEN and FIKEN_BASE_URL from the environment,
    defaulting base_url if unset.
    """
    env = EnvProvider()
    config = env.load()

    # Try FIKEN_ACCESS_TOKEN from config, then from os.environ
    token = config.get("FIKEN_ACCESS_TOKEN") or os.environ.get("FIKEN_ACCESS_TOKEN")
    # Try FIKEN_BASE_URL from config, then from os.environ, then default
    base_url = (
        config.get("FIKEN_BASE_URL")
        or os.environ.get("FIKEN_BASE_URL")
        or "https://api.fiken.no/api/v2"
    )

    # Ensure base_url has a scheme
    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    auth_strategy = BearerAuth(token) if token else None

    client_config = ClientConfig(
        hostname=base_url,
        auth_strategy=auth_strategy,
    )
    return client_config, token, base_url


def test_fiken_apiconfig_setup(
    fiken_config: tuple[ClientConfig, str | None, str],
) -> None:
    """
    Integration test: apiconfig config and auth for Fiken.
    Asserts that config is set up correctly using EnvProvider and BearerAuth.
    """
    client_config, token, base_url = fiken_config

    # Assert base_url is set correctly
    assert client_config.base_url == base_url.rstrip("/")

    if token:
        # Auth strategy should be BearerAuth and token should match
        assert client_config.auth_strategy is not None
        assert isinstance(client_config.auth_strategy, BearerAuth)
        assert client_config.auth_strategy.token == token
        assert len(client_config.auth_strategy.token) > 0
    else:
        # If no token, auth_strategy should be None
        assert client_config.auth_strategy is None


def test_fiken_api_companies(
    fiken_config: tuple[ClientConfig, str | None, str],
) -> None:
    """
    True integration test: Uses apiconfig to load config/auth and makes a real call to Fiken API.
    Skips if no token is set. Asserts on the real API response.
    """
    client_config, token, base_url = fiken_config

    if not token:
        pytest.skip(
            "FIKEN_ACCESS_TOKEN not set in environment; skipping real API call."
        )

    url = f"{base_url.rstrip('/')}/companies"
    headers: dict[str, str] = {}

    # Use BearerAuth to set the Authorization header
    if client_config.auth_strategy is not None:
        headers.update(client_config.auth_strategy.prepare_request_headers())

    with httpx.Client(timeout=10.0) as client:
        response = client.get(url, headers=headers)

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code} - {response.text}"

    data: Any = response.json()
    # Fiken returns a list of companies, so we expect a list or a dict with a key
    assert isinstance(data, (list, dict)), f"Unexpected response type: {type(data)}"
    # If dict, check for expected keys
    if isinstance(data, dict):
        assert (
            "companies" in data or "data" in data or "id" in data
        ), f"Response dict missing expected keys: {data.keys()}"
    # If list, check at least one company object
    if isinstance(data, list):
        assert len(data) > 0, "No companies returned in response."
        assert isinstance(data[0], dict), "Company object is not a dict."
