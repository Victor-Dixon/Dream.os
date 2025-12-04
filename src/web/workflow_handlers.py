"""
Workflow Engine Handlers
========================

Handler classes for workflow engine operations.
Wires workflow engine to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.workflows.engine import WorkflowEngine
    WORKFLOW_ENGINE_AVAILABLE = True
except ImportError:
    WORKFLOW_ENGINE_AVAILABLE = False


class WorkflowHandlers:
    """Handler class for workflow engine operations."""

    @staticmethod
    def handle_execute_workflow(request) -> tuple:
        """
        Handle request to execute a workflow.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not WORKFLOW_ENGINE_AVAILABLE:
            return jsonify({"success": False, "error": "WorkflowEngine not available"}), 503

        try:
            data = request.get_json() or {}
            workflow_config = data.get("workflow_config")

            if not workflow_config:
                return jsonify({"error": "workflow_config is required"}), 400

            engine = WorkflowEngine()
            result = engine.execute_workflow(workflow_config)

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_get_workflow_status(request, workflow_id: str) -> tuple:
        """
        Handle request to get workflow status.

        Args:
            request: Flask request object
            workflow_id: Workflow identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        if not WORKFLOW_ENGINE_AVAILABLE:
            return jsonify({"success": False, "error": "WorkflowEngine not available"}), 503

        try:
            engine = WorkflowEngine()
            status = engine.get_workflow_status(workflow_id)

            if not status:
                return jsonify({"success": False, "error": "Workflow not found"}), 404

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



