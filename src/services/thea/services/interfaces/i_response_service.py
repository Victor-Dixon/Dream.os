#!/usr/bin/env python3
"""
Response Service Interface - Response Extraction Business Logic
==============================================================

<!-- SSOT Domain: thea -->

Service interface for Thea response extraction operations.
Defines the contract for extracting and processing responses.

V2 Compliance: Business logic interface, dependency injection ready.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from ...domain.models import TheaResponse


class IResponseService(Protocol):
    """
    Interface for Thea response extraction and processing operations.

    This interface defines the business logic for response handling,
    abstracting away parsing strategies and extraction mechanisms.
    """

    @abstractmethod
    def extract_response(self, timeout_seconds: int = 120) -> Optional[TheaResponse]:
        """
        Extract a response from Thea using available strategies.

        This tries multiple extraction strategies in order until one succeeds:
        - Assistant message extraction
        - Article content extraction
        - Markdown content extraction
        - Message ID based extraction
        - Manual fallback extraction

        Args:
            timeout_seconds: Maximum time to wait for response

        Returns:
            TheaResponse if extraction successful, None otherwise
        """
        pass

    @abstractmethod
    def wait_for_response_appearance(self, timeout_seconds: int = 120) -> bool:
        """
        Wait for a response to appear on the page.

        Args:
            timeout_seconds: Maximum time to wait

        Returns:
            True if response appears within timeout, False otherwise
        """
        pass

    @abstractmethod
    def validate_response_content(self, response: TheaResponse) -> bool:
        """
        Validate that extracted response content is meaningful.

        Args:
            response: Response to validate

        Returns:
            True if response appears valid, False otherwise
        """
        pass

    @abstractmethod
    def calculate_response_confidence(self, response: TheaResponse) -> float:
        """
        Calculate confidence score for response extraction.

        Args:
            response: Response to analyze

        Returns:
            Confidence score between 0.0 and 1.0
        """
        pass

    @abstractmethod
    def get_available_strategies(self) -> List[str]:
        """
        Get list of available response extraction strategies.

        Returns:
            List of strategy names
        """
        pass

    @abstractmethod
    def try_strategy(self, strategy_name: str, timeout_seconds: int = 30) -> Optional[TheaResponse]:
        """
        Try a specific extraction strategy.

        Args:
            strategy_name: Name of strategy to try
            timeout_seconds: Timeout for this strategy

        Returns:
            TheaResponse if strategy succeeds, None otherwise
        """
        pass

    @abstractmethod
    def get_response_metadata(self, response: TheaResponse) -> dict:
        """
        Extract additional metadata from a response.

        Args:
            response: Response to analyze

        Returns:
            Dictionary of metadata about the response
        """
        pass