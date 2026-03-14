#!/usr/bin/env python3
"""
Simple test of improved login detection logic
"""

import sys
import os

# Add the src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import just what we need for browser automation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def test_login_detection():
    """Test the improved login detection logic."""

    print("🧪 TESTING IMPROVED LOGIN DETECTION")

    driver = None

    try:
        # Start browser
        print("1️⃣ Starting browser...")
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

        # Test improved login detection
        print("3️⃣ Testing login detection...")

        current_url = driver.current_url
        page_title = driver.title

        print(f"   URL: {current_url}")
        print(f"   Title: '{page_title}'")

        # Check for login elements (indicates NOT logged in)
        login_found = False
        try:
            login_indicators = [
                "[data-testid='login-button']",
                "[data-testid='signup-button']",
                "button:contains('Log in')",
                "button:contains('Sign in')",
                "button:contains('Sign up')",
                "a:contains('Log in')",
                "a:contains('Sign in')"
            ]

            for indicator in login_indicators:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                    if elements:
                        visible_login_elements = [elem for elem in elements if elem.is_displayed()]
                        if visible_login_elements:
                            print(f"   ❌ Found login elements ({indicator}) - NOT LOGGED IN")
                            login_found = True
                            break
                except:
                    pass
        except Exception as e:
            print(f"   ⚠️ Error checking login elements: {e}")

        if not login_found:
            print("   ✅ No login elements found - possibly logged in")

            # Check for ChatGPT interface elements
            indicators = [
                "textarea",
                "[contenteditable]",
                "[role='textbox']",
                ".composer",
                "[data-testid*='model']",
                "[data-testid*='new-chat']",
                "[data-testid*='regenerate']"
            ]

            found_indicators = 0
            for indicator in indicators:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                    if elements:
                        visible_elements = [elem for elem in elements if elem.is_displayed()]
                        if visible_elements:
                            found_indicators += 1
                            print(f"   ✅ Found {len(visible_elements)} {indicator} elements")
                except:
                    pass

            print(f"   Found {found_indicators} indicator types")

            if found_indicators >= 2:
                print("   ✅ LIKELY LOGGED IN - interface appears functional")

                # Test element interactability
                print("4️⃣ Testing element interactability...")
                try:
                    textareas = driver.find_elements(By.TAG_NAME, "textarea")
                    contenteditables = driver.find_elements(By.CSS_SELECTOR, "[contenteditable]")

                    if textareas or contenteditables:
                        input_element = textareas[0] if textareas else contenteditables[0]
                        try:
                            input_element.send_keys("test")
                            print("   ✅ Elements are interactable - COOKIES ARE VALID!")
                            input_element.clear()  # Clear the test text
                            return True
                        except Exception as e:
                            print(f"   ❌ Elements not interactable: {e}")
                            print("   ❌ STALE COOKIES DETECTED!")
                            return False
                    else:
                        print("   ❌ No input elements found")
                        return False

                except Exception as e:
                    print(f"   ❌ Error testing interactability: {e}")
                    return False
            else:
                print("   ❌ Not enough interface elements - not logged in")
                return False
        else:
            print("   ❌ Login elements detected - user needs to log in")
            return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if driver:
            driver.quit()
            print("✅ Browser closed")

if __name__ == "__main__":
    success = test_login_detection()
    print("\n" + "=" * 50)
    if success:
        print("🎉 COOKIES ARE VALID - User is logged in and elements work!")
    else:
        print("⚠️ STALE COOKIES DETECTED - Need manual login")
    print("=" * 50)