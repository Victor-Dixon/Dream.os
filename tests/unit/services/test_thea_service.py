"""
Tests for thea_service.py - TheaService class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.services.thea.thea_service import TheaService, SELENIUM_AVAILABLE, PYAUTOGUI_AVAILABLE


class TestTheaService:
    """Test TheaService class."""

    def test_init_defaults(self):
        """Test TheaService initialization with defaults."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            assert service.cookie_file.name == "thea_cookies.json"
            assert service.headless is False
            assert service.thea_url.startswith("https://chatgpt.com/g/")
            assert service.responses_dir.name == "thea_responses"

    def test_init_custom(self):
        """Test TheaService initialization with custom values."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService(cookie_file="custom_cookies.json", headless=True)
            assert service.cookie_file.name == "custom_cookies.json"
            assert service.headless is True

    def test_init_no_selenium(self):
        """Test initialization when Selenium not available."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", False):
            with pytest.raises(ImportError):
                TheaService()

    def test_start_browser_undetected_success(self):
        """Test successful browser start with undetected-chromedriver."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            with patch("src.services.thea.thea_service.UNDETECTED_AVAILABLE", True):
                with patch("undetected_chromedriver.Chrome") as mock_chrome:
                    mock_driver = Mock()
                    mock_chrome.return_value = mock_driver

                    service = TheaService()
                    result = service.start_browser()

                    assert result is True
                    assert service.driver == mock_driver

    def test_start_browser_standard_fallback(self):
        """Test browser start falls back to standard Chrome."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            with patch("src.services.thea.thea_service.UNDETECTED_AVAILABLE", False):
                with patch("selenium.webdriver.Chrome") as mock_chrome:
                    mock_driver = Mock()
                    mock_chrome.return_value = mock_driver

                    service = TheaService()
                    result = service.start_browser()

                    assert result is True
                    assert service.driver == mock_driver

    def test_start_browser_undetected_failure(self):
        """Test browser start when undetected-chromedriver fails."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            with patch("src.services.thea.thea_service.UNDETECTED_AVAILABLE", True):
                with patch("undetected_chromedriver.Chrome", side_effect=Exception("Error")):
                    with patch("selenium.webdriver.Chrome") as mock_chrome:
                        mock_driver = Mock()
                        mock_chrome.return_value = mock_driver

                        service = TheaService()
                        result = service.start_browser()

                        assert result is True  # Falls back to standard Chrome

    def test_start_browser_exception(self):
        """Test browser start with exception."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            with patch("src.services.thea.thea_service.UNDETECTED_AVAILABLE", False):
                with patch("selenium.webdriver.Chrome", side_effect=Exception("Error")):
                    service = TheaService()
                    result = service.start_browser()

                    assert result is False

    def test_are_cookies_fresh_with_manager(self):
        """Test cookie freshness check with cookie manager."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            # Test with cookie manager available - mock the manager after service creation
            service = TheaService()
            # Manually set cookie_manager to simulate it being available
            mock_manager = Mock()
            mock_manager.has_valid_cookies = Mock(return_value=True)
            service.cookie_manager = mock_manager

            result = service.are_cookies_fresh()

            assert result is True
            mock_manager.has_valid_cookies.assert_called_once()

    def test_are_cookies_fresh_no_manager(self):
        """Test cookie freshness check without cookie manager."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            with patch("src.services.thea.thea_service.COOKIE_MANAGER_AVAILABLE", False):
                service = TheaService()
                service.cookie_file = Path("nonexistent.json")

                result = service.are_cookies_fresh()

                assert result is False

    def test_are_cookies_fresh_file_exists(self):
        """Test cookie freshness when file exists."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            with patch("src.services.thea.thea_service.COOKIE_MANAGER_AVAILABLE", False):
                service = TheaService()
                with patch("pathlib.Path.exists", return_value=True):
                    result = service.are_cookies_fresh()

                    assert result is True

    def test_validate_cookies_success(self):
        """Test successful cookie validation."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            mock_driver = Mock()
            service.driver = mock_driver
            service._is_logged_in = Mock(return_value=True)
            service.cookie_manager = Mock()
            service.cookie_manager.load_cookies = Mock()

            with patch("time.sleep"):
                result = service.validate_cookies()

                assert result is True

    def test_validate_cookies_not_logged_in(self):
        """Test cookie validation when not logged in."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            mock_driver = Mock()
            service.driver = mock_driver
            service._is_logged_in = Mock(return_value=False)
            service.cookie_manager = Mock()
            service.cookie_manager.load_cookies = Mock()

            with patch("time.sleep"):
                result = service.validate_cookies()

                assert result is False

    def test_validate_cookies_no_driver(self):
        """Test cookie validation when driver not started."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            service.driver = None
            service.start_browser = Mock(return_value=False)

            result = service.validate_cookies()

            assert result is False

    def test_validate_cookies_exception(self):
        """Test cookie validation with exception."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            mock_driver = Mock()
            service.driver = mock_driver
            mock_driver.get = Mock(side_effect=Exception("Error"))

            result = service.validate_cookies()

            assert result is False

    def test_refresh_cookies_already_logged_in(self):
        """Test cookie refresh when already logged in."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            mock_driver = Mock()
            service.driver = mock_driver
            service._is_logged_in = Mock(return_value=True)
            service.cookie_manager = Mock()
            service.cookie_manager.save_cookies = Mock()

            with patch("time.sleep"):
                result = service.refresh_cookies()

                assert result is True
                service.cookie_manager.save_cookies.assert_called_once()

    def test_refresh_cookies_exception(self):
        """Test cookie refresh with exception."""
        with patch("src.services.thea.thea_service.SELENIUM_AVAILABLE", True):
            service = TheaService()
            service.start_browser = Mock(return_value=False)

            result = service.refresh_cookies()

            assert result is False

