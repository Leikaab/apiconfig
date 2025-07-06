"""
Assertion utilities for type validation.

This module contains the generic assert_type function and convenience assertion
functions that combine type checking with error raising for ergonomic parameter validation.
"""

import inspect
from typing import Any, Callable, Optional, TypeGuard

from .basic import is_bool, is_bytes, is_int, is_str
from .collections import is_dict, is_list, is_tuple
from .complex import is_dict_or_list, is_tuple_of_two_strings
from .optional import is_dict_or_none, is_str_or_none


def assert_type(value: Any, type_guard: Callable[[Any], TypeGuard[Any]], expected_type_name: str, param_name: Optional[str] = None) -> None:
    """
    Assert that a value passes a type guard, raising TypeError if not.

    This function combines type checking and error raising for more ergonomic
    parameter validation. It can automatically extract the parameter name
    from the calling context if not provided.

    Parameters
    ----------
    value : Any
        The value to check
    type_guard : Callable[[Any], TypeGuard[Any]]
        The type guard function to use for validation
    expected_type_name : str
        Human-readable name of the expected type for error messages
    param_name : str, optional
        Name of the parameter for error messages. If None, attempts to
        extract from calling context

    Raises
    ------
    TypeError
        If value does not pass the type guard

    Examples
    --------
    >>> assert_type(endpoint, is_str, "string")
    >>> assert_type(params, is_dict_or_none, "dictionary or None")
    >>> assert_type(handle_response, is_bool, "boolean", "handle_response")
    """
    if not type_guard(value):
        if param_name is None:
            # Try to extract parameter name from calling context
            frame = inspect.currentframe()
            if frame and frame.f_back:
                # Get the calling frame's local variables
                caller_locals = frame.f_back.f_locals
                # Try to find a variable name that matches our value
                for var_name, var_value in caller_locals.items():
                    if var_value is value and not var_name.startswith("_"):
                        param_name = var_name
                        break

            # Fallback if we couldn't extract the name
            if param_name is None:
                param_name = "parameter"

        raise TypeError(f"{param_name} must be {expected_type_name}, got {type(value).__name__}")


# Convenience functions for common type assertions
def assert_str(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a string."""
    assert_type(value, is_str, "a string", param_name)


def assert_int(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is an integer."""
    assert_type(value, is_int, "an integer", param_name)


def assert_bool(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a boolean."""
    assert_type(value, is_bool, "a boolean", param_name)


def assert_bytes(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is bytes."""
    assert_type(value, is_bytes, "bytes", param_name)


def assert_dict(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a dictionary."""
    assert_type(value, is_dict, "a dictionary", param_name)


def assert_list(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a list."""
    assert_type(value, is_list, "a list", param_name)


def assert_tuple(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a tuple."""
    assert_type(value, is_tuple, "a tuple", param_name)


def assert_str_or_none(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a string or None."""
    assert_type(value, is_str_or_none, "a string or None", param_name)


def assert_dict_or_none(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a dictionary or None."""
    assert_type(value, is_dict_or_none, "a dictionary or None", param_name)


def assert_dict_or_list(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a dictionary or list."""
    assert_type(value, is_dict_or_list, "a dictionary or list", param_name)


def assert_tuple_of_two_strings(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a tuple of two strings."""
    assert_type(value, is_tuple_of_two_strings, "a tuple of two strings", param_name)
