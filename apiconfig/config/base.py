import copy
import logging
import warnings
from typing import TYPE_CHECKING, Dict, Optional
from urllib.parse import urljoin

from apiconfig.exceptions.config import InvalidConfigError, MissingConfigError

if TYPE_CHECKING:
    from apiconfig.auth.base import AuthStrategy  # noqa: F401 - Used for type hinting

# Set up logging
logger = logging.getLogger(__name__)


class ClientConfig:
    hostname: Optional[str] = None
    version: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    timeout: float = 10.0
    retries: int = 3
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
        self.hostname = hostname or self.__class__.hostname

        # Store version value before validation
        version_value = version or self.__class__.version
        # Validate version (no leading/trailing slashes)
        if version_value and (version_value.startswith('/') or version_value.endswith('/')):
            raise InvalidConfigError(
                "Version must not contain leading or trailing slashes."
            )
        self.version = version_value

        self.headers = headers or self.__class__.headers or {}

        # Store timeout value before validation
        timeout_value = timeout if timeout is not None else self.__class__.timeout
        # Validate timeout (must be non-negative number)
        if timeout_value is not None:
            if not isinstance(timeout_value, (int, float)):
                raise InvalidConfigError("Timeout must be a number (int or float).")
            if timeout_value < 0:
                raise InvalidConfigError("Timeout must be non-negative.")
        self.timeout = timeout_value

        # Store retries value before validation
        retries_value = retries if retries is not None else self.__class__.retries
        # Validate retries (must be non-negative number)
        if retries_value is not None:
            if not isinstance(retries_value, (int, float)):
                raise InvalidConfigError("Retries must be a number (int or float).")
            if retries_value < 0:
                raise InvalidConfigError("Retries must be non-negative.")
        self.retries = retries_value

        self.auth_strategy = auth_strategy or self.__class__.auth_strategy
        self.log_request_body = (
            log_request_body
            if log_request_body is not None
            else self.__class__.log_request_body
        )
        self.log_response_body = (
            log_response_body
            if log_response_body is not None
            else self.__class__.log_response_body
        )

    @property
    def base_url(self) -> str:
        if not self.hostname:
            logger.error("Hostname is required for base_url")
            raise MissingConfigError("hostname is required to construct base_url.")
        # Ensure hostname has a scheme, default to https if missing
        scheme = "https://" if "://" not in self.hostname else ""
        full_hostname = f"{scheme}{self.hostname}"
        # Join hostname and version, ensuring correct slash handling
        return urljoin(f"{full_hostname}/", self.version or "").rstrip("/")

    def merge(self, other: "ClientConfig") -> "ClientConfig":
        if not isinstance(other, self.__class__):
            logger.warning(
                f"Attempted to merge ClientConfig with incompatible type: {type(other)}"
            )
            return NotImplemented  # type: ignore[return-value]

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
                    logger.warning(
                        f"Attribute '{key}' from other config not found in base config, skipping merge."
                    )

        # Re-validate merged config
        # Validate version (no leading/trailing slashes)
        if new_instance.version and (new_instance.version.startswith('/') or new_instance.version.endswith('/')):
            raise InvalidConfigError(
                "Merged version must not contain leading or trailing slashes."
            )

        # Validate timeout (must be non-negative number)
        if new_instance.timeout is not None:
            if not isinstance(new_instance.timeout, (int, float)):
                raise InvalidConfigError("Merged timeout must be a number (int or float).")
            if new_instance.timeout < 0:
                raise InvalidConfigError("Merged timeout must be non-negative.")

        # Validate retries (must be non-negative number)
        if new_instance.retries is not None:
            if not isinstance(new_instance.retries, (int, float)):
                raise InvalidConfigError("Merged retries must be a number (int or float).")
            if new_instance.retries < 0:
                raise InvalidConfigError("Merged retries must be non-negative.")

        return new_instance

    def __add__(self, other: "ClientConfig") -> "ClientConfig":
        warnings.warn(
            "The __add__ method for ClientConfig is deprecated. Use merge() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        merged = self.merge(other)
        if merged is NotImplemented:
            # Raise TypeError if merge returns NotImplemented
            raise TypeError(
                f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'"
            )
        return merged

    @staticmethod
    def merge_configs(
        base_config: "ClientConfig", other_config: "ClientConfig"
    ) -> "ClientConfig":
        if not isinstance(base_config, ClientConfig) or not isinstance(
            other_config, ClientConfig
        ):
            raise TypeError("Both arguments must be instances of ClientConfig")

        return base_config.merge(other_config)
