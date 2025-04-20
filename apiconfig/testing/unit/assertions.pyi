# -*- coding: utf-8 -*-
# mypy: disable-error-code="empty-body"
"""Type stubs for custom assertion functions."""

from typing import Any, Dict

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig

# No common base class found for providers, using Any.
# A Protocol could be defined later if needed.
ConfigProvider = Any

def assert_client_config_valid(config: ClientConfig) -> None:
    """
    Assert that a ClientConfig instance appears valid.

    Checks for correct type, non-empty hostname, non-negative timeout/retries,
    and successful base_url construction.

    Args:
        config: The ClientConfig instance to validate.

    Raises:
        AssertionError: If the config is invalid.
    """
    ...

def assert_auth_header_correct(
    strategy: AuthStrategy, expected_header: Dict[str, str]
) -> None:
    """
    Assert that the AuthStrategy produces the expected headers.

    Calls the strategy's `prepare_request_headers()` method and compares
    the result to the expected dictionary.

    Args:
        strategy: The AuthStrategy instance to test.
        expected_header: The dictionary of headers the strategy should produce.

    Raises:
        AssertionError: If the actual headers do not match the expected headers,
                      or if the strategy is not a valid AuthStrategy instance.
    """
    ...

def assert_provider_loads(
    provider: ConfigProvider, expected_dict: Dict[str, Any]
) -> None:
    """
    Assert that the ConfigProvider loads the expected dictionary.

    Calls the provider's `load()` method and compares the result to the
    expected dictionary.

    Args:
        provider: The configuration provider instance to test. Must have a
                  callable `load()` method.
        expected_dict: The dictionary the provider should load.

    Raises:
        AssertionError: If the actual dictionary does not match the expected
                      dictionary, or if the provider does not have a callable
                      `load()` method.
    """
    ...
