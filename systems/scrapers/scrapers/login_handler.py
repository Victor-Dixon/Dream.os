"""
Login Handler for ChatGPT Scraper
Handles authentication, login, and session management operations.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import time
import logging
from typing import Optional

# Import modular components
from .credential_login import CredentialLogin
from .login_status import LoginStatusChecker

logger = logging.getLogger(__name__)

class LoginHandler:
    """Handles ChatGPT login and authentication operations."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, 
                 totp_secret: Optional[str] = None, timeout: int = 30):
        """
        Initialize the login handler.
        
        Args:
            username: ChatGPT username/email
            password: ChatGPT password
            totp_secret: TOTP secret for 2FA
            timeout: Timeout for web operations
        """
        # Initialize modular components
        self.credential_login = CredentialLogin(username, password, totp_secret, timeout)
        self.login_status_checker = LoginStatusChecker(timeout)
    
    def login_with_credentials(self, driver) -> bool:
        """
        Attempt to login with stored credentials.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if login successful, False otherwise
        """
        return self.credential_login.login_with_credentials(driver)
    
    def is_logged_in(self, driver) -> bool:
        """
        Check if user is logged in to ChatGPT.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if logged in, False otherwise
        """
        return self.login_status_checker.is_logged_in(driver)
    
    def ensure_login_modern(self, driver, allow_manual: bool = True, manual_timeout: int = 30) -> bool:
        """
        Ensure user is logged in, with fallback to manual login.
        
        Args:
            driver: Selenium webdriver instance
            allow_manual: Allow manual login if automated fails
            manual_timeout: Timeout for manual login
            
        Returns:
            True if logged in, False otherwise
        """
        if not driver:
            logger.error("No driver provided")
            return False
        
        # Check if already logged in
        if self.is_logged_in(driver):
            logger.info("Already logged in")
            return True
        
        # Try automated login
        if self.credential_login.username and self.credential_login.password:
            if self.login_with_credentials(driver):
                logger.info("Automated login successful")
                return True
            else:
                logger.warning("Automated login failed")
        
        # Manual login fallback
        if allow_manual:
            logger.info(f"Please log in manually within {manual_timeout} seconds...")
            start_time = time.time()
            
            while time.time() - start_time < manual_timeout:
                if self.is_logged_in(driver):
                    logger.info("Manual login detected")
                    return True
                time.sleep(1)
            
            logger.error("Manual login timeout")
        
        return False
    
    def ensure_login_with_cookies(self, driver, cookie_manager, allow_manual: bool = True, manual_timeout: int = 30) -> bool:
        """
        Ensure user is logged in with proper cookie management.
        
        Args:
            driver: Selenium webdriver instance
            cookie_manager: CookieManager instance for saving cookies
            allow_manual: Allow manual login if automated fails
            manual_timeout: Timeout for manual login
            
        Returns:
            True if logged in, False otherwise
        """
        if not driver:
            logger.error("No driver provided")
            return False
        
        # Navigate to ChatGPT landing page FIRST
        target_url = os.getenv("CHATGPT_BASE_URL", "https://chat.openai.com")
        try:
            logger.info("[Nav] Opening %s …", target_url)
            driver.get(target_url)
            logger.debug("[Nav] Current URL after get(): %s", driver.current_url)
        except Exception as nav_err:
            logger.error("[Nav] Failed to navigate to %s – %s", target_url, nav_err)

        # 1️⃣  Inject cookies if we have any
        if cookie_manager.cookie_file_exists():
            logger.info("[Cookies] Loading saved cookies from %s", cookie_manager.cookie_file)
            cookie_manager.load_cookies(driver)
            logger.debug("[Cookies] %s injected; refreshing page…", driver.current_url)
            driver.refresh()
            
            # Check if cookies worked
            if self.is_logged_in(driver):
                logger.info("✅ Login successful with cookies")
                return True
            else:
                logger.info("[Cookies] Cookies loaded but login failed - will try other methods")

        # 2️⃣  Automated login attempt
        if self.credential_login.username and self.credential_login.password:
            logger.info("[Login] Attempting automated credential login…")
            if self.login_with_credentials(driver):
                logger.info("Automated login successful")
                # Save cookies after successful automated login
                cookie_manager.save_cookies(driver)
                logger.info("Cookies saved after automated login")
                return True
            else:
                logger.warning("Automated login failed – will %smanual fallback", "" if allow_manual else "NOT ")

        if allow_manual:
            logger.info("[Manual] Awaiting user login – window is now interactive")
            logger.info("          Timeout: %d seconds", manual_timeout)

            start_time = time.time()
            last_ping = 0

            while time.time() - start_time < manual_timeout:
                elapsed = int(time.time() - start_time)
                if elapsed - last_ping >= 5:
                    logger.info("[Manual] %d s elapsed – still waiting…", elapsed)
                    last_ping = elapsed

                if self.is_logged_in(driver):
                    logger.info("✅ Manual login detected – saving cookies…")
                    cookie_manager.save_cookies(driver)
                    logger.info("✅ Cookies saved after manual login")
                    return True

                time.sleep(1)

            logger.error("❌ Manual login timeout after %d s", manual_timeout)

        return False 