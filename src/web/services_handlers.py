"""
Services Layer Handlers
=======================

Handler classes for service layer operations.
Wires services to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
    CHAT_PRESENCE_AVAILABLE = True
except ImportError:
    CHAT_PRESENCE_AVAILABLE = False


class ServicesHandlers:
    """Handler class for service layer operations."""

    @staticmethod
    def handle_get_chat_presence_status(request) -> tuple:
        """
        Handle request to get chat presence status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not CHAT_PRESENCE_AVAILABLE:
            return jsonify({"success": False, "error": "ChatPresenceOrchestrator not available"}), 503

        try:
            orchestrator = ChatPresenceOrchestrator()
            status = orchestrator.get_status()

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_start_chat_presence(request) -> tuple:
        """
        Handle request to start chat presence.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not CHAT_PRESENCE_AVAILABLE:
            return jsonify({"success": False, "error": "ChatPresenceOrchestrator not available"}), 503

        try:
            orchestrator = ChatPresenceOrchestrator()
            result = orchestrator.start()

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_stop_chat_presence(request) -> tuple:
        """
        Handle request to stop chat presence.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not CHAT_PRESENCE_AVAILABLE:
            return jsonify({"success": False, "error": "ChatPresenceOrchestrator not available"}), 503

        try:
            orchestrator = ChatPresenceOrchestrator()
            result = orchestrator.stop()

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



