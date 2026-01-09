#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Thea Service - V2 Compliant Working Implementation
===================================================

Clean, working implementation based on proven thea_automation.py patterns.
Uses PyAutoGUI for reliable message sending and response_detector for capture.

Author: Agent-3 (Infrastructure & DevOps) - V2 Compliance
License: MIT
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

from src.core.base.base_service import BaseService

# Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Undetected ChromeDriver (preferred for anti-bot bypass)
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

# PyAutoGUI for message sending
try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

# Response detector
try:
    from src.services.thea_response_detector import ResponseDetector, ResponseWaitResult

    DETECTOR_AVAILABLE = True
except ImportError:
    DETECTOR_AVAILABLE = False

# Secure cookie manager (V2 compliance)
try:
    from src.services.thea_secure_cookie_manager import SecureCookieManager
    SECURE_COOKIE_MANAGER_AVAILABLE = True
except ImportError:
    SECURE_COOKIE_MANAGER_AVAILABLE = False

# Thea cookie manager (legacy - DEPRECATED)
try:
    import sys
    from pathlib import Path
    thea_tools_path = Path(__file__).parent.parent.parent / "tools" / "thea"
    if thea_tools_path.exists():
        sys.path.insert(0, str(thea_tools_path))
        from thea_login_handler import TheaCookieManager
        COOKIE_MANAGER_AVAILABLE = True
    else:
        COOKIE_MANAGER_AVAILABLE = False
except ImportError:
    COOKIE_MANAGER_AVAILABLE = False


class TheaService(BaseService):
    """
    V2 compliant Thea communication service.

    Features:
    - Cookie-based session persistence
    - PyAutoGUI message sending (proven working)
    - ResponseDetector integration
    - Autonomous operation
    """

    def __init__(self, cookie_file: str = "thea_cookies.enc", key_file: str = "thea_key.bin", headless: bool = False):
        """Initialize Thea service with secure cookie management."""
        super().__init__("TheaService")
        self.cookie_file = cookie_file  # Keep as string for compatibility
        self.key_file = key_file
        self.headless = headless
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        self.responses_dir = Path("thea_responses")
        self.responses_dir.mkdir(exist_ok=True)

        self.driver = None
        self.detector = None

        # Use secure cookie manager by default (V2 compliance)
        if SECURE_COOKIE_MANAGER_AVAILABLE:
            self.cookie_manager = SecureCookieManager(cookie_file, key_file)
            self.secure_cookies = True
            self.logger.info("✅ Using secure encrypted cookie storage")
        elif COOKIE_MANAGER_AVAILABLE:
            # Fallback to legacy manager (deprecated)
            self.cookie_manager = TheaCookieManager(
                str(cookie_file).replace('.enc', '.json'))
            self.secure_cookies = False
            self.logger.warning(
                "⚠️ Using legacy cookie manager - upgrade recommended")
        else:
            self.cookie_manager = None
            self.secure_cookies = False
            self.logger.warning(
                "❌ No cookie manager available - basic handling only")

        # Validate CRITICAL dependencies (fail hard)
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium required: pip install selenium")
        if not UNDETECTED_AVAILABLE:
            raise ImportError("undetected-chromedriver REQUIRED for anti-bot bypass: pip install undetected-chromedriver")
        if not SECURE_COOKIE_MANAGER_AVAILABLE and not COOKIE_MANAGER_AVAILABLE:
            raise ImportError("Secure cookie manager required for credential safety: pip install cryptography")

        # Optional dependencies (warnings only)
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning(
                "PyAutoGUI not available - message sending may not work")
        if not DETECTOR_AVAILABLE:
            self.logger.warning(
                "Response detector not available - will use basic polling")

    def start_browser(self) -> bool:
        """Initialize browser with cookies using undetected-chromedriver."""
        try:
            self.logger.info("🚀 Starting browser...")

            # REQUIRE undetected-chromedriver (no fallback to standard Chrome)
            if not UNDETECTED_AVAILABLE:
                self.logger.error("❌ undetected-chromedriver is REQUIRED for anti-bot bypass")
                self.logger.error("Install with: pip install undetected-chromedriver")
                return False

            try:
                self.logger.info("🔐 Starting undetected-chromedriver for anti-bot bypass...")

                options = uc.ChromeOptions()
                if self.headless:
                    self.logger.warning("⚠️ Headless mode may be detected by anti-bot systems")
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
                self.logger.info("✅ Undetected Chrome browser started successfully")
                return True

            except Exception as e:
                self.logger.error(f"❌ Undetected Chrome failed: {e}")
                self.logger.error("Cannot proceed without anti-bot protection")
                return False
            options = Options()
            if self.headless:
                options.add_argument("--headless=new")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # Anti-detection
            options.add_argument(
                "--disable-blink-features=AutomationControlled")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            self.driver = webdriver.Chrome(options=options)
            self.logger.info("✅ Standard Chrome browser started")
            return True

        except Exception as e:
            self.logger.error(f"❌ Browser start failed: {e}")
            return False

    def are_cookies_fresh(self) -> bool:
        """Check if cookies exist and are fresh (not expired). Uses secure cookie manager."""
        if self.cookie_manager:
            # Use secure cookie manager validation
            is_valid = self.cookie_manager.has_valid_cookies()
            if is_valid:
                self.logger.info(
                    "✅ Cookies are fresh and valid (secure validation)" if self.secure_cookies else "✅ Cookies are fresh (legacy validation)")
            else:
                self.logger.warning("⚠️ Cookies are stale or invalid")
            return is_valid
        else:
            # Emergency fallback
            self.logger.warning(
                "🚨 EMERGENCY: No cookie manager - basic file check only")
            if not Path(self.cookie_file).exists():
                self.logger.info("🍪 No cookie file found")
                return False
            self.logger.warning(
                "⚠️ Using basic file existence check - INSECURE")
            return True  # Assume valid if file exists (not recommended)

    def validate_cookies(self) -> bool:
        """Validate that cookies actually work by testing login."""
        if not self.driver:
            if not self.start_browser():
                return False

        try:
            # Go to main ChatGPT site first (where cookies are typically set)
            chatgpt_main_url = "https://chatgpt.com"
            self.logger.info(f"🔍 Navigating to main ChatGPT site first: {chatgpt_main_url}")
            self.driver.get(chatgpt_main_url)
            time.sleep(3)

            # Load cookies on the main site
            if self.cookie_manager:
                self.logger.info("🍪 Loading cookies on main ChatGPT site...")
                success = self.cookie_manager.load_cookies(self.driver)
                if not success:
                    self.logger.warning(
                        "⚠️ Cookie load failed - may need re-authentication")
                else:
                    self.logger.info("✅ Cookies loaded into browser")

                    # Verify cookies were actually loaded
                    current_cookies = self.driver.get_cookies()
                    self.logger.info(f"🔍 Browser has {len(current_cookies)} cookies after loading")

            # Now navigate to Thea URL with cookies loaded
            self.logger.info(f"🏗️ Navigating to Thea URL for validation: {self.thea_url}")
            self.driver.get(self.thea_url)
            time.sleep(5)  # Allow page to load and stabilize

            # Check current URL after navigation
            current_url = self.driver.current_url
            self.logger.info(f"📍 Current URL after Thea navigation: {current_url}")

            # If redirected to login/auth page, cookies failed
            if "login" in current_url.lower() or "auth" in current_url.lower():
                self.logger.warning("⚠️ Redirected to login page - cookies may be invalid or expired")
                return False
            else:
                self.logger.info("✅ No redirect to login page - cookies appear valid")

            # Additional login check
            login_result = self._is_logged_in()
            self.logger.info(f"🔍 Login check result: {login_result}")

            if login_result:
                self.logger.info("✅ Cookie validation successful")
                return True
            else:
                self.logger.warning(
                    "⚠️ Cookie validation failed - not properly logged in")
                return False

        except Exception as e:
            self.logger.error(f"❌ Cookie validation error: {e}")
            return False

    def refresh_cookies(self) -> bool:
        """Refresh cookies by re-authenticating."""
        self.logger.info("🔄 Refreshing cookies...")

        if not self.driver:
            if not self.start_browser():
                return False

        try:
            # Navigate to main ChatGPT site first
            chatgpt_main_url = "https://chatgpt.com"
            self.logger.info(f"🏠 Going to main ChatGPT site: {chatgpt_main_url}")
            self.driver.get(chatgpt_main_url)
            time.sleep(3)

            # Check if already logged in
            if self._is_logged_in():
                # Save cookies using secure cookie manager ONLY
                if self.cookie_manager:
                    success = self.cookie_manager.save_cookies(self.driver)
                    if success:
                        self.logger.info(
                            "✅ Cookies refreshed securely" if self.secure_cookies else "✅ Cookies refreshed (legacy)")
                        return True
                    else:
                        self.logger.error("❌ Cookie save failed - cannot proceed without secure cookie storage")
                        return False
                else:
                    # NO emergency fallback - fail hard for security
                    self.logger.error("🚨 CRITICAL: No secure cookie manager available - refusing to save credentials insecurely")
                    return False

            # Manual login required
            self.logger.info("⚠️ Manual login required to refresh cookies")
            self.logger.info(
                "Please log in to ChatGPT in the browser window...")
            self.logger.info("⏳ Waiting 60 seconds for manual login...")
            time.sleep(60)

            if self._is_logged_in():
                # Save cookies using secure cookie manager ONLY
                if self.cookie_manager:
                    success = self.cookie_manager.save_cookies(self.driver)
                    if success:
                        self.logger.info(
                            "✅ Cookies refreshed securely after manual login" if self.secure_cookies else "✅ Cookies refreshed after manual login (legacy)")
                        return True
                    else:
                        self.logger.error("❌ Cookie save failed after manual login - secure storage required")
                        return False
                else:
                    # NO emergency fallback - fail hard for security
                    self.logger.error("🚨 CRITICAL: No secure cookie manager available - cannot save credentials after manual login")
                    return False

            self.logger.error("❌ Manual login validation failed - cookies not refreshed")
            return False

        except Exception as e:
            self.logger.error(f"❌ Cookie refresh error: {e}")
            return False

    def ensure_login(self, force_refresh: bool = False) -> bool:
        """Ensure logged in to Thea Manager with fresh cookies."""
        try:
            self.logger.info("🔐 Starting login process...")
            if not self.driver:
                if not self.start_browser():
                    return False

            # Check cookie freshness
            cookies_fresh = self.are_cookies_fresh()
            self.logger.info(f"🍪 Cookies fresh: {cookies_fresh}, force_refresh: {force_refresh}")

            if not force_refresh and cookies_fresh:
                # Validate cookies work by testing login
                self.logger.info("🔍 Validating existing cookies...")
                if self.validate_cookies():
                    self.logger.info("✅ Using fresh, valid cookies")
                    return True
                else:
                    self.logger.warning(
                        "⚠️ Cookies exist but failed validation - they may be stale despite timestamp")
                    force_refresh = True

            # Refresh cookies if needed
            if force_refresh or not cookies_fresh:
                self.logger.info("🔄 Refreshing cookies...")
                if not self.refresh_cookies():
                    self.logger.error("❌ Cookie refresh failed")
                    return False

                # Validate after refresh
                self.logger.info("🔍 Validating refreshed cookies...")
                if not self.validate_cookies():
                    self.logger.error(
                        "❌ Cookies refreshed but validation failed")
                    return False

            self.logger.info("✅ Login ensured with fresh cookies")
            return True

        except Exception as e:
            self.logger.error(f"❌ Login error: {e}")
            return False

    def _is_logged_in(self) -> bool:
        """Check if logged in."""
        try:
            current_url = self.driver.current_url
            self.logger.debug(f"🔍 Login check - URL: {current_url}")

            if "auth" in current_url or "login" in current_url:
                self.logger.debug("❌ Login check: URL contains auth/login")
                return False

            # Check for textarea (indicates logged in)
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, "textarea")
                is_displayed = elem.is_displayed()
                self.logger.debug(f"🔍 Login check - textarea found: {is_displayed}")
                return is_displayed
            except Exception as e:
                self.logger.debug(f"🔍 Login check - textarea not found: {e}")

            url_check = "chatgpt.com" in current_url
            self.logger.debug(f"🔍 Login check - URL contains chatgpt.com: {url_check}")
            return url_check

        except Exception as e:
            self.logger.debug(f"🔍 Login check - error: {e}")
            return False

    def _wait_for_page_ready(self, timeout: float = 15.0) -> bool:
        """Wait for page to be ready for input."""
        try:
            self.logger.debug("⏳ Waiting for page to be ready...")

            # Wait for document ready
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    ready_state = self.driver.execute_script("return document.readyState")
                    if ready_state == "complete":
                        self.logger.debug("✅ Document ready state: complete")
                        break
                except Exception as e:
                    self.logger.debug(f"Document ready check failed: {e}")
                time.sleep(0.5)

            # Wait for ChatGPT/Custom GPT specific elements
            ready_selectors = [
                "textarea",  # Most common input element
                "[contenteditable='true']",  # Contenteditable divs
                "[role='textbox']",  # ARIA textbox role
                "div[data-message-author-role]",  # Message containers
                ".markdown",  # Content areas
                "[data-testid]",  # Any test IDs
                "button",  # Any buttons (usually present when loaded)
            ]

            self.logger.debug("🔍 Checking for page elements...")
            for selector in ready_selectors:
                try:
                    from selenium.webdriver.support import expected_conditions as EC
                    from selenium.webdriver.support.ui import WebDriverWait

                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if element:
                        self.logger.debug(f"✅ Page ready - found element: {selector}")
                        return True
                except Exception as e:
                    self.logger.debug(f"Element {selector} not found: {e}")
                    continue

            # More permissive fallback: check if page has substantial content and no loading indicators
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                page_title = self.driver.title

                self.logger.debug(f"📄 Page title: {page_title}")
                self.logger.debug(f"📏 Body text length: {len(body_text)}")

                # Check for loading indicators
                loading_indicators = ["loading", "please wait", "connecting"]
                has_loading = any(indicator in body_text.lower() for indicator in loading_indicators)

                if len(body_text) > 50 and not has_loading and "chatgpt" in page_title.lower():
                    self.logger.debug("✅ Page appears ready (permissive fallback check)")
                    return True
                elif has_loading:
                    self.logger.debug("⏳ Page still loading...")
                    return False
            except Exception as e:
                self.logger.debug(f"Fallback check failed: {e}")

            self.logger.warning("⚠️ Page readiness check failed - no suitable elements found")
            return False

        except Exception as e:
            self.logger.error(f"❌ Page ready check error: {e}")
            return False

    def send_message(self, message: str, wait_for_response: bool = True) -> str | None:
        """
        Send message to Thea and optionally wait for response.

        Args:
            message: Message to send
            wait_for_response: Whether to wait for response

        Returns:
            Response text if wait_for_response=True, else None
        """
        try:
            # Ensure browser and login
            if not self.driver:
                if not self.start_browser():
                    return None

            if not self.ensure_login():
                return None

            # Ensure we're on the correct Thea URL and page is fully loaded
            current_url = self.driver.current_url
            self.logger.info(f"📍 Current URL: {current_url}")

            # Navigate to Thea URL if not already there
            if self.thea_url not in current_url:
                self.logger.info(f"🏗️ Navigating to Thea: {self.thea_url}")
                self.driver.get(self.thea_url)

                # Wait for page to fully load and stabilize
                if not self._wait_for_page_ready():
                    self.logger.error("❌ Page failed to load properly after navigation")
                    return None

                new_url = self.driver.current_url
                self.logger.info(f"📍 New URL after navigation: {new_url}")

                # Check if we're actually logged in at Thea URL
                if "login" in new_url.lower() or "auth" in new_url.lower():
                    self.logger.warning("⚠️ Redirected to login page - cookies may be invalid")
                    return None

                self.logger.info("✅ Reached Thea URL and page is ready")
            else:
                self.logger.info("✅ Already on Thea URL")

            # Additional check: ensure page is ready for input even if URL is correct
            if not self._wait_for_page_ready():
                self.logger.error("❌ Page not ready for input")
                return None

            # Additional wait for dynamic content - ChatGPT pages often load elements asynchronously
            self.logger.info("⏳ Waiting additional time for dynamic content...")
            max_dynamic_wait = 30  # seconds
            dynamic_start = time.time()

            while time.time() - dynamic_start < max_dynamic_wait:
                try:
                    # Check for any input-like elements that might appear dynamically
                    all_inputs = self.driver.find_elements(By.CSS_SELECTOR,
                        "textarea, input, [contenteditable], [role='textbox'], [data-testid*='input'], [data-testid*='prompt']")

                    if all_inputs:
                        displayed_inputs = [elem for elem in all_inputs if elem.is_displayed()]
                        if displayed_inputs:
                            self.logger.info(f"✅ Found {len(displayed_inputs)} displayed input elements after dynamic wait")
                            break

                    # Check for buttons too
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, [role='button']")
                    if buttons:
                        displayed_buttons = [btn for btn in buttons if btn.is_displayed()]
                        if displayed_buttons:
                            self.logger.info(f"✅ Found {len(displayed_buttons)} displayed buttons after dynamic wait")
                            break

                except Exception as e:
                    self.logger.debug(f"Dynamic content check failed: {e}")

                time.sleep(2)  # Check every 2 seconds

            # Debug: Check what elements are actually on the page
            self.logger.info("🔍 Debugging page content...")
            try:
                # Get page source snippet
                page_source = self.driver.page_source
                self.logger.info(f"📄 Page source length: {len(page_source)}")

                # Check for common ChatGPT elements
                all_elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
                self.logger.info(f"📊 Total elements on page: {len(all_elements)}")

                # Look for form-related elements
                forms = self.driver.find_elements(By.TAG_NAME, "form")
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
                divs = self.driver.find_elements(By.TAG_NAME, "div")

                self.logger.info(f"📋 Forms: {len(forms)}, Buttons: {len(buttons)}, Inputs: {len(inputs)}, Textareas: {len(textareas)}, Divs: {len(divs)}")

                # Check for contenteditable divs specifically
                contenteditable = self.driver.find_elements(By.CSS_SELECTOR, "[contenteditable]")
                self.logger.info(f"📝 Contenteditable elements: {len(contenteditable)}")

                for i, elem in enumerate(contenteditable[:3]):
                    try:
                        text = elem.text[:50] if elem.text else "empty"
                        displayed = elem.is_displayed()
                        enabled = elem.is_enabled()
                        self.logger.info(f"  CE {i+1}: displayed={displayed}, enabled={enabled}, text='{text}'")
                    except Exception as e:
                        self.logger.info(f"  CE {i+1}: error checking - {e}")

                # Check for any data-testid attributes (common in React apps)
                testids = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid]")
                self.logger.info(f"🧪 Data-testid elements: {len(testids)}")

                for i, elem in enumerate(testids[:5]):
                    try:
                        testid = elem.get_attribute("data-testid")
                        tag = elem.tag_name
                        displayed = elem.is_displayed()
                        self.logger.info(f"  TestID {i+1}: {tag}[data-testid='{testid}'] displayed={displayed}")
                    except:
                        pass

                # Check if this is actually a ChatGPT page
                if "chatgpt" not in self.driver.current_url.lower():
                    self.logger.error("❌ Not on ChatGPT page anymore!")
                    return None

                # Try a more permissive approach - look for any interactive input area
                # ChatGPT might be using a different selector
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

                textarea = None
                for selector in interactive_selectors:
                    try:
                        candidates = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if candidates:
                            for candidate in candidates:
                                if candidate.is_displayed() and candidate.is_enabled():
                                    textarea = candidate
                                    self.logger.info(f"✅ Found input with selector: {selector}")
                                    break
                            if textarea:
                                break
                    except Exception as e:
                        self.logger.debug(f"Selector {selector} failed: {e}")

                if not textarea:
                    self.logger.error("❌ No suitable input element found after exhaustive search")
                    return None

                self.logger.info("✅ Input element ready for interaction")

            except Exception as e:
                self.logger.error(f"❌ Error debugging page: {e}")
                return None

            # Send message via Selenium (more reliable than PyAutoGUI in server environments)
            self.logger.info(f"📤 Sending message via Selenium: {message[:50]}...")

            try:
                # Use Selenium's send_keys on the contenteditable element
                textarea.send_keys(message)
                time.sleep(1)  # Allow text to be entered

                # Try to send Enter - different approaches for different input types
                try:
                    from selenium.webdriver.common.keys import Keys

                    if textarea.tag_name.lower() == 'textarea':
                        textarea.send_keys(Keys.ENTER)
                    else:
                        # For contenteditable, try Ctrl+Enter or just Enter
                        textarea.send_keys(Keys.CONTROL, Keys.ENTER)
                        time.sleep(0.5)
                        # Fallback: look for send button
                        try:
                            send_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                "button[data-testid*='send'], button[type='submit'], [role='button']")
                            for btn in send_buttons:
                                if btn.is_displayed() and btn.is_enabled():
                                    btn.click()
                                    self.logger.info("✅ Clicked send button")
                                    break
                        except Exception as e:
                            self.logger.warning(f"Send button click failed: {e}")
                            # Last resort: just Enter key
                            textarea.send_keys(Keys.ENTER)

                except Exception as e:
                    self.logger.warning(f"Enter key failed, trying send button: {e}")
                    # Look for send button
                    send_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                        "button[data-testid*='send'], button[type='submit'], [role='button']")
                    for btn in send_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            self.logger.info("✅ Clicked send button as fallback")
                            break

                self.logger.info("✅ Message sent via Selenium")

            except Exception as e:
                self.logger.error(f"❌ Selenium message sending failed: {e}")
                # Fallback to PyAutoGUI if available
                if PYAUTOGUI_AVAILABLE:
                    try:
                        self.logger.info("🔄 Falling back to PyAutoGUI...")
                        try:
                            pyperclip.copy(message)
                            time.sleep(0.5)
                            pyautogui.hotkey("ctrl", "v")
                        except Exception as clipboard_error:
                            self.logger.warning(f"⚠️ Clipboard paste failed ({clipboard_error}), falling back to typing...")
                            # Fallback: type the message character by character
                            pyautogui.typewrite(message, interval=0.01)
                        time.sleep(0.5)
                        pyautogui.press("enter")
                        self.logger.info("✅ Message sent via PyAutoGUI fallback")
                    except Exception as e2:
                        self.logger.error(f"❌ PyAutoGUI fallback also failed: {e2}")
                        return None
                else:
                    return None

            # Wait for response if requested
            if wait_for_response:
                return self.wait_for_response()

            return None

        except Exception as e:
            self.logger.error(f"❌ Send message failed: {e}")
            return None

    def wait_for_response(self, timeout: int = 120) -> str | None:
        """Wait for and capture Thea's response."""
        try:
            self.logger.info("⏳ Waiting for response...")

            if not DETECTOR_AVAILABLE:
                self.logger.warning(
                    "ResponseDetector not available - basic wait")
                time.sleep(15)
                return self._extract_basic_response()

            if not self.detector:
                self.detector = ResponseDetector(self.driver)

            # Wait for response
            result = self.detector.wait_until_complete(
                timeout=timeout, stable_secs=3.0, auto_continue=True
            )

            if result == ResponseWaitResult.COMPLETE:
                self.logger.info("✅ Response complete")
                response = self.detector.extract_response_text()
                return response
            else:
                self.logger.warning(f"⚠️ Response status: {result}")
                response = self.detector.extract_response_text()
                return response or f"⚠️ Incomplete: {result}"

        except Exception as e:
            self.logger.error(f"❌ Response capture failed: {e}")
            return None

    def _extract_basic_response(self) -> str | None:
        """Basic response extraction fallback."""
        try:
            articles = self.driver.find_elements(By.TAG_NAME, "article")
            if articles and len(articles) > 1:
                return articles[-1].text.strip()
            return None
        except:
            return None

    def communicate(self, message: str, save: bool = True) -> dict:
        """
        Complete communication cycle: send message and get response.

        Args:
            message: Message to send
            save: Whether to save conversation

        Returns:
            dict with 'success', 'message', 'response', 'file' keys
        """
        result = {"success": False, "message": message,
                  "response": "", "file": ""}

        try:
            response = self.send_message(message, wait_for_response=True)

            if response:
                result["response"] = response
                result["success"] = True

                if save:
                    result["file"] = self._save_conversation(message, response)

            return result

        except Exception as e:
            result["response"] = f"Error: {e}"
            return result

    def _save_conversation(self, message: str, response: str) -> str:
        """Save conversation to file."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = self.responses_dir / f"conversation_{timestamp}.json"

            data = {
                "timestamp": timestamp,
                "message": message,
                "response": response,
                "thea_url": self.thea_url,
            }

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"💾 Saved to: {filename}")
            return str(filename)

        except Exception as e:
            self.logger.error(f"❌ Save failed: {e}")
            return ""

    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("✅ Browser closed")
            except:
                pass
            finally:
                self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


# Factory
def create_thea_service(
    cookie_file: str = "thea_cookies.enc",
    key_file: str = "thea_key.bin",
    headless: bool = False
) -> TheaService:
    """Create Thea service instance with secure cookie management."""
    return TheaService(cookie_file, key_file, headless)


__all__ = ["TheaService", "create_thea_service"]
