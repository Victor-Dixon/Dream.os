"""
Base Scraper Class
=================

Unified base class for all scrapers to eliminate code duplication.
Provides common functionality for login, browser management, and error handling.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from ..browser_manager import BrowserManager
from ..cookie_manager import CookieManager
from ..login_handler import LoginHandler
from .login_utils import ensure_login_unified, create_login_components

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """
    Base class for all scrapers providing common functionality.
    
    This class consolidates common patterns from:
    - smart_scraper_with_fallback.py
    - final_working_scraper.py
    - improved_conversation_scraper.py
    - chatgpt_scraper.py
    """
    
    def __init__(
        self,
        headless: bool = False,
        cookie_file: Optional[str] = None,
        manual_timeout: int = 180,
        allow_manual_login: bool = True
    ):
        """
        Initialize the base scraper.
        
        Args:
            headless: Run browser in headless mode
            cookie_file: Path to cookie file for session persistence
            manual_timeout: Timeout for manual login in seconds
            allow_manual_login: Allow manual login if automated fails
        """
        self.headless = headless
        self.cookie_file = cookie_file
        self.manual_timeout = manual_timeout
        self.allow_manual_login = allow_manual_login
        
        # Initialize components
        self.browser_manager = BrowserManager()
        self.cookie_manager, self.login_handler = create_login_components(cookie_file)
        
        # Browser state
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
    def setup_browser(self) -> bool:
        """
        Set up the browser with proper configuration.
        
        Returns:
            True if setup successful, False otherwise
        """
        try:
            logger.info("🌐 Setting up browser...")
            self.driver = self.browser_manager.create_driver(headless=self.headless)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("✅ Browser setup complete")
            return True
        except Exception as e:
            logger.error(f"❌ Browser setup failed: {e}")
            return False
    
    def login(self) -> bool:
        """
        Perform login using unified login method.
        
        Returns:
            True if login successful, False otherwise
        """
        if not self.driver:
            logger.error("❌ No driver available for login")
            return False
            
        return ensure_login_unified(
            driver=self.driver,
            cookie_manager=self.cookie_manager,
            login_handler=self.login_handler,
            allow_manual=self.allow_manual_login,
            manual_timeout=self.manual_timeout,
            cookie_file=self.cookie_file
        )
    
    def navigate_to_url(self, url: str, timeout: int = 30) -> bool:
        """
        Navigate to a URL with error handling.
        
        Args:
            url: URL to navigate to
            timeout: Navigation timeout in seconds
            
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            logger.info(f"🌐 Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            logger.info("✅ Navigation successful")
            return True
            
        except TimeoutException:
            logger.error(f"❌ Navigation timeout: {url}")
            return False
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False
    
    def wait_for_element(
        self,
        by: By,
        value: str,
        timeout: int = 10,
        condition: str = "presence"
    ) -> Optional[Any]:
        """
        Wait for an element with specified condition.
        
        Args:
            by: Selenium locator strategy
            value: Locator value
            timeout: Wait timeout in seconds
            condition: Wait condition ('presence', 'clickable', 'visible')
            
        Returns:
            WebElement if found, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            if condition == "presence":
                return wait.until(EC.presence_of_element_located((by, value)))
            elif condition == "clickable":
                return wait.until(EC.element_to_be_clickable((by, value)))
            elif condition == "visible":
                return wait.until(EC.visibility_of_element_located((by, value)))
            else:
                logger.warning(f"Unknown condition: {condition}, using presence")
                return wait.until(EC.presence_of_element_located((by, value)))
                
        except TimeoutException:
            logger.warning(f"⏰ Element not found: {by}={value} (timeout: {timeout}s)")
            return None
        except Exception as e:
            logger.error(f"❌ Error waiting for element: {e}")
            return None
    
    def safe_click(self, element, timeout: int = 5) -> bool:
        """
        Safely click an element with retry logic.
        
        Args:
            element: WebElement to click
            timeout: Click timeout in seconds
            
        Returns:
            True if click successful, False otherwise
        """
        try:
            # Wait for element to be clickable
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(element))
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Click
            element.click()
            return True
            
        except Exception as e:
            logger.error(f"❌ Click failed: {e}")
            return False
    
    def safe_send_keys(self, element, text: str, clear_first: bool = True) -> bool:
        """
        Safely send keys to an element.
        
        Args:
            element: WebElement to send keys to
            text: Text to send
            clear_first: Clear the field before typing
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if clear_first:
                element.clear()
            
            element.send_keys(text)
            return True
            
        except Exception as e:
            logger.error(f"❌ Send keys failed: {e}")
            return False
    
    def get_page_source(self) -> Optional[str]:
        """
        Get current page source safely.
        
        Returns:
            Page source if available, None otherwise
        """
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"❌ Failed to get page source: {e}")
            return None
    
    def execute_script(self, script: str, *args) -> Optional[Any]:
        """
        Execute JavaScript safely.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Script result if successful, None otherwise
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"❌ JavaScript execution failed: {e}")
            return None
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot safely.
        
        Args:
            filename: Screenshot filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"📸 Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"❌ Screenshot failed: {e}")
            return False
    
    def cleanup(self):
        """
        Clean up resources.
        """
        try:
            if self.driver:
                logger.info("🧹 Cleaning up browser...")
                self.driver.quit()
                self.driver = None
                self.wait = None
                logger.info("✅ Cleanup complete")
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        if not self.setup_browser():
            raise RuntimeError("Failed to setup browser")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
    
    @abstractmethod
    def scrape(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Main scraping method to be implemented by subclasses.
        
        Returns:
            Dictionary containing scraped data
        """
        pass
    
    @abstractmethod
    def validate_scrape_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate scraping result.
        
        Args:
            result: Scraped data to validate
            
        Returns:
            True if result is valid, False otherwise
        """
        pass 