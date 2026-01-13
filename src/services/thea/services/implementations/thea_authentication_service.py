#!/usr/bin/env python3
"""
Thea Authentication Service Implementation - Authentication Business Logic
==========================================================================

<!-- SSOT Domain: thea -->

Service implementation for Thea authentication operations.
Handles login flows, session validation, and cookie management.

V2 Compliance: Business logic service with dependency injection.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

import time
from typing import Optional

from ...domain.models import AuthenticationContext
from ...domain.enums import AuthenticationStatus
from ...repositories.interfaces.i_cookie_repository import ICookieRepository
from ...repositories.interfaces.i_browser_repository import IBrowserRepository
from ..interfaces.i_authentication_service import IAuthenticationService


class TheaAuthenticationService(IAuthenticationService):
    """
    Thea authentication service implementation.

    Handles authentication business logic including:
    - Cookie validation and refresh
    - Login flow orchestration
    - Session state management
    """

    def __init__(self,
                 cookie_repository: ICookieRepository,
                 browser_repository: IBrowserRepository,
                 login_timeout: int = 300):
        """
        Initialize Thea authentication service.

        Args:
            cookie_repository: Repository for cookie operations
            browser_repository: Repository for browser operations
            login_timeout: Timeout for login operations in seconds
        """
        self.cookie_repo = cookie_repository
        self.browser_repo = browser_repository
        self.login_timeout = login_timeout
        self.auth_context = AuthenticationContext(target_url="")

    def ensure_authenticated(self, target_url: str) -> bool:
        """
        Ensure the service is authenticated for the target URL.

        This is the main entry point for authentication. It handles:
        - Checking existing authentication status
        - Refreshing expired credentials
        - Performing login flow if needed

        Args:
            target_url: URL that requires authentication

        Returns:
            True if authenticated and ready, False otherwise
        """
        self.auth_context = AuthenticationContext(target_url=target_url)

        # First, try to validate existing session
        if self.validate_current_session(target_url):
            self.auth_context.record_attempt(success=True)
            return True

        # If validation fails, try to refresh authentication
        if self.refresh_authentication(target_url):
            self.auth_context.record_attempt(success=True)
            return True

        # If refresh fails, perform full login flow
        if self.perform_login_flow(target_url):
            self.auth_context.record_attempt(success=True)
            return True

        # All authentication methods failed
        self.auth_context.record_attempt(success=False, error="All authentication methods failed")
        return False

    def validate_current_session(self, target_url: str) -> bool:
        """
        Validate that the current session is still authenticated using robust patterns from working monolithic version.

        Args:
            target_url: URL to validate authentication for

        Returns:
            True if session is valid, False otherwise
        """
        try:
            print("🔍 Validating current session...")

            # Check if we have valid cookies (secure validation)
            if not self.cookie_repo.has_valid_cookies():
                print("❌ No valid cookies found")
                return False

            # SIMPLIFIED NAVIGATION: Always use basic ChatGPT for validation (from working monolithic)
            chatgpt_main_url = "https://chatgpt.com"
            print(f"🔍 Step 1: Navigating to base domain: {chatgpt_main_url}")
            if not self.browser_repo.navigate_to_url(chatgpt_main_url):
                return False
            time.sleep(3)

            # Load cookies on base domain (critical step from working monolithic)
            cookies = self.cookie_repo.load_cookies()
            if cookies and cookies.cookies:
                print("🍪 Step 2: Loading cookies on base domain...")
                success = self.browser_repo.load_cookies(cookies.cookies)
                if not success:
                    print("⚠️ Step 2 result: Cookie load failed")
                    return False
                print("✅ Step 2 result: Cookies loaded successfully")

                current_cookies = self.browser_repo.get_cookies()
                print(f"🔍 Step 2 result: Browser has {len(current_cookies)} cookies after loading")

            # Refresh to apply cookies
            self.browser_repo.navigate_to_url(chatgpt_main_url)
            time.sleep(2)

            # Now validate on the target URL (Thea GPT or basic ChatGPT)
            print(f"🔍 Step 3: Navigating to target: {target_url}")
            if target_url != chatgpt_main_url:
                if not self.browser_repo.navigate_to_url(target_url):
                    print("⚠️ Target navigation failed, trying basic ChatGPT fallback")
                    target_url = chatgpt_main_url  # Fallback to basic ChatGPT

            # Check if Thea GPT loads properly (from working monolithic)
            current_url = self.browser_repo.get_current_url()
            page_title = self.browser_repo.get_page_title()
            print(f"📍 Step 4 result: Current URL = {current_url}")
            print(f"📍 Step 4 result: Page title = '{page_title}'")

            # If redirected to login/auth page, cookies failed
            if "login" in (current_url or "").lower() or "auth" in (current_url or "").lower():
                print("⚠️ Redirected to login page - cookies invalid")
                return False

            # Check if page loads properly with comprehensive checks (from working monolithic)
            print("🔍 Step 5: Checking if interface loaded...")
            login_result = self._is_logged_in()
            print(f"🔍 Step 5 result: Interface check = {login_result}")

            if login_result:
                # CRITICAL: Check if elements are actually interactable (from working monolithic)
                print("🔍 Step 6: Testing element interactability...")
                interactable_result = self.browser_repo.test_element_interactability()
                print(f"🔍 Step 6 result: Elements interactable = {interactable_result}")

                if interactable_result:
                    print("✅ ===== SESSION VALIDATION SUCCESSFUL =====")
                    return True
                else:
                    print("⚠️ Elements exist but not interactable - likely stale cookies")
                    return False
            else:
                print("⚠️ ===== SESSION VALIDATION FAILED - NOT LOGGED IN =====")
                return False

        except Exception as e:
            print(f"❌ ===== SESSION VALIDATION ERROR: {e} =====")
            return False

    def _is_logged_in(self) -> bool:
        """
        Check if logged in by verifying page has proper ChatGPT interface (from working monolithic version).
        """
        try:
            current_url = self.browser_repo.get_current_url()
            page_title = self.browser_repo.get_page_title()

            # Check for obvious login/auth pages
            if "auth" in (current_url or "").lower() or "login" in (current_url or "").lower():
                return False

            # Check if we're on ChatGPT domain
            if "chatgpt.com" not in (current_url or ""):
                return False

            # Check page title - should be "ChatGPT" or contain GPT info
            if not page_title or "chatgpt" not in page_title.lower():
                return False

            # Check for ChatGPT-specific elements that indicate proper login
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
                    elements = self.browser_repo.execute_script(f"return document.querySelectorAll('{indicator}').length")
                    if elements and elements > 0:
                        found_indicators += 1
                except:
                    pass

            # Require at least 2 different types of indicators for a valid page
            if found_indicators >= 2:
                return True

            return False

        except Exception as e:
            print(f"🔍 Login check error: {e}")
            return False

    def refresh_authentication(self, target_url: str) -> bool:
        """
        Force refresh of authentication credentials using manual login approach from working monolithic version.

        Args:
            target_url: URL to refresh authentication for

        Returns:
            True if refresh successful, False otherwise
        """
        print("🔄 Refreshing cookies...")

        if not self.browser_repo.is_browser_operational():
            if not self.browser_repo.start_browser():
                return False

        try:
            # Navigate to main ChatGPT site first (from working monolithic)
            chatgpt_main_url = "https://chatgpt.com"
            print(f"🏠 Going to main ChatGPT site: {chatgpt_main_url}")
            if not self.browser_repo.navigate_to_url(chatgpt_main_url):
                return False
            time.sleep(3)

            # Load existing cookies if available
            cookies = self.cookie_repo.load_cookies()
            if cookies and cookies.cookies:
                self.browser_repo.load_cookies(cookies.cookies)

            # Check if already logged in (comprehensive check from working monolithic)
            if self._is_logged_in():
                # CRITICAL: Check if elements are actually interactable
                if self.browser_repo.test_element_interactability():
                    # Save cookies using secure cookie manager
                    current_cookies = self.browser_repo.get_cookies()
                    if current_cookies:
                        from ...domain.models import CookieData
                        cookie_data = CookieData(
                            cookies=current_cookies,
                            domain="chatgpt.com"
                        )
                        self.cookie_repo.save_cookies(cookie_data)
                        print("✅ Cookies refreshed securely" if self.cookie_repo.__class__.__name__ == 'SecureCookieRepository' else "✅ Cookies refreshed (legacy)")
                        return True
                else:
                    print("⚠️ Elements not interactable despite login check - continuing to manual login")

            # Manual login required - guide user through the process (from working monolithic)
            print("🔐 ===== MANUAL LOGIN REQUIRED =====")
            print("📋 INSTRUCTIONS:")
            print("   1. Browser window should be open with ChatGPT")
            print("   2. Click 'Log in' or 'Sign in' button")
            print("   3. Complete login process (email/password or Google/Apple)")
            print("   4. Wait for ChatGPT interface to load fully")
            print("   5. Return to this terminal when ready")
            print("")
            print("⏳ Waiting for you to complete login... (press Enter when done)")

            # Wait for user input instead of fixed timeout
            try:
                input("Press Enter when login is complete...")
                print("✅ User indicated login is complete")
            except KeyboardInterrupt:
                print("⏹️ Login process interrupted by user")
                return False

            # Give page time to fully load after login
            print("⏳ Allowing time for page to stabilize after login...")
            time.sleep(5)

            # Verify login was successful with comprehensive checks
            print("🔍 Verifying login success...")

            # Check 1: Basic login detection
            login_check = self._is_logged_in()
            print(f"   Basic login check: {login_check}")

            if not login_check:
                print("❌ Basic login check failed")
                return False

            # Check 2: Element interactability (critical for stale cookie detection)
            interactable_check = self.browser_repo.test_element_interactability()
            print(f"   Element interactability check: {interactable_check}")

            if not interactable_check:
                print("❌ Elements not interactable - login may have failed")
                print("💡 Try logging in again, or check if ChatGPT is blocking automation")
                return False

            # Check 3: Ensure we're on the right page
            current_url = self.browser_repo.get_current_url()
            if "chatgpt.com" not in (current_url or ""):
                print(f"❌ Not on ChatGPT page: {current_url}")
                return False

            print("✅ All login verification checks passed")

            # Save cookies using secure cookie manager
            current_cookies = self.browser_repo.get_cookies()
            if current_cookies:
                from ...domain.models import CookieData
                cookie_data = CookieData(
                    cookies=current_cookies,
                    domain="chatgpt.com"
                )
                success = self.cookie_repo.save_cookies(cookie_data)
                if success:
                    print("✅ Cookies saved securely after manual login" if self.cookie_repo.__class__.__name__ == 'SecureCookieRepository' else "✅ Cookies saved after manual login (legacy)")
                    print("🎉 ===== LOGIN PROCESS COMPLETE =====")
                    return True
                else:
                    print("❌ Cookie save failed after manual login - secure storage required")
                    return False
            else:
                print("❌ No cookies to save after manual login")
                return False

        except Exception as e:
            print(f"❌ Cookie refresh error: {e}")
            return False

    def perform_login_flow(self, target_url: str) -> bool:
        """
        Perform the complete login flow for authentication.

        Args:
            target_url: URL to authenticate with

        Returns:
            True if login successful, False otherwise
        """
        try:
            print("🚀 Performing login flow...")

            # Navigate to main ChatGPT site
            main_url = "https://chatgpt.com"
            if not self.browser_repo.navigate_to_url(main_url):
                return False

            # Load any existing cookies first
            cookies = self.cookie_repo.load_cookies()
            if cookies:
                self.browser_repo.load_cookies(cookies.cookies)

            # Check if login was successful with cookies
            if self.validate_current_session(main_url):
                print("✅ Login successful using existing cookies")
                return True

            # Manual login required
            return self._perform_manual_login(main_url)

        except Exception as e:
            print(f"❌ Login flow failed: {e}")
            return False

    def _perform_manual_login(self, login_url: str) -> bool:
        """
        Perform manual login flow.

        Args:
            login_url: URL to login to

        Returns:
            True if manual login successful, False otherwise
        """
        try:
            print("👤 Manual login required")
            print(f"Please log in to ChatGPT at: {login_url}")
            print(f"You have {self.login_timeout} seconds to complete login...")

            start_time = time.time()
            while time.time() - start_time < self.login_timeout:
                # Check every few seconds if login was successful
                if self.validate_current_session(login_url):
                    # Save the session cookies
                    current_cookies = self.browser_repo.get_cookies()
                    if current_cookies:
                        from ...domain.models import CookieData
                        cookie_data = CookieData(
                            cookies=current_cookies,
                            domain="chatgpt.com"
                        )
                        self.cookie_repo.save_cookies(cookie_data)

                    print("✅ Manual login successful!")
                    return True

                time.sleep(3)  # Check every 3 seconds

            print("⏰ Manual login timeout - authentication failed")
            return False

        except Exception as e:
            print(f"❌ Manual login failed: {e}")
            return False

    def get_authentication_context(self) -> AuthenticationContext:
        """Get current authentication context and status."""
        return self.auth_context

    def is_authenticated(self) -> bool:
        """Quick check if currently authenticated."""
        return self.auth_context.current_status == AuthenticationStatus.AUTHENTICATED

    def logout(self) -> bool:
        """
        Perform logout and cleanup authentication state.

        Returns:
            True if logout successful, False otherwise
        """
        try:
            # Clear cookies
            self.cookie_repo.delete_cookies()

            # Reset authentication context
            self.auth_context = AuthenticationContext(target_url="")

            print("👋 Logout completed")
            return True

        except Exception as e:
            print(f"❌ Logout failed: {e}")
            return False