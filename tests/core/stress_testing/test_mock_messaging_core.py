"""
Unit tests for MockMessagingCore

Tests mock messaging core functionality for stress testing.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.stress_testing.mock_messaging_core import MockMessagingCore
from src.core.stress_testing.metrics_collector import MetricsCollector
from src.core.messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


class TestMockMessagingCore:
    """Test suite for MockMessagingCore."""

    def test_initialization_default(self):
        """Test default initialization."""
        mock_core = MockMessagingCore()
        
        assert mock_core.delivery_success_rate == 1.0
        assert mock_core.simulated_delay == 0.001
        assert mock_core.metrics_collector is None
        assert len(mock_core.sent_messages) == 0

    def test_initialization_with_metrics(self):
        """Test initialization with metrics collector."""
        collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=collector)
        
        assert mock_core.metrics_collector == collector

    def test_initialization_custom_rates(self):
        """Test initialization with custom success rate."""
        mock_core = MockMessagingCore(delivery_success_rate=0.5, simulated_delay=0.01)
        
        assert mock_core.delivery_success_rate == 0.5
        assert mock_core.simulated_delay == 0.01

    def test_send_message_records_message(self):
        """Test that send_message records messages."""
        mock_core = MockMessagingCore()
        
        result = mock_core.send_message(
            content="Test",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        )
        
        assert len(mock_core.sent_messages) == 1
        assert mock_core.sent_messages[0]["content"] == "Test"
        assert mock_core.sent_messages[0]["recipient"] == "Agent-1"
        assert isinstance(result, bool)

    def test_send_message_with_metrics(self):
        """Test that send_message records metrics when collector provided."""
        collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=collector)
        
        mock_core.send_message(
            content="Test",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        )
        
        metrics = collector.get_metrics()
        assert metrics["total_messages"] == 1

    def test_send_message_all_parameters(self):
        """Test send_message with all parameters."""
        mock_core = MockMessagingCore()
        
        result = mock_core.send_message(
            content="Full test",
            sender="Agent-2",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN],
            metadata={"key": "value"},
        )
        
        msg = mock_core.sent_messages[0]
        assert msg["content"] == "Full test"
        assert msg["sender"] == "Agent-2"
        assert msg["priority"] == UnifiedMessagePriority.URGENT
        assert UnifiedMessageTag.CAPTAIN in msg["tags"]
        assert msg["metadata"]["key"] == "value"
        assert isinstance(result, bool)

    def test_get_sent_messages(self):
        """Test getting sent messages."""
        mock_core = MockMessagingCore()
        
        mock_core.send_message(
            content="Test1",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        )
        mock_core.send_message(
            content="Test2",
            sender="SYSTEM",
            recipient="Agent-2",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        )
        
        messages = mock_core.get_sent_messages()
        assert len(messages) == 2
        assert messages[0]["content"] == "Test1"
        assert messages[1]["content"] == "Test2"
        # Should be a copy
        assert messages is not mock_core.sent_messages

    def test_reset(self):
        """Test reset functionality."""
        collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=collector)
        
        mock_core.send_message(
            content="Test",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        )
        
        assert len(mock_core.sent_messages) == 1
        assert collector.get_metrics()["total_messages"] == 1
        
        mock_core.reset()
        
        assert len(mock_core.sent_messages) == 0
        assert collector.get_metrics()["total_messages"] == 0

