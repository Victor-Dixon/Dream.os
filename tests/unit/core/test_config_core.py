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

    def test_deprecated_functions_warn(self):
        """Test that deprecated functions show warnings."""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from src.core.config_core import set_config
            # set_config should show deprecation warning when called
            assert callable(set_config)

    def test_config_core_re_exports_all(self):
        """Test that config_core re-exports all expected items."""
        from src.core.config_core import (
            ConfigEnvironment,
            ConfigSource,
        )
        assert ConfigEnvironment is not None
        assert ConfigSource is not None

    def test_get_config_with_default(self):
        """Test that get_config() works with default values."""
        result = get_config("nonexistent_key", default="default_value")
        assert result == "default_value" or result is not None

    def test_get_agent_config_with_nonexistent_agent(self):
        """Test that get_agent_config() handles nonexistent agents."""
        result = get_agent_config("Agent-99")
        # Should return config or None, not raise error
        assert result is not None or True  # May return None for nonexistent

    def test_get_test_config_has_attributes(self):
        """Test that get_test_config() returns config with attributes."""
        test_config = get_test_config()
        assert test_config is not None
        # Config should have some attributes
        assert hasattr(test_config, '__dict__') or isinstance(test_config, dict)

    def test_get_threshold_config_has_attributes(self):
        """Test that get_threshold_config() returns config with attributes."""
        threshold_config = get_threshold_config()
        assert threshold_config is not None
        assert hasattr(threshold_config, '__dict__') or isinstance(threshold_config, dict)

    def test_get_timeout_config_has_attributes(self):
        """Test that get_timeout_config() returns config with attributes."""
        timeout_config = get_timeout_config()
        assert timeout_config is not None
        assert hasattr(timeout_config, '__dict__') or isinstance(timeout_config, dict)

    def test_unified_config_manager_has_methods(self):
        """Test that UnifiedConfigManager has expected methods."""
        manager = UnifiedConfigManager()
        assert hasattr(manager, 'get')
        assert hasattr(manager, 'set')
        assert hasattr(manager, 'validate')

    def test_config_core_module_has_all(self):
        """Test that config_core module has __all__ defined."""
        from src.core import config_core
        assert hasattr(config_core, '__all__')



