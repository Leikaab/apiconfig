"""Core type definitions for the apiconfig library."""

from typing import Any, Callable, Dict, List, Mapping, Optional, TypeAlias, Union

# JSON Types
JsonPrimitive: TypeAlias = Union[str, int, float, bool, None]
"""Type alias for primitive JSON types."""

JsonValue: TypeAlias = Union[JsonPrimitive, List[Any], Dict[str, Any]]
"""Type alias for any valid JSON value."""

JsonObject: TypeAlias = Dict[str, JsonValue]
"""Type alias for a JSON object (dictionary)."""

JsonList: TypeAlias = List[JsonValue]
"""Type alias for a JSON list."""

# HTTP Types
HeadersType: TypeAlias = Mapping[str, str]
"""Type alias for HTTP headers."""

ParamsType: TypeAlias = Mapping[str, Union[str, int, float, bool, None]]
"""Type alias for URL query parameters."""

DataType: TypeAlias = Union[str, bytes, JsonObject, Mapping[str, Any]]
"""Type alias for HTTP request body data."""

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

# Extension Types
CustomAuthPrepareCallable: TypeAlias = Callable[
    [Any, Optional[ParamsType], Optional[HeadersType], Optional[DataType]],
    tuple[Optional[ParamsType], Optional[HeadersType], Optional[DataType]],
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
