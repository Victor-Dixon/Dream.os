#!/usr/bin/env python3
"""
Activate WordPress Theme via Browser Automation
===============================================

Uses browser automation to activate a WordPress theme via admin interface.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("❌ Selenium not installed. Install with: pip install selenium")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def activate_theme(
    site_url: str,
    theme_name: str,
    auto_login: bool = False,
    wait_timeout: int = 60
) -> bool:
    """
    Activate WordPress theme via browser automation.
    
    Args:
        site_url: Base site URL (e.g., https://ariajet.site)
        theme_name: Theme name to activate (e.g., "ariajet")
        auto_login: If True, attempt login using WORDPRESS_USER/PASS from .env
        wait_timeout: Timeout for manual login (seconds)
    
    Returns:
        True if successful
    """
    if not SELENIUM_AVAILABLE:
        return False
    
    wp_admin_url = f"{site_url}/wp-admin"
    
    print("🚀 Starting browser automation...")
    
    # Setup Chrome options
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Login
        if auto_login:
            wp_user = os.getenv("WORDPRESS_USER")
            wp_pass = os.getenv("WORDPRESS_PASS")
            
            if not wp_user or not wp_pass:
                print("⚠️  Auto-login requested but WORDPRESS_USER/WORDPRESS_PASS not set in .env")
                auto_login = False
        
        if auto_login:
            print("🔐 Attempting automatic WordPress login...")
            driver.get(wp_admin_url)
            time.sleep(2)
            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "form#loginform"))
                )
                user_input = driver.find_element(By.CSS_SELECTOR, "input#user_login")
                pass_input = driver.find_element(By.CSS_SELECTOR, "input#user_pass")
                submit_btn = driver.find_element(By.CSS_SELECTOR, "input#wp-submit")
                
                user_input.clear()
                user_input.send_keys(wp_user)
                pass_input.clear()
                pass_input.send_keys(wp_pass)
                submit_btn.click()
                time.sleep(3)
            except TimeoutException:
                print("⚠️  Could not find login form for auto-login")
                auto_login = False
        
        if not auto_login:
            print(f"📱 Navigating to: {wp_admin_url}")
            driver.get(wp_admin_url)
            time.sleep(2)
            
            print("⏳ Waiting for login...")
            print(f"   Please log in to WordPress admin (waiting {wait_timeout} seconds)")
            
            try:
                WebDriverWait(driver, wait_timeout).until(
                    lambda d: "wp-admin" in d.current_url and 
                             ("dashboard" in d.current_url.lower() or 
                              "themes" in d.current_url.lower() or
                              d.find_elements(By.CSS_SELECTOR, "#wpadminbar"))
                )
                print("✅ Logged in successfully!")
            except TimeoutException:
                print("❌ Login timeout")
                return False
        
        # Navigate to Themes page
        print("🎨 Navigating to Themes page...")
        themes_url = f"{wp_admin_url}/themes.php"
        driver.get(themes_url)
        time.sleep(3)
        
        # Find and activate theme
        print(f"🔍 Looking for theme: {theme_name}...")
        
        try:
            # Wait for themes to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".theme"))
            )
            
            # Find theme by name (check theme name in the theme card)
            themes = driver.find_elements(By.CSS_SELECTOR, ".theme")
            theme_found = False
            
            for theme in themes:
                try:
                    theme_name_element = theme.find_element(By.CSS_SELECTOR, ".theme-name")
                    if theme_name.lower() in theme_name_element.text.lower():
                        print(f"✅ Found theme: {theme_name_element.text}")
                        
                        # Check if already active
                        active_badge = theme.find_elements(By.CSS_SELECTOR, ".theme.active")
                        if active_badge:
                            print(f"✅ Theme '{theme_name}' is already active!")
                            return True
                        
                        # Click activate button
                        activate_button = theme.find_element(By.CSS_SELECTOR, ".button.activate")
                        activate_button.click()
                        time.sleep(2)
                        
                        print(f"✅ Theme '{theme_name}' activated!")
                        theme_found = True
                        break
                except Exception:
                    continue
            
            if not theme_found:
                print(f"❌ Theme '{theme_name}' not found on Themes page")
                print("   Available themes:")
                for theme in themes:
                    try:
                        name = theme.find_element(By.CSS_SELECTOR, ".theme-name").text
                        print(f"     - {name}")
                    except:
                        pass
                return False
            
            # Verify activation
            time.sleep(2)
            active_themes = driver.find_elements(By.CSS_SELECTOR, ".theme.active .theme-name")
            for active_theme in active_themes:
                if theme_name.lower() in active_theme.text.lower():
                    print(f"✅ Verified: Theme '{theme_name}' is now active!")
                    return True
            
            print("⚠️  Theme activation may have succeeded, but verification unclear")
            return True
            
        except TimeoutException:
            print("❌ Could not find themes on page")
            return False
        except Exception as e:
            print(f"❌ Error activating theme: {e}")
            return False
        
    finally:
        print("⏳ Keeping browser open for 10 seconds to verify...")
        time.sleep(10)
        driver.quit()


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Activate WordPress theme via browser")
    parser.add_argument("--site", required=True, help="Site URL (e.g., https://ariajet.site)")
    parser.add_argument("--theme", required=True, help="Theme name to activate")
    parser.add_argument("--auto-login", action="store_true", help="Auto-login using .env credentials")
    parser.add_argument("--wait", type=int, default=60, help="Login wait timeout (seconds)")
    
    args = parser.parse_args()
    
    success = activate_theme(
        site_url=args.site,
        theme_name=args.theme,
        auto_login=args.auto_login,
        wait_timeout=args.wait
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

