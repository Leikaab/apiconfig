import typing
import httpx

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager

_T = typing.TypeVar("_T")


def make_request_with_config(
    config: ClientConfig,
    auth_strategy: AuthStrategy,
    mock_server_url: str,
    path: str,
    method: str = "GET",
    **kwargs: typing.Any,
) -> httpx.Response:
    """
    Makes an HTTP request to a mock server using the provided config and auth strategy.

    This helper encapsulates the common pattern of preparing a request with an
    authentication strategy and sending it using an HTTP client (httpx).

    Args:
        config: The ClientConfig instance to use (e.g., for timeout).
        auth_strategy: The AuthStrategy to apply to the request.
        mock_server_url: The base URL of the mock server.
        path: The specific path for the request endpoint.
        method: The HTTP method (e.g., "GET", "POST"). Defaults to "GET".
        **kwargs: Additional keyword arguments passed directly to `httpx.Client.request`.

    Returns:
        The httpx.Response object from the mock server.
    """
    ...


def setup_multi_provider_manager(
    config_sources: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]]
) -> ConfigManager:
    """
    Sets up a ConfigManager with multiple in-memory providers.

    This helper simplifies the creation of a ConfigManager populated with
    several MemoryProvider instances, useful for testing configuration merging
    or complex scenarios.

    Args:
        config_sources: A list of tuples, where each tuple contains a provider
                        name (str) and a dictionary (Dict[str, Any]) representing
                        the configuration data for that provider.

    Returns:
        A ConfigManager instance initialized with the specified providers.
    """
    ...
