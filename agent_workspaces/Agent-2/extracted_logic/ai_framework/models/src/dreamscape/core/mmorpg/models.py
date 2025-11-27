#!/usr/bin/env python3
"""
MMORPG Data Models
==================

This module contains ONLY data models, enums, and dataclasses for the MMORPG system.
Following the Single Responsibility Principle - this module only handles data structures.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Union
from enum import Enum
from datetime import datetime
# Removed circular import - these classes will be defined locally or imported when needed

# =============================================================================
# ENUMS
# =============================================================================

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

# =============================================================================
# CORE GAME MODELS
# =============================================================================

@dataclass
class Quest:
    """Represents a quest in the MMORPG."""
    id: str
    title: str
    description: str
    quest_type: QuestType
    difficulty: int  # 1-10
    xp_reward: int
    skill_rewards: Dict[str, int]
    status: str = "available"  # available, active, completed, failed
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    conversation_id: Optional[str] = None

@dataclass
class Skill:
    """Represents a skill in the MMORPG."""
    name: str
    current_level: int = 0
    experience_points: int = 0
    max_level: int = 100
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class ArchitectTier:
    """Represents an architect tier in the MMORPG."""
    tier_level: int
    tier_name: str
    experience_required: int
    abilities_unlocked: List[str] = field(default_factory=list)
    achieved_at: Optional[datetime] = None

@dataclass
class Guild:
    """Represents a guild in the MMORPG."""
    id: str
    name: str
    description: str = ""
    leader_id: str = ""
    members: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Equipment:
    """Represents equipment in the MMORPG."""
    id: str
    name: str
    type: str  # weapon, armor, accessory, tool
    rarity: str  # common, rare, epic, legendary, mythic, divine
    level_req: int
    stats: Dict[str, float] = field(default_factory=dict)
    abilities: List[str] = field(default_factory=list)
    description: str = ""
    flavor_text: str = ""
    obtained_from: str = ""

@dataclass
class Title:
    """Represents a title in the MMORPG."""
    id: str
    name: str
    requirement: str
    description: str
    rarity: str
    bonus_effects: List[str] = field(default_factory=list)
    obtained_at: datetime = field(default_factory=datetime.now)

@dataclass
class Ability:
    """Represents an ability in the MMORPG."""
    id: str
    name: str
    type: str  # active, passive, ultimate
    description: str
    cooldown: int
    level_req: int
    effects: List[Dict] = field(default_factory=list)
    scaling: Dict[str, float] = field(default_factory=dict)

@dataclass
class Character:
    """Represents a character in the MMORPG."""
    id: str
    name: str
    titles: List[Title] = field(default_factory=list)
    equipment: Dict[str, Equipment] = field(default_factory=dict)
    abilities: List[Ability] = field(default_factory=list)
    active_title: Optional[str] = None
    active_abilities: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    stats: Dict[str, float] = field(default_factory=dict)

@dataclass
class Player:
    """Represents a player in the MMORPG."""
    name: str
    architect_tier: str = "Tier 1 - Novice"
    xp: int = 0
    total_conversations: int = 0
    total_messages: int = 0
    total_words: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

@dataclass
class Achievement:
    """Represents an achievement in the MMORPG."""
    id: str
    name: str
    description: str
    category: str  # 'quest', 'skill', 'project', 'milestone', 'special'
    difficulty: int  # 1-10 scale
    xp_reward: int
    completed_at: str
    evidence: str  # URL, file path, or description of proof
    tags: List[str] = field(default_factory=list)
    impact_score: int = 5  # 1-10 scale for resume impact

@dataclass
class GameState:
    """Represents the current game state."""
    current_tier: int
    total_xp: int
    skills: Dict[str, Skill] = field(default_factory=dict)
    quests: Dict[str, Quest] = field(default_factory=dict)
    architect_tiers: Dict[int, ArchitectTier] = field(default_factory=dict)
    guilds: Dict[str, Guild] = field(default_factory=dict)
    achievements: List[Achievement] = field(default_factory=list)
    badges: List[Achievement] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class ProgressEvent:
    """Represents a progress event that awards XP and skills."""
    trigger: ProgressTrigger
    xp_amount: int
    skill_rewards: Dict[str, int]
    description: str
    conversation_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

# =============================================================================
# CONFIGURATION MODELS
# =============================================================================

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

# Additional classes for compatibility
class SkillLevel:
    """Skill level enumeration."""
    NOVICE = 1
    APPRENTICE = 2
    JOURNEYMAN = 3
    EXPERT = 4
    MASTER = 5

class SkillDefinition:
    """Skill definition for compatibility."""
    def __init__(self, name: str, description: str, category: str):
        self.name = name
        self.description = description
        self.category = category

class SkillTreeNode:
    """Skill tree node for compatibility."""
    def __init__(self, skill_name: str, level: int, xp: int, category: str):
        self.skill_name = skill_name
        self.level = level
        self.xp = xp
        self.category = category

class AISkillAnalysis:
    """AI skill analysis for compatibility."""
    def __init__(self, skill_name: str, category: str, proficiency_level: str):
        self.skill_name = skill_name
        self.category = category
        self.proficiency_level = proficiency_level

class ResumeSkill:
    """Resume skill for compatibility."""
    def __init__(self, name: str, level: int, category: str):
        self.name = name
        self.level = level
        self.category = category

class Project:
    """Project for compatibility."""
    def __init__(self, name: str, description: str, technologies: List[str]):
        self.name = name
        self.description = description
        self.technologies = technologies

class AIProjectAnalysis:
    """AI project analysis for compatibility."""
    def __init__(self, project_name: str, description: str, technologies: List[str]):
        self.project_name = project_name
        self.description = description
        self.technologies = technologies
