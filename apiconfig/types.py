"""Core type definitions for the apiconfig library."""

import json
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    TypeAlias,
    TypedDict,
    Union,
    runtime_checkable,
)

# JSON Types
JsonPrimitive: TypeAlias = Union[str, int, float, bool, None]
"""Type alias for primitive JSON types."""

JsonValue: TypeAlias = Union[JsonPrimitive, List[Any], Dict[str, Any]]
"""Type alias for any valid JSON value."""

JsonObject: TypeAlias = Dict[str, JsonValue]
"""Type alias for a JSON object (dictionary)."""

JsonList: TypeAlias = List[JsonValue]
"""Type alias for a JSON list."""

# JSON Processing Types
JsonEncoder: TypeAlias = json.JSONEncoder
"""Type alias for JSON encoder instances."""

JsonDecoder: TypeAlias = json.JSONDecoder
"""Type alias for JSON decoder instances."""

JsonSerializerCallable: TypeAlias = Callable[[Any], str]
"""Type alias for a callable that serializes objects to JSON strings."""

JsonDeserializerCallable: TypeAlias = Callable[[str], Any]
"""Type alias for a callable that deserializes JSON strings to objects."""

# HTTP Types
HeadersType: TypeAlias = Mapping[str, str]
"""Type alias for HTTP headers."""

# Simple, clear query parameter types
QueryParamValueType: TypeAlias = Union[str, int, float, bool, Sequence[Union[str, int, float, bool]], None]
"""Type alias for query parameter values."""

QueryParamType: TypeAlias = Mapping[str, QueryParamValueType]
"""Type alias for URL query parameters."""

# Internal type for urllib.parse.urlencode
UrlencodeParamsType: TypeAlias = Dict[str, Union[str, List[str]]]
"""Internal type for urllib.parse.urlencode compatibility."""

DataType: TypeAlias = Union[str, bytes, JsonObject, Mapping[str, Any]]
"""Type alias for HTTP request body data."""

# Type alias for API response body types
ResponseBodyType: TypeAlias = Union[JsonObject, JsonList, bytes, str, None]
"""Type alias for API response body types that apiconfig components might process."""


@runtime_checkable
class HttpRequestProtocol(Protocol):
    """Protocol matching common HTTP request objects (requests.Request, httpx.Request, etc.)."""

    method: str
    url: str
    headers: Any  # Different libraries use different header types


@runtime_checkable
class HttpResponseProtocol(Protocol):
    """Protocol matching common HTTP response objects (requests.Response, httpx.Response, etc.)."""

    status_code: int
    headers: Any
    text: str  # For body preview
    request: Optional[Any]  # Most responses have .request
    reason: Optional[str]


class HttpMethod(Enum):
    """Standard HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


# Configuration Types
ConfigDict: TypeAlias = Dict[str, Any]
"""Type alias for a dictionary representing configuration."""

ConfigProviderCallable: TypeAlias = Callable[[], ConfigDict]
"""Type alias for a callable that provides configuration."""

# Authentication Types
AuthCredentials: TypeAlias = Any
"""Placeholder type alias for various authentication credential types."""

TokenStorageStrategy: TypeAlias = Any
"""Placeholder type alias for token storage strategy implementations."""

TokenRefreshCallable: TypeAlias = Callable[..., Any]
"""Placeholder type alias for token refresh logic callables."""


class RefreshedTokenData(TypedDict, total=False):
    """Holds the data for a newly refreshed token.

    This TypedDict represents the structured data returned from token refresh
    operations, containing the new access token and optional metadata.

    Attributes
    ----------
    access_token : str
        The new access token (required).
    refresh_token : Optional[str]
        The new refresh token, if one was issued.
    expires_in : Optional[int]
        Lifespan of the new access token in seconds.
    token_type : Optional[str]
        Type of the token (e.g., "Bearer").
    scope : Optional[str]
        Scope of the new token, if applicable.

    Notes
    -----
    Additional fields from token endpoint responses can be added as needed.
    The `total=False` parameter allows for partial dictionaries where only
    some fields are present.
    """

    access_token: str
    refresh_token: Optional[str]
    expires_in: Optional[int]
    token_type: Optional[str]
    scope: Optional[str]


class TokenRefreshResult(TypedDict, total=False):
    """Structured result from an AuthStrategy's refresh method.

    This TypedDict represents the complete result of an authentication
    strategy's token refresh operation, including both token data and
    optional configuration updates.

    Attributes
    ----------
    token_data : Optional[RefreshedTokenData]
        The new token information returned from the refresh operation.
    config_updates : Optional[Dict[str, Any]]
        Optional configuration changes that should be applied after refresh,
        such as new API endpoints or updated client settings.

    Notes
    -----
    The `total=False` parameter allows for partial dictionaries where only
    some fields are present, providing flexibility in refresh implementations.
    """

    token_data: Optional[RefreshedTokenData]
    config_updates: Optional[Dict[str, Any]]


# Type alias for an injected HTTP request function
HttpRequestCallable: TypeAlias = Callable[..., Any]
"""Type alias for HTTP request callable that auth strategies can use.

This type represents a callable that can be injected into authentication
strategies to perform HTTP requests. The signature will be refined based
on actual usage patterns as the implementation progresses.

Notes
-----
This is intentionally broad to accommodate various HTTP client interfaces
and will be made more specific as requirements become clearer.
"""

# Type alias for auth refresh callback functions
AuthRefreshCallback: TypeAlias = Callable[[], None]
"""Type alias for auth refresh callback functions compatible with crudclient.

This type represents a callback function that can be invoked when
authentication tokens need to be refreshed. The callback takes no
parameters and returns None, making it compatible with crudclient's
refresh callback interface.

Notes
-----
This callback is typically used to trigger token refresh operations
in response to authentication failures or token expiration.
"""

# Extension Types
CustomAuthPrepareCallable: TypeAlias = Callable[
    [Any, Optional[QueryParamType], Optional[HeadersType], Optional[DataType]],
    tuple[Optional[QueryParamType], Optional[HeadersType], Optional[DataType]],
]
"""Type alias for a custom authentication preparation callable."""

CustomLogFormatter: TypeAlias = Any
"""Placeholder type alias for custom logging formatters."""

CustomLogHandler: TypeAlias = Any
"""Placeholder type alias for custom logging handlers."""

CustomRedactionRule: TypeAlias = Callable[[str], str]
"""Type alias for a custom data redaction rule callable."""

# General Callables
RequestHookCallable: TypeAlias = Callable[[Any], None]
"""Type alias for a callable hook executed before sending a request."""

ResponseHookCallable: TypeAlias = Callable[[Any], None]
"""Type alias for a callable hook executed after receiving a response."""

__all__ = [
    "JsonPrimitive",
    "JsonValue",
    "JsonObject",
    "JsonList",
    "JsonEncoder",
    "JsonDecoder",
    "JsonSerializerCallable",
    "JsonDeserializerCallable",
    "HeadersType",
    "QueryParamType",
    "QueryParamValueType",
    "UrlencodeParamsType",
    "DataType",
    "ResponseBodyType",
    "HttpRequestProtocol",
    "HttpResponseProtocol",
    "HttpMethod",
    "ConfigDict",
    "ConfigProviderCallable",
    "AuthCredentials",
    "TokenStorageStrategy",
    "TokenRefreshCallable",
    "RefreshedTokenData",
    "TokenRefreshResult",
    "HttpRequestCallable",
    "AuthRefreshCallback",
    "CustomAuthPrepareCallable",
    "CustomLogFormatter",
    "CustomLogHandler",
    "CustomRedactionRule",
    "RequestHookCallable",
    "ResponseHookCallable",
]
