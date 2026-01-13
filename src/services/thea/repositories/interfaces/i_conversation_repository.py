#!/usr/bin/env python3
"""
Conversation Repository Interface - Conversation Data Access
===========================================================

<!-- SSOT Domain: thea -->

Repository interface for conversation data persistence.
Defines the contract for storing and retrieving conversation history.

V2 Compliance: Repository pattern for data persistence.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from ...domain.models import TheaConversation


class IConversationRepository(Protocol):
    """
    Interface for conversation data access operations.

    This interface abstracts conversation storage and retrieval,
    allowing different persistence mechanisms (file, database, memory).
    """

    @abstractmethod
    def save_conversation(self, conversation: TheaConversation) -> bool:
        """
        Save a conversation to persistent storage.

        Args:
            conversation: Conversation to save

        Returns:
            True if saved successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_conversation(self, conversation_id: str) -> Optional[TheaConversation]:
        """
        Retrieve a conversation by ID.

        Args:
            conversation_id: Unique identifier of the conversation

        Returns:
            TheaConversation if found, None otherwise
        """
        pass

    @abstractmethod
    def get_recent_conversations(self, limit: int = 10) -> List[TheaConversation]:
        """
        Get recent conversations ordered by timestamp.

        Args:
            limit: Maximum number of conversations to return

        Returns:
            List of recent conversations (newest first)
        """
        pass

    @abstractmethod
    def get_conversations_by_message_id(self, message_id: str) -> List[TheaConversation]:
        """
        Get conversations containing a specific message.

        Args:
            message_id: Message identifier to search for

        Returns:
            List of conversations containing the message
        """
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation by ID.

        Args:
            conversation_id: Unique identifier of conversation to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_conversation_count(self) -> int:
        """
        Get total number of stored conversations.

        Returns:
            Total count of conversations
        """
        pass

    @abstractmethod
    def cleanup_old_conversations(self, days_to_keep: int = 30) -> int:
        """
        Remove conversations older than specified days.

        Args:
            days_to_keep: Number of days of conversations to retain

        Returns:
            Number of conversations deleted
        """
        pass

    @abstractmethod
    def search_conversations(self, query: str, limit: int = 20) -> List[TheaConversation]:
        """
        Search conversations by content.

        Args:
            query: Search query string
            limit: Maximum results to return

        Returns:
            List of matching conversations
        """
        pass