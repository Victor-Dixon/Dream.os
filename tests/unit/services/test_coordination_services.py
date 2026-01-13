#!/usr/bin/env python3
"""
Unit Tests for Coordination Services
====================================

Tests for bulk_coordinator, coordination_throttler, and stats_tracker.

<!-- SSOT Domain: testing -->

Author: Agent-1 (Integration & Core Systems Specialist)
"""

import json
import tempfile
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestCoordinationThrottler:
    """Unit tests for CoordinationThrottler."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temp file for cache
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = Path(self.temp_dir) / "test_coordination_cache.json"
        
        # Import here to avoid import issues
        from src.services.coordination.coordination_throttler import CoordinationThrottler
        self.throttler = CoordinationThrottler(cache_file=self.cache_file)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_creates_cache_file_parent(self):
        """Test that init creates parent directory for cache file."""
        assert self.cache_file.parent.exists()

    def test_can_send_coordination_first_message(self):
        """Test that first message is always allowed."""
        can_send, reason, wait = self.throttler.can_send_coordination("Agent-2", "Agent-1")
        
        assert can_send is True
        assert reason == "OK"
        assert wait is None

    def test_record_coordination_updates_cache(self):
        """Test that recording coordination updates the cache."""
        self.throttler.record_coordination("Agent-2", "Agent-1")
        
        key = "Agent-1->Agent-2"
        assert key in self.throttler.cache
        assert len(self.throttler.cache[key]) == 1

    def test_min_interval_enforcement(self):
        """Test minimum interval between messages is enforced."""
        # Send first message
        self.throttler.record_coordination("Agent-2", "Agent-1")
        
        # Try to send immediately - should be blocked
        can_send, reason, wait = self.throttler.can_send_coordination("Agent-2", "Agent-1")
        
        assert can_send is False
        assert "Rate limited" in reason
        assert wait is not None
        assert wait > 0

    def test_burst_limit_enforcement(self):
        """Test burst limit is enforced."""
        # Simulate 8 messages in quick succession (at allowed intervals)
        for i in range(8):
            self.throttler.burst_buckets["Agent-1->Agent-2"] = []
            for j in range(i + 1):
                self.throttler.burst_buckets["Agent-1->Agent-2"].append(time.time() - j * 0.1)
        
        # Set burst bucket to max
        self.throttler.burst_buckets["Agent-1->Agent-2"] = [time.time()] * 8
        
        can_send, reason, wait = self.throttler.can_send_coordination("Agent-2", "Agent-1")
        
        # Should hit burst limit
        assert can_send is False
        assert "Burst limit" in reason or "Rate limited" in reason

    def test_get_coordination_stats_no_history(self):
        """Test getting stats when no history exists."""
        stats = self.throttler.get_coordination_stats("Agent-2", "Agent-1")
        
        assert stats["total_messages"] == 0
        assert stats["messages_last_24h"] == 0
        assert stats["messages_last_8h"] == 0
        assert stats["last_message_hours_ago"] is None

    def test_get_coordination_stats_with_history(self):
        """Test getting stats with message history."""
        self.throttler.record_coordination("Agent-2", "Agent-1")
        
        stats = self.throttler.get_coordination_stats("Agent-2", "Agent-1")
        
        assert stats["total_messages"] == 1
        assert stats["messages_last_24h"] == 1
        assert stats["messages_last_8h"] == 1
        assert stats["last_message_hours_ago"] is not None
        assert stats["last_message_hours_ago"] < 0.01  # Less than 1 minute ago

    def test_cache_persistence(self):
        """Test that cache is persisted to disk."""
        self.throttler.record_coordination("Agent-2", "Agent-1")
        
        # Check file was written
        assert self.cache_file.exists()
        
        # Verify content
        with open(self.cache_file, 'r') as f:
            data = json.load(f)
        
        assert "Agent-1->Agent-2" in data

    def test_cache_loads_on_init(self):
        """Test that existing cache is loaded on init."""
        # Pre-populate cache file
        test_data = {"Agent-1->Agent-2": [time.time()]}
        with open(self.cache_file, 'w') as f:
            json.dump(test_data, f)
        
        # Create new throttler instance
        from src.services.coordination.coordination_throttler import CoordinationThrottler
        new_throttler = CoordinationThrottler(cache_file=self.cache_file)
        
        assert "Agent-1->Agent-2" in new_throttler.cache


class TestStatsTracker:
    """Unit tests for StatsTracker."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.coordination.stats_tracker import StatsTracker
        self.tracker = StatsTracker()

    def test_init_creates_empty_stats(self):
        """Test that init creates empty stats dictionaries."""
        assert self.tracker.coordination_stats["total_coordinations"] == 0
        assert self.tracker.coordination_stats["successful_coordinations"] == 0
        assert self.tracker.coordination_stats["failed_coordinations"] == 0

    def test_update_coordination_stats_success(self):
        """Test updating stats with successful coordination."""
        self.tracker.update_coordination_stats(
            success=True,
            coordination_time=0.5,
            strategy="direct",
            priority="high"
        )
        
        assert self.tracker.coordination_stats["total_coordinations"] == 1
        assert self.tracker.coordination_stats["successful_coordinations"] == 1
        assert self.tracker.coordination_stats["failed_coordinations"] == 0

    def test_update_coordination_stats_failure(self):
        """Test updating stats with failed coordination."""
        self.tracker.update_coordination_stats(
            success=False,
            coordination_time=0.3
        )
        
        assert self.tracker.coordination_stats["total_coordinations"] == 1
        assert self.tracker.coordination_stats["successful_coordinations"] == 0
        assert self.tracker.coordination_stats["failed_coordinations"] == 1

    def test_average_coordination_time(self):
        """Test average coordination time calculation."""
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        self.tracker.update_coordination_stats(success=True, coordination_time=3.0)
        
        avg = self.tracker.coordination_stats["average_coordination_time"]
        assert avg == 2.0

    def test_detailed_stats_by_strategy(self):
        """Test detailed stats tracking by strategy."""
        self.tracker.update_coordination_stats(
            success=True,
            coordination_time=0.5,
            strategy="bulk"
        )
        
        detailed = self.tracker.get_detailed_stats()
        assert "bulk" in detailed["strategy_stats"]
        assert detailed["strategy_stats"]["bulk"]["total"] == 1
        assert detailed["strategy_stats"]["bulk"]["successful"] == 1

    def test_detailed_stats_by_priority(self):
        """Test detailed stats tracking by priority."""
        self.tracker.update_coordination_stats(
            success=True,
            coordination_time=0.5,
            priority="urgent"
        )
        
        detailed = self.tracker.get_detailed_stats()
        assert "urgent" in detailed["priority_stats"]

    def test_get_coordination_stats_success_rate(self):
        """Test success rate calculation in stats."""
        self.tracker.update_coordination_stats(success=True, coordination_time=0.5)
        self.tracker.update_coordination_stats(success=False, coordination_time=0.5)
        
        stats = self.tracker.get_coordination_stats()
        assert stats["success_rate"] == 0.5

    def test_get_coordination_stats_zero_coordinations(self):
        """Test success rate is 0 when no coordinations."""
        stats = self.tracker.get_coordination_stats()
        assert stats["success_rate"] == 0.0

    def test_performance_history_limit(self):
        """Test performance history is limited to 1000 records."""
        for i in range(1100):
            self.tracker.update_coordination_stats(success=True, coordination_time=0.1)
        
        assert len(self.tracker.performance_history) == 1000

    def test_performance_summary(self):
        """Test performance summary for time period."""
        self.tracker.update_coordination_stats(success=True, coordination_time=0.5)
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        summary = self.tracker.get_performance_summary(hours=1)
        
        assert summary["total_coordinations"] == 2
        assert summary["successful"] == 2
        assert summary["failed"] == 0
        assert summary["success_rate"] == 1.0

    def test_reset_stats(self):
        """Test resetting all stats."""
        self.tracker.update_coordination_stats(success=True, coordination_time=0.5)
        self.tracker.reset_stats()
        
        assert self.tracker.coordination_stats["total_coordinations"] == 0
        assert len(self.tracker.performance_history) == 0

    def test_get_tracker_status(self):
        """Test getting tracker status."""
        status = self.tracker.get_tracker_status()
        
        assert "coordination_stats" in status
        assert "detailed_stats_categories" in status
        assert "performance_history_count" in status


class TestBulkCoordinator:
    """Unit tests for BulkCoordinator."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.coordination.bulk_coordinator import BulkCoordinator
        self.coordinator = BulkCoordinator()

    def test_init_creates_strategy_coordinator(self):
        """Test that init creates strategy coordinator."""
        assert self.coordinator.strategy_coordinator is not None

    def test_coordinate_bulk_messages_empty_list(self):
        """Test coordinating empty message list."""
        result = self.coordinator.coordinate_bulk_messages([])
        
        assert result["success"] is True
        assert result["total_messages"] == 0
        assert result["successful"] == 0
        assert result["failed"] == 0

    @patch('src.services.coordination.bulk_coordinator.StrategyCoordinator')
    def test_coordinate_bulk_messages_with_messages(self, mock_strategy):
        """Test coordinating list of messages."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessagePriority
        
        # Create mock messages
        mock_msg = MagicMock(spec=UnifiedMessage)
        mock_msg.message_id = "test-123"
        mock_msg.recipient = "Agent-2"
        mock_msg.priority = UnifiedMessagePriority.REGULAR
        mock_msg.message_type = MagicMock()
        mock_msg.sender_type = MagicMock()
        
        # Mock strategy coordinator
        mock_strategy_instance = MagicMock()
        mock_strategy_instance.determine_coordination_strategy.return_value = "direct"
        mock_strategy_instance.apply_coordination_rules.return_value = {"applied": True}
        self.coordinator.strategy_coordinator = mock_strategy_instance
        
        result = self.coordinator.coordinate_bulk_messages([mock_msg])
        
        assert result["success"] is True
        assert result["total_messages"] == 1
        assert "results" in result

    def test_group_messages_by_strategy(self):
        """Test message grouping by strategy."""
        from src.core.messaging_models_core import UnifiedMessage
        
        # Create mock messages
        mock_msg1 = MagicMock(spec=UnifiedMessage)
        mock_msg2 = MagicMock(spec=UnifiedMessage)
        
        # Mock strategy coordinator to return different strategies
        self.coordinator.strategy_coordinator.determine_coordination_strategy = MagicMock(
            side_effect=["direct", "bulk"]
        )
        
        grouped = self.coordinator._group_messages_by_strategy([mock_msg1, mock_msg2])
        
        assert "direct" in grouped
        assert "bulk" in grouped

    def test_get_bulk_coordinator_status(self):
        """Test getting bulk coordinator status."""
        status = self.coordinator.get_bulk_coordinator_status()
        
        assert "strategy_coordinator_status" in status
        assert "available_grouping_methods" in status
        assert "strategy" in status["available_grouping_methods"]
        assert "priority" in status["available_grouping_methods"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

