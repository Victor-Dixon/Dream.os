#!/usr/bin/env python3
"""
Memory Prompt API
================

API for prompt-related memory operations.
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class MemoryPromptAPI:
    """API for prompt-related memory operations."""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def search_prompts(self, query: str = None, category: str = None, 
                      prompt_type: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search prompts with filters."""
        return self.memory.search_prompts(query, category, prompt_type, limit)
    
    def get_prompts_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get prompts for a specific conversation."""
        return self.memory.get_prompts_by_conversation(conversation_id)
    
    def get_prompt_categories(self) -> List[str]:
        """Get available prompt categories."""
        return self.memory.get_prompt_categories()
    
    def get_prompt_types(self) -> List[str]:
        """Get available prompt types."""
        return self.memory.get_prompt_types()
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        """Get prompt statistics."""
        return self.memory.get_prompt_stats()
    
    def get_best_prompts(self, category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get best performing prompts."""
        prompts = self.search_prompts(category=category, limit=limit)
        # Sort by effectiveness
        return sorted(prompts, key=lambda x: x.get('prompt_effectiveness', 0), reverse=True) 