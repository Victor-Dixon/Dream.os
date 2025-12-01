"""
Unit Tests for Stress Test Runner
=================================
"""

import pytest
import time
from unittest.mock import MagicMock, patch, Mock
from src.core.stress_test_runner import (
    StressTestRunner,
    AgentSimulator,
    MessageType,
)


class TestAgentSimulator:
    """Tests for AgentSimulator."""

    def test_initialization(self):
        """Test agent simulator initialization."""
        agent = AgentSimulator("Agent-1")
        assert agent.agent_id == "Agent-1"
        assert agent.message_count == 0
        assert agent.success_count == 0
        assert agent.failure_count == 0

    def test_record_send_success(self):
        """Test recording successful send."""
        agent = AgentSimulator("Agent-1")
        agent.record_send(success=True, latency_ms=10.0)
        assert agent.message_count == 1
        assert agent.success_count == 1
        assert agent.failure_count == 0
        assert agent.total_latency_ms == 10.0

    def test_record_send_failure(self):
        """Test recording failed send."""
        agent = AgentSimulator("Agent-1")
        agent.record_send(success=False, latency_ms=5.0)
        assert agent.message_count == 1
        assert agent.success_count == 0
        assert agent.failure_count == 1

    def test_get_stats(self):
        """Test getting agent statistics."""
        agent = AgentSimulator("Agent-1")
        agent.record_send(success=True, latency_ms=10.0)
        agent.record_send(success=True, latency_ms=20.0)
        stats = agent.get_stats()
        assert stats["agent_id"] == "Agent-1"
        assert stats["message_count"] == 2
        assert stats["success_count"] == 2
        assert stats["success_rate"] == 100.0
        assert stats["average_latency_ms"] == 15.0


class TestStressTestRunner:
    """Tests for StressTestRunner."""

    def test_initialization(self):
        """Test runner initialization."""
        callback = MagicMock()
        runner = StressTestRunner(callback, duration_seconds=10, messages_per_second=5.0)
        assert runner.delivery_callback == callback
        assert runner.duration_seconds == 10
        assert runner.messages_per_second == 5.0
        assert len(runner.agents) == 9

    def test_initialization_with_message_types(self):
        """Test initialization with specific message types."""
        callback = MagicMock()
        message_types = [MessageType.TEXT, MessageType.URGENT]
        runner = StressTestRunner(callback, message_types=message_types)
        assert runner.message_types == message_types

    def test_generate_message_content(self):
        """Test generating message content."""
        callback = MagicMock()
        runner = StressTestRunner(callback)
        content = runner._generate_message_content(
            sender="Agent-1",
            recipient="Agent-2",
            message_type=MessageType.TEXT,
            count=1
        )
        assert isinstance(content, str)
        assert len(content) > 0

    def test_send_message_with_callable(self):
        """Test sending message with callable callback."""
        callback = MagicMock(return_value=True)
        runner = StressTestRunner(callback)
        success = runner._send_message(
            sender="Agent-1",
            recipient="Agent-2",
            content="Test message",
            message_type=MessageType.TEXT
        )
        assert success is True
        callback.assert_called_once()

    def test_send_message_with_object(self):
        """Test sending message with object callback."""
        # Create a non-callable mock object
        class MockDelivery:
            def send_message(self, content, sender, recipient):
                return True
        
        mock_obj = MockDelivery()
        runner = StressTestRunner(mock_obj)
        success = runner._send_message(
            sender="Agent-1",
            recipient="Agent-2",
            content="Test message",
            message_type=MessageType.TEXT
        )
        assert success is True

    def test_send_message_exception(self):
        """Test sending message with exception."""
        callback = MagicMock(side_effect=Exception("Test error"))
        runner = StressTestRunner(callback)
        success = runner._send_message(
            sender="Agent-1",
            recipient="Agent-2",
            content="Test message",
            message_type=MessageType.TEXT
        )
        assert success is False

    def test_get_stats_before_start(self):
        """Test getting stats before test starts."""
        callback = MagicMock()
        runner = StressTestRunner(callback)
        stats = runner.get_stats()
        assert stats["test_duration_seconds"] == 0.0
        assert stats["total_messages_sent"] == 0

    def test_get_stats_after_run(self):
        """Test getting stats after test run."""
        callback = MagicMock(return_value=True)
        runner = StressTestRunner(callback, duration_seconds=1, messages_per_second=1.0)
        runner.start()
        stats = runner.get_stats()
        assert stats["test_duration_seconds"] > 0
        assert "agent_stats" in stats
        assert len(stats["agent_stats"]) == 9

    def test_start_and_stop(self):
        """Test starting and stopping test."""
        callback = MagicMock(return_value=True)
        runner = StressTestRunner(callback, duration_seconds=1, messages_per_second=1.0)
        assert runner.running is False
        runner.start()
        # Test should run for 1 second then stop
        time.sleep(1.5)
        assert runner.running is False
        assert runner.end_time is not None

    def test_stop_when_not_running(self):
        """Test stopping when not running."""
        callback = MagicMock()
        runner = StressTestRunner(callback)
        runner.stop()  # Should not raise exception
        assert runner.running is False

    def test_agent_ids_list(self):
        """Test that agent IDs list is correct."""
        callback = MagicMock()
        runner = StressTestRunner(callback)
        assert len(runner.AGENT_IDS) == 9
        assert "Agent-1" in runner.AGENT_IDS
        assert "Agent-9" in runner.AGENT_IDS

    def test_message_templates(self):
        """Test that message templates exist."""
        callback = MagicMock()
        runner = StressTestRunner(callback)
        assert MessageType.TEXT in runner.MESSAGE_TEMPLATES
        assert MessageType.BROADCAST in runner.MESSAGE_TEMPLATES
        assert MessageType.SYSTEM in runner.MESSAGE_TEMPLATES
        assert MessageType.URGENT in runner.MESSAGE_TEMPLATES


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

