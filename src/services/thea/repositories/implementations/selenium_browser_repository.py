#!/usr/bin/env python3
"""
Selenium Browser Repository Implementation - Browser Automation
============================================================

<!-- SSOT Domain: thea -->

Repository implementation for Selenium-based browser automation.
Handles browser lifecycle, navigation, and element interactions.

V2 Compliance: Repository pattern implementation with abstracted browser operations.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

# Selenium imports with fallbacks
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import (
        NoSuchElementException,
        TimeoutException,
        WebDriverException
    )
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = None
    Options = None

# Undetected ChromeDriver
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False
    uc = None

from ...domain.models import BrowserContext
from ...domain.enums import BrowserState
from ..interfaces.i_browser_repository import IBrowserRepository


class SeleniumBrowserRepository(IBrowserRepository):
    """
    Selenium-based browser repository implementation.

    Uses undetected-chromedriver for anti-bot bypass.
    Provides abstracted browser operations through repository interface.
    """

    def __init__(self,
                 headless: bool = False,
                 use_undetected: bool = True,
                 page_load_timeout: int = 30):
        """
        Initialize Selenium browser repository.

        Args:
            headless: Whether to run browser in headless mode
            use_undetected: Whether to use undetected-chromedriver for anti-bot bypass
            page_load_timeout: Page load timeout in seconds
        """
        self.headless = headless
        self.use_undetected = use_undetected and UNDETECTED_AVAILABLE
        self.page_load_timeout = page_load_timeout
        self.driver = None
        self._context = BrowserContext()

        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium required: pip install selenium")

        if use_undetected and not UNDETECTED_AVAILABLE:
            print("⚠️ undetected-chromedriver not available, falling back to standard Chrome")
            self.use_undetected = False

    def start_browser(self) -> bool:
        """
        Start the browser instance.

        Returns:
            True if browser started successfully, False otherwise
        """
        try:
            self._context.update_state(BrowserState.STARTING)

            if self.use_undetected:
                # Use undetected-chromedriver for anti-bot bypass
                options = uc.ChromeOptions()
                if self.headless:
                    options.add_argument("--headless=new")

                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-plugins")
                options.add_argument("--disable-images")  # Speed up loading

                self.driver = uc.Chrome(
                    options=options,
                    use_subprocess=True,
                    driver_executable_path=None  # Auto-download correct version
                )
                print("✅ Undetected Chrome browser started for anti-bot bypass")

            else:
                # Use standard Chrome driver
                options = Options()
                if self.headless:
                    options.add_argument("--headless=new")

                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")

                # Anti-detection measures
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)

                self.driver = webdriver.Chrome(options=options)
                print("✅ Standard Chrome browser started")

            # Set timeouts
            self.driver.set_page_load_timeout(self.page_load_timeout)
            self.driver.implicitly_wait(10)

            self._context.update_state(BrowserState.READY)
            return True

        except Exception as e:
            error_msg = f"Browser start failed: {e}"
            self._context.update_state(BrowserState.ERROR, error_msg)
            print(f"❌ {error_msg}")
            return False

    def close_browser(self) -> bool:
        """
        Close the browser instance.

        Returns:
            True if browser closed successfully, False otherwise
        """
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                print("✅ Browser closed successfully")

            self._context.update_state(BrowserState.CLOSED)
            return True

        except Exception as e:
            print(f"❌ Browser close failed: {e}")
            return False

    def navigate_to_url(self, url: str) -> bool:
        """
        Navigate to the specified URL.

        Args:
            url: URL to navigate to

        Returns:
            True if navigation successful, False otherwise
        """
        try:
            if not self.is_browser_operational():
                return False

            self.driver.get(url)
            time.sleep(2)  # Allow page to stabilize

            self._context.current_url = self.get_current_url()
            self._context.page_title = self.get_page_title()
            self._context.is_page_ready = self.is_page_ready()

            print(f"✅ Navigated to: {url}")
            return True

        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False

    def get_current_url(self) -> Optional[str]:
        """Get the current URL."""
        try:
            return self.driver.current_url if self.driver else None
        except Exception:
            return None

    def get_page_title(self) -> Optional[str]:
        """Get the current page title."""
        try:
            return self.driver.title if self.driver else None
        except Exception:
            return None

    def is_page_ready(self, timeout: float = 15.0) -> bool:
        """
        Check if the page is fully loaded and ready for interaction.
        Uses comprehensive checks like the working monolithic version.
        """
        try:
            if not self.driver:
                return False

            # Wait for document ready
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    ready_state = self.driver.execute_script("return document.readyState")
                    if ready_state == "complete":
                        print("✅ Document ready state: complete")
                        break
                except Exception as e:
                    print(f"Document ready check failed: {e}")
                time.sleep(0.5)

            # Check for ChatGPT/Custom GPT specific elements (from working monolithic version)
            ready_selectors = [
                "textarea",  # Most common input element
                "[contenteditable='true']",  # Contenteditable divs
                "[role='textbox']",  # ARIA textbox role
                "div[data-message-author-role]",  # Message containers
                ".markdown",  # Content areas
                "[data-testid]",  # Any test IDs
                "button",  # Any buttons (usually present when loaded)
            ]

            print("🔍 Checking for page elements...")
            for selector in ready_selectors:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if element:
                        print(f"✅ Page ready - found element: {selector}")
                        return True
                except Exception as e:
                    print(f"Element {selector} not found: {e}")
                    continue

            # More permissive fallback: check if page has substantial content and no loading indicators
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                page_title = self.driver.title

                print(f"📄 Page title: {page_title}")
                print(f"📏 Body text length: {len(body_text)}")

                # Check for loading indicators
                loading_indicators = ["loading", "please wait", "connecting"]
                has_loading = any(indicator in body_text.lower() for indicator in loading_indicators)

                if len(body_text) > 50 and not has_loading and "chatgpt" in page_title.lower():
                    print("✅ Page appears ready (permissive fallback check)")
                    return True
                elif has_loading:
                    print("⏳ Page still loading...")
                    return False
            except Exception as e:
                print(f"Fallback check failed: {e}")

            print("⚠️ Page readiness check failed - no suitable elements found")
            return False

        except Exception as e:
            print(f"❌ Page ready check error: {e}")
            return False

    def find_input_element(self, selector: str) -> Optional[Any]:
        """
        Find an input element on the page.

        Args:
            selector: CSS selector for the input element

        Returns:
            Element object if found, None otherwise
        """
        try:
            if not self.is_browser_operational():
                return None

            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element if element.is_displayed() and element.is_enabled() else None

        except (NoSuchElementException, Exception):
            return None

    def send_text_to_element(self, element: Any, text: str) -> bool:
        """
        Send text to a specific element.

        Args:
            element: Element to send text to
            text: Text to send

        Returns:
            True if successful, False otherwise
        """
        try:
            if not element or not self.is_browser_operational():
                return False

            # Clear existing text first
            element.clear()
            time.sleep(0.5)

            # Send the text
            element.send_keys(text)
            time.sleep(0.5)

            return True

        except Exception as e:
            print(f"❌ Send text failed: {e}")
            return False

    def click_element(self, element: Any) -> bool:
        """
        Click on a specific element.

        Args:
            element: Element to click

        Returns:
            True if successful, False otherwise
        """
        try:
            if not element or not self.is_browser_operational():
                return False

            element.click()
            time.sleep(1)  # Allow for page updates
            return True

        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False

    def submit_form(self, element: Any) -> bool:
        """
        Submit a form via an element.

        Args:
            element: Form element or submit button

        Returns:
            True if successful, False otherwise
        """
        try:
            if not element or not self.is_browser_operational():
                return False

            # Try to submit via form submission
            try:
                form = element.find_element(By.XPATH, "ancestor-or-self::form")
                form.submit()
            except:
                # Fallback to clicking submit button or the element itself
                element.click()

            time.sleep(2)  # Allow for form submission
            return True

        except Exception as e:
            print(f"❌ Form submit failed: {e}")
            return False

    def wait_for_element(self, selector: str, timeout: int = 10) -> Optional[Any]:
        """
        Wait for an element to appear on the page.

        Args:
            selector: CSS selector to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            Element if found within timeout, None otherwise
        """
        try:
            if not self.is_browser_operational():
                return None

            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element

        except (TimeoutException, Exception):
            return None

    def get_element_text(self, selector: str) -> Optional[str]:
        """
        Get text content of an element.

        Args:
            selector: CSS selector for the element

        Returns:
            Text content if found, None otherwise
        """
        try:
            if not self.is_browser_operational():
                return None

            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip() if element.text else ""

        except (NoSuchElementException, Exception):
            return None

    def get_elements_text(self, selector: str) -> list[str]:
        """
        Get text content of multiple elements.

        Args:
            selector: CSS selector for elements

        Returns:
            List of text contents
        """
        try:
            if not self.is_browser_operational():
                return []

            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            return [elem.text.strip() for elem in elements if elem.text]

        except Exception:
            return []

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript in the browser context.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of script execution
        """
        try:
            if not self.is_browser_operational():
                return None

            return self.driver.execute_script(script, *args)

        except Exception as e:
            print(f"❌ Script execution failed: {e}")
            return None

    def load_cookies(self, cookies: Dict[str, Any]) -> bool:
        """
        Load cookies into the browser.

        Args:
            cookies: Cookie dictionary to load

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.is_browser_operational():
                return False

            for cookie in cookies.values() if isinstance(cookies, dict) else cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"⚠️ Failed to add cookie: {e}")
                    continue

            print(f"🍪 Loaded {len(cookies)} cookies into browser")
            return True

        except Exception as e:
            print(f"❌ Cookie loading failed: {e}")
            return False

    def get_cookies(self) -> Dict[str, Any]:
        """
        Get current cookies from the browser.

        Returns:
            Dictionary of current cookies
        """
        try:
            if not self.is_browser_operational():
                return {}

            cookies = self.driver.get_cookies()
            return {cookie['name']: cookie for cookie in cookies}

        except Exception:
            return {}

    def get_browser_context(self) -> BrowserContext:
        """Get current browser context information."""
        # Update context with current state
        self._context.current_url = self.get_current_url()
        self._context.page_title = self.get_page_title()
        self._context.is_page_ready = self.is_page_ready()
        return self._context

    def test_element_interactability(self) -> bool:
        """
        Test if ChatGPT input elements are actually interactable (not just present).
        This is the critical method from the working monolithic version.
        """
        try:
            print("🔍 Testing element interactability...")

            # Find input elements (from working monolithic version)
            input_selectors = [
                "textarea",
                "[contenteditable='true']",
                "[role='textbox']"
            ]

            for selector in input_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                try:
                                    # Try to send a single character to test interactability
                                    element.send_keys("x")
                                    print(f"✅ Element {selector} is interactable")
                                    # Clear the test character
                                    element.clear()
                                    return True
                                except Exception as e:
                                    print(f"⚠️ Element {selector} not interactable: {e}")
                                    continue
                except Exception as e:
                    print(f"⚠️ Error checking {selector}: {e}")

            print("❌ No interactable input elements found")
            return False

        except Exception as e:
            print(f"❌ Element interactability test failed: {e}")
            return False

    def wait_for_dynamic_content(self, max_wait: int = 15) -> bool:
        """
        Wait for dynamic content to load (from working monolithic version).
        ChatGPT pages often load elements asynchronously.
        """
        print("⏳ Waiting for dynamic content...")
        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                # Check for any input-like elements that might appear dynamically
                all_inputs = self.driver.find_elements(By.CSS_SELECTOR,
                                                       "textarea, input, [contenteditable], [role='textbox'], [data-testid*='input'], [data-testid*='prompt']")

                if all_inputs:
                    displayed_inputs = [elem for elem in all_inputs if elem.is_displayed()]
                    if displayed_inputs:
                        print(f"✅ Found {len(displayed_inputs)} displayed input elements after dynamic wait")
                        return True

                # Check for buttons too
                buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, [role='button']")
                if buttons:
                    displayed_buttons = [btn for btn in buttons if btn.is_displayed()]
                    if displayed_buttons:
                        print(f"✅ Found {len(displayed_buttons)} displayed buttons after dynamic wait")
                        return True

            except Exception as e:
                print(f"Dynamic content check failed: {e}")

            time.sleep(2)  # Check every 2 seconds

        print("❌ No interactive elements found after dynamic wait")
        return False

    def find_interactive_input_element(self) -> Optional[Any]:
        """
        Find an interactive input element using comprehensive selectors (from working monolithic version).
        """
        # Interactive selectors from the working monolithic version
        interactive_selectors = [
            "[contenteditable='true']",
            "[role='textbox']",
            "textarea",
            "[data-testid*='prompt']",
            "[data-testid*='input']",
            ".composer textarea",
            ".input textarea",
            "#prompt-textarea",
            "[placeholder*='message' i]",
            "[placeholder*='ask' i]"
        ]

        for selector in interactive_selectors:
            try:
                candidates = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if candidates:
                    for candidate in candidates:
                        if candidate.is_displayed() and candidate.is_enabled():
                            print(f"✅ Found input with selector: {selector}")
                            return candidate
            except Exception as e:
                print(f"Selector {selector} failed: {e}")

        print("❌ No suitable input element found after exhaustive search")
        return None

    def is_browser_operational(self) -> bool:
        """
        Check if browser is operational and ready for commands.

        Returns:
            True if operational, False otherwise
        """
        if not self.driver:
            return False

        try:
            # Try to access a basic property
            self.driver.current_url
            return self._context.state in [BrowserState.STARTING, BrowserState.READY]
        except Exception:
            return False