#!/usr/bin/env python3
"""
Message Queue Service - Service Layer Architecture
===============================================

<!-- SSOT Domain: integration -->

Service for managing message queues with persistence and routing.

Author: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-16
Refactored from messaging_core.py for V2 compliance (file size limits)
"""

import json
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Use relative imports for V2 compliance
from ..messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, MessageStatus
)

logger = logging.getLogger(__name__)


class MessageQueueService:
    """Service for managing message queues with persistence and routing."""

    def __init__(self, queue_dir: str = "message_queues"):
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(exist_ok=True)
        self._lock = threading.Lock()

    def enqueue_message(self, message: UnifiedMessage) -> bool:
        """Add message to appropriate queue with persistence."""
        try:
            with self._lock:
                queue_file = self._get_queue_file(message.recipient)
                queue_data = self._load_queue(queue_file)

                message_data = {
                    'id': str(message.id),
                    'content': message.content,
                    'sender': message.sender,
                    'recipient': message.recipient,
                    'message_type': message.message_type.value,
                    'priority': message.priority.value,
                    'tags': [tag.value for tag in message.tags],
                    'metadata': message.metadata,
                    'timestamp': message.timestamp.isoformat(),
                    'status': MessageStatus.QUEUED.value
                }

                queue_data['messages'].append(message_data)
                self._save_queue(queue_file, queue_data)

            logger.info(f"✅ Message {message.id} queued for {message.recipient}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to enqueue message: {e}")
            return False

    def dequeue_message(self, recipient: str) -> Optional[UnifiedMessage]:
        """Retrieve next message from queue."""
        try:
            with self._lock:
                queue_file = self._get_queue_file(recipient)
                queue_data = self._load_queue(queue_file)

                if not queue_data['messages']:
                    return None

                # Get highest priority message first
                messages = queue_data['messages']
                messages.sort(key=lambda m: self._get_priority_weight(m['priority']), reverse=True)

                message_data = messages.pop(0)
                self._save_queue(queue_file, queue_data)

                return self._deserialize_message(message_data)

        except Exception as e:
            logger.error(f"❌ Failed to dequeue message: {e}")
            return None

    def _get_queue_file(self, recipient: str) -> Path:
        """Get queue file path for recipient."""
        return self.queue_dir / f"{recipient}_queue.json"

    def _load_queue(self, queue_file: Path) -> Dict[str, Any]:
        """Load queue data from file."""
        if not queue_file.exists():
            return {'messages': []}

        try:
            with open(queue_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {'messages': []}

    def _save_queue(self, queue_file: Path, queue_data: Dict[str, Any]) -> None:
        """Save queue data to file."""
        with open(queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)

    def _get_priority_weight(self, priority: str) -> int:
        """Get priority weight for sorting."""
        weights = {
            UnifiedMessagePriority.URGENT.value: 3,
            UnifiedMessagePriority.REGULAR.value: 2,
            'normal': 1,
            'low': 0
        }
        return weights.get(priority, 1)

    def _deserialize_message(self, message_data: Dict[str, Any]) -> UnifiedMessage:
        """Convert queue data back to UnifiedMessage."""
        return UnifiedMessage(
            id=message_data['id'],
            content=message_data['content'],
            sender=message_data['sender'],
            recipient=message_data['recipient'],
            message_type=UnifiedMessageType(message_data['message_type']),
            priority=UnifiedMessagePriority(message_data['priority']),
            tags=[UnifiedMessageTag(tag) for tag in message_data.get('tags', [])],
            metadata=message_data.get('metadata', {}),
            timestamp=datetime.fromisoformat(message_data['timestamp'])
        )