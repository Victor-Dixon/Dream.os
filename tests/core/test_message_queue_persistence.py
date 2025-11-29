"""
Unit tests for message_queue_persistence.py - HIGH PRIORITY

Comprehensive tests for FileQueuePersistence, QueueEntry, and persistence operations.
Target: ≥85% coverage, 12+ test methods.
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
import uuid
import sys
from unittest.mock import MagicMock

# Add project root to path
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
        assert entry.updated_at == now
        assert entry.metadata == {}

    def test_entry_creation_with_metadata(self):
        """Test creating entry with metadata."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now,
            metadata={"key": "value"}
        )
        
        assert entry.metadata == {"key": "value"}

    def test_entry_to_dict(self):
        """Test entry serialization to dict."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now,
            metadata={"key": "value"}
        )
        
        result = entry.to_dict()
        
        assert result["message"] == {"content": "test"}
        assert result["queue_id"] == "test-id"
        assert result["priority_score"] == 0.8
        assert result["status"] == "PENDING"
        assert result["metadata"] == {"key": "value"}
        assert "created_at" in result
        assert "updated_at" in result

    def test_entry_to_dict_with_datetime_isoformat(self):
        """Test entry to_dict handles datetime objects."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id="test-id",
            priority_score=0.5,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        result = entry.to_dict()
        
        # Should convert datetime to ISO format string
        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)

    def test_entry_from_dict(self):
        """Test creating entry from dictionary."""
        now = datetime.now()
        data = {
            "message": {"content": "test"},
            "queue_id": "test-id",
            "priority_score": 0.8,
            "status": "PENDING",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "metadata": {"key": "value"}
        }
        
        entry = QueueEntry.from_dict(data)
        
        assert entry.message == {"content": "test"}
        assert entry.queue_id == "test-id"
        assert entry.priority_score == 0.8
        assert entry.status == "PENDING"
        assert entry.metadata == {"key": "value"}

    def test_entry_from_dict_without_metadata(self):
        """Test creating entry from dict without metadata."""
        now = datetime.now()
        data = {
            "message": {"content": "test"},
            "queue_id": "test-id",
            "priority_score": 0.5,
            "status": "PENDING",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        entry = QueueEntry.from_dict(data)
        
        assert entry.metadata == {}


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
        assert persistence.lock_manager is None

    def test_persistence_initialization_with_lock_manager(self, temp_queue_file):
        """Test persistence initialization with lock manager."""
        mock_lock = MagicMock()
        persistence = FileQueuePersistence(temp_queue_file, lock_manager=mock_lock)
        
        assert persistence.lock_manager == mock_lock

    def test_load_entries_empty_file(self, persistence):
        """Test loading from empty/non-existent file."""
        entries = persistence.load_entries()
        
        assert isinstance(entries, list)
        assert len(entries) == 0

    def test_load_entries_success(self, persistence, temp_queue_file):
        """Test loading entries from file."""
        now = datetime.now()
        entries_data = [
            {
                "message": {"content": "test1", "to": "Agent-1"},
                "queue_id": str(uuid.uuid4()),
                "priority_score": 0.8,
                "status": "PENDING",
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
                "metadata": {}
            },
            {
                "message": {"content": "test2", "to": "Agent-2"},
                "queue_id": str(uuid.uuid4()),
                "priority_score": 0.7,
                "status": "PENDING",
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
                "metadata": {}
            }
        ]
        
        with open(temp_queue_file, 'w', encoding='utf-8') as f:
            json.dump(entries_data, f)
        
        loaded = persistence.load_entries()
        
        assert len(loaded) == 2
        assert loaded[0].message["content"] == "test1"
        assert loaded[1].message["content"] == "test2"

    def test_load_entries_json_decode_error(self, persistence, temp_queue_file):
        """Test loading entries with invalid JSON."""
        with open(temp_queue_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")
        
        entries = persistence.load_entries()
        
        assert isinstance(entries, list)
        assert len(entries) == 0

    def test_load_entries_key_error(self, persistence, temp_queue_file):
        """Test loading entries with missing required fields."""
        invalid_data = [{"queue_id": "test-id"}]  # Missing required fields
        
        with open(temp_queue_file, 'w', encoding='utf-8') as f:
            json.dump(invalid_data, f)
        
        entries = persistence.load_entries()
        
        # Should handle KeyError gracefully
        assert isinstance(entries, list)

    def test_save_entries_success(self, persistence):
        """Test saving entries to file."""
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
        
        persistence.save_entries(entries)
        
        # Verify file was created and contains data
        assert persistence.queue_file.exists()
        loaded = persistence.load_entries()
        assert len(loaded) == 2

    def test_save_entries_empty_list(self, persistence):
        """Test saving empty entries list."""
        persistence.save_entries([])
        
        loaded = persistence.load_entries()
        assert len(loaded) == 0

    def test_save_entries_exception(self, persistence):
        """Test save_entries raises exception on error."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": "test"},
                queue_id="test-id",
                priority_score=0.5,
                status="PENDING",
                created_at=now,
                updated_at=now
            )
        ]
        
        # Make file read-only to cause write error
        persistence.queue_file.parent.mkdir(parents=True, exist_ok=True)
        persistence.queue_file.touch()
        persistence.queue_file.chmod(0o444)  # Read-only
        
        try:
            with pytest.raises(Exception):
                persistence.save_entries(entries)
        finally:
            # Restore permissions for cleanup
            persistence.queue_file.chmod(0o644)

    def test_atomic_operation_without_lock_manager(self, persistence):
        """Test atomic operation without lock manager."""
        def operation():
            return "test_result"
        
        result = persistence.atomic_operation(operation)
        
        assert result == "test_result"

    def test_atomic_operation_with_lock_manager(self, temp_queue_file):
        """Test atomic operation with lock manager."""
        mock_lock = MagicMock()
        mock_lock.atomic_operation.return_value = "locked_result"
        persistence = FileQueuePersistence(temp_queue_file, lock_manager=mock_lock)
        
        def operation():
            return "test_result"
        
        result = persistence.atomic_operation(operation)
        
        assert result == "locked_result"
        mock_lock.atomic_operation.assert_called_once_with(temp_queue_file, operation)

    def test_save_and_load_roundtrip(self, persistence):
        """Test save and load roundtrip preserves data."""
        now = datetime.now()
        original_entries = [
            QueueEntry(
                message={"content": "test1", "to": "Agent-1"},
                queue_id="id-1",
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now,
                metadata={"key": "value"}
            ),
            QueueEntry(
                message={"content": "test2", "to": "Agent-2"},
                queue_id="id-2",
                priority_score=0.7,
                status="PROCESSING",
                created_at=now,
                updated_at=now
            )
        ]
        
        persistence.save_entries(original_entries)
        loaded_entries = persistence.load_entries()
        
        assert len(loaded_entries) == 2
        assert loaded_entries[0].queue_id == "id-1"
        assert loaded_entries[0].priority_score == 0.8
        assert loaded_entries[0].metadata == {"key": "value"}
        assert loaded_entries[1].queue_id == "id-2"
        assert loaded_entries[1].status == "PROCESSING"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
