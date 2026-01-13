#!/usr/bin/env python3
"""
MMORPG Models
============

Data models, enums, and dataclasses for the Dreamscape MMORPG system.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple, Union
from enum import Enum
from datetime import datetime
import math
import uuid


# Configuration classes
@dataclass
class MMORPGConfig:
    """Configuration for MMORPG system."""
    xp_multiplier: float = 1.0
    skill_decay_rate: float = 0.1
    quest_timeout_hours: int = 24
    max_active_quests: int = 5
    auto_save_interval: int = 300  # seconds

@dataclass
class SkillConfig:
    """Configuration for skill system."""
    base_xp_rate: float = 1.0
    skill_cap: int = 100
    level_scaling: float = 1.5
    cross_skill_bonus: float = 0.1

@dataclass
class ProgressConfig:
    """Configuration for progress tracking."""
    save_interval: int = 60  # seconds
    backup_enabled: bool = True
    max_backups: int = 10
    progress_file: str = "mmorpg_progress.json"


# Enums
class QuestType(Enum):
    """Types of quests in the Dreamscape MMORPG."""
    BUG_HUNT = "bug_hunt"
    FEATURE_RAID = "feature_raid"
    SYSTEM_CONVERGENCE = "system_convergence"
    KNOWLEDGE_EXPEDITION = "knowledge_expedition"
    LEGACY_MISSION = "legacy_mission"
    WORKFLOW_AUDIT = "workflow_audit"
    MARKET_ANALYSIS = "market_analysis"
    PERSONAL_STRATEGY = "personal_strategy"

class SkillType(Enum):
    """Core skills in the Dreamscape MMORPG."""
    SYSTEM_CONVERGENCE = "system_convergence"
    EXECUTION_VELOCITY = "execution_velocity"
    STRATEGIC_INTELLIGENCE = "strategic_intelligence"
    AI_SELF_ORGANIZATION = "ai_self_organization"
    DOMAIN_STABILIZATION = "domain_stabilization"

class ProgressTrigger(Enum):
    """Types of progress triggers that can award XP and skills."""
    CONVERSATION_ANALYSIS = "conversation_analysis"
    BREAKTHROUGH_DISCOVERY = "breakthrough_discovery"
    SKILL_APPLICATION = "skill_application"
    PROBLEM_SOLVING = "problem_solving"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    INNOVATION = "innovation"
    MENTORSHIP = "mentorship"
    SYSTEM_ARCHITECTURE = "system_architecture"
    CODE_REVIEW = "code_review"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    COLLABORATION = "collaboration"


# Core MMORPG Models
@dataclass
class Quest:
    """Quest model for MMORPG system."""
    id: str
    title: str
    description: str
    quest_type: QuestType
    difficulty: int  # 1-10
    xp_reward: int
    skill_rewards: Dict[str, int]
    status: str = "available"  # available, active, completed, failed
    created_at: datetime = None
    completed_at: datetime = None
    conversation_id: str = None

@dataclass
class Skill:
    """Skill model for MMORPG system."""
    name: str
    current_level: int = 0
    experience_points: int = 0
    max_level: int = 100
    last_updated: datetime = None

@dataclass
class ArchitectTier:
    """Architect tier model for MMORPG system."""
    tier_level: int
    tier_name: str
    experience_required: int
    abilities_unlocked: List[str]
    achieved_at: datetime = None

@dataclass
class Guild:
    """Guild model for MMORPG system."""
    id: str
    name: str
    description: str = ""
    leader_id: str = ""
    members: List[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.members is None:
            self.members = []

@dataclass
class GameState:
    """Game state model for MMORPG system."""
    current_tier: int
    total_xp: int
    skills: Dict[str, Skill]
    quests: Dict[str, Quest]
    architect_tiers: Dict[int, ArchitectTier]
    guilds: Dict[str, Guild]
    last_updated: datetime = None

@dataclass
class Player:
    """Player model for MMORPG system."""
    name: str
    architect_tier: str = "Tier 1 - Novice"
    xp: int = 0
    total_conversations: int = 0
    total_messages: int = 0
    total_words: int = 0
    created_at: datetime = None
    last_active: datetime = None
    
    def get_next_level_xp(self) -> int:
        """Get XP required for next level."""
        try:
            tier_parts = self.architect_tier.split()
            if len(tier_parts) >= 2:
                current_tier = int(tier_parts[1])
            else:
                current_tier = 1
            
            # Simple tier progression: 1000 XP per tier
            return current_tier * 1000
        except (ValueError, IndexError):
            return 100

@dataclass
class Achievement:
    """Achievement model for MMORPG system."""
    id: str
    name: str
    description: str
    category: str  # 'quest', 'skill', 'project', 'milestone', 'special'
    difficulty: int  # 1-10 scale
    xp_reward: int
    completed_at: str
    evidence: str  # URL, file path, or description of proof
    tags: List[str]
    impact_score: int  # 1-10 scale for resume impact

@dataclass
class ResumeSkill:
    """Resume skill model for MMORPG system."""
    name: str
    category: str  # 'technical', 'soft', 'domain', 'ai'
    current_level: int
    max_level: int
    current_xp: int
    next_level_xp: int
    description: str
    last_updated: str
    achievements: List[str]  # Achievement IDs that contributed

@dataclass
class Project:
    """Project model for MMORPG system."""
    id: str
    name: str
    description: str
    start_date: str
    end_date: Optional[str]
    status: str  # 'active', 'completed', 'paused', 'cancelled'
    technologies: List[str]
    achievements: List[str]
    impact_description: str
    team_size: int
    role: str

@dataclass
class SkillLevel:
    """Skill level model for MMORPG system."""
    level: int
    current_xp: int
    xp_to_next: int
    unlocks: List[str]

@dataclass
class SkillDefinition:
    """Skill definition model for MMORPG system."""
    name: str
    description: str
    category: str
    related_skills: List[str]
    max_level: int = 99

@dataclass
class Equipment:
    """Equipment model for MMORPG system."""
    id: str
    name: str
    type: str  # weapon, armor, accessory, tool
    rarity: str  # common, rare, epic, legendary, mythic, divine
    level_req: int
    stats: Dict[str, float]
    abilities: List[str]
    description: str
    flavor_text: str
    obtained_from: str

@dataclass
class Title:
    """Title model for MMORPG system."""
    id: str
    name: str
    requirement: str
    description: str
    rarity: str
    bonus_effects: List[str]
    obtained_at: datetime

@dataclass
class Ability:
    """Ability model for MMORPG system."""
    id: str
    name: str
    type: str  # active, passive, ultimate
    description: str
    cooldown: int
    effects: List[Dict]
    level_req: int
    scaling: Dict[str, float]

@dataclass
class Character:
    """Character model for MMORPG system."""
    id: str
    name: str
    titles: List[Title]
    equipment: Dict[str, Equipment]
    abilities: List[Ability]
    active_title: Optional[str]
    active_abilities: List[str]
    achievements: List[str]
    stats: Dict[str, float]

@dataclass
class ProgressEvent:
    """Progress event model for MMORPG system."""
    trigger: ProgressTrigger
    xp_amount: int
    skill_rewards: Dict[str, int]
    description: str
    conversation_id: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

@dataclass
class AISkillAnalysis:
    """AI skill analysis model for MMORPG system."""
    skill_name: str
    category: str
    proficiency_level: str  # 'beginner', 'intermediate', 'advanced', 'expert'
    confidence: float
    evidence: List[str]
    conversation_ids: List[str]
    last_used: datetime
    ai_insights: Dict[str, Any]
    skill_relationships: List[str]
    learning_path: List[str]

@dataclass
class AIProjectAnalysis:
    """AI project analysis model for MMORPG system."""
    project_name: str
    description: str
    technologies: List[str]
    complexity_level: str  # 'simple', 'moderate', 'complex', 'enterprise'
    impact_score: float  # 0.0 to 1.0
    team_size: int
    role: str
    duration_days: int
    conversation_ids: List[str]
    ai_insights: Dict[str, Any]
    achievements: List[str]

@dataclass
class SkillTreeNode:
    """Skill tree node model for MMORPG system."""
    skill_name: str
    level: int
    xp: int
    category: str
    dependencies: List[str]
    unlocks: List[str]
    ai_confidence: float
    last_updated: datetime
    metadata: Dict[str, Any]

@dataclass
class KnowledgeNode:
    """Knowledge node model for MMORPG system."""
    id: str
    name: str
    content: str
    category: str
    tags: List[str]
    connections: List[str]  # IDs of connected nodes
    created_at: datetime
    last_updated: datetime
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


# Tier definitions
TIER_DEFINITIONS = [
    (1, "Tier 1 - Novice", 0),
    (2, "Tier 2 - Apprentice", 1000),
    (3, "Tier 3 - Journeyman", 2000),
    (4, "Tier 4 - Expert", 3000),
    (5, "Tier 5 - Master", 4000),
    (6, "Tier 6 - Grandmaster", 5000),
    (7, "Tier 7 - Legend", 6000),
    (8, "Tier 8 - Mythic", 7000),
    (9, "Tier 9 - Divine", 8000),
    (10, "Tier 10 - Transcendent", 9000)
] 