"""
Core System Handlers
====================

<!-- SSOT Domain: web -->

Handler classes for core system operations.
Wires core services to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.core.agent_lifecycle import AgentLifecycle
    AGENT_LIFECYCLE_AVAILABLE = True
except ImportError:
    AGENT_LIFECYCLE_AVAILABLE = False

try:
    from src.core.utils.message_queue_utils import get_queue_status
    MESSAGE_QUEUE_AVAILABLE = True
except ImportError:
    MESSAGE_QUEUE_AVAILABLE = False


class CoreHandlers:
    """Handler class for core system operations."""

    @staticmethod
    def handle_get_agent_lifecycle_status(request, agent_id: str) -> tuple:
        """
        Handle request to get agent lifecycle status.

        Args:
            request: Flask request object
            agent_id: Agent identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        if not AGENT_LIFECYCLE_AVAILABLE:
            return jsonify({"success": False, "error": "AgentLifecycle not available"}), 503

        try:
            lifecycle = AgentLifecycle(agent_id)
            status = lifecycle.get_status()

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_start_cycle(request, agent_id: str) -> tuple:
        """
        Handle request to start agent lifecycle cycle.

        Args:
            request: Flask request object
            agent_id: Agent identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        if not AGENT_LIFECYCLE_AVAILABLE:
            return jsonify({"success": False, "error": "AgentLifecycle not available"}), 503

        try:
            lifecycle = AgentLifecycle(agent_id)
            lifecycle.start_cycle()

            return jsonify({"success": True, "message": f"Cycle started for {agent_id}"}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_get_message_queue_status(request) -> tuple:
        """
        Handle request to get message queue status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not MESSAGE_QUEUE_AVAILABLE:
            return jsonify({"success": False, "error": "Message queue utils not available"}), 503

        try:
            status = get_queue_status()
            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


