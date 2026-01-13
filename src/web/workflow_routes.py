"""
Workflow Engine Routes
======================

Flask routes for workflow engine operations.
Wires workflow engine to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.workflow_handlers import WorkflowHandlers

# Create blueprint
workflow_bp = Blueprint("workflow", __name__, url_prefix="/api/workflows")

# Create handler instance (BaseHandler pattern)
workflow_handlers = WorkflowHandlers()


@workflow_bp.route("/execute", methods=["POST"])
def execute_workflow():
    """Execute a workflow."""
    return workflow_handlers.handle_execute_workflow(request)


@workflow_bp.route("/status/<workflow_id>", methods=["GET"])
def get_workflow_status(workflow_id: str):
    """Get workflow execution status."""
    return workflow_handlers.handle_get_workflow_status(request, workflow_id)


@workflow_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for workflow services."""
    return jsonify({"status": "ok", "service": "workflow_engine"}), 200




