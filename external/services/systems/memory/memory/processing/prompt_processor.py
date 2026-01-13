#!/usr/bin/env python3
"""
Memory Prompt Processor
======================

Processes and manages prompts in the memory system.
"""

import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MemoryPromptProcessor:
    """Processes and manages prompts in the memory system."""
    
    def __init__(self, storage):
        self.storage = storage
    
    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a prompt for storage."""
        processed = {
            'conversation_id': prompt_data.get('conversation_id'),
            'prompt_text': prompt_data.get('prompt_text', ''),
            'prompt_type': prompt_data.get('prompt_type', 'general'),
            'prompt_category': prompt_data.get('prompt_category', 'general'),
            'prompt_effectiveness': prompt_data.get('prompt_effectiveness', 0.0),
            'timestamp': datetime.now().isoformat()
        }
        return processed
    
    def analyze_prompt_effectiveness(self, prompt_text: str, response_quality: float) -> float:
        """Analyze prompt effectiveness based on response quality."""
        # Simple effectiveness scoring
        base_score = response_quality
        
        # Adjust based on prompt characteristics
        if len(prompt_text) > 100:
            base_score += 0.1  # Longer prompts tend to be more specific
        
        if '?' in prompt_text:
            base_score += 0.05  # Questions are often more effective
        
        return min(1.0, max(0.0, base_score)) 