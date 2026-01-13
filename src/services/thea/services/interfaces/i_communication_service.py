#!/usr/bin/env python3
"""
Communication Service Interface - Message Communication Business Logic
======================================================================

<!-- SSOT Domain: thea -->

Service interface for Thea communication operations.
Defines the contract for message sending and response handling.

V2 Compliance: Business logic interface, dependency injection ready.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ...domain.models import CommunicationResult, TheaMessage, TheaResponse


class ICommunicationService(Protocol):
    """
    Interface for Thea communication operations.

    This interface defines the business logic for message communication,
    abstracting away infrastructure details like browser automation and parsing.
    """

    @abstractmethod
    def send_message(self,
                    content: str,
                    priority: str = "normal",
                    metadata: Optional[dict] = None) -> CommunicationResult:
        """
        Send a message to Thea and get the response.

        This is the main entry point for communication. It handles:
        - Message validation and creation
        - Authentication verification
        - Message delivery
        - Response extraction and validation
        - Conversation persistence

        Args:
            content: Message content to send
            priority: Message priority level
            metadata: Optional metadata for the message

        Returns:
            CommunicationResult with success status and data
        """
        pass

    @abstractmethod
    def send_message_async(self,
                          content: str,
                          priority: str = "normal",
                          metadata: Optional[dict] = None) -> str:
        """
        Send a message asynchronously and return a tracking ID.

        Args:
            content: Message content to send
            priority: Message priority level
            metadata: Optional metadata for the message

        Returns:
            Message ID for tracking the async operation
        """
        pass

    @abstractmethod
    def get_message_status(self, message_id: str) -> Optional[TheaMessage]:
        """
        Get the status of a sent message.

        Args:
            message_id: ID of the message to check

        Returns:
            TheaMessage with current status, or None if not found
        """
        pass

    @abstractmethod
    def get_response(self, message_id: str) -> Optional[TheaResponse]:
        """
        Get the response for a sent message.

        Args:
            message_id: ID of the message to get response for

        Returns:
            TheaResponse if available, None otherwise
        """
        pass

    @abstractmethod
    def wait_for_response(self,
                         message_id: str,
                         timeout_seconds: int = 120) -> Optional[TheaResponse]:
        """
        Wait for a response to a message with timeout.

        Args:
            message_id: ID of the message to wait for
            timeout_seconds: Maximum time to wait in seconds

        Returns:
            TheaResponse if received within timeout, None otherwise
        """
        pass

    @abstractmethod
    def validate_message_content(self, content: str) -> bool:
        """
        Validate message content before sending.

        Args:
            content: Message content to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    @abstractmethod
    def get_recent_conversations(self, limit: int = 10) -> list:
        """
        Get recent conversation history.

        Args:
            limit: Maximum number of conversations to return

        Returns:
            List of recent conversations
        """
        pass

    @abstractmethod
    def search_conversations(self, query: str, limit: int = 20) -> list:
        """
        Search conversation history by content.

        Args:
            query: Search query string
            limit: Maximum results to return

        Returns:
            List of matching conversations
        """
        pass