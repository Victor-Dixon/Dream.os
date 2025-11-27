#!/usr/bin/env python3
"""
Quest Models
===========

Data models for quest-related intelligence features.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class QuestContext:
    """Context information for quest generation."""
    conversation_id: str
    conversation_content: str
    conversation_title: str
    user_level: int = 1
    current_skills: List[str] = field(default_factory=list)
    completed_quests: List[str] = field(default_factory=list)
    active_quests: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            'conversation_id': self.conversation_id,
            'conversation_content': self.conversation_content,
            'conversation_title': self.conversation_title,
            'user_level': self.user_level,
            'current_skills': self.current_skills,
            'completed_quests': self.completed_quests,
            'active_quests': self.active_quests,
            'metadata': self.metadata
        }


@dataclass
class QuestSuggestion:
    """A suggested quest for the user."""
    quest_id: str
    title: str
    description: str
    quest_type: str  # 'main', 'side', 'daily', 'achievement'
    difficulty: str  # 'easy', 'medium', 'hard', 'expert'
    estimated_duration: str  # '5 minutes', '1 hour', '1 day'
    xp_reward: int
    skill_rewards: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    reasoning: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quest suggestion to dictionary."""
        return {
            'quest_id': self.quest_id,
            'title': self.title,
            'description': self.description,
            'quest_type': self.quest_type,
            'difficulty': self.difficulty,
            'estimated_duration': self.estimated_duration,
            'xp_reward': self.xp_reward,
            'skill_rewards': self.skill_rewards,
            'prerequisites': self.prerequisites,
            'tags': self.tags,
            'confidence_score': self.confidence_score,
            'reasoning': self.reasoning,
            'metadata': self.metadata
        }
    
    def is_available(self, user_level: int, user_skills: List[str]) -> bool:
        """Check if quest is available for the user."""
        # Check level requirements
        if self.difficulty == 'expert' and user_level < 10:
            return False
        elif self.difficulty == 'hard' and user_level < 5:
            return False
        
        # Check skill prerequisites
        for prereq in self.prerequisites:
            if prereq not in user_skills:
                return False
        
        return True
    
    def get_difficulty_score(self) -> int:
        """Get numerical difficulty score."""
        difficulty_scores = {
            'easy': 1,
            'medium': 2,
            'hard': 3,
            'expert': 4
        }
        return difficulty_scores.get(self.difficulty, 1) 