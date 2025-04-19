import typing

import httpx

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.memory import MemoryProvider

_T = typing.TypeVar("_T")


def make_request_with_config(
    config: ClientConfig,
    auth_strategy: AuthStrategy,
    mock_server_url: str,
    path: str,
    method: str = "GET",
    **kwargs: typing.Any,
) -> httpx.Response:
    """Internal implementation for make_request_with_config."""
    base_url = mock_server_url.rstrip("/")
    url = f"{base_url}/{path.lstrip('/')}"

    headers = kwargs.pop("headers", {})
    params = kwargs.pop("params", {})
    data = kwargs.pop("data", None)
    json_data = kwargs.pop("json", None)

    # Prepare request using auth strategy
    prepared_headers, prepared_params = auth_strategy.prepare_request(
        headers=headers, params=params
    )

    # Use httpx for the actual request
    with httpx.Client(
        base_url=base_url,
        timeout=config.timeout,
        follow_redirects=True,  # Typically desired in tests
    ) as client:
        response = client.request(
            method=method,
            url=url,
            headers=prepared_headers,
            params=prepared_params,
            data=data,
            json=json_data,
            **kwargs,
        )
    return response


def setup_multi_provider_manager(
    config_sources: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]]
) -> ConfigManager:
    """Internal implementation for setup_multi_provider_manager."""
    providers = []
    for name, data in config_sources:
        providers.append(MemoryProvider(data=data, name=name))
    return ConfigManager(providers=providers)
