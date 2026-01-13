"""
Driver Configuration for Browser Management
Handles Chrome options configuration and driver setup.
"""

import os
import logging
from typing import Optional

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.chrome.options import Options
    UNDETECTED_AVAILABLE = True
except ImportError:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        UNDETECTED_AVAILABLE = False
        print("Warning: undetected-chromedriver not available. Using regular selenium.")
    except ImportError:
        UNDETECTED_AVAILABLE = False
        print("Warning: Selenium not available. Browser functionality will be limited.")

# Attempt to use webdriver_manager for automatic driver install in regular Selenium mode
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

logger = logging.getLogger(__name__)

# Hard-pinned Chrome driver version for deterministic builds
PINNED_CHROME_MAJOR: int = 137

class DriverConfig:
    """Handles Chrome driver configuration and options setup."""
    
    # Add class attribute for compatibility
    UNDETECTED_AVAILABLE = UNDETECTED_AVAILABLE
    
    @staticmethod
    def create_chrome_options(headless: bool = False, temp_dir: str = None) -> Options:
        """
        Create Chrome options with standard configuration.
        
        Args:
            headless: Whether to run in headless mode
            temp_dir: Temporary directory for Chrome data
            
        Returns:
            Configured Chrome options
        """
        if UNDETECTED_AVAILABLE:
            options = uc.ChromeOptions()
        else:
            options = Options()
        
        logger.info("Created Chrome options")
        
        # Fix compatibility issue: Add headless property if it doesn't exist
        if not hasattr(options, 'headless'):
            logger.info("Adding headless property for compatibility")
            options.headless = False  # Default to False, will be set by argument
        
        if headless:
            logger.info("Setting headless mode")
            try:
                options.add_argument("--headless=new")
                logger.info("Added --headless=new argument")
                options.headless = True  # Set property for undetected-chromedriver
            except Exception as e:
                logger.error(f"Failed to add --headless=new: {e}")
        
        logger.info("Adding standard Chrome options...")
        try:
            # Essential stability options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # Speed up loading
            options.add_argument("--disable-javascript")  # For basic scraping
            options.add_argument("--window-size=1920,1080")
            
            # Fix DevToolsActivePort issues
            options.add_argument("--remote-debugging-port=0")  # Use random port
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            
            # Memory and performance optimizations
            options.add_argument("--memory-pressure-off")
            options.add_argument("--max_old_space_size=4096")
            
            # Add temp directory to avoid disk space issues
            if temp_dir:
                options.add_argument(f"--user-data-dir={temp_dir}/chrome_user_data")
                options.add_argument(f"--disk-cache-dir={temp_dir}/chrome_cache")
                options.add_argument(f"--crash-dumps-dir={temp_dir}/chrome_crashes")
            
            logger.info("Added standard Chrome arguments")
        except Exception as e:
            logger.error(f"Failed to add standard arguments: {e}")
        
        # Additional undetected options
        if UNDETECTED_AVAILABLE:
            logger.info("Adding undetected-specific options...")
            try:
                options.add_argument("--disable-blink-features=AutomationControlled")
                # Remove problematic options that cause Chrome compatibility issues
                # options.add_experimental_option("excludeSwitches", ["enable-automation"])
                # options.add_experimental_option('useAutomationExtension', False)
                logger.info("Added undetected-specific options")
            except Exception as e:
                logger.error(f"Failed to add undetected options: {e}")
        
        return options
    
    @staticmethod
    def detect_local_chrome_major() -> Optional[int]:
        """
        Detect the major version of locally installed Chrome.
        
        Returns:
            Chrome major version number or None if not detected
        """
        try:
            if os.name == 'nt':  # Windows
                import winreg
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                      r"Software\Google\Chrome\BLBeacon") as key:
                        version = winreg.QueryValueEx(key, "version")[0]
                        major_version = int(version.split('.')[0])
                        logger.info(f"Detected Chrome version: {major_version}")
                        return major_version
                except (FileNotFoundError, OSError):
                    pass
                
                # Try alternative registry location
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                      r"SOFTWARE\Google\Chrome\BLBeacon") as key:
                        version = winreg.QueryValueEx(key, "version")[0]
                        major_version = int(version.split('.')[0])
                        logger.info(f"Detected Chrome version: {major_version}")
                        return major_version
                except (FileNotFoundError, OSError):
                    pass
            else:  # Unix-like
                import subprocess
                try:
                    result = subprocess.run(['google-chrome', '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        major_version = int(version.split()[2].split('.')[0])
                        logger.info(f"Detected Chrome version: {major_version}")
                        return major_version
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, 
                       FileNotFoundError, ValueError, IndexError):
                    pass
        except Exception as e:
            logger.warning(f"Could not detect Chrome version: {e}")
        
        return None
    
    @staticmethod
    def get_chrome_version(driver_version_main: Optional[int] = None) -> int:
        """
        Determine the Chrome major version to use.
        
        Args:
            driver_version_main: Explicit Chrome major version to pin
            
        Returns:
            Chrome major version number
        """
        # Determine desired Chrome major version in priority order:
        # 1) Explicit constructor arg / CHROME_DRIVER_VERSION_MAIN env.
        # 2) Legacy UCDRIVER_VERSION_MAIN env var (kept for backward-compat).
        # 3) Detect local Chrome installation version.
        # 4) Hard-pinned fallback PINNED_CHROME_MAJOR.
        version_main_env = os.getenv("UCDRIVER_VERSION_MAIN")

        chosen_version: Optional[int] = None
        if driver_version_main is not None:
            chosen_version = driver_version_main
        elif version_main_env and version_main_env.isdigit():
            chosen_version = int(version_main_env)
        else:
            detected = DriverConfig.detect_local_chrome_major()
            if detected:
                chosen_version = detected
            else:
                chosen_version = PINNED_CHROME_MAJOR

        if chosen_version:
            logger.info(f"Using Chrome major version: {chosen_version}")
        
        return chosen_version 