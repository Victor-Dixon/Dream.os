"""
Unit tests for message_queue_persistence.py - HIGH PRIORITY

Tests FileQueuePersistence, QueueEntry, and persistence operations.
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
import uuid

# Import persistence components
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_persistence import FileQueuePersistence, QueueEntry


class TestQueueEntry:
    """Test suite for QueueEntry class."""

    def test_entry_creation(self):
        """Test creating a queue entry."""
        message = {"content": "test", "to": "Agent-1"}
        queue_id = str(uuid.uuid4())
        now = datetime.now()
        
        entry = QueueEntry(
            message=message,
            queue_id=queue_id,
            priority_score=0.5,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        assert entry.message == message
        assert entry.queue_id == queue_id
        assert entry.priority_score == 0.5
        assert entry.status == "PENDING"
        assert entry.created_at == now

    def test_entry_serialization(self):
        """Test entry serialization to dict."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        # Entry should be serializable
        assert hasattr(entry, 'message')
        assert hasattr(entry, 'queue_id')


class TestFileQueuePersistence:
    """Test suite for FileQueuePersistence class."""

    @pytest.fixture
    def temp_queue_file(self):
        """Create temporary queue file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = Path(f.name)
        yield temp_path
        if temp_path.exists():
            temp_path.unlink()

    @pytest.fixture
    def persistence(self, temp_queue_file):
        """Create FileQueuePersistence instance."""
        return FileQueuePersistence(temp_queue_file)

    def test_persistence_initialization(self, persistence, temp_queue_file):
        """Test persistence initialization."""
        assert persistence.queue_file == temp_queue_file
        assert temp_queue_file.parent.exists()

    def test_save_and_load_entries(self, persistence):
        """Test saving and loading entries."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": "test1", "to": "Agent-1"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now
            ),
            QueueEntry(
                message={"content": "test2", "to": "Agent-2"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.7,
                status="PENDING",
                created_at=now,
                updated_at=now
            )
        ]
        
        # Save entries
        persistence.save_entries(entries)
        
        # Load entries
        loaded = persistence.load_entries()
        
        assert len(loaded) == 2
        assert loaded[0].message["content"] == "test1"
        assert loaded[1].message["content"] == "test2"

    def test_load_empty_file(self, persistence):
        """Test loading from empty file."""
        entries = persistence.load_entries()
        
        assert isinstance(entries, list)
        assert len(entries) == 0

    def test_atomic_operation(self, persistence):
        """Test atomic operations."""
        def operation():
            entries = persistence.load_entries()
            now = datetime.now()
            entries.append(QueueEntry(
                message={"content": "test"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.5,
                status="PENDING",
                created_at=now,
                updated_at=now
            ))
            persistence.save_entries(entries)
            return len(entries)
        
        result = persistence.atomic_operation(operation)
        
        assert result == 1

    def test_concurrent_access(self, persistence):
        """Test handling concurrent access."""
        # Simulate concurrent operations
        entries1 = persistence.load_entries()
        entries2 = persistence.load_entries()
        
        # Both should see same initial state
        assert len(entries1) == len(entries2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

