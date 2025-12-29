"""
<!-- SSOT Domain: core -->

Message Generator - Generates test messages for stress testing

Creates test messages for 9 concurrent agents and 4 message types.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

import random
from typing import Any
from ..messaging_models_core import UnifiedMessageType


class MessageGenerator:
    """Generates test messages for stress testing."""

    MESSAGE_TYPE_MAPPING = {
        "direct": UnifiedMessageType.SYSTEM_TO_AGENT,
        "broadcast": UnifiedMessageType.BROADCAST,
        "hard_onboard": UnifiedMessageType.ONBOARDING,
        "soft_onboard": UnifiedMessageType.ONBOARDING,
    }

    def __init__(self, num_agents: int = 9, message_types: list | None = None):
        """
        Initialize message generator.

        Args:
            num_agents: Number of concurrent agents (default: 9)
            message_types: List of message types to generate (default: all 4)
        """
        self.num_agents = num_agents
        self.message_types = message_types or ["direct", "broadcast", "hard_onboard", "soft_onboard"]
        self.agents = [f"Agent-{i}" for i in range(1, num_agents + 1)]

    def generate_batch(self, count: int) -> list:
        """
        Generate batch of test messages.

        Args:
            count: Number of messages to generate

        Returns:
            List of message dictionaries ready for queue
        """
        messages = []

        for i in range(count):
            msg_type_key = random.choice(self.message_types)
            recipient = (
                "ALL" if msg_type_key == "broadcast" else random.choice(self.agents)
            )

            message = {
                "type": "agent_message",
                "sender": "SYSTEM",
                "recipient": recipient,
                "content": f"Test message {i+1}",
                "priority": "regular",
                "message_type": self._map_message_type(msg_type_key),
                "tags": ["SYSTEM"],
                "metadata": {"test": True, "message_id": i + 1, "msg_type": msg_type_key},
            }

            messages.append(message)

        return messages

    def _map_message_type(self, msg_type: str) -> str:
        """
        Map message type string to UnifiedMessageType value.

        Args:
            msg_type: Message type string (direct, broadcast, hard_onboard, soft_onboard)

        Returns:
            UnifiedMessageType value string
        """
        mapped_type = self.MESSAGE_TYPE_MAPPING.get(msg_type, UnifiedMessageType.SYSTEM_TO_AGENT)
        return mapped_type.value if hasattr(mapped_type, "value") else str(mapped_type)

