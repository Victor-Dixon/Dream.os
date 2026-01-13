#!/usr/bin/env python3
"""
Memory Agent API
===============

API for agent-related memory operations.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MemoryAgentAPI:
    """API for agent-related memory operations."""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def get_agent_context(self, task: str, limit: int = 3) -> str:
        """Get relevant context for an agent task."""
        # Search for relevant conversations
        conversations = self.memory.search_conversations(task, limit)
        
        context_parts = []
        for conv in conversations:
            context_parts.append(self.memory.format_conversation_for_prompt(conv, max_length=500))
        
        return "\n\n".join(context_parts)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics for agents."""
        return self.memory.get_statistics() 