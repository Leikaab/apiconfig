from __future__ import annotations

from types import TracebackType
from typing import Pattern, Type, overload

from _pytest.fixtures import fixture
from _pytest.mark import MARK_GEN as mark
from _pytest.mark.structures import MarkDecorator
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
skipif: MarkDecorator = mark.skipif
asyncio: MarkDecorator = mark.asyncio

__all__ = [
    "fixture",
    "mark",
    "parametrize",
    "skipif",
    "asyncio",
    "raises",
    "MonkeyPatch",
    "fail",
    "skip",
    "importorskip",
    "RaisesContext",
]
