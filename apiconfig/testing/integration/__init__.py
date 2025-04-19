# -*- coding: utf-8 -*-
"""
Integration testing utilities for apiconfig.

This package provides tools for setting up and running integration tests,
including mock servers and test fixtures.
"""

from .servers import configure_mock_response

__all__ = [
    "configure_mock_response",
]
