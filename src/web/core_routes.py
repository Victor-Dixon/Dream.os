"""
Core System Routes
=================

<!-- SSOT Domain: web -->

Flask routes for core system operations.
Wires core services to web layer.

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.core_handlers import CoreHandlers

# Create blueprint
core_bp = Blueprint("core", __name__, url_prefix="/api/core")


@core_bp.route("/agent-lifecycle/<agent_id>/status", methods=["GET"])
def get_agent_status(agent_id: str):
    """Get agent lifecycle status."""
    return CoreHandlers.handle_get_agent_lifecycle_status(request, agent_id)


@core_bp.route("/agent-lifecycle/<agent_id>/start-cycle", methods=["POST"])
def start_agent_cycle(agent_id: str):
    """Start agent lifecycle cycle."""
    return CoreHandlers.handle_start_cycle(request, agent_id)


@core_bp.route("/message-queue/status", methods=["GET"])
def get_message_queue_status():
    """Get message queue status."""
    return CoreHandlers.handle_get_message_queue_status(request)


@core_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for core services."""
    return jsonify({"status": "ok", "service": "core_system"}), 200


