"""
Unit tests for src/core/config_core.py (DEPRECATED - tests backward compatibility)
"""

import pytest
import warnings

from src.core.config_core import (
    get_config,
    get_agent_config,
    get_test_config,
    get_threshold_config,
    get_timeout_config,
    UnifiedConfigManager,
)


class TestConfigCoreDeprecation:
    """Test that config_core.py properly deprecates and re-exports from config_ssot."""

    def test_deprecation_warning_on_import(self):
        """Test that importing config_core shows deprecation warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from src.core import config_core
            assert len(w) > 0
            assert any("deprecated" in str(warning.message).lower() for warning in w)

    def test_get_config_still_works(self):
        """Test that get_config() still works via re-export."""
        config = get_config()
        assert config is not None

    def test_get_agent_config_still_works(self):
        """Test that get_agent_config() still works via re-export."""
        agent_config = get_agent_config("Agent-1")
        assert agent_config is not None

    def test_get_test_config_still_works(self):
        """Test that get_test_config() still works via re-export."""
        test_config = get_test_config()
        assert test_config is not None

    def test_get_threshold_config_still_works(self):
        """Test that get_threshold_config() still works via re-export."""
        threshold_config = get_threshold_config()
        assert threshold_config is not None

    def test_get_timeout_config_still_works(self):
        """Test that get_timeout_config() still works via re-export."""
        timeout_config = get_timeout_config()
        assert timeout_config is not None

    def test_unified_config_manager_still_works(self):
        """Test that UnifiedConfigManager still works via re-export."""
        manager = UnifiedConfigManager()
        assert manager is not None

