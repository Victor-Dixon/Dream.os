"""
Task Management Routes
=====================

Flask routes for task assignment and completion use cases.
Wires application layer use cases to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.application.use_cases.assign_task_uc import (
    AssignTaskRequest,
    AssignTaskUseCase,
)
from src.application.use_cases.complete_task_uc import (
    CompleteTaskRequest,
    CompleteTaskUseCase,
)
from src.web.task_handlers import TaskHandlers

# Create blueprint
task_bp = Blueprint("task", __name__, url_prefix="/api/tasks")

# Create handler instance (BaseHandler pattern)
task_handlers = TaskHandlers()


@task_bp.route("/assign", methods=["POST"])
def assign_task():
    """Assign a task to an agent."""
    return task_handlers.handle_assign_task(request)


@task_bp.route("/complete", methods=["POST"])
def complete_task():
    """Complete a task."""
    return task_handlers.handle_complete_task(request)


@task_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "task-management"})




