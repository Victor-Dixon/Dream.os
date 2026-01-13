"""
Scheduler Handlers
==================

Handler classes for scheduler operations.
Wires scheduler to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.orchestrators.overnight.scheduler_refactored import TaskScheduler
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False


class SchedulerHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for scheduler operations."""

    def __init__(self):
        """Initialize scheduler handlers."""
        super().__init__("SchedulerHandlers")

    def handle_get_scheduler_status(self, request) -> tuple:
        """
        Handle request to get scheduler status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            SCHEDULER_AVAILABLE,
            "TaskScheduler"
        )
        if availability_error:
            return availability_error

        try:
            scheduler = TaskScheduler()
            status = scheduler.get_status()
            response = self.format_response(status, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "get_scheduler_status")
            return jsonify(error_response), 500

    def handle_schedule_task(self, request) -> tuple:
        """
        Handle request to schedule a task.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            SCHEDULER_AVAILABLE,
            "TaskScheduler"
        )
        if availability_error:
            return availability_error

        try:
            data = request.get_json() or {}
            task_data = data.get("task_data")

            if not task_data:
                error_response = self.format_response(None, success=False, error="task_data is required")
                return jsonify(error_response), 400

            scheduler = TaskScheduler()
            result = scheduler.schedule_task(task_data)
            response = self.format_response(result, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "schedule_task")
            return jsonify(error_response), 500




