"""
Base configuration module for API clients.

Provides the `ClientConfig` class for managing common API client settings
like hostname, version, headers, timeout, retries, and authentication.
"""

import copy
import logging
import warnings
from typing import TYPE_CHECKING, Dict, Optional, TypeVar
from urllib.parse import urljoin

from apiconfig.exceptions.config import InvalidConfigError, MissingConfigError

if TYPE_CHECKING:
    from apiconfig.auth.base import AuthStrategy  # noqa: F401 - Used for type hinting

# Set up logging
logger = logging.getLogger(__name__)


_TClientConfig = TypeVar("_TClientConfig", bound="ClientConfig")


class ClientConfig:
    """Base configuration class for API clients.

    Stores common configuration settings like hostname, API version, headers,
    timeout, retries, and authentication strategy.

    Attributes
    ----------
    hostname
        The base hostname of the API (e.g., "api.example.com").
        If not provided, defaults to None.
    version
        The API version string (e.g., "v1"). Appended to the hostname.
        Must not contain leading or trailing slashes. If not provided, defaults to None.
    headers
        Default headers to include in every request.
        If not provided, defaults to an empty dictionary.
    timeout
        Default request timeout in seconds. Must be a non-negative number when provided.
        Defaults to 10.0 seconds.
    retries
        Default number of retries for failed requests. Must be a non-negative number when provided.
        Defaults to 3 retries.
    auth_strategy
        An instance of AuthStrategy for handling authentication.
        If not provided, defaults to None.
    log_request_body
        Whether to log the request body (potentially sensitive).
        Defaults to False.
    log_response_body
        Whether to log the response body (potentially sensitive).
        Defaults to False.
    """

    hostname: Optional[str] = None
    version: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    timeout: Optional[float] = 10.0
    retries: Optional[int] = 3
    auth_strategy: Optional["AuthStrategy"] = None
    log_request_body: bool = False
    log_response_body: bool = False

    def __init__(
        self,
        hostname: Optional[str] = None,
        version: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
        auth_strategy: Optional["AuthStrategy"] = None,
        log_request_body: Optional[bool] = None,
        log_response_body: Optional[bool] = None,
    ) -> None:
        """Initialize the ClientConfig instance.

        Args
        ----
        hostname
            The base hostname of the API.
        version
            The API version string. Must not contain leading or trailing slashes.
        headers
            Default headers for requests.
        timeout
            Request timeout in seconds. Must be a non-negative number (int or float) when provided.
        retries
            Number of retries for failed requests. Must be a non-negative number (int or float) when provided.
        auth_strategy
            Authentication strategy instance.
        log_request_body
            Flag to enable request body logging.
        log_response_body
            Flag to enable response body logging.

        Raises
        ------
        InvalidConfigError
            If version contains leading or trailing slashes,
            if timeout or retries are negative, or if timeout or retries
            are not numbers (int or float).
        """
        self.hostname = hostname or self.__class__.hostname

        # Store version value before validation
        version_value = version or self.__class__.version
        # Validate version (no leading/trailing slashes)
        if version_value and (version_value.startswith("/") or version_value.endswith("/")):
            raise InvalidConfigError("Version must not contain leading or trailing slashes.")
        self.version = version_value

        self.headers = headers or self.__class__.headers or {}

        # Store timeout value before validation
        timeout_value = timeout if timeout is not None else self.__class__.timeout
        # Validate timeout (must be non-negative number)
        if timeout_value is not None:
            timeout_value = float(timeout_value)
            if timeout_value < 0:
                raise InvalidConfigError("Timeout must be non-negative.")
        self.timeout = timeout_value

        # Store retries value before validation
        retries_value = retries if retries is not None else self.__class__.retries
        # Validate retries (must be non-negative number)
        if retries_value is not None:
            retries_value = int(retries_value)
            if retries_value < 0:
                raise InvalidConfigError("Retries must be non-negative.")
        self.retries = retries_value

        self.auth_strategy = auth_strategy or self.__class__.auth_strategy
        self.log_request_body = log_request_body if log_request_body is not None else self.__class__.log_request_body
        self.log_response_body = log_response_body if log_response_body is not None else self.__class__.log_response_body

    @property
    def base_url(self) -> str:
        """Construct the base URL from hostname and version.

        Ensures the hostname has a scheme (defaults to https) and handles
        joining with the version correctly.

        Returns
        -------
        str
            The constructed base URL string.

        Raises
        ------
        MissingConfigError
            If hostname is not configured.
        """
        if not self.hostname:
            logger.error("Hostname is required for base_url")
            raise MissingConfigError("hostname is required to construct base_url.")
        # Ensure hostname has a scheme, default to https if missing
        scheme = "https://" if "://" not in self.hostname else ""
        full_hostname = f"{scheme}{self.hostname}"
        # Join hostname and version, ensuring correct slash handling
        return urljoin(f"{full_hostname}/", self.version or "").rstrip("/")

    def merge(self, other: _TClientConfig) -> _TClientConfig:
        """Merge this configuration with another ClientConfig instance.

        Creates a deep copy of the current instance and overrides its attributes
        with non-None values from the 'other' instance. Headers are merged,
        with 'other's headers taking precedence. All mutable attributes are
        deep-copied to ensure the merged config is independent of the original configs.

        Args
        ----
        other
            Another ClientConfig instance to merge with.

        Returns
        -------
        _TClientConfig
            A new ClientConfig instance representing the merged configuration.
            Returns NotImplemented if 'other' is not a ClientConfig instance.

        Raises
        ------
        InvalidConfigError
            If the merged version contains leading or trailing slashes,
            if the merged timeout or retries are negative, or if the merged timeout
            or retries are not numbers (int or float).
        TypeError
            If 'other' is not a ClientConfig instance.
        """
        if not isinstance(other, self.__class__):
            logger.warning(f"Attempted to merge ClientConfig with incompatible type: {type(other)}")
            raise TypeError(f"Cannot merge ClientConfig with object of type {type(other)}")

        # Create a deep copy of self as the base for the new instance
        new_instance = copy.deepcopy(self)

        # Merge headers: other's headers take precedence
        if hasattr(other, "headers") and other.headers:
            new_headers = copy.deepcopy(new_instance.headers or {})
            new_headers.update(other.headers)
            new_instance.headers = new_headers

        # Copy all other attributes from other if they are not None, overriding self's values
        for key, value in other.__dict__.items():
            # Skip headers (already handled) and internal/private attributes
            if key != "headers" and not key.startswith("_") and value is not None:
                # Ensure the attribute exists on the class before setting
                if hasattr(new_instance, key):
                    setattr(new_instance, key, copy.deepcopy(value))
                else:
                    logger.warning(f"Attribute '{key}' from other config not found in base config, skipping merge.")

        # Re-validate merged config
        # Validate version (no leading/trailing slashes)
        if new_instance.version and (new_instance.version.startswith("/") or new_instance.version.endswith("/")):
            raise InvalidConfigError("Merged version must not contain leading or trailing slashes.")

        # Validate timeout (must be non-negative number)
        if new_instance.timeout is not None:
            new_instance.timeout = float(new_instance.timeout)
            if new_instance.timeout < 0:
                raise InvalidConfigError("Merged timeout must be non-negative.")

        # Validate retries (must be non-negative number)
        if new_instance.retries is not None:
            new_instance.retries = int(new_instance.retries)
            if new_instance.retries < 0:
                raise InvalidConfigError("Merged retries must be non-negative.")

        from typing import cast

        return cast(_TClientConfig, new_instance)

    def __add__(self, other: _TClientConfig) -> _TClientConfig:
        """Merge this configuration with another using the '+' operator (DEPRECATED).

        Warns about deprecation and calls the merge() method.

        Args
        ----
        other
            Another ClientConfig instance to merge with.

        Returns
        -------
        _TClientConfig
            A new ClientConfig instance representing the merged configuration.

        Raises
        ------
        TypeError
            If the merge operation is not supported between the types.
        """
        warnings.warn(
            "The __add__ method for ClientConfig is deprecated. Use merge() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        merged = self.merge(other)
        if merged is NotImplemented:
            # Raise TypeError if merge returns NotImplemented
            raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
        return merged

    @staticmethod
    def merge_configs(base_config: _TClientConfig, other_config: _TClientConfig) -> _TClientConfig:
        """Merge two ClientConfig instances.

        Static method wrapper around the instance merge() method.

        Args
        ----
        base_config
            The base ClientConfig instance.
        other_config
            The ClientConfig instance to merge into the base.

        Returns
        -------
        _TClientConfig
            A new ClientConfig instance representing the merged configuration.

        """
        return base_config.merge(other_config)
