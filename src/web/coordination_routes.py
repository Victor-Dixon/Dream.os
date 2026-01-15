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




