#!/usr/bin/env python3
"""
Test stale cookie detection - see if we properly detect when cookies are invalid
"""

import sys
import os

# Add the src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import only what we need, avoid the broken modular imports
from src.services.thea.thea_service import TheaService

def test_stale_cookie_detection():
    """Test if Thea properly detects stale cookies."""

    print("🧪 TESTING STALE COOKIE DETECTION")

    thea = TheaService()

    try:
        # Start browser
        print("1️⃣ Starting browser...")
        if not thea.start_browser():
            print("❌ Browser failed to start")
            return

        # Test cookie validation (this should detect stale cookies)
        print("2️⃣ Testing cookie validation...")
        validation_result = thea.validate_cookies()
        print(f"   Validation result: {validation_result}")

        if not validation_result:
            print("✅ CORRECTLY DETECTED STALE COOKIES!")
            print("   This means the validation is working - cookies exist but are not functional")
        else:
            print("❌ INCORRECTLY PASSED VALIDATION")
            print("   This means stale cookie detection is not working")

        # Test ensure_login (should also fail)
        print("3️⃣ Testing ensure_login...")
        login_result = thea.ensure_login()
        print(f"   Login result: {login_result}")

        if not login_result:
            print("✅ CORRECTLY FAILED TO LOGIN")
        else:
            print("❌ UNEXPECTEDLY SUCCEEDED AT LOGIN")

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

    finally:
        thea.cleanup()
        print("✅ Test complete")

if __name__ == "__main__":
    test_stale_cookie_detection()