#!/usr/bin/env python3
"""
Memory Database Schema Manager
=============================

Handles database initialization and schema creation for the memory system.
"""

import logging
import sqlite3
from typing import Optional

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages database schema creation and initialization."""
    
    def __init__(self, db_path: str):
        """
        Initialize the schema manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
    
    def initialize_database(self) -> sqlite3.Connection:
        """
        Initialize the database with proper schema.
        
        Returns:
            SQLite connection with initialized schema
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Create tables
            self._create_tables(conn)
            
            logger.info(f"Database initialized successfully: {self.db_path}")
            return conn
            
        except Exception as e:
            logger.error(f"Failed to initialize memory database: {e}")
            raise
    
    def _create_tables(self, conn: sqlite3.Connection):
        """Create all required database tables."""
        cursor = conn.cursor()
        
        # Create conversations table
        self._create_conversations_table(cursor)
        
        # Create messages table
        self._create_messages_table(cursor)
        
        # Create prompts table
        self._create_prompts_table(cursor)
        
        # Create memory_index table
        self._create_memory_index_table(cursor)
        
        conn.commit()
    
    def _create_conversations_table(self, cursor: sqlite3.Cursor):
        """Create or update conversations table."""
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if not columns:
            # Table doesn't exist, create it
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    timestamp TEXT,
                    message_count INTEGER,
                    word_count INTEGER,
                    content_summary TEXT,
                    topics TEXT,
                    sentiment TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            logger.info("Created conversations table")
        else:
            # Table exists, check for missing columns
            self._add_missing_columns(cursor, 'conversations', columns)
    
    def _create_messages_table(self, cursor: sqlite3.Cursor):
        """Create or update messages table."""
        cursor.execute("PRAGMA table_info(messages)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if not columns:
            cursor.execute("""
                CREATE TABLE messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    message_index INTEGER,
                    role TEXT,
                    content TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            logger.info("Created messages table")
    
    def _create_prompts_table(self, cursor: sqlite3.Cursor):
        """Create or update prompts table."""
        cursor.execute("PRAGMA table_info(prompts)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if not columns:
            cursor.execute("""
                CREATE TABLE prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    prompt_text TEXT,
                    response_text TEXT,
                    template_name TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            logger.info("Created prompts table")
    
    def _create_memory_index_table(self, cursor: sqlite3.Cursor):
        """Create or update memory_index table."""
        cursor.execute("PRAGMA table_info(memory_index)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if not columns:
            cursor.execute("""
                CREATE TABLE memory_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    content_type TEXT,
                    content_hash TEXT,
                    vector_data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            logger.info("Created memory_index table")
    
    def _add_missing_columns(self, cursor: sqlite3.Cursor, table_name: str, existing_columns: list):
        """Add missing columns to existing table."""
        required_columns = {
            'conversations': ['content_summary', 'topics', 'sentiment', 'word_count']
        }
        
        if table_name in required_columns:
            for column in required_columns[table_name]:
                if column not in existing_columns:
                    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT")
                    logger.info(f"Added {column} column to {table_name} table")
    
    def get_table_info(self, table_name: str) -> list:
        """
        Get information about a table's columns.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        conn.close()
        return columns 