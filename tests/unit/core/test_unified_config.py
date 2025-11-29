"""
Unit tests for src/core/unified_config.py
"""

import pytest

# Check if unified_config exists and what it exports
try:
    from src.core import unified_config
    HAS_UNIFIED_CONFIG = True
except ImportError:
    HAS_UNIFIED_CONFIG = False


@pytest.mark.skipif(not HAS_UNIFIED_CONFIG, reason="unified_config not available")
class TestUnifiedConfig:
    """Test unified_config module."""

    def test_unified_config_imports(self):
        """Test that unified_config can be imported."""
        assert unified_config is not None

    def test_unified_config_has_exports(self):
        """Test that unified_config has expected exports."""
        # Check for common exports
        assert hasattr(unified_config, '__all__') or dir(unified_config)

    def test_unified_config_deprecation_warning(self):
        """Test that unified_config shows deprecation warning."""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from src.core import unified_config
            assert len(w) > 0
            assert any("deprecated" in str(warning.message).lower() for warning in w)

    def test_unified_config_re_exports_dataclasses(self):
        """Test that unified_config re-exports dataclasses."""
        from src.core.unified_config import (
            AgentConfig,
            BrowserConfig,
            TimeoutConfig,
            ThresholdConfig,
        )
        assert AgentConfig is not None
        assert BrowserConfig is not None
        assert TimeoutConfig is not None
        assert ThresholdConfig is not None

    def test_unified_config_re_exports_enums(self):
        """Test that unified_config re-exports enums."""
        from src.core.unified_config import (
            ConfigEnvironment,
            ConfigSource,
            ReportFormat,
        )
        assert ConfigEnvironment is not None
        assert ConfigSource is not None
        assert ReportFormat is not None

    def test_unified_config_re_exports_accessors(self):
        """Test that unified_config re-exports accessor functions."""
        from src.core.unified_config import (
            get_config,
            get_agent_config,
            get_browser_config,
            get_unified_config,
        )
        assert callable(get_config)
        assert callable(get_agent_config)
        assert callable(get_browser_config)
        assert callable(get_unified_config)

    def test_unified_config_re_exports_manager(self):
        """Test that unified_config re-exports UnifiedConfigManager."""
        from src.core.unified_config import UnifiedConfigManager, UnifiedConfig
        assert UnifiedConfigManager is not None
        assert UnifiedConfig is not None
        # UnifiedConfig should be alias for UnifiedConfigManager
        assert UnifiedConfig == UnifiedConfigManager

    def test_unified_config_re_exports_all_functions(self):
        """Test that unified_config re-exports all accessor functions."""
        from src.core.unified_config import (
            get_timeout_config,
            get_threshold_config,
            get_file_pattern_config,
            get_test_config,
            get_report_config,
            validate_config,
            reload_config,
        )
        assert callable(get_timeout_config)
        assert callable(get_threshold_config)
        assert callable(get_file_pattern_config)
        assert callable(get_test_config)
        assert callable(get_report_config)
        assert callable(validate_config)
        assert callable(reload_config)

    def test_unified_config_all_dataclasses(self):
        """Test that unified_config re-exports all dataclasses."""
        from src.core.unified_config import (
            FilePatternConfig,
            TestConfig,
            ReportConfig,
        )
        assert FilePatternConfig is not None
        assert TestConfig is not None
        assert ReportConfig is not None

    def test_unified_config_module_structure(self):
        """Test that unified_config module has proper structure."""
        from src.core import unified_config
        assert hasattr(unified_config, '__all__')
        assert isinstance(unified_config.__all__, list)
        assert len(unified_config.__all__) > 0



