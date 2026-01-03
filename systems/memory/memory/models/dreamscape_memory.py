#!/usr/bin/env python3
"""
Dreamscape Memory Model
======================

Manages the continuous MMORPG storyline across conversations.
Handles memory state, quest progression, and story continuity.
"""

import logging
import json
import sqlite3
import threading
import time
from contextlib import contextmanager
from typing import Dict, List, Optional, Any
from datetime import datetime
from dreamscape.core.config import MEMORY_DB_PATH

logger = logging.getLogger(__name__)


class DreamscapeMemory:
    """
    Manages the continuous MMORPG storyline across conversations.
    Handles memory state, quest progression, and story continuity.
    """
    
    def __init__(self, db_path: str = str(MEMORY_DB_PATH)):
        self.db_path = db_path
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._init_database()
    
    def _init_database(self):
        """Initialize the dreamscape database tables."""
        try:
            # Use WAL mode for better concurrent access
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")
            self.conn.execute("PRAGMA cache_size=10000")
            self.conn.execute("PRAGMA temp_store=MEMORY")
            self.conn.row_factory = sqlite3.Row
            
            # Create dreamscape-specific tables
            self._create_dreamscape_schema()
            logger.info("[OK] Dreamscape memory database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize dreamscape database: {e}")
            raise
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections with retry logic."""
        max_retries = 3
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            try:
                with self._lock:
                    yield self.conn
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"Database locked, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise
            except Exception as e:
                logger.error(f"Database operation failed: {e}")
                raise
    
    def _create_dreamscape_schema(self):
        """Create dreamscape-specific database schema."""
        schema_sql = """
        CREATE TABLE IF NOT EXISTS dreamscape_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            memory_state TEXT,
            skill_levels TEXT,
            stabilized_domains TEXT,
            unlocked_protocols TEXT,
            completed_quests TEXT,
            active_quests TEXT,
            architect_tier TEXT,
            tier_progress REAL,
            narrative_summary TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        );
        
        CREATE TABLE IF NOT EXISTS dreamscape_quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quest_name TEXT NOT NULL,
            quest_type TEXT DEFAULT 'main',
            description TEXT,
            status TEXT DEFAULT 'active',
            difficulty TEXT DEFAULT 'normal',
            rewards TEXT,
            prerequisites TEXT,
            started_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            conversation_id TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_dreamscape_conversation ON dreamscape_memory(conversation_id);
        CREATE INDEX IF NOT EXISTS idx_quests_status ON dreamscape_quests(status);
        """
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(schema_sql)
            conn.commit()
            logger.info("[OK] Dreamscape schema created/verified")
    
    def get_current_memory_state(self) -> Dict[str, Any]:
        """Get the current memory state for the dreamscape template."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get latest memory state
                cursor.execute("""
                    SELECT * FROM dreamscape_memory 
                    ORDER BY created_at DESC 
                    LIMIT 1
                """)
                
                latest = cursor.fetchone()
                if latest:
                    return {
                        "skill_levels": json.loads(latest['skill_levels']) if latest['skill_levels'] else {},
                        "stabilized_domains": json.loads(latest['stabilized_domains']) if latest['stabilized_domains'] else [],
                        "unlocked_protocols": json.loads(latest['unlocked_protocols']) if latest['unlocked_protocols'] else [],
                        "completed_quests": json.loads(latest['completed_quests']) if latest['completed_quests'] else [],
                        "active_quests": json.loads(latest['active_quests']) if latest['active_quests'] else [],
                        "architect_tier": latest['architect_tier'] or "Tier 1 - Novice",
                        "tier_progress": latest['tier_progress'] or 0.0,
                        "narrative_summary": latest['narrative_summary'] or ""
                    }
                else:
                    # Return default state if no memory exists
                    return {
                        "skill_levels": {},
                        "stabilized_domains": [],
                        "unlocked_protocols": [],
                        "completed_quests": [],
                        "active_quests": [],
                        "architect_tier": "Tier 1 - Novice",
                        "tier_progress": 0.0,
                        "narrative_summary": ""
                    }
                    
        except Exception as e:
            logger.error(f"Failed to get current memory state: {e}")
            return {
                "skill_levels": {},
                "stabilized_domains": [],
                "unlocked_protocols": [],
                "completed_quests": [],
                "active_quests": [],
                "architect_tier": "Tier 1 - Novice",
                "tier_progress": 0.0,
                "narrative_summary": ""
            }
    
    def update_memory_state(self, conversation_id: str, memory_update: Dict[str, Any], narrative: str = "") -> bool:
        """Update the memory state with new information from a conversation."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Parse memory update
                skill_levels = memory_update.get('skill_level_advancements', {})
                stabilized_domains = memory_update.get('newly_stabilized_domains', [])
                unlocked_protocols = memory_update.get('newly_unlocked_protocols', [])
                completed_quests = memory_update.get('quest_completions', [])
                new_quests = memory_update.get('new_quests_accepted', [])
                tier_progression = memory_update.get('architect_tier_progression', {})
                
                # Insert new memory state
                cursor.execute("""
                    INSERT INTO dreamscape_memory 
                    (conversation_id, memory_state, skill_levels, stabilized_domains, 
                     unlocked_protocols, completed_quests, active_quests, architect_tier, 
                     tier_progress, narrative_summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    conversation_id,
                    json.dumps(memory_update),
                    json.dumps(skill_levels),
                    json.dumps(stabilized_domains),
                    json.dumps(unlocked_protocols),
                    json.dumps(completed_quests),
                    json.dumps(new_quests),
                    tier_progression.get('current_tier', 'Tier 1 - Novice'),
                    tier_progression.get('progress_to_next_tier', 0.0),
                    narrative
                ))
                
                conn.commit()
                logger.info(f"[OK] Updated dreamscape memory for conversation: {conversation_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to update memory state: {e}")
            return False
    
    def get_storyline_progression(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the storyline progression in chronological order."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT dm.*, c.title, c.timestamp
                    FROM dreamscape_memory dm
                    JOIN conversations c ON dm.conversation_id = c.id
                    ORDER BY dm.created_at ASC
                    LIMIT ?
                """, (limit,))
                
                progression = []
                for row in cursor.fetchall():
                    progression.append({
                        "conversation_id": row['conversation_id'],
                        "title": row['title'],
                        "timestamp": row['timestamp'],
                        "narrative": row['narrative_summary'],
                        "memory_state": json.loads(row['memory_state']) if row['memory_state'] else {},
                        "architect_tier": row['architect_tier'],
                        "tier_progress": row['tier_progress']
                    })
                
                return progression
                
        except Exception as e:
            logger.error(f"Failed to get storyline progression: {e}")
            return []
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close() 