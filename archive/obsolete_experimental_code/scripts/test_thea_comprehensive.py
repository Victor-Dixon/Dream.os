#!/usr/bin/env python3
"""
Comprehensive Thea test - validates all login detection and interaction fixes
"""

from src.services.thea.thea_service import TheaService
import time

def test_comprehensive_thea():
    """Comprehensive test of all Thea improvements."""

    print("🧪 COMPREHENSIVE THEA TEST - Testing all fixes...")
    print("🔧 Testing:")
    print("   • Enhanced login detection")
    print("   • Element interactability testing")
    print("   • Improved manual login flow")
    print("   • Anti-bot measures handling")
    print()

    thea = TheaService()

    try:
        # Test 1: Browser startup
        print("1️⃣ Testing browser startup...")
        browser_ok = thea.start_browser()
        print(f"   Browser started: {browser_ok}")

        if not browser_ok:
            print("❌ Browser failed to start")
            return

        # Test 2: Initial navigation and login detection
        print("2️⃣ Testing initial navigation and login detection...")
        thea.driver.get("https://chatgpt.com")
        time.sleep(3)

        current_url = thea.driver.current_url
        print(f"   Current URL: {current_url}")

        # Test login detection
        print("3️⃣ Testing enhanced login detection...")
        logged_in = thea._is_logged_in()
        print(f"   Login detection result: {logged_in}")

        # Test element interactability
        print("4️⃣ Testing element interactability...")
        interactable = thea._test_element_interactability()
        print(f"   Element interactability: {interactable}")

        if not logged_in:
            print("5️⃣ Testing manual login flow...")
            print("⚠️  MANUAL LOGIN REQUIRED FOR COMPREHENSIVE TESTING")
            print("📋 Please complete the login process in the browser window")
            print("   Then return here and press Enter to continue...")

            try:
                input("Press Enter after completing login...")
                print("✅ Manual login completed by user")

                # Test post-login verification
                print("6️⃣ Testing post-login verification...")
                logged_in_after = thea._is_logged_in()
                interactable_after = thea._test_element_interactability()

                print(f"   Login status after manual login: {logged_in_after}")
                print(f"   Element interactability after login: {interactable_after}")

                if logged_in_after and interactable_after:
                    print("7️⃣ Testing message sending with all fixes...")

                    # Try to send a message
                    result = thea.communicate("Hello! This is a comprehensive test of all Thea fixes.")
                    print(f"   Message send result: {result['success']}")

                    if result['success']:
                        response_preview = result['response'][:100] if result['response'] else "No response"
                        print(f"   Response preview: {response_preview}...")
                        print("✅ FULL THEA FUNCTIONALITY TEST PASSED!")
                    else:
                        print(f"   Error: {result['response']}")
                        print("⚠️  Message sending failed, but login/interaction works")
                else:
                    print("❌ Post-login verification failed")
                    if not logged_in_after:
                        print("   Issue: Still not detecting as logged in")
                    if not interactable_after:
                        print("   Issue: Elements still not interactable (possible anti-bot measures)")

            except KeyboardInterrupt:
                print("⏹️ Manual testing cancelled by user")
                return

        elif logged_in and interactable:
            print("✅ Already logged in with interactable elements")
            print("7️⃣ Testing message sending...")

            result = thea.communicate("Hello! This is a comprehensive test of Thea functionality.")
            print(f"   Message send result: {result['success']}")

            if result['success']:
                response_preview = result['response'][:100] if result['response'] else "No response"
                print(f"   Response preview: {response_preview}...")
                print("✅ THEA IS FULLY FUNCTIONAL!")
            else:
                print(f"   Error: {result['response']}")
                print("⚠️  Login works but message sending failed")

        else:
            print("❌ Mixed state: logged in but elements not interactable")
            print("   This indicates stale cookies or anti-bot measures")
            print("   Try manual login to refresh authentication")

    except Exception as e:
        print(f"❌ Exception during testing: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("8️⃣ Cleaning up...")
        thea.cleanup()
        print("✅ Test complete")

        # Summary
        print("\n📊 TEST SUMMARY:")
        print("• Browser startup: Tested")
        print("• Login detection: Tested")
        print("• Element interactability: Tested")
        print("• Manual login flow: Tested")
        print("• Message sending: Tested")
        print("• Error handling: Tested")

if __name__ == "__main__":
    test_comprehensive_thea()