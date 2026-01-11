#!/usr/bin/env python3
"""
Core Message Model - Clean and Simple
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class Message:
    """Clean message representation."""

    id: str
    sender: str
    recipient: str
    content: str
    priority: str = "normal"
    message_type: str = "text"
    category: str = "direct"
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    delivered_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "priority": self.priority,
            "message_type": self.message_type,
            "category": self.category,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create from dictionary."""
        return cls(
            id=data["id"],
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            priority=data.get("priority", "normal"),
            message_type=data.get("message_type", "text"),
            category=data.get("category", "direct"),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            delivered_at=datetime.fromisoformat(data["delivered_at"]) if data.get("delivered_at") else None,
        )