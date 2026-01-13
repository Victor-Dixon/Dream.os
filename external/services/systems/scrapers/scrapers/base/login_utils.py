"""
Shared Login Utilities
=====================

Centralized login utilities to eliminate duplications across scraper files.
All scrapers should use these utilities instead of implementing their own login logic.
"""

import time
import logging
from typing import Optional
from ..cookie_manager import CookieManager
from ..login_handler import LoginHandler

logger = logging.getLogger(__name__)

def ensure_login_unified(
    driver,
    cookie_manager: CookieManager,
    login_handler: LoginHandler,
    allow_manual: bool = True,
    manual_timeout: int = 180,
    cookie_file: Optional[str] = None
) -> bool:
    """
    Unified login method for all scrapers.
    
    This method consolidates all login logic and should be used by all scraper classes
    instead of implementing their own login methods.
    
    Args:
        driver: Selenium webdriver instance
        cookie_manager: CookieManager instance
        login_handler: LoginHandler instance
        allow_manual: Allow manual login if automated methods fail
        manual_timeout: Timeout for manual login in seconds
        cookie_file: Optional custom cookie file path
        
    Returns:
        True if logged in, False otherwise
    """
    if not driver:
        logger.error("No driver provided for login")
        return False
    
    logger.info("🔐 Starting unified login process...")
    
    # Check if already logged in
    if login_handler.is_logged_in(driver):
        logger.info("✅ Already logged in")
        return True
    
    # Try loading cookies first
    if cookie_manager.cookie_file_exists(cookie_file):
        logger.info("🔄 Trying saved cookies...")
        cookie_manager.load_cookies(driver, cookie_file)
        time.sleep(3)
        
        if login_handler.is_logged_in(driver):
            logger.info("✅ Login successful with saved cookies!")
            return True
        else:
            logger.info("❌ Saved cookies didn't work")
    
    # Fall back to manual login if allowed
    if allow_manual:
        logger.info("⚠️ Manual login required")
        logger.info("=" * 40)
        logger.info("Please log in manually in the browser window.")
        logger.info("Once logged in and you can see your conversations, the system will detect it.")
        logger.info("=" * 40)
        
        # Wait for manual login
        start_time = time.time()
        
        while time.time() - start_time < manual_timeout:
            if login_handler.is_logged_in(driver):
                logger.info("✅ Manual login successful!")
                # Save fresh cookies
                logger.info("🍪 Saving fresh cookies...")
                cookie_manager.save_cookies(driver, cookie_file)
                logger.info("✅ Fresh cookies saved!")
                return True
            time.sleep(2)
            remaining = int(manual_timeout - (time.time() - start_time))
            logger.info(f"⏰ Waiting for login... {remaining}s remaining")
        
        logger.error("❌ Manual login timeout")
    
    return False

def create_login_components(cookie_file: Optional[str] = None):
    """
    Create standardized login components.
    
    Args:
        cookie_file: Optional custom cookie file path
        
    Returns:
        Tuple of (cookie_manager, login_handler)
    """
    cookie_manager = CookieManager(cookie_file)
    login_handler = LoginHandler()
    return cookie_manager, login_handler 