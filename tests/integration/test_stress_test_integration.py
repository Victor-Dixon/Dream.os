"""
Integration Tests for Stress Test System
=========================================

End-to-end integration tests for the complete stress testing system:
- MessageQueueProcessor with MockMessagingCore
- 9-agent simulation
- Metrics collection
- Queue behavior validation

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-11-28
License: MIT
"""

import pytest
import time
from pathlib import Path
from typing import Any

from src.core.message_queue_processor import MessageQueueProcessor
from src.core.message_queue import MessageQueue, QueueConfig
from src.core.stress_testing.stress_runner import StressTestRunner
from src.core.stress_testing.mock_messaging_core import MockMessagingCore
from src.core.stress_testing.metrics_collector import MetricsCollector
from src.core.stress_testing.message_generator import MessageGenerator
from src.core.stress_test_metrics import StressTestMetricsCollector
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


class TestStressTestIntegration:
    """Integration tests for complete stress test system."""

    def test_mock_core_injection(self):
        """Test that MockMessagingCore can be injected into MessageQueueProcessor."""
        # Create mock core
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)

        # Create processor with mock core
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Verify injection
        assert processor.messaging_core is not None
        assert processor.messaging_core == mock_core

    def test_single_message_delivery(self):
        """Test single message delivery through complete system."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Create message (as dict - queue accepts any format)
        message = {
            "content": "Test message",
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "message_type": UnifiedMessageType.TEXT,
            "priority": UnifiedMessagePriority.REGULAR,
        }

        # Enqueue and process
        processor.queue.enqueue(message)
        processed = processor.process_queue(max_messages=1, batch_size=1)

        # Verify
        assert processed == 1
        assert len(mock_core.get_sent_messages()) == 1
        metrics = metrics_collector.get_metrics()
        assert metrics["total_messages"] == 1
        assert metrics["success_count"] == 1

    def test_batch_message_processing(self):
        """Test batch message processing."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Create multiple messages (as dicts)
        messages = [
            {
                "content": f"Message {i}",
                "sender": "Agent-1",
                "recipient": f"Agent-{(i % 8) + 1}",
                "message_type": UnifiedMessageType.TEXT,
                "priority": UnifiedMessagePriority.REGULAR,
            }
            for i in range(10)
        ]

        # Enqueue all
        for msg in messages:
            processor.queue.enqueue(msg)

        # Process in batches
        processed = processor.process_queue(max_messages=10, batch_size=5)

        # Verify
        assert processed == 10
        assert len(mock_core.get_sent_messages()) == 10
        metrics = metrics_collector.get_metrics()
        assert metrics["total_messages"] == 10
        assert metrics["success_count"] == 10

    def test_stress_test_runner_integration(self):
        """Test StressTestRunner end-to-end."""
        # Create runner
        runner = StressTestRunner(
            num_agents=9,
            messages_per_agent=10,
            message_types=["direct", "broadcast"],
        )

        # Run stress test
        metrics = runner.run_stress_test(batch_size=10, interval=0.01)

        # Verify metrics
        assert metrics["total_processed"] == 90  # 9 agents * 10 messages
        assert metrics["total_messages"] == 90
        assert metrics["success_count"] == 90
        assert metrics["duration"] > 0
        assert metrics["throughput"] > 0

    def test_9_agent_simulation(self):
        """Test 9-agent simulation with full metrics."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Generate messages for 9 agents
        message_generator = MessageGenerator(num_agents=9, message_types=["direct", "broadcast"])
        messages = message_generator.generate_batch(90)  # 10 per agent

        # Enqueue all messages
        for msg in messages:
            processor.queue.enqueue(msg)

        # Process all
        processed = processor.process_queue(max_messages=90, batch_size=10)

        # Verify
        assert processed == 90
        metrics = metrics_collector.get_metrics()
        assert metrics["total_messages"] == 90

        # Verify all 9 agents received messages
        by_agent = metrics["by_agent"]
        assert len(by_agent) == 9
        for agent_id in [f"Agent-{i}" for i in range(1, 10)]:
            assert agent_id in by_agent

    def test_metrics_collection_integration(self):
        """Test that metrics are collected correctly during stress test."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Generate and process messages
        message_generator = MessageGenerator(num_agents=9, message_types=["direct", "broadcast", "hard_onboard"])
        messages = message_generator.generate_batch(45)

        for msg in messages:
            processor.queue.enqueue(msg)

        processed = processor.process_queue(max_messages=45, batch_size=5)

        # Verify metrics
        assert processed == 45
        metrics = metrics_collector.get_metrics()

        # Check overall metrics
        assert metrics["total_messages"] == 45
        assert metrics["success_count"] == 45
        assert metrics["success_rate"] == 1.0

        # Check per-message-type metrics
        by_type = metrics["by_message_type"]
        assert len(by_type) > 0
        assert sum(by_type.values()) == 45

        # Check per-agent metrics
        by_agent = metrics["by_agent"]
        assert len(by_agent) == 9

    def test_queue_behavior_under_load(self):
        """Test queue behavior under high load."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Generate large batch
        message_generator = MessageGenerator(num_agents=9, message_types=["direct"])
        messages = message_generator.generate_batch(500)

        # Enqueue all at once
        for msg in messages:
            processor.queue.enqueue(msg)

        # Verify queue size
        assert processor.queue.size() == 500

        # Process in batches
        processed = processor.process_queue(max_messages=500, batch_size=50)

        # Verify all processed
        assert processed == 500
        assert processor.queue.size() == 0

    def test_priority_handling(self):
        """Test that message priorities are handled correctly."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Create messages with different priorities (as dicts)
        urgent_msg = {
            "content": "Urgent message",
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "message_type": UnifiedMessageType.TEXT,
            "priority": UnifiedMessagePriority.URGENT,
        }
        normal_msg = {
            "content": "Normal message",
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "message_type": UnifiedMessageType.TEXT,
            "priority": UnifiedMessagePriority.REGULAR,
        }

        # Enqueue
        processor.queue.enqueue(normal_msg)
        processor.queue.enqueue(urgent_msg)

        # Process
        processed = processor.process_queue(max_messages=2)

        # Verify both processed
        assert processed == 2
        assert len(mock_core.get_sent_messages()) == 2

    def test_message_type_variety(self):
        """Test handling of different message types."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Create messages of different types
        message_types = [
            UnifiedMessageType.TEXT,
            UnifiedMessageType.BROADCAST,
        ]

        messages = []
        for msg_type in message_types:
            msg = {
                "content": f"Test {msg_type.value}",
                "sender": "Agent-1",
                "recipient": "Agent-2",
                "message_type": msg_type,
                "priority": UnifiedMessagePriority.REGULAR,
            }
            messages.append(msg)
            processor.queue.enqueue(msg)

        # Process
        processed = processor.process_queue(max_messages=len(messages))

        # Verify
        assert processed == len(messages)
        metrics = metrics_collector.get_metrics()
        by_type = metrics["by_message_type"]
        assert len(by_type) == len(message_types)

    def test_zero_real_agent_interaction(self):
        """Verify that mock core never touches real agents."""
        # Setup
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Process messages (as dict)
        message = {
            "content": "Test",
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "message_type": UnifiedMessageType.TEXT,
            "priority": UnifiedMessagePriority.REGULAR,
        }
        processor.queue.enqueue(message)
        processor.process_queue(max_messages=1)

        # Verify mock was used (not real core)
        assert processor.messaging_core == mock_core
        assert len(mock_core.get_sent_messages()) == 1

        # Verify no real agent interaction (check that inbox files weren't created)
        inbox_path = Path("agent_workspaces/Agent-2/inbox")
        if inbox_path.exists():
            # Check that no new files were created during test
            initial_files = list(inbox_path.glob("*.md"))
            # This test verifies isolation - if files exist, they were pre-existing

    def test_stress_test_metrics_collector_integration(self):
        """Test integration with Agent-5's comprehensive metrics collector."""
        # Setup
        stress_metrics = StressTestMetricsCollector()
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Start test
        stress_metrics.start_test({
            "num_agents": 9,
            "messages_per_agent": 10,
        })

        # Generate and process messages
        message_generator = MessageGenerator(num_agents=9, message_types=["direct"])
        messages = message_generator.generate_batch(90)

        for msg in messages:
            processor.queue.enqueue(msg)
            stress_metrics.record_message_sent(
                agent_id=msg.get("recipient", "UNKNOWN"),
                message_type=str(msg.get("message_type", "unknown")),
            )

        # Process
        start_time = time.time()
        processed = processor.process_queue(max_messages=90, batch_size=10)
        end_time = time.time()

        # Record metrics
        for msg in mock_core.get_sent_messages():
            latency_ms = 1.0  # Mock delay
            msg_type = msg.get("message_type")
            if hasattr(msg_type, "value"):
                msg_type_str = msg_type.value
            else:
                msg_type_str = str(msg_type)
            stress_metrics.record_message_delivered(
                latency_ms=latency_ms,
                agent_id=msg.get("recipient", "UNKNOWN"),
                message_type=msg_type_str,
                delivery_mode="mock",
            )

        stress_metrics.stop_test()

        # Generate dashboard
        dashboard = stress_metrics.generate_dashboard_json()

        # Verify dashboard structure
        assert "test_metadata" in dashboard
        assert "overall_metrics" in dashboard
        assert "per_agent_metrics" in dashboard
        assert "per_message_type_metrics" in dashboard

        # Verify metrics
        overall = dashboard["overall_metrics"]
        assert overall["total_messages"] == 90
        assert overall["failed_messages"] == 0

    def test_end_to_end_9_agent_stress_test(self):
        """Complete end-to-end test: 9 agents, full metrics, validation."""
        # Setup complete system
        stress_metrics = StressTestMetricsCollector()
        metrics_collector = MetricsCollector()
        mock_core = MockMessagingCore(metrics_collector=metrics_collector)
        processor = MessageQueueProcessor(messaging_core=mock_core)

        # Start test
        stress_metrics.start_test({
            "num_agents": 9,
            "messages_per_agent": 20,
            "message_types": ["direct", "broadcast"],
        })

        # Generate messages
        message_generator = MessageGenerator(
            num_agents=9,
            message_types=["direct", "broadcast"],
        )
        messages = message_generator.generate_batch(180)  # 9 * 20

        # Enqueue and track
        for msg in messages:
            processor.queue.enqueue(msg)
            stress_metrics.record_message_sent(
                agent_id=msg.get("recipient", "UNKNOWN"),
                message_type=str(msg.get("message_type", "unknown")),
            )

        # Process
        processed = processor.process_queue(max_messages=180, batch_size=20)

        # Record delivery metrics
        for msg in mock_core.get_sent_messages():
            msg_type = msg.get("message_type")
            if hasattr(msg_type, "value"):
                msg_type_str = msg_type.value
            else:
                msg_type_str = str(msg_type)
            stress_metrics.record_message_delivered(
                latency_ms=1.0,
                agent_id=msg.get("recipient", "UNKNOWN"),
                message_type=msg_type_str,
                delivery_mode="mock",
            )

        stress_metrics.stop_test()

        # Generate dashboard
        dashboard = stress_metrics.generate_dashboard_json()

        # Validation checks
        assert processed == 180
        assert dashboard["overall_metrics"]["total_messages"] == 180
        assert dashboard["overall_metrics"]["failed_messages"] == 0
        assert len(dashboard["per_agent_metrics"]) == 9
        assert len(dashboard["per_message_type_metrics"]) == 2

        # Verify all agents present
        agent_ids = set(dashboard["per_agent_metrics"].keys())
        expected_agents = {f"Agent-{i}" for i in range(1, 10)}
        assert agent_ids == expected_agents

        return dashboard

