"""Core type definitions for the apiconfig library."""

# Import all types from submodules to maintain the same public API
from .auth import (
    AuthCredentials,
    AuthRefreshCallback,
    CustomAuthPrepareCallable,
    HttpRequestCallable,
    RefreshedTokenData,
    TokenData,
    TokenRefreshCallable,
    TokenRefreshResult,
    TokenStorageStrategy,
)
from .config import (
    ConfigDict,
    ConfigProviderCallable,
)
from .extensions import (
    CustomLogFormatter,
    CustomLogHandler,
    CustomRedactionRule,
    RequestHookCallable,
    ResponseHookCallable,
)
from .http import (
    DataType,
    HeadersType,
    HttpMethod,
    HttpRequestProtocol,
    HttpResponseProtocol,
    QueryParamType,
    QueryParamValueType,
    ResponseBodyType,
    UrlencodeParamsType,
)
from .json import (
    JsonDecoder,
    JsonDeserializerCallable,
    JsonEncoder,
    JsonList,
    JsonObject,
    JsonPrimitive,
    JsonSerializerCallable,
    JsonValue,
)

__all__ = [
    # JSON types
    "JsonPrimitive",
    "JsonValue",
    "JsonObject",
    "JsonList",
    "JsonEncoder",
    "JsonDecoder",
    "JsonSerializerCallable",
    "JsonDeserializerCallable",
    # HTTP types
    "HeadersType",
    "QueryParamType",
    "QueryParamValueType",
    "UrlencodeParamsType",
    "DataType",
    "ResponseBodyType",
    "HttpRequestProtocol",
    "HttpResponseProtocol",
    "HttpMethod",
    # Config types
    "ConfigDict",
    "ConfigProviderCallable",
    # Auth types
    "AuthCredentials",
    "TokenStorageStrategy",
    "TokenData",
    "TokenRefreshCallable",
    "RefreshedTokenData",
    "TokenRefreshResult",
    "HttpRequestCallable",
    "AuthRefreshCallback",
    "CustomAuthPrepareCallable",
    # Extension types
    "CustomLogFormatter",
    "CustomLogHandler",
    "CustomRedactionRule",
    "RequestHookCallable",
    "ResponseHookCallable",
]
