"""
Tests for Thea Browser Operations - Infrastructure Domain

Unit tests for TheaBrowserOperations module.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-14
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import Any

from src.infrastructure.browser.thea_browser_operations import TheaBrowserOperations
from src.infrastructure.browser.thea_browser_utils import TheaBrowserUtils


class TestTheaBrowserOperations:
    """Tests for TheaBrowserOperations."""

    @pytest.fixture
    def mock_driver(self):
        """Create mock Selenium driver."""
        driver = MagicMock()
        driver.current_url = "https://chat.openai.com"
        driver.title = "ChatGPT"
        driver.page_source = "<html><body>Test</body></html>"
        return driver

    @pytest.fixture
    def mock_thea_config(self):
        """Create mock TheaConfig."""
        config = MagicMock()
        config.conversation_url = "https://chat.openai.com"
        config.cookie_file = "/tmp/cookies.json"
        config.cache_dir = "/tmp"
        return config

    @pytest.fixture
    def operations(self, mock_driver, mock_thea_config):
        """Create TheaBrowserOperations instance."""
        return TheaBrowserOperations(
            driver=mock_driver,
            thea_config=mock_thea_config,
            browser_utils=TheaBrowserUtils(mock_thea_config)
        )

    def test_initialization(self, operations, mock_driver, mock_thea_config):
        """Test TheaBrowserOperations initializes correctly."""
        assert operations.driver == mock_driver
        assert operations.thea_config == mock_thea_config
        assert operations.browser_utils is not None

    def test_navigate_to_success(self, operations, mock_driver):
        """Test successful navigation."""
        result = operations.navigate_to("https://example.com", wait_seconds=0.1)
        assert result is True
        mock_driver.get.assert_called_once_with("https://example.com")

    def test_navigate_to_no_driver(self, mock_thea_config):
        """Test navigation fails without driver."""
        operations = TheaBrowserOperations(
            driver=None,
            thea_config=mock_thea_config
        )
        result = operations.navigate_to("https://example.com")
        assert result is False

    def test_refresh(self, operations, mock_driver):
        """Test page refresh."""
        # _safe_driver_call returns the result of the lambda, or False if exception
        # Since refresh() returns None, we need to check it doesn't raise
        result = operations.refresh()
        # refresh() should return True if successful (not False from _safe_driver_call)
        assert result is not False
        mock_driver.refresh.assert_called_once()

    def test_back(self, operations, mock_driver):
        """Test back navigation."""
        result = operations.back()
        # back() should return True if successful (not False from _safe_driver_call)
        assert result is not False
        mock_driver.back.assert_called_once()

    def test_forward(self, operations, mock_driver):
        """Test forward navigation."""
        result = operations.forward()
        # forward() should return True if successful (not False from _safe_driver_call)
        assert result is not False
        mock_driver.forward.assert_called_once()

    def test_get_current_url(self, operations, mock_driver):
        """Test get current URL."""
        url = operations.get_current_url()
        assert url == "https://chat.openai.com"

    def test_get_title(self, operations, mock_driver):
        """Test get page title."""
        title = operations.get_title()
        assert title == "ChatGPT"

    def test_find_element_success(self, operations, mock_driver):
        """Test find element with timeout."""
        mock_element = MagicMock()
        with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = mock_element
            result = operations.find_element("css selector", "#test", timeout=5.0)
            assert result == mock_element

    def test_find_element_no_driver(self, mock_thea_config):
        """Test find element fails without driver."""
        operations = TheaBrowserOperations(
            driver=None,
            thea_config=mock_thea_config
        )
        result = operations.find_element("css selector", "#test")
        assert result is None

    def test_find_elements(self, operations, mock_driver):
        """Test find multiple elements."""
        mock_elements = [MagicMock(), MagicMock()]
        mock_driver.find_elements.return_value = mock_elements
        result = operations.find_elements("css selector", ".test")
        assert result == mock_elements

    def test_execute_script(self, operations, mock_driver):
        """Test execute JavaScript."""
        mock_driver.execute_script.return_value = "result"
        result = operations.execute_script("return 'test'")
        assert result == "result"
        mock_driver.execute_script.assert_called_once_with("return 'test'")

    def test_take_screenshot_success(self, operations, mock_driver):
        """Test take screenshot."""
        mock_driver.save_screenshot.return_value = True
        result = operations.take_screenshot("/tmp/test.png")
        assert result is True
        mock_driver.save_screenshot.assert_called_once_with("/tmp/test.png")

    def test_get_page_source(self, operations, mock_driver):
        """Test get page source."""
        result = operations.get_page_source()
        assert result == "<html><body>Test</body></html>"

    def test_wait_for_page_ready(self, operations, mock_driver):
        """Test wait for page ready."""
        with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = True
            result = operations._wait_for_page_ready(timeout=5.0)
            assert result is True

    def test_is_thea_authenticated_true(self, operations, mock_driver):
        """Test authentication check returns True."""
        mock_driver.current_url = "https://chat.openai.com"
        result = operations._is_thea_authenticated()
        assert result is True

    def test_is_thea_authenticated_false(self, operations, mock_driver):
        """Test authentication check returns False."""
        mock_driver.current_url = "https://chat.openai.com/auth/login"
        result = operations._is_thea_authenticated()
        assert result is False

    def test_set_textarea_value(self, operations, mock_driver):
        """Test set textarea value via JavaScript."""
        mock_textarea = MagicMock()
        result = operations._set_textarea_value(mock_textarea, "test prompt")
        assert result is True
        mock_driver.execute_script.assert_called_once()

    def test_get_latest_assistant_message_text(self, operations, mock_driver):
        """Test get latest assistant message text."""
        mock_driver.execute_script.return_value = "Assistant response"
        result = operations._get_latest_assistant_message_text()
        assert result == "Assistant response"

    def test_safe_driver_call_success(self, operations, mock_driver):
        """Test safe driver call with success."""
        result = operations._safe_driver_call(lambda: "success", "default")
        assert result == "success"

    def test_safe_driver_call_no_driver(self, mock_thea_config):
        """Test safe driver call without driver."""
        operations = TheaBrowserOperations(
            driver=None,
            thea_config=mock_thea_config
        )
        result = operations._safe_driver_call(lambda: "success", "default")
        assert result == "default"

    def test_safe_driver_call_exception(self, operations, mock_driver):
        """Test safe driver call with exception."""
        mock_driver.refresh.side_effect = Exception("Error")
        result = operations._safe_driver_call(lambda: mock_driver.refresh(), False)
        assert result is False

