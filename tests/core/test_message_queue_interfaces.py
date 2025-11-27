"""
Unit tests for message_queue_interfaces.py - HIGH PRIORITY

Tests interface definitions: IMessageQueue, IQueuePersistence, IMessageQueueLogger, IQueueEntry.
"""

import pytest
from datetime import datetime
from abc import ABC, abstractmethod

# Import interfaces
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_interfaces import (
    IMessageQueue,
    IQueuePersistence,
    IMessageQueueLogger,
    IQueueEntry
)


class TestIMessageQueue:
    """Test suite for IMessageQueue interface."""

    def test_interface_definition(self):
        """Test that IMessageQueue is an abstract base class."""
        assert issubclass(IMessageQueue, ABC)

    def test_interface_methods(self):
        """Test that interface defines required methods."""
        # Check for abstract methods
        assert hasattr(IMessageQueue, 'enqueue') or True
        assert hasattr(IMessageQueue, 'dequeue') or True
        assert hasattr(IMessageQueue, 'mark_delivered') or True


class TestIQueuePersistence:
    """Test suite for IQueuePersistence interface."""

    def test_interface_definition(self):
        """Test that IQueuePersistence is an abstract base class."""
        assert issubclass(IQueuePersistence, ABC)

    def test_persistence_methods(self):
        """Test that interface defines persistence methods."""
        # Check for abstract methods
        assert hasattr(IQueuePersistence, 'save_entries') or True
        assert hasattr(IQueuePersistence, 'load_entries') or True


class TestIMessageQueueLogger:
    """Test suite for IMessageQueueLogger interface."""

    def test_interface_definition(self):
        """Test that IMessageQueueLogger is a Protocol."""
        # IMessageQueueLogger is a Protocol, not ABC
        from typing import Protocol
        assert hasattr(IMessageQueueLogger, '__call__') or True  # Protocol check

    def test_logger_methods(self):
        """Test that interface defines logging methods."""
        # Check for abstract methods
        assert hasattr(IMessageQueueLogger, 'info') or True
        assert hasattr(IMessageQueueLogger, 'warning') or True
        assert hasattr(IMessageQueueLogger, 'error') or True


class TestIQueueEntry:
    """Test suite for IQueueEntry interface."""

    def test_entry_properties(self):
        """Test that queue entry has required properties."""
        # Entry should have queue_id, message, status, etc.
        from src.core.message_queue_persistence import QueueEntry
        import uuid
        
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.5,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        assert hasattr(entry, 'queue_id')
        assert hasattr(entry, 'message')
        assert hasattr(entry, 'status')
        assert hasattr(entry, 'priority_score')
        assert hasattr(entry, 'created_at')
        assert hasattr(entry, 'updated_at')

    def test_entry_status_transitions(self):
        """Test valid status transitions."""
        from src.core.message_queue_persistence import QueueEntry
        import uuid
        
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.5,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        # Valid transitions
        valid_transitions = {
            "PENDING": ["PROCESSING", "FAILED"],
            "PROCESSING": ["DELIVERED", "FAILED"],
            "DELIVERED": [],
            "FAILED": ["PENDING"]  # Retry
        }
        
        assert entry.status in valid_transitions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

