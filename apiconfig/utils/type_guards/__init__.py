"""
Type guard utilities for runtime validation.

This module contains TypeGuard functions that help static type checkers understand
the intent of isinstance checks, making them explicit runtime validation rather
than redundant type checking.

The module is organized into several submodules:
- basic: Basic type guards for primitive types (str, int, bool, etc.)
- collections: Type guards for collection types (list, dict, tuple, etc.)
- optional: Type guards for optional/nullable types
- complex: Type guards for complex composite types
- assertions: Generic assertion utilities and convenience functions
"""

from .assertions import (
    assert_bool,
    assert_bytes,
    assert_dict,
    assert_dict_or_list,
    assert_dict_or_none,
    assert_int,
    assert_list,
    assert_str,
    assert_str_or_none,
    assert_tuple,
    assert_tuple_of_two_strings,
    assert_type,
)

# Import all type guards and assertions for backward compatibility
from .basic import (
    is_bool,
    is_bytes,
    is_int,
    is_str,
)
from .collections import (
    is_dict,
    is_list,
    is_tuple,
)
from .complex import (
    is_dict_or_list,
    is_tuple_of_two_strings,
)
from .optional import (
    is_dict_or_none,
    is_str_or_none,
)

__all__ = [
    # Basic type guards
    "is_str",
    "is_int",
    "is_bool",
    "is_bytes",
    # Collection type guards
    "is_dict",
    "is_list",
    "is_tuple",
    # Optional type guards
    "is_str_or_none",
    "is_dict_or_none",
    # Complex type guards
    "is_dict_or_list",
    "is_tuple_of_two_strings",
    # Assertion utilities
    "assert_type",
    "assert_str",
    "assert_int",
    "assert_bool",
    "assert_bytes",
    "assert_dict",
    "assert_list",
    "assert_tuple",
    "assert_str_or_none",
    "assert_dict_or_none",
    "assert_dict_or_list",
    "assert_tuple_of_two_strings",
]
