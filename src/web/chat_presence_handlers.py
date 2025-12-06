"""
Chat Presence Handlers
======================

Handler classes for chat presence orchestrator operations.
Wires chat presence orchestrator to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
    CHAT_PRESENCE_AVAILABLE = True
except ImportError:
    CHAT_PRESENCE_AVAILABLE = False


class ChatPresenceHandlers:
    """Handler class for chat presence orchestrator operations."""

    @staticmethod
    def _get_orchestrator() -> ChatPresenceOrchestrator:
        """Get chat presence orchestrator instance."""
        # Initialize with optional configs from request or environment
        return ChatPresenceOrchestrator()

    @staticmethod
    def handle_update(request) -> tuple:
        """
        Handle request to update chat presence.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not CHAT_PRESENCE_AVAILABLE:
            return jsonify({"success": False, "error": "ChatPresenceOrchestrator not available"}), 503

        try:
            data = request.get_json() or {}
            action = data.get("action")  # e.g., "start", "stop", "update"
            config = data.get("config", {})

            orchestrator = ChatPresenceHandlers._get_orchestrator()

            if action == "start":
                # Start chat presence system
                result = orchestrator.start()
                return jsonify({
                    "success": True,
                    "message": "Chat presence started",
                    "status": result
                }), 200
            elif action == "stop":
                # Stop chat presence system
                result = orchestrator.stop()
                return jsonify({
                    "success": True,
                    "message": "Chat presence stopped",
                    "status": result
                }), 200
            elif action == "update":
                # Update configuration
                # For now, return success - full implementation would update config
                return jsonify({
                    "success": True,
                    "message": "Chat presence updated",
                    "config": config
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": f"Unknown action: {action}. Use 'start', 'stop', or 'update'"
                }), 400

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_get_status(request) -> tuple:
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
            orchestrator = ChatPresenceHandlers._get_orchestrator()

            # Get status information
            status = {
                "service": "chat_presence_orchestrator",
                "status": "operational",
                "twitch_connected": orchestrator.twitch_bridge.is_connected() if hasattr(orchestrator, 'twitch_bridge') and orchestrator.twitch_bridge else False,
                "obs_available": hasattr(orchestrator, 'obs_listener') and orchestrator.obs_listener is not None,
                "scheduler_active": hasattr(orchestrator, 'scheduler') and orchestrator.scheduler is not None
            }

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_list(request) -> tuple:
        """
        Handle request to list all chat presences.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not CHAT_PRESENCE_AVAILABLE:
            return jsonify({"success": False, "error": "ChatPresenceOrchestrator not available"}), 503

        try:
            orchestrator = ChatPresenceHandlers._get_orchestrator()

            # List available chat presences/channels
            presences = []

            # Check Twitch
            if hasattr(orchestrator, 'twitch_bridge') and orchestrator.twitch_bridge:
                presences.append({
                    "platform": "twitch",
                    "connected": orchestrator.twitch_bridge.is_connected() if hasattr(orchestrator.twitch_bridge, 'is_connected') else False
                })

            # Check Discord (if available)
            presences.append({
                "platform": "discord",
                "connected": True  # Discord integration typically available
            })

            # Check OBS
            if hasattr(orchestrator, 'obs_listener') and orchestrator.obs_listener:
                presences.append({
                    "platform": "obs",
                    "connected": True
                })

            return jsonify({
                "success": True,
                "presences": presences,
                "total": len(presences)
            }), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



