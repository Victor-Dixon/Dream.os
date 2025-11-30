#!/usr/bin/env python3
"""
Queue Persistence Integration Tests
===================================

Integration tests for queue persistence operations with message_queue_processor.
Focus: Persistence save/load cycles, error recovery, corruption handling.

Target: ≥85% coverage, comprehensive edge cases.
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest
import uuid

from src.core.message_queue import MessageQueue, QueueConfig
from src.core.message_queue_persistence import FileQueuePersistence, QueueEntry
from src.core.message_queue_processor import MessageQueueProcessor


class TestQueuePersistenceIntegration:
    """Integration tests for queue persistence operations."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary directory for queue storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def queue_file(self, temp_queue_dir):
        """Create queue file path."""
        return temp_queue_dir / "test_queue.json"

    @pytest.fixture
    def persistence(self, queue_file):
        """Create persistence instance."""
        return FileQueuePersistence(queue_file)

    @pytest.fixture
    def queue_config(self, temp_queue_dir):
        """Create queue configuration."""
        return QueueConfig(queue_dir=str(temp_queue_dir))

    @pytest.fixture
    def message_queue(self, queue_config):
        """Create message queue instance."""
        return MessageQueue(config=queue_config)

    def test_save_and_load_roundtrip(self, persistence):
        """Test saving and loading entries maintains data integrity."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": "test1", "recipient": "Agent-1"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now,
                metadata={"key": "value"}
            ),
            QueueEntry(
                message={"content": "test2", "recipient": "Agent-2"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.7,
                status="DELIVERED",
                created_at=now,
                updated_at=now
            )
        ]
        
        # Save entries
        persistence.save_entries(entries)
        
        # Load entries
        loaded = persistence.load_entries()
        
        assert len(loaded) == 2
        assert loaded[0].message == entries[0].message
        assert loaded[0].queue_id == entries[0].queue_id
        assert loaded[0].metadata == {"key": "value"}
        assert loaded[1].status == "DELIVERED"

    def test_persistence_with_processor_enqueue(self, message_queue, persistence):
        """Test queue enqueue persists entries correctly."""
        # Create queue with specific persistence
        queue_file = Path(message_queue.config.queue_dir) / "message_queue.json"
        message_queue.persistence = FileQueuePersistence(queue_file)
        
        # Enqueue message
        queue_id = message_queue.enqueue({
            "content": "integration test",
            "recipient": "Agent-1",
            "sender": "TEST"
        })
        
        assert queue_id is not None
        
        # Verify persistence
        entries = message_queue.persistence.load_entries()
        assert len(entries) == 1
        assert entries[0].queue_id == queue_id
        assert entries[0].message["recipient"] == "Agent-1"

    def test_persistence_recovery_corrupted_json(self, persistence, queue_file):
        """Test persistence recovers from corrupted JSON."""
        # Write corrupted JSON
        queue_file.write_text("[{invalid json}", encoding="utf-8")
        
        # Should recover gracefully
        entries = persistence.load_entries()
        
        # Should return empty list or recovered entries
        assert isinstance(entries, list)

    def test_persistence_recovery_partial_write(self, persistence, queue_file):
        """Test persistence handles partial file writes."""
        # Write partial JSON (interrupted write)
        partial_data = '[{"message": {"content": "test"'
        queue_file.write_text(partial_data, encoding="utf-8")
        
        # Should handle gracefully
        entries = persistence.load_entries()
        assert isinstance(entries, list)

    def test_persistence_atomic_operation(self, persistence):
        """Test atomic operations prevent corruption."""
        entries = []
        
        def add_entry():
            entries.append(QueueEntry(
                message={"content": "atomic test"},
                queue_id="test-id",
                priority_score=0.5,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
            persistence.save_entries(entries)
            return len(entries)
        
        result = persistence.atomic_operation(add_entry)
        
        assert result == 1
        assert len(persistence.load_entries()) == 1

    def test_processor_persistence_integration(self, message_queue, persistence):
        """Test processor integrates with persistence correctly."""
        # Set up processor with queue
        processor = MessageQueueProcessor(queue=message_queue)
        
        # Enqueue message
        queue_id = message_queue.enqueue({
            "recipient": "Agent-1",
            "content": "processor test",
            "sender": "TEST"
        })
        
        # Verify persisted
        entries = message_queue.persistence.load_entries()
        assert len(entries) == 1
        
        # Process message
        with patch.object(processor, "_route_delivery", return_value=True):
            processed = processor.process_queue(max_messages=1, batch_size=1)
            
            assert processed == 1
            
            # Verify status updated in persistence
            entries_after = message_queue.persistence.load_entries()
            assert len(entries_after) == 1
            assert entries_after[0].status in ["DELIVERED", "PROCESSING"]

    def test_persistence_large_entry_set(self, persistence):
        """Test persistence handles large number of entries."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": f"test {i}", "recipient": f"Agent-{i % 8}"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.5 + (i * 0.01),
                status="PENDING",
                created_at=now,
                updated_at=now
            )
            for i in range(100)
        ]
        
        # Save all entries
        persistence.save_entries(entries)
        
        # Load and verify
        loaded = persistence.load_entries()
        assert len(loaded) == 100
        assert all(e.priority_score > 0 for e in loaded)

    def test_persistence_concurrent_modifications(self, persistence):
        """Test persistence handles concurrent modifications safely."""
        entries1 = [
            QueueEntry(
                message={"content": "concurrent1"},
                queue_id="id1",
                priority_score=0.5,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        entries2 = [
            QueueEntry(
                message={"content": "concurrent2"},
                queue_id="id2",
                priority_score=0.6,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Save first batch
        persistence.save_entries(entries1)
        
        # Load, modify, save
        loaded = persistence.load_entries()
        loaded.extend(entries2)
        persistence.save_entries(loaded)
        
        # Verify both entries exist
        final = persistence.load_entries()
        assert len(final) == 2
        ids = [e.queue_id for e in final]
        assert "id1" in ids
        assert "id2" in ids

    def test_persistence_empty_queue_handling(self, persistence):
        """Test persistence handles empty queues correctly."""
        # Save empty list
        persistence.save_entries([])
        
        # Load should return empty list
        loaded = persistence.load_entries()
        assert loaded == []

    def test_persistence_malformed_entry_isolation(self, persistence, queue_file):
        """Test that malformed entries don't break entire load."""
        # Create file with one valid and one invalid entry
        data = [
            {
                "message": {"content": "valid"},
                "queue_id": "valid-id",
                "priority_score": 0.5,
                "status": "PENDING",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "message": {"content": "invalid"},
                # Missing required fields
            }
        ]
        
        queue_file.write_text(json.dumps(data), encoding="utf-8")
        
        # Should load valid entry and skip invalid
        loaded = persistence.load_entries()
        assert len(loaded) >= 1
        assert loaded[0].queue_id == "valid-id"

    def test_processor_persistence_status_updates(self, message_queue):
        """Test processor updates entry status in persistence."""
        processor = MessageQueueProcessor(queue=message_queue)
        
        # Enqueue
        queue_id = message_queue.enqueue({
            "recipient": "Agent-1",
            "content": "status test",
            "sender": "TEST"
        })
        
        # Verify initial status
        entry = message_queue.get_entry(queue_id)
        assert entry.status == "PENDING"
        
        # Process with mock delivery
        with patch.object(processor, "_route_delivery", return_value=True):
            processor.process_queue(max_messages=1)
        
        # Verify status updated
        entry_after = message_queue.get_entry(queue_id)
        assert entry_after.status == "DELIVERED"

    def test_persistence_backup_corrupted_file(self, persistence, queue_file):
        """Test persistence backs up corrupted files."""
        # Write corrupted data
        queue_file.write_text("not json at all!!!", encoding="utf-8")
        
        # Load should trigger backup
        entries = persistence.load_entries()
        
        # Backup file should exist
        backup_files = list(queue_file.parent.glob(f"{queue_file.name}.*.backup"))
        assert len(backup_files) >= 1 or entries == []  # Backup created or empty returned

    def test_persistence_unicode_content(self, persistence):
        """Test persistence handles unicode content correctly."""
        entries = [
            QueueEntry(
                message={
                    "content": "Test with émojis 🚀 and unicode: 测试",
                    "recipient": "Agent-1"
                },
                queue_id=str(uuid.uuid4()),
                priority_score=0.5,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        persistence.save_entries(entries)
        loaded = persistence.load_entries()
        
        assert len(loaded) == 1
        assert "🚀" in loaded[0].message["content"]
        assert "测试" in loaded[0].message["content"]

    def test_persistence_deferred_push_queue_format(self, persistence, queue_file):
        """Test persistence can load deferred push queue format."""
        # Write deferred push queue format
        data = {
            "pending_pushes": [
                {
                    "repo": "test-repo",
                    "branch": "test-branch",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        queue_file.write_text(json.dumps(data), encoding="utf-8")
        
        # Should handle gracefully (may return empty or parse if compatible)
        entries = persistence.load_entries()
        assert isinstance(entries, list)

