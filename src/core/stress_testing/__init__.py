"""
<!-- SSOT Domain: core -->

Stress Testing Module for MessageQueueProcessor

Provides mock messaging core and stress testing utilities for testing
message queue processing without real agent interaction.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

from .messaging_core_protocol import MessagingCoreProtocol
from .mock_messaging_core import MockMessagingCore
from .real_messaging_core_adapter import RealMessagingCoreAdapter
from .metrics_collector import MetricsCollector
from .message_generator import MessageGenerator
from .stress_runner import StressTestRunner

__all__ = [
    "MessagingCoreProtocol",
    "MockMessagingCore",
    "RealMessagingCoreAdapter",
    "MetricsCollector",
    "MessageGenerator",
    "StressTestRunner",
]




