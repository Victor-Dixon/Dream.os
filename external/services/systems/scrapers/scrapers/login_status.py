"""
Login Status Checker
Handles checking if user is logged in to ChatGPT.
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class LoginStatusChecker:
    """Handles checking login status for ChatGPT."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the login status checker.
        
        Args:
            timeout: Timeout for web operations
        """
        self.timeout = timeout
    
    def is_logged_in(self, driver) -> bool:
        """
        Check if user is logged in to ChatGPT.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if logged in, False otherwise
        """
        if not driver:
            logger.error("No driver provided for login check")
            return False
        
        try:
            # Check multiple indicators of successful login
            indicators = [
                self._check_url_indicator,
                self._check_ui_elements,
                self._check_user_menu,
                self._check_conversation_list
            ]
            
            for indicator in indicators:
                if indicator(driver):
                    logger.info("✅ Login status confirmed")
                    return True
            
            logger.info("❌ Not logged in")
            return False
            
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False
    
    def _check_url_indicator(self, driver) -> bool:
        """Check if URL indicates successful login."""
        try:
            current_url = driver.current_url
            
            # If we're on the main chat page, we're logged in
            if "chat.openai.com" in current_url and "login" not in current_url.lower():
                logger.debug("URL indicates logged in state")
                return True
            
            return False
        except Exception as e:
            logger.debug(f"Error checking URL indicator: {e}")
            return False
    
    def _check_ui_elements(self, driver) -> bool:
        """Check for UI elements that indicate logged in state."""
        try:
            wait = WebDriverWait(driver, 5)  # Shorter timeout for UI checks
            
            # Look for elements that indicate logged in state
            logged_in_selectors = [
                "//div[contains(text(), 'New chat')]",
                "//div[contains(text(), 'Chat')]",
                "//div[contains(@class, 'conversation')]",
                "//div[@data-testid='chat']",
                "//div[contains(@class, 'sidebar')]",
                "//div[contains(@class, 'conversation-list')]",
                "//button[contains(text(), 'New chat')]",
                "//button[contains(text(), 'Chat')]",
            ]
            
            for selector in logged_in_selectors:
                try:
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        logger.debug(f"Found logged in indicator: {selector}")
                        return True
                except TimeoutException:
                    continue
            
            return False
        except Exception as e:
            logger.debug(f"Error checking UI elements: {e}")
            return False
    
    def _check_user_menu(self, driver) -> bool:
        """Check for user menu or profile elements."""
        try:
            wait = WebDriverWait(driver, 5)
            
            # Look for user menu/profile elements
            user_selectors = [
                "//div[contains(@class, 'user')]",
                "//div[contains(@class, 'profile')]",
                "//button[contains(@class, 'user')]",
                "//button[contains(@class, 'profile')]",
                "//div[@data-testid='user-menu']",
                "//div[contains(@aria-label, 'user')]",
                "//div[contains(@aria-label, 'profile')]",
            ]
            
            for selector in user_selectors:
                try:
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        logger.debug(f"Found user menu indicator: {selector}")
                        return True
                except TimeoutException:
                    continue
            
            return False
        except Exception as e:
            logger.debug(f"Error checking user menu: {e}")
            return False
    
    def _check_conversation_list(self, driver) -> bool:
        """Check for conversation list elements."""
        try:
            wait = WebDriverWait(driver, 5)
            
            # Look for conversation list elements
            conversation_selectors = [
                "//div[contains(@class, 'conversation')]",
                "//div[contains(@class, 'chat')]",
                "//div[@data-testid='conversation']",
                "//div[@data-testid='chat']",
                "//div[contains(@class, 'sidebar')]//div[contains(@class, 'item')]",
            ]
            
            for selector in conversation_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if len(elements) > 0:
                        logger.debug(f"Found conversation list indicator: {selector}")
                        return True
                except:
                    continue
            
            return False
        except Exception as e:
            logger.debug(f"Error checking conversation list: {e}")
            return False 