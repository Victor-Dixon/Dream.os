#!/usr/bin/env python3
"""
Cookie Repository Interface - Data Access Contract
==================================================

<!-- SSOT Domain: thea -->

Repository interface for cookie data access.
Defines the contract for cookie storage and retrieval operations.

V2 Compliance: Repository pattern, dependency injection ready.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ...domain.models import CookieData


class ICookieRepository(Protocol):
    """
    Interface for cookie data access operations.

    This interface abstracts cookie storage and retrieval,
    allowing different implementations (secure, plain, in-memory).
    """

    @abstractmethod
    def save_cookies(self, cookies: CookieData) -> bool:
        """
        Save cookie data to persistent storage.

        Args:
            cookies: Cookie data to save

        Returns:
            True if saved successfully, False otherwise
        """
        pass

    @abstractmethod
    def load_cookies(self) -> Optional[CookieData]:
        """
        Load cookie data from persistent storage.

        Returns:
            CookieData if found and valid, None otherwise
        """
        pass

    @abstractmethod
    def delete_cookies(self) -> bool:
        """
        Delete stored cookie data.

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    def has_valid_cookies(self) -> bool:
        """
        Check if valid, non-expired cookies exist.

        Returns:
            True if valid cookies exist, False otherwise
        """
        pass

    @abstractmethod
    def get_storage_type(self) -> str:
        """
        Get the type of storage mechanism used.

        Returns:
            String identifier for storage type (e.g., "secure_encrypted")
        """
        pass