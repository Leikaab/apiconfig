"""HTTP-related type definitions."""

from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    TypeAlias,
    Union,
    runtime_checkable,
)

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

DataType: TypeAlias = Union[str, bytes, Dict[str, Any], Mapping[str, Any]]
"""Type alias for HTTP request body data."""

# Type alias for API response body types
ResponseBodyType: TypeAlias = Union[Dict[str, Any], List[Any], bytes, str, None]
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
    history: Optional[List[Any]]  # For redirect history (requests, httpx)


class HttpMethod(Enum):
    """Standard HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


__all__ = [
    "HeadersType",
    "QueryParamType",
    "QueryParamValueType",
    "UrlencodeParamsType",
    "DataType",
    "ResponseBodyType",
    "HttpRequestProtocol",
    "HttpResponseProtocol",
    "HttpMethod",
]
