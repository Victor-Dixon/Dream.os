"""
Robinhood Authentication Module
==============================

V2 Compliant: Yes (<100 lines)
Single Responsibility: Authentication and session management

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import os
import logging
from datetime import datetime
from typing import Optional

import robin_stocks.robinhood as rs
import pyotp

from ...core.config.config_manager import UnifiedConfigManager


class RobinhoodAuthenticator:
    """
    V2 Compliant Authentication Module

    Handles all Robinhood authentication logic including:
    - Credential validation
    - TOTP generation
    - Login/logout operations
    - Session management
    - Error handling
    """

    def __init__(self, config_manager: Optional[UnifiedConfigManager] = None):
        self.config_manager = config_manager or UnifiedConfigManager()
        self.logger = logging.getLogger("RobinhoodAuthenticator")

        # Authentication state
        self.is_authenticated = False
        self.last_auth_time: Optional[datetime] = None
        self.username = os.getenv("ROBINHOOD_USERNAME", "").strip()
        self.password = os.getenv("ROBINHOOD_PASSWORD", "").strip()
        self.totp_secret = os.getenv("ROBINHOOD_TOTP_SECRET", "").strip()

    def validate_credentials(self) -> bool:
        """Validate credentials before authentication attempt."""
        if not all([self.username, self.password]):
            self.logger.error("❌ MISSING CREDENTIALS")
            self.logger.error("💡 REQUIRED: ROBINHOOD_USERNAME and ROBINHOOD_PASSWORD")
            return False

        if not self.username or not self.password:
            self.logger.error("❌ EMPTY CREDENTIALS: Username/password cannot be empty")
            return False

        if len(self.username) < 3 or len(self.password) < 6:
            self.logger.error("❌ INVALID CREDENTIALS: Check username/password format")
            return False

        self.logger.info(f"✅ Credentials validated for user: {self.username[:3]}***")
        return True

    def generate_totp(self) -> Optional[str]:
        """Generate TOTP token if secret is available."""
        if not self.totp_secret:
            return None

        try:
            totp = pyotp.TOTP(self.totp_secret.strip())
            token = totp.now()
            self.logger.info("✅ TOTP code generated for automatic 2FA")
            return token
        except Exception as e:
            self.logger.error(f"❌ TOTP generation failed: {e}")
            return None

    def authenticate(self, max_retries: int = 1) -> bool:
        """
        Authenticate with Robinhood API.

        Args:
            max_retries: Maximum authentication attempts

        Returns:
            bool: True if authentication successful
        """
        if not self.validate_credentials():
            return False

        mfa_code = self.generate_totp()

        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"🔄 RETRY ATTEMPT {attempt}/{max_retries}")
                    import time
                    wait_time = min(30 * attempt, 300)
                    self.logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)

                self.logger.info(f"Authenticating as {self.username}")

                login_result = rs.login(
                    username=self.username,
                    password=self.password,
                    mfa_code=mfa_code,
                    store_session=False
                )

                if login_result:
                    self.is_authenticated = True
                    self.last_auth_time = datetime.now()
                    self.logger.info("✅ Successfully authenticated with Robinhood")
                    return True
                else:
                    self.logger.error("❌ Robinhood authentication failed - check credentials")
                    if attempt < max_retries:
                        continue
                    return False

            except Exception as auth_error:
                error_msg = str(auth_error).lower()

                if ("rate limit" in error_msg or "429" in error_msg):
                    self.logger.warning("⏱️ RATE LIMITED by Robinhood - authentication blocked")
                    self.logger.warning("💡 SOLUTION: Wait 15-30 minutes before trying again")
                    return False

                elif ("challenge" in error_msg or "verification" in error_msg):
                    return self._handle_manual_2fa()

                elif ("invalid" in error_msg and "credentials" in error_msg):
                    self.logger.error("💡 CHECK: Verify ROBINHOOD_USERNAME and ROBINHOOD_PASSWORD")
                    return False

                else:
                    self.logger.error(f"❌ AUTHENTICATION ERROR: {auth_error}")
                    if attempt < max_retries:
                        continue
                    return False

        return False

    def _handle_manual_2fa(self) -> bool:
        """Handle manual 2FA approval workflow."""
        print("\n🔐 ROBINHOOD REQUIRES MANUAL 2FA APPROVAL:")
        print("=" * 60)
        print("📱 STEP-BY-STEP INSTRUCTIONS:")
        print("   1. Open Robinhood APP on your phone RIGHT NOW")
        print("   2. Look for 'Device Approval' or 'Login Request' notification")
        print("   3. TAP 'APPROVE' or 'ALLOW' immediately")
        print("   4. Return here and wait for confirmation")
        print("⏳ IMPORTANT: Act quickly - approval window is limited!")
        print("=" * 60)

        try:
            import sys
            if not sys.stdin.isatty():
                raise EOFError("Non-interactive environment detected")

            input("   ✅ Press Enter AFTER approving in the Robinhood app: ")
            print("   🔄 Checking authentication status...")

            import time
            time.sleep(5)

            test_data = rs.account.get_account()
            if test_data and 'cash' in test_data:
                self.is_authenticated = True
                self.last_auth_time = datetime.now()
                print("   ✅ SUCCESS! Authentication approved and verified!")
                return True
            else:
                print("   ❌ VERIFICATION FAILED: Account data incomplete")
                return False

        except (KeyboardInterrupt, EOFError):
            print("   ❌ CANCELLED: Interactive approval not available")
            print("   💡 SOLUTION: Run in interactive terminal or set up TOTP")
            return False
        except Exception as e:
            print(f"   ❌ AUTHENTICATION FAILED: {e}")
            return False

    def logout(self) -> None:
        """Logout from Robinhood."""
        try:
            rs.logout()
            self.is_authenticated = False
            self.logger.info("✅ Logged out from Robinhood")
        except Exception as e:
            self.logger.error(f"Logout error: {e}")

    def is_session_valid(self) -> bool:
        """Check if current session is still valid."""
        if not self.is_authenticated:
            return False

        try:
            test_data = rs.account.get_account()
            return test_data is not None and 'cash' in test_data
        except Exception:
            self.is_authenticated = False
            return False