#!/usr/bin/env python3
"""
MMORPG System - Refactored
==========================

Main orchestrator for the modular MMORPG system.
Integrates core engine, character system, and world system.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .core.mmorpg_engine import MMORPGEngine
from .systems.character_system import CharacterSystem
from .systems.world_system import WorldSystem
from .models.mmorpg_models import (
    Player, GameState, Quest, Skill, ArchitectTier, Guild,
    QuestType, SkillType, MMORPGConfig
)

logger = logging.getLogger(__name__)


class MMORPGSystem:
    """Main MMORPG system orchestrator."""
    
    def __init__(self, db_path: str = "dreamos_resume.db", config: MMORPGConfig = None):
        """Initialize the MMORPG system with all components."""
        self.db_path = db_path
        self.config = config or MMORPGConfig()
        
        # Initialize all system components
        self.engine = MMORPGEngine(db_path, self.config)
        self.character_system = CharacterSystem(db_path)
        self.world_system = WorldSystem(db_path)
        
        logger.info("MMORPG System initialized with all components")
    
    # Core Engine Methods (delegated)
    def get_player_info(self) -> Dict[str, Any]:
        """Get current player information."""
        return self.engine.get_player_info()
    
    def get_player(self) -> Player:
        """Get the current player object."""
        return self.engine.get_player()
    
    def get_active_quests(self) -> List[Quest]:
        """Get all active quests."""
        return self.engine.get_active_quests()
    
    def get_available_quests(self) -> List[Quest]:
        """Get all available quests."""
        return self.engine.get_available_quests()
    
    def get_skills(self) -> Dict[str, Skill]:
        """Get all player skills."""
        return self.engine.get_skills()
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a specific skill by name."""
        return self.engine.get_skill(skill_name)
    
    def award_xp(self, amount: int, skill_rewards: Dict[str, int] = None):
        """Award XP to the player."""
        self.engine.award_xp(amount, skill_rewards)
    
    def create_quest(self, title: str, description: str, quest_type: QuestType,
                    difficulty: int, xp_reward: int, skill_rewards: Dict[str, int] = None) -> str:
        """Create a new quest."""
        return self.engine.create_quest(title, description, quest_type, difficulty, xp_reward, skill_rewards)
    
    def start_quest(self, quest_id: str) -> bool:
        """Start a quest."""
        return self.engine.start_quest(quest_id)
    
    def complete_quest(self, quest_id: str) -> bool:
        """Complete a quest and award rewards."""
        return self.engine.complete_quest(quest_id)
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.engine.get_game_state()
    
    # Character System Methods (delegated)
    def create_character(self, player_id: int, name: str) -> str:
        """Create a new character for a player."""
        return self.character_system.create_character(player_id, name)
    
    def get_character(self, character_id: str) -> Optional[Any]:
        """Get a character by ID."""
        return self.character_system.get_character(character_id)
    
    def add_equipment(self, character_id: str, equipment_data: Dict[str, Any]) -> str:
        """Add equipment to a character."""
        return self.character_system.add_equipment(character_id, equipment_data)
    
    def equip_item(self, character_id: str, equipment_id: str) -> bool:
        """Equip an item on a character."""
        return self.character_system.equip_item(character_id, equipment_id)
    
    def add_title(self, character_id: str, title_data: Dict[str, Any]) -> str:
        """Add a title to a character."""
        return self.character_system.add_title(character_id, title_data)
    
    def set_active_title(self, character_id: str, title_id: str) -> bool:
        """Set the active title for a character."""
        return self.character_system.set_active_title(character_id, title_id)
    
    def add_ability(self, character_id: str, ability_data: Dict[str, Any]) -> str:
        """Add an ability to a character."""
        return self.character_system.add_ability(character_id, ability_data)
    
    def activate_ability(self, character_id: str, ability_id: str) -> bool:
        """Activate an ability for a character."""
        return self.character_system.activate_ability(character_id, ability_id)
    
    def update_character_stats(self, character_id: str, stats: Dict[str, Any]) -> bool:
        """Update character statistics."""
        return self.character_system.update_character_stats(character_id, stats)
    
    def add_achievement(self, character_id: str, achievement_id: str) -> bool:
        """Add an achievement to a character."""
        return self.character_system.add_achievement(character_id, achievement_id)
    
    def get_character_summary(self, character_id: str) -> Dict[str, Any]:
        """Get a summary of character information."""
        return self.character_system.get_character_summary(character_id)
    
    # World System Methods (delegated)
    def create_zone(self, name: str, description: str, zone_type: str,
                   difficulty_level: int = 1, required_level: int = 1,
                   max_players: int = 10) -> str:
        """Create a new world zone."""
        return self.world_system.create_zone(name, description, zone_type, difficulty_level, required_level, max_players)
    
    def get_zones(self, zone_type: str = None, status: str = "active") -> List[Dict[str, Any]]:
        """Get world zones with optional filtering."""
        return self.world_system.get_zones(zone_type, status)
    
    def create_world_event(self, name: str, description: str, event_type: str,
                          start_time: datetime, end_time: datetime,
                          zone_id: str = None, max_participants: int = 50,
                          rewards: Dict[str, Any] = None) -> str:
        """Create a new world event."""
        return self.world_system.create_world_event(name, description, event_type, start_time, end_time, zone_id, max_participants, rewards)
    
    def get_active_events(self) -> List[Dict[str, Any]]:
        """Get currently active world events."""
        return self.world_system.get_active_events()
    
    def join_event(self, event_id: str, player_id: str) -> bool:
        """Join a world event."""
        return self.world_system.join_event(event_id, player_id)
    
    def create_guild_territory(self, guild_id: str, zone_id: str, territory_name: str,
                              control_level: int = 1) -> str:
        """Create a guild territory in a zone."""
        return self.world_system.create_guild_territory(guild_id, zone_id, territory_name, control_level)
    
    def get_guild_territories(self, guild_id: str = None) -> List[Dict[str, Any]]:
        """Get guild territories."""
        return self.world_system.get_guild_territories(guild_id)
    
    def add_world_resource(self, zone_id: str, resource_type: str, resource_name: str,
                          quantity: int = 100, respawn_time: int = 3600) -> str:
        """Add a resource to a world zone."""
        return self.world_system.add_world_resource(zone_id, resource_type, resource_name, quantity, respawn_time)
    
    def harvest_resource(self, resource_id: str, player_id: str, amount: int = 1) -> Dict[str, Any]:
        """Harvest a world resource."""
        return self.world_system.harvest_resource(resource_id, player_id, amount)
    
    def respawn_resources(self):
        """Respawn depleted resources based on their respawn timers."""
        self.world_system.respawn_resources()
    
    def generate_random_quest(self, zone_id: str, player_level: int) -> Dict[str, Any]:
        """Generate a random quest for a zone."""
        return self.world_system.generate_random_quest(zone_id, player_level)
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get the current world state."""
        return self.world_system.get_world_state()
    
    # Integrated Methods
    def process_conversation_progress(self, conversation_id: str, message_count: int,
                                    word_count: int, skill_insights: Dict[str, int] = None):
        """Process conversation progress and award XP/skills."""
        try:
            # Award XP for conversation participation
            base_xp = message_count * 5 + word_count // 10
            self.award_xp(base_xp)
            
            # Award skill XP if insights provided
            if skill_insights:
                for skill_name, xp_amount in skill_insights.items():
                    skill_rewards = {skill_name: xp_amount}
                    self.award_xp(0, skill_rewards)
            
            # Update player conversation stats
            player = self.get_player()
            player.total_conversations += 1
            player.total_messages += message_count
            player.total_words += word_count
            player.last_active = datetime.now()
            
            # Save updated player state
            self.engine._save_player_state()
            
            logger.info(f"Processed conversation progress: {conversation_id}")
            
        except Exception as e:
            logger.error(f"Failed to process conversation progress: {e}")
    
    def create_quest_from_conversation(self, conversation_id: str, conversation_summary: str,
                                     skill_insights: Dict[str, int]) -> str:
        """Create a quest based on conversation analysis."""
        try:
            # Determine quest type based on conversation content
            quest_type = self._determine_quest_type(conversation_summary)
            
            # Generate quest details
            title = f"Conversation Quest: {conversation_summary[:50]}..."
            description = f"Complete objectives based on conversation: {conversation_summary}"
            
            # Calculate difficulty and rewards based on skill insights
            total_skill_xp = sum(skill_insights.values())
            difficulty = min(10, max(1, total_skill_xp // 50))
            xp_reward = total_skill_xp * 2
            
            # Create the quest
            quest_id = self.create_quest(
                title=title,
                description=description,
                quest_type=quest_type,
                difficulty=difficulty,
                xp_reward=xp_reward,
                skill_rewards=skill_insights
            )
            
            # Link quest to conversation
            self._link_quest_to_conversation(quest_id, conversation_id)
            
            logger.info(f"Created quest from conversation: {quest_id}")
            return quest_id
            
        except Exception as e:
            logger.error(f"Failed to create quest from conversation: {e}")
            return ""
    
    def _determine_quest_type(self, conversation_summary: str) -> QuestType:
        """Determine quest type based on conversation content."""
        summary_lower = conversation_summary.lower()
        
        if any(word in summary_lower for word in ["bug", "error", "fix", "debug"]):
            return QuestType.BUG_HUNT
        elif any(word in summary_lower for word in ["feature", "implement", "add", "create"]):
            return QuestType.FEATURE_RAID
        elif any(word in summary_lower for word in ["system", "architecture", "design"]):
            return QuestType.SYSTEM_CONVERGENCE
        elif any(word in summary_lower for word in ["learn", "research", "study", "knowledge"]):
            return QuestType.KNOWLEDGE_EXPEDITION
        elif any(word in summary_lower for word in ["legacy", "old", "migrate", "update"]):
            return QuestType.LEGACY_MISSION
        elif any(word in summary_lower for word in ["workflow", "process", "automate"]):
            return QuestType.WORKFLOW_AUDIT
        elif any(word in summary_lower for word in ["market", "business", "strategy"]):
            return QuestType.MARKET_ANALYSIS
        else:
            return QuestType.PERSONAL_STRATEGY
    
    def _link_quest_to_conversation(self, quest_id: str, conversation_id: str):
        """Link a quest to a conversation in the database."""
        try:
            cursor = self.engine.connection.cursor()
            cursor.execute("""
                UPDATE quests SET conversation_id = ? WHERE id = ?
            """, (conversation_id, quest_id))
            self.engine.connection.commit()
            
        except Exception as e:
            logger.error(f"Failed to link quest to conversation: {e}")
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the MMORPG system."""
        try:
            player_info = self.get_player_info()
            game_state = self.get_game_state()
            world_state = self.get_world_state()
            
            summary = {
                "player": player_info,
                "game_state": {
                    "current_tier": game_state.current_tier,
                    "total_xp": game_state.total_xp,
                    "skill_count": len(game_state.skills),
                    "quest_count": len(game_state.quests),
                    "active_quests": len([q for q in game_state.quests.values() if q.status == "active"]),
                    "architect_tiers": len(game_state.architect_tiers),
                    "guild_count": len(game_state.guilds)
                },
                "world": world_state,
                "system_status": "active",
                "last_updated": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get system summary: {e}")
            return {}
    
    def close(self):
        """Close all MMORPG system components."""
        try:
            self.engine.close()
            self.character_system.close()
            self.world_system.close()
            logger.info("MMORPG System closed")
        except Exception as e:
            logger.error(f"Error closing MMORPG System: {e}")


# Convenience functions for backward compatibility
def get_mmorpg_system(db_path: str = "dreamos_resume.db") -> MMORPGSystem:
    """Get the MMORPG system instance."""
    return MMORPGSystem(db_path)

def get_player_info() -> Dict[str, Any]:
    """Get current player information."""
    system = MMORPGSystem()
    try:
        return system.get_player_info()
    finally:
        system.close()

def get_active_quests() -> List[Quest]:
    """Get all active quests."""
    system = MMORPGSystem()
    try:
        return system.get_active_quests()
    finally:
        system.close()

def award_xp(amount: int, skill_rewards: Dict[str, int] = None):
    """Award XP to the player."""
    system = MMORPGSystem()
    try:
        system.award_xp(amount, skill_rewards)
    finally:
        system.close() 