"""
Basic type guards for primitive types.

This module contains type guards for fundamental Python types like str, int, bool, etc.
"""

from typing import Any, TypeGuard


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


def is_int(value: Any) -> TypeGuard[int]:
    """
    Runtime type guard to validate integer parameters.

    This function tells static type checkers that isinstance checks for integers
    are intentional runtime validation, not redundant type checking.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[int]
        True if value is an integer, False otherwise
    """
    return isinstance(value, int)


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


def is_bytes(value: Any) -> TypeGuard[bytes]:
    """
    Runtime type guard to validate bytes parameters.

    This function tells static type checkers that isinstance checks for bytes
    are intentional runtime validation, not redundant type checking.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[bytes]
        True if value is bytes, False otherwise
    """
    return isinstance(value, bytes)
