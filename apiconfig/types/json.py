"""JSON-related type definitions."""

import json
from typing import Any, Callable, Dict, List, TypeAlias, Union

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

__all__ = [
    "JsonPrimitive",
    "JsonValue",
    "JsonObject",
    "JsonList",
    "JsonEncoder",
    "JsonDecoder",
    "JsonSerializerCallable",
    "JsonDeserializerCallable",
]
