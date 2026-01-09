#!/usr/bin/env python3
"""
Authentication Service Interface - Authentication Business Logic
===============================================================

<!-- SSOT Domain: thea -->

Service interface for authentication operations.
Defines the contract for Thea authentication business logic.

V2 Compliance: Business logic interface, dependency injection ready.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ...domain.models import AuthenticationContext


class IAuthenticationService(Protocol):
    """
    Interface for Thea authentication operations.

    This interface defines the business logic for authentication,
    abstracting away infrastructure details like browser automation.
    """

    @abstractmethod
    def ensure_authenticated(self, target_url: str) -> bool:
        """
        Ensure the service is authenticated for the target URL.

        This is the main entry point for authentication. It handles:
        - Checking existing authentication status
        - Refreshing expired credentials
        - Performing login flow if needed

        Args:
            target_url: URL that requires authentication

        Returns:
            True if authenticated and ready, False otherwise
        """
        pass

    @abstractmethod
    def validate_current_session(self, target_url: str) -> bool:
        """
        Validate that the current session is still authenticated.

        Args:
            target_url: URL to validate authentication for

        Returns:
            True if session is valid, False otherwise
        """
        pass

    @abstractmethod
    def refresh_authentication(self, target_url: str) -> bool:
        """
        Force refresh of authentication credentials.

        Args:
            target_url: URL to refresh authentication for

        Returns:
            True if refresh successful, False otherwise
        """
        pass

    @abstractmethod
    def perform_login_flow(self, target_url: str) -> bool:
        """
        Perform the complete login flow for authentication.

        Args:
            target_url: URL to authenticate with

        Returns:
            True if login successful, False otherwise
        """
        pass

    @abstractmethod
    def get_authentication_context(self) -> AuthenticationContext:
        """
        Get current authentication context and status.

        Returns:
            AuthenticationContext with current state
        """
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Quick check if currently authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        pass

    @abstractmethod
    def logout(self) -> bool:
        """
        Perform logout and cleanup authentication state.

        Returns:
            True if logout successful, False otherwise
        """
        pass