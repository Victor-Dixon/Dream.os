#!/usr/bin/env python3
"""
MMORPG Engine
=============

This module contains ONLY the core MMORPG game engine logic.
Following the Single Responsibility Principle - this module only handles game engine operations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import Player, Quest, GameState, QuestType, Achievement

class MMORPGEngine:
    """
    Core MMORPG game engine responsible for:
    - Quest management
    - Player state management
    - Game state coordination
    - Basic game mechanics
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the MMORPG engine."""
        self.game_state = GameState(
            current_tier=1,
            total_xp=0,
            skills={},
            quests={},
            architect_tiers={},
            guilds={},
            achievements=[],
            badges=[],
            last_updated=datetime.now()
        )
        self.player = Player(
            name="Dreamscape Player", 
            architect_tier="Tier 1 - Novice",
            created_at=datetime.now(),
            last_active=datetime.now()
        )
        self.active_quests: Dict[str, Quest] = {}
        self.available_quests: Dict[str, Quest] = {}
        
        # Initialize with some sample achievements
        self._initialize_sample_achievements()
        
    def get_active_quests(self) -> List[Quest]:
        """Get all currently active quests."""
        return list(self.active_quests.values())
        
    def get_available_quests(self) -> List[Quest]:
        """Get all available quests."""
        return list(self.available_quests.values())
        
    def get_player_info(self) -> Dict[str, Any]:
        """Get player information."""
        return {
            'name': self.player.name,
            'tier': self.player.architect_tier,
            'xp': self.player.xp,
            'total_conversations': self.player.total_conversations,
            'total_messages': self.player.total_messages,
            'total_words': self.player.total_words,
            'created_at': self.player.created_at,
            'last_active': self.player.last_active
        }
        
    def get_player(self) -> Player:
        """Get the player object."""
        return self.player
        
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.game_state
        
    def start_quest(self, quest_id: str) -> bool:
        """Start a quest."""
        if quest_id in self.available_quests:
            quest = self.available_quests[quest_id]
            quest.status = "active"
            quest.created_at = datetime.now()
            self.active_quests[quest_id] = quest
            del self.available_quests[quest_id]
            return True
        return False
        
    def complete_quest(self, quest_id: str) -> bool:
        """Complete a quest."""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.status = "completed"
            quest.completed_at = datetime.now()
            
            # Award XP
            self.player.xp += quest.xp_reward
            self.game_state.total_xp += quest.xp_reward
            
            # Update game state
            self.game_state.quests[quest_id] = quest
            del self.active_quests[quest_id]
            
            return True
        return False
        
    def fail_quest(self, quest_id: str, reason: str = "Unknown") -> bool:
        """Fail a quest."""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.status = "failed"
            quest.completed_at = datetime.now()
            
            # Move back to available quests
            self.available_quests[quest_id] = quest
            del self.active_quests[quest_id]
            
            return True
        return False
        
    def add_quest(self, quest: Quest) -> bool:
        """Add a new quest to the available quests."""
        if quest.id not in self.available_quests:
            self.available_quests[quest.id] = quest
            self.game_state.quests[quest.id] = quest
            return True
        return False
        
    def update_player_stats(self, conversations: int = 0, messages: int = 0, words: int = 0) -> None:
        """Update player statistics."""
        self.player.total_conversations += conversations
        self.player.total_messages += messages
        self.player.total_words += words
        self.player.last_active = datetime.now()
        
    def award_xp(self, xp_amount: int) -> None:
        """Award XP to the player."""
        self.player.xp += xp_amount
        self.game_state.total_xp += xp_amount
        
    def get_player_level(self) -> int:
        """Get the player's current level based on XP."""
        # Simple level calculation (can be enhanced)
        return max(1, self.player.xp // 100)
        
    def get_quest_by_id(self, quest_id: str) -> Optional[Quest]:
        """Get a quest by its ID."""
        if quest_id in self.active_quests:
            return self.active_quests[quest_id]
        elif quest_id in self.available_quests:
            return self.available_quests[quest_id]
        elif quest_id in self.game_state.quests:
            return self.game_state.quests[quest_id]
        return None
        
    def get_quests_by_type(self, quest_type: QuestType) -> List[Quest]:
        """Get all quests of a specific type."""
        quests = []
        for quest in self.game_state.quests.values():
            if quest.quest_type == quest_type:
                quests.append(quest)
        return quests
        
    def get_quests_by_status(self, status: str) -> List[Quest]:
        """Get all quests with a specific status."""
        quests = []
        for quest in self.game_state.quests.values():
            if quest.status == status:
                quests.append(quest)
        return quests
        
    def update_game_state(self) -> None:
        """Update the game state timestamp."""
        self.game_state.last_updated = datetime.now()
        
    def reset_engine(self) -> None:
        """Reset the engine to initial state."""
        self.__init__() 

    def get_achievements(self, category: str = None) -> List[Achievement]:
        # EDIT START — Agent 2: Surface all achievements for the player (optionally filtered by category).
        """Return all achievements for the player, optionally filtered by category."""
        achievements = []
        for ach in self.game_state.achievements:
            if category is None or ach.category == category:
                achievements.append(ach)
        return achievements
        # EDIT END

    def get_badges(self) -> List[Achievement]:
        # EDIT START — Agent 2: Return all badge-type achievements (category or tag based).
        """Return all badge achievements for the player."""
        return self.game_state.badges
        # EDIT END

    def get_quest_log(self, status: str = None) -> List[Quest]:
        # EDIT START — Agent 2: Return all quests for the player, optionally filtered by status.
        """Return all quests for the player, optionally filtered by status (active, completed, failed, etc.)."""
        if status:
            return [q for q in self.game_state.quests.values() if getattr(q, 'status', None) == status]
        return list(self.game_state.quests.values())
        # EDIT END

    def _initialize_sample_achievements(self):
        """Initialize the engine with sample achievements for testing."""
        sample_achievements = [
            Achievement(
                id="first_conversation",
                name="First Conversation",
                description="Completed your first conversation analysis",
                category="milestone",
                difficulty=1,
                xp_reward=50,
                completed_at="2024-12-01",
                evidence="First conversation processed",
                tags=["beginner", "milestone"],
                impact_score=3
            ),
            Achievement(
                id="skill_master",
                name="Skill Master",
                description="Reached level 10 in any skill",
                category="skill",
                difficulty=5,
                xp_reward=200,
                completed_at="2024-12-15",
                evidence="Python skill reached level 10",
                tags=["skill", "progression"],
                impact_score=7
            ),
            Achievement(
                id="quest_completer",
                name="Quest Completer",
                description="Completed 5 quests",
                category="quest",
                difficulty=3,
                xp_reward=150,
                completed_at="2024-12-10",
                evidence="5 quests completed",
                tags=["quest", "completion"],
                impact_score=5
            ),
            Achievement(
                id="ai_expert",
                name="AI Expert",
                description="Demonstrated advanced AI knowledge",
                category="badge",
                difficulty=8,
                xp_reward=500,
                completed_at="2024-12-20",
                evidence="Advanced AI conversation analysis",
                tags=["ai", "expertise", "badge"],
                impact_score=9
            ),
            Achievement(
                id="system_architect",
                name="System Architect",
                description="Designed and implemented a complex system",
                category="project",
                difficulty=9,
                xp_reward=750,
                completed_at="2024-12-25",
                evidence="Dreamscape MMORPG Skill Engine",
                tags=["architecture", "project", "badge"],
                impact_score=10
            )
        ]
        
        # Add achievements to game state
        self.game_state.achievements.extend(sample_achievements)
        
        # Add some as badges
        badge_achievements = [ach for ach in sample_achievements if ach.category == "badge"]
        self.game_state.badges.extend(badge_achievements) 