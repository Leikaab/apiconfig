import os
from typing import Any, Dict, Optional, Tuple

import httpx
import pytest

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.config.base import ClientConfig
from apiconfig.config.providers.env import EnvProvider


@pytest.fixture
def oneflow_config() -> Tuple[ClientConfig, Optional[str], Optional[str], str]:
    """
    Fixture to create a Oneflow API config using apiconfig's EnvProvider and ApiKeyAuth.
    Loads ONEFLOW_API_KEY, ONEFLOW_USER_EMAIL, and ONEFLOW_BASE_URL from the environment,
    defaulting base_url if unset.
    """
    env = EnvProvider(prefix="")
    config = env.load()

    api_key = config.get("ONEFLOW_API_KEY") or os.environ.get("ONEFLOW_API_KEY")
    user_email = config.get("ONEFLOW_USER_EMAIL") or os.environ.get("ONEFLOW_USER_EMAIL")
    base_url = (
        config.get("ONEFLOW_BASE_URL")
        or os.environ.get("ONEFLOW_BASE_URL")
        or "https://api.test.oneflow.com/v1"
    )

    # Ensure base_url has a scheme
    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    auth_strategy = ApiKeyAuth(api_key, header_name="x-oneflow-api-token") if api_key else None

    headers: Dict[str, str] = {}
    if user_email:
        headers["x-oneflow-user-email"] = user_email

    client_config = ClientConfig(
        hostname=base_url,
        auth_strategy=auth_strategy,
        headers=headers,
    )
    return client_config, api_key, user_email, base_url


def test_oneflow_apiconfig_setup(
    oneflow_config: Tuple[ClientConfig, Optional[str], Optional[str], str]
) -> None:
    """
    Integration test: apiconfig config and auth for Oneflow.
    Asserts that config is set up correctly using EnvProvider and ApiKeyAuth.
    """
    client_config, api_key, user_email, base_url = oneflow_config

    # Assert base_url is set correctly
    assert client_config.base_url == base_url.rstrip("/")

    if api_key:
        # Auth strategy should be ApiKeyAuth and api_key should match
        assert client_config.auth_strategy is not None
        assert isinstance(client_config.auth_strategy, ApiKeyAuth)
        assert client_config.auth_strategy.api_key == api_key
        assert len(client_config.auth_strategy.api_key) > 0
    else:
        # If no api_key, auth_strategy should be None
        assert client_config.auth_strategy is None

    if user_email:
        assert client_config.headers is not None
        assert "x-oneflow-user-email" in client_config.headers
        assert client_config.headers["x-oneflow-user-email"] == user_email
    else:
        if client_config.headers is not None:
            assert "x-oneflow-user-email" not in client_config.headers


def test_oneflow_api_users(
    oneflow_config: Tuple[ClientConfig, Optional[str], Optional[str], str]
) -> None:
    """
    True integration test: Uses apiconfig to load config/auth and makes a real call to Oneflow API.
    Skips if no API key or user email is set. Asserts on the real API response.
    """
    client_config, api_key, user_email, base_url = oneflow_config

    if not api_key:
        pytest.skip("ONEFLOW_API_KEY not set in environment; skipping real API call.")
    if not user_email:
        pytest.skip("ONEFLOW_USER_EMAIL not set in environment; skipping real API call.")

    url = f"{base_url.rstrip('/')}/users"
    headers: Dict[str, str] = {}

    # Use ApiKeyAuth to set the x-oneflow-api-token header
    if client_config.auth_strategy is not None:
        headers.update(client_config.auth_strategy.prepare_request_headers())
    # Add the user email header
    headers.update(client_config.headers or {})

    with httpx.Client(timeout=10.0) as client:
        response = client.get(url, headers=headers)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code} - {response.text}"

    data: Any = response.json()
    # Oneflow returns a dict with a "data" key containing a list of users
    assert isinstance(data, dict), f"Unexpected response type: {type(data)}"
    assert "data" in data, f"Response dict missing 'data' key: {data.keys()}"
    users = data["data"]
    assert isinstance(users, list), f"'data' is not a list: {type(users)}"
    assert len(users) > 0, "No users returned in response."
    # At least one user should have an "id" field
    assert any("id" in user for user in users), "No user in response contains an 'id' field."
