"""Quest Manager for Dynamic Quest System.
<!-- SSOT Domain: gaming -->

Manages quest lifecycle, progress tracking, and agent quest assignments.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: SOLID principles, comprehensive state management, validation
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .quest_generator import DynamicQuestGenerator
from ..models.quest_models import (
    Quest,
    QuestType,
    QuestDifficulty,
    QuestStatus,
    IQuestManager
)

logger = logging.getLogger(__name__)


class QuestManager(IQuestManager):
    """Manages quest lifecycle and progress tracking."""

    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.agent_quests: Dict[str, List[str]] = {}  # agent_id -> [quest_ids]
        self.generator = DynamicQuestGenerator()

    def create_quest(self, agent_id: str, quest_type: QuestType,
                    difficulty: QuestDifficulty,
                    agent_capabilities: Optional[List[str]] = None,
                    agent_status: Optional[Dict[str, Any]] = None) -> Optional[Quest]:
        """Create a new quest for an agent."""
        try:
            # Use provided context or default values
            capabilities = agent_capabilities or ["general"]
            status = agent_status or {"current_phase": "PHASE_1", "mission_priority": "NORMAL"}

            # Generate quest using the generator
            quest = self.generator.generate_quest(agent_id, capabilities, status)
            if not quest:
                logger.warning(f"Failed to generate quest for agent {agent_id}")
                return None

            # Store quest
            self.quests[quest.quest_id] = quest

            # Track agent quest assignment
            if agent_id not in self.agent_quests:
                self.agent_quests[agent_id] = []
            self.agent_quests[agent_id].append(quest.quest_id)

            # Clean up expired quests for this agent
            self._cleanup_expired_quests(agent_id)

            logger.info(f"Created quest '{quest.title}' ({quest.quest_id}) for agent {agent_id}")
            return quest

        except Exception as e:
            logger.error(f"Error creating quest for agent {agent_id}: {e}")
            return None

    def get_agent_quests(self, agent_id: str) -> List[Quest]:
        """Get all quests for an agent."""
        quest_ids = self.agent_quests.get(agent_id, [])
        agent_quests = []

        for quest_id in quest_ids:
            quest = self.quests.get(quest_id)
            if quest and not quest.is_expired():
                agent_quests.append(quest)
            elif quest and quest.is_expired() and quest.status == QuestStatus.ACTIVE:
                # Mark expired active quests as failed
                quest.fail_quest()

        return agent_quests

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Get a specific quest by ID."""
        quest = self.quests.get(quest_id)
        if quest and quest.is_expired() and quest.status == QuestStatus.ACTIVE:
            quest.fail_quest()
        return quest

    def update_quest_progress(self, quest_id: str, objective_id: str,
                            progress_increment: int = 1) -> bool:
        """Update progress for a specific quest objective."""
        try:
            quest = self.quests.get(quest_id)
            if not quest:
                return False

            if quest.status != QuestStatus.ACTIVE:
                return False

            # Find and update the objective
            objective = None
            for obj in quest.objectives:
                if obj.objective_id == objective_id:
                    objective = obj
                    break

            if not objective:
                return False

            # Update objective progress
            objective.update_progress(progress_increment)

            # Update overall quest progress
            quest.update_progress()

            logger.debug(f"Updated quest {quest_id} objective {objective_id}: +{progress_increment}")
            return True

        except Exception as e:
            logger.error(f"Error updating quest progress: {e}")
            return False

    def start_quest(self, quest_id: str) -> bool:
        """Start a quest."""
        try:
            quest = self.quests.get(quest_id)
            if not quest:
                return False

            return quest.start_quest()

        except Exception as e:
            logger.error(f"Error starting quest {quest_id}: {e}")
            return False

    def complete_quest(self, quest_id: str) -> bool:
        """Mark a quest as completed."""
        try:
            quest = self.quests.get(quest_id)
            if not quest:
                return False

            success = quest.complete_quest()
            if success:
                logger.info(f"Quest {quest_id} completed by agent {quest.assigned_agent}")

                # Award XP and achievements (would integrate with gamification system)
                self._award_quest_rewards(quest)

            return success

        except Exception as e:
            logger.error(f"Error completing quest {quest_id}: {e}")
            return False

    def fail_quest(self, quest_id: str) -> bool:
        """Mark a quest as failed."""
        try:
            quest = self.quests.get(quest_id)
            if not quest:
                return False

            success = quest.fail_quest()
            if success:
                logger.info(f"Quest {quest_id} failed for agent {quest.assigned_agent}")

            return success

        except Exception as e:
            logger.error(f"Error failing quest {quest_id}: {e}")
            return False

    def get_active_quests_count(self, agent_id: str) -> int:
        """Get count of active quests for an agent."""
        quests = self.get_agent_quests(agent_id)
        return len([q for q in quests if q.status == QuestStatus.ACTIVE])

    def get_completed_quests_count(self, agent_id: str) -> int:
        """Get count of completed quests for an agent."""
        quests = self.get_agent_quests(agent_id)
        return len([q for q in quests if q.status == QuestStatus.COMPLETED])

    def get_available_quests(self, agent_id: str, limit: int = 5) -> List[Quest]:
        """Get available quests that can be started by an agent."""
        # For now, generate new quests on demand
        # In a full implementation, this would have a pool of pre-generated quests
        available_quests = []

        # Generate quests of different types
        quest_types = [QuestType.COLLABORATION, QuestType.PERFORMANCE,
                      QuestType.INNOVATION, QuestType.DEVELOPMENT]

        for quest_type in quest_types[:limit]:
            quest = self.create_quest(agent_id, quest_type, QuestDifficulty.MEDIUM)
            if quest:
                available_quests.append(quest)

        return available_quests

    def _cleanup_expired_quests(self, agent_id: str):
        """Clean up expired quests for an agent."""
        if agent_id not in self.agent_quests:
            return

        active_quest_ids = []
        for quest_id in self.agent_quests[agent_id]:
            quest = self.quests.get(quest_id)
            if quest:
                if quest.is_expired() and quest.status == QuestStatus.ACTIVE:
                    quest.fail_quest()
                elif not quest.is_expired():
                    active_quest_ids.append(quest_id)
                # Remove expired completed/failed quests after 7 days
                elif quest.status in [QuestStatus.COMPLETED, QuestStatus.FAILED]:
                    completed_time = quest.completed_at or quest.created_at
                    if (datetime.now() - completed_time).days > 7:
                        del self.quests[quest_id]
                    else:
                        active_quest_ids.append(quest_id)

        self.agent_quests[agent_id] = active_quest_ids

    def _award_quest_rewards(self, quest: Quest):
        """Award quest completion rewards."""
        # This would integrate with the gamification system to award XP and achievements
        # For now, just log the rewards
        logger.info(f"Awarding quest rewards for {quest.quest_id}: "
                   f"{quest.rewards.xp_reward} XP, "
                   f"{quest.rewards.bonus_points} bonus points, "
                   f"achievements: {quest.rewards.achievements}")

        # Integrate with gamification system
        try:
            # Import gamification system if available
            from src.gaming.dreamos.ui_integration import GamificationSystem

            gamification = GamificationSystem()

            # Award XP and achievements
            gamification.award_xp(quest.rewards.xp_reward)
            gamification.award_achievement(quest.rewards.achievements)
            gamification.add_points(quest.rewards.bonus_points)

            # Update agent stats
            agent_stats = gamification.get_agent_stats()
            logger.info(f"Gamification updated - Total XP: {agent_stats.get('total_xp', 0)}, "
                       f"Level: {agent_stats.get('level', 1)}, "
                       f"Achievements: {len(agent_stats.get('achievements', []))}")

        except ImportError:
            # Fallback: create basic gamification data structure
            logger.warning("GamificationSystem not available - using fallback implementation")

            # Create or update agent gamification file
            gamification_file = Path("agent_workspaces") / "gamification_stats.json"

            try:
                # Load existing stats
                if gamification_file.exists():
                    with open(gamification_file, 'r') as f:
                        stats = json.load(f)
                else:
                    stats = {
                        "total_xp": 0,
                        "level": 1,
                        "achievements": [],
                        "bonus_points": 0,
                        "completed_quests": []
                    }

                # Update stats
                stats["total_xp"] += quest.rewards.xp_reward
                stats["bonus_points"] += quest.rewards.bonus_points
                stats["achievements"].extend(quest.rewards.achievements)
                stats["completed_quests"].append(quest.quest_id)

                # Calculate new level (simple XP-based leveling)
                new_level = (stats["total_xp"] // 1000) + 1
                if new_level > stats["level"]:
                    stats["level"] = new_level
                    logger.info(f"🎉 Level up! Reached level {new_level}")

                # Save updated stats
                with open(gamification_file, 'w') as f:
                    json.dump(stats, f, indent=2)

                logger.info(f"Gamification stats updated - Level {stats['level']}, "
                           f"Total XP: {stats['total_xp']}")

            except Exception as e:
                logger.error(f"Failed to update gamification stats: {e}")
        except Exception as e:
            logger.error(f"Failed to integrate with gamification system: {e}")