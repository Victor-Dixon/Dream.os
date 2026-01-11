#!/usr/bin/env python3
"""
Memory Database Storage
======================

Handles SQLite database operations for memory management.
Uses modular components for different operation types.
"""

import logging
import sqlite3
from typing import List, Dict, Optional, Any

from ...utils.context_mixin import ContextManagerMixin
from .schema_manager import SchemaManager
from .conversation_operations import ConversationOperations
from .message_operations import MessageOperations
from .prompt_operations import PromptOperations
from .index_operations import IndexOperations
from dreamscape.core.config import MEMORY_DB_PATH

logger = logging.getLogger(__name__)


class MemoryStorage(ContextManagerMixin):
    """Handles SQLite database operations for memory management."""
    
    def __init__(self, db_path: str = str(MEMORY_DB_PATH), db_manager=None):
        """
        Initialize the memory storage.
        
        Args:
            db_path: Path to SQLite database file
            db_manager: Optional thread-safe database manager
        """
        self.db_path = db_path
        self.db_manager = db_manager
        self.conn = None
        self.schema_manager = SchemaManager(db_path)
        self.conversation_ops = None
        self.message_ops = None
        self.prompt_ops = None
        self.index_ops = None
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with schema."""
        try:
            if self.db_manager:
                # Use thread-safe connection
                self.conn = self.db_manager.get_connection()
            else:
                # Use traditional connection
                self.conn = self.schema_manager.initialize_database()
            
            self._init_operations()
            
        except Exception as e:
            logger.error(f"Failed to initialize memory database: {e}")
            raise
    
    def _init_operations(self):
        """Initialize operation components."""
        self.conversation_ops = ConversationOperations(self.conn)
        self.message_ops = MessageOperations(self.conn)
        self.prompt_ops = PromptOperations(self.conn)
        self.index_ops = IndexOperations(self.conn)
    
    # Conversation operations
    def store_conversation(self, conversation_data: Dict[str, Any]) -> bool:
        """Store a conversation in the database."""
        return self.conversation_ops.store_conversation(conversation_data)
    
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a conversation by ID."""
        return self.conversation_ops.get_conversation_by_id(conversation_id)
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations ordered by creation date."""
        return self.conversation_ops.get_recent_conversations(limit)
    
    def get_conversations_chronological(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversations ordered chronologically by timestamp."""
        return self.conversation_ops.get_conversations_chronological(limit)
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about stored conversations."""
        return self.conversation_ops.get_conversation_stats()
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and its associated data."""
        return self.conversation_ops.delete_conversation(conversation_id)
    
    # Message operations
    def store_messages(self, conversation_id: str, messages: List[Dict[str, Any]]) -> bool:
        """Store messages for a conversation."""
        return self.message_ops.store_messages(conversation_id, messages)
    
    def get_messages_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Retrieve all messages for a conversation."""
        return self.message_ops.get_messages_by_conversation(conversation_id)
    
    def get_message_by_index(self, conversation_id: str, message_index: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific message by conversation ID and index."""
        return self.message_ops.get_message_by_index(conversation_id, message_index)
    
    def get_messages_by_role(self, conversation_id: str, role: str) -> List[Dict[str, Any]]:
        """Retrieve messages by role for a conversation."""
        return self.message_ops.get_messages_by_role(conversation_id, role)
    
    def update_message(self, conversation_id: str, message_index: int, content: str) -> bool:
        """Update a specific message."""
        return self.message_ops.update_message(conversation_id, message_index, content)
    
    def delete_message(self, conversation_id: str, message_index: int) -> bool:
        """Delete a specific message."""
        return self.message_ops.delete_message(conversation_id, message_index)
    
    def get_message_stats(self, conversation_id: str) -> Dict[str, Any]:
        """Get statistics about messages in a conversation."""
        return self.message_ops.get_message_stats(conversation_id)
    
    # Prompt operations
    def store_prompt(self, prompt_data: Dict[str, Any]) -> bool:
        """Store a prompt in the database."""
        return self.prompt_ops.store_prompt(prompt_data)
    
    def get_prompts_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Retrieve all prompts for a conversation."""
        return self.prompt_ops.get_prompts_by_conversation(conversation_id)
    
    def get_prompts_by_template(self, template_name: str) -> List[Dict[str, Any]]:
        """Retrieve all prompts using a specific template."""
        return self.prompt_ops.get_prompts_by_template(template_name)
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific prompt by ID."""
        return self.prompt_ops.get_prompt_by_id(prompt_id)
    
    def update_prompt(self, prompt_id: int, prompt_data: Dict[str, Any]) -> bool:
        """Update a specific prompt."""
        return self.prompt_ops.update_prompt(prompt_id, prompt_data)
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """Delete a specific prompt."""
        return self.prompt_ops.delete_prompt(prompt_id)
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        """Get statistics about stored prompts."""
        return self.prompt_ops.get_prompt_stats()
    
    def get_recent_prompts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent prompts ordered by creation date."""
        return self.prompt_ops.get_recent_prompts(limit)
    
    # Index operations
    def store_memory_index(self, index_data: Dict[str, Any]) -> bool:
        """Store memory index data."""
        return self.index_ops.store_memory_index(index_data)
    
    def get_index_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Retrieve memory index data for a conversation."""
        return self.index_ops.get_index_by_conversation(conversation_id)
    
    def get_index_by_content_type(self, content_type: str) -> List[Dict[str, Any]]:
        """Retrieve memory index data by content type."""
        return self.index_ops.get_index_by_content_type(content_type)
    
    def get_index_by_hash(self, content_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieve memory index data by content hash."""
        return self.index_ops.get_index_by_hash(content_hash)
    
    def update_index(self, index_id: int, index_data: Dict[str, Any]) -> bool:
        """Update memory index data."""
        return self.index_ops.update_index(index_id, index_data)
    
    def delete_index(self, index_id: int) -> bool:
        """Delete memory index data."""
        return self.index_ops.delete_index(index_id)
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about memory index data."""
        return self.index_ops.get_index_stats()
    
    def search_by_content_type(self, content_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memory indices by content type."""
        return self.index_ops.search_by_content_type(content_type, limit)
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 