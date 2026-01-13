"""
Player Manager - MMORPG Player Management
========================================

This module handles player management and character data
for the MMORPG system.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

from .base_system import MMORPGComponent

logger = logging.getLogger(__name__)


@dataclass
class Player:
    """Represents a player in the MMORPG system."""
    id: str
    name: str
    level: int = 1
    experience: int = 0
    tier: str = "Tier 1"
    created_at: datetime = None
    last_active: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()


class PlayerManager(MMORPGComponent):
    """Manages player data and character information."""
    
    def __init__(self, db_path: str = "dreamos_resume.db"):
        """Initialize the player manager."""
        super().__init__(db_path, "PlayerManager")
        self.current_player = None
        self._load_current_player()
    
    def _create_schema(self):
        """Create player database schema."""
        try:
            schema = """
                CREATE TABLE IF NOT EXISTS players (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    experience INTEGER DEFAULT 0,
                    tier TEXT DEFAULT 'Tier 1',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_active TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_current BOOLEAN DEFAULT FALSE
                )
            """
            
            self.execute_update(schema)
            logger.info("Player database schema created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create player schema: {e}")
            raise
    
    def _load_current_player(self):
        """Load current player from database."""
        try:
            if not self.table_exists("players"):
                self._create_schema()
                self._create_default_player()
                return
            
            # Get current player
            players = self.execute_query("SELECT * FROM players WHERE is_current = 1 LIMIT 1")
            
            if players:
                player_data = players[0]
                self.current_player = Player(
                    id=player_data["id"],
                    name=player_data["name"],
                    level=player_data["level"],
                    experience=player_data["experience"],
                    tier=player_data["tier"],
                    created_at=datetime.fromisoformat(player_data["created_at"]),
                    last_active=datetime.fromisoformat(player_data["last_active"])
                )
                
                logger.info(f"Loaded current player: {self.current_player.name}")
            else:
                self._create_default_player()
                
        except Exception as e:
            logger.error(f"Failed to load current player: {e}")
            self._create_default_player()
    
    def _create_default_player(self):
        """Create default player."""
        import uuid
        
        player = Player(
            id=str(uuid.uuid4()),
            name="Victor",
            level=5,
            experience=500,
            tier="Tier 1"
        )
        
        self.create_player(player, set_as_current=True)
        logger.info("Created default player: Victor")
    
    def create_player(self, player: Player, set_as_current: bool = False) -> bool:
        """Create a new player."""
        try:
            # Insert player into database
            query = """
                INSERT OR REPLACE INTO players (id, name, level, experience, tier, created_at, last_active, is_current)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            success = self.execute_update(query, (
                player.id,
                player.name,
                player.level,
                player.experience,
                player.tier,
                player.created_at.isoformat(),
                player.last_active.isoformat(),
                set_as_current
            ))
            
            if success and set_as_current:
                # Clear other current players
                self.execute_update("UPDATE players SET is_current = 0 WHERE id != ?", (player.id,))
                self.current_player = player
                
            self.log_activity(f"Created player: {player.name}")
            return success
            
        except Exception as e:
            logger.error(f"Failed to create player: {e}")
            return False
    
    def get_player_info(self) -> Dict[str, Any]:
        """Get current player information."""
        if not self.current_player:
            return {
                "name": "Victor",
                "level": 5,
                "experience": 500,
                "tier": "Tier 1",
                "skills": []
            }
        
        return {
            "id": self.current_player.id,
            "name": self.current_player.name,
            "level": self.current_player.level,
            "experience": self.current_player.experience,
            "tier": self.current_player.tier,
            "created_at": self.current_player.created_at.isoformat(),
            "last_active": self.current_player.last_active.isoformat(),
            "skills": []  # Will be populated by SkillManager
        }
    
    def update_player(self, **kwargs) -> bool:
        """Update current player information."""
        try:
            if not self.current_player:
                return False
            
            # Update player object
            for key, value in kwargs.items():
                if hasattr(self.current_player, key):
                    setattr(self.current_player, key, value)
            
            # Update last active
            self.current_player.last_active = datetime.now()
            
            # Save to database
            query = """
                UPDATE players 
                SET name = ?, level = ?, experience = ?, tier = ?, last_active = ?
                WHERE id = ?
            """
            
            success = self.execute_update(query, (
                self.current_player.name,
                self.current_player.level,
                self.current_player.experience,
                self.current_player.tier,
                self.current_player.last_active.isoformat(),
                self.current_player.id
            ))
            
            if success:
                self.log_activity(f"Updated player: {self.current_player.name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update player: {e}")
            return False
    
    def add_experience(self, amount: int) -> Dict[str, Any]:
        """Add experience to current player."""
        try:
            if not self.current_player:
                return {"success": False, "error": "No current player"}
            
            old_level = self.current_player.level
            self.current_player.experience += amount
            
            # Calculate new level (simple progression)
            new_level = max(1, int((self.current_player.experience / 100) ** 0.5))
            levels_gained = new_level - old_level
            
            if new_level != old_level:
                self.current_player.level = new_level
            
            # Save changes
            self.update_player()
            
            result = {
                "success": True,
                "xp_gained": amount,
                "levels_gained": levels_gained,
                "new_level": self.current_player.level,
                "total_xp": self.current_player.experience
            }
            
            if levels_gained > 0:
                self.log_activity(f"Player leveled up! New level: {self.current_player.level}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to add experience: {e}")
            return {"success": False, "error": str(e)}
    
    def get_all_players(self) -> List[Dict[str, Any]]:
        """Get all players."""
        try:
            players_data = self.execute_query("SELECT * FROM players ORDER BY level DESC, experience DESC")
            
            players = []
            for player_data in players_data:
                players.append({
                    "id": player_data["id"],
                    "name": player_data["name"],
                    "level": player_data["level"],
                    "experience": player_data["experience"],
                    "tier": player_data["tier"],
                    "created_at": player_data["created_at"],
                    "last_active": player_data["last_active"],
                    "is_current": bool(player_data["is_current"])
                })
            
            return players
            
        except Exception as e:
            logger.error(f"Failed to get all players: {e}")
            return []
    
    def switch_player(self, player_id: str) -> bool:
        """Switch to a different player."""
        try:
            # Check if player exists
            players = self.execute_query("SELECT * FROM players WHERE id = ?", (player_id,))
            
            if not players:
                return False
            
            # Clear current player flag
            self.execute_update("UPDATE players SET is_current = 0")
            
            # Set new current player
            success = self.execute_update("UPDATE players SET is_current = 1 WHERE id = ?", (player_id,))
            
            if success:
                # Reload current player
                self._load_current_player()
                self.log_activity(f"Switched to player: {self.current_player.name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to switch player: {e}")
            return False
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate player data."""
        required_fields = ["name"]
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate level and experience
        if "level" in data and not isinstance(data["level"], int):
            return False
        
        if "experience" in data and not isinstance(data["experience"], int):
            return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get player statistics."""
        if not self.current_player:
            return {"total_players": 0}
        
        all_players = self.get_all_players()
        
        return {
            "total_players": len(all_players),
            "current_player": {
                "name": self.current_player.name,
                "level": self.current_player.level,
                "experience": self.current_player.experience,
                "tier": self.current_player.tier
            },
            "highest_level": max((p["level"] for p in all_players), default=0),
            "total_experience": sum(p["experience"] for p in all_players)
        } 