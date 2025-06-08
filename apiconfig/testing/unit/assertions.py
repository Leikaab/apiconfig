# -*- coding: utf-8 -*-
"""Custom assertion functions for apiconfig unit tests."""

from typing import TYPE_CHECKING, Any, Dict

# Import specific provider types if needed, or use Any/Protocol
# from apiconfig.config.providers.env import EnvProvider
# from apiconfig.config.providers.file import FileProvider
# from apiconfig.config.providers.memory import MemoryProvider

if TYPE_CHECKING:
    from apiconfig.auth.base import AuthStrategy
    from apiconfig.config.base import ClientConfig

    # No common base class found, using Any for provider type hint
    ConfigProvider = Any


def assert_client_config_valid(config: "ClientConfig") -> None:
    """
    Assert that a ClientConfig instance appears valid.

    Checks for correct type, non-empty hostname, non-negative timeout/retries,
    and successful base_url construction.

    Parameters
    ----------
    config : ClientConfig
        The ClientConfig instance to validate.

    Raises
    ------
    AssertionError
        If the config is invalid.
    """
    # Import locally to avoid potential circular dependency issues
    from apiconfig.config.base import ClientConfig

    if not isinstance(config, ClientConfig):
        raise AssertionError(f"Object {config!r} is not an instance of ClientConfig.")
    if not config.hostname:
        raise AssertionError("ClientConfig hostname cannot be empty or None.")
    if config.timeout is not None and config.timeout < 0:
        raise AssertionError(f"ClientConfig timeout cannot be negative: {config.timeout}")
    if config.retries is not None and config.retries < 0:
        raise AssertionError(f"ClientConfig retries cannot be negative: {config.retries}")
    # Implicitly check base_url construction works
    try:
        _ = config.base_url
    except Exception as e:
        raise AssertionError(f"ClientConfig failed base_url construction: {e}")


def assert_auth_header_correct(strategy: "AuthStrategy", expected_header: Dict[str, str]) -> None:
    """
    Assert that the AuthStrategy produces the expected headers.

    Calls the strategy's `prepare_request_headers()` method and compares
    the result to the expected dictionary.

    Parameters
    ----------
    strategy : AuthStrategy
        The AuthStrategy instance to test.
    expected_header : Dict[str, str]
        The dictionary of headers the strategy should produce.

    Raises
    ------
    AssertionError
        If the actual headers do not match the expected headers,
        or if the strategy is not a valid AuthStrategy instance.
    """
    # Import locally if needed
    from apiconfig.auth.base import AuthStrategy

    if not isinstance(strategy, AuthStrategy):
        raise AssertionError(f"Object {strategy!r} is not an instance of AuthStrategy.")

    actual_header = strategy.prepare_request_headers()
    assert actual_header == expected_header, f"Auth header mismatch. Expected: {expected_header}, Got: {actual_header}"


def assert_provider_loads(provider: "ConfigProvider", expected_dict: Dict[str, Any]) -> None:
    """
    Assert that the ConfigProvider loads the expected dictionary.

    Calls the provider's `load()` method and compares the result to the
    expected dictionary.

    Parameters
    ----------
    provider : ConfigProvider
        The configuration provider instance to test. Must have a
        callable `load()` method.
    expected_dict : Dict[str, Any]
        The dictionary the provider should load.

    Raises
    ------
    AssertionError
        If the actual dictionary does not match the expected
        dictionary, or if the provider does not have a callable
        `load()` method.
    """
    # Check if the provider has a 'load' method
    if not hasattr(provider, "load") or not callable(provider.load):
        raise AssertionError(f"Object {provider!r} does not have a callable 'load' method.")

    actual_dict = provider.load()
    assert actual_dict == expected_dict, f"Provider load mismatch. Expected: {expected_dict}, Got: {actual_dict}"
