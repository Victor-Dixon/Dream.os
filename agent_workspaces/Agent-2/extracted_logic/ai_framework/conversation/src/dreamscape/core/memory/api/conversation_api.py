#!/usr/bin/env python3
"""
Memory Conversation API
======================

API for conversation-related memory operations.
"""

import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class MemoryConversationAPI:
    """API for conversation-related memory operations."""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def search_conversations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search conversations by content."""
        return self.memory.search_conversations(query, limit)
    
    def advanced_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Advanced conversation search."""
        return self.memory.advanced_search(query, limit)
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by ID."""
        return self.memory.get_conversation_by_id(conversation_id)
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations."""
        return self.memory.get_recent_conversations(limit)
    
    def get_conversations_by_ids(self, conversation_ids: List[str]) -> List[Dict[str, Any]]:
        """Get multiple conversations by IDs."""
        conversations = []
        for conv_id in conversation_ids:
            conv = self.memory.get_conversation_by_id(conv_id)
            if conv:
                conversations.append(conv)
        return conversations
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[str]:
        """Get conversation summary."""
        conv = self.memory.get_conversation_by_id(conversation_id)
        return conv.get('content_summary') if conv else None
    
    def get_conversation_metadata(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation metadata."""
        conv = self.memory.get_conversation_by_id(conversation_id)
        if conv:
            return {
                'id': conv['id'],
                'title': conv['title'],
                'timestamp': conv['timestamp'],
                'message_count': conv['message_count'],
                'topics': conv['topics'],
                'sentiment': conv['sentiment']
            }
        return {}
    
    def format_conversation_for_prompt(self, conversation: Dict[str, Any], max_length: int = 1000) -> str:
        """Format conversation for use in prompts."""
        if not conversation or 'messages' not in conversation:
            return ""
        
        formatted = f"Conversation: {conversation.get('title', 'Untitled')}\n\n"
        
        for msg in conversation['messages']:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            formatted += f"{role.title()}: {content}\n\n"
        
        # Truncate if too long
        if len(formatted) > max_length:
            formatted = formatted[:max_length] + "..."
        
        return formatted 
