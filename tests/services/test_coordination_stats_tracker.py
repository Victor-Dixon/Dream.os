"""Tests for stats_tracker.py - V2 Compliant Test Suite"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from src.services.coordination.stats_tracker import StatsTracker


class TestStatsTracker(unittest.TestCase):
    """Test suite for StatsTracker class."""

    def setUp(self):
        """Set up test fixtures."""
        self.tracker = StatsTracker()

    def test_initialization(self):
        """Test StatsTracker initialization."""
        self.assertEqual(self.tracker.coordination_stats["total_coordinations"], 0)
        self.assertEqual(self.tracker.coordination_stats["successful_coordinations"], 0)
        self.assertEqual(self.tracker.coordination_stats["failed_coordinations"], 0)
        self.assertEqual(self.tracker.coordination_stats["average_coordination_time"], 0.0)
        self.assertEqual(len(self.tracker.detailed_stats), 4)
        self.assertEqual(len(self.tracker.performance_history), 0)

    def test_update_coordination_stats_success(self):
        """Test updating stats with successful coordination."""
        self.tracker.update_coordination_stats(
            success=True, coordination_time=1.5, strategy="bulk", priority="normal"
        )
        
        self.assertEqual(self.tracker.coordination_stats["total_coordinations"], 1)
        self.assertEqual(self.tracker.coordination_stats["successful_coordinations"], 1)
        self.assertEqual(self.tracker.coordination_stats["failed_coordinations"], 0)
        self.assertEqual(self.tracker.coordination_stats["average_coordination_time"], 1.5)

    def test_update_coordination_stats_failure(self):
        """Test updating stats with failed coordination."""
        self.tracker.update_coordination_stats(
            success=False, coordination_time=0.5, strategy="direct", priority="urgent"
        )
        
        self.assertEqual(self.tracker.coordination_stats["total_coordinations"], 1)
        self.assertEqual(self.tracker.coordination_stats["successful_coordinations"], 0)
        self.assertEqual(self.tracker.coordination_stats["failed_coordinations"], 1)
        self.assertEqual(self.tracker.coordination_stats["average_coordination_time"], 0.5)

    def test_update_coordination_stats_average_time(self):
        """Test average coordination time calculation."""
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        self.tracker.update_coordination_stats(success=True, coordination_time=3.0)
        
        self.assertEqual(self.tracker.coordination_stats["average_coordination_time"], 2.0)

    def test_update_detailed_stats_strategy(self):
        """Test detailed stats update for strategy."""
        self.tracker.update_coordination_stats(
            success=True, coordination_time=1.0, strategy="bulk"
        )
        
        self.assertIn("bulk", self.tracker.detailed_stats["strategy_stats"])
        stats = self.tracker.detailed_stats["strategy_stats"]["bulk"]
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["successful"], 1)
        self.assertEqual(stats["failed"], 0)

    def test_update_detailed_stats_priority(self):
        """Test detailed stats update for priority."""
        self.tracker.update_coordination_stats(
            success=False, coordination_time=0.5, priority="urgent"
        )
        
        self.assertIn("urgent", self.tracker.detailed_stats["priority_stats"])
        stats = self.tracker.detailed_stats["priority_stats"]["urgent"]
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["successful"], 0)
        self.assertEqual(stats["failed"], 1)

    def test_update_detailed_stats_message_type(self):
        """Test detailed stats update for message type."""
        self.tracker.update_coordination_stats(
            success=True, coordination_time=2.0, message_type="broadcast"
        )
        
        self.assertIn("broadcast", self.tracker.detailed_stats["type_stats"])
        stats = self.tracker.detailed_stats["type_stats"]["broadcast"]
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["successful"], 1)

    def test_update_detailed_stats_sender_type(self):
        """Test detailed stats update for sender type."""
        self.tracker.update_coordination_stats(
            success=True, coordination_time=1.5, sender_type="agent"
        )
        
        self.assertIn("agent", self.tracker.detailed_stats["sender_stats"])
        stats = self.tracker.detailed_stats["sender_stats"]["agent"]
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["successful"], 1)

    def test_get_coordination_stats(self):
        """Test getting coordination statistics."""
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        self.tracker.update_coordination_stats(success=True, coordination_time=2.0)
        self.tracker.update_coordination_stats(success=False, coordination_time=0.5)
        
        stats = self.tracker.get_coordination_stats()
        
        self.assertEqual(stats["total_coordinations"], 3)
        self.assertEqual(stats["successful_coordinations"], 2)
        self.assertEqual(stats["failed_coordinations"], 1)
        self.assertEqual(stats["success_rate"], 2/3)

    def test_get_coordination_stats_no_data(self):
        """Test getting stats with no data."""
        stats = self.tracker.get_coordination_stats()
        
        self.assertEqual(stats["total_coordinations"], 0)
        self.assertEqual(stats["success_rate"], 0.0)

    def test_get_detailed_stats(self):
        """Test getting detailed statistics."""
        self.tracker.update_coordination_stats(
            success=True, coordination_time=1.0, strategy="bulk", priority="normal"
        )
        
        detailed = self.tracker.get_detailed_stats()
        
        self.assertIn("strategy_stats", detailed)
        self.assertIn("bulk", detailed["strategy_stats"])
        self.assertIn("success_rate", detailed["strategy_stats"]["bulk"])

    def test_get_performance_summary(self):
        """Test getting performance summary."""
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        self.tracker.update_coordination_stats(success=True, coordination_time=2.0)
        
        summary = self.tracker.get_performance_summary(hours=24)
        
        self.assertEqual(summary["total_coordinations"], 2)
        self.assertEqual(summary["successful"], 2)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["success_rate"], 1.0)

    def test_get_performance_summary_no_data(self):
        """Test performance summary with no data."""
        summary = self.tracker.get_performance_summary(hours=1)
        
        self.assertIn("message", summary)
        self.assertEqual(summary["message"], "No data available for the specified time period")

    def test_performance_history_limit(self):
        """Test performance history is limited to 1000 records."""
        for i in range(1001):
            self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        self.assertEqual(len(self.tracker.performance_history), 1000)

    def test_reset_stats(self):
        """Test resetting statistics."""
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        self.tracker.reset_stats()
        
        self.assertEqual(self.tracker.coordination_stats["total_coordinations"], 0)
        self.assertEqual(len(self.tracker.detailed_stats["strategy_stats"]), 0)
        self.assertEqual(len(self.tracker.performance_history), 0)

    def test_get_tracker_status(self):
        """Test getting tracker status."""
        self.tracker.update_coordination_stats(success=True, coordination_time=1.0)
        
        status = self.tracker.get_tracker_status()
        
        self.assertIn("coordination_stats", status)
        self.assertIn("detailed_stats_categories", status)
        self.assertIn("performance_history_count", status)
        self.assertEqual(status["performance_history_count"], 1)


if __name__ == "__main__":
    unittest.main()
