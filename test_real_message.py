#!/usr/bin/env python3
"""
Test sending an actual message to see if Thea works end-to-end
"""

import sys
import os

# Add the src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.thea.thea_service import TheaService

def test_real_message():
    """Test sending a real message to see if everything works."""

    print("🧪 TESTING REAL MESSAGE SENDING")

    thea = TheaService()

    try:
        print("1️⃣ Starting browser...")
        if not thea.start_browser():
            print("❌ Browser failed to start")
            return

        print("2️⃣ Ensuring login...")
        login_success = thea.ensure_login()
        print(f"   Login success: {login_success}")

        if login_success:
            print("3️⃣ Sending real message...")
            message = "Hello Thea, this is a comprehensive test. Please respond with a brief acknowledgment."

            result = thea.communicate(message)
            print(f"   Communication success: {result['success']}")

            if result['success']:
                response = result.get('response', '')
                print("✅ MESSAGE SUCCESSFUL!")
                print(f"Response length: {len(response)}")
                print(f"Response preview: {response[:200]}...")
                return True
            else:
                error = result.get('response', 'Unknown error')
                print(f"❌ MESSAGE FAILED: {error}")
                return False
        else:
            print("❌ Login failed")
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
    success = test_real_message()
    if success:
        print("\n🎉 THEA IS WORKING! Cookies are valid and messages can be sent.")
    else:
        print("\n❌ THEA IS NOT WORKING - stale cookies or other issues.")