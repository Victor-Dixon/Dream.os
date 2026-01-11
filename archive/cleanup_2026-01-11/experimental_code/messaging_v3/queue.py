#!/usr/bin/env python3
"""
Simple Message Queue - Clean Implementation
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from message import Message

logger = logging.getLogger(__name__)


class MessageQueue:
    """Simple JSON-based message queue."""

    def __init__(self, queue_file: str = "messaging_v3/queue.json"):
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(exist_ok=True)
        self._messages: List[Message] = []
        self._load_queue()

    def _load_queue(self):
        """Load queue from file."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                    self._messages = [Message.from_dict(msg) for msg in data]
                logger.info(f"Loaded {len(self._messages)} messages from queue")
            except Exception as e:
                logger.error(f"Failed to load queue: {e}")
                self._messages = []
        else:
            self._messages = []

    def _save_queue(self):
        """Save queue to file."""
        try:
            data = [msg.to_dict() for msg in self._messages]
            with open(self.queue_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save queue: {e}")

    def enqueue(self, message: Message) -> str:
        """Add message to queue."""
        self._messages.append(message)
        self._save_queue()
        logger.info(f"Enqueued message {message.id} to {message.recipient}")
        return message.id

    def dequeue(self, count: int = 1) -> List[Message]:
        """Get and remove messages from queue."""
        if not self._messages:
            return []

        # Get oldest messages
        messages = self._messages[:count]
        self._messages = self._messages[count:]

        # Mark as delivered
        for msg in messages:
            msg.delivered_at = datetime.now()

        self._save_queue()
        logger.info(f"Dequeued {len(messages)} messages")
        return messages

    def peek(self, count: int = 1) -> List[Message]:
        """Look at messages without removing them."""
        return self._messages[:count]

    def count(self) -> int:
        """Get queue size."""
        return len(self._messages)

    def clear(self):
        """Clear all messages."""
        self._messages = []
        self._save_queue()
        logger.info("Queue cleared")

    def get_by_recipient(self, recipient: str) -> List[Message]:
        """Get messages for specific recipient."""
        return [msg for msg in self._messages if msg.recipient == recipient]

    def remove_delivered(self):
        """Remove messages that have been delivered."""
        original_count = len(self._messages)
        self._messages = [msg for msg in self._messages if msg.delivered_at is None]
        if len(self._messages) != original_count:
            self._save_queue()
            logger.info(f"Removed {original_count - len(self._messages)} delivered messages")