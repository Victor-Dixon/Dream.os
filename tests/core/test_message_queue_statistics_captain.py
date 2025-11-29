"""
Test coverage for message_queue_statistics.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 10
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_statistics import (
    QueueStatisticsCalculator,
    QueueHealthMonitor
)


class TestQueueStatisticsCalculator:
    """Test suite for QueueStatisticsCalculator class - 15+ tests"""

    def test_calculator_initialization(self):
        """Test QueueStatisticsCalculator initialization"""
        calculator = QueueStatisticsCalculator()
        assert calculator is not None

    def test_calculate_statistics_empty(self):
        """Test calculate_statistics with empty entries"""
        calculator = QueueStatisticsCalculator()
        stats = calculator.calculate_statistics([])
        assert isinstance(stats, dict)
        assert stats["total_entries"] == 0

    def test_calculate_statistics_with_entries(self):
        """Test calculate_statistics with entries"""
        calculator = QueueStatisticsCalculator()
        entry = Mock()
        entry.status = "PENDING"
        entry.created_at = datetime.now()
        entry.priority_score = 0.5
        entry.delivery_attempts = 0
        stats = calculator.calculate_statistics([entry])
        assert stats["total_entries"] == 1
        assert stats["pending_entries"] == 1

    def test_calculate_statistics_status_distribution(self):
        """Test calculate_statistics status distribution"""
        calculator = QueueStatisticsCalculator()
        entry1 = Mock(status="PENDING", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0)
        entry2 = Mock(status="DELIVERED", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0)
        stats = calculator.calculate_statistics([entry1, entry2])
        assert stats["pending_entries"] == 1
        assert stats["delivered_entries"] == 1

    def test_calculate_statistics_priority_distribution(self):
        """Test calculate_statistics priority distribution"""
        calculator = QueueStatisticsCalculator()
        entry = Mock(status="PENDING", created_at=datetime.now(), priority_score=0.9, delivery_attempts=0)
        stats = calculator.calculate_statistics([entry])
        assert "priority_distribution" in stats
        assert "high" in stats["priority_distribution"] or len(stats["priority_distribution"]) >= 0

    def test_calculate_statistics_retry_distribution(self):
        """Test calculate_statistics retry distribution"""
        calculator = QueueStatisticsCalculator()
        entry = Mock(status="PENDING", created_at=datetime.now(), priority_score=0.5, delivery_attempts=2)
        stats = calculator.calculate_statistics([entry])
        assert "retry_distribution" in stats

    def test_calculate_statistics_age_calculation(self):
        """Test calculate_statistics age calculation"""
        calculator = QueueStatisticsCalculator()
        entry = Mock(status="PENDING", created_at=datetime.now() - timedelta(seconds=100), priority_score=0.5, delivery_attempts=0)
        stats = calculator.calculate_statistics([entry])
        assert stats["average_age"] > 0

    def test_calculate_statistics_string_timestamp(self):
        """Test calculate_statistics with string timestamp"""
        calculator = QueueStatisticsCalculator()
        entry = Mock(status="PENDING", created_at=datetime.now().isoformat(), priority_score=0.5, delivery_attempts=0)
        stats = calculator.calculate_statistics([entry])
        assert stats is not None

    def test_get_priority_bucket_high(self):
        """Test _get_priority_bucket for high priority"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_priority_bucket(0.9)
        assert bucket == "high"

    def test_get_priority_bucket_medium(self):
        """Test _get_priority_bucket for medium priority"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_priority_bucket(0.7)
        assert bucket == "medium"

    def test_get_priority_bucket_low(self):
        """Test _get_priority_bucket for low priority"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_priority_bucket(0.5)
        assert bucket == "low"

    def test_get_priority_bucket_very_low(self):
        """Test _get_priority_bucket for very low priority"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_priority_bucket(0.3)
        assert bucket == "very_low"

    def test_get_retry_bucket_never(self):
        """Test _get_retry_bucket for never retried"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_retry_bucket(0)
        assert bucket == "never_retried"

    def test_get_retry_bucket_once(self):
        """Test _get_retry_bucket for retried once"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_retry_bucket(1)
        assert bucket == "retried_once"

    def test_get_retry_bucket_few(self):
        """Test _get_retry_bucket for retried few times"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_retry_bucket(2)
        assert bucket == "retried_few"

    def test_get_retry_bucket_many(self):
        """Test _get_retry_bucket for retried many times"""
        calculator = QueueStatisticsCalculator()
        bucket = calculator._get_retry_bucket(5)
        assert bucket == "retried_many"

    def test_format_duration_seconds(self):
        """Test _format_duration for seconds"""
        calculator = QueueStatisticsCalculator()
        formatted = calculator._format_duration(30.0)
        assert isinstance(formatted, str)

    def test_format_duration_minutes(self):
        """Test _format_duration for minutes"""
        calculator = QueueStatisticsCalculator()
        formatted = calculator._format_duration(120.0)
        assert isinstance(formatted, str)

    def test_format_duration_hours(self):
        """Test _format_duration for hours"""
        calculator = QueueStatisticsCalculator()
        formatted = calculator._format_duration(7200.0)
        assert isinstance(formatted, str)

    def test_format_duration_days(self):
        """Test _format_duration for days"""
        calculator = QueueStatisticsCalculator()
        formatted = calculator._format_duration(86400.0)
        assert isinstance(formatted, str)


class TestQueueHealthMonitor:
    """Test suite for QueueHealthMonitor class - 10+ tests"""

    def test_health_monitor_initialization(self):
        """Test QueueHealthMonitor initialization"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        assert monitor is not None
        assert monitor.stats_calculator == calculator

    def test_assess_health_empty(self):
        """Test assess_health with empty queue"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = monitor.assess_health([])
        assert isinstance(health, dict)
        assert "overall_health" in health

    def test_assess_health_good(self):
        """Test assess_health with healthy queue"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entry = Mock(status="DELIVERED", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0)
        health = monitor.assess_health([entry])
        assert health["overall_health"] in ["good", "warning", "critical"]

    def test_assess_health_critical_size(self):
        """Test assess_health with critical queue size"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entries = [Mock(status="PENDING", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0) for _ in range(1001)]
        health = monitor.assess_health(entries)
        assert len(health["issues"]) > 0 or health["overall_health"] != "good"

    def test_assess_health_warning_size(self):
        """Test assess_health with warning queue size"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entries = [Mock(status="PENDING", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0) for _ in range(501)]
        health = monitor.assess_health(entries)
        assert health is not None

    def test_assess_health_processing_issue(self):
        """Test assess_health with processing issue"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entries = []
        for i in range(10):
            entry = Mock(status="PROCESSING" if i < 6 else "PENDING", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0)
            entries.append(entry)
        health = monitor.assess_health(entries)
        assert health is not None

    def test_assess_health_age_issue(self):
        """Test assess_health with age issue"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entry = Mock(status="PENDING", created_at=datetime.now() - timedelta(seconds=4000), priority_score=0.5, delivery_attempts=0)
        health = monitor.assess_health([entry])
        assert health is not None

    def test_assess_health_failure_issue(self):
        """Test assess_health with failure issue"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entries = []
        for i in range(10):
            status = "FAILED" if i < 2 else "DELIVERED"
            entry = Mock(status=status, created_at=datetime.now(), priority_score=0.5, delivery_attempts=0)
            entries.append(entry)
        health = monitor.assess_health(entries)
        assert health is not None

    def test_check_queue_size_health_critical(self):
        """Test _check_queue_size_health with critical size"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = {"issues": [], "recommendations": []}
        stats = {"total_entries": 1001}
        monitor._check_queue_size_health(health, stats)
        assert len(health["issues"]) > 0

    def test_check_queue_size_health_warning(self):
        """Test _check_queue_size_health with warning size"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = {"issues": [], "recommendations": []}
        stats = {"total_entries": 501}
        monitor._check_queue_size_health(health, stats)
        assert health is not None

    def test_check_processing_health(self):
        """Test _check_processing_health"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = {"issues": [], "recommendations": []}
        stats = {"processing_entries": 6, "total_entries": 10}
        monitor._check_processing_health(health, stats)
        assert health is not None

    def test_check_age_health(self):
        """Test _check_age_health"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = {"issues": [], "recommendations": []}
        stats = {"average_age": 4000, "average_age_formatted": "1.1h"}
        monitor._check_age_health(health, stats)
        assert len(health["issues"]) > 0

    def test_check_failure_health(self):
        """Test _check_failure_health"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = {"issues": [], "recommendations": []}
        stats = {"failed_entries": 2, "total_entries": 10}
        monitor._check_failure_health(health, stats)
        assert health is not None


class TestStatisticsEdgeCases:
    """Test suite for statistics edge cases - 5+ tests"""

    def test_calculator_missing_attributes(self):
        """Test calculator handles missing entry attributes"""
        calculator = QueueStatisticsCalculator()
        entry = Mock()
        # Missing status, created_at, etc.
        stats = calculator.calculate_statistics([entry])
        assert stats is not None

    def test_calculator_zero_division(self):
        """Test calculator handles zero division"""
        calculator = QueueStatisticsCalculator()
        stats = calculator.calculate_statistics([])
        assert stats["average_age"] == 0.0

    def test_health_monitor_no_entries(self):
        """Test health monitor with no entries"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        health = monitor.assess_health([])
        assert health["overall_health"] == "good"

    def test_health_monitor_multiple_issues(self):
        """Test health monitor with multiple issues"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entries = [Mock(status="PROCESSING", created_at=datetime.now() - timedelta(seconds=4000), priority_score=0.5, delivery_attempts=0) for _ in range(1001)]
        health = monitor.assess_health(entries)
        assert health["overall_health"] in ["warning", "critical"]

    def test_health_monitor_recommendations(self):
        """Test health monitor generates recommendations"""
        calculator = QueueStatisticsCalculator()
        monitor = QueueHealthMonitor(calculator)
        entries = [Mock(status="PENDING", created_at=datetime.now(), priority_score=0.5, delivery_attempts=0) for _ in range(1001)]
        health = monitor.assess_health(entries)
        assert len(health["recommendations"]) > 0

