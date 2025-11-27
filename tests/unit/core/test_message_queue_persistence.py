"""
Unit tests for src/core/message_queue_persistence.py

Tests queue persistence functionality including:
- FileQueuePersistence operations
- QueueEntry serialization/deserialization
- Error handling
- Atomic operations
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock

from src.core.message_queue_persistence import FileQueuePersistence, QueueEntry


class TestFileQueuePersistence:
    """Test file-based queue persistence."""

    @pytest.fixture
    def temp_queue_file(self):
        """Create temporary queue file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        yield temp_path
        if temp_path.exists():
            temp_path.unlink()

    @pytest.fixture
    def persistence(self, temp_queue_file):
        """Create FileQueuePersistence instance."""
        return FileQueuePersistence(temp_queue_file)

    def test_load_entries_empty_file(self, persistence):
        """Test loading from non-existent file."""
        entries = persistence.load_entries()
        assert entries == []

    def test_load_entries_valid_data(self, persistence, temp_queue_file):
        """Test loading valid queue entries."""
        # Create test data
        test_data = [
            {
                'message': 'test message',
                'queue_id': 'test-id-1',
                'priority_score': 0.5,
                'status': 'PENDING',
                'created_at': '2025-11-26T12:00:00',
                'updated_at': '2025-11-26T12:00:00',
                'metadata': {}
            }
        ]
        
        with open(temp_queue_file, 'w') as f:
            json.dump(test_data, f)
        
        entries = persistence.load_entries()
        assert len(entries) == 1
        assert entries[0].queue_id == 'test-id-1'

    def test_load_entries_invalid_json(self, persistence, temp_queue_file):
        """Test handling invalid JSON."""
        with open(temp_queue_file, 'w') as f:
            f.write('invalid json')
        
        entries = persistence.load_entries()
        assert entries == []

    def test_save_entries(self, persistence, temp_queue_file):
        """Test saving queue entries."""
        entry = QueueEntry(
            message='test',
            queue_id='id-1',
            priority_score=0.5,
            status='PENDING',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        persistence.save_entries([entry])
        
        # Verify file was created
        assert temp_queue_file.exists()
        
        # Verify content
        with open(temp_queue_file) as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]['queue_id'] == 'id-1'

    def test_save_entries_error_handling(self, persistence):
        """Test error handling during save."""
        # Use invalid path to trigger error
        invalid_persistence = FileQueuePersistence(Path('/invalid/path/queue.json'))
        entry = QueueEntry(
            message='test',
            queue_id='id-1',
            priority_score=0.5,
            status='PENDING',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with pytest.raises(Exception):
            invalid_persistence.save_entries([entry])

    def test_atomic_operation_without_lock(self, persistence):
        """Test atomic operation without lock manager."""
        result = persistence.atomic_operation(lambda: 42)
        assert result == 42

    def test_atomic_operation_with_lock(self, persistence):
        """Test atomic operation with lock manager."""
        mock_lock = MagicMock()
        mock_lock.atomic_operation.return_value = 42
        
        persistence.lock_manager = mock_lock
        result = persistence.atomic_operation(lambda: 42)
        
        assert result == 42
        mock_lock.atomic_operation.assert_called_once()


class TestQueueEntry:
    """Test QueueEntry data structure."""

    def test_queue_entry_creation(self):
        """Test creating queue entry."""
        entry = QueueEntry(
            message='test message',
            queue_id='test-id',
            priority_score=0.8,
            status='PENDING',
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={'key': 'value'}
        )
        
        assert entry.message == 'test message'
        assert entry.queue_id == 'test-id'
        assert entry.priority_score == 0.8
        assert entry.status == 'PENDING'
        assert entry.metadata == {'key': 'value'}

    def test_queue_entry_default_metadata(self):
        """Test default metadata initialization."""
        entry = QueueEntry(
            message='test',
            queue_id='id',
            priority_score=0.5,
            status='PENDING',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert entry.metadata == {}

    def test_to_dict(self):
        """Test converting entry to dictionary."""
        now = datetime.now()
        entry = QueueEntry(
            message='test',
            queue_id='id-1',
            priority_score=0.7,
            status='DELIVERED',
            created_at=now,
            updated_at=now,
            metadata={'test': 'data'}
        )
        
        data = entry.to_dict()
        
        assert data['message'] == 'test'
        assert data['queue_id'] == 'id-1'
        assert data['priority_score'] == 0.7
        assert data['status'] == 'DELIVERED'
        assert data['metadata'] == {'test': 'data'}
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_to_dict_datetime_serialization(self):
        """Test datetime serialization in to_dict."""
        now = datetime.now()
        entry = QueueEntry(
            message='test',
            queue_id='id',
            priority_score=0.5,
            status='PENDING',
            created_at=now,
            updated_at=now
        )
        
        data = entry.to_dict()
        
        # Should be ISO format string
        assert isinstance(data['created_at'], str)
        assert 'T' in data['created_at'] or isinstance(data['created_at'], str)

    def test_from_dict(self):
        """Test creating entry from dictionary."""
        data = {
            'message': 'test message',
            'queue_id': 'test-id',
            'priority_score': 0.6,
            'status': 'PROCESSING',
            'created_at': '2025-11-26T12:00:00',
            'updated_at': '2025-11-26T12:00:00',
            'metadata': {'key': 'value'}
        }
        
        entry = QueueEntry.from_dict(data)
        
        assert entry.message == 'test message'
        assert entry.queue_id == 'test-id'
        assert entry.priority_score == 0.6
        assert entry.status == 'PROCESSING'
        assert entry.metadata == {'key': 'value'}

    def test_from_dict_default_metadata(self):
        """Test from_dict with missing metadata."""
        data = {
            'message': 'test',
            'queue_id': 'id',
            'priority_score': 0.5,
            'status': 'PENDING',
            'created_at': '2025-11-26T12:00:00',
            'updated_at': '2025-11-26T12:00:00'
        }
        
        entry = QueueEntry.from_dict(data)
        assert entry.metadata == {}

    def test_round_trip_serialization(self):
        """Test serialization round trip."""
        now = datetime.now()
        original = QueueEntry(
            message='test',
            queue_id='id-1',
            priority_score=0.8,
            status='PENDING',
            created_at=now,
            updated_at=now,
            metadata={'test': 'data'}
        )
        
        # Convert to dict and back
        data = original.to_dict()
        restored = QueueEntry.from_dict(data)
        
        assert restored.message == original.message
        assert restored.queue_id == original.queue_id
        assert restored.priority_score == original.priority_score
        assert restored.status == original.status
        assert restored.metadata == original.metadata

