"""
Type guard utilities for runtime validation.

This module contains TypeGuard functions that help static type checkers understand
the intent of isinstance checks, making them explicit runtime validation rather
than redundant type checking.
"""

import inspect
from typing import Any, Callable, Dict, Optional, TypeGuard


def is_str(value: Any) -> TypeGuard[str]:
    """
    Runtime type guard to validate string parameters.

    This function tells static type checkers that isinstance checks for strings
    are intentional runtime validation, not redundant type checking.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[str]
        True if value is a string, False otherwise
    """
    return isinstance(value, str)


def is_dict_or_none(value: Any) -> TypeGuard[Optional[Dict[str, Any]]]:
    """
    Runtime type guard to validate optional dictionary parameters.

    This function tells static type checkers that isinstance checks for
    optional dictionaries are intentional runtime validation.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[Optional[Dict[str, Any]]]
        True if value is None or a dictionary, False otherwise
    """
    return value is None or isinstance(value, dict)


def is_bool(value: Any) -> TypeGuard[bool]:
    """
    Runtime type guard to validate boolean parameters.

    This function tells static type checkers that isinstance checks for booleans
    are intentional runtime validation, not redundant type checking.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[bool]
        True if value is a boolean, False otherwise
    """
    return isinstance(value, bool)


def is_dict(value: Any) -> TypeGuard[Dict[str, Any]]:
    """
    Runtime type guard to validate dictionary parameters.

    This function tells static type checkers that isinstance checks for
    dictionaries are intentional runtime validation.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[Dict[str, Any]]
        True if value is a dictionary, False otherwise
    """
    return isinstance(value, dict)


# Generic assertion function for ergonomic parameter validation
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


def assert_dict_or_none(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a dictionary or None."""
    assert_type(value, is_dict_or_none, "a dictionary or None", param_name)


def assert_bool(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a boolean."""
    assert_type(value, is_bool, "a boolean", param_name)


def assert_dict(value: Any, param_name: Optional[str] = None) -> None:
    """Assert that a value is a dictionary."""
    assert_type(value, is_dict, "a dictionary", param_name)
