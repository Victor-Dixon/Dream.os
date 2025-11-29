"""
Tests for stats_tracker.py

Comprehensive tests for coordination statistics tracking and reporting.
Target: ≥85% coverage
"""

import pytest
from datetime import datetime
from src.services.coordination.stats_tracker import StatsTracker


class TestStatsTracker:
    """Tests for StatsTracker."""

    def test_initialization(self):
        """Test tracker initialization."""
        tracker = StatsTracker()
        assert tracker.coordination_stats["total_coordinations"] == 0
        assert tracker.coordination_stats["successful_coordinations"] == 0
        assert tracker.coordination_stats["failed_coordinations"] == 0
        assert tracker.coordination_stats["average_coordination_time"] == 0.0
        assert isinstance(tracker.detailed_stats, dict)
        assert isinstance(tracker.performance_history, list)

    def test_update_coordination_stats_success(self):
        """Test updating stats for successful coordination."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.5,
            strategy="urgent_delivery",
            priority="urgent",
            message_type="text",
            sender_type="agent",
        )
        
        assert tracker.coordination_stats["total_coordinations"] == 1
        assert tracker.coordination_stats["successful_coordinations"] == 1
        assert tracker.coordination_stats["failed_coordinations"] == 0
        assert tracker.coordination_stats["average_coordination_time"] == 1.5
        assert len(tracker.performance_history) == 1

    def test_update_coordination_stats_failure(self):
        """Test updating stats for failed coordination."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=False,
            coordination_time=0.5,
        )
        
        assert tracker.coordination_stats["total_coordinations"] == 1
        assert tracker.coordination_stats["successful_coordinations"] == 0
        assert tracker.coordination_stats["failed_coordinations"] == 1
        assert tracker.coordination_stats["average_coordination_time"] == 0.5

    def test_update_coordination_stats_average_time_calculation(self):
        """Test average time calculation with multiple updates."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        tracker.update_coordination_stats(success=True, coordination_time=2.0)
        tracker.update_coordination_stats(success=True, coordination_time=3.0)
        
        assert tracker.coordination_stats["total_coordinations"] == 3
        assert tracker.coordination_stats["average_coordination_time"] == 2.0

    def test_update_detailed_stats_strategy(self):
        """Test updating detailed stats for strategy."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.0,
            strategy="urgent_delivery",
        )
        
        assert "urgent_delivery" in tracker.detailed_stats["strategy_stats"]
        stats = tracker.detailed_stats["strategy_stats"]["urgent_delivery"]
        assert stats["total"] == 1
        assert stats["successful"] == 1
        assert stats["failed"] == 0
        assert stats["avg_time"] == 1.0

    def test_update_detailed_stats_priority(self):
        """Test updating detailed stats for priority."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.5,
            priority="urgent",
        )
        
        assert "urgent" in tracker.detailed_stats["priority_stats"]
        stats = tracker.detailed_stats["priority_stats"]["urgent"]
        assert stats["total"] == 1
        assert stats["successful"] == 1

    def test_update_detailed_stats_message_type(self):
        """Test updating detailed stats for message type."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=2.0,
            message_type="broadcast",
        )
        
        assert "broadcast" in tracker.detailed_stats["type_stats"]
        stats = tracker.detailed_stats["type_stats"]["broadcast"]
        assert stats["total"] == 1

    def test_update_detailed_stats_sender_type(self):
        """Test updating detailed stats for sender type."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.0,
            sender_type="captain",
        )
        
        assert "captain" in tracker.detailed_stats["sender_stats"]
        stats = tracker.detailed_stats["sender_stats"]["captain"]
        assert stats["total"] == 1

    def test_update_category_stats_multiple_updates(self):
        """Test category stats with multiple updates."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.0,
            strategy="urgent_delivery",
        )
        tracker.update_coordination_stats(
            success=False,
            coordination_time=2.0,
            strategy="urgent_delivery",
        )
        
        stats = tracker.detailed_stats["strategy_stats"]["urgent_delivery"]
        assert stats["total"] == 2
        assert stats["successful"] == 1
        assert stats["failed"] == 1
        assert stats["avg_time"] == 1.5

    def test_performance_history_recording(self):
        """Test performance history recording."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.5,
            strategy="test_strategy",
        )
        
        assert len(tracker.performance_history) == 1
        record = tracker.performance_history[0]
        assert record["success"] is True
        assert record["coordination_time"] == 1.5
        assert record["strategy"] == "test_strategy"
        assert "timestamp" in record

    def test_performance_history_limit(self):
        """Test performance history limit (1000 records)."""
        tracker = StatsTracker()
        for i in range(1001):
            tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        assert len(tracker.performance_history) == 1000

    def test_get_coordination_stats(self):
        """Test getting coordination stats."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        tracker.update_coordination_stats(success=True, coordination_time=2.0)
        tracker.update_coordination_stats(success=False, coordination_time=1.0)
        
        stats = tracker.get_coordination_stats()
        assert stats["total_coordinations"] == 3
        assert stats["successful_coordinations"] == 2
        assert stats["failed_coordinations"] == 1
        assert stats["success_rate"] == 2/3

    def test_get_coordination_stats_no_coordinations(self):
        """Test getting stats with no coordinations."""
        tracker = StatsTracker()
        stats = tracker.get_coordination_stats()
        assert stats["total_coordinations"] == 0
        assert stats["success_rate"] == 0.0

    def test_get_detailed_stats(self):
        """Test getting detailed stats."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.0,
            strategy="test_strategy",
            priority="urgent",
        )
        
        detailed = tracker.get_detailed_stats()
        assert "strategy_stats" in detailed
        assert "priority_stats" in detailed
        assert "test_strategy" in detailed["strategy_stats"]
        assert "urgent" in detailed["priority_stats"]
        assert "success_rate" in detailed["strategy_stats"]["test_strategy"]

    def test_get_detailed_stats_empty(self):
        """Test getting detailed stats with no data."""
        tracker = StatsTracker()
        detailed = tracker.get_detailed_stats()
        assert isinstance(detailed, dict)
        assert "strategy_stats" in detailed

    def test_get_performance_summary(self):
        """Test getting performance summary."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        tracker.update_coordination_stats(success=True, coordination_time=2.0)
        tracker.update_coordination_stats(success=False, coordination_time=1.0)
        
        summary = tracker.get_performance_summary(hours=24)
        assert summary["total_coordinations"] == 3
        assert summary["successful"] == 2
        assert summary["failed"] == 1
        assert summary["success_rate"] == 2/3
        assert summary["average_coordination_time"] == pytest.approx(4/3)

    def test_get_performance_summary_no_data(self):
        """Test getting performance summary with no data."""
        tracker = StatsTracker()
        summary = tracker.get_performance_summary(hours=24)
        assert "message" in summary
        assert "No data available" in summary["message"]

    def test_get_performance_summary_custom_hours(self):
        """Test getting performance summary with custom hours."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        summary = tracker.get_performance_summary(hours=1)
        assert summary["time_period_hours"] == 1

    def test_reset_stats(self):
        """Test resetting stats."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        tracker.update_coordination_stats(success=True, coordination_time=2.0)
        
        tracker.reset_stats()
        
        assert tracker.coordination_stats["total_coordinations"] == 0
        assert tracker.coordination_stats["successful_coordinations"] == 0
        assert tracker.coordination_stats["failed_coordinations"] == 0
        assert tracker.coordination_stats["average_coordination_time"] == 0.0
        assert len(tracker.detailed_stats["strategy_stats"]) == 0
        assert len(tracker.performance_history) == 0

    def test_get_tracker_status(self):
        """Test getting tracker status."""
        tracker = StatsTracker()
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        status = tracker.get_tracker_status()
        assert "coordination_stats" in status
        assert "detailed_stats_categories" in status
        assert "performance_history_count" in status
        assert status["performance_history_count"] == 1

