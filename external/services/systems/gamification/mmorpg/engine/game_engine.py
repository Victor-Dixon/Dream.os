"""
MMORPG Game Engine
Contains the main game engine for the Dreamscape MMORPG system.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os

from ..models import (
    Player, Quest, Skill, ArchitectTier, Guild, 
    GameState, MMORPGConfig
)


class MMORPGEngine:
    """Main engine for the Dreamscape MMORPG system."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the MMORPG engine."""
        self.config = MMORPGConfig()
        self.game_state = None
        self.players = {}
        self.quests = {}
        self.skills = {}
        
    def get_active_quests(self):
        """Get all active quests."""
        return [quest for quest in self.quests.values() if quest.is_active()]
        
    def get_player_info(self):
        """Get current player information."""
        if not self.players:
            return None
        # Return the first player (assuming single player for now)
        player_name = list(self.players.keys())[0]
        return self.players[player_name]
        
    def get_player(self):
        """Get the current player."""
        if not self.players:
            return None
        # Return the first player (assuming single player for now)
        player_name = list(self.players.keys())[0]
        return self.players[player_name]
        
    def add_player(self, player: Player) -> bool:
        """Add a player to the game."""
        if player.name not in self.players:
            self.players[player.name] = player
            return True
        return False
        
    def remove_player(self, player_name: str) -> bool:
        """Remove a player from the game."""
        if player_name in self.players:
            del self.players[player_name]
            return True
        return False
        
    def get_player_by_name(self, player_name: str) -> Optional[Player]:
        """Get a player by name."""
        return self.players.get(player_name)
        
    def add_quest(self, quest: Quest) -> bool:
        """Add a quest to the game."""
        if quest.id not in self.quests:
            self.quests[quest.id] = quest
            return True
        return False
        
    def remove_quest(self, quest_id: str) -> bool:
        """Remove a quest from the game."""
        if quest_id in self.quests:
            del self.quests[quest_id]
            return True
        return False
        
    def get_quest_by_id(self, quest_id: str) -> Optional[Quest]:
        """Get a quest by ID."""
        return self.quests.get(quest_id)
        
    def get_available_quests(self) -> List[Quest]:
        """Get all available quests."""
        return [quest for quest in self.quests.values() if quest.is_available()]
        
    def get_completed_quests(self) -> List[Quest]:
        """Get all completed quests."""
        return [quest for quest in self.quests.values() if quest.is_completed()]
        
    def get_failed_quests(self) -> List[Quest]:
        """Get all failed quests."""
        return [quest for quest in self.quests.values() if quest.is_failed()]
        
    def add_skill(self, skill: Skill) -> bool:
        """Add a skill to the game."""
        if skill.name not in self.skills:
            self.skills[skill.name] = skill
            return True
        return False
        
    def remove_skill(self, skill_name: str) -> bool:
        """Remove a skill from the game."""
        if skill_name in self.skills:
            del self.skills[skill_name]
            return True
        return False
        
    def get_skill_by_name(self, skill_name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self.skills.get(skill_name)
        
    def get_all_skills(self) -> List[Skill]:
        """Get all skills in the game."""
        return list(self.skills.values())
        
    def update_game_state(self, game_state: GameState) -> bool:
        """Update the game state."""
        self.game_state = game_state
        return True
        
    def get_game_state(self) -> Optional[GameState]:
        """Get the current game state."""
        return self.game_state
        
    def save_game_state(self, file_path: str = "game_state.json") -> bool:
        """Save the game state to a file."""
        try:
            if self.game_state:
                state_data = {
                    'current_tier': self.game_state.current_tier,
                    'total_xp': self.game_state.total_xp,
                    'skills': {name: skill.to_dict() for name, skill in self.game_state.skills.items()},
                    'quests': {quest_id: quest.to_dict() for quest_id, quest in self.game_state.quests.items()},
                    'architect_tiers': {tier: tier_data.to_dict() for tier, tier_data in self.game_state.architect_tiers.items()},
                    'guilds': {guild_id: guild.to_dict() for guild_id, guild in self.game_state.guilds.items()},
                    'last_updated': self.game_state.last_updated.isoformat() if self.game_state.last_updated else None
                }
                
                with open(file_path, 'w') as f:
                    json.dump(state_data, f, indent=2)
                return True
        except Exception as e:
            print(f"Error saving game state: {e}")
            return False
            
    def load_game_state(self, file_path: str = "game_state.json") -> bool:
        """Load the game state from a file."""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    state_data = json.load(f)
                    
                # Reconstruct skills
                skills = {}
                for name, skill_data in state_data.get('skills', {}).items():
                    skills[name] = Skill.from_dict(skill_data)
                    
                # Reconstruct quests
                quests = {}
                for quest_id, quest_data in state_data.get('quests', {}).items():
                    quests[quest_id] = Quest.from_dict(quest_data)
                    
                # Reconstruct architect tiers
                architect_tiers = {}
                for tier, tier_data in state_data.get('architect_tiers', {}).items():
                    architect_tiers[int(tier)] = ArchitectTier.from_dict(tier_data)
                    
                # Reconstruct guilds
                guilds = {}
                for guild_id, guild_data in state_data.get('guilds', {}).items():
                    guilds[guild_id] = Guild.from_dict(guild_data)
                    
                # Create game state
                last_updated = None
                if state_data.get('last_updated'):
                    last_updated = datetime.fromisoformat(state_data['last_updated'])
                    
                self.game_state = GameState(
                    current_tier=state_data.get('current_tier', 1),
                    total_xp=state_data.get('total_xp', 0),
                    skills=skills,
                    quests=quests,
                    architect_tiers=architect_tiers,
                    guilds=guilds,
                    last_updated=last_updated
                )
                return True
        except Exception as e:
            print(f"Error loading game state: {e}")
            return False
            
    def get_game_stats(self) -> Dict[str, Any]:
        """Get comprehensive game statistics."""
        stats = {
            'total_players': len(self.players),
            'total_quests': len(self.quests),
            'active_quests': len(self.get_active_quests()),
            'available_quests': len(self.get_available_quests()),
            'completed_quests': len(self.get_completed_quests()),
            'failed_quests': len(self.get_failed_quests()),
            'total_skills': len(self.skills),
            'game_state_exists': self.game_state is not None
        }
        
        if self.game_state:
            stats.update({
                'current_tier': self.game_state.current_tier,
                'total_xp': self.game_state.total_xp,
                'total_architect_tiers': len(self.game_state.architect_tiers),
                'total_guilds': len(self.game_state.guilds),
                'last_updated': self.game_state.last_updated.isoformat() if self.game_state.last_updated else None
            })
            
        return stats 