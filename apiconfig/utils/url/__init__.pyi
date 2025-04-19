"""Type stubs for URL utilities."""

# Explicit re-exports required by mypy's no_implicit_reexport setting
from .parsing import add_query_params as add_query_params
from .parsing import get_query_params as get_query_params
from .parsing import parse_url as parse_url

__all__: list[str]
