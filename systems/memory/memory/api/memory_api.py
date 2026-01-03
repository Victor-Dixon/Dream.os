#!/usr/bin/env python3
"""
Memory API
=========

High-level Memory API for Dream.OS.

Provides simplified access to memory operations for agents and components.
"""

import logging
from typing import List, Dict, Optional, Any

from ...utils.context_mixin import ContextManagerMixin
from .conversation_api import MemoryConversationAPI
from .prompt_api import MemoryPromptAPI
from .agent_api import MemoryAgentAPI
from ..manager import MemoryManager
from dreamscape.core.config import MEMORY_DB_PATH

logger = logging.getLogger(__name__)


class MemoryAPI(ContextManagerMixin):
    """
    High-level Memory API for Dream.OS.
    
    Provides simplified access to memory operations for agents and components.
    """
    
    def __init__(self, db_path: str = str(MEMORY_DB_PATH)):
        """
        Initialize the Memory API.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._memory = None
        self._conversation_api = None
        self._prompt_api = None
        self._agent_api = None
    
    def _get_memory(self) -> MemoryManager:
        """Get or create MemoryManager instance."""
        if self._memory is None:
            self._memory = MemoryManager(self.db_path)
        return self._memory
    
    def _get_conversation_api(self) -> MemoryConversationAPI:
        """Get or create conversation API instance."""
        if self._conversation_api is None:
            self._conversation_api = MemoryConversationAPI(self._get_memory())
        return self._conversation_api
    
    def _get_prompt_api(self) -> MemoryPromptAPI:
        """Get or create prompt API instance."""
        if self._prompt_api is None:
            self._prompt_api = MemoryPromptAPI(self._get_memory())
        return self._prompt_api
    
    def _get_agent_api(self) -> MemoryAgentAPI:
        """Get or create agent API instance."""
        if self._agent_api is None:
            self._agent_api = MemoryAgentAPI(self._get_memory())
        return self._agent_api
    
    def close(self):
        """Close the memory connection."""
        if self._memory:
            self._memory.close()
            self._memory = None
            self._conversation_api = None
            self._prompt_api = None
            self._agent_api = None
    
    # Conversation operations
    def search_conversations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return self._get_conversation_api().search_conversations(query, limit)

    def advanced_search_conversations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Expose advanced conversation search."""
        return self._get_conversation_api().advanced_search(query, limit)
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        return self._get_conversation_api().get_conversation(conversation_id)
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get_conversation_api().get_recent_conversations(limit)
    
    def get_conversations_by_ids(self, conversation_ids: List[str]) -> List[Dict[str, Any]]:
        return self._get_conversation_api().get_conversations_by_ids(conversation_ids)
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[str]:
        return self._get_conversation_api().get_conversation_summary(conversation_id)
    
    def get_conversation_metadata(self, conversation_id: str) -> Dict[str, Any]:
        return self._get_conversation_api().get_conversation_metadata(conversation_id)
    
    def format_conversation_for_prompt(self, conversation: Dict[str, Any], max_length: int = 1000) -> str:
        return self._get_conversation_api().format_conversation_for_prompt(conversation, max_length)
    
    def batch_search(self, queries: List[str], limit_per_query: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """Search multiple queries at once."""
        results = {}
        for query in queries:
            results[query] = self.search_conversations(query, limit_per_query)
        return results
    
    def get_conversations_chronological(self, limit: int = None, offset: int = 0) -> List[Dict]:
        """Get conversations in chronological order."""
        return self._get_memory().get_conversations_chronological(limit or 10)
    
    def get_conversations_count(self) -> int:
        """Get total number of conversations."""
        return self._get_memory().get_conversations_count()
    
    # Prompt operations
    def search_prompts(self, query: str = None, category: str = None, prompt_type: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        return self._get_prompt_api().search_prompts(query, category, prompt_type, limit)
    
    def get_prompts_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        return self._get_prompt_api().get_prompts_by_conversation(conversation_id)
    
    def get_prompt_categories(self) -> List[str]:
        return self._get_prompt_api().get_prompt_categories()
    
    def get_prompt_types(self) -> List[str]:
        return self._get_prompt_api().get_prompt_types()
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        return self._get_prompt_api().get_prompt_stats()
    
    def get_best_prompts(self, category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get_prompt_api().get_best_prompts(category, limit)
    
    # Agent operations
    def get_agent_context(self, task: str, limit: int = 3) -> str:
        return self._get_agent_api().get_agent_context(task, limit)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        return self._get_agent_api().get_memory_stats()
    
    # General operations
    def ingest_conversations(self, conversations_dir: str = "data/conversations") -> int:
        return self._get_memory().ingest_conversations(conversations_dir)
    
    def is_memory_ready(self) -> bool:
        """Check if memory system is ready."""
        try:
            count = self.get_conversations_count()
            return count >= 0  # Any non-negative count means system is working
        except Exception:
            return False 