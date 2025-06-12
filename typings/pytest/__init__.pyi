from __future__ import annotations

from typing import Type, Pattern, overload
from types import TracebackType
from _pytest.fixtures import fixture
from _pytest.mark import MARK_GEN as mark
from _pytest.monkeypatch import MonkeyPatch
from _pytest.outcomes import fail, importorskip, skip

# Define raises context manager with proper attributes

class RaisesContext:
    value: BaseException
    type: Type[BaseException]
    tb: TracebackType

    def __enter__(self) -> RaisesContext: ...
    def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> bool: ...

@overload
def raises(
    expected_exception: Type[BaseException] | tuple[Type[BaseException], ...],
) -> RaisesContext: ...
@overload
def raises(
    expected_exception: Type[BaseException] | tuple[Type[BaseException], ...],
    *,
    match: str | Pattern[str] | None = None,
) -> RaisesContext: ...

parametrize = mark.parametrize

__all__ = [
    "fixture",
    "mark",
    "parametrize",
    "raises",
    "MonkeyPatch",
    "fail",
    "skip",
    "importorskip",
    "RaisesContext",
]
