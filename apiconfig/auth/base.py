# -*- coding: utf-8 -*-
"""Abstract base class for authentication strategies."""

from abc import ABC, abstractmethod
from typing import Dict


class AuthStrategy(ABC):
    """Abstract base class for defining authentication strategies."""

    @abstractmethod
    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepare authentication headers for an HTTP request.

        Returns:
            A dictionary containing header names and values.
        """
        pass  # pragma: no cover

    @abstractmethod
    def prepare_request_params(self) -> Dict[str, str]:
        """
        Prepare authentication parameters for an HTTP request (e.g., query params).

        Returns:
            A dictionary containing parameter names and values.
        """
        pass  # pragma: no cover
