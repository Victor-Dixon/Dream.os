"""
Coordination Handlers
=====================

Handler classes for coordination engine operations.
Wires coordination engines to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.core.coordination.swarm.engines.task_coordination_engine import TaskCoordinationEngine
    TASK_COORDINATION_AVAILABLE = True
except ImportError:
    TASK_COORDINATION_AVAILABLE = False


class CoordinationHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for coordination engine operations."""

    def __init__(self):
        """Initialize coordination handlers."""
        super().__init__("CoordinationHandlers")

    def handle_get_task_coordination_status(self, request) -> tuple:
        """
        Handle request to get task coordination status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_check = self.check_availability(TASK_COORDINATION_AVAILABLE, "TaskCoordinationEngine")
        if availability_check:
            return availability_check

        try:
            engine = TaskCoordinationEngine()
            status = engine.get_status()

            response_data = self.format_response(status, success=True)
            return jsonify(response_data), 200

        except Exception as e:
            error_response = self.handle_error(e, "handle_get_task_coordination_status")
            return jsonify(error_response), 500

    def handle_execute_task_coordination(self, request) -> tuple:
        """
        Handle request to execute task coordination.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_check = self.check_availability(TASK_COORDINATION_AVAILABLE, "TaskCoordinationEngine")
        if availability_check:
            return availability_check

        try:
            data = request.get_json() or {}
            task_data = data.get("task_data")

            if not task_data:
                error_response = self.format_response(None, success=False, error="task_data is required")
                return jsonify(error_response), 400

            engine = TaskCoordinationEngine()
            result = engine.coordinate_task(task_data)

            response_data = self.format_response(result, success=True)
            return jsonify(response_data), 200

        except Exception as e:
            error_response = self.handle_error(e, "handle_execute_task_coordination")
            return jsonify(error_response), 500

    def handle_coordinate_task(self, request) -> tuple:
        """
        Handle request to coordinate a specific task.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_check = self.check_availability(TASK_COORDINATION_AVAILABLE, "TaskCoordinationEngine")
        if availability_check:
            return availability_check

        try:
            data = request.get_json() or {}
            task_id = data.get("task_id")
            coordination_data = data.get("coordination_data", {})
            
            if not task_id:
                error_response = self.format_response(None, success=False, error="task_id is required")
                return jsonify(error_response), 400
            
            engine = TaskCoordinationEngine()
            result = engine.coordinate_task(task_id, coordination_data)
            
            response_data = self.format_response(result, success=True)
            return jsonify(response_data), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_coordinate_task")
            return jsonify(error_response), 500

    def handle_resolve_coordination(self, request) -> tuple:
        """
        Handle request to resolve coordination conflicts.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_check = self.check_availability(TASK_COORDINATION_AVAILABLE, "TaskCoordinationEngine")
        if availability_check:
            return availability_check

        try:
            data = request.get_json() or {}
            conflict_id = data.get("conflict_id")
            resolution = data.get("resolution", {})
            
            if not conflict_id:
                error_response = self.format_response(None, success=False, error="conflict_id is required")
                return jsonify(error_response), 400
            
            engine = TaskCoordinationEngine()
            result = engine.resolve_conflict(conflict_id, resolution)
            
            response_data = self.format_response(result, success=True)
            return jsonify(response_data), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_resolve_coordination")
            return jsonify(error_response), 500



