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

# Create handler instance (BaseHandler pattern)
core_handlers = CoreHandlers()


@core_bp.route("/agent-lifecycle/<agent_id>/status", methods=["GET"])
def get_agent_status(agent_id: str):
    """Get agent lifecycle status."""
    return core_handlers.handle_get_agent_lifecycle_status(request, agent_id)


@core_bp.route("/agent-lifecycle/<agent_id>/start-cycle", methods=["POST"])
def start_agent_cycle(agent_id: str):
    """Start agent lifecycle cycle."""
    return core_handlers.handle_start_cycle(request, agent_id)


@core_bp.route("/message-queue/status", methods=["GET"])
def get_message_queue_status():
    """Get message queue status."""
    return core_handlers.handle_get_message_queue_status(request)


@core_bp.route("/message-queue/process", methods=["POST"])
def process_message_queue():
    """Process message queue entries."""
    return core_handlers.handle_process_message_queue(request)


@core_bp.route("/message-queue/queue-size", methods=["GET"])
def get_queue_size():
    """Get message queue size."""
    return core_handlers.handle_get_queue_size(request)


@core_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for core services."""
    return jsonify({"status": "ok", "service": "core_system"}), 200


@core_bp.route("/execution/status", methods=["GET"])
def get_execution_status():
    """Get execution manager status."""
    return core_handlers.handle_get_execution_status(request)


@core_bp.route("/service/status", methods=["GET"])
def get_service_status():
    """Get service manager status."""
    return core_handlers.handle_get_service_status(request)


@core_bp.route("/resource/status", methods=["GET"])
def get_resource_status():
    """Get resource manager status."""
    return core_handlers.handle_get_resource_status(request)


@core_bp.route("/recovery/status", methods=["GET"])
def get_recovery_status():
    """Get recovery manager status."""
    return core_handlers.handle_get_recovery_status(request)


@core_bp.route("/results/status", methods=["GET"])
def get_results_status():
    """Get results manager status."""
    return core_handlers.handle_get_results_status(request)


