import warnings
from typing import TYPE_CHECKING, Dict, Optional, Type, TypeVar
from urllib.parse import urljoin

if TYPE_CHECKING:
    from apiconfig.auth.base import AuthStrategy

_TClientConfig = TypeVar("_TClientConfig", bound="ClientConfig")


class ClientConfig:
    """
    Base configuration class for API clients.

    Stores common configuration settings like hostname, API version, headers,
    timeout, retries, and authentication strategy.

    Attributes:
        hostname: The base hostname of the API (e.g., "api.example.com").
        version: The API version string (e.g., "v1"). Appended to the hostname.
        headers: Default headers to include in every request.
        timeout: Default request timeout in seconds.
        retries: Default number of retries for failed requests.
        auth_strategy: An instance of AuthStrategy for handling authentication.
        log_request_body: Whether to log the request body (potentially sensitive).
        log_response_body: Whether to log the response body (potentially sensitive).
    """

    hostname: Optional[str]
    version: Optional[str]
    headers: Optional[Dict[str, str]]
    timeout: float
    retries: int
    auth_strategy: Optional["AuthStrategy"]
    log_request_body: bool
    log_response_body: bool

    def __init__(
        self,
        hostname: Optional[str] = ...,
        version: Optional[str] = ...,
        headers: Optional[Dict[str, str]] = ...,
        timeout: Optional[float] = ...,
        retries: Optional[int] = ...,
        auth_strategy: Optional["AuthStrategy"] = ...,
        log_request_body: Optional[bool] = ...,
        log_response_body: Optional[bool] = ...,
    ) -> None:
        """
        Initializes the ClientConfig instance.

        Args:
            hostname: The base hostname of the API.
            version: The API version string.
            headers: Default headers for requests.
            timeout: Request timeout in seconds.
            retries: Number of retries for failed requests.
            auth_strategy: Authentication strategy instance.
            log_request_body: Flag to enable request body logging.
            log_response_body: Flag to enable response body logging.

        Raises:
            InvalidConfigError: If timeout or retries are negative.
        """
        ...

    @property
    def base_url(self) -> str:
        """
        Constructs the base URL from hostname and version.

        Ensures the hostname has a scheme (defaults to https) and handles
        joining with the version correctly.

        Returns:
            The constructed base URL string.

        Raises:
            MissingConfigError: If hostname is not configured.
        """
        ...

    def merge(self: _TClientConfig, other: _TClientConfig) -> _TClientConfig:
        """
        Merges this configuration with another ClientConfig instance.

        Creates a deep copy of the current instance and overrides its attributes
        with non-None values from the 'other' instance. Headers are merged,
        with 'other's headers taking precedence.

        Args:
            other: Another ClientConfig instance to merge with.

        Returns:
            A new ClientConfig instance representing the merged configuration.

        Raises:
            InvalidConfigError: If the merged timeout or retries are negative.
        """
        ...

    def __add__(self: _TClientConfig, other: _TClientConfig) -> _TClientConfig:
        """
        Deprecated: Merges this configuration with another using the '+' operator.

        Warns about deprecation and calls the merge() method.

        Args:
            other: Another ClientConfig instance to merge with.

        Returns:
            A new ClientConfig instance representing the merged configuration.

        Raises:
            TypeError: If the merge operation is not supported between the types.
        """
        ...

    @staticmethod
    def merge_configs(
        base_config: _TClientConfig, other_config: _TClientConfig
    ) -> _TClientConfig:
        """
        Merges two ClientConfig instances.

        Static method wrapper around the instance merge() method.

        Args:
            base_config: The base ClientConfig instance.
            other_config: The ClientConfig instance to merge into the base.

        Returns:
            A new ClientConfig instance representing the merged configuration.

        Raises:
            TypeError: If either argument is not an instance of ClientConfig.
        """
        ...
