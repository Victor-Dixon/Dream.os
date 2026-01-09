#!/usr/bin/env python3
"""
Memory Message Operations
========================

Handles message CRUD operations for the memory system.
"""

import logging
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class MessageOperations:
    """Handles message CRUD operations."""
    
    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize message operations.
        
        Args:
            conn: SQLite database connection
        """
        self.conn = conn
    
    def store_messages(self, conversation_id: str, messages: List[Dict[str, Any]]) -> bool:
        """
        Store messages for a conversation.
        
        Args:
            conversation_id: Conversation ID
            messages: List of message dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            for i, message in enumerate(messages):
                role = message.get('role', '')
                content = message.get('content', '')
                timestamp = message.get('timestamp', datetime.now().isoformat())
                
                cursor.execute("""
                    INSERT INTO messages 
                    (conversation_id, message_index, role, content, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (conversation_id, i, role, content, timestamp))
            
            self.conn.commit()
            logger.info(f"Stored {len(messages)} messages for conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store messages for conversation {conversation_id}: {e}")
            return False
    
    def get_messages_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all messages for a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of message data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM messages 
                WHERE conversation_id = ? 
                ORDER BY message_index ASC
            """, (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append(dict(row))
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages for conversation {conversation_id}: {e}")
            return []
    
    def get_message_by_index(self, conversation_id: str, message_index: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific message by conversation ID and index.
        
        Args:
            conversation_id: Conversation ID
            message_index: Message index
            
        Returns:
            Message data or None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM messages 
                WHERE conversation_id = ? AND message_index = ?
            """, (conversation_id, message_index))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            logger.error(f"Failed to get message {message_index} for conversation {conversation_id}: {e}")
            return None
    
    def get_messages_by_role(self, conversation_id: str, role: str) -> List[Dict[str, Any]]:
        """
        Retrieve messages by role for a conversation.
        
        Args:
            conversation_id: Conversation ID
            role: Message role (e.g., 'user', 'assistant')
            
        Returns:
            List of message data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM messages 
                WHERE conversation_id = ? AND role = ?
                ORDER BY message_index ASC
            """, (conversation_id, role))
            
            messages = []
            for row in cursor.fetchall():
                messages.append(dict(row))
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get {role} messages for conversation {conversation_id}: {e}")
            return []
    
    def update_message(self, conversation_id: str, message_index: int, 
                      content: str) -> bool:
        """
        Update a specific message.
        
        Args:
            conversation_id: Conversation ID
            message_index: Message index
            content: New message content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE messages 
                SET content = ? 
                WHERE conversation_id = ? AND message_index = ?
            """, (content, conversation_id, message_index))
            
            self.conn.commit()
            logger.info(f"Updated message {message_index} for conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update message {message_index} for conversation {conversation_id}: {e}")
            return False
    
    def delete_message(self, conversation_id: str, message_index: int) -> bool:
        """
        Delete a specific message.
        
        Args:
            conversation_id: Conversation ID
            message_index: Message index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM messages 
                WHERE conversation_id = ? AND message_index = ?
            """, (conversation_id, message_index))
            
            self.conn.commit()
            logger.info(f"Deleted message {message_index} for conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete message {message_index} for conversation {conversation_id}: {e}")
            return False
    
    def get_message_stats(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get statistics about messages in a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Dictionary with message statistics
        """
        try:
            cursor = self.conn.cursor()
            
            # Total messages
            cursor.execute("SELECT COUNT(*) FROM messages WHERE conversation_id = ?", (conversation_id,))
            total_messages = cursor.fetchone()[0]
            
            # Messages by role
            cursor.execute("""
                SELECT role, COUNT(*) as count 
                FROM messages 
                WHERE conversation_id = ? 
                GROUP BY role
            """, (conversation_id,))
            
            role_counts = {}
            for row in cursor.fetchall():
                role_counts[row[0]] = row[1]
            
            # Average message length
            cursor.execute("""
                SELECT AVG(LENGTH(content)) as avg_length 
                FROM messages 
                WHERE conversation_id = ?
            """, (conversation_id,))
            
            avg_length = cursor.fetchone()[0] or 0
            
            return {
                'total_messages': total_messages,
                'role_counts': role_counts,
                'avg_message_length': round(avg_length, 2)
            }
            
        except Exception as e:
            logger.error(f"Failed to get message stats for conversation {conversation_id}: {e}")
            return {} 