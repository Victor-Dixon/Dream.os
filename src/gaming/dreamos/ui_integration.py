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
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify
from flask_socketio import SocketIO, emit

# Create blueprint for gamification endpoints
gamification_bp = Blueprint("gaming", __name__, url_prefix="/api/gaming")

# Initialize SocketIO for real-time updates
socketio = SocketIO(cors_allowed_origins="*")

logger = logging.getLogger(__name__)

# Initialize FSMOrchestrator (lazy initialization)
_orchestrator = None

# Real-time leaderboard broadcaster
_leaderboard_broadcaster = None

# Quest system manager
_quest_manager = None


class LeaderboardBroadcaster:
    """Real-time leaderboard broadcaster using WebSocket."""

    def __init__(self, socketio_instance: SocketIO):
        self.socketio = socketio_instance
        self.status_reader = None
        self.running = False
        self.thread = None
        self.last_leaderboard_hash = None

    def start_broadcasting(self):
        """Start the real-time broadcasting thread."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.thread.start()
        logger.info("🎯 Leaderboard real-time broadcasting started")

    def stop_broadcasting(self):
        """Stop the real-time broadcasting."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        logger.info("🎯 Leaderboard real-time broadcasting stopped")

    def _get_leaderboard_data(self) -> list[dict[str, Any]]:
        """Get current leaderboard data."""
        try:
            if not self.status_reader:
                self.status_reader = get_status_reader()

            if not self.status_reader:
                return self._get_mock_leaderboard()

            # Get all agent statuses
            all_statuses = self.status_reader.read_all_statuses()
            leaderboard = []

            for agent_id, status_data in all_statuses.items():
                # Extract points from various possible locations
                points = self._extract_points(status_data)

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
                        "last_updated": status_data.get("last_updated", ""),
                        "phase": status_data.get("current_phase", "unknown"),
                    }
                )

            # Sort by points (descending) and assign ranks
            leaderboard.sort(key=lambda x: x["points"], reverse=True)
            for i, entry in enumerate(leaderboard):
                entry["rank"] = i + 1

            return leaderboard

        except Exception as e:
            logger.error(f"Error generating leaderboard for broadcast: {e}")
            return self._get_mock_leaderboard()

    def _extract_points(self, status_data: dict) -> int:
        """Extract points from status data."""
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
        return points

    def _get_mock_leaderboard(self) -> list[dict[str, Any]]:
        """Return mock leaderboard data."""
        return [
            {"agent": "Agent-6", "points": 3000, "level": 12, "rank": 1, "status": "ACTIVE", "mission": "Gaming Enhancement", "last_updated": "", "phase": "PHASE_5"},
            {"agent": "Agent-7", "points": 2000, "level": 10, "rank": 2, "status": "ACTIVE", "mission": "Web Development", "last_updated": "", "phase": "PHASE_5"},
            {"agent": "Agent-5", "points": 1800, "level": 9, "rank": 3, "status": "ACTIVE", "mission": "Business Intelligence", "last_updated": "", "phase": "PHASE_5"},
        ]

    def _calculate_hash(self, data: list) -> str:
        """Calculate a simple hash of the leaderboard data for change detection."""
        import hashlib
        data_str = str(sorted([f"{item['agent']}:{item['points']}" for item in data]))
        return hashlib.md5(data_str.encode()).hexdigest()

    def _broadcast_loop(self):
        """Main broadcasting loop."""
        while self.running:
            try:
                leaderboard = self._get_leaderboard_data()
                current_hash = self._calculate_hash(leaderboard)

                # Only broadcast if leaderboard has changed
                if current_hash != self.last_leaderboard_hash:
                    self.socketio.emit('leaderboard_update', {
                        'leaderboard': leaderboard,
                        'timestamp': int(time.time() * 1000),
                        'agent_count': len(leaderboard)
                    }, namespace='/gamification')
                    self.last_leaderboard_hash = current_hash
                    logger.debug(f"📡 Broadcast leaderboard update to {len(leaderboard)} agents")

            except Exception as e:
                logger.error(f"Error in leaderboard broadcast loop: {e}")

            # Broadcast every 30 seconds
            time.sleep(30)

    def force_broadcast(self):
        """Force an immediate broadcast."""
        try:
            leaderboard = self._get_leaderboard_data()
            self.socketio.emit('leaderboard_update', {
                'leaderboard': leaderboard,
                'timestamp': int(time.time() * 1000),
                'agent_count': len(leaderboard),
                'forced': True
            }, namespace='/gamification')
            logger.info("🎯 Forced leaderboard broadcast")
        except Exception as e:
            logger.error(f"Error in forced broadcast: {e}")


def get_leaderboard_broadcaster() -> LeaderboardBroadcaster:
    """Get or create leaderboard broadcaster instance."""
    global _leaderboard_broadcaster
    if _leaderboard_broadcaster is None:
        _leaderboard_broadcaster = LeaderboardBroadcaster(socketio)
    return _leaderboard_broadcaster


def get_quest_manager():
    """Get or create quest manager instance."""
    global _quest_manager
    if _quest_manager is None:
        from ..quests.quest_manager import QuestManager
        _quest_manager = QuestManager()
        logger.info("🎯 Quest manager initialized")
    return _quest_manager


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


# WebSocket event handlers
@socketio.on('connect', namespace='/gamification')
def handle_gamification_connect():
    """Handle client connection to gamification namespace."""
    logger.info("🎮 Client connected to gamification WebSocket")
    # Send initial leaderboard data
    broadcaster = get_leaderboard_broadcaster()
    leaderboard = broadcaster._get_leaderboard_data()
    emit('leaderboard_update', {
        'leaderboard': leaderboard,
        'timestamp': int(time.time() * 1000),
        'agent_count': len(leaderboard),
        'initial': True
    })


@socketio.on('disconnect', namespace='/gamification')
def handle_gamification_disconnect():
    """Handle client disconnection from gamification namespace."""
    logger.info("🎮 Client disconnected from gamification WebSocket")


@socketio.on('request_leaderboard_update', namespace='/gamification')
def handle_leaderboard_request():
    """Handle manual leaderboard update request."""
    logger.info("📡 Manual leaderboard update requested")
    broadcaster = get_leaderboard_broadcaster()
    broadcaster.force_broadcast()


@gamification_bp.route("/leaderboard/realtime", methods=["GET"])
def get_realtime_leaderboard_status():
    """
    Get real-time leaderboard status and WebSocket connection info.

    Returns:
        Dict: Status information for real-time leaderboard
    """
    try:
        broadcaster = get_leaderboard_broadcaster()
        return jsonify({
            "realtime_enabled": True,
            "websocket_namespace": "/gamification",
            "broadcast_interval": 30,
            "status": "active" if broadcaster.running else "inactive",
            "connected_clients": len(socketio.server.manager.rooms.get('/gamification', {})),
            "features": [
                "real_time_updates",
                "live_ranking_changes",
                "agent_status_tracking",
                "mission_progress_sync"
            ]
        })
    except Exception as e:
        logger.error(f"Error getting realtime leaderboard status: {e}")
        return jsonify({
            "realtime_enabled": False,
            "error": str(e),
            "status": "error"
        }), 500


@gamification_bp.route("/leaderboard/force-update", methods=["POST"])
def force_leaderboard_update():
    """
    Force an immediate leaderboard update broadcast.

    Returns:
        Dict: Update status
    """
    try:
        broadcaster = get_leaderboard_broadcaster()
        broadcaster.force_broadcast()
        return jsonify({
            "status": "success",
            "message": "Leaderboard update broadcast initiated",
            "timestamp": int(time.time() * 1000)
        })
    except Exception as e:
        logger.error(f"Error forcing leaderboard update: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ================================
# SOCIAL API ENDPOINTS
# ================================

@gamification_bp.route("/social/profile/<agent_id>", methods=["GET"])
def get_social_profile(agent_id: str):
    """
    Get social profile for an agent.

    Args:
        agent_id: Agent identifier

    Returns:
        Social profile data
    """
    try:
        from ..social.social_profile_manager import SocialProfileManager

        profile_manager = SocialProfileManager()
        profile = profile_manager.get_or_create_profile(agent_id)

        return jsonify({
            "agent_id": agent_id,
            "profile": profile.to_dict(),
            "social_score": profile.get_social_score(),
            "active_relationships": len(profile.get_active_relationships()),
            "total_interactions": len(profile.interaction_history)
        })

    except Exception as e:
        logger.error(f"Error getting social profile for {agent_id}: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id
        }), 500


@gamification_bp.route("/social/leaderboard", methods=["GET"])
def get_social_leaderboard():
    """
    Get social leaderboard ranked by social engagement.

    Query Parameters:
        limit: Maximum number of results (default: 10)

    Returns:
        Social leaderboard
    """
    try:
        from ..social.social_profile_manager import SocialProfileManager

        limit = int(request.args.get('limit', 10))
        profile_manager = SocialProfileManager()
        leaderboard = profile_manager.get_social_leaderboard(limit)

        return jsonify({
            "leaderboard": leaderboard,
            "limit": limit,
            "total_agents": len(leaderboard)
        })

    except Exception as e:
        logger.error(f"Error getting social leaderboard: {e}")
        return jsonify({
            "error": str(e),
            "leaderboard": []
        }), 500


@gamification_bp.route("/social/interaction", methods=["POST"])
def record_social_interaction():
    """
    Record a social interaction between agents.

    Expected JSON payload:
    {
        "from_agent": "Agent-1",
        "to_agent": "Agent-2",
        "interaction_type": "collaboration",
        "context": "Brief description",
        "impact_score": 0.5
    }

    Returns:
        Success status
    """
    try:
        from ..social.social_profile_manager import SocialProfileManager
        from ..models.social_models import SocialInteraction, InteractionType

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate required fields
        required_fields = ["from_agent", "to_agent", "interaction_type", "context"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Create interaction
        interaction = SocialInteraction(
            interaction_id="",
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            interaction_type=InteractionType(data["interaction_type"]),
            timestamp=datetime.now(),
            context=data["context"],
            impact_score=data.get("impact_score", 0.0),
            metadata=data.get("metadata", {})
        )

        # Record interaction
        profile_manager = SocialProfileManager()
        success = profile_manager.record_interaction(interaction)

        if success:
            return jsonify({
                "success": True,
                "interaction_id": interaction.interaction_id,
                "message": f"Social interaction recorded: {data['from_agent']} -> {data['to_agent']}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to record interaction"
            }), 500

    except Exception as e:
        logger.error(f"Error recording social interaction: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/social/network", methods=["GET"])
def get_social_network():
    """
    Get social network data for visualization.

    Returns:
        Network data with nodes and links
    """
    try:
        from ..social.social_profile_manager import SocialProfileManager

        profile_manager = SocialProfileManager()
        network_data = profile_manager.get_collaboration_network()

        return jsonify(network_data)

    except Exception as e:
        logger.error(f"Error getting social network: {e}")
        return jsonify({
            "error": str(e),
            "nodes": [],
            "links": []
        }), 500


@gamification_bp.route("/social/relationships/<agent_id>", methods=["GET"])
def get_agent_relationships(agent_id: str):
    """
    Get relationships for a specific agent.

    Args:
        agent_id: Agent identifier

    Returns:
        Agent relationships
    """
    try:
        from ..social.social_profile_manager import SocialProfileManager

        profile_manager = SocialProfileManager()
        profile = profile_manager.get_profile(agent_id)

        if not profile:
            return jsonify({
                "agent_id": agent_id,
                "relationships": [],
                "message": "No social profile found"
            })

        relationships = profile.get_active_relationships()

        return jsonify({
            "agent_id": agent_id,
            "relationships": [rel.to_dict() for rel in relationships],
            "total_relationships": len(relationships),
            "active_relationships": len([r for r in relationships if r.is_active()])
        })

    except Exception as e:
        logger.error(f"Error getting relationships for {agent_id}: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id,
            "relationships": []
        }), 500


@gamification_bp.route("/social/insights/<agent_id>", methods=["GET"])
def get_social_insights(agent_id: str):
    """
    Get social insights and recommendations for an agent.

    Args:
        agent_id: Agent identifier

    Returns:
        Social insights and recommendations
    """
    try:
        from ..social.social_integration_service import SocialIntegrationService

        integration_service = SocialIntegrationService()
        insights = integration_service.get_agent_social_insights(agent_id)

        return jsonify(insights)

    except Exception as e:
        logger.error(f"Error getting social insights for {agent_id}: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id,
            "insights": "Error retrieving insights"
        }), 500


@gamification_bp.route("/social/activity", methods=["POST"])
def record_agent_activity():
    """
    Record agent activity for automatic social interaction detection.

    Expected JSON payload:
    {
        "agent_id": "Agent-1",
        "activity_type": "message_sent",
        "metadata": {
            "recipients": ["Agent-2", "Agent-3"],
            "category": "a2a",
            "context": "Coordination message"
        }
    }

    Returns:
        Success status
    """
    try:
        from ..social.social_integration_service import SocialIntegrationService

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        agent_id = data.get("agent_id")
        activity_type = data.get("activity_type")
        metadata = data.get("metadata", {})

        if not agent_id or not activity_type:
            return jsonify({"error": "agent_id and activity_type are required"}), 400

        integration_service = SocialIntegrationService()
        integration_service.analyze_agent_activity(agent_id, {
            "type": activity_type,
            "metadata": metadata
        })

        return jsonify({
            "success": True,
            "message": f"Activity recorded for {agent_id}: {activity_type}"
        })

    except Exception as e:
        logger.error(f"Error recording agent activity: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ================================
# ANALYTICS API ENDPOINTS
# ================================

@gamification_bp.route("/analytics/metrics/<metric_name>", methods=["GET"])
def get_metric_data(metric_name: str):
    """
    Get performance metric data and statistics.

    Args:
        metric_name: Name of the metric to retrieve

    Query Parameters:
        hours: Time range in hours (default: 24)

    Returns:
        Metric data and statistics
    """
    try:
        from ..analytics.performance_analytics import PerformanceAnalytics

        hours = int(request.args.get('hours', 24))
        analytics = PerformanceAnalytics()

        # Get metric statistics
        stats = analytics.calculate_metric_stats(metric_name, hours)

        # Get recent history
        history = analytics.get_metric_history(metric_name, hours)

        return jsonify({
            "metric_name": metric_name,
            "time_range_hours": hours,
            "statistics": stats,
            "history": history[-50:],  # Last 50 data points
            "data_points": len(history)
        })

    except Exception as e:
        logger.error(f"Error getting metric data for {metric_name}: {e}")
        return jsonify({
            "error": str(e),
            "metric_name": metric_name
        }), 500


@gamification_bp.route("/analytics/health", methods=["GET"])
def get_system_health():
    """
    Get overall system health score and component breakdown.

    Returns:
        System health assessment
    """
    try:
        from ..analytics.performance_analytics import PerformanceAnalytics

        analytics = PerformanceAnalytics()
        health_score = analytics.get_system_health_score()

        return jsonify(health_score)

    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        return jsonify({
            "error": str(e),
            "overall_score": 0,
            "health_status": "error"
        }), 500


@gamification_bp.route("/analytics/report", methods=["GET"])
def get_performance_report():
    """
    Get comprehensive performance report.

    Query Parameters:
        hours: Time range in hours (default: 24)

    Returns:
        Complete performance report
    """
    try:
        from ..analytics.performance_analytics import PerformanceAnalytics

        hours = int(request.args.get('hours', 24))
        analytics = PerformanceAnalytics()

        report = analytics.generate_performance_report(hours)

        return jsonify(report)

    except Exception as e:
        logger.error(f"Error generating performance report: {e}")
        return jsonify({
            "error": str(e),
            "generated_at": datetime.now().isoformat(),
            "status": "error"
        }), 500


@gamification_bp.route("/analytics/metrics", methods=["POST"])
def record_performance_metric():
    """
    Record a performance metric.

    Expected JSON payload:
    {
        "metric_name": "response_time",
        "value": 150.5,
        "metadata": {
            "source": "api_endpoint",
            "user_agent": "Agent-6"
        }
    }

    Returns:
        Success status
    """
    try:
        from ..analytics.performance_analytics import PerformanceAnalytics

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        metric_name = data.get("metric_name")
        value = data.get("value")
        metadata = data.get("metadata", {})

        if not metric_name or value is None:
            return jsonify({"error": "metric_name and value are required"}), 400

        analytics = PerformanceAnalytics()
        analytics.record_metric(metric_name, value, metadata=metadata)

        return jsonify({
            "success": True,
            "message": f"Metric '{metric_name}' recorded: {value}",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error recording performance metric: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/analytics/baseline/<metric_name>", methods=["POST"])
def set_metric_baseline(metric_name: str):
    """
    Set baseline value for a performance metric.

    Expected JSON payload:
    {
        "baseline_value": 100.0,
        "description": "Expected response time baseline"
    }

    Returns:
        Success status
    """
    try:
        from ..analytics.performance_analytics import PerformanceAnalytics

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        baseline_value = data.get("baseline_value")
        if baseline_value is None:
            return jsonify({"error": "baseline_value is required"}), 400

        analytics = PerformanceAnalytics()
        analytics.set_baseline(metric_name, baseline_value)

        return jsonify({
            "success": True,
            "metric_name": metric_name,
            "baseline_value": baseline_value,
            "message": f"Baseline set for {metric_name}: {baseline_value}"
        })

    except Exception as e:
        logger.error(f"Error setting baseline for {metric_name}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/analytics/baseline/<metric_name>", methods=["GET"])
def get_metric_baseline(metric_name: str):
    """
    Get baseline comparison for a performance metric.

    Returns:
        Baseline comparison data
    """
    try:
        from ..analytics.performance_analytics import PerformanceAnalytics

        analytics = PerformanceAnalytics()
        comparison = analytics.get_baseline_comparison(metric_name)

        return jsonify({
            "metric_name": metric_name,
            "comparison": comparison
        })

    except Exception as e:
        logger.error(f"Error getting baseline comparison for {metric_name}: {e}")
        return jsonify({
            "error": str(e),
            "metric_name": metric_name
        }), 500


# ================================
# QUEST API ENDPOINTS
# ================================

@gamification_bp.route("/quests/<agent_id>", methods=["GET"])
def get_agent_quests(agent_id: str):
    """
    Get all quests for a specific agent.

    Args:
        agent_id: Agent identifier

    Returns:
        List of quest data
    """
    try:
        quest_manager = get_quest_manager()
        quests = quest_manager.get_agent_quests(agent_id)

        return jsonify({
            "agent_id": agent_id,
            "quests": [quest.to_dict() for quest in quests],
            "total_quests": len(quests),
            "active_quests": len([q for q in quests if q.status.value == "active"]),
            "completed_quests": len([q for q in quests if q.status.value == "completed"])
        })

    except Exception as e:
        logger.error(f"Error getting quests for agent {agent_id}: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id,
            "quests": []
        }), 500


@gamification_bp.route("/quests/<agent_id>/available", methods=["GET"])
def get_available_quests(agent_id: str):
    """
    Get available quests that can be started by an agent.

    Args:
        agent_id: Agent identifier

    Returns:
        List of available quests
    """
    try:
        quest_manager = get_quest_manager()
        available_quests = quest_manager.get_available_quests(agent_id, limit=5)

        return jsonify({
            "agent_id": agent_id,
            "available_quests": [quest.to_dict() for quest in available_quests],
            "count": len(available_quests)
        })

    except Exception as e:
        logger.error(f"Error getting available quests for agent {agent_id}: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id,
            "available_quests": []
        }), 500


@gamification_bp.route("/quests/<agent_id>/create", methods=["POST"])
def create_agent_quest(agent_id: str):
    """
    Create a new quest for an agent.

    Args:
        agent_id: Agent identifier

    Query Parameters:
        type: Quest type (collaboration, performance, innovation, etc.)
        difficulty: Quest difficulty (easy, medium, hard, epic, legendary)

    Returns:
        Created quest data
    """
    try:
        from flask import request

        # Get parameters from query string or JSON body
        quest_type_str = request.args.get('type', 'collaboration')
        difficulty_str = request.args.get('difficulty', 'medium')

        # Validate and convert parameters
        try:
            quest_type = QuestType(quest_type_str)
        except ValueError:
            return jsonify({
                "error": f"Invalid quest type: {quest_type_str}",
                "valid_types": [t.value for t in QuestType]
            }), 400

        try:
            difficulty = QuestDifficulty(difficulty_str)
        except ValueError:
            return jsonify({
                "error": f"Invalid difficulty: {difficulty_str}",
                "valid_difficulties": [d.value for d in QuestDifficulty]
            }), 400

        quest_manager = get_quest_manager()
        quest = quest_manager.create_quest(agent_id, quest_type, difficulty)

        if quest:
            return jsonify({
                "success": True,
                "quest": quest.to_dict(),
                "message": f"Quest '{quest.title}' created for agent {agent_id}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to create quest"
            }), 500

    except Exception as e:
        logger.error(f"Error creating quest for agent {agent_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/quests/<quest_id>/start", methods=["POST"])
def start_quest(quest_id: str):
    """
    Start a quest.

    Args:
        quest_id: Quest identifier

    Returns:
        Success status
    """
    try:
        quest_manager = get_quest_manager()
        success = quest_manager.start_quest(quest_id)

        if success:
            quest = quest_manager.get_quest(quest_id)
            return jsonify({
                "success": True,
                "quest_id": quest_id,
                "message": f"Quest started successfully",
                "started_at": quest.started_at.isoformat() if quest and quest.started_at else None
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to start quest (may already be active or not found)"
            }), 400

    except Exception as e:
        logger.error(f"Error starting quest {quest_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/quests/<quest_id>/progress", methods=["POST"])
def update_quest_progress(quest_id: str):
    """
    Update progress for a quest objective.

    Args:
        quest_id: Quest identifier

    Query Parameters:
        objective_id: Objective identifier
        increment: Progress increment (default: 1)

    Returns:
        Updated progress data
    """
    try:
        from flask import request

        objective_id = request.args.get('objective_id')
        increment = int(request.args.get('increment', 1))

        if not objective_id:
            return jsonify({
                "success": False,
                "error": "objective_id parameter is required"
            }), 400

        quest_manager = get_quest_manager()
        success = quest_manager.update_quest_progress(quest_id, objective_id, increment)

        if success:
            quest = quest_manager.get_quest(quest_id)
            if quest:
                return jsonify({
                    "success": True,
                    "quest_id": quest_id,
                    "objective_id": objective_id,
                    "progress_increment": increment,
                    "overall_progress": quest.progress_percentage,
                    "completed": quest.status.value == "completed"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Quest not found after update"
                }), 404
        else:
            return jsonify({
                "success": False,
                "error": "Failed to update quest progress"
            }), 400

    except Exception as e:
        logger.error(f"Error updating quest progress: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/quests/<quest_id>/complete", methods=["POST"])
def complete_quest(quest_id: str):
    """
    Mark a quest as completed.

    Args:
        quest_id: Quest identifier

    Returns:
        Completion status and rewards
    """
    try:
        quest_manager = get_quest_manager()
        success = quest_manager.complete_quest(quest_id)

        if success:
            quest = quest_manager.get_quest(quest_id)
            if quest:
                return jsonify({
                    "success": True,
                    "quest_id": quest_id,
                    "message": f"Quest '{quest.title}' completed!",
                    "rewards": {
                        "xp_reward": quest.rewards.xp_reward,
                        "bonus_points": quest.rewards.bonus_points,
                        "achievements": quest.rewards.achievements,
                        "special_unlocks": quest.rewards.special_unlocks
                    },
                    "completed_at": quest.completed_at.isoformat() if quest.completed_at else None
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Quest not found after completion"
                }), 404
        else:
            return jsonify({
                "success": False,
                "error": "Failed to complete quest"
            }), 400

    except Exception as e:
        logger.error(f"Error completing quest {quest_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@gamification_bp.route("/quests/stats/<agent_id>", methods=["GET"])
def get_quest_stats(agent_id: str):
    """
    Get quest statistics for an agent.

    Args:
        agent_id: Agent identifier

    Returns:
        Quest statistics
    """
    try:
        quest_manager = get_quest_manager()

        active_count = quest_manager.get_active_quests_count(agent_id)
        completed_count = quest_manager.get_completed_quests_count(agent_id)

        return jsonify({
            "agent_id": agent_id,
            "active_quests": active_count,
            "completed_quests": completed_count,
            "total_quests": active_count + completed_count,
            "completion_rate": (completed_count / (active_count + completed_count)) * 100 if (active_count + completed_count) > 0 else 0
        })

    except Exception as e:
        logger.error(f"Error getting quest stats for agent {agent_id}: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id,
            "active_quests": 0,
            "completed_quests": 0,
            "total_quests": 0,
            "completion_rate": 0
        }), 500


def register_gamification_blueprint(app):
    """
    Register gamification blueprint with Flask app.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(gamification_bp)

    # Start leaderboard broadcaster
    broadcaster = get_leaderboard_broadcaster()
    broadcaster.start_broadcasting()

    logger.info("🎯 Gamification blueprint registered with real-time leaderboard and quest system support")


def initialize_socketio(app):
    """
    Initialize SocketIO with the Flask app.

    Args:
        app: Flask application instance
    """
    socketio.init_app(app, cors_allowed_origins="*")
    logger.info("🔌 SocketIO initialized for gamification real-time features")
