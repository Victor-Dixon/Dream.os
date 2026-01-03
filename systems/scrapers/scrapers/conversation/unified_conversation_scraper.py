#!/usr/bin/env python3
"""
Unified Conversation Scraper
============================

Consolidates all conversation scraping strategies into a single, configurable system.
Eliminates duplication across multiple scraper files.
"""

import time
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from ..base.login_utils import ensure_login_unified, create_login_components
from ..cookie_manager import CookieManager
from ..login_handler import LoginHandler
from ..browser_manager import BrowserManager

logger = logging.getLogger(__name__)

class ScrollingStrategy(Enum):
    """Different scrolling strategies for conversation extraction."""
    TARGETED = "targeted"           # From targeted_scroll_scraper.py
    AGGRESSIVE = "aggressive"       # From improved_conversation_scraper.py
    SUPER_AGGRESSIVE = "super_aggressive"  # From smart_scraper_with_fallback.py
    SCROLLPORT = "scrollport"       # From final_working_scraper.py

class UnifiedConversationScraper:
    """
    Unified conversation scraper that consolidates all scraping strategies.
    
    This replaces:
    - targeted_scroll_scraper.py
    - improved_conversation_scraper.py
    - smart_scraper_with_fallback.py
    - final_working_scraper.py
    """
    
    def __init__(self, 
                 timeout: int = 30,
                 scrolling_strategy: ScrollingStrategy = ScrollingStrategy.TARGETED,
                 max_conversations: Optional[int] = None,
                 scroll_delay: float = 1.0):
        """
        Initialize the unified conversation scraper.
        
        Args:
            timeout: Timeout for web operations
            scrolling_strategy: Which scrolling strategy to use
            max_conversations: Maximum conversations to extract (None for all)
            scroll_delay: Delay between scroll operations
        """
        self.timeout = timeout
        self.scrolling_strategy = scrolling_strategy
        self.max_conversations = max_conversations
        self.scroll_delay = scroll_delay
        
        logger.info(f"✅ UnifiedConversationScraper initialized with {scrolling_strategy.value} strategy")
    
    def ensure_login(self, driver, cookie_manager, login_handler):
        """Ensure we're logged in using the unified login utility."""
        return ensure_login_unified(driver, cookie_manager, login_handler)
    
    def get_conversation_list(self, driver) -> List[Dict[str, str]]:
        """
        Get all conversations using the configured scrolling strategy.
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            List of conversation dictionaries
        """
        if not driver:
            logger.error("❌ No driver provided")
            return []
        
        try:
            logger.info(f"📋 Extracting conversations using {self.scrolling_strategy.value} strategy...")
            
            # Wait for page to load
            wait = WebDriverWait(driver, self.timeout)
            
            # Wait for initial conversations to load
            logger.info("⏳ Waiting for initial conversations to load...")
            time.sleep(5)
            
            # Find the appropriate container based on strategy
            container = self._find_scrollable_container(driver)
            if not container:
                logger.error("❌ Could not find scrollable container")
                return []
            
            # Apply the configured scrolling strategy
            logger.info(f"🔄 Starting {self.scrolling_strategy.value} scrolling...")
            self._apply_scrolling_strategy(driver, container)
            
            # Extract all conversations
            logger.info("📝 Extracting conversation data...")
            conversations = self._extract_conversations(driver)
            
            logger.info(f"✅ Successfully extracted {len(conversations)} conversations!")
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Error extracting conversations: {e}")
            return []
    
    def _find_scrollable_container(self, driver):
        """Find the appropriate scrollable container based on strategy."""
        if self.scrolling_strategy == ScrollingStrategy.SCROLLPORT:
            return self._find_scrollport_container(driver)
        elif self.scrolling_strategy == ScrollingStrategy.TARGETED:
            return self._find_targeted_container(driver)
        else:
            return self._find_sidebar_container(driver)
    
    def _find_scrollport_container(self, driver):
        """Find the scrollport container (from final_working_scraper.py)."""
        logger.info("🔍 Finding scrollport container...")
        
        scrollport_selectors = [
            "//nav[contains(@class, 'scrollport')]",
            "//nav[contains(@class, 'group/scrollport')]",
            "//nav[contains(@class, 'relative') and contains(@class, 'flex') and contains(@class, 'overflow')]"
        ]
        
        for selector in scrollport_selectors:
            try:
                container = driver.find_element(By.XPATH, selector)
                logger.info(f"✅ Found scrollport container using: {selector}")
                
                # Verify it's scrollable
                scroll_height = driver.execute_script("return arguments[0].scrollHeight", container)
                client_height = driver.execute_script("return arguments[0].clientHeight", container)
                
                if scroll_height > client_height:
                    logger.info("✅ Container is scrollable!")
                    return container
                else:
                    logger.warning("❌ Container is not scrollable")
                    
            except Exception as e:
                logger.debug(f"⚠️ Selector {selector} failed: {e}")
                continue
        
        logger.error("❌ Could not find scrollport container")
        return None
    
    def _find_targeted_container(self, driver):
        """Find the targeted container (from targeted_scroll_scraper.py)."""
        logger.info("🔍 Finding targeted scrollable container...")
        
        try:
            # Find conversation links first
            conversation_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]")
            if not conversation_links:
                logger.error("❌ No conversation links found")
                return None
            
            logger.info(f"📊 Found {len(conversation_links)} conversation links")
            
            # Get the grandparent of the first conversation link
            first_link = conversation_links[0]
            parent = first_link.find_element(By.XPATH, "./..")
            grandparent = parent.find_element(By.XPATH, "./..")
            
            # Check scroll properties
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", grandparent)
            client_height = driver.execute_script("return arguments[0].clientHeight", grandparent)
            
            if scroll_height > client_height:
                logger.info("✅ Found scrollable grandparent container!")
                return grandparent
            else:
                logger.error("❌ Grandparent is not scrollable")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error finding targeted container: {e}")
            return None
    
    def _find_sidebar_container(self, driver):
        """Find the sidebar container (from improved_conversation_scraper.py)."""
        logger.info("🔍 Finding sidebar container...")
        
        sidebar_selectors = [
            "//div[contains(@class, 'bg-token-sidebar-surface-primary')]",
            "//div[contains(@class, 'sidebar')]",
            "//nav[contains(@class, 'sidebar')]",
            "//aside[contains(@class, 'sidebar')]",
            "//div[contains(@class, 'conversations')]",
            "//nav[contains(@class, 'conversations')]",
            "//div[contains(@class, 'flex-col') and contains(@class, 'overflow')]"
        ]
        
        for selector in sidebar_selectors:
            try:
                container = driver.find_element(By.XPATH, selector)
                logger.info(f"✅ Found sidebar using selector: {selector}")
                return container
            except Exception as e:
                logger.debug(f"⚠️ Selector {selector} failed: {e}")
                continue
        
        logger.error("❌ Could not find sidebar container")
        return None
    
    def _apply_scrolling_strategy(self, driver, container):
        """Apply the configured scrolling strategy."""
        if self.scrolling_strategy == ScrollingStrategy.TARGETED:
            self._targeted_scroll(driver, container)
        elif self.scrolling_strategy == ScrollingStrategy.AGGRESSIVE:
            self._aggressive_scroll(driver, container)
        elif self.scrolling_strategy == ScrollingStrategy.SUPER_AGGRESSIVE:
            self._super_aggressive_scroll(driver, container)
        elif self.scrolling_strategy == ScrollingStrategy.SCROLLPORT:
            self._scrollport_scroll(driver, container)
    
    def _targeted_scroll(self, driver, container):
        """Targeted scrolling strategy (from targeted_scroll_scraper.py)."""
        logger.info("🔄 Applying targeted scrolling...")
        
        try:
            initial_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
            logger.info(f"📊 Initial conversation count: {initial_count}")
            
            last_count = 0
            no_change_count = 0
            max_no_change = 3
            
            while True:
                # Scroll to bottom of container
                driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
                time.sleep(self.scroll_delay)
                
                # Count conversations
                current_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
                logger.info(f"📊 Current conversation count: {current_count}")
                
                # Check if we've reached the limit
                if self.max_conversations and current_count >= self.max_conversations:
                    logger.info(f"✅ Reached target of {self.max_conversations} conversations")
                    break
                
                # Check if count hasn't changed
                if current_count == last_count:
                    no_change_count += 1
                    if no_change_count >= max_no_change:
                        logger.info("✅ No new conversations found after multiple attempts")
                        break
                else:
                    no_change_count = 0
                
                last_count = current_count
                
        except Exception as e:
            logger.error(f"❌ Error during targeted scrolling: {e}")
    
    def _aggressive_scroll(self, driver, container):
        """Aggressive scrolling strategy (from improved_conversation_scraper.py)."""
        logger.info("🔄 Applying aggressive scrolling...")
        
        try:
            initial_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
            logger.info(f"📊 Initial conversation count: {initial_count}")
            
            last_count = 0
            no_change_count = 0
            max_no_change = 5  # More attempts for aggressive strategy
            
            while True:
                # Scroll multiple times per iteration
                for _ in range(3):
                    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
                    time.sleep(self.scroll_delay * 0.5)
                
                # Count conversations
                current_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
                logger.info(f"📊 Current conversation count: {current_count}")
                
                # Check if we've reached the limit
                if self.max_conversations and current_count >= self.max_conversations:
                    logger.info(f"✅ Reached target of {self.max_conversations} conversations")
                    break
                
                # Check if count hasn't changed
                if current_count == last_count:
                    no_change_count += 1
                    if no_change_count >= max_no_change:
                        logger.info("✅ No new conversations found after multiple attempts")
                        break
                else:
                    no_change_count = 0
                
                last_count = current_count
                
        except Exception as e:
            logger.error(f"❌ Error during aggressive scrolling: {e}")
    
    def _super_aggressive_scroll(self, driver, container):
        """Super aggressive scrolling strategy (from smart_scraper_with_fallback.py)."""
        logger.info("🔄 Applying super aggressive scrolling...")
        
        try:
            initial_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
            logger.info(f"📊 Initial conversation count: {initial_count}")
            
            last_count = 0
            no_change_count = 0
            max_no_change = 8  # Even more attempts for super aggressive strategy
            
            while True:
                # Scroll multiple times per iteration with shorter delays
                for _ in range(5):
                    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
                    time.sleep(self.scroll_delay * 0.3)
                
                # Count conversations
                current_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
                logger.info(f"📊 Current conversation count: {current_count}")
                
                # Check if we've reached the limit
                if self.max_conversations and current_count >= self.max_conversations:
                    logger.info(f"✅ Reached target of {self.max_conversations} conversations")
                    break
                
                # Check if count hasn't changed
                if current_count == last_count:
                    no_change_count += 1
                    if no_change_count >= max_no_change:
                        logger.info("✅ No new conversations found after multiple attempts")
                        break
                else:
                    no_change_count = 0
                
                last_count = current_count
                
        except Exception as e:
            logger.error(f"❌ Error during super aggressive scrolling: {e}")
    
    def _scrollport_scroll(self, driver, container):
        """Scrollport scrolling strategy (from final_working_scraper.py)."""
        logger.info("🔄 Applying scrollport scrolling...")
        
        try:
            initial_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
            logger.info(f"📊 Initial conversation count: {initial_count}")
            
            last_count = 0
            no_change_count = 0
            max_no_change = 4
            
            while True:
                # Scroll to bottom of scrollport container
                driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
                time.sleep(self.scroll_delay)
                
                # Count conversations
                current_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]"))
                logger.info(f"📊 Current conversation count: {current_count}")
                
                # Check if we've reached the limit
                if self.max_conversations and current_count >= self.max_conversations:
                    logger.info(f"✅ Reached target of {self.max_conversations} conversations")
                    break
                
                # Check if count hasn't changed
                if current_count == last_count:
                    no_change_count += 1
                    if no_change_count >= max_no_change:
                        logger.info("✅ No new conversations found after multiple attempts")
                        break
                else:
                    no_change_count = 0
                
                last_count = current_count
                
        except Exception as e:
            logger.error(f"❌ Error during scrollport scrolling: {e}")
    
    def _extract_conversations(self, driver) -> List[Dict[str, str]]:
        """Extract conversation data from the page."""
        try:
            conversations = []
            conversation_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]")
            
            for link in conversation_links:
                try:
                    href = link.get_attribute('href')
                    if not href:
                        continue
                    
                    # Extract conversation ID from URL
                    conversation_id = href.split('/c/')[-1] if '/c/' in href else href
                    
                    # Try to get title from various possible elements
                    title = self._extract_conversation_title(link)
                    
                    conversation = {
                        'id': conversation_id,
                        'title': title,
                        'url': href,
                        'extracted_at': datetime.now().isoformat()
                    }
                    
                    conversations.append(conversation)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Error extracting conversation: {e}")
                    continue
            
            logger.info(f"📝 Extracted {len(conversations)} conversations")
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Error extracting conversations: {e}")
            return []
    
    def _extract_conversation_title(self, link_element) -> str:
        """Extract conversation title from link element."""
        try:
            # Try to find title in the link element or its children
            title_selectors = [
                ".//span[contains(@class, 'text')]",
                ".//div[contains(@class, 'text')]",
                ".//p[contains(@class, 'text')]",
                ".//span",
                ".//div",
                ".//p"
            ]
            
            for selector in title_selectors:
                try:
                    title_element = link_element.find_element(By.XPATH, selector)
                    title = title_element.text.strip()
                    if title:
                        return title
                except:
                    continue
            
            # Fallback to link text
            title = link_element.text.strip()
            if title:
                return title
            
            # Final fallback
            return f"Conversation {link_element.get_attribute('href', '').split('/c/')[-1] if '/c/' in link_element.get_attribute('href', '') else 'Unknown'}"
            
        except Exception as e:
            logger.warning(f"⚠️ Error extracting title: {e}")
            return "Unknown Title"
    
    def run_scraper(self, driver, output_file: str = "conversations.json") -> bool:
        """
        Run the complete scraping process.
        
        Args:
            driver: Selenium WebDriver instance
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("🚀 Starting unified conversation scraper...")
            
            # Extract conversations
            conversations = self.get_conversation_list(driver)
            
            if not conversations:
                logger.error("❌ No conversations extracted")
                return False
            
            # Save to file
            self._save_conversations(conversations, output_file)
            
            logger.info(f"✅ Successfully scraped {len(conversations)} conversations")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error running scraper: {e}")
            return False
    
    def _save_conversations(self, conversations: List[Dict[str, str]], output_file: str):
        """Save conversations to JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved {len(conversations)} conversations to {output_file}")
            
        except Exception as e:
            logger.error(f"❌ Error saving conversations: {e}")


# Convenience functions for different strategies
def create_targeted_scraper(timeout: int = 30, max_conversations: Optional[int] = None) -> UnifiedConversationScraper:
    """Create a scraper with targeted scrolling strategy."""
    return UnifiedConversationScraper(
        timeout=timeout,
        scrolling_strategy=ScrollingStrategy.TARGETED,
        max_conversations=max_conversations
    )

def create_aggressive_scraper(timeout: int = 30, max_conversations: Optional[int] = None) -> UnifiedConversationScraper:
    """Create a scraper with aggressive scrolling strategy."""
    return UnifiedConversationScraper(
        timeout=timeout,
        scrolling_strategy=ScrollingStrategy.AGGRESSIVE,
        max_conversations=max_conversations
    )

def create_super_aggressive_scraper(timeout: int = 30, max_conversations: Optional[int] = None) -> UnifiedConversationScraper:
    """Create a scraper with super aggressive scrolling strategy."""
    return UnifiedConversationScraper(
        timeout=timeout,
        scrolling_strategy=ScrollingStrategy.SUPER_AGGRESSIVE,
        max_conversations=max_conversations
    )

def create_scrollport_scraper(timeout: int = 30, max_conversations: Optional[int] = None) -> UnifiedConversationScraper:
    """Create a scraper with scrollport scrolling strategy."""
    return UnifiedConversationScraper(
        timeout=timeout,
        scrolling_strategy=ScrollingStrategy.SCROLLPORT,
        max_conversations=max_conversations
    ) 