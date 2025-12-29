"""
<!-- SSOT Domain: core -->

Metrics Collector - Collects and analyzes stress test metrics

Tracks message delivery metrics, calculates statistics, and generates reports.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

from typing import Any
from collections import defaultdict


class MetricsCollector:
    """Collects and analyzes stress test metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.messages: list[dict] = []
        self.delivery_times: list[float] = []
        self.success_count = 0
        self.failure_count = 0

    def record_message(self, message_record: dict):
        """
        Record a message delivery attempt.

        Args:
            message_record: Dictionary with message details including 'delivered' key
        """
        self.messages.append(message_record)

        if message_record.get("delivered", False):
            self.success_count += 1
        else:
            self.failure_count += 1

    def get_metrics(self) -> dict:
        """
        Calculate and return metrics.

        Returns:
            Dictionary with comprehensive metrics
        """
        total = self.success_count + self.failure_count
        success_rate = self.success_count / total if total > 0 else 0.0

        # Group by message type
        by_type = defaultdict(int)
        for msg in self.messages:
            msg_type = msg.get("message_type")
            if msg_type:
                type_value = msg_type.value if hasattr(msg_type, "value") else str(msg_type)
                by_type[type_value] += 1

        # Group by agent
        by_agent = defaultdict(int)
        for msg in self.messages:
            agent = msg.get("recipient", "UNKNOWN")
            by_agent[agent] += 1

        # Group by sender
        by_sender = defaultdict(int)
        for msg in self.messages:
            sender = msg.get("sender", "UNKNOWN")
            by_sender[sender] += 1

        return {
            "total_messages": total,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": success_rate,
            "by_message_type": dict(by_type),
            "by_agent": dict(by_agent),
            "by_sender": dict(by_sender),
        }

    def reset(self):
        """Reset all collected metrics."""
        self.messages.clear()
        self.delivery_times.clear()
        self.success_count = 0
        self.failure_count = 0

