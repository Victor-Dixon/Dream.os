"""
Chat Presence Routes
====================

Flask routes for chat presence orchestrator operations.
Wires chat presence orchestrator to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.chat_presence_handlers import ChatPresenceHandlers

# Create blueprint
chat_presence_bp = Blueprint("chat_presence", __name__, url_prefix="/api/chat-presence")

# Create handler instance (BaseHandler pattern)
chat_presence_handlers = ChatPresenceHandlers()


@chat_presence_bp.route("/update", methods=["POST"])
def update_presence():
    """Update chat presence status."""
    return chat_presence_handlers.handle_update(request)


@chat_presence_bp.route("/status", methods=["GET"])
def get_status():
    """Get chat presence status."""
    return chat_presence_handlers.handle_get_status(request)


@chat_presence_bp.route("/list", methods=["GET"])
def list_presences():
    """List all chat presences."""
    return chat_presence_handlers.handle_list(request)


@chat_presence_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for chat presence services."""
    return jsonify({"status": "ok", "service": "chat_presence"}), 200



