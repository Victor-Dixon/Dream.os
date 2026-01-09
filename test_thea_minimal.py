#!/usr/bin/env python3
"""
Minimal Thea test - just the core browser automation without all the abstractions
"""

import time
import sys
import os

# Add the src path so we can import what we need
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Import only what we need for browser automation
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import undetected_chromedriver as uc
    import pyperclip
    import pyautogui
    from selenium.webdriver.common.by import By

    SELENIUM_OK = True
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    SELENIUM_OK = False

def test_minimal_browser():
    """Test just the basic browser interaction without Thea abstractions."""

    if not SELENIUM_OK:
        print("❌ Dependencies not available")
        return

    print("🧪 MINIMAL BROWSER TEST - Just the basics...")

    driver = None

    try:
        # Start browser
        print("1️⃣ Starting undetected Chrome...")
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = uc.Chrome(options=options, use_subprocess=True)
        print("✅ Browser started")

        # Go to ChatGPT
        print("2️⃣ Going to ChatGPT...")
        driver.get("https://chatgpt.com")
        time.sleep(5)

        current_url = driver.current_url
        page_title = driver.title
        print(f"   URL: {current_url}")
        print(f"   Title: {page_title}")

        # Check if we need to log in
        print("3️⃣ Checking login status...")

        # Simple check: if we're still on chatgpt.com and not redirected, might be logged in
        if "chatgpt.com" in current_url and "login" not in current_url.lower():
            print("   ✅ Appears to be on ChatGPT (possibly logged in)")

            # Try to find input elements
            try:
                textareas = driver.find_elements(By.TAG_NAME, "textarea")
                contenteditables = driver.find_elements(By.CSS_SELECTOR, "[contenteditable]")

                print(f"   Found {len(textareas)} textareas, {len(contenteditables)} contenteditable elements")

                if textareas or contenteditables:
                    print("   ✅ Found input elements - likely logged in")

                    # Try a simple message
                    input_element = textareas[0] if textareas else contenteditables[0]
                    print("4️⃣ Attempting to send message...")

                    # Type the message
                    message = "Hello ChatGPT, this is a minimal test."
                    input_element.send_keys(message)
                    print("   ✅ Message typed")

                    time.sleep(2)

                    # Try to send it
                    try:
                        # Look for send button or use Ctrl+Enter
                        from selenium.webdriver.common.keys import Keys
                        input_element.send_keys(Keys.CONTROL, Keys.ENTER)
                        print("   ✅ Sent with Ctrl+Enter")

                        # Wait for response
                        print("5️⃣ Waiting for response...")
                        time.sleep(10)

                        # Try to get response
                        try:
                            response_elements = driver.find_elements(By.CSS_SELECTOR, "[data-message-author-role='assistant']")
                            if response_elements:
                                response_text = response_elements[-1].text[:200]
                                print(f"   ✅ Got response: {response_text}...")
                            else:
                                print("   ⚠️ No response elements found")
                        except Exception as e:
                            print(f"   ⚠️ Could not extract response: {e}")

                    except Exception as e:
                        print(f"   ❌ Send failed: {e}")
                else:
                    print("   ❌ No input elements found - probably not logged in")

            except Exception as e:
                print(f"   ❌ Error checking elements: {e}")
        else:
            print("   ❌ Redirected to login page - not logged in")

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            print("6️⃣ Cleaning up...")
            try:
                driver.quit()
                print("✅ Browser closed")
            except:
                print("⚠️ Browser close failed")

if __name__ == "__main__":
    test_minimal_browser()