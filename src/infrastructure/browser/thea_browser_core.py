#!/usr/bin/env python3
"""
Thea Browser Core
=================

Core browser initialization and lifecycle management:
- Browser driver setup and configuration
- Chrome options configuration
- Context manager support
- Cleanup and teardown

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - V2 Refactoring
Date: 2025-12-14
License: MIT
"""

import logging
import os
from typing import Any

try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False

from .browser_models import BrowserConfig, TheaConfig

logger = logging.getLogger(__name__)


class TheaBrowserCore:
    """Core browser initialization and lifecycle management."""

    def __init__(self, config: BrowserConfig | None = None, thea_config: TheaConfig | None = None):
        """Initialize browser core."""
        self.config = config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()
        self.driver: Any | None = None
        self.profile: dict[str, Any] | None = None
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
            options = self._create_chrome_options(profile_name, user_data_dir)
            self.driver = uc.Chrome(options=options, headless=self.config.headless)
            self._configure_driver_timeouts()
            self._initialized = True
            logger.info("✅ Browser initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Browser initialization failed: {e}")
            return False

    def _create_chrome_options(self, profile_name: str | None, user_data_dir: str | None) -> Any:
        """Create and configure Chrome options."""
        options = uc.ChromeOptions()

        if self.config.headless:
            options.add_argument("--headless=new")

        if user_data_dir or (self.profile and self.profile.get("user_data_dir")):
            data_dir = user_data_dir or self.profile.get("user_data_dir")
            options.add_argument(f"--user-data-dir={data_dir}")

        if profile_name or (self.profile and self.profile.get("profile_name")):
            prof_name = profile_name or self.profile.get("profile_name")
            options.add_argument(f"--profile-directory={prof_name}")

        # Anti-detection options
        options.add_argument("--disable-blink-features=AutomationControlled")
        w, h = self.config.window_size
        options.add_argument(f"--window-size={w}x{h}")

        return options

    def _configure_driver_timeouts(self) -> None:
        """Configure driver timeouts."""
        if not self.driver:
            return

        self.driver.implicitly_wait(self.config.implicit_wait)
        try:
            self.driver.set_page_load_timeout(self.config.page_load_timeout)
        except Exception:
            pass

    def close(self) -> None:
        """Close browser and cleanup resources."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None
                self._initialized = False

    def is_initialized(self) -> bool:
        """Check if browser is initialized."""
        return self._initialized and self.driver is not None

    def get_driver(self) -> Any | None:
        """Get browser driver instance."""
        return self.driver if self.is_initialized() else None

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def create_thea_browser_core(
    config: BrowserConfig | None = None,
    thea_config: TheaConfig | None = None
) -> TheaBrowserCore:
    """Create Thea browser core instance."""
    return TheaBrowserCore(config, thea_config)


__all__ = ["TheaBrowserCore", "create_thea_browser_core"]


