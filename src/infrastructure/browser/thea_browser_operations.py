#!/usr/bin/env python3
"""
Thea Browser Operations
=======================

Browser operations for Thea Manager automation:
- Navigation operations
- Authentication operations
- Prompt/response operations
- General browser operations

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - V2 Refactoring
Date: 2025-12-14
License: MIT
"""

import logging
import time
from typing import Any

from .thea_browser_utils import TheaBrowserUtils

logger = logging.getLogger(__name__)


class TheaBrowserOperations:
    """Browser operations for Thea Manager automation."""

    def __init__(
        self,
        driver: Any,
        thea_config: Any,
        browser_utils: TheaBrowserUtils | None = None,
        find_textarea_func: Any = None,
        find_send_button_func: Any = None,
    ):
        """Initialize browser operations."""
        self.driver = driver
        self.thea_config = thea_config
        self.browser_utils = browser_utils or TheaBrowserUtils(thea_config)
        self._find_textarea = find_textarea_func
        self._find_send_button = find_send_button_func

    # ========== Navigation Operations ==========

    def navigate_to(self, url: str, wait_seconds: float = 2.0) -> bool:
        """Navigate to URL with optional wait."""
        if not self.driver:
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

    def refresh(self) -> bool:
        """Refresh current page."""
        result = self._safe_driver_call(lambda: self.driver.refresh(), False)
        return result is not False

    def back(self) -> bool:
        """Navigate back."""
        result = self._safe_driver_call(lambda: self.driver.back(), False)
        return result is not False

    def forward(self) -> bool:
        """Navigate forward."""
        result = self._safe_driver_call(lambda: self.driver.forward(), False)
        return result is not False

    def get_current_url(self) -> str | None:
        """Get current URL."""
        return self._safe_driver_call(lambda: self.driver.current_url, None)

    def get_title(self) -> str | None:
        """Get page title."""
        return self._safe_driver_call(lambda: self.driver.title, None)

    def _safe_driver_call(self, func, default):
        """Safely call driver method with error handling."""
        if not self.driver:
            return default
        try:
            return func()
        except Exception:
            return default

    # ========== Authentication Operations ==========

    def ensure_thea_authenticated(self, thea_url: str | None = None, allow_manual: bool = True) -> bool:
        """Ensure authenticated to Thea Manager."""
        if not self.driver:
            return False

        try:
            target_url = thea_url or self.thea_config.conversation_url


            if not self.navigate_to(target_url, wait_seconds=5.0):
                return False

            time.sleep(3)  # Wait for page stabilization


            self._wait_for_page_ready()

            if self._is_thea_authenticated():
                logger.info("✅ Already authenticated to Thea (via cookies)")
                self.browser_utils.save_cookies(self.driver)
                return True



            if allow_manual:
                logger.info("⚠️  Manual authentication required - waiting 45 seconds...")
                time.sleep(45)
                if self._is_thea_authenticated():
                    logger.info("✅ Authentication successful")
                    self.browser_utils.save_cookies(self.driver)
                    return True

            logger.error("❌ Authentication failed")
            return False
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False

    def _wait_for_page_ready(self, timeout: float = 10.0) -> bool:
        """Wait for page to be ready by checking for common elements."""
        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            ready_selectors = ["textarea", "div[contenteditable='true']", "[data-testid]",
                              ".composer", "form", "[role='textbox']", "button", "input"]
            for selector in ready_selectors:
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(("css selector", selector))
                    )
                    return True
                except:
                    continue
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True

        except Exception as e:
            logger.debug(f"Page ready wait failed: {e}")
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

    # ========== Prompt & Response Operations ==========

    def send_prompt_and_get_response_text(
        self, prompt: str, timeout: float = 90.0, poll_interval: float = 2.0
    ) -> str | None:
        """Send a prompt and return the assistant reply text (headless-safe)."""
        if not self.driver:
            logger.error("Browser not initialized")
            return None

        self.navigate_to(self.thea_config.conversation_url, wait_seconds=5.0)
        if not self._wait_for_page_ready(timeout=15.0):
            logger.error("Page failed to load properly")
            return None

        time.sleep(3)  # Wait for dynamic content
        textarea = self._find_textarea() if self._find_textarea else None
        if not textarea or not self._set_textarea_value(textarea, prompt):
            logger.error("Could not find or set textarea for prompt input")
            return None

        send_btn = self._find_send_button() if self._find_send_button else None
        try:
            if send_btn:
                send_btn.click()
            else:
                from selenium.webdriver.common.keys import Keys
                tag_name = textarea.tag_name.lower()
                if tag_name == 'div':
                    textarea.send_keys(Keys.CONTROL, Keys.ENTER)
                    time.sleep(0.5)
                    textarea.send_keys(Keys.ENTER)
                else:
                    textarea.send_keys(Keys.ENTER)

                # Backup: try clicking submit elements
                try:
                    submit_elements = self.driver.find_elements("css selector",
                        "button[type='submit'], input[type='submit'], [role='button']")
                    for elem in submit_elements:
                        if elem.is_displayed() and elem.is_enabled():
                            elem.click()
                            break
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Failed to submit prompt: {e}")
            return None

        # Wait for response
        start = time.time()
        baseline = self._get_latest_assistant_message_text()
        while time.time() - start < timeout:
            time.sleep(poll_interval)
            latest = self._get_latest_assistant_message_text()
            if latest and latest != baseline:
                logger.info("✅ Received assistant response")
                return latest.strip()

        logger.error("❌ Timed out waiting for assistant response")
        return None

    def _set_textarea_value(self, textarea: Any, prompt: str) -> bool:
        """Inject prompt text via JS to avoid flaky send_keys."""
        try:
            self.driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
                textarea,
                prompt,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set prompt value: {e}")
            return False

    def _get_latest_assistant_message_text(self) -> str | None:
        """Return latest assistant message text."""
        try:
            script = """
                const nodes = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
                if (!nodes.length) return null;
                const last = nodes[nodes.length - 1];
                return last.innerText || last.textContent || null;
            """
            return self.driver.execute_script(script)
        except Exception:
            return None

    # ========== General Browser Operations ==========

    def execute_script(self, script: str) -> Any:
        """Execute JavaScript in browser."""
        return self._safe_driver_call(lambda: self.driver.execute_script(script), None)

    def find_element(self, by: str, value: str, timeout: float = 10.0) -> Any | None:
        """Find element with timeout."""
        if not self.driver:
            return None
        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception:
            return None

    def find_elements(self, by: str, value: str) -> list:
        """Find multiple elements."""
        return self._safe_driver_call(lambda: self.driver.find_elements(by, value), [])

    def take_screenshot(self, filepath: str) -> bool:
        """Take screenshot and save to file."""
        if not self._safe_driver_call(lambda: self.driver.save_screenshot(filepath), False):
            return False
        logger.info(f"✅ Screenshot saved to {filepath}")
        return True

    def get_page_source(self) -> str | None:
        """Get current page HTML source."""
        return self._safe_driver_call(lambda: self.driver.page_source, None)


__all__ = ["TheaBrowserOperations"]

