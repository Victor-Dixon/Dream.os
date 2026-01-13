"""
Tests for Browser Models - Infrastructure Domain

Tests for browser configuration models.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.browser.browser_models import BrowserConfig, TheaConfig


class TestBrowserConfig:
    """Tests for BrowserConfig."""

    @patch('src.infrastructure.browser.browser_models._unified_config', None)
    def test_browser_config_defaults(self):
        """Test BrowserConfig with default values (no unified config)."""
        config = BrowserConfig()
        assert config.headless is False
        assert config.window_size == (1920, 1080)
        assert config.timeout == 30.0
        assert config.implicit_wait == 10.0
        assert config.page_load_timeout == 120.0

    @patch('src.infrastructure.browser.browser_models._unified_config', None)
    def test_browser_config_custom_values(self):
        """Test BrowserConfig with custom values (no unified config)."""
        config = BrowserConfig(
            headless=True,
            window_size=(1280, 720),
            timeout=60.0,
        )
        assert config.headless is True
        assert config.window_size == (1280, 720)
        assert config.timeout == 60.0


class TestTheaConfig:
    """Tests for TheaConfig."""

    def test_thea_config_defaults(self):
        """Test TheaConfig with default values."""
        config = TheaConfig()
        assert config.auto_save_cookies is True
        assert isinstance(config.cookie_file, str)

    def test_thea_config_custom_values(self):
        """Test TheaConfig with custom values."""
        config = TheaConfig(
            auto_save_cookies=False,
            cookie_file="custom_cookies.json",
        )
        assert config.auto_save_cookies is False
        assert config.cookie_file == "custom_cookies.json"

