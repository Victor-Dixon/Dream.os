"""
@file
@summary Legacy-compatible Thea browser operations interface.
@registry docs/recovery/recovery_registry.yaml#thea-browser-operations
"""

from __future__ import annotations

from typing import Any


class TheaBrowserOperations:
    """High-level browser operations used by legacy tests and call-sites."""

    def __init__(self, driver=None, thea_config=None, browser_utils=None):
        self.driver = driver
        self.thea_config = thea_config
        self.browser_utils = browser_utils

    def _safe_driver_call(self, fn, default=None):
        if self.driver is None:
            return default
        try:
            result = fn()
            return default if result is None and default is not None else result
        except Exception:
            return default

    def navigate_to(self, url: str, wait_seconds: float = 0.0) -> bool:
        if self.driver is None:
            return False
        self.driver.get(url)
        if wait_seconds > 0:
            self._wait_for_page_ready(timeout=wait_seconds)
        return True

    def refresh(self):
        return self._safe_driver_call(lambda: self.driver.refresh(), True)

    def back(self):
        return self._safe_driver_call(lambda: self.driver.back(), True)

    def forward(self):
        return self._safe_driver_call(lambda: self.driver.forward(), True)

    def get_current_url(self) -> str:
        return self._safe_driver_call(lambda: self.driver.current_url, "")

    def get_title(self) -> str:
        return self._safe_driver_call(lambda: self.driver.title, "")

    def find_element(self, by: str, value: str, timeout: float = 10.0):
        if self.driver is None:
            return None
        from selenium.webdriver.support.ui import WebDriverWait

        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(by, value)
        )

    def find_elements(self, by: str, value: str):
        return self._safe_driver_call(lambda: self.driver.find_elements(by, value), [])

    def execute_script(self, script: str, *args):
        return self._safe_driver_call(lambda: self.driver.execute_script(script, *args))

    def take_screenshot(self, path: str) -> bool:
        return bool(self._safe_driver_call(lambda: self.driver.save_screenshot(path), False))

    def get_page_source(self) -> str:
        return self._safe_driver_call(lambda: self.driver.page_source, "")

    def _wait_for_page_ready(self, timeout: float = 10.0) -> bool:
        if self.driver is None:
            return False
        from selenium.webdriver.support.ui import WebDriverWait

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") in ("complete", "interactive")
            )
            return True
        except Exception:
            return False

    def _is_thea_authenticated(self) -> bool:
        current_url = self.get_current_url().lower()
        return "login" not in current_url and "auth" not in current_url

    def _set_textarea_value(self, textarea: Any, prompt: str) -> bool:
        if self.driver is None:
            return False
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
            textarea,
            prompt,
        )
        return True

    def _get_latest_assistant_message_text(self) -> str:
        result = self.execute_script(
            "return (document.querySelector('[data-message-author-role=assistant]:last-of-type') || {}).innerText || '';"
        )
        return result or ""


__all__ = ["TheaBrowserOperations"]
