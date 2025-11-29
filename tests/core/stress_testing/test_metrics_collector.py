"""
Unit tests for MetricsCollector

Tests metrics collection and analysis functionality.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.stress_testing.metrics_collector import MetricsCollector
from src.core.messaging_models_core import UnifiedMessageType


class TestMetricsCollector:
    """Test suite for MetricsCollector."""

    def test_initialization(self):
        """Test initialization."""
        collector = MetricsCollector()
        
        assert collector.success_count == 0
        assert collector.failure_count == 0
        assert len(collector.messages) == 0

    def test_record_message_success(self):
        """Test recording successful message."""
        collector = MetricsCollector()
        
        collector.record_message({"delivered": True})
        
        assert collector.success_count == 1
        assert collector.failure_count == 0
        assert len(collector.messages) == 1

    def test_record_message_failure(self):
        """Test recording failed message."""
        collector = MetricsCollector()
        
        collector.record_message({"delivered": False})
        
        assert collector.success_count == 0
        assert collector.failure_count == 1

    def test_get_metrics_empty(self):
        """Test getting metrics with no messages."""
        collector = MetricsCollector()
        
        metrics = collector.get_metrics()
        
        assert metrics["total_messages"] == 0
        assert metrics["success_count"] == 0
        assert metrics["failure_count"] == 0
        assert metrics["success_rate"] == 0.0

    def test_get_metrics_with_messages(self):
        """Test getting metrics with messages."""
        collector = MetricsCollector()
        
        collector.record_message({"delivered": True, "message_type": UnifiedMessageType.SYSTEM_TO_AGENT, "recipient": "Agent-1"})
        collector.record_message({"delivered": True, "message_type": UnifiedMessageType.BROADCAST, "recipient": "ALL"})
        collector.record_message({"delivered": False, "message_type": UnifiedMessageType.SYSTEM_TO_AGENT, "recipient": "Agent-2"})
        
        metrics = collector.get_metrics()
        
        assert metrics["total_messages"] == 3
        assert metrics["success_count"] == 2
        assert metrics["failure_count"] == 1
        assert metrics["success_rate"] == 2/3

    def test_get_metrics_by_type(self):
        """Test grouping by message type."""
        collector = MetricsCollector()
        
        collector.record_message({"delivered": True, "message_type": UnifiedMessageType.SYSTEM_TO_AGENT, "recipient": "Agent-1"})
        collector.record_message({"delivered": True, "message_type": UnifiedMessageType.BROADCAST, "recipient": "ALL"})
        collector.record_message({"delivered": True, "message_type": UnifiedMessageType.SYSTEM_TO_AGENT, "recipient": "Agent-2"})
        
        metrics = collector.get_metrics()
        
        # Check that message types are present (value format may vary)
        assert len(metrics["by_message_type"]) == 2
        type_values = list(metrics["by_message_type"].values())
        assert 2 in type_values  # SYSTEM_TO_AGENT count
        assert 1 in type_values  # BROADCAST count

    def test_get_metrics_by_agent(self):
        """Test grouping by agent."""
        collector = MetricsCollector()
        
        collector.record_message({"delivered": True, "recipient": "Agent-1"})
        collector.record_message({"delivered": True, "recipient": "Agent-2"})
        collector.record_message({"delivered": True, "recipient": "Agent-1"})
        
        metrics = collector.get_metrics()
        
        assert metrics["by_agent"]["Agent-1"] == 2
        assert metrics["by_agent"]["Agent-2"] == 1

    def test_reset(self):
        """Test reset functionality."""
        collector = MetricsCollector()
        
        collector.record_message({"delivered": True})
        collector.record_message({"delivered": False})
        
        assert collector.success_count == 1
        assert collector.failure_count == 1
        
        collector.reset()
        
        assert collector.success_count == 0
        assert collector.failure_count == 0
        assert len(collector.messages) == 0

