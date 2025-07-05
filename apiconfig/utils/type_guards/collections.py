"""
Collection type guards for container types.

This module contains type guards for Python collection types like dict, list, tuple, etc.
"""

from typing import Any, Dict, List, Tuple, TypeGuard


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


def is_list(value: Any) -> TypeGuard[List[Any]]:
    """
    Runtime type guard to validate list parameters.

    This function tells static type checkers that isinstance checks for lists
    are intentional runtime validation, not redundant type checking.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[list]
        True if value is a list, False otherwise
    """
    return isinstance(value, list)


def is_tuple(value: Any) -> TypeGuard[Tuple[Any, ...]]:
    """
    Runtime type guard to validate tuple parameters.

    This function tells static type checkers that isinstance checks for tuples
    are intentional runtime validation, not redundant type checking.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[tuple]
        True if value is a tuple, False otherwise
    """
    return isinstance(value, tuple)
