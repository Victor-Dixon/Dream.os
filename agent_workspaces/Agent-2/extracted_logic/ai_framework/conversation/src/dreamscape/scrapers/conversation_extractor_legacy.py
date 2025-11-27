"""
Legacy Conversation Extractor
Handles conversation extraction using scrollport scrolling for final_working_scraper.py
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

logger = logging.getLogger(__name__)

class ConversationExtractorLegacy:
    """Handles conversation extraction using scrollport scrolling."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the conversation extractor.
        
        Args:
            timeout: Timeout for web operations
        """
        self.timeout = timeout
    
    def find_scrollport_container(self, driver):
        """
        Find the scrollport container for conversation list.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            Scrollport container element or None
        """
        try:
            # Look for scrollport container
            scrollport_selectors = [
                "div[data-testid='conversation-list']",
                "div[class*='conversation-list']",
                "div[class*='sidebar'] div[class*='scroll']",
                "nav div[class*='scroll']",
                "div[role='navigation'] div[class*='scroll']",
            ]
            
            for selector in scrollport_selectors:
                try:
                    container = driver.find_element(By.CSS_SELECTOR, selector)
                    if container:
                        logger.info(f"Found scrollport container: {selector}")
                        return container
                except:
                    continue
            
            logger.warning("No scrollport container found")
            return None
            
        except Exception as e:
            logger.error(f"Error finding scrollport container: {e}")
            return None
    
    def get_conversation_list(self, driver) -> list:
        """
        Get list of conversations using scrollport scrolling.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            List of conversation dictionaries
        """
        try:
            # Find scrollport container
            scroll_container = self.find_scrollport_container(driver)
            if not scroll_container:
                logger.error("No scrollport container found")
                return []
            
            # Perform scrollport scrolling
            self._scrollport_scroll(driver, scroll_container)
            
            # Extract conversations
            conversations = self._extract_conversations(driver)
            
            logger.info(f"Extracted {len(conversations)} conversations")
            return conversations
            
        except Exception as e:
            logger.error(f"Error getting conversation list: {e}")
            return []
    
    def _scrollport_scroll(self, driver, scroll_container):
        """
        Perform scrollport scrolling to load all conversations.
        
        Args:
            driver: Selenium webdriver instance
            scroll_container: Scrollport container element
        """
        try:
            logger.info("Starting scrollport scrolling...")
            
            # Get initial scroll height
            last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
            
            scroll_attempts = 0
            max_attempts = 10
            
            while scroll_attempts < max_attempts:
                # Scroll to bottom of container
                driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_container)
                
                # Wait for new content to load
                time.sleep(2)
                
                # Calculate new scroll height
                new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
                
                # If height is the same, we've reached the bottom
                if new_height == last_height:
                    logger.info("Reached bottom of conversation list")
                    break
                
                last_height = new_height
                scroll_attempts += 1
                logger.info(f"Scroll attempt {scroll_attempts}/{max_attempts}")
            
            logger.info("Scrollport scrolling completed")
            
        except Exception as e:
            logger.error(f"Error during scrollport scrolling: {e}")
    
    def _extract_conversations(self, driver) -> list:
        """
        Extract conversation data from the page.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            List of conversation dictionaries
        """
        try:
            conversations = []
            
            # Look for conversation links
            conversation_selectors = [
                "a[href*='/c/']",
                "div[class*='conversation'] a",
                "nav a[href*='/c/']",
                "div[data-testid='conversation'] a",
            ]
            
            for selector in conversation_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        logger.info(f"Found {len(elements)} conversations with selector: {selector}")
                        
                        for element in elements:
                            try:
                                # Extract conversation data
                                href = element.get_attribute('href')
                                if not href or '/c/' not in href:
                                    continue
                                
                                # Extract conversation ID from URL
                                conversation_id = href.split('/c/')[-1].split('?')[0]
                                
                                # Extract title
                                title = element.text.strip()
                                if not title:
                                    title = f"Conversation {conversation_id}"
                                
                                conversations.append({
                                    'id': conversation_id,
                                    'title': title,
                                    'url': href
                                })
                                
                            except StaleElementReferenceException:
                                continue
                            except Exception as e:
                                logger.warning(f"Error extracting conversation: {e}")
                                continue
                        
                        break  # Use first selector that finds conversations
                        
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            return conversations
            
        except Exception as e:
            logger.error(f"Error extracting conversations: {e}")
            return [] 