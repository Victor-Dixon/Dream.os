import pytest
from datetime import datetime

from dreamscape.core.mmorpg import (
    Quest, QuestType, Skill, SkillType, Character, Player,
    Achievement, ProgressEvent, MMORPGConfig, SkillConfig, ProgressTrigger,
    KnowledgeNode,
)


def test_quest_init():
    quest = Quest(
        id="q1", 
        title="First Quest", 
        description="A test quest",
        quest_type=QuestType.BUG_HUNT,
        difficulty=5,
        xp_reward=100,
        skill_rewards={"debugging": 10}
    )
    assert quest.id == "q1"
    assert quest.title == "First Quest"
    assert quest.quest_type == QuestType.BUG_HUNT
    # TODO: Add more assertions for quest logic

def test_skill_init():
    skill = Skill(name="Swordsmanship", current_level=1)
    assert skill.name == "Swordsmanship"
    assert skill.current_level == 1
    # TODO: Add more assertions for skill logic

def test_character_init():
    # Character requires all fields to be provided
    character = Character(
        id="char1", 
        name="TestHero",
        titles=[],  # Required field
        equipment={},  # Required field
        abilities=[],  # Required field
        active_title=None,  # Required field
        active_abilities=[],  # Required field
        achievements=[],  # Required field
        stats={}  # Required field
    )
    assert character.id == "char1"
    assert character.name == "TestHero"
    # TODO: Add more assertions for character state

def test_achievement_init():
    achievement = Achievement(
        id="ach1",
        name="First Blood",
        description="First achievement",
        category="quest",
        difficulty=1,
        xp_reward=50,
        completed_at="2024-01-01",
        evidence="test evidence",
        tags=[],  # Required field
        impact_score=5  # Required field
    )
    assert achievement.id == "ach1"
    assert achievement.name == "First Blood"
    # TODO: Add more assertions for achievement logic

def test_progress_event_init():
    event = ProgressEvent(
        trigger=ProgressTrigger.CONVERSATION_ANALYSIS,
        xp_amount=100,
        skill_rewards={"debugging": 10},
        description="Test progress event",
        conversation_id="conv1",
        timestamp=datetime.now()  # Required field
    )
    assert event.trigger == ProgressTrigger.CONVERSATION_ANALYSIS
    # TODO: Add more assertions for progress logic


def test_knowledge_node_init():
    node = KnowledgeNode(topic="AsyncIO", category="python", level=2, xp=150)
    assert node.topic == "AsyncIO"
    assert node.level == 2
    assert node.xp == 150

# TODO: Add tests for model methods, state changes, and integration with systems 