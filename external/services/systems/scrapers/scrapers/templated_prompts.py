"""
Templated Prompts Processor
Handles processing of templated prompts on conversations.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class TemplatedPromptsProcessor:
    """Handles processing of templated prompts on conversations."""
    
    def __init__(self, conversation_extractor):
        """
        Initialize the templated prompts processor.
        
        Args:
            conversation_extractor: Conversation extractor instance
        """
        self.conversation_extractor = conversation_extractor
    
    def run_templated_prompts(self, driver, conversations: List[Dict[str, str]], prompt_template: str) -> List[Dict[str, str]]:
        """
        Run templated prompts on a list of conversations.
        
        Args:
            driver: Selenium webdriver instance
            conversations: List of conversation dictionaries
            prompt_template: Template prompt to use
            
        Returns:
            List of conversation results with prompts
        """
        results = []
        
        for conversation in conversations:
            try:
                logger.info(f"Processing conversation: {conversation.get('title', 'Unknown')}")
                
                # Enter conversation
                if not self.conversation_extractor.enter_conversation(driver, conversation['url']):
                    logger.warning(f"Failed to enter conversation: {conversation.get('title', 'Unknown')}")
                    continue
                
                # Send templated prompt
                if self.conversation_extractor.send_prompt(driver, prompt_template):
                    # Get updated content
                    content = self.conversation_extractor.get_conversation_content(driver)
                    conversation['updated_content'] = content
                    results.append(conversation)
                    logger.info(f"✅ Processed conversation: {conversation.get('title', 'Unknown')}")
                else:
                    logger.warning(f"Failed to send prompt to: {conversation.get('title', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error processing conversation: {e}")
                continue
        
        return results 