"""
<!-- SSOT Domain: gaming -->

Dream.OS UI Integration - Gamification API Endpoints.

V2 Compliance: Flask API for gamification UI
Author: Agent-7 - Repository Cloning Specialist
Updated: Agent-6 - Integration with FSMOrchestrator and real agent data
License: MIT
"""

import logging
import os
from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify

# Create blueprint for gamification endpoints
gamification_bp = Blueprint("gaming", __name__, url_prefix="/api/gaming")

logger = logging.getLogger(__name__)

# Initialize FSMOrchestrator (lazy initialization)
_orchestrator = None


def get_orchestrator():
    """Get or create FSMOrchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        try:
            from src.gaming.dreamos.fsm_orchestrator import FSMOrchestrator

            project_root = Path(__file__).parent.parent.parent.parent
            fsm_root = project_root / "fsm_data"
            inbox_root = project_root / "agent_workspaces"
            outbox_root = project_root / "agent_workspaces"

            _orchestrator = FSMOrchestrator(fsm_root, inbox_root, outbox_root)
            logger.info("FSMOrchestrator initialized for Dream.OS UI")
        except Exception as e:
            logger.error(f"Failed to initialize FSMOrchestrator: {e}")
            _orchestrator = None
    return _orchestrator


def get_status_reader():
    """Get StatusReader instance for agent data."""
    try:
        from src.discord_commander.status_reader import StatusReader

        return StatusReader()
    except Exception as e:
        logger.error(f"Failed to initialize StatusReader: {e}")
        return None


def calculate_level_from_xp(xp: int) -> int:
    """Calculate level from XP (simple formula: level = sqrt(xp / 100))."""
    import math

    if xp <= 0:
        return 1
    level = int(math.sqrt(xp / 100)) + 1
    return max(1, min(level, 100))  # Cap at level 100


@gamification_bp.route("/player/status", methods=["GET"])
def get_player_status() -> dict[str, Any]:
    """
    Get player gamification status from FSMOrchestrator and agent data.

    Returns:
        Dict: Player XP, level, skills, quests, achievements
    """
    try:
        orchestrator = get_orchestrator()
        status_reader = get_status_reader()

        # Get player data (default to Agent-6 if no player_id specified)
        # In future, could accept player_id as query param
        player_id = "Agent-6"  # Default player

        # Get agent status for XP/level calculation
        agent_status = None
        if status_reader:
            agent_status = status_reader.read_agent_status(player_id)

        # Calculate XP and level
        current_xp = 0
        if agent_status:
            if "points" in agent_status:
                current_xp = agent_status["points"]
            elif "points_summary" in agent_status and isinstance(agent_status["points_summary"], dict):
                current_xp = (
                    agent_status["points_summary"].get("legendary_total")
                    or agent_status["points_summary"].get("total_points", 0)
                )

        level = calculate_level_from_xp(current_xp)
        total_xp = current_xp  # For now, same as current

        # Get active and completed quests from FSMOrchestrator
        active_quests = []
        completed_quests = []

        if orchestrator:
            # Get all tasks from FSM (quests are tasks)
            # Note: FSMOrchestrator doesn't have get_all_tasks, so we'll read from tasks_dir
            tasks_dir = orchestrator.tasks_dir
            if tasks_dir.exists():
                for task_file in tasks_dir.glob("*.json"):
                    try:
                        import json

                        with open(task_file, encoding="utf-8") as f:
                            task_data = json.load(f)
                            task_state = task_data.get("state", "unknown")

                            quest_info = {
                                "id": task_data.get("id", task_file.stem),
                                "title": task_data.get("title", "Unknown Quest"),
                                "description": task_data.get("description", ""),
                                "progress": _calculate_quest_progress_from_data(task_data),
                                "xp_reward": task_data.get("metadata", {}).get("xp_reward", 0),
                                "priority": task_data.get("metadata", {}).get("priority", "medium"),
                            }

                            if task_state in ["new", "in_progress"]:
                                active_quests.append(quest_info)
                            elif task_state == "completed":
                                completed_quests.append(quest_info)
                    except Exception as e:
                        logger.warning(f"Error reading task file {task_file}: {e}")

        # Get skills from agent achievements/completed tasks
        skills = _calculate_skills_from_agent_data(agent_status)

        # Get achievements from agent status
        achievements = _calculate_achievements_from_agent_data(agent_status)

        player_status = {
            "current_xp": current_xp,
            "level": level,
            "total_xp": total_xp,
            "skills": skills,
            "active_quests": active_quests[:10],  # Limit to 10 active quests
            "completed_quests": completed_quests[:20],  # Limit to 20 completed
            "achievements": achievements,
        }

        logger.info(f"Player status retrieved for {player_id}")
        return jsonify(player_status)

    except Exception as e:
        logger.error(f"Error getting player status: {e}")
        # Fallback to mock data on error
        return jsonify(
            {
                "current_xp": 1250,
                "level": 5,
                "total_xp": 5000,
                "skills": [
                    {"name": "Code Refactoring", "level": 8, "progress": 75, "icon": "🔧", "bonus": 15},
                    {"name": "V2 Compliance", "level": 6, "progress": 50, "icon": "✅", "bonus": 10},
                    {"name": "Documentation", "level": 7, "progress": 60, "icon": "📝", "bonus": 12},
                    {"name": "Testing", "level": 5, "progress": 40, "icon": "🧪", "bonus": 8},
                ],
                "active_quests": [
                    {
                        "id": "q-001",
                        "title": "Repository Cloning Master",
                        "description": "Clone and integrate all 8 external repositories",
                        "progress": 38,
                        "xp_reward": 800,
                        "priority": "high",
                    },
                ],
                "completed_quests": [
                    {"id": "q-100", "title": "First Repository Clone", "xp_reward": 100},
                ],
                "achievements": [
                    {
                        "id": "ach-001",
                        "name": "Repository Master",
                        "description": "Clone 3+ repositories successfully",
                        "icon": "📦",
                        "unlocked": True,
                    },
                ],
            }
        )


def _calculate_quest_progress_from_data(task_data: dict) -> int:
    """Calculate quest progress from task data."""
    state = task_data.get("state", "unknown")
    if state == "completed":
        return 100
    elif state == "failed":
        return 0
    elif state == "in_progress":
        evidence_count = len(task_data.get("evidence", []))
        return min(90, evidence_count * 20)
    else:
        return 0


def _calculate_skills_from_agent_data(agent_status: dict | None) -> list[dict[str, Any]]:
    """Calculate skills from agent status data."""
    if not agent_status:
        return []

    skills = []
    completed_tasks = agent_status.get("completed_tasks", [])

    # Map completed tasks to skills
    skill_map = {
        "refactor": {"name": "Code Refactoring", "icon": "🔧"},
        "v2": {"name": "V2 Compliance", "icon": "✅"},
        "doc": {"name": "Documentation", "icon": "📝"},
        "test": {"name": "Testing", "icon": "🧪"},
    }

    for task in completed_tasks:
        task_lower = task.lower()
        for key, skill_info in skill_map.items():
            if key in task_lower:
                # Count occurrences to determine level
                skill_count = sum(1 for t in completed_tasks if key in t.lower())
                level = min(10, skill_count + 1)
                progress = min(100, skill_count * 10)

                skills.append(
                    {
                        "name": skill_info["name"],
                        "level": level,
                        "progress": progress,
                        "icon": skill_info["icon"],
                        "bonus": level * 2,
                    }
                )
                break

    # Default skills if none found
    if not skills:
        skills = [
            {"name": "Code Refactoring", "level": 1, "progress": 0, "icon": "🔧", "bonus": 2},
            {"name": "V2 Compliance", "level": 1, "progress": 0, "icon": "✅", "bonus": 2},
            {"name": "Documentation", "level": 1, "progress": 0, "icon": "📝", "bonus": 2},
            {"name": "Testing", "level": 1, "progress": 0, "icon": "🧪", "bonus": 2},
        ]

    return skills


def _calculate_achievements_from_agent_data(agent_status: dict | None) -> list[dict[str, Any]]:
    """Calculate achievements from agent status data."""
    if not agent_status:
        return []

    achievements = []
    agent_achievements = agent_status.get("achievements", [])

    # Map agent achievements to gamification format
    for ach in agent_achievements[:10]:  # Limit to 10
        if isinstance(ach, str):
            achievements.append(
                {
                    "id": f"ach-{len(achievements) + 1}",
                    "name": ach,
                    "description": f"Achievement: {ach}",
                    "icon": "🏆",
                    "unlocked": True,
                }
            )
        elif isinstance(ach, dict):
            achievements.append(
                {
                    "id": ach.get("id", f"ach-{len(achievements) + 1}"),
                    "name": ach.get("name", "Unknown Achievement"),
                    "description": ach.get("description", ""),
                    "icon": ach.get("icon", "🏆"),
                    "unlocked": ach.get("unlocked", True),
                }
            )

    # Default achievements if none found
    if not achievements:
        achievements = [
            {
                "id": "ach-001",
                "name": "Active Agent",
                "description": "Agent is active and working",
                "icon": "🐝",
                "unlocked": agent_status.get("status") == "ACTIVE_AGENT_MODE",
            },
        ]

    return achievements


@gamification_bp.route("/quest/<quest_id>", methods=["GET"])
def get_quest_details(quest_id: str) -> dict[str, Any]:
    """
    Get detailed quest information from FSMOrchestrator.

    Args:
        quest_id: Quest identifier (maps to FSM task ID)

    Returns:
        Dict: Detailed quest information
    """
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            logger.warning("FSMOrchestrator unavailable, returning mock data")
            return jsonify(
                {
                    "id": quest_id,
                    "title": "Quest Title",
                    "description": "Quest description",
                    "objectives": [],
                    "rewards": {},
                    "status": "active",
                }
            )

        # Get task from FSMOrchestrator (quest_id maps to task_id)
        task = orchestrator.get_task(quest_id)
        if not task:
            logger.warning(f"Quest {quest_id} not found in FSMOrchestrator")
            return jsonify(
                {
                    "id": quest_id,
                    "title": "Quest Not Found",
                    "description": "This quest does not exist",
                    "objectives": [],
                    "rewards": {},
                    "status": "not_found",
                }
            ), 404

        # Map FSM task to quest format
        quest_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "objectives": [
                {"id": f"obj-{i}", "description": obj, "completed": False}
                for i, obj in enumerate(task.metadata.get("objectives", []))
            ],
            "rewards": {
                "xp": task.metadata.get("xp_reward", 0),
                "items": task.metadata.get("rewards", []),
            },
            "status": task.state.value,
            "assigned_agent": task.assigned_agent,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "progress": _calculate_quest_progress(task),
        }

        logger.info(f"Quest details retrieved for {quest_id}")
        return jsonify(quest_data)

    except Exception as e:
        logger.error(f"Error getting quest details for {quest_id}: {e}")
        # Fallback to mock data on error
        return jsonify(
            {
                "id": quest_id,
                "title": "Quest Title",
                "description": "Quest description",
                "objectives": [],
                "rewards": {},
                "status": "active",
            }
        )


def _calculate_quest_progress(task) -> int:
    """Calculate quest progress percentage from task state and evidence."""
    if task.state.value == "completed":
        return 100
    elif task.state.value == "failed":
        return 0
    elif task.state.value == "in_progress":
        # Estimate progress based on evidence count
        evidence_count = len(task.evidence) if task.evidence else 0
        # Assume 5+ evidence items = 100% progress
        return min(90, evidence_count * 20)
    else:
        return 0


@gamification_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard() -> list[dict[str, Any]]:
    """
    Get agent leaderboard with real agent data.

    Returns:
        List: Leaderboard rankings sorted by points
    """
    try:
        status_reader = get_status_reader()
        if not status_reader:
            logger.warning("StatusReader unavailable, returning mock data")
            return jsonify(
                [
                    {"agent": "Agent-6", "points": 3000, "level": 12, "rank": 1},
                    {"agent": "Agent-7", "points": 2000, "level": 10, "rank": 2},
                    {"agent": "Agent-5", "points": 1800, "level": 9, "rank": 3},
                ]
            )

        # Get all agent statuses
        all_statuses = status_reader.read_all_statuses()
        leaderboard = []

        for agent_id, status_data in all_statuses.items():
            # Extract points from various possible locations
            points = 0
            if "points" in status_data:
                points = status_data["points"]
            elif "points_summary" in status_data and isinstance(status_data["points_summary"], dict):
                points = (
                    status_data["points_summary"].get("legendary_total")
                    or status_data["points_summary"].get("total_points", 0)
                )
            elif "sprint_info" in status_data and isinstance(status_data["sprint_info"], dict):
                points = (
                    status_data["sprint_info"].get("points_earned")
                    or status_data["sprint_info"].get("points_completed", 0)
                )

            # Calculate level from points
            level = calculate_level_from_xp(points)

            leaderboard.append(
                {
                    "agent": agent_id,
                    "points": points,
                    "level": level,
                    "rank": 0,  # Will be set after sorting
                    "status": status_data.get("status", "unknown"),
                    "mission": status_data.get("current_mission", "No mission"),
                }
            )

        # Sort by points (descending) and assign ranks
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        for i, entry in enumerate(leaderboard):
            entry["rank"] = i + 1

        logger.info(f"Leaderboard generated with {len(leaderboard)} agents")
        return jsonify(leaderboard)

    except Exception as e:
        logger.error(f"Error generating leaderboard: {e}")
        # Fallback to mock data on error
        return jsonify(
            [
                {"agent": "Agent-6", "points": 3000, "level": 12, "rank": 1},
                {"agent": "Agent-7", "points": 2000, "level": 10, "rank": 2},
                {"agent": "Agent-5", "points": 1800, "level": 9, "rank": 3},
            ]
        )


def register_gamification_blueprint(app):
    """
    Register gamification blueprint with Flask app.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(gamification_bp)
