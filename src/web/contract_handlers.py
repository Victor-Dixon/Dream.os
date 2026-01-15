"""
Contract Management Handlers
=============================

Handler classes for contract management operations.
Wires contract manager to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler (30% code reduction).
"""

from flask import jsonify, request

from src.core.base.base_handler import BaseHandler

from src.services.unified_service_managers import UnifiedContractManager



class ContractHandlers(BaseHandler):
    """Handler class for contract management operations."""

    def __init__(self):
        """Initialize contract handlers."""
        super().__init__("ContractHandlers")

    def handle_get_system_status(self, request) -> tuple:
        """
        Handle request to get system contract status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        try:

            manager = UnifiedContractManager()

            status = manager.get_system_status()

            if "error" in status:
                error_response = self.format_response(None, success=False, error=status["error"])
                return jsonify(error_response), 500

            response = self.format_response(status, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "get_system_status")
            return jsonify(error_response), 500

    def handle_get_agent_status(self, request, agent_id: str) -> tuple:
        """
        Handle request to get agent contract status.

        Args:
            request: Flask request object
            agent_id: Agent identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        try:

            manager = UnifiedContractManager()

            status = manager.get_agent_status(agent_id)

            if "error" in status:
                error_response = self.format_response(None, success=False, error=status["error"])
                return jsonify(error_response), 500

            response = self.format_response(status, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "get_agent_status")
            return jsonify(error_response), 500

    def handle_get_next_task(self, request) -> tuple:
        """
        Handle request to get next available task.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            data = request.get_json() or {}
            agent_id = data.get("agent_id")

            if not agent_id:
                error_response = self.format_response(None, success=False, error="agent_id is required")
                return jsonify(error_response), 400


            manager = UnifiedContractManager()

            task = manager.get_next_task(agent_id)

            if "error" in task:
                error_response = self.format_response(None, success=False, error=task["error"])
                return jsonify(error_response), 400

            if not task:
                response = self.format_response(
                    None,
                    success=True
                )
                response["message"] = "No tasks available"
                return jsonify(response), 200

            response = self.format_response(task, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "get_next_task")
            return jsonify(error_response), 500




