"""
Contract Management Handlers
=============================

Handler classes for contract management operations.
Wires contract manager to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

from src.services.contract_system.manager import ContractManager


class ContractHandlers:
    """Handler class for contract management operations."""

    @staticmethod
    def handle_get_system_status(request) -> tuple:
        """
        Handle request to get system contract status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            manager = ContractManager()
            status = manager.get_system_status()

            if "error" in status:
                return jsonify({"success": False, "error": status["error"]}), 500

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_get_agent_status(request, agent_id: str) -> tuple:
        """
        Handle request to get agent contract status.

        Args:
            request: Flask request object
            agent_id: Agent identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            manager = ContractManager()
            status = manager.get_agent_status(agent_id)

            if "error" in status:
                return jsonify({"success": False, "error": status["error"]}), 500

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_get_next_task(request) -> tuple:
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
                return jsonify({"error": "agent_id is required"}), 400

            manager = ContractManager()
            task = manager.get_next_task(agent_id)

            if "error" in task:
                return jsonify({"success": False, "error": task["error"]}), 400

            if not task:
                return jsonify({"success": True, "data": None, "message": "No tasks available"}), 200

            return jsonify({"success": True, "data": task}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



