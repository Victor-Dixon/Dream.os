"""
Discord Routes
==============

Flask routes for Discord operations.
Wires Discord controllers and views to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.discord_handlers import DiscordHandlers

# Create blueprint
discord_bp = Blueprint("discord", __name__, url_prefix="/api/discord")

# Instantiate handler (BaseHandler pattern)
discord_handlers = DiscordHandlers()


@discord_bp.route("/swarm-tasks", methods=["GET"])
def get_swarm_tasks():
    """Get swarm tasks information."""
    return discord_handlers.handle_get_swarm_tasks(request)


@discord_bp.route("/templates/broadcast", methods=["GET"])
def get_broadcast_templates():
    """Get available broadcast templates."""
    return discord_handlers.handle_get_broadcast_templates(request)


@discord_bp.route("/control-panel/status", methods=["GET"])
def get_control_panel_status():
    """Get control panel status."""
    return discord_handlers.handle_get_control_panel_status(request)


@discord_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Discord services."""
    return jsonify({"status": "ok", "service": "discord"}), 200

