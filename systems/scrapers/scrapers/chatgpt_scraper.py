"""
Simplified ChatGPT Scraper for Digital Dreamscape Standalone
Handles automated ChatGPT conversation extraction without external dependencies.
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Import modular components
from dreamscape.scrapers.browser_manager import BrowserManager
from dreamscape.scrapers.base import ensure_login_unified, create_login_components
from dreamscape.scrapers.conversation_extractor import ConversationExtractor
from dreamscape.scrapers.demo_conversations import DemoConversationGenerator
from dreamscape.scrapers.templated_prompts import TemplatedPromptsProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTScraper:
    """
    Simplified ChatGPT scraper for extracting conversation history.
    Uses modular components for browser management, login, and extraction.
    """
    
    def __init__(self, headless: bool = False, timeout: int = 30, use_undetected: bool = True, 
                 username: Optional[str] = None, password: Optional[str] = None,
                 cookie_file: Optional[str] = None, totp_secret: Optional[str] = None):
        """
        Initialize the ChatGPT scraper.
        
        Args:
            headless: Run browser in headless mode
            timeout: Timeout for web operations
            use_undetected: Use undetected-chromedriver if available
            username: ChatGPT username/email
            password: ChatGPT password
            cookie_file: Path to cookie file for session persistence
            totp_secret: TOTP secret for 2FA
        """
        # Initialize modular components
        self.browser_manager = BrowserManager(headless=headless, use_undetected=use_undetected)
        self.cookie_manager, self.login_handler = create_login_components(cookie_file)
        self.login_handler.credential_login.username = username
        self.login_handler.credential_login.password = password
        self.login_handler.credential_login.two_factor_auth.totp_secret = totp_secret
        self.conversation_extractor = ConversationExtractor(timeout=timeout)
        self.templated_prompts_processor = TemplatedPromptsProcessor(self.conversation_extractor)
        
        self.driver = None
        self.timeout = timeout
        
        # Expose init params for external checks/tests
        self.use_undetected = use_undetected
        self.headless = headless
        self.cookie_file = cookie_file or ""
        
        logger.info("✅ ChatGPT Scraper initialized with modular components")
    
    def __enter__(self):
        """Context manager entry."""
        self.start_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()
    
    def start_driver(self) -> bool:
        """Start the web driver using the browser manager."""
        self.driver = self.browser_manager.create_driver()
        if self.driver:
            logger.info("✅ Driver started successfully")
            return True
        else:
            logger.error("❌ Failed to start driver")
            return False
    
    def close_driver(self):
        """Close the web driver using the browser manager."""
        self.browser_manager.close_driver()
        self.driver = None
        logger.info("✅ Driver closed")
    
    def navigate_to_chatgpt(self, model: str = "") -> bool:
        """
        Navigate to ChatGPT with optional model selection.
        
        Args:
            model: Specific model to navigate to (e.g., "gpt-4o", "gpt-4o-mini")
            
        Returns:
            True if navigation successful, False otherwise
        """
        if not self.driver:
            logger.error("No driver available")
            return False
        
        try:
            base_url = "https://chat.openai.com/"
            if model:
                base_url += f"?model={model}"
            
            logger.info(f"Navigating to ChatGPT: {base_url}")
            self.driver.get(base_url)
            time.sleep(3)
            
            logger.info("✅ Successfully navigated to ChatGPT")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to navigate to ChatGPT: {e}")
            return False
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in using the login handler.
        
        Returns:
            True if logged in, False otherwise
        """
        return self.login_handler.is_logged_in(self.driver)
    
    def get_conversation_list(self, progress_callback=None) -> List[Dict[str, str]]:
        """
        Get list of available conversations using the conversation extractor.
        Optionally provide a progress_callback for GUI progress bar.
        """
        # EDIT: Propagate progress_callback
        return self.conversation_extractor.get_conversation_list(self.driver, progress_callback=progress_callback)
    
    def run_scraper(self, model: str = "", output_file: str = "chatgpt_chats.json") -> bool:
        """
        Run the complete scraping workflow.
        
        Args:
            model: Specific model to scrape
            output_file: Output file for conversations
            
        Returns:
            True if scraping successful, False otherwise
        """
        try:
            logger.info("🚀 Starting ChatGPT scraper workflow")
            
            # Navigate to ChatGPT
            if not self.navigate_to_chatgpt(model):
                return False
            
            # Ensure login with comprehensive fallback strategy
            if not self.ensure_login(allow_manual=True, manual_timeout=60):
                logger.error("❌ Login failed")
                return False
            
            # Get conversation list
            conversations = self.get_conversation_list()
            if not conversations:
                logger.warning("No conversations found")
                return False
            
            # Save conversations
            self._save_conversations(conversations, output_file)
            
            logger.info(f"✅ Scraping completed: {len(conversations)} conversations saved")
            return True
            
        except Exception as e:
            logger.error(f"❌ Scraping failed: {e}")
            return False
    
    def _save_conversations(self, conversations: List[Dict[str, str]], output_file: str):
        """Save conversations to JSON file."""
        try:
            # Ensure output directory exists
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False)
                
            logger.info(f"✅ Saved {len(conversations)} conversations to {output_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save conversations: {e}")
    
    def enter_conversation(self, conversation_url: str) -> bool:
        """
        Enter a specific conversation using the conversation extractor.
        
        Args:
            conversation_url: URL of the conversation to enter
            
        Returns:
            True if successfully entered conversation, False otherwise
        """
        return self.conversation_extractor.enter_conversation(self.driver, conversation_url)
    
    def get_conversation_content(self) -> Dict[str, str]:
        """
        Get content from the current conversation using the conversation extractor.
        
        Returns:
            Dictionary containing conversation content
        """
        return self.conversation_extractor.get_conversation_content(self.driver)
    
    def send_prompt(self, prompt: str, wait_for_response: bool = True) -> bool:
        """
        Send a prompt to the current conversation using the conversation extractor.
        
        Args:
            prompt: Text prompt to send
            wait_for_response: Whether to wait for response
            
        Returns:
            True if prompt sent successfully, False otherwise
        """
        return self.conversation_extractor.send_prompt(self.driver, prompt, wait_for_response)
    
    def run_templated_prompts(self, conversations: List[Dict[str, str]], prompt_template: str) -> List[Dict[str, str]]:
        """
        Run templated prompts on a list of conversations.
        
        Args:
            conversations: List of conversation dictionaries
            prompt_template: Template prompt to use
            
        Returns:
            List of conversation results with prompts
        """
        return self.templated_prompts_processor.run_templated_prompts(
            self.driver, conversations, prompt_template
        )

    def _get_demo_conversations(self, limit: int = 5) -> List[Dict[str, str]]:
        """Return a small set of demo conversations for offline/testing flows."""
        return DemoConversationGenerator.get_demo_conversations(limit)

    def ensure_login(self, allow_manual: bool = True, manual_timeout: int = 60) -> bool:
        """
        Ensure user is logged in with comprehensive fallback strategy.
        
        This is the PRIMARY login method that consolidates all login strategies.
        
        Strategy:
        1. Check if already logged in
        2. Try loading cookies if available
        3. Try automated login with credentials
        4. Fall back to manual login if allowed
        
        Args:
            allow_manual: Allow manual login if automated methods fail
            manual_timeout: Timeout for manual login in seconds
            
        Returns:
            True if logged in, False otherwise
        """
        if not self.driver:
            logger.error("No driver available for login")
            return False
        
        logger.info("🔐 Starting comprehensive login process...")
        
        # Step 1: Check if already logged in
        if self.is_logged_in():
            logger.info("✅ Already logged in")
            return True
        
        # Step 2: Navigate to ChatGPT if not already there
        if not self.navigate_to_chatgpt():
            logger.error("❌ Failed to navigate to ChatGPT")
            return False
        
        # Step 3: Use unified login utility
        success = ensure_login_unified(
            driver=self.driver,
            cookie_manager=self.cookie_manager,
            login_handler=self.login_handler,
            allow_manual=allow_manual,
            manual_timeout=manual_timeout,
            cookie_file=self.cookie_file
        )
        
        if success:
            logger.info("✅ Login successful with fallback strategy")
        else:
            logger.error("❌ All login methods failed")
        
        return success
    
    # Backward compatibility aliases
    def ensure_login_with_fallback(self, allow_manual: bool = True, manual_timeout: int = 60) -> bool:
        """Alias for ensure_login() - maintained for backward compatibility."""
        return self.ensure_login(allow_manual=allow_manual, manual_timeout=manual_timeout)
    
    def ensure_login_modern(self, allow_manual: bool = True, manual_timeout: int = 30) -> bool:
        """Alias for ensure_login() - maintained for backward compatibility."""
        return self.ensure_login(allow_manual=allow_manual, manual_timeout=manual_timeout)

def main():
    """Main function for command-line usage."""
    from dreamscape.scrapers.cli_handler import CLIHandler
    
    parser = CLIHandler.create_parser()
    args = parser.parse_args()
    
    success = CLIHandler.run_scraper_from_args(args, ChatGPTScraper)
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 