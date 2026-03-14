#!/usr/bin/env python3
"""
Test Thea automatic cookie loading and login
"""

from src.services.thea.thea_service import TheaService
import time

def test_auto_login():
    """Test Thea's automatic cookie loading and login."""

    print("🧪 TESTING THEA AUTOMATIC LOGIN")
    print("This will test if Thea can load saved cookies and login automatically")
    print()

    thea = TheaService()

    try:
        print("1️⃣ Starting browser...")
        browser_ok = thea.start_browser()
        print(f"   Browser started: {browser_ok}")

        if not browser_ok:
            print("❌ Browser failed to start")
            return

        print("2️⃣ Checking if cookies are fresh...")
        cookies_fresh = thea.are_cookies_fresh()
        print(f"   Cookies fresh: {cookies_fresh}")

        if cookies_fresh:
            print("3️⃣ Attempting automatic login with saved cookies...")

            # Test the ensure_login method (this loads cookies and validates)
            login_success = thea.ensure_login()
            print(f"   Automatic login result: {login_success}")

            if login_success:
                print("✅ SUCCESS: Thea automatically logged in using saved cookies!")
                print("   No manual intervention required!")

                # Quick test of functionality
                print("4️⃣ Testing basic functionality...")
                current_url = thea.driver.current_url
                logged_in = thea._is_logged_in()
                print(f"   Current URL: {current_url}")
                print(f"   Detected as logged in: {logged_in}")

                if "chatgpt.com" in current_url and logged_in:
                    print("✅ Thea is fully operational with automatic authentication!")
                else:
                    print("⚠️ Login succeeded but some validation checks failed")

            else:
                print("❌ Automatic login failed - cookies may be stale")
                print("💡 Run: python tools/thea_manual_login.py")
                print("   to refresh cookies with manual login")

        else:
            print("❌ No fresh cookies available")
            print("💡 Run: python tools/thea_manual_login.py")
            print("   to capture cookies with manual login")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("5️⃣ Cleaning up...")
        thea.cleanup()
        print("✅ Test complete")

if __name__ == "__main__":
    test_auto_login()