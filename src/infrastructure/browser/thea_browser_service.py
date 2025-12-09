#!/usr/bin/env python3
"""
Thea Browser Service - V2 Compliance
====================================

Unified browser service for Thea Manager automation.
Consolidates: browser_adapter, chrome_undetected, thea_login_handler, thea_manager_profile

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - Browser Consolidation
License: MIT
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any

try:
    import undetected_chromedriver as uc

    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False

from .browser_models import BrowserConfig, TheaConfig

logger = logging.getLogger(__name__)


class TheaBrowserService:
    """Unified browser service for Thea Manager automation."""

    def __init__(self, config: BrowserConfig | None = None, thea_config: TheaConfig | None = None):
        """Initialize browser service."""
        self.config = config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()
        self.driver = None
        self.profile = None
        self._initialized = False

    def initialize(self, profile_name: str | None = None, user_data_dir: str | None = None) -> bool:
        """Initialize browser with optional profile."""
        if os.getenv("DISABLE_BROWSER") == "1":
            logger.warning("Browser disabled via DISABLE_BROWSER=1")
            return False

        if not UC_AVAILABLE:
            logger.error("undetected_chromedriver not available - install with `pip install undetected-chromedriver`")
            return False

        try:
            self.profile = {"profile_name": profile_name, "user_data_dir": user_data_dir}

            # Setup Chrome options (undetected only)
            options = uc.ChromeOptions()

            if self.config.headless:
                options.add_argument("--headless=new")

            if user_data_dir or (self.profile and self.profile.get("user_data_dir")):
                data_dir = user_data_dir or self.profile.get("user_data_dir")
                options.add_argument(f"--user-data-dir={data_dir}")

            if profile_name or (self.profile and self.profile.get("profile_name")):
                prof_name = profile_name or self.profile.get("profile_name")
                options.add_argument(f"--profile-directory={prof_name}")

            # Anti-detection options (minimal for uc compatibility)
            options.add_argument("--disable-blink-features=AutomationControlled")
            w, h = self.config.window_size
            options.add_argument(f"--window-size={w}x{h}")

            # Initialize driver
            self.driver = uc.Chrome(options=options, headless=self.config.headless)

            self.driver.implicitly_wait(self.config.implicit_wait)
            try:
                self.driver.set_page_load_timeout(self.config.page_load_timeout)
            except Exception:
                pass
            self._initialized = True

            logger.info("✅ Browser initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Browser initialization failed: {e}")
            return False

    def navigate_to(self, url: str, wait_seconds: float = 2.0) -> bool:
        """Navigate to URL with optional wait."""
        if not self._initialized or not self.driver:
            logger.error("Browser not initialized")
            return False

        try:
            self.driver.get(url)
            time.sleep(wait_seconds)
            logger.info(f"✅ Navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False

    def ensure_thea_authenticated(self, thea_url: str | None = None, allow_manual: bool = True) -> bool:
        """Ensure authenticated to Thea Manager."""
        if not self._initialized:
            return False

        try:
            target_url = thea_url or self.thea_config.conversation_url
            # Navigate to Thea
            if not self.navigate_to(target_url):
                return False

            # Try loading cookies if available
            self._load_cookies(target_url)
            self.driver.refresh()
            time.sleep(2)

            # Check if already authenticated
            if self._is_thea_authenticated():
                logger.info("✅ Already authenticated to Thea (via cookies)")
                self._save_cookies()
                return True

            # Manual authentication if allowed
            if allow_manual:
                logger.info("⚠️  Manual authentication required")
                logger.info("Please log in to Thea Manager in the browser window...")
                time.sleep(30)  # Allow time for manual login

                if self._is_thea_authenticated():
                    logger.info("✅ Authentication successful")
                    self._save_cookies()
                    return True

            logger.error("❌ Authentication failed")
            return False

        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False

    def _is_thea_authenticated(self) -> bool:
        """Check if authenticated to Thea Manager."""
        try:
            # Check for authenticated page elements
            current_url = self.driver.current_url
            return (
                ("chat.openai.com" in current_url or "chatgpt.com" in current_url)
                and "auth" not in current_url
            )
        except:
            return False

    def execute_script(self, script: str) -> Any:
        """Execute JavaScript in browser."""
        if not self._initialized:
            return None
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            logger.error(f"Script execution error: {e}")
            return None

    def find_element(self, by: str, value: str, timeout: float = 10.0) -> Any | None:
        """Find element with timeout."""
        if not self._initialized:
            return None

        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception:
            logger.debug(f"Element not found: {by}={value}")
            return None

    def find_elements(self, by: str, value: str) -> list:
        """Find multiple elements."""
        if not self._initialized:
            return []
        try:
            return self.driver.find_elements(by, value)
        except Exception:
            logger.debug(f"Elements not found: {by}={value}")
            return []

    def take_screenshot(self, filepath: str) -> bool:
        """Take screenshot and save to file."""
        if not self._initialized:
            return False
        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"✅ Screenshot saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Screenshot failed: {e}")
            return False

    def get_page_source(self) -> str | None:
        """Get current page HTML source."""
        if not self._initialized:
            return None
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Error getting page source: {e}")
            return None

    def refresh(self) -> bool:
        """Refresh current page."""
        if not self._initialized:
            return False
        try:
            self.driver.refresh()
            return True
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            return False

    def back(self) -> bool:
        """Navigate back."""
        if not self._initialized:
            return False
        try:
            self.driver.back()
            return True
        except Exception as e:
            logger.error(f"Back navigation failed: {e}")
            return False

    def forward(self) -> bool:
        """Navigate forward."""
        if not self._initialized:
            return False
        try:
            self.driver.forward()
            return True
        except Exception as e:
            logger.error(f"Forward navigation failed: {e}")
            return False

    def get_current_url(self) -> str | None:
        """Get current URL."""
        if not self._initialized:
            return None
        try:
            return self.driver.current_url
        except:
            return None

    def get_title(self) -> str | None:
        """Get page title."""
        if not self._initialized:
            return None
        try:
            return self.driver.title
        except:
            return None

    def close(self) -> None:
        """Close browser."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None
                self._initialized = False

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # ========== Cookie helpers ==========
    def _cookie_file(self) -> Path:
        return Path(self.thea_config.cookie_file)

    def _load_cookies(self, base_url: str) -> None:
        try:
            cookie_path = self._cookie_file()
            if not cookie_path.exists():
                return
            with open(cookie_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            self.driver.get(base_url)
            for cookie in cookies:
                # Selenium/uc requires domain stripped when adding after navigation
                cookie.pop("domain", None)
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    continue
            logger.info("✅ Cookies loaded")
        except Exception as e:
            logger.debug(f"Cookie load skipped: {e}")

    def _save_cookies(self) -> None:
        try:
            cookies = self.driver.get_cookies()
            cookie_path = self._cookie_file()
            cookie_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)
            logger.info("✅ Cookies saved")
        except Exception as e:
            logger.debug(f"Cookie save skipped: {e}")


# Factory function
def create_thea_browser_service(config: BrowserConfig | None = None) -> TheaBrowserService:
    """Create Thea browser service instance."""
    return TheaBrowserService(config)


__all__ = ["TheaBrowserService", "create_thea_browser_service"]
