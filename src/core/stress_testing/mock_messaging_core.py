"""
<!-- SSOT Domain: core -->

Mock Messaging Core - Zero real agent interaction simulation

Simulates message delivery for stress testing without touching real agents.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

import time
import random
from datetime import datetime
from typing import Any, Optional

from ..messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .metrics_collector import MetricsCollector


class MockMessagingCore:
    """Mock messaging core for stress testing - zero real agent interaction."""

    def __init__(
        self,
        metrics_collector: Optional[MetricsCollector] = None,
        delivery_success_rate: float = 1.0,
        simulated_delay: float = 0.001,
    ):
        """
        Initialize mock messaging core.

        Args:
            metrics_collector: Optional metrics collector for tracking
            delivery_success_rate: Rate of successful deliveries (0.0-1.0)
            simulated_delay: Delay in seconds to simulate delivery time
        """
        self.metrics_collector = metrics_collector
        self.delivery_success_rate = delivery_success_rate
        self.simulated_delay = simulated_delay
        self.sent_messages: list[dict] = []

    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Simulate message delivery - NO REAL AGENT INTERACTION.

        Args:
            content: Message content
            sender: Message sender
            recipient: Message recipient
            message_type: Type of message
            priority: Message priority
            tags: Message tags
            metadata: Additional metadata

        Returns:
            True if simulated delivery successful, False otherwise
        """
        # Record message for metrics
        message_record = {
            "content": content,
            "sender": sender,
            "recipient": recipient,
            "message_type": message_type,
            "priority": priority,
            "tags": tags or [],
            "metadata": metadata or {},
            "timestamp": datetime.now(),
            "delivered": random.random() < self.delivery_success_rate,
        }

        self.sent_messages.append(message_record)

        # Collect metrics
        if self.metrics_collector:
            self.metrics_collector.record_message(message_record)

        # Simulate delivery delay
        time.sleep(self.simulated_delay)

        return message_record["delivered"]

    def get_sent_messages(self) -> list[dict]:
        """Get all sent messages for analysis."""
        return self.sent_messages.copy()

    def reset(self):
        """Reset mock state for new test run."""
        self.sent_messages.clear()
        if self.metrics_collector:
            self.metrics_collector.reset()




