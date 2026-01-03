"""
MMORPG System Enums
Contains all enumeration types for the Dreamscape MMORPG system.
"""

from enum import Enum


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


class ArchitectTier(Enum):
    """Architect tiers for player progression."""
    NOVICE = "Tier 1 - Novice"
    APPRENTICE = "Tier 2 - Apprentice"
    ARCHITECT = "Tier 3 - Architect"
    MASTER_ARCHITECT = "Tier 4 - Master Architect"
    GRANDMASTER_ARCHITECT = "Tier 5 - Grandmaster Architect"


# Tier definitions for architect progression
TIER_DEFINITIONS = [
    (1, "Novice", 0),
    (2, "Apprentice", 1000),
    (3, "Architect", 5000),
    (4, "Master Architect", 15000),
    (5, "Grandmaster Architect", 50000)
] 