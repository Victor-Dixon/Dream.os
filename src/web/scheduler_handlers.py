"""
Scheduler Handlers
==================

Handler classes for scheduler operations.
Wires scheduler to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.orchestrators.overnight.scheduler_refactored import TaskScheduler
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False


class SchedulerHandlers:
    """Handler class for scheduler operations."""

    @staticmethod
    def handle_get_scheduler_status(request) -> tuple:
        """
        Handle request to get scheduler status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not SCHEDULER_AVAILABLE:
            return jsonify({"success": False, "error": "TaskScheduler not available"}), 503

        try:
            scheduler = TaskScheduler()
            status = scheduler.get_status()

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_schedule_task(request) -> tuple:
        """
        Handle request to schedule a task.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not SCHEDULER_AVAILABLE:
            return jsonify({"success": False, "error": "TaskScheduler not available"}), 503

        try:
            data = request.get_json() or {}
            task_data = data.get("task_data")

            if not task_data:
                return jsonify({"error": "task_data is required"}), 400

            scheduler = TaskScheduler()
            result = scheduler.schedule_task(task_data)

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



