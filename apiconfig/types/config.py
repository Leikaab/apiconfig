"""Configuration-related type definitions."""

from typing import Any, Callable, Dict, TypeAlias

# Configuration Types
ConfigDict: TypeAlias = Dict[str, Any]
"""Type alias for a dictionary representing configuration."""

ConfigProviderCallable: TypeAlias = Callable[[], ConfigDict]
"""Type alias for a callable that provides configuration."""

__all__ = [
    "ConfigDict",
    "ConfigProviderCallable",
]
