"""
Workflow Engine Handlers
========================

Handler classes for workflow engine operations.
Wires workflow engine to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.workflows.engine import WorkflowEngine
    WORKFLOW_ENGINE_AVAILABLE = True
except ImportError:
    WORKFLOW_ENGINE_AVAILABLE = False


class WorkflowHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for workflow engine operations."""

    def __init__(self):
        """Initialize workflow handlers."""
        super().__init__("WorkflowHandlers")

    def handle_execute_workflow(self, request) -> tuple:
        """
        Handle request to execute a workflow.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            WORKFLOW_ENGINE_AVAILABLE,
            "WorkflowEngine"
        )
        if availability_error:
            return availability_error

        try:
            data = request.get_json() or {}
            workflow_config = data.get("workflow_config")

            if not workflow_config:
                error_response = self.format_response(None, success=False, error="workflow_config is required")
                return jsonify(error_response), 400

            engine = WorkflowEngine()
            result = engine.execute_workflow(workflow_config)
            response = self.format_response(result, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "execute_workflow")
            return jsonify(error_response), 500

    def handle_get_workflow_status(self, request, workflow_id: str) -> tuple:
        """
        Handle request to get workflow status.

        Args:
            request: Flask request object
            workflow_id: Workflow identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            WORKFLOW_ENGINE_AVAILABLE,
            "WorkflowEngine"
        )
        if availability_error:
            return availability_error

        try:
            engine = WorkflowEngine()
            status = engine.get_workflow_status(workflow_id)

            if not status:
                error_response = self.format_response(None, success=False, error="Workflow not found")
                return jsonify(error_response), 404

            response = self.format_response(status, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "get_workflow_status")
            return jsonify(error_response), 500




