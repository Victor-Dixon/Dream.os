"""
Browser Manager for ChatGPT Scraper
Handles browser setup, configuration, and management operations.
"""

import sys
import os
import logging
from typing import Optional
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    # Load .env file from project root
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        logging.info(f"Loaded environment variables from {env_file}")
    else:
        # Try to load .env from current directory
        load_dotenv()
        logging.info("Loaded environment variables from dreamscape.scrapers.env file")
except ImportError:
    logging.info("python-dotenv not available - using system environment variables only")

# Import modular components
from .system_utils import SystemUtils
from .driver_config import DriverConfig
from .driver_creator import DriverCreator

# Configure logging
logger = logging.getLogger(__name__)

class BrowserManager:
    """Manages browser setup and configuration for ChatGPT scraping."""
    
    def __init__(self, headless: bool = False, use_undetected: bool = True, driver_version_main: int | None = None):
        """
        Initialize the browser manager.
        
        Args:
            headless: Run browser in headless mode
            use_undetected: Use undetected-chromedriver if available
            driver_version_main: Explicit Chrome *major* version to pin the driver to
        """
        self.headless = SystemUtils.get_env_bool('CHATGPT_HEADLESS', headless)
        # Respect explicit request even in non-headless mode so users can bypass login detection.
        self.use_undetected = (
            SystemUtils.get_env_bool('CHATGPT_USE_UNDETECTED', use_undetected) and DriverConfig.UNDETECTED_AVAILABLE
        )
        # Resolve driver version pinning (None = auto)
        env_version = os.getenv("CHROME_DRIVER_VERSION_MAIN") or os.getenv("UCDRIVER_VERSION_MAIN")
        try:
            env_version_int: int | None = int(env_version) if env_version and env_version.isdigit() else None
        except Exception:
            env_version_int = None

        self.driver_version_main: int | None = driver_version_main if driver_version_main is not None else env_version_int

        if self.driver_version_main:
            logger.info("🔒 Hard-pinning Chrome driver major version to %s", self.driver_version_main)

        self.driver = None
        
        if self.use_undetected:
            logger.info("Using undetected-chromedriver for enhanced anti-detection")
        else:
            logger.info("Using regular selenium webdriver")
    

    
    def create_driver(self):
        """Create and configure the web driver."""
        if not DriverConfig.UNDETECTED_AVAILABLE and not self.use_undetected:
            logger.warning("Cannot create driver - Selenium not available")
            return None
            
        try:
            logger.info(f"Creating driver with use_undetected={self.use_undetected}, headless={self.headless}")
            
            # Check disk space before attempting to create driver
            if not SystemUtils.check_disk_space():
                logger.warning("Insufficient disk space - forcing regular selenium mode")
                self.use_undetected = False
            
            # Get temp directory and Chrome version
            temp_dir = SystemUtils.get_temp_dir_with_space()
            chrome_version = DriverConfig.get_chrome_version(self.driver_version_main)
            
            # Create Chrome options
            options = DriverConfig.create_chrome_options(self.headless, temp_dir)
            
            if self.use_undetected:
                driver = DriverCreator.create_undetected_driver(options, temp_dir, chrome_version)
                if driver:
                    self.driver = driver  # ensure close_driver() can quit instance
                    return driver
                # If undetected failed, fall back automatically
                logger.warning("Undetected-chromedriver failed – falling back to regular Selenium driver")
            
            # Create regular driver and persist reference
            driver = DriverCreator.create_regular_driver(options, temp_dir)
            self.driver = driver  # may be None if creation failed
            return driver
                
        except Exception as e:
            logger.error(f"Failed to create driver: {e}")
            return None
    

    

    

    
    def close_driver(self):
        """Close the web driver."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
            finally:
                self.driver = None

 