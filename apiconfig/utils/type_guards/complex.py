"""
Complex type guards for composite types.

This module contains type guards for more complex composite types and unions.
"""

from typing import Any, Dict, List, TypeGuard, Union, cast


def is_dict_or_list(value: Any) -> TypeGuard[Union[Dict[str, Any], List[Any]]]:
    """
    Runtime type guard to validate dict or list parameters.

    This function tells static type checkers that isinstance checks for
    dict or list are intentional runtime validation.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[Union[Dict[str, Any], list]]
        True if value is a dict or list, False otherwise
    """
    return isinstance(value, (dict, list))


def is_tuple_of_two_strings(value: Any) -> TypeGuard[tuple[str, str]]:
    """
    Runtime type guard to validate tuple of two strings.

    This function tells static type checkers that isinstance checks for
    tuples of two strings are intentional runtime validation.

    Parameters
    ----------
    value : Any
        The value to check

    Returns
    -------
    TypeGuard[tuple[str, str]]
        True if value is a tuple of exactly two strings, False otherwise
    """
    if not isinstance(value, tuple):
        return False
    # Cast to help type checker understand we're working with a tuple
    tuple_value = cast(tuple[str, str], value)
    # Check length and element types
    return len(tuple_value) == 2 and isinstance(value[0], str) and isinstance(value[1], str)
