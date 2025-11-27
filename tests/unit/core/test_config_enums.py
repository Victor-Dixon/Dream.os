"""
Unit tests for src/core/config/config_enums.py
"""

import pytest

from src.core.config.config_enums import (
    ConfigEnvironment,
    ConfigSource,
)


class TestConfigEnums:
    """Test configuration enum classes."""

    def test_config_environment_enum(self):
        """Test ConfigEnvironment enum values."""
        assert ConfigEnvironment.DEVELOPMENT.value == "development"
        assert ConfigEnvironment.PRODUCTION.value == "production"
        assert ConfigEnvironment.TESTING.value == "testing"

    def test_config_source_enum(self):
        """Test ConfigSource enum values."""
        assert ConfigSource.FILE.value == "file"
        assert ConfigSource.ENVIRONMENT.value == "environment"
        assert ConfigSource.DEFAULT.value == "default"

