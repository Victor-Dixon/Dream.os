"""
Test coverage for message_queue_helpers.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 4
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.core.message_queue_helpers import (
    log_message_to_repository,
    track_queue_metrics,
    track_agent_activity,
    wait_for_queue_delivery
)


class TestMessageQueueHelpers:
    """Test suite for message_queue_helpers - 20+ tests for ≥85% coverage"""

    # ========== Log Message to Repository Tests ==========

    def test_log_message_to_repository_with_repo(self):
        """Test logging message to repository when repo exists"""
        mock_repo = Mock()
        message = {
            "sender": "Agent-4",
            "recipient": "Agent-1",
            "content": "test message",
            "type": "text",
            "priority": "normal"
        }
        now = datetime.now()
        
        log_message_to_repository(mock_repo, message, "test-123", now)
        assert mock_repo.save_message.called
        call_args = mock_repo.save_message.call_args[0][0]
        assert call_args["from"] == "Agent-4"
        assert call_args["to"] == "Agent-1"

    def test_log_message_to_repository_no_repo(self):
        """Test logging when repository is None (should not error)"""
        message = {"content": "test"}
        now = datetime.now()
        
        # Should not raise exception
        log_message_to_repository(None, message, "test-123", now)

    def test_log_message_to_repository_dict_message(self):
        """Test logging with dict message"""
        mock_repo = Mock()
        message = {
            "sender": "Agent-4",
            "recipient": "Agent-1",
            "content": "test"
        }
        now = datetime.now()
        
        log_message_to_repository(mock_repo, message, "test-123", now)
        assert mock_repo.save_message.called

    def test_log_message_to_repository_object_message(self):
        """Test logging with object message (converts to dict)"""
        mock_repo = Mock()
        message = Mock()  # Object instead of dict
        now = datetime.now()
        
        log_message_to_repository(mock_repo, message, "test-123", now)
        assert mock_repo.save_message.called

    def test_log_message_to_repository_long_content(self):
        """Test logging with long content (should truncate)"""
        mock_repo = Mock()
        message = {
            "content": "x" * 1000  # Long content
        }
        now = datetime.now()
        
        log_message_to_repository(mock_repo, message, "test-123", now)
        call_args = mock_repo.save_message.call_args[0][0]
        assert len(call_args["content"]) <= 500  # Should be truncated

    def test_log_message_to_repository_exception_handling(self):
        """Test exception handling in repository logging"""
        mock_repo = Mock()
        mock_repo.save_message.side_effect = Exception("Repo error")
        mock_logger = Mock()
        message = {"content": "test"}
        now = datetime.now()
        
        # Should not raise exception
        log_message_to_repository(mock_repo, message, "test-123", now, mock_logger)
        assert mock_logger.warning.called

    # ========== Track Queue Metrics Tests ==========

    def test_track_queue_metrics_with_engine(self):
        """Test tracking metrics when engine exists"""
        mock_engine = Mock()
        message = {
            "sender": "Agent-4",
            "recipient": "Agent-1"
        }
        
        track_queue_metrics(mock_engine, message, 5)
        assert mock_engine.increment_metric.called
        assert mock_engine.record_metric.called

    def test_track_queue_metrics_no_engine(self):
        """Test tracking when engine is None (should not error)"""
        message = {"content": "test"}
        
        # Should not raise exception
        track_queue_metrics(None, message, 5)

    def test_track_queue_metrics_unknown_sender_recipient(self):
        """Test tracking with unknown sender/recipient"""
        mock_engine = Mock()
        message = {}  # No sender/recipient
        
        track_queue_metrics(mock_engine, message, 5)
        assert mock_engine.increment_metric.called

    def test_track_queue_metrics_exception_handling(self):
        """Test exception handling in metrics tracking"""
        mock_engine = Mock()
        mock_engine.increment_metric.side_effect = Exception("Metrics error")
        message = {"content": "test"}
        
        # Should not raise exception (non-blocking)
        track_queue_metrics(mock_engine, message, 5)

    # ========== Track Agent Activity Tests ==========

    @patch('src.core.message_queue_helpers.get_activity_tracker')
    def test_track_agent_activity_agent_sender(self, mock_get_tracker):
        """Test tracking activity for Agent- sender"""
        mock_tracker = Mock()
        mock_get_tracker.return_value = mock_tracker
        message = {"sender": "Agent-1"}
        
        track_agent_activity(message)
        assert mock_tracker.mark_active.called
        assert mock_tracker.mark_active.call_args[0][0] == "Agent-1"

    @patch('src.core.message_queue_helpers.get_activity_tracker')
    def test_track_agent_activity_from_key(self, mock_get_tracker):
        """Test tracking activity using 'from' key"""
        mock_tracker = Mock()
        mock_get_tracker.return_value = mock_tracker
        message = {"from": "Agent-2"}
        
        track_agent_activity(message)
        assert mock_tracker.mark_active.called

    @patch('src.core.message_queue_helpers.get_activity_tracker')
    def test_track_agent_activity_non_agent_sender(self, mock_get_tracker):
        """Test tracking with non-Agent sender (should not track)"""
        mock_tracker = Mock()
        mock_get_tracker.return_value = mock_tracker
        message = {"sender": "System"}
        
        track_agent_activity(message)
        assert not mock_tracker.mark_active.called

    @patch('src.core.message_queue_helpers.get_activity_tracker')
    def test_track_agent_activity_exception_handling(self, mock_get_tracker):
        """Test exception handling in activity tracking"""
        mock_get_tracker.side_effect = Exception("Tracker error")
        mock_logger = Mock()
        message = {"sender": "Agent-1"}
        
        # Should not raise exception
        track_agent_activity(message, mock_logger)
        assert mock_logger.warning.called

    # ========== Wait for Queue Delivery Tests ==========

    @patch('src.core.message_queue_helpers.time.sleep')
    def test_wait_for_queue_delivery_success(self, mock_sleep):
        """Test waiting for successful delivery"""
        mock_queue = Mock()
        mock_queue.get_entry_status.return_value = "DELIVERED"
        
        result = wait_for_queue_delivery(mock_queue, "test-123", timeout=1.0)
        assert result is True
        assert mock_queue.get_entry_status.called

    @patch('src.core.message_queue_helpers.time.sleep')
    def test_wait_for_queue_delivery_failure(self, mock_sleep):
        """Test waiting for failed delivery"""
        mock_queue = Mock()
        mock_queue.get_entry_status.return_value = "FAILED"
        
        result = wait_for_queue_delivery(mock_queue, "test-123", timeout=1.0)
        assert result is False

    @patch('src.core.message_queue_helpers.time.sleep')
    def test_wait_for_queue_delivery_timeout(self, mock_sleep):
        """Test waiting with timeout"""
        mock_queue = Mock()
        mock_queue.get_entry_status.return_value = "PENDING"  # Never completes
        mock_logger = Mock()
        
        result = wait_for_queue_delivery(mock_queue, "test-123", timeout=0.1, poll_interval=0.05, logger=mock_logger)
        assert result is False
        assert mock_logger.warning.called

    @patch('src.core.message_queue_helpers.time.sleep')
    def test_wait_for_queue_delivery_entry_not_found(self, mock_sleep):
        """Test waiting when entry not found"""
        mock_queue = Mock()
        mock_queue.get_entry_status.return_value = None
        mock_logger = Mock()
        
        result = wait_for_queue_delivery(mock_queue, "test-123", timeout=1.0, logger=mock_logger)
        assert result is False
        assert mock_logger.warning.called

    @patch('src.core.message_queue_helpers.time.sleep')
    def test_wait_for_queue_delivery_processing_state(self, mock_sleep):
        """Test waiting when entry is in PROCESSING state"""
        mock_queue = Mock()
        # First call returns PROCESSING, second returns DELIVERED
        mock_queue.get_entry_status.side_effect = ["PROCESSING", "DELIVERED"]
        
        result = wait_for_queue_delivery(mock_queue, "test-123", timeout=1.0, poll_interval=0.05)
        assert result is True
        assert mock_sleep.called  # Should have slept between checks

