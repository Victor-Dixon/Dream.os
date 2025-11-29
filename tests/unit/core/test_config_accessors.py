"""
Unit tests for src/core/config/config_accessors.py
"""

import pytest
from unittest.mock import Mock, patch

from src.core.config.config_accessors import (
    get_config,
    get_unified_config,
    get_timeout_config,
    get_agent_config,
    get_browser_config,
    get_threshold_config,
    get_file_pattern_config,
    get_test_config,
    get_report_config,
    validate_config,
    reload_config,
)


class TestConfigAccessors:
    """Test configuration accessor functions."""

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_config(self, mock_manager):
        """Test get_config function."""
        mock_manager.get.return_value = "test_value"
        result = get_config("test_key", "default")
        assert result == "test_value"
        mock_manager.get.assert_called_once_with("test_key", "default")

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_config_with_default(self, mock_manager):
        """Test get_config with default value."""
        mock_manager.get.return_value = "default_value"
        result = get_config("missing_key", "default_value")
        assert result == "default_value"
        mock_manager.get.assert_called_once_with("missing_key", "default_value")

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_unified_config(self, mock_manager):
        """Test get_unified_config function."""
        result = get_unified_config()
        assert result == mock_manager

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_timeout_config(self, mock_manager):
        """Test get_timeout_config function."""
        mock_timeout = Mock()
        mock_manager.get_timeout_config.return_value = mock_timeout
        result = get_timeout_config()
        assert result == mock_timeout
        mock_manager.get_timeout_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_agent_config(self, mock_manager):
        """Test get_agent_config function."""
        mock_agent = Mock()
        mock_manager.get_agent_config.return_value = mock_agent
        result = get_agent_config()
        assert result == mock_agent
        mock_manager.get_agent_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_browser_config(self, mock_manager):
        """Test get_browser_config function."""
        mock_browser = Mock()
        mock_manager.get_browser_config.return_value = mock_browser
        result = get_browser_config()
        assert result == mock_browser
        mock_manager.get_browser_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_threshold_config(self, mock_manager):
        """Test get_threshold_config function."""
        mock_threshold = Mock()
        mock_manager.get_threshold_config.return_value = mock_threshold
        result = get_threshold_config()
        assert result == mock_threshold
        mock_manager.get_threshold_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_file_pattern_config(self, mock_manager):
        """Test get_file_pattern_config function."""
        mock_pattern = Mock()
        mock_manager.get_file_pattern_config.return_value = mock_pattern
        result = get_file_pattern_config()
        assert result == mock_pattern
        mock_manager.get_file_pattern_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_test_config(self, mock_manager):
        """Test get_test_config function."""
        mock_test = Mock()
        mock_manager.get_test_config.return_value = mock_test
        result = get_test_config()
        assert result == mock_test
        mock_manager.get_test_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_get_report_config(self, mock_manager):
        """Test get_report_config function."""
        mock_report = Mock()
        mock_manager.get_report_config.return_value = mock_report
        result = get_report_config()
        assert result == mock_report
        mock_manager.get_report_config.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_validate_config(self, mock_manager):
        """Test validate_config function."""
        mock_manager.validate.return_value = []
        result = validate_config()
        assert result == []
        mock_manager.validate.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_validate_config_with_errors(self, mock_manager):
        """Test validate_config with validation errors."""
        errors = ["Error 1", "Error 2"]
        mock_manager.validate.return_value = errors
        result = validate_config()
        assert result == errors
        mock_manager.validate.assert_called_once()

    @patch('src.core.config.config_accessors._config_manager')
    def test_reload_config(self, mock_manager):
        """Test reload_config function."""
        reload_config()
        mock_manager.reload.assert_called_once()



