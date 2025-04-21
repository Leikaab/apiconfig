import contextlib
import os
import tempfile
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
    assert hasattr(
        strategy_instance, "prepare_request"
    ), "Strategy instance must have a 'prepare_request' method."
    assert callable(
        strategy_instance.prepare_request
    ), "'prepare_request' must be callable."


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
    headers: Dict[str, str] = {}
    params: Dict[str, Any] = {}
    data: Optional[Any] = None

    try:
        strategy.prepare_request(headers, params, data)
    except AuthenticationError as e:
        raise AssertionError(
            f"Strategy raised unexpected AuthenticationError: {e}"
        ) from e

    assert (
        expected_header in headers
    ), f"Expected header '{expected_header}' not found in {headers}."
    assert (
        headers[expected_header] == expected_value
    ), f"Header '{expected_header}' has value '{headers[expected_header]}', expected '{expected_value}'."


@contextlib.contextmanager
def temp_env_vars(vars_to_set: Dict[str, str]) -> Generator[None, None, None]:
    """
    Context manager to temporarily set environment variables.

    Args:
        vars_to_set: A dictionary where keys are variable names and values are
                     the values to set.
    """
    original_values: Dict[str, Optional[str]] = {}
    try:
        for key, value in vars_to_set.items():
            original_values[key] = os.environ.get(key)
            os.environ[key] = value
        yield
    finally:
        for key, original_value in original_values.items():
            if original_value is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = original_value


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
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, "w") as tmp:
            tmp.write(content)
        yield path
    finally:
        os.remove(path)


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
    try:
        loaded_config = provider.load()
    except Exception as e:
        raise AssertionError(
            f"Provider '{type(provider).__name__}' raised unexpected error during load: {e}"
        ) from e

    assert (
        loaded_config == expected_config
    ), f"Provider loaded {loaded_config}, expected {expected_config}."


# --- Base Test Classes (Optional - Use Mixins or Helpers directly) ---

# Note: Using helper functions/context managers directly or creating mixins
# is often more flexible than requiring inheritance from a specific base class.
# These are provided as examples if a TestCase structure is preferred.


class BaseAuthStrategyTest(unittest.TestCase):
    """
    Optional base class for testing AuthStrategy implementations using unittest.

    Subclasses should override `get_strategy_instance` to provide the
    strategy they want to test.
    """

    strategy: AuthStrategy

    @classmethod
    def setUpClass(cls) -> None:
        """Ensures subclasses provide a strategy."""
        if cls is BaseAuthStrategyTest:
            return  # Skip setup for the base class itself
        if not hasattr(cls, "strategy") or not isinstance(cls.strategy, AuthStrategy):
            raise NotImplementedError(
                f"{cls.__name__} must define a class attribute 'strategy' "
                "of type AuthStrategy."
            )
        check_auth_strategy_interface(cls.strategy)

    def assertAuthHeaderCorrect(
        self, expected_header: str, expected_value: str
    ) -> None:
        """Asserts the strategy adds the correct authorization header."""
        assert_auth_header_correct(self.strategy, expected_header, expected_value)


class BaseConfigProviderTest(unittest.TestCase):
    """
    Optional base class for testing ConfigProvider implementations using unittest.

    Provides helper context managers for temporary environments.
    """

    provider_class: Optional[Type[ConfigProviderProtocol]] = None
    required_env_vars: Optional[Dict[str, str]] = None
    config_content: Optional[str] = None
    config_suffix: str = ".tmp"

    def get_provider_instance(
        self, *args: Any, **kwargs: Any
    ) -> ConfigProviderProtocol:
        """Instantiates the provider_class."""
        if self.provider_class is None:
            raise NotImplementedError(
                f"{type(self).__name__} must define 'provider_class'."
            )
        return self.provider_class(*args, **kwargs)

    @contextlib.contextmanager
    def env_vars(
        self, vars_to_set: Optional[Dict[str, str]] = None
    ) -> Generator[None, None, None]:
        """Context manager for temporary environment variables."""
        actual_vars = vars_to_set if vars_to_set is not None else {}
        if self.required_env_vars:
            actual_vars.update(self.required_env_vars)
        with temp_env_vars(actual_vars):
            yield

    @contextlib.contextmanager
    def config_file(
        self, content: Optional[str] = None, suffix: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Context manager for a temporary configuration file."""
        actual_content = content if content is not None else self.config_content
        actual_suffix = suffix if suffix is not None else self.config_suffix
        if actual_content is None:
            raise ValueError("No content provided for temporary config file.")
        with temp_config_file(actual_content, actual_suffix) as path:
            yield path

    def assertProviderLoads(
        self, provider: ConfigProviderProtocol, expected_config: Dict[str, Any]
    ) -> None:
        """Asserts the provider loads the expected configuration."""
        assert_provider_loads(provider, expected_config)
