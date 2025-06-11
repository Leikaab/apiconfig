from __future__ import annotations

from _pytest.fixtures import fixture
from _pytest.mark import MARK_GEN as mark
from _pytest.monkeypatch import MonkeyPatch
from _pytest.outcomes import fail, importorskip, skip
from _pytest.python_api import raises

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
]
