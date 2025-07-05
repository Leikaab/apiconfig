"""Extension-related type definitions."""

import logging
from typing import Any, Callable, TypeAlias

# Extension Types
CustomLogFormatter: TypeAlias = logging.Formatter
"""Type alias for custom log formatter instances."""

CustomLogHandler: TypeAlias = logging.Handler
"""Type alias for custom log handler instances."""

CustomRedactionRule: TypeAlias = Callable[[str], str]
"""Type alias for custom redaction rule callables."""

RequestHookCallable: TypeAlias = Callable[[Any], Any]
"""Type alias for request hook callables."""

ResponseHookCallable: TypeAlias = Callable[[Any], Any]
"""Type alias for response hook callables."""

__all__ = [
    "CustomLogFormatter",
    "CustomLogHandler",
    "CustomRedactionRule",
    "RequestHookCallable",
    "ResponseHookCallable",
]
