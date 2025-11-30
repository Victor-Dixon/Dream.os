"""
Unit tests for stats_tracker.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.coordination.stats_tracker import StatsTracker


class TestStatsTracker:
    """Test suite for StatsTracker."""

    @pytest.fixture
    def tracker(self):
        """Create StatsTracker instance."""
        return StatsTracker()

    def test_tracker_initialization(self, tracker):
        """Test tracker initializes correctly."""
        assert tracker is not None
        assert tracker.coordination_stats is not None
        assert tracker.detailed_stats is not None
        assert tracker.performance_history == []

    def test_update_coordination_stats_success(self, tracker):
        """Test updating stats for successful coordination."""
        initial_total = tracker.coordination_stats["total_coordinations"]
        initial_successful = tracker.coordination_stats["successful_coordinations"]
        
        tracker.update_coordination_stats(success=True, coordination_time=1.5)
        
        assert tracker.coordination_stats["total_coordinations"] == initial_total + 1
        assert tracker.coordination_stats["successful_coordinations"] == initial_successful + 1

    def test_update_coordination_stats_failure(self, tracker):
        """Test updating stats for failed coordination."""
        initial_total = tracker.coordination_stats["total_coordinations"]
        initial_failed = tracker.coordination_stats["failed_coordinations"]
        
        tracker.update_coordination_stats(success=False, coordination_time=2.0)
        
        assert tracker.coordination_stats["total_coordinations"] == initial_total + 1
        assert tracker.coordination_stats["failed_coordinations"] == initial_failed + 1

    def test_update_coordination_stats_averages_time(self, tracker):
        """Test coordination time averaging."""
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        tracker.update_coordination_stats(success=True, coordination_time=3.0)
        
        avg_time = tracker.coordination_stats["average_coordination_time"]
        assert avg_time == 2.0  # (1.0 + 3.0) / 2

    def test_update_coordination_stats_with_metadata(self, tracker):
        """Test updating stats with strategy and priority metadata."""
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.5,
            strategy="priority",
            priority="urgent",
            message_type="broadcast",
            sender_type="captain"
        )
        
        assert len(tracker.performance_history) == 1
        entry = tracker.performance_history[0]
        assert entry["strategy"] == "priority"
        assert entry["priority"] == "urgent"

    def test_get_coordination_stats(self, tracker):
        """Test getting coordination statistics."""
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        stats = tracker.get_coordination_stats()
        
        assert stats["total_coordinations"] == 1
        assert stats["successful_coordinations"] == 1

    def test_get_detailed_stats(self, tracker):
        """Test getting detailed statistics."""
        tracker.update_coordination_stats(
            success=True,
            coordination_time=1.0,
            strategy="priority"
        )
        
        detailed = tracker.get_detailed_stats()
        
        assert "strategy_stats" in detailed
        assert "priority_stats" in detailed

    def test_reset_stats(self, tracker):
        """Test resetting statistics."""
        tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        tracker.reset_stats()
        
        assert tracker.coordination_stats["total_coordinations"] == 0
        assert len(tracker.performance_history) == 0

