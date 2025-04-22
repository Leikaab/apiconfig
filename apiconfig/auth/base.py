# -*- coding: utf-8 -*-
"""Abstract base class for authentication strategies."""

from abc import ABC, abstractmethod
from typing import Dict


class AuthStrategy(ABC):
    """
    Abstract base class for defining authentication strategies.

    This class provides a common interface for different authentication
    methods (e.g., Basic Auth, Bearer Token, API Key). Subclasses must
    implement the abstract methods to provide the specific logic for
    preparing request headers and/or parameters.
    """

    @abstractmethod
    def prepare_request_headers(self) -> Dict[str, str]:
        """Prepare authentication headers for an HTTP request.

        This method should generate the necessary HTTP headers required
        by the specific authentication strategy.

        Raises
        ------
        AuthStrategyError
            If headers cannot be prepared (e.g., missing credentials).

        Returns
        -------
        Dict[str, str]
            A dictionary containing header names and values. An empty
            dictionary should be returned if the strategy does not require headers.
        """
        pass  # pragma: no cover

    @abstractmethod
    def prepare_request_params(self) -> Dict[str, str]:
        """Prepare authentication parameters for an HTTP request (e.g., query params).

        This method should generate the necessary request parameters (like
        query parameters) required by the specific authentication strategy.

        Raises
        ------
        AuthStrategyError
            If parameters cannot be prepared (e.g., missing credentials).

        Returns
        -------
        Dict[str, str]
            A dictionary containing parameter names and values. An empty
            dictionary should be returned if the strategy does not require parameters.
        """
        pass  # pragma: no cover
