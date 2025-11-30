"""
Unit tests for src/core/deferred_push_queue.py

Target: ≥10 tests, 100% passing
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from datetime import datetime, timedelta

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.deferred_push_queue import DeferredPushQueue, PushStatus


class TestDeferredPushQueue:
    """Test suite for DeferredPushQueue."""

    @pytest.fixture
    def temp_queue_file(self):
        """Create temporary queue file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        yield temp_path
        if temp_path.exists():
            temp_path.unlink()

    @pytest.fixture
    def queue(self, temp_queue_file):
        """Create DeferredPushQueue instance with temp file."""
        return DeferredPushQueue(queue_file=temp_queue_file)

    def test_queue_initialization(self, queue):
        """Test queue initializes correctly."""
        assert queue is not None
        assert queue.queue_file is not None
        assert queue.pending_pushes == []

    def test_queue_initialization_with_file(self, temp_queue_file):
        """Test queue initialization with existing file."""
        # Create initial queue data
        initial_data = {
            "pending_pushes": [
                {
                    "id": "test1",
                    "repo": "test_repo",
                    "branch": "test_branch",
                    "status": PushStatus.PENDING.value,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        temp_queue_file.write_text(json.dumps(initial_data))
        
        queue = DeferredPushQueue(queue_file=temp_queue_file)
        assert len(queue.pending_pushes) == 1
        assert queue.pending_pushes[0]["id"] == "test1"

    def test_enqueue_push(self, queue):
        """Test enqueueing a push operation."""
        entry_id = queue.enqueue_push(
            repo="test_repo",
            branch="test_branch",
            reason="rate_limit"
        )
        
        assert entry_id is not None
        assert len(queue.pending_pushes) == 1
        assert queue.pending_pushes[0]["repo"] == "test_repo"
        assert queue.pending_pushes[0]["branch"] == "test_branch"
        assert queue.pending_pushes[0]["status"] == PushStatus.PENDING.value

    def test_enqueue_push_with_metadata(self, queue):
        """Test enqueueing push with metadata."""
        metadata = {"pr_number": 123, "merge_method": "merge"}
        entry_id = queue.enqueue_push(
            repo="test_repo",
            branch="test_branch",
            reason="sandbox_mode",
            metadata=metadata
        )
        
        assert queue.pending_pushes[0]["metadata"] == metadata

    def test_dequeue_push(self, queue):
        """Test dequeuing a push operation."""
        # Enqueue a push
        entry_id = queue.enqueue_push("repo1", "branch1", reason="test")
        
        # Dequeue it
        entry = queue.dequeue_push()
        
        assert entry is not None
        assert entry["id"] == entry_id
        assert entry["status"] == PushStatus.RETRYING.value

    def test_dequeue_push_empty_queue(self, queue):
        """Test dequeuing from empty queue."""
        entry = queue.dequeue_push()
        assert entry is None

    def test_mark_completed(self, queue):
        """Test marking push as completed."""
        entry_id = queue.enqueue_push("repo1", "branch1", reason="test")
        
        result = queue.mark_completed(entry_id)
        
        assert result is True
        entry = next((e for e in queue.pending_pushes if e["id"] == entry_id), None)
        assert entry is not None
        assert entry["status"] == PushStatus.COMPLETED.value

    def test_mark_failed(self, queue):
        """Test marking push as failed."""
        entry_id = queue.enqueue_push("repo1", "branch1", reason="test")
        
        result = queue.mark_failed(entry_id, error="Test error")
        
        assert result is True
        entry = next((e for e in queue.pending_pushes if e["id"] == entry_id), None)
        assert entry is not None
        assert entry["status"] == PushStatus.FAILED.value

    def test_get_pending_count(self, queue):
        """Test getting count of pending operations."""
        queue.enqueue_push("repo1", "branch1", reason="test")
        queue.enqueue_push("repo2", "branch2", reason="test")
        
        count = queue.get_pending_count()
        
        assert count == 2

    def test_load_queue_filters_old_completed(self, temp_queue_file):
        """Test that loading queue filters old completed entries."""
        old_timestamp = (datetime.now() - timedelta(hours=25)).isoformat()
        recent_timestamp = datetime.now().isoformat()
        
        initial_data = {
            "pending_pushes": [
                {
                    "id": "old",
                    "status": PushStatus.COMPLETED.value,
                    "timestamp": old_timestamp
                },
                {
                    "id": "recent",
                    "status": PushStatus.COMPLETED.value,
                    "timestamp": recent_timestamp
                },
                {
                    "id": "pending",
                    "status": PushStatus.PENDING.value,
                    "timestamp": old_timestamp
                }
            ]
        }
        temp_queue_file.write_text(json.dumps(initial_data))
        
        queue = DeferredPushQueue(queue_file=temp_queue_file)
        
        # Should keep recent completed and pending, but filter old completed
        ids = [e["id"] for e in queue.pending_pushes]
        assert "old" not in ids  # Old completed filtered out
        assert "recent" in ids  # Recent completed kept
        assert "pending" in ids  # Pending kept

    def test_save_queue_persistence(self, queue, temp_queue_file):
        """Test that queue saves to file."""
        queue.enqueue_push("repo1", "branch1", reason="test")
        queue._save_queue()
        
        # Reload and verify
        new_queue = DeferredPushQueue(queue_file=temp_queue_file)
        assert len(new_queue.pending_pushes) == 1
        assert new_queue.pending_pushes[0]["repo"] == "repo1"

    def test_get_pending_operations(self, queue):
        """Test getting list of pending operations."""
        queue.enqueue_push("repo1", "branch1", reason="test1")
        queue.enqueue_push("repo2", "branch2", reason="test2")
        
        operations = queue.get_pending_operations()
        
        assert len(operations) == 2
        assert operations[0]["repo"] == "repo1"
        assert operations[1]["repo"] == "repo2"

