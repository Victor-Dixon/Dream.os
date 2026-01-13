"""
Scheduler Routes
================

Flask routes for scheduler operations.
Wires scheduler to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.scheduler_handlers import SchedulerHandlers

# Create blueprint
scheduler_bp = Blueprint("scheduler", __name__, url_prefix="/api/scheduler")

# Create handler instance (BaseHandler pattern)
scheduler_handlers = SchedulerHandlers()


@scheduler_bp.route("/status", methods=["GET"])
def get_scheduler_status():
    """Get scheduler status."""
    return scheduler_handlers.handle_get_scheduler_status(request)


@scheduler_bp.route("/schedule", methods=["POST"])
def schedule_task():
    """Schedule a task."""
    return scheduler_handlers.handle_schedule_task(request)


@scheduler_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for scheduler services."""
    return jsonify({"status": "ok", "service": "scheduler"}), 200

