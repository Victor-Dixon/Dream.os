"""
Coordination Handlers
=====================

Handler classes for coordination engine operations.
Wires coordination engines to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.core.coordination.swarm.engines.task_coordination_engine import TaskCoordinationEngine
    TASK_COORDINATION_AVAILABLE = True
except ImportError:
    TASK_COORDINATION_AVAILABLE = False


class CoordinationHandlers:
    """Handler class for coordination engine operations."""

    @staticmethod
    def handle_get_task_coordination_status(request) -> tuple:
        """
        Handle request to get task coordination status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not TASK_COORDINATION_AVAILABLE:
            return jsonify({"success": False, "error": "TaskCoordinationEngine not available"}), 503

        try:
            engine = TaskCoordinationEngine()
            status = engine.get_status()

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_execute_task_coordination(request) -> tuple:
        """
        Handle request to execute task coordination.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not TASK_COORDINATION_AVAILABLE:
            return jsonify({"success": False, "error": "TaskCoordinationEngine not available"}), 503

        try:
            data = request.get_json() or {}
            task_data = data.get("task_data")

            if not task_data:
                return jsonify({"error": "task_data is required"}), 400

            engine = TaskCoordinationEngine()
            result = engine.coordinate_task(task_data)

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_coordinate_task(request) -> tuple:
        """
        Handle request to coordinate a specific task.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        if not TASK_COORDINATION_AVAILABLE:
            return jsonify({"success": False, "error": "TaskCoordinationEngine not available"}), 503

        try:
            data = request.get_json() or {}
            task_id = data.get("task_id")
            coordination_data = data.get("coordination_data", {})
            
            if not task_id:
                return jsonify({"error": "task_id is required"}), 400
            
            engine = TaskCoordinationEngine()
            result = engine.coordinate_task(task_id, coordination_data)
            
            return jsonify({"success": True, "data": result}), 200
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_resolve_coordination(request) -> tuple:
        """
        Handle request to resolve coordination conflicts.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        if not TASK_COORDINATION_AVAILABLE:
            return jsonify({"success": False, "error": "TaskCoordinationEngine not available"}), 503

        try:
            data = request.get_json() or {}
            conflict_id = data.get("conflict_id")
            resolution = data.get("resolution", {})
            
            if not conflict_id:
                return jsonify({"error": "conflict_id is required"}), 400
            
            engine = TaskCoordinationEngine()
            result = engine.resolve_conflict(conflict_id, resolution)
            
            return jsonify({"success": True, "data": result}), 200
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



