"""
Optional type guards for nullable types.

This module contains type guards for optional/nullable versions of types.
"""

from typing import Any, Dict, Optional, TypeGuard


def is_str_or_none(value: Any) -> TypeGuard[Optional[str]]:
    """
    Runtime type guard to validate optional string parameters.

    This function tells static type checkers that isinstance checks for
    optional strings are intentional runtime validation.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[Optional[str]]
        True if value is None or a string, False otherwise
    """
    return value is None or isinstance(value, str)


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
