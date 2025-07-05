"""Tripletex session-based authentication strategy for apiconfig's contrib."""

import base64
import json
import logging as logging_mod
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Callable, Dict, Optional, cast

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import (
    AuthStrategyError,
    InvalidCredentialsError,
    MissingCredentialsError,
    TokenRefreshError,
)
from apiconfig.types import (
    HttpMethod,
    HttpRequestCallable,
    RefreshedTokenData,
    TokenRefreshResult,
)

if TYPE_CHECKING:
    pass

TRIPLETEX_TOKEN_CREATE_PATH = "/token/session/:create"


def _create_expiration_date() -> str:
    """
    Create an expiration date string for the session token.

    Sets the expiration date to two days ahead at 23:59:59 UTC to ensure
    it is always in the future, matching the pattern observed in tests.
    """
    two_days_ahead = (datetime.now(timezone.utc) + timedelta(days=2)).replace(hour=23, minute=59, second=59, microsecond=0)
    return two_days_ahead.strftime("%Y-%m-%dT%H:%M:%S.000Z")


class TripletexSessionAuth(AuthStrategy):
    """
    Authentication strategy for Tripletex using session tokens.

    Obtains a session token using a consumer token and an employee token.
    This session token is then used for Basic Authentication on subsequent
    requests, with the company ID as the username and the session token
    as the password.
    """

    def __init__(
        self,
        consumer_token: str,
        employee_token: str,
        company_id: str,
        session_token_hostname: str,
        token_api_version: Optional[str] = None,
        http_request_callable: Optional[HttpRequestCallable] = None,
    ):
        """
        Initialize TripletexSessionAuth with refresh capabilities.

        Args
        ----
        consumer_token : str
            The consumer token for Tripletex.
        employee_token : str
            The employee token for Tripletex.
        company_id : str
            The Tripletex company ID.
        session_token_hostname : str
            The hostname for the Tripletex token API
            (e.g., "https://api.tripletex.io" or
            "https://api-test.tripletex.tech").
        token_api_version : Optional[str]
            The API version for token creation (e.g., "v2").
            If None, no version path is prepended.
        http_request_callable : Optional[HttpRequestCallable]
            HTTP callable for making refresh requests.
        """
        super().__init__(http_request_callable)
        if not consumer_token:
            raise MissingCredentialsError("consumer_token cannot be empty.")
        if not employee_token:
            raise MissingCredentialsError("employee_token cannot be empty.")

        self.consumer_token = consumer_token
        self.employee_token = employee_token
        self.company_id = company_id
        self.session_token_hostname = session_token_hostname.rstrip("/")
        self.token_api_version = token_api_version.strip("/") if token_api_version else None
        self._session_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    @property
    def session_token(self) -> Optional[str]:
        """Return the currently cached session token."""
        return self._session_token

    @session_token.setter
    def session_token(self, value: Optional[str]) -> None:
        self._session_token = value

    @property
    def token_expires_at(self) -> Optional[datetime]:
        """Return the expiration datetime of the current session token."""
        return self._token_expires_at

    @token_expires_at.setter
    def token_expires_at(self, value: Optional[datetime]) -> None:
        self._token_expires_at = value

    def _get_session_token_url(self) -> str:
        """Construct the URL for fetching the session token."""
        path_prefix = ""
        if self.token_api_version:
            path_prefix = f"/{self.token_api_version}"
        return f"{self.session_token_hostname}{path_prefix}{TRIPLETEX_TOKEN_CREATE_PATH}"

    def _fetch_session_token(self) -> str:
        """Fetch a new session token from Tripletex."""
        token_url = self._get_session_token_url()
        params = {
            "consumerToken": self.consumer_token,
            "employeeToken": self.employee_token,
            "expirationDate": _create_expiration_date(),
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{token_url}?{query_string}"

        req = urllib.request.Request(full_url, method=HttpMethod.PUT.value)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                response_body_bytes = response.read()
                response_body_str = response_body_bytes.decode(response.headers.get_content_charset() or "utf-8", errors="ignore")
                if response.status == 200:
                    try:
                        response_data = json.loads(response_body_str)
                    except json.JSONDecodeError as e:
                        raise AuthStrategyError(
                            f"Failed to decode JSON response from token endpoint: {e}. " f"Response body: {response_body_str}"
                        ) from e

                    token_value_data_untyped = response_data.get("value")
                    if not isinstance(token_value_data_untyped, dict):
                        raise AuthStrategyError(
                            f"Unexpected 'value' format in token response: {token_value_data_untyped}. " f"Full response: {response_data}"
                        )

                    if "token" not in token_value_data_untyped:
                        raise AuthStrategyError(f"'token' missing from Tripletex response value: {token_value_data_untyped}.")

                    token_value_data = cast(Dict[str, object], token_value_data_untyped)
                    token_value_raw: object = token_value_data["token"]
                    if not isinstance(token_value_raw, str) or not token_value_raw:
                        raise AuthStrategyError(
                            "Session token not found, not a string, or empty in Tripletex response. "
                            f"'value.token' was: {token_value_raw!r}. Full response: {response_data}"
                        )

                    token_value: str = token_value_raw

                    # Set token expiration time (2 days from now)
                    self._token_expires_at = datetime.now(timezone.utc) + timedelta(days=2)

                    return token_value
                elif response.status in [401, 403]:
                    raise InvalidCredentialsError(
                        f"Failed to fetch Tripletex session token: {response.status} "
                        f"{response.reason}. Check consumer/employee tokens. "
                        f"Response: {response_body_str}"
                    )
                else:
                    raise AuthStrategyError(
                        f"Failed to fetch Tripletex session token: {response.status} " f"{response.reason}. Response: {response_body_str}"
                    )
        except urllib.error.HTTPError as e:  # Should be caught by status check above, but as fallback
            response_body = e.read().decode(errors="ignore") if hasattr(e, "read") else ""
            raise AuthStrategyError(f"HTTP error fetching Tripletex session token: {e.code} {e.reason}. " f"Response: {response_body}") from e
        except urllib.error.URLError as e:
            raise AuthStrategyError(f"URL error fetching Tripletex session token: {e.reason}") from e
        except Exception as e:  # Catch any other unexpected errors
            raise AuthStrategyError(f"Unexpected error fetching Tripletex session token: {e}") from e

    def can_refresh(self) -> bool:
        """Tripletex session tokens can be refreshed using consumer/employee tokens."""
        return self._http_request_callable is not None

    def is_expired(self) -> bool:
        """Check if session token is expired or close to expiring."""
        if self._token_expires_at is None:
            return True  # No token yet
        # Refresh 5 minutes before expiration
        return datetime.now(timezone.utc) >= (self._token_expires_at - timedelta(minutes=5))

    def refresh(self) -> Optional[TokenRefreshResult]:
        """Refresh the session token using consumer/employee tokens."""
        logger = logging_mod.getLogger(__name__)
        logger.debug("Starting token refresh")

        if not self.can_refresh():
            logger.debug("Cannot refresh: refresh not supported")
            return None

        try:
            old_token = self._session_token
            old_expires_at = self._token_expires_at

            # Use _fetch_session_token to get new session token
            new_token = self._fetch_session_token()
            self._session_token = new_token

            logger.debug(
                f"Token refresh completed: old_token={'[REDACTED]' if old_token else None}, new_token={'[REDACTED]' if new_token else None}, old_expires_at={old_expires_at}, new_expires_at={self._token_expires_at}"
            )

            # Return structured result for application persistence
            refreshed_token_data: RefreshedTokenData = {"access_token": new_token, "expires_in": 172800, "token_type": "session"}  # 2 days in seconds

            result: TokenRefreshResult = {"token_data": refreshed_token_data, "config_updates": None}

            return result

        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise TokenRefreshError(f"Failed to refresh Tripletex session token: {str(e)}") from e

    def get_refresh_callback(self) -> Optional[Callable[[], None]]:
        """Get callback function for crudclient-style refresh integration."""
        if self.can_refresh():

            def refresh_callback() -> None:
                self.refresh()

            return refresh_callback
        return None

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepare authentication headers for an HTTP request.

        Fetches a session token if not already available or if expired,
        and prepares the Basic Authentication header.
        """
        # Check if we need to refresh the token
        if self._session_token is None or self.is_expired():
            self._session_token = self._fetch_session_token()

        auth_string = f"{self.company_id}:{self._session_token}"
        encoded_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {encoded_auth_string}"}

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Prepare authentication parameters for an HTTP request.

        This strategy does not add any authentication-specific query parameters
        to regular API calls.
        """
        return {}

    def get_session_token(self) -> str:
        """
        Get the current session token, fetching one if necessary.

        Returns
        -------
        str
            The session token.

        Raises
        ------
        AuthStrategyError
            If there's an error fetching the session token.
        InvalidCredentialsError
            If the credentials are invalid.
        MissingCredentialsError
            If credentials are missing.
        """
        if self._session_token is None:
            self._session_token = self._fetch_session_token()
        return self._session_token

    def __repr__(self) -> str:
        """Return string representation of the auth strategy."""
        return (
            f"{self.__class__.__name__}("
            f"consumer_token='[REDACTED]', "
            f"employee_token='[REDACTED]', "
            f"company_id='{self.company_id}', "
            f"session_token_hostname='{self.session_token_hostname}', "
            f"token_api_version='{self.token_api_version}'"
            ")"
        )
