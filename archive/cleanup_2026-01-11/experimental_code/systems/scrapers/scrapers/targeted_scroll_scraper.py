#!/usr/bin/env python3
"""
Targeted Scroll Scraper
======================

A conversation scraper that uses targeted scrolling and the unified login utility
for reliable conversation extraction.
"""

import time
import json
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from dreamscape.scrapers.login_utils import ensure_login_unified, create_login_components
from dreamscape.scrapers.cookie_manager import CookieManager
from dreamscape.scrapers.login_handler import LoginHandler
from dreamscape.scrapers.browser_manager import BrowserManager

class TargetedScrollScraper:
    """Targeted scroll scraper with unified login and targeted scrolling."""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def ensure_login(self, driver, cookie_manager, login_handler):
        """Ensure we're logged in using the unified login utility."""
        return ensure_login_unified(driver, cookie_manager, login_handler)
    
    def find_scrollable_container(self, driver):
        """Find the actual scrollable container based on debug analysis."""
        print("🔍 Finding the correct scrollable container...")
        
        try:
            # Find conversation links first
            conversation_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]")
            if not conversation_links:
                print("❌ No conversation links found")
                return None
            
            print(f"📊 Found {len(conversation_links)} conversation links")
            
            # Get the grandparent of the first conversation link (based on debug analysis)
            first_link = conversation_links[0]
            parent = first_link.find_element(By.XPATH, "./..")
            grandparent = parent.find_element(By.XPATH, "./..")
            
            print(f"📄 First link: {first_link.tag_name} - {first_link.get_attribute('class')}")
            print(f"📄 Parent: {parent.tag_name} - {parent.get_attribute('class')}")
            print(f"📄 Grandparent: {grandparent.tag_name} - {grandparent.get_attribute('class')}")
            
            # Check scroll properties
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", grandparent)
            client_height = driver.execute_script("return arguments[0].clientHeight", grandparent)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", grandparent)
            
            print(f"📏 Grandparent scroll height: {scroll_height}")
            print(f"📏 Grandparent client height: {client_height}")
            print(f"📏 Grandparent current scroll top: {scroll_top}")
            print(f"📏 Can scroll: {scroll_height > client_height}")
            
            if scroll_height > client_height:
                print("✅ Found scrollable grandparent container!")
                return grandparent
            else:
                print("❌ Grandparent is not scrollable")
                return None
                
        except Exception as e:
            print(f"❌ Error finding scrollable container: {e}")
            return None
    
    def get_conversation_list(self, driver) -> list:
        """Get all conversations by scrolling the correct container."""
        if not driver:
            print("❌ No driver provided")
            return []
        
        try:
            print("📋 Extracting conversation list with targeted scrolling...")
            
            # Wait for page to load
            wait = WebDriverWait(driver, self.timeout)
            
            # Wait for initial conversations to load
            print("⏳ Waiting for initial conversations to load...")
            time.sleep(5)
            
            # Find the correct scrollable container
            scroll_container = self.find_scrollable_container(driver)
            if not scroll_container:
                print("❌ Could not find scrollable container")
                return []
            
            # Targeted scrolling of the correct container
            print("🔄 Starting targeted scrolling...")
            self._targeted_scroll(driver, scroll_container)
            
            # Extract all conversations
            print("📝 Extracting conversation data...")
            conversations = self._extract_conversations(driver)
            
            print(f"✅ Successfully extracted {len(conversations)} conversations!")
            return conversations
            
        except Exception as e:
            print(f"❌ Error extracting conversations: {e}")
            return []
    
    def _targeted_scroll(self, driver, scroll_container):
        """Targeted scrolling of the correct container."""
        try:
            # Get initial count
            initial_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
            print(f"📊 Initial conversation count: {initial_count}")
            
            # Targeted scrolling with multiple techniques
            max_scrolls = 200
            no_change_count = 0
            max_no_change = 15
            
            for i in range(max_scrolls):
                # Technique 1: Scroll the correct container to bottom
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
                time.sleep(1)
                
                # Technique 2: Trigger scroll event on the correct container
                driver.execute_script("""
                    var event = new Event('scroll', { bubbles: true });
                    arguments[0].dispatchEvent(event);
                """, scroll_container)
                time.sleep(1)
                
                # Technique 3: Try scrolling by pixels
                current_scroll = driver.execute_script("return arguments[0].scrollTop", scroll_container)
                scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
                client_height = driver.execute_script("return arguments[0].clientHeight", scroll_container)
                
                # Scroll down by client height amount
                new_scroll = min(current_scroll + client_height, scroll_height)
                driver.execute_script("arguments[0].scrollTop = arguments[1]", scroll_container, new_scroll)
                time.sleep(1)
                
                # Check new count
                new_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"📈 Scroll {i+1}/{max_scrolls}: {new_count} conversations")
                
                # Check if we're still loading new conversations
                if new_count <= initial_count:
                    no_change_count += 1
                    
                    # Try more aggressive techniques after a few attempts
                    if no_change_count >= 5:
                        print("🚀 Trying burst scrolling on correct container...")
                        
                        # Multiple rapid scrolls
                        for j in range(10):
                            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
                            time.sleep(0.2)
                        
                        # Check again
                        new_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
                        print(f"📊 After burst scrolling: {new_count} conversations")
                        
                        if new_count <= initial_count:
                            no_change_count += 1
                        else:
                            no_change_count = 0
                else:
                    no_change_count = 0
                
                # Stop if no changes for several attempts
                if no_change_count >= max_no_change:
                    print(f"⏹️ Stopping scroll after {max_no_change} attempts with no new conversations")
                    break
                
                initial_count = new_count
            
            final_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
            print(f"🎯 Final conversation count after targeted scrolling: {final_count}")
            
        except Exception as e:
            print(f"⚠️ Error during targeted scrolling: {e}")
    
    def _extract_conversations(self, driver) -> list:
        """Extract conversation data from the page."""
        try:
            # Get all conversation links
            conversation_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]")
            
            conversations = []
            seen_ids = set()
            
            for link in conversation_links:
                try:
                    href = link.get_attribute('href')
                    if not href:
                        continue
                    
                    # Extract conversation ID
                    conversation_id = None
                    if '/c/' in href:
                        conversation_id = href.split('/c/')[-1].split('?')[0]
                    
                    if not conversation_id or conversation_id in seen_ids:
                        continue
                    
                    seen_ids.add(conversation_id)
                    
                    # Get title
                    title = link.text.strip()
                    if not title:
                        try:
                            parent = link.find_element(By.XPATH, "./..")
                            title = parent.text.strip()
                        except:
                            title = f"Conversation {conversation_id[:8]}"
                    
                    # Skip demo conversations
                    if 'demo' in title.lower() or 'demo' in conversation_id.lower():
                        continue
                    
                    conversations.append({
                        'id': conversation_id,
                        'title': title,
                        'url': href
                    })
                    
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    print(f"⚠️ Error extracting conversation: {e}")
                    continue
            
            return conversations
            
        except Exception as e:
            print(f"❌ Error extracting conversations: {e}")
            return []

def main():
    print("🚀 Targeted Scroll Scraper")
    print("=" * 35)
    
    try:
        # EDIT START: Use BrowserManager for automatic driver management
        print("📱 Creating browser driver with automatic version management...")
        driver = BrowserManager(headless=False, use_undetected=True).create_driver()
        if not driver:
            print("❌ Failed to create browser driver")
            return 1
        print("✅ Browser driver created successfully")
        # EDIT END
        
        # Navigate to ChatGPT
        print("🌐 Navigating to ChatGPT...")
        driver.get('https://chat.openai.com/')
        print("✅ Navigated to ChatGPT")
        
        # Wait for page to load
        time.sleep(3)
        
        # Initialize managers
        cookie_manager = CookieManager('data/chatgpt_cookies.pkl')
        login_handler = LoginHandler()
        scraper = TargetedScrollScraper()
        
        # Ensure login (tries cookies first, falls back to manual)
        if not scraper.ensure_login(driver, cookie_manager, login_handler):
            print("❌ Failed to login")
            driver.quit()
            return 1
        
        # Extract conversations with targeted scrolling
        print("📋 Extracting conversations with targeted scrolling...")
        conversations = scraper.get_conversation_list(driver)
        
        if conversations:
            print(f"🎉 Successfully found {len(conversations)} conversations!")
            
            # Save to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'data/conversations/targeted_scroll_{timestamp}.json'
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved to {output_file}")
            
            # Show first 20 conversations
            print("\n📝 First 20 conversations:")
            for i, conv in enumerate(conversations[:20]):
                title = conv.get('title', 'No title')
                conv_id = conv.get('id', 'No ID')
                print(f"  {i+1:2d}. {title} (ID: {conv_id})")
            
            if len(conversations) > 20:
                print(f"  ... and {len(conversations) - 20} more conversations")
            
        else:
            print("❌ No conversations found")
        
        # Close browser
        driver.quit()
        print("✅ Browser closed")
        
        print("\n🎉 Targeted scroll scraper completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 