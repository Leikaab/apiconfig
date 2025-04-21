# tests/unit/testing/unit/mocks/test_auth.py
import pytest

from apiconfig.auth.base import AuthStrategy
from apiconfig.auth.strategies import ApiKeyAuth, BasicAuth, BearerAuth, CustomAuth
from apiconfig.exceptions.auth import AuthenticationError
from apiconfig.testing.unit.mocks.auth import MockApiKeyAuth, MockAuthStrategy, MockBasicAuth, MockBearerAuth, MockCustomAuth


def test_mock_auth_strategy_inheritance() -> None:
    """Verify MockAuthStrategy inherits from AuthStrategy."""
    assert issubclass(MockAuthStrategy, AuthStrategy)


def test_mock_auth_strategy_initialization() -> None:
    """Test initialization of MockAuthStrategy."""
    mock_auth = MockAuthStrategy()
    assert mock_auth.override_headers == {}
    assert mock_auth.override_params == {}
    assert mock_auth.raise_exception is None

    headers = {"X-Test": "Header"}
    params = {"test": "param"}
    exception = AuthenticationError("Test Error")
    mock_auth = MockAuthStrategy(
        override_headers=headers,
        override_params=params,
        raise_exception=exception,
    )
    assert mock_auth.override_headers == headers
    assert mock_auth.override_params == params
    assert mock_auth.raise_exception == exception


def test_mock_auth_strategy_prepare_request_no_overrides() -> None:
    """Test prepare_request with no overrides."""
    mock_auth = MockAuthStrategy()
    original_headers = {"Authorization": "Original"}
    original_params = {"key": "original"}
    headers, params = mock_auth.prepare_request(headers=original_headers.copy(), params=original_params.copy())
    assert headers == original_headers
    assert params == original_params


def test_mock_auth_strategy_prepare_request_with_overrides() -> None:
    """Test prepare_request applies overrides correctly."""
    override_headers = {"Authorization": "Override", "X-New": "Value"}
    override_params = {"key": "override", "new": "val"}
    mock_auth = MockAuthStrategy(override_headers=override_headers, override_params=override_params)

    original_headers = {"Authorization": "Original", "Keep-Me": "Yes"}
    original_params = {"key": "original", "keep": "yes"}

    headers, params = mock_auth.prepare_request(headers=original_headers.copy(), params=original_params.copy())

    expected_headers = {"Keep-Me": "Yes", "Authorization": "Override", "X-New": "Value"}
    expected_params = {"keep": "yes", "key": "override", "new": "val"}

    assert headers == expected_headers
    assert params == expected_params


def test_mock_auth_strategy_prepare_request_raises_exception() -> None:
    """Test prepare_request raises the configured exception."""
    exception_to_raise = AuthenticationError("Configured Error")
    mock_auth = MockAuthStrategy(raise_exception=exception_to_raise)

    with pytest.raises(AuthenticationError, match="Configured Error"):
        mock_auth.prepare_request()


def test_mock_basic_auth_inheritance() -> None:
    """Verify MockBasicAuth inherits correctly."""
    assert issubclass(MockBasicAuth, MockAuthStrategy)
    assert issubclass(MockBasicAuth, BasicAuth)


def test_mock_basic_auth_prepare_request() -> None:
    """Test MockBasicAuth prepare_request behavior (delegates to base mock)."""
    override_headers = {"Authorization": "Basic Mocked"}
    mock_auth = MockBasicAuth(override_headers=override_headers)
    headers, params = mock_auth.prepare_request(headers={})
    assert headers == override_headers
    assert params == {}


def test_mock_bearer_auth_inheritance() -> None:
    """Verify MockBearerAuth inherits correctly."""
    assert issubclass(MockBearerAuth, MockAuthStrategy)
    assert issubclass(MockBearerAuth, BearerAuth)


def test_mock_bearer_auth_prepare_request() -> None:
    """Test MockBearerAuth prepare_request behavior (delegates to base mock)."""
    override_headers = {"Authorization": "Bearer Mocked"}
    mock_auth = MockBearerAuth(override_headers=override_headers)
    headers, params = mock_auth.prepare_request(headers={})
    assert headers == override_headers
    assert params == {}


def test_mock_api_key_auth_inheritance() -> None:
    """Verify MockApiKeyAuth inherits correctly."""
    assert issubclass(MockApiKeyAuth, MockAuthStrategy)
    assert issubclass(MockApiKeyAuth, ApiKeyAuth)


def test_mock_api_key_auth_prepare_request() -> None:
    """Test MockApiKeyAuth prepare_request behavior (delegates to base mock)."""
    override_params = {"api_key": "mocked_key"}
    mock_auth = MockApiKeyAuth(override_params=override_params)
    headers, params = mock_auth.prepare_request(params={})
    assert headers == {}
    assert params == override_params


def test_mock_custom_auth_inheritance() -> None:
    """Verify MockCustomAuth inherits correctly."""
    assert issubclass(MockCustomAuth, MockAuthStrategy)
    assert issubclass(MockCustomAuth, CustomAuth)


def test_mock_custom_auth_prepare_request() -> None:
    """Test MockCustomAuth prepare_request behavior (delegates to base mock)."""
    override_headers = {"X-Custom": "Mocked"}
    mock_auth = MockCustomAuth(override_headers=override_headers)
    headers, params = mock_auth.prepare_request(headers={})
    assert headers == override_headers
    assert params == {}
