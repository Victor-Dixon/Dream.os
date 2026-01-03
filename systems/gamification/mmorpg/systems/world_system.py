#!/usr/bin/env python3
"""
World System
============

World management system for the Dreamscape MMORPG.
Handles world state, zones, events, and environmental interactions.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import sqlite3
import random

from ..models.mmorpg_models import (
    Guild, Quest, QuestType, Player, GameState
)

logger = logging.getLogger(__name__)


class WorldSystem:
    """World management system for MMORPG."""
    
    def __init__(self, db_path: str = "dreamos_resume.db"):
        """Initialize the world system."""
        self.db_path = db_path
        self.connection = None
        self.world_state = {}
        self._initialize_database()
        
        logger.info("World System initialized")
    
    def _initialize_database(self):
        """Initialize world database tables."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            
            # Create world tables
            self._create_world_tables()
            
        except Exception as e:
            logger.error(f"Failed to initialize world database: {e}")
            raise
    
    def _create_world_tables(self):
        """Create world-related database tables."""
        cursor = self.connection.cursor()
        
        # World zones table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS world_zones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                zone_type TEXT NOT NULL,
                difficulty_level INTEGER DEFAULT 1,
                required_level INTEGER DEFAULT 1,
                max_players INTEGER DEFAULT 10,
                current_players INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # World events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS world_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                event_type TEXT NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                zone_id INTEGER,
                max_participants INTEGER DEFAULT 50,
                current_participants INTEGER DEFAULT 0,
                status TEXT DEFAULT 'scheduled',
                rewards TEXT,  -- JSON string
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (zone_id) REFERENCES world_zones (id)
            )
        """)
        
        # Guild territories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_territories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                zone_id INTEGER,
                territory_name TEXT NOT NULL,
                control_level INTEGER DEFAULT 1,
                resources TEXT,  -- JSON string
                defenses TEXT,  -- JSON string
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (guild_id) REFERENCES guilds (id),
                FOREIGN KEY (zone_id) REFERENCES world_zones (id)
            )
        """)
        
        # World resources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS world_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zone_id INTEGER,
                resource_type TEXT NOT NULL,
                resource_name TEXT NOT NULL,
                quantity INTEGER DEFAULT 100,
                respawn_time INTEGER DEFAULT 3600,  -- seconds
                last_respawn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'available',
                FOREIGN KEY (zone_id) REFERENCES world_zones (id)
            )
        """)
        
        self.connection.commit()
        logger.info("World database tables created/verified")
    
    def create_zone(self, name: str, description: str, zone_type: str,
                   difficulty_level: int = 1, required_level: int = 1,
                   max_players: int = 10) -> str:
        """Create a new world zone."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO world_zones (name, description, zone_type, difficulty_level,
                                       required_level, max_players)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, zone_type, difficulty_level, required_level, max_players))
            
            zone_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Created world zone: {name}")
            return zone_id
            
        except Exception as e:
            logger.error(f"Failed to create zone: {e}")
            raise
    
    def get_zones(self, zone_type: str = None, status: str = "active") -> List[Dict[str, Any]]:
        """Get world zones with optional filtering."""
        try:
            cursor = self.connection.cursor()
            
            query = "SELECT * FROM world_zones WHERE status = ?"
            params = [status]
            
            if zone_type:
                query += " AND zone_type = ?"
                params.append(zone_type)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            zones = []
            for row in rows:
                zones.append({
                    "id": str(row['id']),
                    "name": row['name'],
                    "description": row['description'],
                    "zone_type": row['zone_type'],
                    "difficulty_level": row['difficulty_level'],
                    "required_level": row['required_level'],
                    "max_players": row['max_players'],
                    "current_players": row['current_players'],
                    "status": row['status'],
                    "created_at": row['created_at']
                })
            
            return zones
            
        except Exception as e:
            logger.error(f"Failed to get zones: {e}")
            return []
    
    def create_world_event(self, name: str, description: str, event_type: str,
                          start_time: datetime, end_time: datetime,
                          zone_id: str = None, max_participants: int = 50,
                          rewards: Dict[str, Any] = None) -> str:
        """Create a new world event."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO world_events (name, description, event_type, start_time, end_time,
                                        zone_id, max_participants, rewards)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, description, event_type, start_time.isoformat(),
                end_time.isoformat(), zone_id, max_participants,
                json.dumps(rewards or {})
            ))
            
            event_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Created world event: {name}")
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to create world event: {e}")
            raise
    
    def get_active_events(self) -> List[Dict[str, Any]]:
        """Get currently active world events."""
        try:
            cursor = self.connection.cursor()
            
            now = datetime.now().isoformat()
            cursor.execute("""
                SELECT * FROM world_events 
                WHERE status = 'active' 
                AND start_time <= ? 
                AND end_time >= ?
            """, (now, now))
            
            rows = cursor.fetchall()
            events = []
            
            for row in rows:
                events.append({
                    "id": str(row['id']),
                    "name": row['name'],
                    "description": row['description'],
                    "event_type": row['event_type'],
                    "start_time": row['start_time'],
                    "end_time": row['end_time'],
                    "zone_id": str(row['zone_id']) if row['zone_id'] else None,
                    "max_participants": row['max_participants'],
                    "current_participants": row['current_participants'],
                    "rewards": json.loads(row['rewards']) if row['rewards'] else {}
                })
            
            return events
            
        except Exception as e:
            logger.error(f"Failed to get active events: {e}")
            return []
    
    def join_event(self, event_id: str, player_id: str) -> bool:
        """Join a world event."""
        try:
            cursor = self.connection.cursor()
            
            # Check if event is full
            cursor.execute("""
                SELECT current_participants, max_participants FROM world_events 
                WHERE id = ? AND status = 'active'
            """, (event_id,))
            
            row = cursor.fetchone()
            if not row:
                return False
            
            if row['current_participants'] >= row['max_participants']:
                logger.warning(f"Event {event_id} is full")
                return False
            
            # Increment participant count
            cursor.execute("""
                UPDATE world_events 
                SET current_participants = current_participants + 1 
                WHERE id = ?
            """, (event_id,))
            
            self.connection.commit()
            logger.info(f"Player {player_id} joined event {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to join event: {e}")
            return False
    
    def create_guild_territory(self, guild_id: str, zone_id: str, territory_name: str,
                              control_level: int = 1) -> str:
        """Create a guild territory in a zone."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO guild_territories (guild_id, zone_id, territory_name, control_level,
                                             resources, defenses)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                guild_id, zone_id, territory_name, control_level,
                json.dumps({"gold": 1000, "materials": 500}),
                json.dumps({"walls": 1, "towers": 0})
            ))
            
            territory_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Created guild territory: {territory_name}")
            return territory_id
            
        except Exception as e:
            logger.error(f"Failed to create guild territory: {e}")
            raise
    
    def get_guild_territories(self, guild_id: str = None) -> List[Dict[str, Any]]:
        """Get guild territories."""
        try:
            cursor = self.connection.cursor()
            
            query = "SELECT * FROM guild_territories"
            params = []
            
            if guild_id:
                query += " WHERE guild_id = ?"
                params.append(guild_id)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            territories = []
            for row in rows:
                territories.append({
                    "id": str(row['id']),
                    "guild_id": str(row['guild_id']),
                    "zone_id": str(row['zone_id']),
                    "territory_name": row['territory_name'],
                    "control_level": row['control_level'],
                    "resources": json.loads(row['resources']),
                    "defenses": json.loads(row['defenses']),
                    "last_updated": row['last_updated']
                })
            
            return territories
            
        except Exception as e:
            logger.error(f"Failed to get guild territories: {e}")
            return []
    
    def add_world_resource(self, zone_id: str, resource_type: str, resource_name: str,
                          quantity: int = 100, respawn_time: int = 3600) -> str:
        """Add a resource to a world zone."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO world_resources (zone_id, resource_type, resource_name,
                                           quantity, respawn_time)
                VALUES (?, ?, ?, ?, ?)
            """, (zone_id, resource_type, resource_name, quantity, respawn_time))
            
            resource_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Added world resource: {resource_name}")
            return resource_id
            
        except Exception as e:
            logger.error(f"Failed to add world resource: {e}")
            raise
    
    def harvest_resource(self, resource_id: str, player_id: str, amount: int = 1) -> Dict[str, Any]:
        """Harvest a world resource."""
        try:
            cursor = self.connection.cursor()
            
            # Get resource info
            cursor.execute("""
                SELECT * FROM world_resources WHERE id = ? AND status = 'available'
            """, (resource_id,))
            
            row = cursor.fetchone()
            if not row:
                return {"success": False, "message": "Resource not available"}
            
            if row['quantity'] < amount:
                return {"success": False, "message": "Insufficient resource quantity"}
            
            # Update resource quantity
            new_quantity = row['quantity'] - amount
            cursor.execute("""
                UPDATE world_resources 
                SET quantity = ?, last_respawn = ? 
                WHERE id = ?
            """, (new_quantity, datetime.now().isoformat(), resource_id))
            
            # If resource is depleted, set status to respawning
            if new_quantity <= 0:
                cursor.execute("""
                    UPDATE world_resources SET status = 'respawning' WHERE id = ?
                """, (resource_id,))
            
            self.connection.commit()
            
            result = {
                "success": True,
                "resource_name": row['resource_name'],
                "resource_type": row['resource_type'],
                "amount": amount,
                "remaining": new_quantity
            }
            
            logger.info(f"Player {player_id} harvested {amount} {row['resource_name']}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to harvest resource: {e}")
            return {"success": False, "message": "Harvest failed"}
    
    def respawn_resources(self):
        """Respawn depleted resources based on their respawn timers."""
        try:
            cursor = self.connection.cursor()
            
            now = datetime.now()
            
            # Get resources that need respawning
            cursor.execute("""
                SELECT * FROM world_resources 
                WHERE status = 'respawning' 
                AND datetime(last_respawn, '+' || respawn_time || ' seconds') <= ?
            """, (now.isoformat(),))
            
            rows = cursor.fetchall()
            
            for row in rows:
                # Respawn the resource
                cursor.execute("""
                    UPDATE world_resources 
                    SET quantity = 100, status = 'available', last_respawn = ?
                    WHERE id = ?
                """, (now.isoformat(), row['id']))
                
                logger.info(f"Respawned resource: {row['resource_name']}")
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Failed to respawn resources: {e}")
    
    def generate_random_quest(self, zone_id: str, player_level: int) -> Dict[str, Any]:
        """Generate a random quest for a zone."""
        try:
            quest_templates = {
                "bug_hunt": {
                    "title": "Bug Hunt in {zone_name}",
                    "description": "Find and fix bugs in the {zone_name} area",
                    "difficulty": lambda level: max(1, min(10, level // 2)),
                    "xp_reward": lambda level: level * 50,
                    "skill_rewards": {"debugging": lambda level: level * 5}
                },
                "feature_raid": {
                    "title": "Feature Raid: {zone_name}",
                    "description": "Implement new features in the {zone_name} zone",
                    "difficulty": lambda level: max(1, min(10, level // 2 + 1)),
                    "xp_reward": lambda level: level * 75,
                    "skill_rewards": {"coding": lambda level: level * 8}
                },
                "system_convergence": {
                    "title": "System Convergence in {zone_name}",
                    "description": "Optimize system integration in {zone_name}",
                    "difficulty": lambda level: max(1, min(10, level // 2 + 2)),
                    "xp_reward": lambda level: level * 100,
                    "skill_rewards": {"architecture": lambda level: level * 10}
                }
            }
            
            # Get zone name
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM world_zones WHERE id = ?", (zone_id,))
            zone_row = cursor.fetchone()
            zone_name = zone_row['name'] if zone_row else "Unknown Zone"
            
            # Select random quest type
            quest_type = random.choice(list(quest_templates.keys()))
            template = quest_templates[quest_type]
            
            # Generate quest data
            quest_data = {
                "title": template["title"].format(zone_name=zone_name),
                "description": template["description"].format(zone_name=zone_name),
                "quest_type": quest_type,
                "difficulty": template["difficulty"](player_level),
                "xp_reward": template["xp_reward"](player_level),
                "skill_rewards": {
                    skill: reward_func(player_level)
                    for skill, reward_func in template["skill_rewards"].items()
                }
            }
            
            return quest_data
            
        except Exception as e:
            logger.error(f"Failed to generate random quest: {e}")
            return {}
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get the current world state."""
        try:
            cursor = self.connection.cursor()
            
            # Get zone statistics
            cursor.execute("""
                SELECT COUNT(*) as total_zones,
                       SUM(current_players) as total_players,
                       COUNT(CASE WHEN status = 'active' THEN 1 END) as active_zones
                FROM world_zones
            """)
            zone_stats = cursor.fetchone()
            
            # Get event statistics
            cursor.execute("""
                SELECT COUNT(*) as total_events,
                       COUNT(CASE WHEN status = 'active' THEN 1 END) as active_events,
                       SUM(current_participants) as total_participants
                FROM world_events
            """)
            event_stats = cursor.fetchone()
            
            # Get resource statistics
            cursor.execute("""
                SELECT COUNT(*) as total_resources,
                       COUNT(CASE WHEN status = 'available' THEN 1 END) as available_resources,
                       SUM(quantity) as total_quantity
                FROM world_resources
            """)
            resource_stats = cursor.fetchone()
            
            world_state = {
                "zones": {
                    "total": zone_stats['total_zones'],
                    "active": zone_stats['active_zones'],
                    "total_players": zone_stats['total_players'] or 0
                },
                "events": {
                    "total": event_stats['total_events'],
                    "active": event_stats['active_events'],
                    "total_participants": event_stats['total_participants'] or 0
                },
                "resources": {
                    "total": resource_stats['total_resources'],
                    "available": resource_stats['available_resources'],
                    "total_quantity": resource_stats['total_quantity'] or 0
                },
                "last_updated": datetime.now().isoformat()
            }
            
            return world_state
            
        except Exception as e:
            logger.error(f"Failed to get world state: {e}")
            return {}
    
    def close(self):
        """Close the world system database connection."""
        if self.connection:
            self.connection.close()
            logger.info("World System closed") 