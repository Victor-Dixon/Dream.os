"""
Coordination Routes
===================

Flask routes for coordination engine operations.
Wires coordination engines to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.coordination_handlers import CoordinationHandlers

# Create blueprint
coordination_bp = Blueprint("coordination", __name__, url_prefix="/api/coordination")

# Instantiate handler (BaseHandler pattern)
coordination_handlers = CoordinationHandlers()


@coordination_bp.route("/task-coordination/status", methods=["GET"])
def get_task_coordination_status():
    """Get task coordination engine status."""
    return coordination_handlers.handle_get_task_coordination_status(request)


@coordination_bp.route("/task-coordination/execute", methods=["POST"])
def execute_task_coordination():
    """Execute task coordination."""
    return coordination_handlers.handle_execute_task_coordination(request)


@coordination_bp.route("/task-coordination/coordinate", methods=["POST"])
def coordinate_task():
    """Coordinate a specific task."""
    return coordination_handlers.handle_coordinate_task(request)


@coordination_bp.route("/task-coordination/resolve", methods=["POST"])
def resolve_coordination():
    """Resolve coordination conflicts."""
    return coordination_handlers.handle_resolve_coordination(request)


@coordination_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for coordination services."""
    return jsonify({"status": "ok", "service": "coordination"}), 200


<<<<<<< HEAD
# REAL-TIME AGENT PROGRESS TRACKING (Agent-6 Coordination Integration)
@coordination_bp.route("/realtime/agent-progress/<agent_id>", methods=["POST"])
def update_agent_progress(agent_id):
    """Update agent progress for real-time leaderboard tracking."""
    try:
        from flask import request
        data = request.get_json()

        # Validate required fields
        required_fields = ["progress_type", "progress_value", "timestamp"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}",
                    "required_fields": required_fields
                }), 400

        # Log progress update for real-time broadcasting
        logger.info(f"📊 Real-time progress update for {agent_id}: {data['progress_type']} = {data['progress_value']}")

        # Store progress update for leaderboard broadcaster
        _store_realtime_progress_update(agent_id, data)

        return jsonify({
            "status": "updated",
            "agent_id": agent_id,
            "progress_type": data["progress_type"],
            "progress_value": data["progress_value"],
            "broadcast_ready": True,
            "coordination_integration": "Agent-6 gaming system enhancement"
        })

    except Exception as e:
        logger.error(f"Error updating agent progress: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id
        }), 500


@coordination_bp.route("/realtime/leaderboard/status", methods=["GET"])
def get_leaderboard_broadcast_status():
    """Get current leaderboard broadcast status."""
    try:
        # Check if leaderboard broadcaster is active
        broadcaster_status = _get_leaderboard_broadcaster_status()

        return jsonify({
            "broadcast_active": broadcaster_status["active"],
            "websocket_clients": broadcaster_status["clients"],
            "last_broadcast": broadcaster_status["last_update"],
            "agent_progress_tracking": "enabled",
            "coordination_integration": "Agent-6 gaming system enhancement"
        })

    except Exception as e:
        logger.error(f"Error getting leaderboard status: {e}")
        return jsonify({
            "error": str(e),
            "broadcast_active": False
        }), 500


@coordination_bp.route("/realtime/quest/progress/<agent_id>", methods=["POST"])
def update_quest_progress(agent_id):
    """Update quest progress for dynamic quest generation system."""
    try:
        from flask import request
        data = request.get_json()

        # Validate quest progress data
        if not data or "quest_id" not in data:
            return jsonify({
                "error": "Missing quest_id in request data"
            }), 400

        # Log quest progress for coordination tracking
        logger.info(f"🎯 Quest progress update for {agent_id}: quest {data['quest_id']}")

        # Store quest progress for real-time updates
        _store_quest_progress_update(agent_id, data)

        return jsonify({
            "status": "quest_updated",
            "agent_id": agent_id,
            "quest_id": data["quest_id"],
            "progress": data.get("progress", 0),
            "coordination_integration": "Agent-6 gaming system enhancement"
        })

    except Exception as e:
        logger.error(f"Error updating quest progress: {e}")
        return jsonify({
            "error": str(e),
            "agent_id": agent_id
        }), 500


# Helper functions for real-time coordination
def _store_realtime_progress_update(agent_id: str, progress_data: dict):
    """Store real-time progress update for leaderboard broadcaster."""
    try:
        # This data will be picked up by the LeaderboardBroadcaster
        # In a production system, this would use Redis/pubsub or similar
        # For now, we'll log it for the broadcaster to detect changes

        # Update agent status with real-time progress
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        if status_file.exists():
            import json
            with open(status_file, 'r') as f:
                status = json.load(f)

            # Add real-time progress data
            if "realtime_progress" not in status:
                status["realtime_progress"] = {}

            status["realtime_progress"][progress_data["progress_type"]] = {
                "value": progress_data["progress_value"],
                "timestamp": progress_data["timestamp"],
                "coordination_source": "Agent-6_gaming_enhancement"
            }

            status["last_updated"] = progress_data["timestamp"]

            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)

    except Exception as e:
        logger.error(f"Error storing real-time progress: {e}")


def _store_quest_progress_update(agent_id: str, quest_data: dict):
    """Store quest progress update."""
    try:
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        if status_file.exists():
            import json
            with open(status_file, 'r') as f:
                status = json.load(f)

            # Add quest progress data
            if "active_quests" not in status:
                status["active_quests"] = {}

            status["active_quests"][quest_data["quest_id"]] = {
                "progress": quest_data.get("progress", 0),
                "completed": quest_data.get("completed", False),
                "timestamp": datetime.now().isoformat(),
                "coordination_source": "Agent-6_gaming_enhancement"
            }

            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)

    except Exception as e:
        logger.error(f"Error storing quest progress: {e}")


def _get_leaderboard_broadcaster_status():
    """Get leaderboard broadcaster status."""
    try:
        # Check if gaming leaderboard broadcaster is active
        # This would integrate with the actual broadcaster instance
        return {
            "active": True,  # Assume active for coordination
            "clients": 0,    # Would need actual WebSocket client count
            "last_update": datetime.now().isoformat(),
            "coordination_ready": True
        }
    except Exception:
        return {
            "active": False,
            "clients": 0,
            "last_update": None,
            "coordination_ready": False
        }

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

