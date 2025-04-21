import base64
import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# This line was removed as the combined import was added at line 10
from typing import Any, Dict, List, Optional

import pytest
from dotenv import load_dotenv

from apiconfig.config.providers.env import EnvProvider

load_dotenv(dotenv_path=".env", override=True)  # Explicitly load .env from workspace root and override existing vars
# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
TRIPLETEX_TEST_HOSTNAME = "https://api-test.tripletex.tech"
TRIPLETEX_API_VERSION = "v2"
TRIPLETEX_COMPANY_ID = "0"  # Default for Tripletex API


@pytest.fixture(scope="module")
def tripletex_config() -> Dict[str, str]:
    """Loads Tripletex test configuration from environment variables."""
    provider = EnvProvider(prefix="")
    loaded_env_vars = provider.load()

    consumer_token = loaded_env_vars.get("TRIPLETEX_TEST_CONSUMER_TOKEN")
    employee_token = loaded_env_vars.get("TRIPLETEX_TEST_EMPLOYEE_TOKEN")

    if not consumer_token or not employee_token:
        pytest.skip("Missing TRIPLETEX_TEST_CONSUMER_TOKEN or " "TRIPLETEX_TEST_EMPLOYEE_TOKEN environment variables.")

    if not isinstance(consumer_token, str) or not isinstance(employee_token, str):
        pytest.fail("TRIPLETEX_TEST_CONSUMER_TOKEN or TRIPLETEX_TEST_EMPLOYEE_TOKEN " "environment variables are not strings.")

    config = {
        "hostname": TRIPLETEX_TEST_HOSTNAME,
        "consumer_token": consumer_token,
        "employee_token": employee_token,
    }
    return config


def create_expiration_date() -> str:
    """
    Creates an expiration date string for the session token that is always a valid future date.

    Sets the expiration date to two days ahead at 23:59:59 UTC to ensure it is always in the future,
    regardless of when the test is run.
    """
    two_days_ahead = (datetime.now(timezone.utc) + timedelta(days=2)).replace(hour=23, minute=59, second=59, microsecond=0)
    return two_days_ahead.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def get_session_token(config: Dict[str, str]) -> Optional[str]:
    """Requests a session token from the Tripletex test API."""
    base_url = f"{config['hostname']}/{TRIPLETEX_API_VERSION}"
    url = f"{base_url}/token/session/:create"
    params = {
        "consumerToken": config["consumer_token"],
        "employeeToken": config["employee_token"],
        "expirationDate": create_expiration_date(),
    }
    # Encode parameters for PUT request URL
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    logger.info("Requesting session token from %s", url)
    req = urllib.request.Request(full_url, method="PUT")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                token_data = data.get("value", {})
                token = token_data.get("token") if isinstance(token_data, dict) else None
                # Ensure token is a non-empty string before returning
                if isinstance(token, str) and token:
                    logger.info("Successfully obtained session token.")
                    return token
                elif token is not None:
                    # Log if token exists but is not a string or is empty
                    logger.error(
                        "Invalid or empty token received: %s (type: %s)",
                        token,
                        type(token).__name__,
                    )
                    return None
                else:  # token is None
                    logger.error("Session token not found in response: %s", data)
                    return None
            else:
                logger.error(
                    "Failed to get session token. Status: %s, Body: %s",
                    response.status,
                    response.read().decode("utf-8"),
                )
                return None
    except urllib.error.HTTPError as e:
        logger.error(
            "HTTP Error getting session token: %s %s\n%s",
            e.code,
            e.reason,
            e.read().decode("utf-8"),
            exc_info=True,
        )
        return None
    except urllib.error.URLError as e:
        logger.error("URL Error getting session token: %s", e.reason, exc_info=True)
        return None
    except Exception as e:
        logger.error("Unexpected error getting session token: %s", e, exc_info=True)
        return None


def list_countries(config: Dict[str, str], session_token: str) -> Optional[List[Dict[str, Any]]]:
    """Lists countries using the obtained session token."""
    base_url = f"{config['hostname']}/{TRIPLETEX_API_VERSION}"
    url = f"{base_url}/country"

    # Prepare Basic Auth header
    raw_auth = f"{TRIPLETEX_COMPANY_ID}:{session_token}"
    encoded_auth = base64.b64encode(raw_auth.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_auth}"}

    logger.info("Requesting country list from %s", url)
    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                countries = data.get("values")
                if isinstance(countries, list):
                    logger.info("Successfully retrieved %d countries.", len(countries))
                    return countries
                else:
                    logger.error("Invalid country list format in response: %s", data)
                    return None
            else:
                logger.error(
                    "Failed to list countries. Status: %s, Body: %s",
                    response.status,
                    response.read().decode("utf-8"),
                )
                return None
    except urllib.error.HTTPError as e:
        logger.error(
            "HTTP Error listing countries: %s %s\n%s",
            e.code,
            e.reason,
            e.read().decode("utf-8"),
            exc_info=True,
        )
        return None
    except urllib.error.URLError as e:
        logger.error("URL Error listing countries: %s", e.reason, exc_info=True)
        return None
    except Exception as e:
        logger.error("Unexpected error listing countries: %s", e, exc_info=True)
        return None


# --- Test Function ---


def test_tripletex_auth_and_list_countries(tripletex_config: Dict[str, str]) -> None:
    """
    Tests getting a session token and listing countries using apiconfig
    for configuration and urllib for HTTP requests.
    """
    # 1. Get Session Token
    session_token = get_session_token(tripletex_config)
    assert session_token is not None, "Failed to obtain session token"
    assert isinstance(session_token, str)
    assert len(session_token) > 0

    # 2. List Countries using the token
    countries = list_countries(tripletex_config, session_token)
    assert countries is not None, "Failed to list countries"
    assert isinstance(countries, list)
    assert len(countries) > 0, "Country list should not be empty"

    # 3. Basic check of country data structure
    first_country = countries[0]
    assert isinstance(first_country, dict)
    assert "id" in first_country
    assert "displayName" in first_country
    assert "isoAlpha2Code" in first_country
