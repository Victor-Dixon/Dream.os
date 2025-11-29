"""
Unit tests for src/core/config_thresholds.py
"""

import pytest
from unittest.mock import patch

from src.core.config_thresholds import ThresholdConfig


class TestThresholdConfig:
    """Test ThresholdConfig dataclass."""

    @patch('src.core.config_thresholds.get_config')
    def test_threshold_config_creation(self, mock_get_config):
        """Test that ThresholdConfig can be created."""
        mock_get_config.side_effect = lambda key, default: default
        config = ThresholdConfig()
        assert config is not None

    @patch('src.core.config_thresholds.get_config')
    def test_threshold_config_quality_monitoring(self, mock_get_config):
        """Test quality monitoring threshold fields."""
        mock_get_config.side_effect = lambda key, default: default
        config = ThresholdConfig()
        assert isinstance(config.test_failure_threshold, int)
        assert isinstance(config.performance_degradation_threshold, float)
        assert isinstance(config.coverage_threshold, float)

    @patch('src.core.config_thresholds.get_config')
    def test_threshold_config_performance_targets(self, mock_get_config):
        """Test performance benchmark target fields."""
        mock_get_config.side_effect = lambda key, default: default
        config = ThresholdConfig()
        assert isinstance(config.response_time_target, float)
        assert isinstance(config.throughput_target, float)
        assert isinstance(config.scalability_target, int)
        assert isinstance(config.reliability_target, float)
        assert isinstance(config.latency_target, float)

    @patch('src.core.config_thresholds.get_config')
    def test_threshold_config_messaging_thresholds(self, mock_get_config):
        """Test messaging performance threshold fields."""
        mock_get_config.side_effect = lambda key, default: default
        config = ThresholdConfig()
        assert isinstance(config.single_message_timeout, float)
        assert isinstance(config.bulk_message_timeout, float)
        assert isinstance(config.concurrent_message_timeout, float)
        assert isinstance(config.min_throughput, float)
        assert isinstance(config.max_memory_per_message, int)

    @patch('src.core.config_thresholds.get_config')
    def test_threshold_config_alert_rules(self, mock_get_config):
        """Test alert_rules property."""
        mock_get_config.side_effect = lambda key, default: default
        config = ThresholdConfig()
        rules = config.alert_rules
        assert isinstance(rules, dict)
        assert "test_failure" in rules
        assert "performance_degradation" in rules
        assert "low_coverage" in rules
        assert rules["test_failure"]["severity"] == "high"
        assert rules["performance_degradation"]["severity"] == "medium"
        assert rules["low_coverage"]["severity"] == "medium"

    @patch('src.core.config_thresholds.get_config')
    def test_threshold_config_benchmark_targets(self, mock_get_config):
        """Test benchmark_targets property."""
        mock_get_config.side_effect = lambda key, default: default
        config = ThresholdConfig()
        targets = config.benchmark_targets
        assert isinstance(targets, dict)
        assert "response_time" in targets
        assert "throughput" in targets
        assert "scalability" in targets
        assert "reliability" in targets
        assert "latency" in targets
        assert targets["response_time"]["unit"] == "ms"
        assert targets["throughput"]["unit"] == "ops/sec"



