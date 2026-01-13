#!/usr/bin/env python3
"""
Test Automated Thea Login
========================

Tests the new automated login functionality for Thea.
"""

from src.services.thea.thea_service import TheaService
import time

def test_automated_login():
    """Test the automated login functionality."""
    print("🤖 Testing Automated Thea Login")
    print("=" * 40)

    thea = TheaService()

    try:
        # Start browser
        print("1️⃣ Starting browser...")
        if not thea.start_browser():
            print("❌ Failed to start browser")
            return False

        # Navigate to ChatGPT
        print("2️⃣ Navigating to ChatGPT...")
        thea.driver.get("https://chatgpt.com")
        time.sleep(3)

        # Check current login status
        print("3️⃣ Checking login status...")
        logged_in = thea._is_logged_in()
        print(f"   Currently logged in: {logged_in}")

        if logged_in:
            print("✅ Already logged in!")
            return True

        # Attempt automated login
        print("4️⃣ Attempting automated login...")
        login_success = thea._attempt_automated_login()

        if login_success:
            print("✅ Automated login successful!")
            return True
        else:
            print("❌ Automated login failed")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        if hasattr(thea, 'driver') and thea.driver:
            thea.driver.quit()

if __name__ == "__main__":
    success = test_automated_login()
    print("\n" + "=" * 40)
    if success:
        print("🎉 Automated login test PASSED!")
    else:
        print("❌ Automated login test FAILED!")
    print("=" * 40)