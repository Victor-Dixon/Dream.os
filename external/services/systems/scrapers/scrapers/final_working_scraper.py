#!/usr/bin/env python3
"""
Final Working Scraper
Legacy scraper using scrollport scrolling for conversation extraction.
"""

import os
import json
import time
import logging
from datetime import datetime

# Import modular components
from .browser_manager import BrowserManager
from .cookie_manager import CookieManager
from .login_handler import LoginHandler
from .conversation_extractor_legacy import ConversationExtractorLegacy

logger = logging.getLogger(__name__)

class FinalWorkingScraper:
    """Legacy scraper using scrollport scrolling for conversation extraction."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the final working scraper.
        
        Args:
            timeout: Timeout for web operations
        """
        self.timeout = timeout
        self.conversation_extractor = ConversationExtractorLegacy(timeout)
    
    def ensure_login(self, driver, cookie_manager, login_handler):
        """
        Ensure user is logged in.
        
        Args:
            driver: Selenium webdriver instance
            cookie_manager: CookieManager instance
            login_handler: LoginHandler instance
            
        Returns:
            True if logged in, False otherwise
        """
        return login_handler.ensure_login_with_cookies(driver, cookie_manager)
    
    def get_conversation_list(self, driver) -> list:
        """
        Get list of conversations using the conversation extractor.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            List of conversation dictionaries
        """
        return self.conversation_extractor.get_conversation_list(driver)

def main():
    """Main function for command-line usage."""
    print("🚀 Final Working Scraper")
    print("=" * 30)
    
    try:
        # Create browser driver with automatic version management
        print("📱 Creating browser driver with automatic version management...")
        driver = BrowserManager(headless=False, use_undetected=True).create_driver()
        if not driver:
            print("❌ Failed to create browser driver")
            return 1
        print("✅ Browser driver created successfully")
        
        # Navigate to ChatGPT
        print("🌐 Navigating to ChatGPT...")
        driver.get('https://chat.openai.com/')
        print("✅ Navigated to ChatGPT")
        
        # Wait for page to load
        time.sleep(3)
        
        # Initialize managers
        cookie_manager = CookieManager('data/chatgpt_cookies.pkl')
        login_handler = LoginHandler()
        scraper = FinalWorkingScraper()
        
        # Ensure login (tries cookies first, falls back to manual)
        if not scraper.ensure_login(driver, cookie_manager, login_handler):
            print("❌ Failed to login")
            driver.quit()
            return 1
        
        # Extract conversations with scrollport scrolling
        print("📋 Extracting conversations with scrollport scrolling...")
        conversations = scraper.get_conversation_list(driver)
        
        if conversations:
            print(f"🎉 Successfully found {len(conversations)} conversations!")
            
            # Save to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'data/conversations/final_working_{timestamp}.json'
            
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
        
        print("\n🎉 Final working scraper completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 