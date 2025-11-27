"""
Unit tests for src/core/config/config_manager.py
"""

import pytest

from src.core.config.config_manager import _config_manager


class TestConfigManager:
    """Test ConfigManager functionality."""

    def test_config_manager_exists(self):
        """Test that _config_manager exists."""
        assert _config_manager is not None

    def test_config_manager_get(self):
        """Test that config_manager.get() works."""
        # Test getting a config value
        result = _config_manager.get("test_key", default="default_value")
        assert result == "default_value"

    def test_config_manager_set(self):
        """Test that config_manager.set() works."""
        # Test setting a config value
        _config_manager.set("test_key", "test_value")
        result = _config_manager.get("test_key")
        assert result == "test_value"

    def test_config_manager_reload(self):
        """Test that config_manager.reload() works."""
        result = _config_manager.reload()
        assert result is not None

