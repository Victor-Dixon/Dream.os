#!/usr/bin/env python3
"""
Message Deduplication Service - Prevent Duplicate Message Processing
===================================================================

<!-- SSOT Domain: integration -->

Strategic improvement to prevent duplicate message processing and coordination loops.
Implements message ID tracking with configurable retention and cleanup policies.

V2 Compliance: Service layer pattern with repository abstraction.

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-11
License: MIT
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Dict, Optional, Set

from src.core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class MessageDeduplicationService(BaseService):
    """
    Service for preventing duplicate message processing.

    Tracks seen message IDs with automatic cleanup of expired entries.
    Prevents coordination loops and duplicate work execution.
    """

    def __init__(self,
                 storage_path: str = "data/message_deduplication.json",
                 retention_hours: int = 24,
                 max_entries: int = 10000):
        """
        Initialize message deduplication service.

        Args:
            storage_path: Path to store seen message IDs
            retention_hours: Hours to retain message IDs
            max_entries: Maximum number of entries to keep
        """
        super().__init__("MessageDeduplicationService")

        self.storage_path = Path(storage_path)
        self.retention_seconds = retention_hours * 3600
        self.max_entries = max_entries

        # In-memory cache for fast lookups
        self._seen_messages: Dict[str, float] = {}
        self._last_cleanup = time.time()

        # Load existing data
        self._load_seen_messages()

    def is_duplicate(self, message_id: str) -> bool:
        """
        Check if a message ID has been seen before.

        Args:
            message_id: Message ID to check

        Returns:
            bool: True if message is duplicate, False otherwise
        """
        # Clean up expired entries periodically
        self._periodic_cleanup()

        # Check if message ID exists
        if message_id in self._seen_messages:
            logger.info(f"🚫 Duplicate message detected: {message_id}")
            return True

        # Mark as seen
        self._seen_messages[message_id] = time.time()
        self._save_seen_messages()

        return False

    def mark_seen(self, message_id: str) -> None:
        """
        Explicitly mark a message ID as seen.

        Args:
            message_id: Message ID to mark as seen
        """
        self._seen_messages[message_id] = time.time()
        self._save_seen_messages()

    def get_stats(self) -> Dict[str, int]:
        """
        Get deduplication statistics.

        Returns:
            Dict containing stats about seen messages
        """
        return {
            "total_seen": len(self._seen_messages),
            "max_entries": self.max_entries,
            "retention_hours": int(self.retention_seconds / 3600)
        }

    def force_cleanup(self) -> int:
        """
        Force cleanup of expired entries.

        Returns:
            int: Number of entries cleaned up
        """
        return self._cleanup_expired()

    def _periodic_cleanup(self) -> None:
        """Perform periodic cleanup of expired entries."""
        current_time = time.time()
        if current_time - self._last_cleanup > 3600:  # Clean up every hour
            cleaned = self._cleanup_expired()
            if cleaned > 0:
                logger.info(f"🧹 Cleaned up {cleaned} expired message IDs")
            self._last_cleanup = current_time

    def _cleanup_expired(self) -> int:
        """
        Clean up expired message entries.

        Returns:
            int: Number of entries cleaned up
        """
        current_time = time.time()
        expired_cutoff = current_time - self.retention_seconds

        # Find expired entries
        expired_ids = [
            msg_id for msg_id, timestamp in self._seen_messages.items()
            if timestamp < expired_cutoff
        ]

        # Remove expired entries
        for msg_id in expired_ids:
            del self._seen_messages[msg_id]

        # Enforce max entries limit (remove oldest)
        if len(self._seen_messages) > self.max_entries:
            # Sort by timestamp and keep newest
            sorted_entries = sorted(
                self._seen_messages.items(),
                key=lambda x: x[1],
                reverse=True
            )
            self._seen_messages = dict(sorted_entries[:self.max_entries])
            expired_ids.extend([
                msg_id for msg_id, _ in sorted_entries[self.max_entries:]
            ])

        if expired_ids:
            self._save_seen_messages()

        return len(expired_ids)

    def _load_seen_messages(self) -> None:
        """Load seen messages from storage."""
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self._seen_messages = {
                    msg_id: float(timestamp)
                    for msg_id, timestamp in data.items()
                }
                logger.info(f"📂 Loaded {len(self._seen_messages)} seen message IDs")
            else:
                logger.info("📂 No existing deduplication data found, starting fresh")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load deduplication data: {e}")
            self._seen_messages = {}

    def _save_seen_messages(self) -> None:
        """Save seen messages to storage."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                msg_id: str(timestamp)
                for msg_id, timestamp in self._seen_messages.items()
            }
            self.storage_path.write_text(
                json.dumps(data, indent=2, sort_keys=True),
                encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"❌ Failed to save deduplication data: {e}")


# Global instance for easy access
_deduplication_service: Optional[MessageDeduplicationService] = None


def get_message_deduplication_service() -> MessageDeduplicationService:
    """
    Get the global message deduplication service instance.

    Returns:
        MessageDeduplicationService: Global service instance
    """
    global _deduplication_service
    if _deduplication_service is None:
        _deduplication_service = MessageDeduplicationService()
    return _deduplication_service


def check_message_duplicate(message_id: str) -> bool:
    """
    Convenience function to check if a message is duplicate.

    Args:
        message_id: Message ID to check

    Returns:
        bool: True if duplicate, False otherwise
    """
    return get_message_deduplication_service().is_duplicate(message_id)