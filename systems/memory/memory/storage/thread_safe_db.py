#!/usr/bin/env python3
"""
Thread-Safe Database Connection Manager
======================================

Provides thread-safe database connections for the memory system.
Each thread gets its own SQLite connection to avoid threading issues.
"""

import sqlite3
import threading
import logging
from pathlib import Path
from typing import Optional
from dreamscape.core.config import MEMORY_DB_PATH

logger = logging.getLogger(__name__)


class ThreadSafeDBManager:
    """Thread-safe database connection manager."""
    
    def __init__(self, db_path: str):
        """
        Initialize the thread-safe database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self._local = threading.local()
        self._lock = threading.Lock()
        
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize the database schema
        self._init_database()
    
    def _init_database(self):
        """Initialize the database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    timestamp TEXT,
                    message_count INTEGER DEFAULT 0,
                    content_summary TEXT,
                    topics TEXT,
                    sentiment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create other necessary tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    content TEXT,
                    embedding BLOB,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            ''')
            
            conn.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a thread-local database connection.
        
        Returns:
            SQLite connection for the current thread
        """
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            # Create a new connection for this thread
            self._local.connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False
            )
            self._local.connection.row_factory = sqlite3.Row
            
            logger.debug(f"Created new database connection for thread {threading.current_thread().ident}")
        
        return self._local.connection
    
    def close_connection(self):
        """Close the current thread's database connection."""
        if hasattr(self._local, 'connection') and self._local.connection is not None:
            self._local.connection.close()
            self._local.connection = None
            logger.debug(f"Closed database connection for thread {threading.current_thread().ident}")
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Execute a query safely in the current thread.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            Query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an update query safely in the current thread.
        
        Args:
            query: SQL update query
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount


# Global thread-safe database manager instance
_thread_safe_db = None


def get_thread_safe_db(db_path: str = str(MEMORY_DB_PATH)) -> ThreadSafeDBManager:
    """
    Get the global thread-safe database manager.
    
    Args:
        db_path: Database file path
        
    Returns:
        Thread-safe database manager instance
    """
    global _thread_safe_db
    if _thread_safe_db is None:
        _thread_safe_db = ThreadSafeDBManager(db_path)
    return _thread_safe_db


def close_thread_connections():
    """Close all thread-local database connections."""
    global _thread_safe_db
    if _thread_safe_db is not None:
        _thread_safe_db.close_connection() 