#!/usr/bin/env python3
"""
Memory Conversation Operations
=============================

Handles conversation CRUD operations for the memory system.
"""

import logging
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class ConversationOperations:
    """Handles conversation CRUD operations."""
    
    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize conversation operations.
        
        Args:
            conn: SQLite database connection
        """
        self.conn = conn
    
    def store_conversation(self, conversation_data: Dict[str, Any]) -> bool:
        """
        Store a conversation in the database.
        
        Args:
            conversation_data: Conversation data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            # Extract conversation data
            conversation_id = conversation_data.get('id')
            title = conversation_data.get('title', '')
            timestamp = conversation_data.get('timestamp', '')
            message_count = conversation_data.get('message_count', 0)
            content_summary = conversation_data.get('content_summary', '')
            topics = json.dumps(conversation_data.get('topics', []))
            sentiment = conversation_data.get('sentiment', '')
            
            # Insert or update conversation
            cursor.execute("""
                INSERT OR REPLACE INTO conversations 
                (id, title, timestamp, message_count, content_summary, topics, sentiment)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (conversation_id, title, timestamp, message_count, 
                  content_summary, topics, sentiment))
            
            self.conn.commit()
            logger.info(f"Stored conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")
            return False
    
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a conversation by ID.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation data or None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM conversations WHERE id = ?
            """, (conversation_id,))
            
            row = cursor.fetchone()
            if row:
                conversation = dict(row)
                # Parse JSON fields
                if conversation.get('topics'):
                    conversation['topics'] = json.loads(conversation['topics'])
                return conversation
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get conversation {conversation_id}: {e}")
            return None
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversations ordered by creation date.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversation data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM conversations 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            conversations = []
            for row in cursor.fetchall():
                conversation = dict(row)
                # Parse JSON fields
                if conversation.get('topics'):
                    conversation['topics'] = json.loads(conversation['topics'])
                conversations.append(conversation)
            
            return conversations
            
        except Exception as e:
            logger.error(f"Failed to get recent conversations: {e}")
            return []
    
    def get_conversations_chronological(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversations ordered chronologically by timestamp.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversation data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, title, timestamp, message_count, content_summary, topics, sentiment, created_at
                FROM conversations 
                ORDER BY created_at ASC, timestamp ASC 
                LIMIT ?
            """, (limit,))
            
            conversations = []
            for row in cursor.fetchall():
                try:
                    conversation = {
                        'id': row[0],
                        'title': row[1] or 'Untitled',
                        'timestamp': row[2] or '',
                        'message_count': row[3] or 0,
                        'content_summary': row[4] or '',
                        'topics': row[5] or '[]',
                        'sentiment': row[6] or 'neutral',
                        'created_at': row[7] or row[2] or ''  # Use timestamp as fallback
                    }
                    
                    # Parse JSON fields safely
                    if conversation.get('topics') and conversation['topics'] != '[]':
                        try:
                            conversation['topics'] = json.loads(conversation['topics'])
                        except (json.JSONDecodeError, TypeError):
                            conversation['topics'] = []
                    else:
                        conversation['topics'] = []
                    
                    conversations.append(conversation)
                except Exception as e:
                    logger.warning(f"Skipping conversation with invalid data: {e}")
                    continue
            
            return conversations
            
        except Exception as e:
            logger.error(f"Failed to get chronological conversations: {e}")
            return []
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored conversations.
        
        Returns:
            Dictionary with conversation statistics
        """
        try:
            cursor = self.conn.cursor()
            
            # Total conversations
            cursor.execute("SELECT COUNT(*) FROM conversations")
            total_conversations = cursor.fetchone()[0]
            
            # Total messages
            cursor.execute("SELECT SUM(message_count) FROM conversations")
            total_messages = cursor.fetchone()[0] or 0
            
            # Average messages per conversation
            avg_messages = total_messages / total_conversations if total_conversations > 0 else 0
            
            # Date range
            cursor.execute("""
                SELECT MIN(created_at), MAX(created_at) 
                FROM conversations
            """)
            date_range = cursor.fetchone()
            earliest_date = date_range[0] if date_range[0] else None
            latest_date = date_range[1] if date_range[1] else None
            
            return {
                'total_conversations': total_conversations,
                'total_messages': total_messages,
                'avg_messages_per_conversation': round(avg_messages, 2),
                'earliest_date': earliest_date,
                'latest_date': latest_date
            }
            
        except Exception as e:
            logger.error(f"Failed to get conversation stats: {e}")
            return {}
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation and its associated data.
        
        Args:
            conversation_id: Conversation ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            # Delete associated messages
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            
            # Delete associated prompts
            cursor.execute("DELETE FROM prompts WHERE conversation_id = ?", (conversation_id,))
            
            # Delete associated memory index entries
            cursor.execute("DELETE FROM memory_index WHERE conversation_id = ?", (conversation_id,))
            
            # Delete conversation
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            
            self.conn.commit()
            logger.info(f"Deleted conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete conversation {conversation_id}: {e}")
            return False 
