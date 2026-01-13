#!/usr/bin/env python3
"""
Browser Manager Utility - V2 Compliance
=======================================

Utility class for managing browser operations in Thea service.

V2 Compliance: <400 lines, modular design
Author: Agent-7 (Modularization)
<!-- SSOT Domain: integration -->
"""

from typing import Optional
import time

# Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Undetected ChromeDriver (preferred for anti-bot bypass)
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False


class BrowserManager:
    """Manages browser operations for Thea service."""

    def __init__(self, headless: bool = False):
        """Initialize browser manager."""
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None

    def start_browser(self) -> bool:
        """Start the browser with appropriate configuration."""
        try:
            if not SELENIUM_AVAILABLE:
                print("❌ Selenium not available")
                return False

            options = Options()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # Try undetected chromedriver first (better anti-bot)
            if UNDETECTED_AVAILABLE:
                try:
                    self.driver = uc.Chrome(options=options)
                    print("✅ Browser started with undetected chromedriver")
                    return True
                except Exception as e:
                    print(f"⚠️ Undetected chromedriver failed: {e}")

            # Fallback to regular selenium
            if SELENIUM_AVAILABLE:
                self.driver = webdriver.Chrome(options=options)
                print("✅ Browser started with selenium chromedriver")
                return True

            print("❌ No compatible chromedriver available")
            return False

        except Exception as e:
            print(f"❌ Browser start failed: {e}")
            return False

    def get_driver(self) -> Optional[webdriver.Chrome]:
        """Get the browser driver instance."""
        return self.driver

    def is_running(self) -> bool:
        """Check if browser is running."""
        return self.driver is not None

    def navigate_to(self, url: str) -> bool:
        """Navigate to a URL."""
        try:
            if self.driver:
                self.driver.get(url)
                time.sleep(2)  # Allow page to load
                return True
            return False
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False

    def close(self):
        """Close the browser."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass  # Ignore errors during cleanup
            self.driver = None