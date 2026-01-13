"""
Thea Browser Utilities
======================

Utility functions for Thea browser service: cookie management, selector caching.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - V2 Refactoring
License: MIT
"""

<<<<<<< HEAD
=======
import json
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class TheaBrowserUtils:
    """Utility functions for Thea browser operations."""

    def __init__(self, thea_config: Any):
        """Initialize utilities with Thea configuration."""
        self.thea_config = thea_config
<<<<<<< HEAD
        self._secure_cookie_manager = None

    def _get_secure_cookie_manager(self):
        """Get or create secure cookie manager instance."""
        if self._secure_cookie_manager is None:
            try:
                from src.services.thea_secure_cookie_manager import SecureCookieManager
                self._secure_cookie_manager = SecureCookieManager(
                    cookie_file=getattr(self.thea_config, 'encrypted_cookie_file', 'thea_cookies.enc'),
                    key_file=getattr(self.thea_config, 'key_file', 'thea_key.bin')
                )
            except ImportError as e:
                logger.warning(f"Secure cookie manager not available, falling back to plain JSON: {e}")
                self._secure_cookie_manager = None
        return self._secure_cookie_manager

    def load_cookies(self, driver: Any, base_url: str) -> None:
        """Load cookies from secure storage into browser driver."""
        secure_manager = self._get_secure_cookie_manager()

        if secure_manager:
            # Use secure encrypted cookie manager
            try:
                # Navigate to domain first to set cookie context
                driver.get(base_url)
                import time
                time.sleep(2)  # Allow page to load

                if secure_manager.load_cookies(driver):
                    logger.info("✅ Cookies loaded securely")
                else:
                    logger.debug("No secure cookies available")
            except Exception as e:
                logger.warning(f"Secure cookie loading failed: {e}")
        else:
            # Fallback to plain JSON (legacy)
            self._load_cookies_legacy(driver, base_url)

    def save_cookies(self, driver: Any) -> None:
        """Save cookies from browser driver to secure storage."""
        secure_manager = self._get_secure_cookie_manager()

        if secure_manager:
            # Use secure encrypted cookie manager
            if secure_manager.save_cookies(driver):
                logger.info("✅ Cookies saved securely")
            else:
                logger.debug("Cookie save failed")
        else:
            # Fallback to plain JSON (legacy)
            self._save_cookies_legacy(driver)

    def _load_cookies_legacy(self, driver: Any, base_url: str) -> None:
        """Legacy cookie loading using plain JSON."""
        try:
            import json
            import time
            from pathlib import Path

            cookie_path = Path(getattr(self.thea_config, 'cookie_file', 'cookies.json'))
            if not cookie_path.exists():
                logger.debug("No legacy cookie file found")
                return

            with open(cookie_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)

            if not cookies:
                logger.debug("Legacy cookie file is empty")
                return

            # Navigate to domain first to set cookie context
            driver.get(base_url)
            time.sleep(2)  # Allow page to load

            # Add cookies to browser session
            cookies_added = 0
            for cookie in cookies:
                try:
                    # Create a clean cookie dict for Selenium
                    cookie_dict = {
                        'name': cookie.get('name', ''),
                        'value': cookie.get('value', ''),
                        'path': cookie.get('path', '/'),
                        'secure': cookie.get('secure', False),
                    }

                    # Add optional fields if present
                    if 'expiry' in cookie:
                        cookie_dict['expiry'] = cookie['expiry']

                    driver.add_cookie(cookie_dict)
                    cookies_added += 1
                except Exception as e:
                    logger.debug(f"Failed to add cookie {cookie.get('name', 'unknown')}: {e}")
                    continue

            logger.info(f"✅ Loaded {cookies_added} cookies from legacy storage")

        except Exception as e:
            logger.warning(f"Legacy cookie loading failed: {e}")

    def _save_cookies_legacy(self, driver: Any) -> None:
        """Legacy cookie saving using plain JSON."""
        try:
            import json
            from pathlib import Path

            cookies = driver.get_cookies()
            if not cookies:
                logger.debug("No cookies to save")
                return

            cookie_path = Path(getattr(self.thea_config, 'cookie_file', 'cookies.json'))
            cookie_path.parent.mkdir(parents=True, exist_ok=True)

            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)

            logger.info("✅ Cookies saved to legacy storage")
        except Exception as e:
            logger.debug(f"Legacy cookie save failed: {e}")
=======

    def cookie_file(self) -> Path:
        """Get cookie file path."""
        return Path(self.thea_config.cookie_file)

    def load_cookies(self, driver: Any, base_url: str) -> None:
        """Load cookies from file into browser driver."""
        try:
            cookie_path = self.cookie_file()
            if not cookie_path.exists():
                return
            with open(cookie_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            driver.get(base_url)
            for cookie in cookies:
                # Selenium/uc requires domain stripped when adding after navigation
                cookie.pop("domain", None)
                try:
                    driver.add_cookie(cookie)
                except Exception:
                    continue
            logger.info("✅ Cookies loaded")
        except Exception as e:
            logger.debug(f"Cookie load skipped: {e}")

    def save_cookies(self, driver: Any) -> None:
        """Save cookies from browser driver to file."""
        try:
            cookies = driver.get_cookies()
            cookie_path = self.cookie_file()
            cookie_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)
            logger.info("✅ Cookies saved")
        except Exception as e:
            logger.debug(f"Cookie save skipped: {e}")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

    def get_selector_cache_file(self) -> Path:
        """Get selector success cache file path."""
        return Path(self.thea_config.cache_dir) / "selector_success.json"

    def load_selector_cache(self) -> dict[str, Any]:
        """Load selector success cache from file."""
        try:
            cache_file = self.get_selector_cache_file()
            if cache_file.exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.debug(f"Selector cache load failed: {e}")
        return {}

    def save_selector_cache(self, cache_data: dict[str, Any]) -> None:
        """Save selector success cache to file."""
        try:
            cache_file = self.get_selector_cache_file()
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            logger.debug(f"Selector cache save failed: {e}")

    def record_successful_selector(self, selector: str) -> None:
        """Record successful selector usage in cache (matches original implementation)."""
        try:
            from datetime import datetime

            cache_file = self.get_selector_cache_file()
            cache_file.parent.mkdir(parents=True, exist_ok=True)

            success_data = self.load_selector_cache()

            # Update success metrics (match original format)
            if selector not in success_data:
                success_data[selector] = {"attempts": 0, "successes": 0}

            success_data[selector]["attempts"] = success_data[selector].get("attempts", 0) + 1
            success_data[selector]["successes"] = success_data[selector].get("successes", 0) + 1
            success_data[selector]["success_rate"] = (
                success_data[selector]["successes"] / success_data[selector]["attempts"]
            )
            success_data[selector]["last_success"] = datetime.now().isoformat()

            self.save_selector_cache(success_data)

        except Exception as e:
            logger.debug(f"Could not record selector success: {e}")


__all__ = ["TheaBrowserUtils"]

