#!/usr/bin/env python3
"""
Search Storage
=============

Handles search operations and indexing for conversations.
"""

import logging
import sqlite3
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class SearchStorage:
    """Handles search operations and indexing for conversations."""
    
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._init_search_tables()
    
    def _init_search_tables(self):
        """Initialize search-related tables."""
        cursor = self.conn.cursor()
        
        # Create search index table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                content TEXT,
                role TEXT,
                timestamp TEXT,
                search_vector TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        
        # Create full-text search index
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts 
            USING fts5(conversation_id, content, role, timestamp)
        """)
        
        self.conn.commit()
    
    def search_conversations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search conversations using full-text search."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT conversation_id, content, role, timestamp, rank
            FROM conversations_fts 
            WHERE conversations_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'conversation_id': row[0],
                'content': row[1],
                'role': row[2],
                'timestamp': row[3],
                'rank': row[4]
            })
        
        return results
    
    def advanced_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Run advanced boolean search across conversations."""
        cursor = self.conn.cursor()
        
        # Parse boolean query and build SQL
        sql = """
            SELECT DISTINCT c.id, c.title, c.timestamp, c.message_count
            FROM conversations c
            JOIN conversations_fts fts ON c.id = fts.conversation_id
            WHERE fts MATCH ?
            ORDER BY c.timestamp DESC
            LIMIT ?
        """
        
        cursor.execute(sql, (query, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'title': row[1],
                'timestamp': row[2],
                'message_count': row[3]
            })
        
        return results 