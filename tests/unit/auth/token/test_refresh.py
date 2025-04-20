from apiconfig.exceptions.auth import TokenRefreshError
from apiconfig.auth.token.refresh import refresh_oauth2_token
from typing import Any
import pytest


class TestRefreshOAuth2Token:
    """Tests for the refresh_oauth2_token function."""

    def test_refresh_oauth2_token_raises_not_implemented(self) -> None:
        """Test that refresh_oauth2_token raises TokenRefreshError as it's a placeholder."""
        with pytest.raises(TokenRefreshError, match="not implemented yet"):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token"
            )

    def test_refresh_oauth2_token_constructs_payload_correctly(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that refresh_oauth2_token constructs the payload correctly."""
        # Mock the print function to capture the payload
        captured_output = []

        def mock_print(message: Any) -> None:
            captured_output.append(message)

        monkeypatch.setattr("builtins.print", mock_print)

        # The function will still raise TokenRefreshError, but we can check the payload
        # construction via the print statement
        with pytest.raises(TokenRefreshError):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
                client_id="test_client_id",
                client_secret="test_client_secret",
                extra_params={"scope": "read write"}
            )

        # Check that the print statement was called with the expected payload
        assert len(captured_output) == 1
        output = captured_output[0]
        assert "test_refresh_token" in output
        assert "https://example.com/token" in output
        assert "test_client_id" in output
        assert "test_client_secret" in output
        assert "scope" in output
        assert "read write" in output

    def test_refresh_oauth2_token_minimal_payload(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that refresh_oauth2_token works with minimal parameters."""
        captured_output = []

        def mock_print(message: Any) -> None:
            captured_output.append(message)

        monkeypatch.setattr("builtins.print", mock_print)

        with pytest.raises(TokenRefreshError):
            refresh_oauth2_token(
                refresh_token="minimal_token",
                token_url="https://example.com/token"
            )

        # Check that the print statement was called with the expected payload
        assert len(captured_output) == 1
        output = captured_output[0]
        assert "minimal_token" in output
        assert "https://example.com/token" in output
        assert "grant_type" in output
        assert "refresh_token" in output
        # These should not be in the payload
        assert "client_id" not in output or "client_id': None" in output
        assert "client_secret" not in output or "client_secret': None" in output

    def test_refresh_oauth2_token_with_client_id_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that refresh_oauth2_token works with only client_id."""
        captured_output = []

        def mock_print(message: Any) -> None:
            captured_output.append(message)

        monkeypatch.setattr("builtins.print", mock_print)

        with pytest.raises(TokenRefreshError):
            refresh_oauth2_token(
                refresh_token="token_with_client_id",
                token_url="https://example.com/token",
                client_id="test_client_id"
            )

        # Check that the print statement was called with the expected payload
        assert len(captured_output) == 1
        output = captured_output[0]
        assert "token_with_client_id" in output
        assert "test_client_id" in output
        assert "client_secret" not in output or "client_secret': None" in output

    def test_refresh_oauth2_token_with_extra_params_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that refresh_oauth2_token works with only extra_params."""
        captured_output = []

        def mock_print(message: Any) -> None:
            captured_output.append(message)

        monkeypatch.setattr("builtins.print", mock_print)

        with pytest.raises(TokenRefreshError):
            refresh_oauth2_token(
                refresh_token="token_with_extra",
                token_url="https://example.com/token",
                extra_params={"audience": "api://default", "scope": "profile"}
            )

        # Check that the print statement was called with the expected payload
        assert len(captured_output) == 1
        output = captured_output[0]
        assert "token_with_extra" in output
        assert "audience" in output
        assert "api://default" in output
        assert "scope" in output
        assert "profile" in output
