"""
Base MMORPG System - Core Functionality
======================================

This module provides the base MMORPG system class with common functionality
that all MMORPG components inherit from.
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


class BaseMMORPGSystem(ABC):
    """Base class for all MMORPG system components."""
    
    def __init__(self, db_path: str = "dreamos_resume.db"):
        """Initialize the base MMORPG system."""
        self.db_path = db_path
        self.initialized = False
        self.last_updated = None
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database connection and schema."""
        try:
            # Ensure database file exists
            db_file = Path(self.db_path)
            if not db_file.exists():
                logger.info(f"Creating new MMORPG database: {self.db_path}")
            
            # Test connection
            conn = sqlite3.connect(self.db_path)
            conn.close()
            
            # Create schema
            self._create_schema()
            
            self.initialized = True
            logger.info(f"MMORPG database initialized: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize MMORPG database: {e}")
            raise
    
    def _create_schema(self):
        """Create database schema. Override in subclasses."""
        pass
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute a database query and return results."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute an update/insert/delete query."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            conn.close()
            
            self.last_updated = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"Database update failed: {e}")
            return False
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        results = self.execute_query(query, (table_name,))
        return len(results) > 0
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        return {
            "class": self.__class__.__name__,
            "db_path": self.db_path,
            "initialized": self.initialized,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate data for this system component."""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for this system component."""
        pass


class MMORPGComponent(BaseMMORPGSystem):
    """Base class for specific MMORPG components."""
    
    def __init__(self, db_path: str = "dreamos_resume.db", component_name: str = ""):
        """Initialize MMORPG component."""
        super().__init__(db_path)
        self.component_name = component_name
        self.data_cache = {}
        self.cache_timestamp = None
        
    def clear_cache(self):
        """Clear data cache."""
        self.data_cache.clear()
        self.cache_timestamp = None
    
    def is_cache_valid(self, max_age_seconds: int = 300) -> bool:
        """Check if cache is still valid."""
        if not self.cache_timestamp:
            return False
        
        age = (datetime.now() - self.cache_timestamp).total_seconds()
        return age < max_age_seconds
    
    def update_cache(self, data: Dict[str, Any]):
        """Update data cache."""
        self.data_cache.update(data)
        self.cache_timestamp = datetime.now()
    
    def get_cached_data(self, key: str, default: Any = None) -> Any:
        """Get data from cache."""
        return self.data_cache.get(key, default)
    
    def log_activity(self, activity: str, details: Dict[str, Any] = None):
        """Log component activity."""
        log_entry = {
            "component": self.component_name,
            "activity": activity,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"[{self.component_name}] {activity}")
        
        # Store in activity log table if it exists
        try:
            if self.table_exists("activity_log"):
                query = """
                    INSERT INTO activity_log (component, activity, details, timestamp)
                    VALUES (?, ?, ?, ?)
                """
                import json
                self.execute_update(query, (
                    self.component_name,
                    activity,
                    json.dumps(details or {}),
                    datetime.now().isoformat()
                ))
        except Exception as e:
            logger.warning(f"Failed to log activity: {e}")


class MMORPGError(Exception):
    """Base exception class for MMORPG system errors."""
    pass


class DatabaseError(MMORPGError):
    """Database-related error."""
    pass


class ValidationError(MMORPGError):
    """Data validation error."""
    pass


class GameStateError(MMORPGError):
    """Game state related error."""
    pass 