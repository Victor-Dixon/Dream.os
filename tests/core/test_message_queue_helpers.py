"""
Unit tests for message_queue_helpers.py - NEXT PRIORITY

Tests helper functions: log_message_to_repository, track_queue_metrics, track_agent_activity, wait_for_queue_delivery.
Expanded to ≥85% coverage.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import time

# Import helpers
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_helpers import (
    log_message_to_repository,
    track_queue_metrics,
    track_agent_activity,
    wait_for_queue_delivery
)


class TestLogMessageToRepository:
    """Test suite for log_message_to_repository function."""

    def test_log_with_repository(self):
        """Test logging message when repository is available."""
        mock_repository = MagicMock()
        mock_repository.save_message = Mock()
        
        message = {
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "content": "test message",
            "type": "text",
            "priority": "normal"
        }
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-queue-id",
            now=datetime.now(),
            logger=None
        )
        
        assert mock_repository.save_message.called
        call_args = mock_repository.save_message.call_args[0][0]
        assert call_args["from"] == "Agent-1"
        assert call_args["to"] == "Agent-2"
        assert call_args["queue_id"] == "test-queue-id"

    def test_log_without_repository(self):
        """Test logging when repository is None."""
        message = {"content": "test"}
        
        # Should not raise error
        log_message_to_repository(
            message_repository=None,
            message=message,
            queue_id="test-id",
            now=datetime.now(),
            logger=None
        )

    def test_log_with_dict_message(self):
        """Test logging with dict message using 'from' and 'to' keys."""
        mock_repository = MagicMock()
        message = {
            "from": "Agent-1",
            "to": "Agent-2",
            "content": "test",
            "type": "text",
            "priority": "normal",
            "source": "test_source"
        }
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now()
        )
        
        assert mock_repository.save_message.called
        call_args = mock_repository.save_message.call_args[0][0]
        assert call_args["from"] == "Agent-1"
        assert call_args["to"] == "Agent-2"
        assert call_args["source"] == "test_source"

    def test_log_with_object_message(self):
        """Test logging with object message."""
        mock_repository = MagicMock()
        
        class MessageObj:
            def __init__(self):
                self.content = "test"
                self.sender = "Agent-1"
                self.recipient = "Agent-2"
        
        message = MessageObj()
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now()
        )
        
        assert mock_repository.save_message.called

    def test_log_with_long_content(self):
        """Test logging with content longer than 500 characters."""
        mock_repository = MagicMock()
        long_content = "x" * 600
        message = {
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "content": long_content
        }
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now()
        )
        
        call_args = mock_repository.save_message.call_args[0][0]
        assert len(call_args["content"]) == 500
        assert call_args["content_length"] == 600

    def test_log_with_logger(self):
        """Test logging with logger instance."""
        mock_repository = MagicMock()
        mock_logger = MagicMock()
        message = {"sender": "Agent-1", "content": "test"}
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now(),
            logger=mock_logger
        )
        
        assert mock_repository.save_message.called
        mock_logger.debug.assert_called_once()

    def test_log_exception_handling(self):
        """Test logging exception handling."""
        mock_repository = MagicMock()
        mock_repository.save_message.side_effect = Exception("Save failed")
        mock_logger = MagicMock()
        message = {"content": "test"}
        
        # Should not raise error
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now(),
            logger=mock_logger
        )
        
        mock_logger.warning.assert_called_once()


class TestTrackQueueMetrics:
    """Test suite for track_queue_metrics function."""

    def test_track_with_metrics_engine(self):
        """Test tracking metrics when engine is available."""
        mock_engine = MagicMock()
        mock_engine.increment_metric = Mock()
        mock_engine.record_metric = Mock()
        
        message = {
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "content": "test"
        }
        queue_size = 5
        
        track_queue_metrics(
            metrics_engine=mock_engine,
            message=message,
            queue_size=queue_size,
            logger=None
        )
        
        assert mock_engine.increment_metric.called
        assert mock_engine.record_metric.called
        mock_engine.increment_metric.assert_any_call("queue.enqueued")
        mock_engine.increment_metric.assert_any_call("queue.enqueued.by_sender.Agent-1")
        mock_engine.increment_metric.assert_any_call("queue.enqueued.by_recipient.Agent-2")
        mock_engine.record_metric.assert_called_with("queue.size", 5)

    def test_track_without_metrics_engine(self):
        """Test tracking when metrics engine is None."""
        message = {"content": "test"}
        
        # Should not raise error
        track_queue_metrics(
            metrics_engine=None,
            message=message,
            queue_size=0,
            logger=None
        )

    def test_track_with_unknown_sender_recipient(self):
        """Test tracking with unknown sender/recipient."""
        mock_engine = MagicMock()
        message = {"content": "test"}  # No sender/recipient
        
        track_queue_metrics(
            metrics_engine=mock_engine,
            message=message,
            queue_size=10,
            logger=None
        )
        
        mock_engine.increment_metric.assert_any_call("queue.enqueued.by_sender.UNKNOWN")
        mock_engine.increment_metric.assert_any_call("queue.enqueued.by_recipient.UNKNOWN")

    def test_track_exception_handling(self):
        """Test tracking exception handling."""
        mock_engine = MagicMock()
        mock_engine.increment_metric.side_effect = Exception("Metrics error")
        message = {"content": "test"}
        
        # Should not raise error
        track_queue_metrics(
            metrics_engine=mock_engine,
            message=message,
            queue_size=5,
            logger=None
        )


class TestTrackAgentActivity:
    """Test suite for track_agent_activity function."""

    @patch('src.core.agent_activity_tracker.get_activity_tracker')
    def test_track_activity_with_agent_sender(self, mock_get_tracker):
        """Test tracking agent activity with Agent- sender."""
        mock_tracker = MagicMock()
        mock_tracker.mark_active = Mock()
        mock_get_tracker.return_value = mock_tracker
        
        message = {
            "sender": "Agent-1",
            "content": "test"
        }
        
        track_agent_activity(message, logger=None)
        
        mock_tracker.mark_active.assert_called_once_with("Agent-1", "message_queuing")

    @patch('src.core.agent_activity_tracker.get_activity_tracker')
    def test_track_activity_with_from_key(self, mock_get_tracker):
        """Test tracking agent activity with 'from' key."""
        mock_tracker = MagicMock()
        mock_get_tracker.return_value = mock_tracker
        
        message = {
            "from": "Agent-2",
            "content": "test"
        }
        
        track_agent_activity(message, logger=None)
        
        mock_tracker.mark_active.assert_called_once_with("Agent-2", "message_queuing")

    @patch('src.core.agent_activity_tracker.get_activity_tracker')
    def test_track_activity_non_agent_sender(self, mock_get_tracker):
        """Test tracking activity with non-Agent sender."""
        mock_tracker = MagicMock()
        mock_get_tracker.return_value = mock_tracker
        
        message = {
            "sender": "User-1",
            "content": "test"
        }
        
        track_agent_activity(message, logger=None)
        
        # Should not call mark_active for non-Agent senders
        mock_tracker.mark_active.assert_not_called()

    @patch('src.core.agent_activity_tracker.get_activity_tracker')
    def test_track_activity_exception_handling(self, mock_get_tracker):
        """Test tracking activity exception handling."""
        mock_get_tracker.side_effect = Exception("Tracker error")
        mock_logger = MagicMock()
        message = {"sender": "Agent-1"}
        
        # Should not raise error
        track_agent_activity(message, logger=mock_logger)
        
        mock_logger.warning.assert_called_once()


class TestWaitForQueueDelivery:
    """Test suite for wait_for_queue_delivery function."""

    def test_wait_for_delivery_success(self):
        """Test waiting for successful delivery."""
        mock_queue = MagicMock()
        mock_queue.get_entry_status = Mock(return_value="DELIVERED")
        mock_logger = MagicMock()
        
        result = wait_for_queue_delivery(
            queue=mock_queue,
            queue_id="test-id",
            timeout=5.0,
            poll_interval=0.1,
            logger=mock_logger
        )
        
        assert result is True
        mock_logger.debug.assert_called_once()

    def test_wait_for_delivery_failed(self):
        """Test waiting for failed delivery."""
        mock_queue = MagicMock()
        mock_queue.get_entry_status = Mock(return_value="FAILED")
        mock_logger = MagicMock()
        
        result = wait_for_queue_delivery(
            queue=mock_queue,
            queue_id="test-id",
            timeout=5.0,
            poll_interval=0.1,
            logger=mock_logger
        )
        
        assert result is False
        mock_logger.debug.assert_called_once()

    def test_wait_for_delivery_entry_not_found(self):
        """Test waiting when entry is not found."""
        mock_queue = MagicMock()
        mock_queue.get_entry_status = Mock(return_value=None)
        mock_logger = MagicMock()
        
        result = wait_for_queue_delivery(
            queue=mock_queue,
            queue_id="test-id",
            timeout=5.0,
            poll_interval=0.1,
            logger=mock_logger
        )
        
        assert result is False
        mock_logger.warning.assert_called_once()

    def test_wait_for_delivery_timeout(self):
        """Test waiting for delivery with timeout."""
        mock_queue = MagicMock()
        mock_queue.get_entry_status = Mock(return_value="PENDING")
        mock_logger = MagicMock()
        
        result = wait_for_queue_delivery(
            queue=mock_queue,
            queue_id="test-id",
            timeout=0.1,
            poll_interval=0.05,
            logger=mock_logger
        )
        
        assert result is False
        mock_logger.warning.assert_called_once()

    def test_wait_for_delivery_processing_then_delivered(self):
        """Test waiting when entry goes from PROCESSING to DELIVERED."""
        mock_queue = MagicMock()
        mock_queue.get_entry_status = Mock(side_effect=["PROCESSING", "DELIVERED"])
        mock_logger = MagicMock()
        
        result = wait_for_queue_delivery(
            queue=mock_queue,
            queue_id="test-id",
            timeout=5.0,
            poll_interval=0.1,
            logger=mock_logger
        )
        
        assert result is True

    def test_wait_for_delivery_without_logger(self):
        """Test waiting for delivery without logger."""
        mock_queue = MagicMock()
        mock_queue.get_entry_status = Mock(return_value="DELIVERED")
        
        result = wait_for_queue_delivery(
            queue=mock_queue,
            queue_id="test-id",
            timeout=5.0,
            poll_interval=0.1,
            logger=None
        )
        
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

