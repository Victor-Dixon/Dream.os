#!/usr/bin/env python3
"""
Thea Service Coordinator - Main Orchestrator
===========================================

<!-- SSOT Domain: thea -->

Main coordinator for Thea service operations.
Provides the public API that combines all Thea functionality.

V2 Compliance: Clean public API with dependency injection.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from typing import Optional

from .domain.models import CommunicationResult
from .services.interfaces.i_authentication_service import IAuthenticationService
from .services.interfaces.i_communication_service import ICommunicationService


class TheaServiceCoordinator:
    """
    Main coordinator for Thea service operations.

    This is the main entry point that combines authentication and communication services.
    Provides a clean public API while delegating to specialized services.
    """

    def __init__(self,
                 authentication_service: IAuthenticationService,
                 communication_service: ICommunicationService,
                 default_target_url: str = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"):
        """
        Initialize Thea service coordinator.

        Args:
            authentication_service: Service for authentication operations
            communication_service: Service for communication operations
            default_target_url: Default Thea URL to use
        """
        self.auth_service = authentication_service
        self.comm_service = communication_service
        self.default_target_url = default_target_url

    def send_message(self,
                    message: str,
                    target_url: Optional[str] = None,
                    priority: str = "normal",
                    metadata: Optional[dict] = None) -> CommunicationResult:
        """
        Send a message to Thea and get the response.

        This is the main public API method that handles the complete flow:
        1. Authentication (if needed)
        2. Message sending
        3. Response extraction
        4. Conversation persistence

        Args:
            message: Message content to send
            target_url: Target URL (uses default if not specified)
            priority: Message priority level
            metadata: Optional metadata for the message

        Returns:
            CommunicationResult with success status and data
        """
        target = target_url or self.default_target_url

        # Ensure authentication for the target URL
        if not self.auth_service.ensure_authenticated(target):
            return CommunicationResult(
                success=False,
                message=type('Message', (), {'content': message, 'priority': priority, 'metadata': metadata or {}})(),
                error_message="Authentication failed"
            )

        # Send the message and get response
        return self.comm_service.send_message(
            content=message,
            priority=priority,
            metadata=metadata
        )

    def authenticate(self, target_url: Optional[str] = None) -> bool:
        """
        Ensure authentication for the target URL.

        Args:
            target_url: URL to authenticate with (uses default if not specified)

        Returns:
            True if authenticated, False otherwise
        """
        target = target_url or self.default_target_url
        return self.auth_service.ensure_authenticated(target)

    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        return self.auth_service.is_authenticated()

    def logout(self) -> bool:
        """
        Perform logout and cleanup.

        Returns:
            True if logout successful, False otherwise
        """
        return self.auth_service.logout()

    def get_recent_conversations(self, limit: int = 10) -> list:
        """
        Get recent conversation history.

        Args:
            limit: Maximum number of conversations to return

        Returns:
            List of recent conversations
        """
        return self.comm_service.get_recent_conversations(limit)

    def search_conversations(self, query: str, limit: int = 20) -> list:
        """
        Search conversation history by content.

        Args:
            query: Search query string
            limit: Maximum results to return

        Returns:
            List of matching conversations
        """
        return self.comm_service.search_conversations(query, limit)

    def get_message_status(self, message_id: str):
        """
        Get the status of a sent message.

        Args:
            message_id: ID of the message to check

        Returns:
            Message status information, or None if not found
        """
        return self.comm_service.get_message_status(message_id)

    def get_response(self, message_id: str):
        """
        Get the response for a sent message.

        Args:
            message_id: ID of the message to get response for

        Returns:
            Response data, or None if not available
        """
        return self.comm_service.get_response(message_id)

    def wait_for_response(self, message_id: str, timeout_seconds: int = 120):
        """
        Wait for a response to a message with timeout.

        Args:
            message_id: ID of the message to wait for
            timeout_seconds: Maximum time to wait in seconds

        Returns:
            Response data if received within timeout, None otherwise
        """
        return self.comm_service.wait_for_response(message_id, timeout_seconds)

    def send_message_async(self, message: str, priority: str = "normal", metadata: Optional[dict] = None) -> str:
        """
        Send a message asynchronously and return a tracking ID.

        Args:
            message: Message content to send
            priority: Message priority level
            metadata: Optional metadata for the message

        Returns:
            Message ID for tracking the async operation
        """
        return self.comm_service.send_message_async(message, priority, metadata)

    def get_authentication_context(self):
        """
        Get current authentication context and status.

        Returns:
            Authentication context information
        """
        return self.auth_service.get_authentication_context()


# Factory function for easy instantiation
def create_thea_coordinator(**kwargs):
    """
    Factory function to create a Thea coordinator.

    Uses the DI container to wire all dependencies.

    Args:
        **kwargs: Configuration options for the DI container

    Returns:
        TheaServiceCoordinator instance
    """
    from .di_container import create_thea_container

    container = create_thea_container(**kwargs)

    if not container.is_fully_operational():
        status = container.get_status_report()
        missing = [k for k, v in status.items() if isinstance(v, bool) and not v]
        raise RuntimeError(f"Thea container not fully operational. Missing: {missing}")

    return container.coordinator


# Convenience functions for common use cases
def create_default_thea_coordinator():
    """
    Create a Thea coordinator with default settings.

    Returns:
        TheaServiceCoordinator with default configuration
    """
    return create_thea_coordinator()


def quick_send_message(message: str, **kwargs) -> CommunicationResult:
    """
    Quick utility to send a message with default settings.

    Args:
        message: Message to send
        **kwargs: Additional configuration options

    Returns:
        CommunicationResult
    """
    coordinator = create_thea_coordinator(**kwargs)
    return coordinator.send_message(message)