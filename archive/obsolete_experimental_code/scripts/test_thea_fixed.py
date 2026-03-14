#!/usr/bin/env python3
"""
Fixed Thea test - addresses anti-bot measures and element interaction issues
"""

from src.services.thea.thea_service import TheaService
import time

def test_fixed_thea():
    """Test Thea with fixes for anti-bot measures and element interaction."""

    print("🛠️ FIXED THEA TEST - Testing anti-bot fixes...")
    print("🔧 Fixes applied:")
    print("   • Simplified navigation (basic ChatGPT only)")
    print("   • Enhanced element readiness checks")
    print("   • Manual fallback for automation failures")
    print()

    thea = TheaService()

    try:
        # Step 1: Start browser
        print("1️⃣ Starting browser...")
        browser_ok = thea.start_browser()
        print(f"   Browser started: {browser_ok}")

        if not browser_ok:
            print("❌ Browser failed to start")
            return

        # Step 2: Navigate to ChatGPT
        print("2️⃣ Navigating to ChatGPT...")
        thea.driver.get("https://chatgpt.com")
        time.sleep(3)

        current_url = thea.driver.current_url
        print(f"   Current URL: {current_url}")

        # Step 3: Check login status
        print("3️⃣ Checking login status...")
        logged_in = thea._is_logged_in()
        print(f"   Logged in: {logged_in}")

        if not logged_in:
            print("❌ Not logged in - manual login required")
            print("   Please log in to ChatGPT in the browser window...")
            print("   Press Enter when ready...")
            input()
            logged_in = thea._is_logged_in()
            print(f"   After manual login: {logged_in}")

        if logged_in:
            # Step 4: Try to send a message (with improved error handling)
            print("4️⃣ Attempting to send test message...")

            # First, let user manually interact to bypass anti-bot
            print("💡 ANTI-BOT PREVENTION: Please manually click in the ChatGPT input area first")
            print("   This helps bypass ChatGPT's automation detection")
            input("Press Enter after clicking in the input area...")

            result = thea.communicate("Hello! This is a test with anti-bot fixes.")
            print(f"   Success: {result['success']}")
            if result['success']:
                response_preview = result['response'][:100] if result['response'] else "No response"
                print(f"   Response: {response_preview}...")
            else:
                print(f"   Error: {result['response']}")
        else:
            print("❌ Still not logged in after manual attempt")

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("5️⃣ Cleaning up...")
        thea.cleanup()
        print("✅ Test complete")

if __name__ == "__main__":
    test_fixed_thea()