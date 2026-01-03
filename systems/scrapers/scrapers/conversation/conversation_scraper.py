"""
Unified Conversation Scraper
===========================

Consolidates functionality from:
- smart_scraper_with_fallback.py
- final_working_scraper.py  
- improved_conversation_scraper.py

Provides a single, robust conversation scraping solution.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ..base.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class ConversationScraper(BaseScraper):
    """
    Unified conversation scraper with fallback strategies.
    
    Consolidates the best practices from multiple scraper implementations
    to provide a robust, reliable conversation extraction solution.
    """
    
    # ChatGPT-specific selectors
    SELECTORS = {
        # Conversation list selectors
        'conversation_list': 'nav a[href*="/c/"]',
        'conversation_links': 'a[href*="/c/"]',
        'conversation_titles': 'nav a[href*="/c/"] span',
        
        # Conversation content selectors
        'conversation_container': 'main',
        'message_containers': '[data-message-author-role]',
        'user_messages': '[data-message-author-role="user"]',
        'assistant_messages': '[data-message-author-role="assistant"]',
        'message_content': '.markdown',
        'message_text': '.markdown p, .markdown div',
        
        # Navigation selectors
        'new_chat_button': 'a[href="/"]',
        'sidebar_toggle': 'button[aria-label="Open sidebar"]',
        'sidebar': 'nav',
        
        # Loading indicators
        'loading_indicator': '.animate-spin',
        'typing_indicator': '[data-testid="conversation-turn-2"]'
    }
    
    def __init__(self, **kwargs):
        """
        Initialize the conversation scraper.
        
        Args:
            **kwargs: Arguments passed to BaseScraper
        """
        super().__init__(**kwargs)
        self.chatgpt_url = "https://chat.openai.com"
        
    def scrape(self, max_conversations: int = 10, include_content: bool = True) -> Dict[str, Any]:
        """
        Main scraping method for conversations.
        
        Args:
            max_conversations: Maximum number of conversations to scrape
            include_content: Whether to include full conversation content
            
        Returns:
            Dictionary containing scraped conversations
        """
        try:
            logger.info("🚀 Starting conversation scraping...")
            
            # Setup and login
            if not self.setup_browser():
                return {"error": "Browser setup failed"}
                
            if not self.navigate_to_url(self.chatgpt_url):
                return {"error": "Failed to navigate to ChatGPT"}
                
            if not self.login():
                return {"error": "Login failed"}
            
            # Wait for page to load
            time.sleep(3)
            
            # Scrape conversations
            conversations = self._scrape_conversation_list(max_conversations)
            
            # Scrape content if requested
            if include_content:
                conversations = self._scrape_conversation_content(conversations)
            
            result = {
                "success": True,
                "conversations": conversations,
                "total_count": len(conversations),
                "scraped_at": time.time()
            }
            
            logger.info(f"✅ Scraping complete: {len(conversations)} conversations")
            return result
            
        except Exception as e:
            logger.error(f"❌ Scraping failed: {e}")
            return {"error": str(e)}
        finally:
            self.cleanup()
    
    def _scrape_conversation_list(self, max_conversations: int) -> List[Dict[str, Any]]:
        """
        Scrape the list of conversations from the sidebar.
        
        Args:
            max_conversations: Maximum number of conversations to scrape
            
        Returns:
            List of conversation metadata
        """
        conversations = []
        
        try:
            # Ensure sidebar is open
            self._ensure_sidebar_open()
            
            # Wait for conversation list to load
            conversation_elements = self.wait_for_element(
                By.CSS_SELECTOR, 
                self.SELECTORS['conversation_list'],
                timeout=15
            )
            
            if not conversation_elements:
                logger.warning("⚠️ No conversation list found")
                return conversations
            
            # Get all conversation links
            conversation_links = self.driver.find_elements(
                By.CSS_SELECTOR, 
                self.SELECTORS['conversation_links']
            )
            
            logger.info(f"📋 Found {len(conversation_links)} conversation links")
            
            # Extract conversation metadata
            for i, link in enumerate(conversation_links[:max_conversations]):
                try:
                    conversation = self._extract_conversation_metadata(link, i)
                    if conversation:
                        conversations.append(conversation)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to extract conversation {i}: {e}")
                    continue
            
            logger.info(f"✅ Extracted {len(conversations)} conversations")
            
        except Exception as e:
            logger.error(f"❌ Failed to scrape conversation list: {e}")
        
        return conversations
    
    def _extract_conversation_metadata(self, link_element, index: int) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from a conversation link element.
        
        Args:
            link_element: WebElement representing conversation link
            index: Index of the conversation
            
        Returns:
            Conversation metadata dictionary
        """
        try:
            # Get conversation URL
            href = link_element.get_attribute('href')
            if not href or '/c/' not in href:
                return None
            
            # Extract conversation ID
            conversation_id = href.split('/c/')[-1]
            
            # Get conversation title
            title_element = link_element.find_element(By.CSS_SELECTOR, 'span')
            title = title_element.text.strip() if title_element else f"Conversation {index + 1}"
            
            return {
                "id": conversation_id,
                "title": title,
                "url": href,
                "index": index,
                "scraped_at": time.time()
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to extract metadata: {e}")
            return None
    
    def _scrape_conversation_content(self, conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scrape full content for each conversation.
        
        Args:
            conversations: List of conversation metadata
            
        Returns:
            List of conversations with full content
        """
        logger.info(f"📄 Scraping content for {len(conversations)} conversations...")
        
        for i, conversation in enumerate(conversations):
            try:
                logger.info(f"📖 Scraping conversation {i + 1}/{len(conversations)}: {conversation['title']}")
                
                # Navigate to conversation
                if not self.navigate_to_url(conversation['url']):
                    logger.warning(f"⚠️ Failed to navigate to conversation {conversation['id']}")
                    continue
                
                # Wait for conversation to load
                time.sleep(2)
                
                # Scrape messages
                messages = self._scrape_messages()
                conversation['messages'] = messages
                conversation['message_count'] = len(messages)
                
                # Add summary statistics
                conversation['statistics'] = self._calculate_conversation_stats(messages)
                
                logger.info(f"✅ Scraped {len(messages)} messages")
                
            except Exception as e:
                logger.error(f"❌ Failed to scrape conversation {conversation['id']}: {e}")
                conversation['error'] = str(e)
                continue
        
        return conversations
    
    def _scrape_messages(self) -> List[Dict[str, Any]]:
        """
        Scrape all messages from the current conversation.
        
        Returns:
            List of message dictionaries
        """
        messages = []
        
        try:
            # Wait for conversation container
            container = self.wait_for_element(
                By.CSS_SELECTOR,
                self.SELECTORS['conversation_container'],
                timeout=10
            )
            
            if not container:
                logger.warning("⚠️ No conversation container found")
                return messages
            
            # Find all message containers
            message_containers = self.driver.find_elements(
                By.CSS_SELECTOR,
                self.SELECTORS['message_containers']
            )
            
            logger.info(f"💬 Found {len(message_containers)} message containers")
            
            # Extract each message
            for i, container in enumerate(message_containers):
                try:
                    message = self._extract_message(container, i)
                    if message:
                        messages.append(message)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to extract message {i}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"❌ Failed to scrape messages: {e}")
        
        return messages
    
    def _extract_message(self, container, index: int) -> Optional[Dict[str, Any]]:
        """
        Extract a single message from its container.
        
        Args:
            container: WebElement containing the message
            index: Index of the message
            
        Returns:
            Message dictionary
        """
        try:
            # Get message role
            role = container.get_attribute('data-message-author-role')
            if not role:
                return None
            
            # Get message content
            content_element = container.find_element(By.CSS_SELECTOR, self.SELECTORS['message_content'])
            content = content_element.text.strip() if content_element else ""
            
            # Get HTML content for rich formatting
            html_content = content_element.get_attribute('innerHTML') if content_element else ""
            
            return {
                "index": index,
                "role": role,
                "content": content,
                "html_content": html_content,
                "timestamp": time.time(),
                "word_count": len(content.split())
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to extract message: {e}")
            return None
    
    def _ensure_sidebar_open(self):
        """Ensure the conversation sidebar is open."""
        try:
            # Check if sidebar is visible
            sidebar = self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS['sidebar'])
            if not sidebar.is_displayed():
                # Try to open sidebar
                toggle_button = self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS['sidebar_toggle'])
                if toggle_button:
                    toggle_button.click()
                    time.sleep(1)
                    
        except NoSuchElementException:
            logger.info("ℹ️ Sidebar toggle not found, assuming sidebar is open")
        except Exception as e:
            logger.warning(f"⚠️ Failed to ensure sidebar is open: {e}")
    
    def _calculate_conversation_stats(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics for a conversation.
        
        Args:
            messages: List of messages in the conversation
            
        Returns:
            Statistics dictionary
        """
        if not messages:
            return {}
        
        user_messages = [m for m in messages if m['role'] == 'user']
        assistant_messages = [m for m in messages if m['role'] == 'assistant']
        
        total_words = sum(m.get('word_count', 0) for m in messages)
        user_words = sum(m.get('word_count', 0) for m in user_messages)
        assistant_words = sum(m.get('word_count', 0) for m in assistant_messages)
        
        return {
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_words": total_words,
            "user_words": user_words,
            "assistant_words": assistant_words,
            "average_message_length": total_words / len(messages) if messages else 0
        }
    
    def validate_scrape_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate the scraping result.
        
        Args:
            result: Scraped data to validate
            
        Returns:
            True if result is valid, False otherwise
        """
        if not result:
            return False
        
        if 'error' in result:
            return False
        
        if 'conversations' not in result:
            return False
        
        conversations = result['conversations']
        if not isinstance(conversations, list):
            return False
        
        # Check that at least one conversation has content
        for conversation in conversations:
            if 'messages' in conversation and conversation['messages']:
                return True
        
        return False 