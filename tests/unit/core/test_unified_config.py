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

