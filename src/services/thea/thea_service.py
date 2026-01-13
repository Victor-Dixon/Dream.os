<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
import os
import time
from datetime import datetime
from pathlib import Path

from src.core.base.base_service import BaseService

# Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

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
            raise ImportError(
                "undetected-chromedriver REQUIRED for anti-bot bypass: pip install undetected-chromedriver")
        if not SECURE_COOKIE_MANAGER_AVAILABLE and not COOKIE_MANAGER_AVAILABLE:
            raise ImportError(
                "Secure cookie manager required for credential safety: pip install cryptography")

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
                self.logger.error(
                    "❌ undetected-chromedriver is REQUIRED for anti-bot bypass")
                self.logger.error(
                    "Install with: pip install undetected-chromedriver")
                return False

            try:
                self.logger.info(
                    "🔐 Starting undetected-chromedriver for anti-bot bypass...")

                options = uc.ChromeOptions()
                if self.headless:
                    self.logger.warning(
                        "⚠️ Headless mode may be detected by anti-bot systems")
                    options.add_argument("--headless=new")

                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument(
                    "--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-plugins")
                # Prefer prefs over unknown flags like --disable-images
                options.add_experimental_option(
                    "prefs", {"profile.managed_default_content_settings.images": 2})

                self.driver = uc.Chrome(
                    options=options,
                    use_subprocess=True,
                    driver_executable_path=None  # Auto-download correct version
                )
                self.logger.info(
                    "✅ Undetected Chrome browser started successfully")
                return True

            except Exception as e:
                self.logger.error(f"❌ Undetected Chrome failed: {e}")
                self.logger.error("Cannot proceed without anti-bot protection")
                return False

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
            # Cookie load MUST happen on base domain first, then refresh, then navigate
            self.logger.info(
                "🔍 ===== STARTING COOKIE VALIDATION (THEA GPT) =====")
            base_url = "https://chatgpt.com"
            self.logger.info(
                f"🔍 Step 1: Navigating to base domain: {base_url}")
            self.driver.get(base_url)
            time.sleep(3)

            # Load cookies on base domain
            if self.cookie_manager:
                self.logger.info("🍪 Step 2: Loading cookies on base domain...")
                success = self.cookie_manager.load_cookies(self.driver)
                if not success:
                    self.logger.warning("⚠️ Step 2 result: Cookie load failed")
                    return False
                else:
                    self.logger.info(
                        "✅ Step 2 result: Cookies loaded successfully")
                    current_cookies = self.driver.get_cookies()
                    self.logger.info(
                        f"🔍 Step 2 result: Browser has {len(current_cookies)} cookies after loading")

            # Refresh to apply cookies
            self.driver.get(base_url)
            time.sleep(2)

            # Now try Thea GPT URL (preferred)
            self.logger.info(
                f"🔍 Step 3: Navigating to Thea GPT: {self.thea_url}")
            self.driver.get(self.thea_url)
            time.sleep(3)

            # Check if Thea GPT loads properly
            current_url = self.driver.current_url
            page_title = self.driver.title
            self.logger.info(f"📍 Step 4 result: Current URL = {current_url}")
            self.logger.info(f"📍 Step 4 result: Page title = '{page_title}'")

            # If redirected to login/auth page, cookies failed
            if "login" in current_url.lower() or "auth" in current_url.lower():
                self.logger.warning(
                    "⚠️ Redirected to login page - cookies invalid")
                return False

            # Check if Thea GPT actually loaded (has interface elements)
            self.logger.info(
                "🔍 Step 5: Checking if Thea GPT interface loaded...")
            login_result = self._is_logged_in()
            self.logger.info(
                f"🔍 Step 5 result: Interface check = {login_result}")

            if login_result:
                # CRITICAL: Check if elements are actually interactable
                self.logger.info(
                    "🔍 Step 6: Testing Thea GPT element interactability...")
                interactable_result = self._test_element_interactability()
                self.logger.info(
                    f"🔍 Step 6 result: Thea GPT elements interactable = {interactable_result}")

                if interactable_result:
                    self.logger.info(
                        "✅ ===== THEA GPT VALIDATION SUCCESSFUL =====")
                return True
            else:
                self.logger.warning(
                        "⚠️ Thea GPT elements exist but not interactable - likely stale cookies")
                    # Continue to fallback

            # SECOND: If Thea GPT fails, try basic ChatGPT as fallback
            self.logger.warning(
                "⚠️ Thea GPT interface not functional, trying basic ChatGPT fallback...")
            self.logger.info(
                "🔍 ===== FALLBACK: BASIC CHATGPT VALIDATION =====")

            chatgpt_main_url = "https://chatgpt.com"
            self.logger.info(
                f"🔍 Fallback Step 1: Navigating to basic ChatGPT: {chatgpt_main_url}")
            self.driver.get(chatgpt_main_url)
            time.sleep(3)

            # Cookies were already loaded on base domain; just ensure still not redirected
            current_url = self.driver.current_url
            page_title = self.driver.title
            self.logger.info(
                f"📍 Fallback Step 3 result: URL = {current_url}, Title = '{page_title}'")

            if "login" in current_url.lower() or "auth" in current_url.lower():
                self.logger.warning("⚠️ Fallback failed: Still on login page")
                return False

            login_result = self._is_logged_in()
            self.logger.info(
                f"🔍 Fallback Step 4 result: Basic ChatGPT interface check = {login_result}")

            if login_result:
                # CRITICAL: Check if elements are actually interactable (not just present)
                self.logger.info(
                    "🔍 Fallback Step 5: Testing element interactability...")
                interactable_result = self._test_element_interactability()
                self.logger.info(
                    f"🔍 Fallback Step 5 result: Elements interactable = {interactable_result}")

                if interactable_result:
                    self.logger.info(
                        "✅ ===== BASIC CHATGPT VALIDATION SUCCESSFUL =====")
                    self.logger.warning(
                        "⚠️ NOTE: Using basic ChatGPT instead of Thea GPT (Thea GPT appears unavailable)")
                    # Update URL to basic ChatGPT for future use
                    self.thea_url = chatgpt_main_url
                return True
            else:
                self.logger.warning("⚠️ ===== STALE COOKIES DETECTED =====")
                self.logger.warning(
                    "⚠️ Elements exist but are not interactable - cookies are stale")
                return False
        except Exception as e:
            self.logger.error(
                "❌ ===== ALL VALIDATION METHODS FAILED =====")
            self.logger.error(
                "❌ Neither Thea GPT nor basic ChatGPT interface is functional")
            self.logger.error(f"❌ Validation error: {e}")
            return False

        except Exception as e:
            self.logger.error(f"❌ ===== COOKIE VALIDATION ERROR: {e} =====")
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
            self.logger.info(
                f"🏠 Going to main ChatGPT site: {chatgpt_main_url}")
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
                        self.logger.error(
                            "❌ Cookie save failed - cannot proceed without secure cookie storage")
                        return False
                else:
                    # NO emergency fallback - fail hard for security
                    self.logger.error(
                        "🚨 CRITICAL: No secure cookie manager available - refusing to save credentials insecurely")
                    return False

            # Attempt automated login first
            self.logger.info("🔄 Attempting automated login...")
            if self._attempt_automated_login():
                self.logger.info("✅ Automated login successful!")
                # Save cookies after successful login
                if self.cookie_manager:
                    success = self.cookie_manager.save_cookies(self.driver)
                    if success:
                        self.logger.info("✅ Cookies saved after automated login")
                        return True
                    else:
                        self.logger.error("❌ Failed to save cookies after login")
                        return False
                return True
            else:
                self.logger.warning("❌ Automated login failed, manual login required")

            # Manual login required - guide user through the process
            self.logger.info("🔐 ===== MANUAL LOGIN REQUIRED =====")
            self.logger.info("📋 INSTRUCTIONS:")
            self.logger.info(
                "   1. Browser window should be open with ChatGPT")
            self.logger.info("   2. Click 'Log in' or 'Sign in' button")
            self.logger.info(
                "   3. Complete login process (email/password or Google/Apple)")
            self.logger.info("   4. Wait for ChatGPT interface to load fully")
            self.logger.info("   5. Return to this terminal when ready")
            self.logger.info("")
            self.logger.info(
                "⏳ Waiting for you to complete login... (press Enter when done)")

            # Wait for user input instead of fixed timeout
            try:
                input("Press Enter when login is complete...")
                self.logger.info("✅ User indicated login is complete")
            except KeyboardInterrupt:
                self.logger.info("⏹️ Login process interrupted by user")
                return False

            # Give page time to fully load after login
            self.logger.info(
                "⏳ Allowing time for page to stabilize after login...")
            time.sleep(5)

            # Verify login was successful with comprehensive checks
            self.logger.info("🔍 Verifying login success...")

            # Check 1: Basic login detection
            login_check = self._is_logged_in()
            self.logger.info(f"   Basic login check: {login_check}")

            if not login_check:
                self.logger.error("❌ Basic login check failed")
                return False

            # Check 2: Element interactability (critical for stale cookie detection)
            interactable_check = self._test_element_interactability()
            self.logger.info(
                f"   Element interactability check: {interactable_check}")

            if not interactable_check:
                self.logger.error(
                    "❌ Elements not interactable - login may have failed")
                self.logger.info(
                    "💡 Try logging in again, or check if ChatGPT is blocking automation")
                return False

            # Check 3: Ensure we're on the right page
            current_url = self.driver.current_url
            if "chatgpt.com" not in current_url:
                self.logger.error(f"❌ Not on ChatGPT page: {current_url}")
                return False

            self.logger.info("✅ All login verification checks passed")

            # Save cookies using secure cookie manager ONLY
            if self.cookie_manager:
                    self.logger.info("💾 Saving new cookies...")
                    success = self.cookie_manager.save_cookies(self.driver)
                    if success:
                        self.logger.info(
                            "✅ Cookies saved securely after manual login" if self.secure_cookies else "✅ Cookies saved after manual login (legacy)")
                        self.logger.info(
                            "🎉 ===== LOGIN PROCESS COMPLETE =====")
                        return True
                    else:
                        self.logger.error(
                            "❌ Cookie save failed after manual login - secure storage required")
                        return False
            else:
                # NO emergency fallback - fail hard for security
                self.logger.error(
                    "🚨 CRITICAL: No secure cookie manager available - cannot save credentials after manual login")
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
            self.logger.info(
                f"🍪 Cookies fresh: {cookies_fresh}, force_refresh: {force_refresh}")

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
        """Check if logged in by verifying page has proper ChatGPT interface."""
        try:
            current_url = self.driver.current_url
            page_title = self.driver.title
            self.logger.debug(f"🔍 Login check - URL: {current_url}")
            self.logger.debug(f"🔍 Login check - Title: '{page_title}'")

            # Check for obvious login/auth pages
            if "auth" in current_url.lower() or "login" in current_url.lower():
                self.logger.debug("❌ Login check: URL contains auth/login")
                return False

            # Check if we're on ChatGPT domain
            if "chatgpt.com" not in current_url:
                self.logger.debug("❌ Login check: Not on chatgpt.com domain")
                return False

            # Check page title - should be "ChatGPT" or contain GPT info
            if not page_title or "chatgpt" not in page_title.lower():
                self.logger.debug(
                    f"❌ Login check: Unexpected page title: '{page_title}'")
                return False

            # Check for login-specific elements that indicate we're NOT logged in
            try:
                # Look for login buttons or signup elements
                login_indicators = [
                    "[data-testid='login-button']",
                    "[data-testid='signup-button']",
                    "button:contains('Log in')",
                    "button:contains('Sign in')",
                    "button:contains('Sign up')",
                    "a:contains('Log in')",
                    "a:contains('Sign in')"
                ]

                for indicator in login_indicators:
                    try:
                        elements = self.driver.find_elements(
                            By.CSS_SELECTOR, indicator)
                        if elements:
                            visible_login_elements = [
                                elem for elem in elements if elem.is_displayed()]
                            if visible_login_elements:
                                self.logger.debug(
                                    f"❌ Login check: Found login elements ({indicator}) - user is NOT logged in")
                                return False
                    except:
                        pass

            except Exception as e:
                self.logger.debug(
                    f"🔍 Login check - login element search error: {e}")

            # Check for ChatGPT-specific elements that indicate proper login
            # Look for multiple indicators of a working ChatGPT page
            indicators = [
                    "textarea",  # Input area
                    "[contenteditable]",  # Alternative input
                    "[role='textbox']",  # ARIA textbox role
                    ".composer",  # Composer area
                    "[data-testid*='model']",  # Model selector
                    "[data-testid*='new-chat']",  # New chat button
                    "[data-testid*='regenerate']",  # Regenerate button
                ]

            found_indicators = 0
            for indicator in indicators:
                    try:
                        elements = self.driver.find_elements(
                            By.CSS_SELECTOR, indicator)
                        if elements:
                            # Check if any are displayed and enabled
                            visible_elements = [
                                elem for elem in elements if elem.is_displayed()]
                            if visible_elements:
                                found_indicators += 1
                                self.logger.debug(
                                    f"✅ Login check: Found {len(visible_elements)} visible {indicator} elements")
                    except:
                        pass

            # Require at least 2 different types of indicators for a valid page
            if found_indicators >= 2:
                self.logger.debug(
                    f"✅ Login check: Found {found_indicators} indicator types - testing interactability...")

                # CRITICAL: Test if elements are actually interactable (not just displayed)
                if self._test_element_interactability():
                    self.logger.debug("✅ Elements are interactable - user is logged in")
                    return True
                else:
                    self.logger.debug("❌ Elements exist but not interactable - STALE COOKIES DETECTED")
                    return False
            else:
                self.logger.debug(
                    f"❌ Login check: Only found {found_indicators} indicator types - page not fully loaded or not logged in")
                return False

        except Exception as e:
            self.logger.debug(f"❌ Login check failed: {e}")
            return False

    def _attempt_automated_login(self) -> bool:
        """Attempt automated login using stored credentials."""
        try:
            self.logger.info("🚀 Starting automated login process...")

            # Check for login credentials in environment/config
            email = os.getenv('CHATGPT_EMAIL') or os.getenv('OPENAI_EMAIL')
            password = os.getenv('CHATGPT_PASSWORD') or os.getenv('OPENAI_PASSWORD')

            if not email or not password:
                self.logger.warning("⚠️ No login credentials found in environment variables")
                self.logger.info("💡 Set CHATGPT_EMAIL and CHATGPT_PASSWORD environment variables for automated login")
                return False

            self.logger.info("🔑 Found login credentials, attempting automated login...")

            # Look for login button and click it
            login_selectors = [
                "[data-testid='login-button']",
                "button:contains('Log in')",
                "button:contains('Sign in')",
                "a:contains('Log in')",
                "a:contains('Sign in')"
            ]

            login_button = None
            for selector in login_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        login_button = elements[0]
                        self.logger.info(f"✅ Found login button: {selector}")
                        break
                except:
                    continue

            if not login_button:
                self.logger.warning("❌ Could not find login button")
                return False

            # Click login button
            login_button.click()
            time.sleep(2)

            # Look for email input
            email_selectors = [
                "input[type='email']",
                "input[name='email']",
                "input[name='username']",
                "input[placeholder*='email']",
                "input[placeholder*='Email']"
            ]

            email_input = None
            for selector in email_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        email_input = elements[0]
                        self.logger.info(f"✅ Found email input: {selector}")
                        break
                except:
                    continue

            if not email_input:
                self.logger.warning("❌ Could not find email input field")
                return False

            # Enter email
            email_input.clear()
            email_input.send_keys(email)
            time.sleep(1)

            # Look for continue/next button
            continue_selectors = [
                "button:contains('Continue')",
                "button:contains('Next')",
                "button[type='submit']",
                "[data-testid*='continue']"
            ]

            continue_button = None
            for selector in continue_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        continue_button = elements[0]
                        self.logger.info(f"✅ Found continue button: {selector}")
                        break
                except:
                    continue

            if continue_button:
                continue_button.click()
                time.sleep(2)

            # Look for password input
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "input[placeholder*='password']",
                "input[placeholder*='Password']"
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        password_input = elements[0]
                        self.logger.info(f"✅ Found password input: {selector}")
                        break
                except:
                    continue

            if not password_input:
                self.logger.warning("❌ Could not find password input field")
                return False

            # Enter password
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(1)

            # Look for submit/login button
            submit_selectors = [
                "button:contains('Log in')",
                "button:contains('Sign in')",
                "button[type='submit']",
                "[data-testid*='login']"
            ]

            submit_button = None
            for selector in submit_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        submit_button = elements[0]
                        self.logger.info(f"✅ Found submit button: {selector}")
                        break
                except:
                    continue

            if not submit_button:
                # Try pressing Enter on password field
                self.logger.info("⚠️ No submit button found, trying Enter key")
                password_input.send_keys(Keys.RETURN)
            else:
                submit_button.click()

            # Wait for login to complete
            self.logger.info("⏳ Waiting for login to complete...")
            time.sleep(5)

            # Check if login was successful
            if self._is_logged_in():
                self.logger.info("✅ Automated login successful!")
                return True
            else:
                self.logger.warning("❌ Login appeared to complete but interface check failed")
                return False

        except Exception as e:
            self.logger.error(f"❌ Automated login failed: {e}")
            return False

    def _test_element_interactability(self) -> bool:
        """Test if ChatGPT input elements are actually interactable (not just present)."""
        try:
            self.logger.debug("🔍 Testing element interactability...")

            # Find input elements
            input_selectors = [
                "textarea",
                "[contenteditable='true']",
                "[role='textbox']"
            ]

            for selector in input_selectors:
                try:
                    elements = self.driver.find_elements(
                        By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                try:
                                    # Try to send a single character to test interactability
                                    element.send_keys("x")
                                    self.logger.debug(
                                        f"✅ Element {selector} is interactable")
                                    # Clear the test character
                                    element.clear()
                                    return True
                                except Exception as e:
                                    self.logger.debug(
                                        f"⚠️ Element {selector} not interactable: {e}")
                                    continue
                except Exception as e:
                    self.logger.debug(f"⚠️ Error checking {selector}: {e}")

            self.logger.debug("❌ No interactable input elements found")
            return False

        except Exception as e:
            self.logger.debug(f"❌ Element interactability test failed: {e}")
            return False

    def _manual_response_extraction(self) -> str | None:
        """Manual response extraction using the working debug approach."""
        try:
            from selenium.webdriver.common.by import By

            # Use the same selectors and approach as the working debug code
            response_selectors = [
                "[data-message-author-role='assistant']",
                "article",
                ".markdown",
                "[data-message-id]",
                ".agent-turn"
            ]

            for selector in response_selectors:
                try:
                    elements = self.driver.find_elements(
                        By.CSS_SELECTOR, selector)
                    if elements:
                        # Check the last elements (like the debug code does)
                        for elem in elements[-2:]:  # Last 2 elements
                            if elem and elem.is_displayed():
                                text = elem.text.strip() if elem.text else ""
                                if text and len(text) > 10:  # Minimum viable response
                                    self.logger.info(
                                        f"✅ Manual extraction found response with selector '{selector}'")
                                    return text
                except Exception as e:
                    self.logger.debug(
                        f"Manual extraction selector '{selector}' failed: {e}")

            self.logger.warning(
                "❌ Manual response extraction found no valid response text")
            return None

        except Exception as e:
            self.logger.error(f"❌ Manual response extraction error: {e}")
            return None

    def _wait_for_page_ready(self, timeout: float = 15.0) -> bool:
        """Wait for page to be ready for input."""
        try:
            self.logger.debug("⏳ Waiting for page to be ready...")

            # Wait for document ready
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    ready_state = self.driver.execute_script(
                        "return document.readyState")
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
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, selector))
                    )
                    if element:
                        self.logger.debug(
                            f"✅ Page ready - found element: {selector}")
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
                has_loading = any(indicator in body_text.lower()
                                  for indicator in loading_indicators)

                if len(body_text) > 50 and not has_loading and "chatgpt" in page_title.lower():
                    self.logger.debug(
                        "✅ Page appears ready (permissive fallback check)")
                    return True
                elif has_loading:
                    self.logger.debug("⏳ Page still loading...")
                    return False
            except Exception as e:
                self.logger.debug(f"Fallback check failed: {e}")

            self.logger.warning(
                "⚠️ Page readiness check failed - no suitable elements found")
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

            # SIMPLIFIED NAVIGATION: Always use basic ChatGPT to avoid session issues
            target_url = "https://chatgpt.com"  # Use basic ChatGPT to avoid Thea GPT issues
            target_desc = "basic ChatGPT"

            if target_url not in current_url:
                self.logger.info(f"🏗️ Navigating to {target_desc}: {target_url}")
                try:
                    self.driver.get(target_url)
                    # Brief stabilization wait
                    time.sleep(3)
                except Exception as nav_e:
                    self.logger.error(f"❌ Navigation failed: {nav_e}")
                    return None

                new_url = self.driver.current_url
                self.logger.info(f"📍 New URL after navigation: {new_url}")

                # Check if we're on an error/login page
                if any(keyword in new_url.lower() for keyword in ["login", "auth", "error"]):
                    self.logger.warning("⚠️ Navigation resulted in login/error page")
                    return None

                self.logger.info(f"✅ Navigation to {target_desc} completed")
            else:
                self.logger.info(f"✅ Already on {target_desc}")

            # Additional check: ensure page is ready for input even if URL is correct
            if not self._wait_for_page_ready():
                self.logger.error("❌ Page not ready for input")
                return None

            # Additional wait for dynamic content - ChatGPT pages often load elements asynchronously
            self.logger.info(
                "⏳ Waiting additional time for dynamic content...")
            max_dynamic_wait = 15  # seconds - reduced to prevent session timeout
            dynamic_start = time.time()

            # Check session health before starting long wait
            try:
                current_url_check = self.driver.current_url
                self.logger.info(
                    f"🔍 Session health check: URL = {current_url_check}")
            except Exception as e:
                self.logger.error(
                    f"❌ Session became invalid before dynamic wait: {e}")
                return None

            while time.time() - dynamic_start < max_dynamic_wait:
                try:
                    # Check for any input-like elements that might appear dynamically
                    all_inputs = self.driver.find_elements(By.CSS_SELECTOR,
                                                           "textarea, input, [contenteditable], [role='textbox'], [data-testid*='input'], [data-testid*='prompt']")

                    if all_inputs:
                        displayed_inputs = [
                            elem for elem in all_inputs if elem.is_displayed()]
                        if displayed_inputs:
                            self.logger.info(
                                f"✅ Found {len(displayed_inputs)} displayed input elements after dynamic wait")
                            break

                    # Check for buttons too
                    buttons = self.driver.find_elements(
                        By.CSS_SELECTOR, "button, [role='button']")
                    if buttons:
                        displayed_buttons = [
                            btn for btn in buttons if btn.is_displayed()]
                        if displayed_buttons:
                            self.logger.info(
                                f"✅ Found {len(displayed_buttons)} displayed buttons after dynamic wait")
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
                self.logger.info(
                    f"📊 Total elements on page: {len(all_elements)}")

                # Look for form-related elements
                forms = self.driver.find_elements(By.TAG_NAME, "form")
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
                divs = self.driver.find_elements(By.TAG_NAME, "div")

                self.logger.info(
                    f"📋 Forms: {len(forms)}, Buttons: {len(buttons)}, Inputs: {len(inputs)}, Textareas: {len(textareas)}, Divs: {len(divs)}")

                # Check for contenteditable divs specifically
                contenteditable = self.driver.find_elements(
                    By.CSS_SELECTOR, "[contenteditable]")
                self.logger.info(
                    f"📝 Contenteditable elements: {len(contenteditable)}")

                for i, elem in enumerate(contenteditable[:3]):
                    try:
                        text = elem.text[:50] if elem.text else "empty"
                        displayed = elem.is_displayed()
                        enabled = elem.is_enabled()
                        self.logger.info(
                            f"  CE {i+1}: displayed={displayed}, enabled={enabled}, text='{text}'")
                    except Exception as e:
                        self.logger.info(f"  CE {i+1}: error checking - {e}")

                # Check for any data-testid attributes (common in React apps)
                testids = self.driver.find_elements(
                    By.CSS_SELECTOR, "[data-testid]")
                self.logger.info(f"🧪 Data-testid elements: {len(testids)}")

                for i, elem in enumerate(testids[:5]):
                    try:
                        testid = elem.get_attribute("data-testid")
                        tag = elem.tag_name
                        displayed = elem.is_displayed()
                        self.logger.info(
                            f"  TestID {i+1}: {tag}[data-testid='{testid}'] displayed={displayed}")
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
                        candidates = self.driver.find_elements(
                            By.CSS_SELECTOR, selector)
                        if candidates:
                            for candidate in candidates:
                                if candidate.is_displayed() and candidate.is_enabled():
                                    textarea = candidate
                                    self.logger.info(
                                        f"✅ Found input with selector: {selector}")
                                    break
                            if textarea:
                                break
                    except Exception as e:
                        self.logger.debug(f"Selector {selector} failed: {e}")

                if not textarea:
                    self.logger.error(
                        "❌ No suitable input element found after exhaustive search")
                    return None

                self.logger.info("✅ Input element ready for interaction")

            except Exception as e:
                self.logger.error(f"❌ Error debugging page: {e}")
                return None

            # Focus + clear input before sending (prevents hidden focus issues)
            try:
                self.logger.info("🧭 Focusing input element...")
                textarea.click()
                time.sleep(0.2)
                # Clear existing content safely
                from selenium.webdriver.common.keys import Keys
                textarea.send_keys(Keys.CONTROL, "a")
                textarea.send_keys(Keys.BACKSPACE)
                time.sleep(0.2)
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Input focus/clear failed (continuing): {e}")

            # Send message via Selenium (more reliable than PyAutoGUI in server environments)
            self.logger.info(f"📤 ===== SENDING MESSAGE VIA SELENIUM =====")
            self.logger.info(f"📤 Message preview: {message[:50]}...")
            self.logger.info(f"📤 Input element tag: {textarea.tag_name}")
            self.logger.info(
                f"📤 Input element displayed: {textarea.is_displayed()}")
            self.logger.info(
                f"📤 Input element enabled: {textarea.is_enabled()}")

            try:
                # Use Selenium's send_keys on the contenteditable element
                self.logger.info("📤 Step 1: Sending message text...")
                textarea.send_keys(message)
                time.sleep(1)  # Allow text to be entered
                self.logger.info("📤 Step 1 result: Text sent successfully")

                # Try to send Enter - different approaches for different input types
                self.logger.info("📤 Step 2: Attempting to submit message...")
                try:
                    from selenium.webdriver.common.keys import Keys

                    if textarea.tag_name.lower() == 'textarea':
                        self.logger.info(
                            "📤 Step 2: Using textarea - sending ENTER key")
                        textarea.send_keys(Keys.ENTER)
                    else:
                        # For ChatGPT contenteditable, ENTER is typically "send"
                        self.logger.info(
                            "📤 Step 2: Using contenteditable - sending ENTER key")
                        textarea.send_keys(Keys.ENTER)
                        time.sleep(0.5)
                        # Fallback: look for send button
                        try:
                            self.logger.info(
                                "📤 Step 2: Looking for send button...")
                            send_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                                     "button[data-testid*='send'], button[type='submit'], [role='button']")
                            self.logger.info(
                                f"📤 Step 2: Found {len(send_buttons)} potential send buttons")

                            for i, btn in enumerate(send_buttons):
                                if btn.is_displayed() and btn.is_enabled():
                                    btn_text = btn.text or btn.get_attribute(
                                        "aria-label") or f"button-{i}"
                                    self.logger.info(
                                        f"📤 Step 2: Clicking send button: {btn_text}")
                                    btn.click()
                                    self.logger.info(
                                        "✅ Step 2 result: Send button clicked successfully")
                                    break
                        except Exception as e:
                            self.logger.warning(
                                f"📤 Step 2: Send button click failed: {e}")
                            # Last resort: just Enter key
                            self.logger.info(
                                "📤 Step 2: Last resort - sending ENTER key")
                            textarea.send_keys(Keys.ENTER)

                except Exception as e:
                    self.logger.warning(
                        f"Enter key failed, trying send button: {e}")
                    # Look for send button
                    send_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                             "button[data-testid*='send'], button[type='submit'], [role='button']")
                    for btn in send_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            self.logger.info(
                                "✅ Clicked send button as fallback")
                            break

                self.logger.info(
                    "✅ ===== MESSAGE SENT SUCCESSFULLY VIA SELENIUM =====")

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
                        time.sleep(0.5)
                        pyautogui.press("enter")
                        self.logger.info(
                            "✅ Message sent via PyAutoGUI fallback")
                    except Exception as clipboard_error:
                        self.logger.warning(
                            f"⚠️ Clipboard paste failed ({clipboard_error}), falling back to typing...")
                        # Fallback: type the message character by character
                        pyautogui.typewrite(message, interval=0.01)
                        time.sleep(0.5)
                        pyautogui.press("enter")
                        self.logger.info(
                            "✅ Message sent via PyAutoGUI typing fallback")
                except Exception as e2:
                    self.logger.error(
                        f"❌ PyAutoGUI fallback also failed: {e2}")
                    return None
            else:
                return None

            # Wait for response if requested
            if wait_for_response:
                response = self.wait_for_response()
                # If response extraction failed but detector says complete, use working debug approach
                if not response and self.detector:
                    self.logger.info(
                        "🔄 Response detector complete but extraction failed - using manual extraction...")
                    time.sleep(2)  # Give it a moment for text to populate
                    response = self._manual_response_extraction()
                    if response:
                        self.logger.info(
                            "✅ Response extracted using manual approach")
                    else:
                        self.logger.warning(
                            "❌ Manual response extraction also failed")
                return response

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
<<<<<<< HEAD
>>>>>>> rescue/dreamos-down-
=======
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
    from response_detector import ResponseDetector, ResponseWaitResult

    DETECTOR_AVAILABLE = True
except ImportError:
    DETECTOR_AVAILABLE = False

# Thea cookie manager (existing functionality)
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

    def __init__(self, cookie_file: str = "thea_cookies.json", headless: bool = False):
        """Initialize Thea service."""
        super().__init__("TheaService")
        self.cookie_file = Path(cookie_file)
        self.headless = headless
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        self.responses_dir = Path("thea_responses")
        self.responses_dir.mkdir(exist_ok=True)

        self.driver = None
        self.detector = None
        
        # Use existing TheaCookieManager if available
        if COOKIE_MANAGER_AVAILABLE:
            self.cookie_manager = TheaCookieManager(str(cookie_file))
        else:
            self.cookie_manager = None
            self.self.logger.warning("TheaCookieManager not available - using basic cookie handling")

        # Validate dependencies
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium required: pip install selenium")
        if not PYAUTOGUI_AVAILABLE:
            self.self.logger.warning("PyAutoGUI not available - message sending may not work")
        if not UNDETECTED_AVAILABLE:
            self.self.logger.warning("undetected-chromedriver not available - will use standard Chrome (may be detected)")
            self.self.logger.info("💡 Install with: pip install undetected-chromedriver")

    def start_browser(self) -> bool:
        """Initialize browser with cookies using undetected-chromedriver."""
        try:
            self.logger.info("🚀 Starting browser...")

            # Try undetected-chromedriver first (bypasses bot detection)
            if UNDETECTED_AVAILABLE:
                try:
                    self.logger.info("🔐 Using undetected-chromedriver for anti-bot bypass...")
                    
                    options = uc.ChromeOptions()
                    if self.headless:
                        self.logger.warning("⚠️ Headless mode may be detected by anti-bot systems")
                        options.add_argument("--headless=new")
                    
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")
                    options.add_argument("--disable-blink-features=AutomationControlled")

                    self.driver = uc.Chrome(
                        options=options,
                        use_subprocess=True,
                        driver_executable_path=None  # Auto-download correct version
                    )
                    self.logger.info("✅ Undetected Chrome browser started")
                    return True
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Undetected Chrome failed: {e}")
                    self.logger.info("🔄 Falling back to standard Chrome...")

            # Fallback to standard Chrome
            if not SELENIUM_AVAILABLE:
                self.logger.error("❌ Selenium not available")
                return False

            self.logger.info("🚀 Using standard Chrome (may be detected by anti-bot systems)...")
            options = Options()
            if self.headless:
                options.add_argument("--headless=new")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            self.driver = webdriver.Chrome(options=options)
            self.logger.info("✅ Standard Chrome browser started")
            return True

        except Exception as e:
            self.logger.error(f"❌ Browser start failed: {e}")
            return False

    def are_cookies_fresh(self) -> bool:
        """Check if cookies exist and are fresh (not expired). Uses existing TheaCookieManager."""
        if self.cookie_manager:
            # Use existing TheaCookieManager.has_valid_cookies() which already checks expiry
            is_valid = self.cookie_manager.has_valid_cookies()
            if is_valid:
                self.logger.info("✅ Cookies are fresh (validated by TheaCookieManager)")
            else:
                self.logger.warning("⚠️ Cookies are stale or invalid (TheaCookieManager check)")
            return is_valid
        else:
            # Fallback to basic check
            if not self.cookie_file.exists():
                self.logger.info("🍪 No cookie file found")
                return False
            self.logger.warning("⚠️ Using basic cookie check (TheaCookieManager not available)")
            return True  # Assume valid if file exists

    def validate_cookies(self) -> bool:
        """Validate that cookies actually work by testing login."""
        if not self.driver:
            if not self.start_browser():
                return False
        
        try:
            # Navigate to domain first
            self.logger.info("🔍 Validating cookies...")
            self.driver.get("https://chatgpt.com/")
            time.sleep(2)
            
            # Load cookies using TheaCookieManager if available
            if self.cookie_manager:
                self.cookie_manager.load_cookies(self.driver)
            else:
                # Fallback to manual loading
                if self.cookie_file.exists():
                    with open(self.cookie_file) as f:
                        cookies = json.load(f)
                    for cookie in cookies:
                        try:
                            self.driver.add_cookie(cookie)
                        except Exception as e:
                            self.logger.debug(f"Skipped cookie: {e}")
            
            # Navigate to Thea and check login
            self.driver.get(self.thea_url)
            time.sleep(3)
            
            if self._is_logged_in():
                self.logger.info("✅ Cookie validation successful")
                return True
            else:
                self.logger.warning("⚠️ Cookie validation failed - cookies don't work")
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
            # Navigate to Thea
            self.driver.get(self.thea_url)
            time.sleep(3)
            
            # Check if already logged in
            if self._is_logged_in():
                # Save cookies using TheaCookieManager if available
                if self.cookie_manager:
                    self.cookie_manager.save_cookies(self.driver)
                else:
                    # Fallback to manual save
                    cookies = self.driver.get_cookies()
                    self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(self.cookie_file, "w") as f:
                        json.dump(cookies, f, indent=2)
                self.logger.info("✅ Cookies refreshed")
                return True
            
            # Manual login required
            self.logger.info("⚠️ Manual login required to refresh cookies")
            self.logger.info("Please log in to ChatGPT in the browser window...")
            self.logger.info("⏳ Waiting 60 seconds for manual login...")
            time.sleep(60)
            
            if self._is_logged_in():
                # Save cookies using TheaCookieManager if available
                if self.cookie_manager:
                    self.cookie_manager.save_cookies(self.driver)
                else:
                    # Fallback to manual save
                    cookies = self.driver.get_cookies()
                    self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(self.cookie_file, "w") as f:
                        json.dump(cookies, f, indent=2)
                self.logger.info("✅ Cookies refreshed after manual login")
                return True
            
            self.logger.error("❌ Cookie refresh failed")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Cookie refresh error: {e}")
            return False

    def ensure_login(self, force_refresh: bool = False) -> bool:
        """Ensure logged in to Thea Manager with fresh cookies."""
        try:
            if not self.driver:
                if not self.start_browser():
                    return False

            # Check cookie freshness
            if not force_refresh and self.are_cookies_fresh():
                # Validate cookies work
                if self.validate_cookies():
                    self.logger.info("✅ Using fresh, valid cookies")
                    return True
                else:
                    self.logger.warning("⚠️ Cookies are fresh but invalid, refreshing...")
                    force_refresh = True

            # Refresh cookies if needed
            if force_refresh or not self.are_cookies_fresh():
                if not self.refresh_cookies():
                    return False
                
                # Validate after refresh
                if not self.validate_cookies():
                    self.logger.error("❌ Cookies refreshed but validation failed")
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
            if "auth" in current_url or "login" in current_url:
                return False

            # Check for textarea (indicates logged in)
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, "textarea")
                return elem.is_displayed()
            except:
                pass

            return "chatgpt.com" in current_url

        except:
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

            # Send message via PyAutoGUI (proven working method)
            if PYAUTOGUI_AVAILABLE:
                self.logger.info(f"📤 Sending message: {message[:50]}...")
                pyperclip.copy(message)
                time.sleep(0.5)

                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.5)
                pyautogui.press("enter")
                self.logger.info("✅ Message sent")
            else:
                self.logger.error("❌ PyAutoGUI not available")
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
                self.logger.warning("ResponseDetector not available - basic wait")
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
        result = {"success": False, "message": message, "response": "", "file": ""}

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
    cookie_file: str = "thea_cookies.json", headless: bool = False
) -> TheaService:
    """Create Thea service instance."""
    return TheaService(cookie_file, headless)


__all__ = ["TheaService", "create_thea_service"]
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
