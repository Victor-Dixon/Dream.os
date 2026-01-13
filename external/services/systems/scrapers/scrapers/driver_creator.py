"""
Driver Creator for Browser Management
Handles creation of undetected and regular Chrome drivers.
"""

import os
import logging
from typing import Optional

try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

# Attempt to use webdriver_manager for automatic driver install in regular Selenium mode
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

from .driver_config import DriverConfig
from .process_manager import ProcessManager

logger = logging.getLogger(__name__)

class DriverCreator:
    """Handles creation of Chrome drivers."""
    
    @staticmethod
    def create_undetected_driver(options, temp_dir: str, version_main: Optional[int] = None):
        """
        Create undetected-chromedriver instance with robust error handling.
        
        Args:
            options: Chrome options
            temp_dir: Temporary directory for Chrome data
            version_main: Chrome major version to use
            
        Returns:
            Undetected Chrome driver instance or None if failed
        """
        logger.info("Using undetected-chromedriver")
        
        # Set temp directory to avoid disk space issues
        os.environ['TEMP'] = temp_dir
        os.environ['TMP'] = temp_dir
        
        # Kill any existing Chrome processes to avoid conflicts
        ProcessManager.kill_existing_chrome_processes()
        
        driver = None
        try:
            # Install or reuse the driver for the chosen version.
            if version_main:
                # undetected-chromedriver handles version management internally.
                # We just need to pass the version_main parameter.
                logger.info("Creating uc.Chrome with version_main=%s", version_main)
                chrome_kwargs = {
                    "options": options,
                    "version_main": version_main,
                    "patcher_force_close": True,
                    "use_subprocess": True,  # Use subprocess to avoid disk space issues
                    "driver_executable_path": None,  # Let it auto-download
                    "browser_executable_path": None,  # Let it auto-detect
                }

                driver = uc.Chrome(**chrome_kwargs)
            else:
                logger.info("Creating uc.Chrome instance (auto version)")
                driver = uc.Chrome(options=options, use_subprocess=True)

            logger.info("Successfully created uc.Chrome instance")
            return driver
        except Exception as e:
            logger.error(f"Failed to create uc.Chrome: {e}")
            return None
    
    @staticmethod
    def create_regular_driver(options, temp_dir: str):
        """
        Create regular Selenium Chrome driver with fallback options.
        
        Args:
            options: Chrome options
            temp_dir: Temporary directory for Chrome data
            
        Returns:
            Regular Chrome driver instance or None if failed
        """
        logger.info("Using regular Selenium Chrome driver")
        
        # Set temp directory
        os.environ['TEMP'] = temp_dir
        os.environ['TMP'] = temp_dir
        
        # Kill any existing Chrome processes
        ProcessManager.kill_existing_chrome_processes()
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                # Use webdriver_manager for automatic driver installation
                logger.info("Using webdriver_manager for automatic driver installation")
                service = ChromeService(ChromeDriverManager().install())
                from selenium import webdriver
                driver = webdriver.Chrome(service=service, options=options)
            else:
                # Try to use system-installed ChromeDriver
                logger.info("Using system-installed ChromeDriver")
                from selenium import webdriver
                driver = webdriver.Chrome(options=options)
            
            logger.info("Successfully created regular Chrome driver")
            return driver
        except Exception as e:
            logger.error(f"Failed to create regular Chrome driver: {e}")
            
            # Try fallback without webdriver_manager
            if WEBDRIVER_MANAGER_AVAILABLE:
                try:
                    logger.info("Trying fallback without webdriver_manager")
                    from selenium import webdriver
                    driver = webdriver.Chrome(options=options)
                    logger.info("Successfully created Chrome driver with fallback")
                    return driver
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
            
            return None 