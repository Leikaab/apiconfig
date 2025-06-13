"""
Unit tests for apiconfig.testing.unit.helpers.

Covers: check_auth_strategy_interface, assert_auth_header_correct, temp_env_vars,
temp_config_file, assert_provider_loads, BaseAuthStrategyTest, BaseConfigProviderTest.
"""

import os
from typing import Any, Dict, Optional, Type, cast

import pytest

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions import AuthenticationError
from apiconfig.testing.unit import helpers
from apiconfig.testing.unit.helpers import ConfigProviderProtocol


class DummyAuthStrategy(AuthStrategy):
    """Dummy AuthStrategy implementing AuthStrategy interface for testing."""

    def prepare_request(self, *args: Any, **kwargs: Any) -> None:
        pass

    def prepare_request_headers(self) -> Dict[str, str]:
        return {}

    def prepare_request_params(self) -> Dict[str, str]:
        return {}


class DummyAuthStrategyNonCallable:
    """Dummy AuthStrategy with non-callable prepare_request."""

    prepare_request: int = 123


class DummyAuthStrategyMissing:
    """Dummy AuthStrategy missing prepare_request."""


class DummyAuthStrategyHeaders(DummyAuthStrategy):
    """Dummy AuthStrategy with prepare_request_headers."""

    def __init__(self, headers: Dict[str, str]) -> None:
        self._headers = headers

    def prepare_request_headers(self) -> Dict[str, str]:
        return self._headers


class DummyAuthStrategyRaises(DummyAuthStrategy):
    """Dummy AuthStrategy whose prepare_request_headers raises AuthenticationError."""

    def prepare_request_headers(self) -> Dict[str, str]:
        raise AuthenticationError("auth failed")


class DummyProvider:
    """Dummy config provider for testing."""

    def __init__(self, to_return: Any = None, to_raise: Optional[Exception] = None) -> None:
        self._to_return = to_return
        self._to_raise = to_raise

    def load(self) -> Any:
        if self._to_raise:
            raise self._to_raise
        return self._to_return


def test_check_auth_strategy_interface_pass() -> None:
    """
    Test check_auth_strategy_interface passes for object with callable prepare_request.
    """
    helpers.check_auth_strategy_interface(DummyAuthStrategy())


def test_check_auth_strategy_interface_missing_method() -> None:
    """
    Test check_auth_strategy_interface fails if prepare_request is missing.
    """
    with pytest.raises(AssertionError, match="must have a 'prepare_request'"):
        helpers.check_auth_strategy_interface(DummyAuthStrategyMissing())


def test_check_auth_strategy_interface_non_callable() -> None:
    """
    Test check_auth_strategy_interface fails if prepare_request is not callable.
    """
    with pytest.raises(AssertionError, match="must be callable"):
        helpers.check_auth_strategy_interface(DummyAuthStrategyNonCallable())


def test_assert_auth_header_correct_success() -> None:
    """
    Test assert_auth_header_correct passes when header and value are correct.
    """
    strat = DummyAuthStrategyHeaders({"Authorization": "Bearer token"})
    helpers.assert_auth_header_correct(strat, "Authorization", "Bearer token")


def test_assert_auth_header_correct_missing_header() -> None:
    """
    Test assert_auth_header_correct fails if header is missing.
    """
    strat = DummyAuthStrategyHeaders({"X-Other": "val"})
    with pytest.raises(AssertionError, match="not found"):
        helpers.assert_auth_header_correct(strat, "Authorization", "Bearer token")


def test_assert_auth_header_correct_wrong_value() -> None:
    """
    Test assert_auth_header_correct fails if header value is wrong.
    """
    strat = DummyAuthStrategyHeaders({"Authorization": "wrong"})
    with pytest.raises(AssertionError, match="has value 'wrong', expected 'Bearer token'"):
        helpers.assert_auth_header_correct(strat, "Authorization", "Bearer token")


def test_assert_auth_header_correct_auth_error() -> None:
    """
    Test assert_auth_header_correct raises AssertionError if prepare_request_headers raises AuthenticationError.
    """
    strat = DummyAuthStrategyRaises()
    with pytest.raises(AssertionError, match="Strategy raised unexpected AuthenticationError"):
        helpers.assert_auth_header_correct(strat, "Authorization", "Bearer token")


def test_temp_env_vars_sets_and_restores(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test temp_env_vars sets new vars, overrides existing, and restores original values.
    """
    key_new = "TEST_TEMP_ENV_NEW"
    key_existing = "TEST_TEMP_ENV_EXISTING"
    orig_value = "orig"
    monkeypatch.setenv(key_existing, orig_value)
    assert os.environ.get(key_new) is None
    assert os.environ[key_existing] == orig_value

    with helpers.temp_env_vars({key_new: "val1", key_existing: "val2"}):
        assert os.environ[key_new] == "val1"
        assert os.environ[key_existing] == "val2"
    # After context, new var is gone, existing is restored
    assert key_new not in os.environ
    assert os.environ[key_existing] == orig_value


def test_temp_env_vars_unsets(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test temp_env_vars unsets variables that were not originally present.
    """
    key = "TEST_TEMP_ENV_UNSET"
    if key in os.environ:
        monkeypatch.delenv(key)
    with helpers.temp_env_vars({key: "foo"}):
        assert os.environ[key] == "foo"
    assert key not in os.environ


def test_temp_config_file_creates_and_removes() -> None:
    """
    Test temp_config_file creates a file with correct content and suffix, and removes it after exit.
    """
    content = "abc123"
    suffix = ".test"
    with helpers.temp_config_file(content, suffix) as path:
        assert os.path.exists(path)
        assert path.endswith(suffix)
        with open(path) as f:
            assert f.read() == content
    # File should be removed
    assert not os.path.exists(path)


def test_assert_provider_loads_success() -> None:
    """
    Test assert_provider_loads passes when provider returns expected config.
    """
    expected = {"a": 1}
    provider = DummyProvider(to_return=expected)
    helpers.assert_provider_loads(provider, expected)


def test_assert_provider_loads_mismatch() -> None:
    """
    Test assert_provider_loads fails if loaded config does not match expected.
    """
    provider = DummyProvider(to_return={"a": 2})
    with pytest.raises(AssertionError, match="Provider loaded"):
        helpers.assert_provider_loads(provider, {"a": 1})


def test_assert_provider_loads_raises() -> None:
    """
    Test assert_provider_loads fails if provider.load() raises Exception.
    """
    provider = DummyProvider(to_raise=RuntimeError("fail"))
    with pytest.raises(AssertionError, match="raised unexpected error during load"):
        helpers.assert_provider_loads(provider, {"a": 1})


def test_base_auth_strategy_test_setUpClass_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test BaseAuthStrategyTest.setUpClass passes if subclass defines valid strategy.
    """

    class SubTest(helpers.BaseAuthStrategyTest):
        pass

    # Assign strategy to the class before calling setUpClass
    SubTest.strategy = DummyAuthStrategy()

    # Should not raise
    SubTest.setUpClass()


def test_base_auth_strategy_test_setUpClass_not_implemented() -> None:
    """
    Test BaseAuthStrategyTest.setUpClass raises if subclass does not define strategy.
    """

    class SubTest(helpers.BaseAuthStrategyTest):
        pass

    with pytest.raises(NotImplementedError, match="must define a class attribute 'strategy'"):
        SubTest.setUpClass()


def test_base_auth_strategy_test_setUpClass_wrong_type() -> None:
    """
    Test BaseAuthStrategyTest.setUpClass raises if strategy is not AuthStrategy instance.
    """

    class SubTest(helpers.BaseAuthStrategyTest):
        strategy = object()  # type: ignore

    with pytest.raises(AssertionError, match="prepare_request"):
        SubTest.setUpClass()


def test_base_config_provider_test_get_provider_instance_not_implemented() -> None:
    """
    Test BaseConfigProviderTest.get_provider_instance raises if provider_class is not set.
    """

    class SubTest(helpers.BaseConfigProviderTest):
        pass

    inst = SubTest()
    with pytest.raises(NotImplementedError, match="must define 'provider_class'"):
        inst.get_provider_instance()


def test_base_config_provider_test_config_file_raises_if_no_content() -> None:
    """
    Test BaseConfigProviderTest.config_file raises ValueError if no content is provided and config_content is None.
    """

    class SubTest(helpers.BaseConfigProviderTest):
        config_content = None

    inst = SubTest()
    with pytest.raises(ValueError, match="No content provided for temporary config file"):
        with inst.config_file():
            pass


# New tests to increase coverage


def test_config_provider_protocol_load_signature() -> None:
    """
    Test that ConfigProviderProtocol can be used for duck typing and its load method is present.
    This dummy test ensures coverage of the protocol ellipsis.
    """

    class Dummy(helpers.ConfigProviderProtocol):
        def load(self) -> Dict[str, Any]:
            return {"x": 1}

    d = Dummy()
    assert hasattr(d, "load")
    # Try to execute the load method to improve coverage
    result = d.load()
    assert result == {"x": 1}


def test_base_auth_strategy_test_setUpClass_on_base() -> None:
    """
    Test BaseAuthStrategyTest.setUpClass returns early when called on the base class itself.
    """
    # Should not raise or do anything
    helpers.BaseAuthStrategyTest.setUpClass()


def test_base_auth_strategy_test_assertAuthHeaderCorrect() -> None:
    """
    Test BaseAuthStrategyTest.assertAuthHeaderCorrect method.
    """

    class SubTest(helpers.BaseAuthStrategyTest):
        strategy = DummyAuthStrategyHeaders({"Authorization": "Bearer test"})

    inst = SubTest()
    inst.assertAuthHeaderCorrect("Authorization", "Bearer test")


def test_base_config_provider_test_get_provider_instance_with_class() -> None:
    """
    Test BaseConfigProviderTest.get_provider_instance when provider_class is set.
    """

    class DummyProviderClass:
        def __init__(self, x: int = 1) -> None:
            self.x = x

        def load(self) -> Dict[str, Any]:
            return {"x": self.x}

    class SubTest(helpers.BaseConfigProviderTest):
        provider_class = cast(Type[ConfigProviderProtocol], DummyProviderClass)

    inst = SubTest()
    provider = inst.get_provider_instance(5)
    assert provider.load() == {"x": 5}


def test_base_config_provider_test_env_vars_merges(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test BaseConfigProviderTest.env_vars merges vars_to_set and required_env_vars.
    """

    class SubTest(helpers.BaseConfigProviderTest):
        required_env_vars = {"ENV1": "A"}

    inst = SubTest()
    monkeypatch.delenv("ENV1", raising=False)
    monkeypatch.delenv("ENV2", raising=False)

    with inst.env_vars({"ENV2": "B"}):
        assert os.environ["ENV1"] == "A"
        assert os.environ["ENV2"] == "B"

    assert "ENV1" not in os.environ or os.environ["ENV1"] != "A"
    assert "ENV2" not in os.environ


def test_base_config_provider_test_config_file_variants() -> None:
    """
    Test BaseConfigProviderTest.config_file with content, config_content, suffix, and config_suffix.
    """

    class SubTest(helpers.BaseConfigProviderTest):
        config_content = "abc"
        config_suffix = ".foo"

    inst = SubTest()

    # Test with explicit content and suffix
    with inst.config_file(content="xyz", suffix=".bar") as path:
        assert os.path.exists(path)
        with open(path) as f:
            assert f.read() == "xyz"
        assert path.endswith(".bar")

    # Test with config_content and config_suffix
    with inst.config_file() as path:
        assert os.path.exists(path)
        with open(path) as f:
            assert f.read() == "abc"
        assert path.endswith(".foo")


def test_base_config_provider_test_assertProviderLoads() -> None:
    """
    Test BaseConfigProviderTest.assertProviderLoads method.
    """

    class Dummy(helpers.ConfigProviderProtocol):
        def load(self) -> Dict[str, Any]:
            return {"a": 1}

    class SubTest(helpers.BaseConfigProviderTest):
        pass

    inst = SubTest()
    inst.assertProviderLoads(Dummy(), {"a": 1})
