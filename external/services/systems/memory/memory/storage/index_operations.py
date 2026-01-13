#!/usr/bin/env python3
"""
Memory Index Operations
======================

Handles memory index CRUD operations for the memory system.
"""

import logging
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class IndexOperations:
    """Handles memory index CRUD operations."""
    
    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize index operations.
        
        Args:
            conn: SQLite database connection
        """
        self.conn = conn
    
    def store_memory_index(self, index_data: Dict[str, Any]) -> bool:
        """
        Store memory index data.
        
        Args:
            index_data: Index data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            conversation_id = index_data.get('conversation_id')
            content_type = index_data.get('content_type', '')
            content_hash = index_data.get('content_hash', '')
            vector_data = json.dumps(index_data.get('vector_data', {}))
            
            cursor.execute("""
                INSERT INTO memory_index 
                (conversation_id, content_type, content_hash, vector_data)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, content_type, content_hash, vector_data))
            
            self.conn.commit()
            logger.info(f"Stored memory index for conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store memory index: {e}")
            return False
    
    def get_index_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve memory index data for a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of index data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM memory_index 
                WHERE conversation_id = ? 
                ORDER BY created_at ASC
            """, (conversation_id,))
            
            indices = []
            for row in cursor.fetchall():
                index_data = dict(row)
                # Parse JSON fields
                if index_data.get('vector_data'):
                    index_data['vector_data'] = json.loads(index_data['vector_data'])
                indices.append(index_data)
            
            return indices
            
        except Exception as e:
            logger.error(f"Failed to get memory index for conversation {conversation_id}: {e}")
            return []
    
    def get_index_by_content_type(self, content_type: str) -> List[Dict[str, Any]]:
        """
        Retrieve memory index data by content type.
        
        Args:
            content_type: Content type filter
            
        Returns:
            List of index data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM memory_index 
                WHERE content_type = ? 
                ORDER BY created_at DESC
            """, (content_type,))
            
            indices = []
            for row in cursor.fetchall():
                index_data = dict(row)
                # Parse JSON fields
                if index_data.get('vector_data'):
                    index_data['vector_data'] = json.loads(index_data['vector_data'])
                indices.append(index_data)
            
            return indices
            
        except Exception as e:
            logger.error(f"Failed to get memory index for content type {content_type}: {e}")
            return []
    
    def get_index_by_hash(self, content_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve memory index data by content hash.
        
        Args:
            content_hash: Content hash
            
        Returns:
            Index data or None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM memory_index WHERE content_hash = ?
            """, (content_hash,))
            
            row = cursor.fetchone()
            if row:
                index_data = dict(row)
                # Parse JSON fields
                if index_data.get('vector_data'):
                    index_data['vector_data'] = json.loads(index_data['vector_data'])
                return index_data
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get memory index for hash {content_hash}: {e}")
            return None
    
    def update_index(self, index_id: int, index_data: Dict[str, Any]) -> bool:
        """
        Update memory index data.
        
        Args:
            index_id: Index ID
            index_data: Updated index data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            content_type = index_data.get('content_type', '')
            content_hash = index_data.get('content_hash', '')
            vector_data = json.dumps(index_data.get('vector_data', {}))
            
            cursor.execute("""
                UPDATE memory_index 
                SET content_type = ?, content_hash = ?, vector_data = ?
                WHERE id = ?
            """, (content_type, content_hash, vector_data, index_id))
            
            self.conn.commit()
            logger.info(f"Updated memory index: {index_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update memory index {index_id}: {e}")
            return False
    
    def delete_index(self, index_id: int) -> bool:
        """
        Delete memory index data.
        
        Args:
            index_id: Index ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM memory_index WHERE id = ?", (index_id,))
            
            self.conn.commit()
            logger.info(f"Deleted memory index: {index_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete memory index {index_id}: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about memory index data.
        
        Returns:
            Dictionary with index statistics
        """
        try:
            cursor = self.conn.cursor()
            
            # Total indices
            cursor.execute("SELECT COUNT(*) FROM memory_index")
            total_indices = cursor.fetchone()[0]
            
            # Indices by content type
            cursor.execute("""
                SELECT content_type, COUNT(*) as count 
                FROM memory_index 
                GROUP BY content_type
            """)
            
            content_type_counts = {}
            for row in cursor.fetchall():
                content_type_counts[row[0]] = row[1]
            
            # Unique conversations with indices
            cursor.execute("SELECT COUNT(DISTINCT conversation_id) FROM memory_index")
            unique_conversations = cursor.fetchone()[0]
            
            return {
                'total_indices': total_indices,
                'content_type_counts': content_type_counts,
                'unique_conversations': unique_conversations
            }
            
        except Exception as e:
            logger.error(f"Failed to get memory index stats: {e}")
            return {}
    
    def search_by_content_type(self, content_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search memory indices by content type.
        
        Args:
            content_type: Content type to search for
            limit: Maximum number of results
            
        Returns:
            List of matching index data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM memory_index 
                WHERE content_type = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (content_type, limit))
            
            indices = []
            for row in cursor.fetchall():
                index_data = dict(row)
                # Parse JSON fields
                if index_data.get('vector_data'):
                    index_data['vector_data'] = json.loads(index_data['vector_data'])
                indices.append(index_data)
            
            return indices
            
        except Exception as e:
            logger.error(f"Failed to search memory indices by content type {content_type}: {e}")
            return [] 