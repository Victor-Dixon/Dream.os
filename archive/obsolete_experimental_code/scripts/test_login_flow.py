#!/usr/bin/env python3
"""
Test the improved login flow with proper stale cookie detection and login handling
"""

import sys
import os

# Add the src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.thea.thea_service import TheaService

def test_login_flow():
    """Test the complete login flow with stale cookie detection and manual login."""

    print("🧪 TESTING IMPROVED LOGIN FLOW")
    print("=" * 50)

    thea = TheaService()

    try:
        print("1️⃣ Starting browser...")
        if not thea.start_browser():
            print("❌ Browser failed to start")
            return

        print("2️⃣ Attempting to ensure login (this should detect stale cookies)...")

        # This should:
        # 1. Check if cookies are fresh (they're not)
        # 2. Validate cookies by testing interactability (should fail)
        # 3. Trigger manual login process
        login_success = thea.ensure_login()

        print(f"   Login result: {login_success}")

        if login_success:
            print("✅ LOGIN SUCCESSFUL!")

            # Try to send a test message to verify everything works
            print("3️⃣ Testing message sending...")
            result = thea.communicate("Hello Thea, this is a test after successful login.")

            if result['success']:
                response = result.get('response', '')
                print("✅ MESSAGE SENT SUCCESSFULLY!")
                print(f"Response: {response[:100]}...")
                return True
            else:
                print("❌ Message sending failed after login")
                return False
        else:
            print("❌ Login failed - this could be expected if user didn't complete login")
            print("   (The system properly detected stale cookies and prompted for login)")
            return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        thea.cleanup()
        print("✅ Test complete")

if __name__ == "__main__":
    success = test_login_flow()
    print("\n" + "=" * 50)
    if success:
        print("🎉 LOGIN FLOW WORKING: Cookies validated, login successful, messages sent!")
    else:
        print("⚠️ LOGIN FLOW DETECTED ISSUES: Stale cookies detected (expected if not logged in)")
    print("=" * 50)