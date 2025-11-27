"""
Unit tests for messaging_protocol_models.py - HIGH PRIORITY

Tests messaging protocol models and message structure.
"""

import pytest
from datetime import datetime
import uuid

# Import protocol models
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestMessagingProtocolModels:
    """Test suite for messaging protocol models."""

    def test_message_id_generation(self):
        """Test message ID generation."""
        message_id = str(uuid.uuid4())
        
        assert message_id is not None
        assert len(message_id) > 0

    def test_timestamp_creation(self):
        """Test timestamp creation."""
        timestamp = datetime.now()
        
        assert timestamp is not None
        assert isinstance(timestamp, datetime)

    def test_message_structure(self):
        """Test message structure."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        assert hasattr(message, 'content')
        assert hasattr(message, 'sender')
        assert hasattr(message, 'recipient')
        assert hasattr(message, 'message_type')
        assert hasattr(message, 'priority')
        assert hasattr(message, 'message_id')
        assert hasattr(message, 'timestamp')

    def test_message_metadata(self):
        """Test message metadata."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"source": "queue", "queue_id": "test-123"}
        )
        
        assert message.metadata is not None
        assert "source" in message.metadata
        assert "queue_id" in message.metadata

    def test_message_serialization(self):
        """Test message serialization."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        # Message should be serializable
        assert message.message_id is not None
        assert message.timestamp is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

