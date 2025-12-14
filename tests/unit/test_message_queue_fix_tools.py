#!/usr/bin/env python3
"""
Unit Tests for Message Queue Fix Tools
======================================

Tests for message queue diagnostic and fix tools:
- diagnose_message_queue.py
- fix_message_queue.py
- check_queue_status.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-14
"""

import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest


class TestMessageQueueFixTools:
    """Test message queue fix tools functionality."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary queue directory."""
        temp_dir = tempfile.mkdtemp()
        queue_dir = Path(temp_dir) / "message_queue"
        queue_dir.mkdir()
        yield queue_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_queue_file(self, temp_queue_dir):
        """Create sample queue.json file."""
        queue_file = temp_queue_dir / "queue.json"
        entries = [
            {
                "queue_id": "test-001",
                "status": "PENDING",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message": {
                    "recipient": "Agent-1",
                    "content": "Test message 1"
                }
            },
            {
                "queue_id": "test-002",
                "status": "PROCESSING",
                "created_at": (datetime.now() - timedelta(minutes=10)).isoformat(),
                "updated_at": (datetime.now() - timedelta(minutes=10)).isoformat(),
                "message": {
                    "recipient": "Agent-2",
                    "content": "Test message 2"
                }
            },
            {
                "queue_id": "test-003",
                "status": "DELIVERED",
                "created_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "updated_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "message": {
                    "recipient": "Agent-3",
                    "content": "Test message 3"
                }
            }
        ]
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2)
        return queue_file

    def test_clear_lock_files(self, temp_queue_dir):
        """Test clearing lock files."""
        # Create lock files
        lock_files = [
            "delivered.json.lock",
            "failed.json.lock",
            "pending.json.lock",
            "processing.json.lock"
        ]
        for lock_file in lock_files:
            (temp_queue_dir / lock_file).touch()
        
        # Import and test clear_lock_files
        import sys
        from pathlib import Path as PathLib
        
        # Mock project_root
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import clear_lock_files
            
            cleared = clear_lock_files()
            assert cleared == 4
            
            # Verify all lock files are gone
            for lock_file in lock_files:
                assert not (temp_queue_dir / lock_file).exists()

    def test_reset_stuck_messages(self, temp_queue_dir, sample_queue_file):
        """Test resetting stuck messages."""
        # Load original entries
        with open(sample_queue_file, 'r', encoding='utf-8') as f:
            original_entries = json.load(f)
        
        # Verify we have a PROCESSING message
        processing_count = sum(1 for e in original_entries if e['status'] == 'PROCESSING')
        assert processing_count == 1
        
        # Mock project_root and test reset
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import reset_stuck_messages
            
            reset_count = reset_stuck_messages()
            assert reset_count == 1
            
            # Verify message was reset
            with open(sample_queue_file, 'r', encoding='utf-8') as f:
                updated_entries = json.load(f)
            
            # Find the stuck message
            stuck_message = next(
                (e for e in updated_entries if e['queue_id'] == 'test-002'),
                None
            )
            assert stuck_message is not None
            assert stuck_message['status'] == 'PENDING'
            
            # Verify backup was created
            backup_files = list(temp_queue_dir.glob('queue_backup_*.json'))
            assert len(backup_files) == 1

    def test_reset_stuck_messages_no_stuck(self, temp_queue_dir):
        """Test reset when no stuck messages exist."""
        queue_file = temp_queue_dir / "queue.json"
        entries = [
            {
                "queue_id": "test-001",
                "status": "PENDING",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message": {
                    "recipient": "Agent-1",
                    "content": "Test message"
                }
            }
        ]
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2)
        
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import reset_stuck_messages
            
            reset_count = reset_stuck_messages()
            assert reset_count == 0

    def test_reset_stuck_messages_missing_file(self, temp_queue_dir):
        """Test reset when queue file doesn't exist."""
        queue_file = temp_queue_dir / "queue.json"
        if queue_file.exists():
            queue_file.unlink()
        
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import reset_stuck_messages
            
            reset_count = reset_stuck_messages()
            assert reset_count == 0

    def test_diagnose_queue_file(self, temp_queue_dir, sample_queue_file):
        """Test queue file diagnosis."""
        with patch('tools.diagnose_message_queue.project_root', temp_queue_dir.parent):
            from tools.diagnose_message_queue import analyze_queue_file
            
            # Capture output
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            try:
                analyze_queue_file()
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Verify output contains expected information
            assert "Total entries: 3" in output
            assert "PENDING" in output
            assert "PROCESSING" in output
            assert "DELIVERED" in output

    def test_check_queue_status(self, temp_queue_dir, sample_queue_file):
        """Test quick queue status check."""
        with patch('tools.check_queue_status.project_root', temp_queue_dir.parent):
            from tools.check_queue_status import check_queue_status
            
            # Capture output
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            try:
                check_queue_status()
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Verify output contains status information
            assert "Total messages: 3" in output
            assert "PENDING" in output
            assert "PROCESSING" in output
            assert "DELIVERED" in output

    def test_fix_creates_backup(self, temp_queue_dir, sample_queue_file):
        """Test that fix creates backup before modifying queue."""
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import reset_stuck_messages
            
            # Get original file size
            original_size = sample_queue_file.stat().st_size
            
            # Reset stuck messages
            reset_stuck_messages()
            
            # Verify backup exists
            backup_files = list(temp_queue_dir.glob('queue_backup_*.json'))
            assert len(backup_files) == 1
            
            # Verify backup has same content structure
            with open(backup_files[0], 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            assert len(backup_data) == 3

    def test_fix_handles_corrupted_queue(self, temp_queue_dir):
        """Test fix handles corrupted queue file gracefully."""
        queue_file = temp_queue_dir / "queue.json"
        with open(queue_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content {")
        
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import reset_stuck_messages
            
            # Should handle error gracefully
            reset_count = reset_stuck_messages()
            # Returns 0 on error
            assert reset_count == 0

    def test_fix_handles_missing_fields(self, temp_queue_dir):
        """Test fix handles entries with missing fields."""
        queue_file = temp_queue_dir / "queue.json"
        entries = [
            {
                "queue_id": "test-001",
                "status": "PROCESSING",
                # Missing updated_at
            },
            {
                "queue_id": "test-002",
                "status": "PROCESSING",
                "updated_at": (datetime.now() - timedelta(minutes=10)).isoformat(),
                "message": {
                    "recipient": "Agent-1",
                    "content": "Test"
                }
            }
        ]
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2)
        
        with patch('tools.fix_message_queue.project_root', temp_queue_dir.parent):
            from tools.fix_message_queue import reset_stuck_messages
            
            # Should handle missing fields gracefully
            reset_count = reset_stuck_messages()
            # At least one message should be reset (the one with updated_at)
            assert reset_count >= 1


