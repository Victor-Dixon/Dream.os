#!/usr/bin/env python3
"""
Memory Prompt Operations
=======================

Handles prompt CRUD operations for the memory system.
"""

import logging
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class PromptOperations:
    """Handles prompt CRUD operations."""
    
    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize prompt operations.
        
        Args:
            conn: SQLite database connection
        """
        self.conn = conn
    
    def store_prompt(self, prompt_data: Dict[str, Any]) -> bool:
        """
        Store a prompt in the database.
        
        Args:
            prompt_data: Prompt data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            conversation_id = prompt_data.get('conversation_id')
            prompt_text = prompt_data.get('prompt_text', '')
            response_text = prompt_data.get('response_text', '')
            template_name = prompt_data.get('template_name', '')
            
            cursor.execute("""
                INSERT INTO prompts 
                (conversation_id, prompt_text, response_text, template_name)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, prompt_text, response_text, template_name))
            
            self.conn.commit()
            logger.info(f"Stored prompt for conversation: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store prompt: {e}")
            return False
    
    def get_prompts_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all prompts for a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of prompt data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts 
                WHERE conversation_id = ? 
                ORDER BY created_at ASC
            """, (conversation_id,))
            
            prompts = []
            for row in cursor.fetchall():
                prompts.append(dict(row))
            
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to get prompts for conversation {conversation_id}: {e}")
            return []
    
    def get_prompts_by_template(self, template_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve all prompts using a specific template.
        
        Args:
            template_name: Template name
            
        Returns:
            List of prompt data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts 
                WHERE template_name = ? 
                ORDER BY created_at DESC
            """, (template_name,))
            
            prompts = []
            for row in cursor.fetchall():
                prompts.append(dict(row))
            
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to get prompts for template {template_name}: {e}")
            return []
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific prompt by ID.
        
        Args:
            prompt_id: Prompt ID
            
        Returns:
            Prompt data or None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts WHERE id = ?
            """, (prompt_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            logger.error(f"Failed to get prompt {prompt_id}: {e}")
            return None
    
    def update_prompt(self, prompt_id: int, prompt_data: Dict[str, Any]) -> bool:
        """
        Update a specific prompt.
        
        Args:
            prompt_id: Prompt ID
            prompt_data: Updated prompt data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            
            prompt_text = prompt_data.get('prompt_text', '')
            response_text = prompt_data.get('response_text', '')
            template_name = prompt_data.get('template_name', '')
            
            cursor.execute("""
                UPDATE prompts 
                SET prompt_text = ?, response_text = ?, template_name = ?
                WHERE id = ?
            """, (prompt_text, response_text, template_name, prompt_id))
            
            self.conn.commit()
            logger.info(f"Updated prompt: {prompt_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update prompt {prompt_id}: {e}")
            return False
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """
        Delete a specific prompt.
        
        Args:
            prompt_id: Prompt ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            
            self.conn.commit()
            logger.info(f"Deleted prompt: {prompt_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete prompt {prompt_id}: {e}")
            return False
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored prompts.
        
        Returns:
            Dictionary with prompt statistics
        """
        try:
            cursor = self.conn.cursor()
            
            # Total prompts
            cursor.execute("SELECT COUNT(*) FROM prompts")
            total_prompts = cursor.fetchone()[0]
            
            # Prompts by template
            cursor.execute("""
                SELECT template_name, COUNT(*) as count 
                FROM prompts 
                GROUP BY template_name
            """)
            
            template_counts = {}
            for row in cursor.fetchall():
                template_counts[row[0]] = row[1]
            
            # Average prompt length
            cursor.execute("SELECT AVG(LENGTH(prompt_text)) as avg_length FROM prompts")
            avg_prompt_length = cursor.fetchone()[0] or 0
            
            # Average response length
            cursor.execute("SELECT AVG(LENGTH(response_text)) as avg_length FROM prompts")
            avg_response_length = cursor.fetchone()[0] or 0
            
            return {
                'total_prompts': total_prompts,
                'template_counts': template_counts,
                'avg_prompt_length': round(avg_prompt_length, 2),
                'avg_response_length': round(avg_response_length, 2)
            }
            
        except Exception as e:
            logger.error(f"Failed to get prompt stats: {e}")
            return {}
    
    def get_recent_prompts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent prompts ordered by creation date.
        
        Args:
            limit: Maximum number of prompts to return
            
        Returns:
            List of prompt data
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            prompts = []
            for row in cursor.fetchall():
                prompts.append(dict(row))
            
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to get recent prompts: {e}")
            return [] 