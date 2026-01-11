"""Dynamic Quest Generator.
<!-- SSOT Domain: gaming -->

Generates dynamic quests based on agent capabilities, status, and current system state.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: SOLID principles, dependency injection, comprehensive quest templates
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..models.quest_models import (
    Quest,
    QuestType,
    QuestDifficulty,
    QuestObjective,
    QuestReward,
    QuestStatus,
    IQuestGenerator
)

logger = logging.getLogger(__name__)


class DynamicQuestGenerator(IQuestGenerator):
    """Dynamic quest generator that creates quests based on agent context."""

    def __init__(self):
        self.quest_templates = self._load_quest_templates()

    def _load_quest_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load quest templates for different types and difficulties."""
        return {
            "collaboration": {
                "easy": {
                    "title": "Team Coordination Starter",
                    "description": "Coordinate with 2 other agents on a simple task",
                    "objectives": [
                        {"description": "Send coordination message to 2 agents", "target": 2},
                        {"description": "Receive acknowledgment from both agents", "target": 2}
                    ],
                    "xp_base": 100
                },
                "medium": {
                    "title": "Cross-Agent Integration",
                    "description": "Integrate features across 3 different agent workspaces",
                    "objectives": [
                        {"description": "Identify integration points", "target": 3},
                        {"description": "Implement basic integration", "target": 1}
                    ],
                    "xp_base": 250
                }
            },
            "performance": {
                "easy": {
                    "title": "Efficiency Optimization",
                    "description": "Improve performance metrics by 10%",
                    "objectives": [
                        {"description": "Identify performance bottleneck", "target": 1},
                        {"description": "Implement optimization", "target": 1}
                    ],
                    "xp_base": 150
                },
                "medium": {
                    "title": "System Health Enhancement",
                    "description": "Improve overall system health metrics",
                    "objectives": [
                        {"description": "Run health check", "target": 1},
                        {"description": "Fix identified issues", "target": 3}
                    ],
                    "xp_base": 300
                }
            },
            "innovation": {
                "easy": {
                    "title": "Feature Enhancement",
                    "description": "Add a new feature to existing functionality",
                    "objectives": [
                        {"description": "Identify enhancement opportunity", "target": 1},
                        {"description": "Implement new feature", "target": 1}
                    ],
                    "xp_base": 200
                },
                "medium": {
                    "title": "System Integration Innovation",
                    "description": "Create innovative integration between systems",
                    "objectives": [
                        {"description": "Design integration approach", "target": 1},
                        {"description": "Implement and test integration", "target": 1}
                    ],
                    "xp_base": 400
                }
            },
            "development": {
                "easy": {
                    "title": "Code Quality Improvement",
                    "description": "Improve code quality metrics in your workspace",
                    "objectives": [
                        {"description": "Fix linting errors", "target": 5},
                        {"description": "Add documentation", "target": 3}
                    ],
                    "xp_base": 120
                },
                "medium": {
                    "title": "API Enhancement",
                    "description": "Enhance existing API with new endpoints",
                    "objectives": [
                        {"description": "Design new API endpoint", "target": 1},
                        {"description": "Implement and test endpoint", "target": 1}
                    ],
                    "xp_base": 350
                }
            }
        }

    def generate_quest(self, agent_id: str, agent_capabilities: List[str],
                      agent_status: Dict[str, Any]) -> Optional[Quest]:
        """Generate a quest based on agent context."""
        try:
            # Determine appropriate quest type based on agent capabilities
            quest_type = self._determine_quest_type(agent_capabilities, agent_status)

            # Determine difficulty based on agent performance
            difficulty = self._determine_difficulty(agent_status)

            # Get template for this type/difficulty combination
            template = self._get_template(quest_type, difficulty)
            if not template:
                return None

            # Create quest objectives
            objectives = self._create_objectives(template["objectives"])

            # Create rewards
            rewards = self._create_rewards(template["xp_base"], difficulty)

            # Create quest
            quest = Quest(
                quest_id="",
                title=template["title"],
                description=template["description"],
                quest_type=quest_type,
                difficulty=difficulty,
                objectives=objectives,
                rewards=rewards,
                assigned_agent=agent_id,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=24),  # 24 hour expiry
                tags=self._generate_tags(quest_type, difficulty),
                metadata={
                    "generated_by": "DynamicQuestGenerator",
                    "agent_capabilities": agent_capabilities,
                    "agent_status": agent_status
                }
            )

            logger.info(f"Generated quest '{quest.title}' for agent {agent_id}")
            return quest

        except Exception as e:
            logger.error(f"Error generating quest for agent {agent_id}: {e}")
            return None

    def _determine_quest_type(self, capabilities: List[str],
                            status: Dict[str, Any]) -> QuestType:
        """Determine appropriate quest type based on agent context."""
        # Map capabilities to quest types
        capability_map = {
            "integration": QuestType.INTEGRATION,
            "coordination": QuestType.COORDINATION,
            "development": QuestType.DEVELOPMENT,
            "optimization": QuestType.OPTIMIZATION,
            "quality_assurance": QuestType.MAINTENANCE,
            "research": QuestType.INNOVATION,
            "data_analysis": QuestType.PERFORMANCE
        }

        # Find matching capabilities
        matching_types = []
        for cap in capabilities:
            cap_lower = cap.lower()
            for key, quest_type in capability_map.items():
                if key in cap_lower:
                    matching_types.append(quest_type)
                    break

        # Default to collaboration if no specific match
        if not matching_types:
            return QuestType.COLLABORATION

        # Return random matching type
        return random.choice(matching_types)

    def _determine_difficulty(self, status: Dict[str, Any]) -> QuestDifficulty:
        """Determine quest difficulty based on agent status."""
        # Check current phase and mission priority
        current_phase = status.get("current_phase", "PHASE_1")
        mission_priority = status.get("mission_priority", "NORMAL")

        # Higher phases get harder quests
        if "PHASE_5" in current_phase:
            return random.choice([QuestDifficulty.HARD, QuestDifficulty.EPIC])
        elif "PHASE_4" in current_phase:
            return random.choice([QuestDifficulty.MEDIUM, QuestDifficulty.HARD])
        elif "PHASE_3" in current_phase:
            return random.choice([QuestDifficulty.EASY, QuestDifficulty.MEDIUM])
        else:
            return random.choice([QuestDifficulty.EASY, QuestDifficulty.MEDIUM, QuestDifficulty.HARD])

    def _get_template(self, quest_type: QuestType,
                     difficulty: QuestDifficulty) -> Optional[Dict[str, Any]]:
        """Get quest template for type and difficulty."""
        type_key = quest_type.value
        diff_key = difficulty.value

        if type_key not in self.quest_templates:
            return None

        type_templates = self.quest_templates[type_key]
        return type_templates.get(diff_key)

    def _create_objectives(self, objective_templates: List[Dict[str, Any]]) -> List[QuestObjective]:
        """Create quest objectives from templates."""
        objectives = []
        for i, template in enumerate(objective_templates):
            objective = QuestObjective(
                objective_id=f"obj_{i+1}",
                description=template["description"],
                target_value=template["target"],
                current_value=0,
                completed=False,
                metadata={"template": template}
            )
            objectives.append(objective)
        return objectives

    def _create_rewards(self, xp_base: int, difficulty: QuestDifficulty) -> QuestReward:
        """Create quest rewards based on XP base and difficulty."""
        # Scale XP by difficulty
        difficulty_multiplier = {
            QuestDifficulty.EASY: 1.0,
            QuestDifficulty.MEDIUM: 1.5,
            QuestDifficulty.HARD: 2.0,
            QuestDifficulty.EPIC: 3.0,
            QuestDifficulty.LEGENDARY: 4.0
        }

        xp_reward = int(xp_base * difficulty_multiplier[difficulty])
        bonus_points = int(xp_reward * 0.2)  # 20% bonus

        # Generate achievements based on difficulty
        achievements = []
        if difficulty in [QuestDifficulty.HARD, QuestDifficulty.EPIC, QuestDifficulty.LEGENDARY]:
            achievements.append(f"{difficulty.value.title()} Quest Master")
        if xp_reward > 500:
            achievements.append("High Value Contributor")

        return QuestReward(
            xp_reward=xp_reward,
            bonus_points=bonus_points,
            achievements=achievements,
            special_unlocks=[],
            metadata={"difficulty": difficulty.value}
        )

    def _generate_tags(self, quest_type: QuestType, difficulty: QuestDifficulty) -> List[str]:
        """Generate tags for the quest."""
        tags = [quest_type.value, difficulty.value]

        # Add special tags based on type
        if quest_type == QuestType.COLLABORATION:
            tags.extend(["teamwork", "coordination"])
        elif quest_type == QuestType.INNOVATION:
            tags.extend(["creativity", "improvement"])
        elif quest_type == QuestType.PERFORMANCE:
            tags.extend(["optimization", "efficiency"])

        return tags