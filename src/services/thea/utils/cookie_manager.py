#!/usr/bin/env python3
"""
Cookie Manager Utility - V2 Compliance
======================================

Utility class for managing cookies in Thea service.

V2 Compliance: <400 lines, modular design
Author: Agent-7 (Modularization)
<!-- SSOT Domain: integration -->
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    from selenium import webdriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class CookieManager:
    """Manages cookie operations for Thea service."""

    def __init__(self, cookie_file: str = "thea_cookies.enc", key_file: str = "thea_key.bin"):
        """Initialize cookie manager."""
        self.cookie_file = Path(cookie_file)
        self.key_file = Path(key_file)

    def are_cookies_fresh(self) -> bool:
        """Check if cookies are fresh (less than 24 hours old)."""
        try:
            if not self.cookie_file.exists():
                return False

            # Check file modification time
            mtime = datetime.fromtimestamp(self.cookie_file.stat().st_mtime)
            age = datetime.now() - mtime

            return age < timedelta(hours=24)
        except Exception:
            return False

    def validate_cookies(self) -> bool:
        """Validate that cookies exist and are readable."""
        try:
            if not self.cookie_file.exists():
                print(f"❌ Cookie file not found: {self.cookie_file}")
                return False

            # Try to read and parse cookies
            with open(self.cookie_file, 'r') as f:
                cookies = json.load(f)

            if not isinstance(cookies, list) or len(cookies) == 0:
                print("❌ Invalid or empty cookie data")
                return False

            # Check for essential cookies
            has_session = any(c.get('name', '').lower() in ['session', 'sessionid'] for c in cookies)
            has_auth = any('auth' in c.get('name', '').lower() for c in cookies)

            if not (has_session or has_auth):
                print("⚠️ No session or auth cookies found")
                return False

            print(f"✅ Cookies validated ({len(cookies)} cookies)")
            return True

        except json.JSONDecodeError:
            print("❌ Invalid JSON in cookie file")
            return False
        except Exception as e:
            print(f"❌ Cookie validation failed: {e}")
            return False

    def load_cookies(self, driver: webdriver.Chrome) -> bool:
        """Load cookies into the browser."""
        try:
            with open(self.cookie_file, 'r') as f:
                cookies = json.load(f)

            for cookie in cookies:
                try:
                    # Ensure cookie has required fields
                    if 'name' in cookie and 'value' in cookie:
                        driver.add_cookie(cookie)
                except Exception as e:
                    print(f"⚠️ Failed to add cookie {cookie.get('name', 'unknown')}: {e}")

            print(f"✅ Loaded {len(cookies)} cookies")
            return True

        except Exception as e:
            print(f"❌ Failed to load cookies: {e}")
            return False

    def save_cookies(self, driver: webdriver.Chrome) -> bool:
        """Save cookies from the browser."""
        try:
            cookies = driver.get_cookies()

            with open(self.cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)

            print(f"✅ Saved {len(cookies)} cookies")
            return True

        except Exception as e:
            print(f"❌ Failed to save cookies: {e}")
            return False

    def refresh_cookies(self) -> bool:
        """Refresh cookies by re-authenticating."""
        # This would need to be implemented with specific authentication logic
        # For now, just mark as needing manual intervention
        print("🔄 Cookie refresh required - manual authentication needed")
        return False