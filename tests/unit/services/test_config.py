"""
Tests for config.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services import config


class TestConfig:
    """Test config module constants."""

    def test_default_mode_exists(self):
        """Test DEFAULT_MODE constant exists."""
        assert hasattr(config, 'DEFAULT_MODE')
        assert isinstance(config.DEFAULT_MODE, str)

    def test_default_coordinate_mode_exists(self):
        """Test DEFAULT_COORDINATE_MODE constant exists."""
        assert hasattr(config, 'DEFAULT_COORDINATE_MODE')
        assert isinstance(config.DEFAULT_COORDINATE_MODE, str)

    def test_agent_count_exists(self):
        """Test AGENT_COUNT constant exists."""
        assert hasattr(config, 'AGENT_COUNT')
        assert isinstance(config.AGENT_COUNT, int)

    def test_captain_id_exists(self):
        """Test CAPTAIN_ID constant exists."""
        assert hasattr(config, 'CAPTAIN_ID')
        assert isinstance(config.CAPTAIN_ID, str)

    def test_config_uses_ssot_pattern(self):
        """Test that config module uses SSOT pattern (get_config imported)."""
        import src.services.config as config_module
        
        # Verify get_config is imported (SSOT pattern)
        assert hasattr(config_module, 'get_config') or 'get_config' in str(config_module.__dict__)

    def test_agent_count_is_integer(self):
        """Test AGENT_COUNT is an integer value."""
        assert isinstance(config.AGENT_COUNT, int)
        assert config.AGENT_COUNT > 0

    def test_default_mode_is_string(self):
        """Test DEFAULT_MODE is a string value."""
        assert isinstance(config.DEFAULT_MODE, str)
        assert len(config.DEFAULT_MODE) > 0

    def test_default_coordinate_mode_is_string(self):
        """Test DEFAULT_COORDINATE_MODE is a string value."""
        assert isinstance(config.DEFAULT_COORDINATE_MODE, str)
        assert len(config.DEFAULT_COORDINATE_MODE) > 0

    def test_captain_id_is_string(self):
        """Test CAPTAIN_ID is a string value."""
        assert isinstance(config.CAPTAIN_ID, str)
        assert len(config.CAPTAIN_ID) > 0

