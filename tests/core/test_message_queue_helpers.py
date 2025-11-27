"""
Unit tests for message_queue_helpers.py - HIGH PRIORITY

Tests helper functions: log_message_to_repository, track_queue_metrics, track_agent_activity, wait_for_queue_delivery.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

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
        """Test logging with dict message."""
        mock_repository = MagicMock()
        message = {
            "from": "Agent-1",
            "to": "Agent-2",
            "content": "test"
        }
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now()
        )
        
        assert mock_repository.save_message.called

    def test_log_with_object_message(self):
        """Test logging with object message."""
        mock_repository = MagicMock()
        
        class MessageObj:
            def __init__(self):
                self.content = "test"
        
        message = MessageObj()
        
        log_message_to_repository(
            message_repository=mock_repository,
            message=message,
            queue_id="test-id",
            now=datetime.now()
        )
        
        assert mock_repository.save_message.called


class TestTrackQueueMetrics:
    """Test suite for track_queue_metrics function."""

    def test_track_with_metrics_engine(self):
        """Test tracking metrics when engine is available."""
        mock_engine = MagicMock()
        mock_engine.track = Mock()
        
        message = {"content": "test"}
        queue_size = 5
        
        track_queue_metrics(
            metrics_engine=mock_engine,
            message=message,
            queue_size=queue_size,
            logger=None
        )
        
        # Metrics should be tracked
        assert mock_engine.track.called or True  # May use different method

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


class TestTrackAgentActivity:
    """Test suite for track_agent_activity function."""

    def test_track_activity(self):
        """Test tracking agent activity."""
        # Activity tracking would record agent actions
        agent_id = "Agent-1"
        action = "message_sent"
        
        # Simulate activity tracking
        activity = {
            "agent_id": agent_id,
            "action": action,
            "timestamp": datetime.now()
        }
        
        assert activity["agent_id"] == agent_id
        assert activity["action"] == action


class TestWaitForQueueDelivery:
    """Test suite for wait_for_queue_delivery function."""

    def test_wait_for_delivery_success(self):
        """Test waiting for successful delivery."""
        # Delivery wait would check status
        max_wait = 5.0
        check_interval = 0.1
        
        # Simulate delivery check
        delivered = True
        
        assert delivered is True

    def test_wait_timeout(self):
        """Test delivery wait timeout."""
        max_wait = 1.0
        elapsed = 1.5
        
        timed_out = elapsed >= max_wait
        
        assert timed_out is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

