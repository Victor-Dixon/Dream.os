"""
Unit tests for src/core/config_ssot.py - SSOT Configuration System
"""

import pytest

from src.core.config_ssot import (
    get_config,
    get_agent_config,
    get_browser_config,
    get_test_config,
    get_threshold_config,
    get_timeout_config,
    get_unified_config,
    reload_config,
    validate_config,
    AgentConfig,
    BrowserConfig,
    TestConfig,
    ThresholdConfig,
    TimeoutConfig,
)


class TestConfigSSOTAccessors:
    """Test configuration accessor functions."""

    def test_get_config_returns_config(self):
        """Test that get_config() returns a configuration object."""
        config = get_config()
        assert config is not None

    def test_get_agent_config_returns_agent_config(self):
        """Test that get_agent_config() returns agent configuration."""
        agent_config = get_agent_config("Agent-1")
        assert agent_config is not None

    def test_get_browser_config_returns_browser_config(self):
        """Test that get_browser_config() returns browser configuration."""
        browser_config = get_browser_config()
        assert browser_config is not None

    def test_get_test_config_returns_test_config(self):
        """Test that get_test_config() returns test configuration."""
        test_config = get_test_config()
        assert test_config is not None

    def test_get_threshold_config_returns_threshold_config(self):
        """Test that get_threshold_config() returns threshold configuration."""
        threshold_config = get_threshold_config()
        assert threshold_config is not None

    def test_get_timeout_config_returns_timeout_config(self):
        """Test that get_timeout_config() returns timeout configuration."""
        timeout_config = get_timeout_config()
        assert timeout_config is not None

    def test_get_unified_config_returns_unified_config(self):
        """Test that get_unified_config() returns unified configuration."""
        unified_config = get_unified_config()
        assert unified_config is not None

    def test_reload_config_reloads_configuration(self):
        """Test that reload_config() reloads configuration."""
        result = reload_config()
        assert result is not None

    def test_validate_config_validates_configuration(self):
        """Test that validate_config() validates configuration."""
        result = validate_config()
        assert isinstance(result, bool)


class TestConfigSSOTDataclasses:
    """Test configuration dataclasses."""

    def test_agent_config_creation(self):
        """Test that AgentConfig can be created."""
        # Test with minimal required fields
        config = AgentConfig(agent_id="Agent-1")
        assert config.agent_id == "Agent-1"

    def test_browser_config_creation(self):
        """Test that BrowserConfig can be created."""
        config = BrowserConfig()
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

