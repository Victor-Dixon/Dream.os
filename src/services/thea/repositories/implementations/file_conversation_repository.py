#!/usr/bin/env python3
"""
File Conversation Repository Implementation - Conversation Persistence
====================================================================

<!-- SSOT Domain: thea -->

Repository implementation for conversation data persistence using JSON files.
Stores conversations in timestamped files with search capabilities.

V2 Compliance: Repository pattern implementation for conversation data.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from ...domain.models import TheaConversation
from ..interfaces.i_conversation_repository import IConversationRepository


class FileConversationRepository(IConversationRepository):
    """
    File-based conversation repository implementation.

    Stores conversations as JSON files with timestamp-based naming.
    Provides search and cleanup capabilities.
    """

    def __init__(self, storage_dir: str = "thea_conversations"):
        """
        Initialize file conversation repository.

        Args:
            storage_dir: Directory to store conversation files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_conversation(self, conversation: TheaConversation) -> bool:
        """
        Save a conversation to a JSON file.

        Args:
            conversation: Conversation to save

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            filename = f"conversation_{conversation.conversation_id}_{conversation.started_at.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.storage_dir / filename

            # Prepare data for JSON serialization
            data = {
                "conversation_id": conversation.conversation_id,
                "message": {
                    "message_id": conversation.message.message_id,
                    "content": conversation.message.content,
                    "priority": conversation.message.priority.value,
                    "timestamp": conversation.message.timestamp.isoformat(),
                    "status": conversation.message.status.value,
                    "metadata": conversation.message.metadata
                },
                "response": None,
                "started_at": conversation.started_at.isoformat(),
                "completed_at": conversation.completed_at.isoformat() if conversation.completed_at else None,
                "total_duration_seconds": conversation.total_duration_seconds
            }

            if conversation.response:
                data["response"] = {
                    "content": conversation.response.content,
                    "message_id": conversation.response.message_id,
                    "response_id": conversation.response.response_id,
                    "timestamp": conversation.response.timestamp.isoformat(),
                    "confidence_score": conversation.response.confidence_score,
                    "processing_time_seconds": conversation.response.processing_time_seconds,
                    "metadata": conversation.response.metadata
                }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"💾 Saved conversation: {filepath}")
            return True

        except Exception as e:
            print(f"❌ Failed to save conversation: {e}")
            return False

    def get_conversation(self, conversation_id: str) -> Optional[TheaConversation]:
        """
        Retrieve a conversation by ID.

        Args:
            conversation_id: Unique identifier of the conversation

        Returns:
            TheaConversation if found, None otherwise
        """
        try:
            # Find the conversation file
            pattern = f"conversation_{conversation_id}_*.json"
            matching_files = list(self.storage_dir.glob(pattern))

            if not matching_files:
                return None

            # Use the most recent file if multiple exist
            filepath = max(matching_files, key=lambda f: f.stat().st_mtime)

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruct conversation
            conversation = self._data_to_conversation(data)
            return conversation

        except Exception as e:
            print(f"❌ Failed to load conversation {conversation_id}: {e}")
            return None

    def get_recent_conversations(self, limit: int = 10) -> List[TheaConversation]:
        """
        Get recent conversations ordered by timestamp.

        Args:
            limit: Maximum number of conversations to return

        Returns:
            List of recent conversations (newest first)
        """
        try:
            conversations = []

            # Get all conversation files
            conversation_files = list(self.storage_dir.glob("conversation_*.json"))

            # Sort by modification time (newest first)
            conversation_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

            for filepath in conversation_files[:limit]:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    conversation = self._data_to_conversation(data)
                    if conversation:
                        conversations.append(conversation)

                except Exception as e:
                    print(f"⚠️ Failed to load conversation from {filepath}: {e}")
                    continue

            return conversations

        except Exception as e:
            print(f"❌ Failed to get recent conversations: {e}")
            return []

    def get_conversations_by_message_id(self, message_id: str) -> List[TheaConversation]:
        """
        Get conversations containing a specific message.

        Args:
            message_id: Message identifier to search for

        Returns:
            List of conversations containing the message
        """
        try:
            conversations = []

            for filepath in self.storage_dir.glob("conversation_*.json"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if data.get("message", {}).get("message_id") == message_id:
                        conversation = self._data_to_conversation(data)
                        if conversation:
                            conversations.append(conversation)

                except Exception:
                    continue

            return conversations

        except Exception as e:
            print(f"❌ Failed to search conversations by message ID: {e}")
            return []

    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation by ID.

        Args:
            conversation_id: Unique identifier of conversation to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            pattern = f"conversation_{conversation_id}_*.json"
            matching_files = list(self.storage_dir.glob(pattern))

            deleted = False
            for filepath in matching_files:
                filepath.unlink()
                deleted = True
                print(f"🗑️ Deleted conversation file: {filepath}")

            return deleted

        except Exception as e:
            print(f"❌ Failed to delete conversation {conversation_id}: {e}")
            return False

    def get_conversation_count(self) -> int:
        """
        Get total number of stored conversations.

        Returns:
            Total count of conversations
        """
        try:
            return len(list(self.storage_dir.glob("conversation_*.json")))
        except Exception:
            return 0

    def cleanup_old_conversations(self, days_to_keep: int = 30) -> int:
        """
        Remove conversations older than specified days.

        Args:
            days_to_keep: Number of days of conversations to retain

        Returns:
            Number of conversations deleted
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            deleted_count = 0

            for filepath in self.storage_dir.glob("conversation_*.json"):
                try:
                    # Extract timestamp from filename
                    filename = filepath.name
                    # Format: conversation_{conversation_id}_{YYYYMMDD_HHMMSS}.json
                    timestamp_str = filename.split('_')[-1].replace('.json', '')
                    file_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

                    if file_date < cutoff_date:
                        filepath.unlink()
                        deleted_count += 1
                        print(f"🗑️ Cleaned up old conversation: {filepath}")

                except (ValueError, OSError) as e:
                    print(f"⚠️ Failed to process {filepath}: {e}")
                    continue

            print(f"🧹 Cleaned up {deleted_count} old conversations")
            return deleted_count

        except Exception as e:
            print(f"❌ Failed to cleanup old conversations: {e}")
            return 0

    def search_conversations(self, query: str, limit: int = 20) -> List[TheaConversation]:
        """
        Search conversations by content.

        Args:
            query: Search query string
            limit: Maximum results to return

        Returns:
            List of matching conversations
        """
        try:
            conversations = []
            query_lower = query.lower()

            for filepath in self.storage_dir.glob("conversation_*.json"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Search in message content
                    message_content = data.get("message", {}).get("content", "").lower()
                    response_content = ""
                    if data.get("response"):
                        response_content = data.get("response", {}).get("content", "").lower()

                    if query_lower in message_content or query_lower in response_content:
                        conversation = self._data_to_conversation(data)
                        if conversation:
                            conversations.append(conversation)

                            if len(conversations) >= limit:
                                break

                except Exception:
                    continue

            return conversations

        except Exception as e:
            print(f"❌ Failed to search conversations: {e}")
            return []

    def _data_to_conversation(self, data: dict) -> Optional[TheaConversation]:
        """
        Convert JSON data to TheaConversation object.

        Args:
            data: JSON data from file

        Returns:
            TheaConversation object, or None if invalid data
        """
        try:
            from ...domain.models import TheaMessage, TheaResponse
            from ...domain.enums import MessagePriority, MessageStatus

            # Reconstruct message
            message_data = data["message"]
            message = TheaMessage(
                content=message_data["content"],
                message_id=message_data["message_id"],
                priority=MessagePriority(message_data["priority"]),
                timestamp=datetime.fromisoformat(message_data["timestamp"]),
                status=MessageStatus(message_data["status"]),
                metadata=message_data.get("metadata", {})
            )

            # Reconstruct response if present
            response = None
            if data.get("response"):
                response_data = data["response"]
                response = TheaResponse(
                    content=response_data["content"],
                    message_id=response_data["message_id"],
                    response_id=response_data["response_id"],
                    timestamp=datetime.fromisoformat(response_data["timestamp"]),
                    confidence_score=response_data.get("confidence_score"),
                    processing_time_seconds=response_data.get("processing_time_seconds"),
                    metadata=response_data.get("metadata", {})
                )

            # Create conversation
            conversation = TheaConversation(
                message=message,
                response=response,
                conversation_id=data["conversation_id"],
                started_at=datetime.fromisoformat(data["started_at"]),
                completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
                total_duration_seconds=data.get("total_duration_seconds")
            )

            return conversation

        except Exception as e:
            print(f"❌ Failed to reconstruct conversation from data: {e}")
            return None