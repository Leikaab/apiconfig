"""Core type definitions for the apiconfig library."""

from typing import Any, Callable, Dict, List, Mapping, Optional, TypeAlias, Union

# JSON Types
JsonPrimitive: TypeAlias = Union[str, int, float, bool, None]
JsonValue: TypeAlias = Union[JsonPrimitive, List[Any], Dict[str, Any]]
JsonObject: TypeAlias = Dict[str, JsonValue]
JsonList: TypeAlias = List[JsonValue]

# HTTP Types
HeadersType: TypeAlias = Mapping[str, str]
ParamsType: TypeAlias = Mapping[str, Union[str, int, float, bool, None]]
DataType: TypeAlias = Union[str, bytes, JsonObject, Mapping[str, Any]]

# Configuration Types
ConfigDict: TypeAlias = Dict[str, Any]
ConfigProviderCallable: TypeAlias = Callable[[], ConfigDict]

# Authentication Types
AuthCredentials: TypeAlias = Any  # Placeholder for various credential types
TokenStorageStrategy: TypeAlias = Any  # Placeholder for token storage implementations
TokenRefreshCallable: TypeAlias = Callable[
    ..., Any
]  # Placeholder for token refresh logic

# Extension Types
CustomAuthPrepareCallable: TypeAlias = Callable[
    [Any, Optional[ParamsType], Optional[HeadersType], Optional[DataType]],
    tuple[Optional[ParamsType], Optional[HeadersType], Optional[DataType]],
]
CustomLogFormatter: TypeAlias = Any  # Placeholder for custom logging formatters
CustomLogHandler: TypeAlias = Any  # Placeholder for custom logging handlers
CustomRedactionRule: TypeAlias = Callable[[str], str]

# General Callables
RequestHookCallable: TypeAlias = Callable[[Any], None]  # e.g., for request modification
ResponseHookCallable: TypeAlias = Callable[[Any], None]  # e.g., for response processing
