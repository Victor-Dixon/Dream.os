#!/usr/bin/env python3
"""
Simple Thea test - minimal approach to see what actually works
"""

from src.services.thea.thea_service import TheaService
import time

def test_simple_thea():
    """Test Thea with the simplest possible approach."""

    print("🧪 SIMPLE THEA TEST - Let's see what actually works...")

    thea = TheaService()

    try:
        # Step 1: Just start browser and go to ChatGPT
        print("1️⃣ Starting browser...")
        browser_ok = thea.start_browser()
        print(f"   Browser started: {browser_ok}")

        if not browser_ok:
            print("❌ Browser failed to start")
            return

        # Step 2: Go directly to ChatGPT (skip complex validation)
        print("2️⃣ Going to ChatGPT...")
        thea.driver.get("https://chatgpt.com")
        time.sleep(5)

        current_url = thea.driver.current_url
        print(f"   Current URL: {current_url}")

        # Step 3: Check if we're logged in (simple check)
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
            # Step 4: Try to send a simple message
            print("4️⃣ Sending test message...")
            result = thea.communicate("Hello! This is a simple test.")
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
    test_simple_thea()