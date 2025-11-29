"""
Unit tests for src/core/config/config_dataclasses.py
"""

import pytest

from src.core.config.config_dataclasses import (
    AgentConfig,
    BrowserConfig,
    FilePatternConfig,
    ReportConfig,
    TestConfig,
    ThresholdConfig,
    TimeoutConfig,
)


class TestConfigDataclasses:
    """Test configuration dataclasses."""

    def test_agent_config_creation(self):
        """Test that AgentConfig can be created."""
        config = AgentConfig()
        assert config is not None

    def test_browser_config_creation(self):
        """Test that BrowserConfig can be created."""
        config = BrowserConfig()
        assert config is not None

    def test_file_pattern_config_creation(self):
        """Test that FilePatternConfig can be created."""
        config = FilePatternConfig()
        assert config is not None

    def test_report_config_creation(self):
        """Test that ReportConfig can be created."""
        config = ReportConfig()
        assert config is not None

    def test_test_config_creation(self):
        """Test that TestConfig can be created."""
        config = TestConfig()
        assert config is not None

    def test_threshold_config_creation(self):
        """Test that ThresholdConfig can be created."""
        config = ThresholdConfig()
        assert config is not None

    def test_timeout_config_creation(self):
        """Test that TimeoutConfig can be created."""
        config = TimeoutConfig()
        assert config is not None



