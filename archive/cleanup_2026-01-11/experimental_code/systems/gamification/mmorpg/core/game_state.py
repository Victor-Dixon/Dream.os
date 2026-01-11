"""
Game State Manager - MMORPG State Management
===========================================

This module handles game state management and persistence
for the MMORPG system.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .base_system import MMORPGComponent

logger = logging.getLogger(__name__)


class GameStateManager(MMORPGComponent):
    """Manages MMORPG game state and persistence."""
    
    def __init__(self, db_path: str = "dreamos_resume.db"):
        """Initialize the game state manager."""
        super().__init__(db_path, "GameStateManager")
        self.current_state = {}
        self._load_game_state()
    
    def _create_schema(self):
        """Create game state database schema."""
        try:
            schema = """
                CREATE TABLE IF NOT EXISTS game_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    data_type TEXT DEFAULT 'string',
                    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            
            self.execute_update(schema)
            logger.info("Game state database schema created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create game state schema: {e}")
            raise
    
    def _load_game_state(self):
        """Load game state from database."""
        try:
            if not self.table_exists("game_state"):
                self._create_schema()
                self._initialize_default_state()
                return
            
            # Load state from database
            state_data = self.execute_query("SELECT * FROM game_state")
            
            for item in state_data:
                key = item["key"]
                value = item["value"]
                data_type = item["data_type"]
                
                # Convert value based on type
                if data_type == "json":
                    try:
                        value = json.loads(value)
                    except:
                        value = {}
                elif data_type == "int":
                    value = int(value)
                elif data_type == "float":
                    value = float(value)
                elif data_type == "bool":
                    value = value.lower() == 'true'
                
                self.current_state[key] = value
            
            logger.info(f"Loaded {len(self.current_state)} game state items")
            
        except Exception as e:
            logger.error(f"Failed to load game state: {e}")
            self._initialize_default_state()
    
    def _initialize_default_state(self):
        """Initialize default game state."""
        default_state = {
            "player_name": "Victor",
            "player_level": 5,
            "player_tier": "Tier 1",
            "total_experience": 500,
            "active_quests": [],
            "completed_quests": [],
            "current_skills": 5,
            "game_version": "1.0.0",
            "last_played": datetime.now().isoformat()
        }
        
        for key, value in default_state.items():
            self.set_state(key, value)
        
        logger.info("Initialized default game state")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.current_state.get(key, default)
    
    def set_state(self, key: str, value: Any) -> bool:
        """Set a state value."""
        try:
            # Determine data type
            if isinstance(value, dict) or isinstance(value, list):
                data_type = "json"
                db_value = json.dumps(value)
            elif isinstance(value, int):
                data_type = "int"
                db_value = str(value)
            elif isinstance(value, float):
                data_type = "float"
                db_value = str(value)
            elif isinstance(value, bool):
                data_type = "bool"
                db_value = str(value).lower()
            else:
                data_type = "string"
                db_value = str(value)
            
            # Update in memory
            self.current_state[key] = value
            
            # Save to database
            query = """
                INSERT OR REPLACE INTO game_state (key, value, data_type, last_updated)
                VALUES (?, ?, ?, ?)
            """
            
            success = self.execute_update(query, (
                key,
                db_value,
                data_type,
                datetime.now().isoformat()
            ))
            
            if success:
                self.log_activity(f"Updated state: {key}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to set state {key}: {e}")
            return False
    
    def get_player_info(self) -> Dict[str, Any]:
        """Get player information."""
        return {
            "name": self.get_state("player_name", "Victor"),
            "level": self.get_state("player_level", 5),
            "tier": self.get_state("player_tier", "Tier 1"),
            "experience": self.get_state("total_experience", 500),
            "skills": self.get_state("current_skills", 5)
        }
    
    def update_player_info(self, **kwargs) -> bool:
        """Update player information."""
        try:
            for key, value in kwargs.items():
                state_key = f"player_{key}"
                self.set_state(state_key, value)
            
            # Update last played
            self.set_state("last_played", datetime.now().isoformat())
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update player info: {e}")
            return False
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get complete game state."""
        player_info = self.get_player_info()
        
        return {
            "player": player_info["name"],
            "level": player_info["level"],
            "tier": player_info["tier"],
            "skills": player_info["skills"],
            "experience": player_info["experience"],
            "last_played": self.get_state("last_played"),
            "game_version": self.get_state("game_version", "1.0.0")
        }
    
    def save_game_state(self) -> bool:
        """Force save current game state."""
        try:
            self.set_state("last_saved", datetime.now().isoformat())
            logger.info("Game state saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save game state: {e}")
            return False
    
    def reset_game_state(self) -> bool:
        """Reset game state to defaults."""
        try:
            # Clear current state
            self.current_state.clear()
            
            # Clear database
            self.execute_update("DELETE FROM game_state")
            
            # Reinitialize
            self._initialize_default_state()
            
            logger.info("Game state reset to defaults")
            return True
            
        except Exception as e:
            logger.error(f"Failed to reset game state: {e}")
            return False
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate game state data."""
        # Basic validation
        if not isinstance(data, dict):
            return False
        
        # Check for required fields in player info
        required_fields = ["player_name", "player_level"]
        for field in required_fields:
            if field in data:
                if field == "player_level" and not isinstance(data[field], int):
                    return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get game state statistics."""
        return {
            "total_state_items": len(self.current_state),
            "player_name": self.get_state("player_name", "Victor"),
            "player_level": self.get_state("player_level", 5),
            "total_experience": self.get_state("total_experience", 500),
            "last_played": self.get_state("last_played"),
            "game_version": self.get_state("game_version", "1.0.0")
        } 