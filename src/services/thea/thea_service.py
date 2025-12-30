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
