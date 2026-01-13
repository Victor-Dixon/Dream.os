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
        Validate that the current session is still authenticated.

        Args:
            target_url: URL to validate authentication for

        Returns:
            True if session is valid, False otherwise
        """
        try:
            # Check if we have valid cookies
            if not self.cookie_repo.has_valid_cookies():
                return False

            # Navigate to the target URL
            if not self.browser_repo.navigate_to_url(target_url):
                return False

            # Wait for page to be ready
            if not self.browser_repo.is_page_ready():
                time.sleep(3)  # Give it a moment
                if not self.browser_repo.is_page_ready():
                    return False

            # Check if we're still on a login/auth page
            current_url = self.browser_repo.get_current_url()
            if current_url and any(auth_indicator in current_url.lower()
                                 for auth_indicator in ['login', 'auth', 'signin']):
                return False

            # Check for authentication indicators on the page
            page_title = self.browser_repo.get_page_title()
            if page_title and 'chatgpt' in page_title.lower():
                return True

            # Check for presence of chat interface elements
            input_element = self.browser_repo.find_input_element('textarea')
            if input_element:
                return True

            return False

        except Exception as e:
            print(f"❌ Session validation failed: {e}")
            return False

    def refresh_authentication(self, target_url: str) -> bool:
        """
        Force refresh of authentication credentials.

        Args:
            target_url: URL to refresh authentication for

        Returns:
            True if refresh successful, False otherwise
        """
        try:
            print("🔄 Refreshing authentication...")

            # Navigate to main ChatGPT site first
            main_url = "https://chatgpt.com"
            if not self.browser_repo.navigate_to_url(main_url):
                return False

            # Load cookies if available
            cookies = self.cookie_repo.load_cookies()
            if cookies:
                self.browser_repo.load_cookies(cookies.cookies)

            # Check if we're already logged in
            if self.validate_current_session(main_url):
                # Save the current session cookies
                current_cookies = self.browser_repo.get_cookies()
                if current_cookies:
                    from ...domain.models import CookieData
                    cookie_data = CookieData(
                        cookies=current_cookies,
                        domain="chatgpt.com"
                    )
                    self.cookie_repo.save_cookies(cookie_data)

                print("✅ Authentication refreshed with existing session")
                return True

            # If not logged in, we need manual login
            print("⚠️ Manual login required to refresh authentication")
            return self._perform_manual_login(main_url)

        except Exception as e:
            print(f"❌ Authentication refresh failed: {e}")
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