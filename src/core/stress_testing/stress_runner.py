"""
<!-- SSOT Domain: core -->

Stress Test Runner - Orchestrates stress tests for MessageQueueProcessor

Main stress test orchestrator that coordinates message generation,
queue processing, and metrics collection.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

import time
from typing import Optional, Any

from ..message_queue_processor import MessageQueueProcessor
from .mock_messaging_core import MockMessagingCore
from .metrics_collector import MetricsCollector
from .message_generator import MessageGenerator


class StressTestRunner:
    """Orchestrates stress tests for MessageQueueProcessor."""

    def __init__(
        self,
        num_agents: int = 9,
        messages_per_agent: int = 100,
        message_types: Optional[list] = None,
    ):
        """
        Initialize stress test runner.

        Args:
            num_agents: Number of concurrent agents (default: 9)
            messages_per_agent: Messages per agent (default: 100)
            message_types: List of message types to test (default: all 4)
        """
        self.num_agents = num_agents
        self.messages_per_agent = messages_per_agent
        self.message_types = message_types or [
            "direct",
            "broadcast",
            "hard_onboard",
            "soft_onboard",
        ]

        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.mock_core = MockMessagingCore(self.metrics_collector)
        self.message_generator = MessageGenerator(self.num_agents, self.message_types)

    def run_stress_test(
        self, batch_size: int = 10, interval: float = 0.1
    ) -> dict[str, Any]:
        """
        Run complete stress test.

        Args:
            batch_size: Number of messages to process per batch
            interval: Sleep interval between batches

        Returns:
            Dictionary with comprehensive test metrics
        """
        # Create processor with mock core
        processor = MessageQueueProcessor(messaging_core=self.mock_core)

        # Generate test messages
        total_messages = self.messages_per_agent * self.num_agents
        messages = self.message_generator.generate_batch(total_messages)

        # Enqueue all messages
        for msg in messages:
            processor.queue.enqueue(msg)

        # Process queue
        start_time = time.time()
        processed = processor.process_queue(
            max_messages=len(messages), batch_size=batch_size, interval=interval
        )
        end_time = time.time()

        # Collect metrics
        metrics = self.metrics_collector.get_metrics()
        duration = end_time - start_time
        metrics["total_processed"] = processed
        metrics["duration"] = duration
        metrics["throughput"] = processed / duration if duration > 0 else 0.0
        metrics["messages_per_second"] = metrics["throughput"]

        return metrics

