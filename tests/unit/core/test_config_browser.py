"""
Unit tests for src/core/config_browser.py
"""

import pytest
from unittest.mock import patch

from src.core.config_browser import BrowserConfig


class TestBrowserConfig:
    """Test BrowserConfig dataclass."""

    @patch('src.core.config_browser.get_config')
    def test_browser_config_creation(self, mock_get_config):
        """Test that BrowserConfig can be created."""
        mock_get_config.side_effect = lambda key, default: default
        config = BrowserConfig()
        assert config is not None
        assert config.gpt_url is not None
        assert config.conversation_url is not None

    @patch('src.core.config_browser.get_config')
    def test_browser_config_urls(self, mock_get_config):
        """Test browser config URL fields."""
        mock_get_config.side_effect = lambda key, default: default
        config = BrowserConfig()
        assert "chatgpt.com" in config.gpt_url
        assert "chatgpt.com" in config.conversation_url

    @patch('src.core.config_browser.get_config')
    def test_browser_config_selectors(self, mock_get_config):
        """Test browser config selector fields."""
        mock_get_config.side_effect = lambda key, default: default
        config = BrowserConfig()
        assert config.input_selector is not None
        assert config.send_button_selector is not None
        assert config.response_selector is not None
        assert config.thinking_indicator is not None

    @patch('src.core.config_browser.get_config')
    def test_browser_config_fallback_selectors(self, mock_get_config):
        """Test browser config fallback selector lists."""
        mock_get_config.side_effect = lambda key, default: default
        config = BrowserConfig()
        assert isinstance(config.input_fallback_selectors, list)
        assert len(config.input_fallback_selectors) > 0
        assert isinstance(config.send_fallback_selectors, list)
        assert len(config.send_fallback_selectors) > 0
        assert isinstance(config.response_fallback_selectors, list)
        assert len(config.response_fallback_selectors) > 0

    @patch('src.core.config_browser.get_config')
    def test_browser_config_max_retries(self, mock_get_config):
        """Test browser config max scrape retries."""
        mock_get_config.side_effect = lambda key, default: default
        config = BrowserConfig()
        assert isinstance(config.max_scrape_retries, int)
        assert config.max_scrape_retries >= 0

