import contextlib
import unittest
from typing import Any, Dict, Generator, Optional, Protocol, Type

from apiconfig.auth.base import AuthStrategy
# Removed direct import of ConfigProvider
from apiconfig.exceptions import AuthenticationError

# Define a Protocol for duck typing ConfigProvider
class ConfigProviderProtocol(Protocol):
    def load(self) -> Dict[str, Any]: ...

def check_auth_strategy_interface(strategy_instance: Any) -> None:
    """
    Verifies that an object implements the basic AuthStrategy interface.

    Raises:
        AssertionError: If the object does not have the required methods.
    """
    ...

def assert_auth_header_correct(
    strategy: AuthStrategy, expected_header: str, expected_value: str
) -> None:
    """
    Asserts that the strategy adds the correct authorization header.

    Args:
        strategy: The AuthStrategy instance to test.
        expected_header: The name of the expected header (e.g., "Authorization").
        expected_value: The expected value of the header.

    Raises:
        AssertionError: If the header is missing or has an incorrect value.
        AuthenticationError: If the strategy raises an auth error during preparation.
    """
    ...

@contextlib.contextmanager
def temp_env_vars(vars_to_set: Dict[str, str]) -> Generator[None, None, None]:
    """
    Context manager to temporarily set environment variables.

    Args:
        vars_to_set: A dictionary where keys are variable names and values are
                     the values to set.
    """
    ...

@contextlib.contextmanager
def temp_config_file(content: str, suffix: str = ".tmp") -> Generator[str, None, None]:
    """
    Context manager to create a temporary file with given content.

    Args:
        content: The string content to write to the file.
        suffix: The suffix for the temporary file (e.g., '.json', '.yaml').

    Yields:
        The path to the temporary file.
    """
    ...

def assert_provider_loads(
    provider: ConfigProviderProtocol, expected_config: Dict[str, Any]
) -> None:
    """
    Asserts that a configuration provider-like object loads the expected dictionary.

    Args:
        provider: An object implementing the ConfigProviderProtocol (i.e., has a load() method).
        expected_config: The dictionary the provider is expected to load.

    Raises:
        AssertionError: If the loaded config does not match the expected config.
        Exception: If the provider raises an unexpected error during loading.
    """
    ...

class BaseAuthStrategyTest(unittest.TestCase):
    """
    Optional base class for testing AuthStrategy implementations using unittest.

    Subclasses should override `get_strategy_instance` to provide the
    strategy they want to test.
    """

    strategy: AuthStrategy

    @classmethod
    def setUpClass(cls) -> None: ...
    def assertAuthHeaderCorrect(
        self, expected_header: str, expected_value: str
    ) -> None:
        """Asserts the strategy adds the correct authorization header."""
        ...

class BaseConfigProviderTest(unittest.TestCase):
    """
    Optional base class for testing ConfigProvider implementations using unittest.

    Provides helper context managers for temporary environments.
    """

    provider_class: Optional[Type[ConfigProviderProtocol]]
    required_env_vars: Optional[Dict[str, str]]
    config_content: Optional[str]
    config_suffix: str

    def get_provider_instance(
        self, *args: Any, **kwargs: Any
    ) -> ConfigProviderProtocol:
        """Instantiates the provider_class."""
        ...

    @contextlib.contextmanager
    def env_vars(
        self, vars_to_set: Optional[Dict[str, str]] = ...
    ) -> Generator[None, None, None]:
        """Context manager for temporary environment variables."""
        ...

    @contextlib.contextmanager
    def config_file(
        self, content: Optional[str] = ..., suffix: Optional[str] = ...
    ) -> Generator[str, None, None]:
        """Context manager for a temporary configuration file."""
        ...

    def assertProviderLoads(
        self, provider: ConfigProviderProtocol, expected_config: Dict[str, Any]
    ) -> None:
        """Asserts the provider loads the expected configuration."""
        ...
