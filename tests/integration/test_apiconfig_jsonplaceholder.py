import os
from typing import Any, Dict

import httpx

from apiconfig.config.base import ClientConfig
from apiconfig.config.providers.env import EnvProvider


def test_jsonplaceholder_get_post_1() -> None:
    """
    Integration test: GET /posts/1 from jsonplaceholder API using apiconfig EnvProvider and ClientConfig.
    Asserts status code 200 and required fields in the response.
    """
    # Load base URL from environment using EnvProvider (default if not set)
    env = EnvProvider(prefix="")
    env_vars: Dict[str, Any] = env.load()
    base_url: str = env_vars.get(
        "JSONPLACEHOLDER_BASE_URL",
        os.environ.get(
            "JSONPLACEHOLDER_BASE_URL", "https://jsonplaceholder.typicode.com"
        ),
    )

    # Set up API config (no auth required)
    config = ClientConfig(hostname=base_url)

    # Compose endpoint URL
    url = f"{config.base_url}/posts/1"

    # Make real HTTP GET request
    with httpx.Client(timeout=10.0) as client:
        response = client.get(url)

    # Assert status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Parse and validate response JSON
    data: Dict[str, Any] = response.json()
    for field in ("userId", "id", "title", "body"):
        assert field in data, f"Missing field '{field}' in response: {data}"

    # Optionally, check types of fields for robustness/extensibility
    assert isinstance(data["userId"], int)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)
