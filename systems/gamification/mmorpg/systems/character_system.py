#!/usr/bin/env python3
"""
Character System
================

Character management system for the Dreamscape MMORPG.
Handles character creation, progression, equipment, abilities, and titles.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import sqlite3

from ..models.mmorpg_models import (
    Character, Equipment, Title, Ability, Player,
    Skill, ArchitectTier, Quest, Achievement
)

logger = logging.getLogger(__name__)


class CharacterSystem:
    """Character management system for MMORPG."""
    
    def __init__(self, db_path: str = "dreamos_resume.db"):
        """Initialize the character system."""
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
        
        logger.info("Character System initialized")
    
    def _initialize_database(self):
        """Initialize character database tables."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            
            # Create character tables
            self._create_character_tables()
            
        except Exception as e:
            logger.error(f"Failed to initialize character database: {e}")
            raise
    
    def _create_character_tables(self):
        """Create character-related database tables."""
        cursor = self.connection.cursor()
        
        # Characters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                name TEXT NOT NULL,
                active_title TEXT,
                active_abilities TEXT,  -- JSON string
                achievements TEXT,  -- JSON string
                stats TEXT,  -- JSON string
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """)
        
        # Equipment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                rarity TEXT NOT NULL,
                level_req INTEGER DEFAULT 1,
                stats TEXT,  -- JSON string
                abilities TEXT,  -- JSON string
                description TEXT,
                flavor_text TEXT,
                obtained_from TEXT,
                equipped BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id) REFERENCES characters (id)
            )
        """)
        
        # Titles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER,
                name TEXT NOT NULL,
                requirement TEXT,
                description TEXT,
                rarity TEXT NOT NULL,
                bonus_effects TEXT,  -- JSON string
                obtained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (character_id) REFERENCES characters (id)
            )
        """)
        
        # Abilities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS abilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                cooldown INTEGER DEFAULT 0,
                effects TEXT,  -- JSON string
                level_req INTEGER DEFAULT 1,
                scaling TEXT,  -- JSON string
                active BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id) REFERENCES characters (id)
            )
        """)
        
        self.connection.commit()
        logger.info("Character database tables created/verified")
    
    def create_character(self, player_id: int, name: str) -> str:
        """Create a new character for a player."""
        try:
            cursor = self.connection.cursor()
            
            # Create character
            cursor.execute("""
                INSERT INTO characters (player_id, name, active_abilities, achievements, stats)
                VALUES (?, ?, ?, ?, ?)
            """, (
                player_id, name, json.dumps([]), json.dumps([]), json.dumps({})
            ))
            
            character_id = str(cursor.lastrowid)
            
            # Initialize default equipment and abilities
            self._initialize_default_equipment(character_id)
            self._initialize_default_abilities(character_id)
            
            self.connection.commit()
            logger.info(f"Created character: {name}")
            return character_id
            
        except Exception as e:
            logger.error(f"Failed to create character: {e}")
            raise
    
    def _initialize_default_equipment(self, character_id: str):
        """Initialize default equipment for a new character."""
        default_equipment = [
            {
                "name": "Novice Staff",
                "type": "weapon",
                "rarity": "common",
                "level_req": 1,
                "stats": {"attack": 5, "magic": 3},
                "abilities": ["Basic Cast"],
                "description": "A simple staff for novice architects",
                "flavor_text": "The first tool of many great architects",
                "obtained_from": "Starting Equipment"
            },
            {
                "name": "Apprentice Robes",
                "type": "armor",
                "rarity": "common",
                "level_req": 1,
                "stats": {"defense": 3, "magic_defense": 5},
                "abilities": ["Magic Protection"],
                "description": "Basic robes for apprentice architects",
                "flavor_text": "Woven with threads of knowledge",
                "obtained_from": "Starting Equipment"
            }
        ]
        
        cursor = self.connection.cursor()
        for equip_data in default_equipment:
            cursor.execute("""
                INSERT INTO equipment (character_id, name, type, rarity, level_req,
                                     stats, abilities, description, flavor_text, obtained_from)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                character_id, equip_data["name"], equip_data["type"],
                equip_data["rarity"], equip_data["level_req"],
                json.dumps(equip_data["stats"]), json.dumps(equip_data["abilities"]),
                equip_data["description"], equip_data["flavor_text"],
                equip_data["obtained_from"]
            ))
    
    def _initialize_default_abilities(self, character_id: str):
        """Initialize default abilities for a new character."""
        default_abilities = [
            {
                "name": "Code Analysis",
                "type": "active",
                "description": "Analyze code for bugs and improvements",
                "cooldown": 30,
                "effects": [{"type": "skill_boost", "target": "debugging", "value": 10}],
                "level_req": 1,
                "scaling": {"skill_level": 0.5}
            },
            {
                "name": "Architect's Insight",
                "type": "passive",
                "description": "Gain bonus XP from system architecture tasks",
                "cooldown": 0,
                "effects": [{"type": "xp_bonus", "target": "architecture", "value": 0.1}],
                "level_req": 1,
                "scaling": {"tier_level": 0.05}
            }
        ]
        
        cursor = self.connection.cursor()
        for ability_data in default_abilities:
            cursor.execute("""
                INSERT INTO abilities (character_id, name, type, description, cooldown,
                                     effects, level_req, scaling)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                character_id, ability_data["name"], ability_data["type"],
                ability_data["description"], ability_data["cooldown"],
                json.dumps(ability_data["effects"]), ability_data["level_req"],
                json.dumps(ability_data["scaling"])
            ))
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """Get a character by ID."""
        try:
            cursor = self.connection.cursor()
            
            # Get character data
            cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
            char_row = cursor.fetchone()
            
            if not char_row:
                return None
            
            # Get equipment
            cursor.execute("SELECT * FROM equipment WHERE character_id = ?", (character_id,))
            equip_rows = cursor.fetchall()
            equipment = {}
            
            for row in equip_rows:
                equip = Equipment(
                    id=str(row['id']),
                    name=row['name'],
                    type=row['type'],
                    rarity=row['rarity'],
                    level_req=row['level_req'],
                    stats=json.loads(row['stats']),
                    abilities=json.loads(row['abilities']),
                    description=row['description'],
                    flavor_text=row['flavor_text'],
                    obtained_from=row['obtained_from']
                )
                equipment[equip.id] = equip
            
            # Get titles
            cursor.execute("SELECT * FROM titles WHERE character_id = ?", (character_id,))
            title_rows = cursor.fetchall()
            titles = []
            
            for row in title_rows:
                title = Title(
                    id=str(row['id']),
                    name=row['name'],
                    requirement=row['requirement'],
                    description=row['description'],
                    rarity=row['rarity'],
                    bonus_effects=json.loads(row['bonus_effects']),
                    obtained_at=datetime.fromisoformat(row['obtained_at'])
                )
                titles.append(title)
            
            # Get abilities
            cursor.execute("SELECT * FROM abilities WHERE character_id = ?", (character_id,))
            ability_rows = cursor.fetchall()
            abilities = []
            
            for row in ability_rows:
                ability = Ability(
                    id=str(row['id']),
                    name=row['name'],
                    type=row['type'],
                    description=row['description'],
                    cooldown=row['cooldown'],
                    effects=json.loads(row['effects']),
                    level_req=row['level_req'],
                    scaling=json.loads(row['scaling'])
                )
                abilities.append(ability)
            
            # Create character object
            character = Character(
                id=str(char_row['id']),
                name=char_row['name'],
                titles=titles,
                equipment=equipment,
                abilities=abilities,
                active_title=char_row['active_title'],
                active_abilities=json.loads(char_row['active_abilities']),
                achievements=json.loads(char_row['achievements']),
                stats=json.loads(char_row['stats'])
            )
            
            return character
            
        except Exception as e:
            logger.error(f"Failed to get character: {e}")
            return None
    
    def add_equipment(self, character_id: str, equipment_data: Dict[str, Any]) -> str:
        """Add equipment to a character."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO equipment (character_id, name, type, rarity, level_req,
                                     stats, abilities, description, flavor_text, obtained_from)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                character_id, equipment_data["name"], equipment_data["type"],
                equipment_data["rarity"], equipment_data.get("level_req", 1),
                json.dumps(equipment_data.get("stats", {})),
                json.dumps(equipment_data.get("abilities", [])),
                equipment_data.get("description", ""),
                equipment_data.get("flavor_text", ""),
                equipment_data.get("obtained_from", "Unknown")
            ))
            
            equipment_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Added equipment: {equipment_data['name']}")
            return equipment_id
            
        except Exception as e:
            logger.error(f"Failed to add equipment: {e}")
            raise
    
    def equip_item(self, character_id: str, equipment_id: str) -> bool:
        """Equip an item on a character."""
        try:
            cursor = self.connection.cursor()
            
            # Unequip any items of the same type
            cursor.execute("""
                SELECT type FROM equipment WHERE id = ?
            """, (equipment_id,))
            equip_type = cursor.fetchone()['type']
            
            cursor.execute("""
                UPDATE equipment SET equipped = FALSE 
                WHERE character_id = ? AND type = ?
            """, (character_id, equip_type))
            
            # Equip the new item
            cursor.execute("""
                UPDATE equipment SET equipped = TRUE 
                WHERE id = ? AND character_id = ?
            """, (equipment_id, character_id))
            
            self.connection.commit()
            logger.info(f"Equipped item: {equipment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to equip item: {e}")
            return False
    
    def add_title(self, character_id: str, title_data: Dict[str, Any]) -> str:
        """Add a title to a character."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO titles (character_id, name, requirement, description,
                                  rarity, bonus_effects)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                character_id, title_data["name"], title_data.get("requirement", ""),
                title_data.get("description", ""), title_data["rarity"],
                json.dumps(title_data.get("bonus_effects", []))
            ))
            
            title_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Added title: {title_data['name']}")
            return title_id
            
        except Exception as e:
            logger.error(f"Failed to add title: {e}")
            raise
    
    def set_active_title(self, character_id: str, title_id: str) -> bool:
        """Set the active title for a character."""
        try:
            cursor = self.connection.cursor()
            
            # Deactivate all titles
            cursor.execute("""
                UPDATE titles SET active = FALSE WHERE character_id = ?
            """, (character_id,))
            
            # Activate the selected title
            cursor.execute("""
                UPDATE titles SET active = TRUE WHERE id = ? AND character_id = ?
            """, (title_id, character_id))
            
            # Update character's active title
            cursor.execute("""
                SELECT name FROM titles WHERE id = ?
            """, (title_id,))
            title_name = cursor.fetchone()['name']
            
            cursor.execute("""
                UPDATE characters SET active_title = ? WHERE id = ?
            """, (title_name, character_id))
            
            self.connection.commit()
            logger.info(f"Set active title: {title_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set active title: {e}")
            return False
    
    def add_ability(self, character_id: str, ability_data: Dict[str, Any]) -> str:
        """Add an ability to a character."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO abilities (character_id, name, type, description, cooldown,
                                     effects, level_req, scaling)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                character_id, ability_data["name"], ability_data["type"],
                ability_data.get("description", ""), ability_data.get("cooldown", 0),
                json.dumps(ability_data.get("effects", [])),
                ability_data.get("level_req", 1),
                json.dumps(ability_data.get("scaling", {}))
            ))
            
            ability_id = str(cursor.lastrowid)
            self.connection.commit()
            
            logger.info(f"Added ability: {ability_data['name']}")
            return ability_id
            
        except Exception as e:
            logger.error(f"Failed to add ability: {e}")
            raise
    
    def activate_ability(self, character_id: str, ability_id: str) -> bool:
        """Activate an ability for a character."""
        try:
            cursor = self.connection.cursor()
            
            # Deactivate all abilities
            cursor.execute("""
                UPDATE abilities SET active = FALSE WHERE character_id = ?
            """, (character_id,))
            
            # Activate the selected ability
            cursor.execute("""
                UPDATE abilities SET active = TRUE WHERE id = ? AND character_id = ?
            """, (ability_id, character_id))
            
            # Update character's active abilities
            cursor.execute("""
                SELECT name FROM abilities WHERE id = ?
            """, (ability_id,))
            ability_name = cursor.fetchone()['name']
            
            cursor.execute("""
                SELECT active_abilities FROM characters WHERE id = ?
            """, (character_id,))
            current_abilities = json.loads(cursor.fetchone()['active_abilities'])
            current_abilities.append(ability_name)
            
            cursor.execute("""
                UPDATE characters SET active_abilities = ? WHERE id = ?
            """, (json.dumps(current_abilities), character_id))
            
            self.connection.commit()
            logger.info(f"Activated ability: {ability_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to activate ability: {e}")
            return False
    
    def update_character_stats(self, character_id: str, stats: Dict[str, Any]) -> bool:
        """Update character statistics."""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                UPDATE characters SET stats = ?, last_updated = ? WHERE id = ?
            """, (json.dumps(stats), datetime.now().isoformat(), character_id))
            
            self.connection.commit()
            logger.info(f"Updated character stats: {character_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update character stats: {e}")
            return False
    
    def add_achievement(self, character_id: str, achievement_id: str) -> bool:
        """Add an achievement to a character."""
        try:
            cursor = self.connection.cursor()
            
            # Get current achievements
            cursor.execute("""
                SELECT achievements FROM characters WHERE id = ?
            """, (character_id,))
            current_achievements = json.loads(cursor.fetchone()['achievements'])
            
            if achievement_id not in current_achievements:
                current_achievements.append(achievement_id)
                
                cursor.execute("""
                    UPDATE characters SET achievements = ? WHERE id = ?
                """, (json.dumps(current_achievements), character_id))
                
                self.connection.commit()
                logger.info(f"Added achievement: {achievement_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to add achievement: {e}")
            return False
    
    def get_character_summary(self, character_id: str) -> Dict[str, Any]:
        """Get a summary of character information."""
        character = self.get_character(character_id)
        if not character:
            return {}
        
        return {
            "id": character.id,
            "name": character.name,
            "active_title": character.active_title,
            "active_abilities": character.active_abilities,
            "equipment_count": len(character.equipment),
            "title_count": len(character.titles),
            "ability_count": len(character.abilities),
            "achievement_count": len(character.achievements),
            "stats": character.stats
        }
    
    def close(self):
        """Close the character system database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Character System closed") 