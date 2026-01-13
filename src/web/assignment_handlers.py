"""
Assignment Service Handlers
===========================

Handler classes for assignment service operations.
Wires assignment service to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.base_handler import BaseHandler

try:
    from src.domain.services.assignment_service import AssignmentService
    from src.domain.ports.logger import Logger
    from src.infrastructure.dependency_injection import get_dependencies
    ASSIGNMENT_SERVICE_AVAILABLE = True
except ImportError:
    ASSIGNMENT_SERVICE_AVAILABLE = False


class AssignmentHandlers(BaseHandler):
    """Handler class for assignment service operations."""

    def __init__(self):
        """Initialize assignment handlers."""
        super().__init__("AssignmentHandlers")

    def _get_service(self) -> AssignmentService:
        """Get assignment service instance with dependencies."""
        deps = get_dependencies()
        logger: Logger = deps.get("logger")
        return AssignmentService(logger=logger)

    def handle_assign(self, request) -> tuple:
        """
        Handle request to assign task to best agent.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not ASSIGNMENT_SERVICE_AVAILABLE:
            return jsonify({"success": False, "error": "AssignmentService not available"}), 503

        try:
            data = request.get_json() or {}
            task_id = data.get("task_id")
            available_agents = data.get("available_agents", [])

            if not task_id:
                return jsonify({"success": False, "error": "task_id is required"}), 400

            # Get task and agents from repositories
            deps = get_dependencies()
            task_repo = deps.get("task_repository")
            agent_repo = deps.get("agent_repository")

            if not task_repo or not agent_repo:
                return jsonify({"success": False, "error": "Repositories not available"}), 503

            # Get task
            task = task_repo.get(task_id)
            if not task:
                return jsonify({"success": False, "error": f"Task {task_id} not found"}), 404

            # Get available agents
            agents = []
            if available_agents:
                for agent_id in available_agents:
                    agent = agent_repo.get(agent_id)
                    if agent:
                        agents.append(agent)
            else:
                # Get all active agents
                agents = list(agent_repo.list_all())

            # Get assignment service
            service = self._get_service()

            # Find best agent
            best_agent = service.find_best_agent_for_task(task, agents)

            if not best_agent:
                return jsonify({"success": False, "error": "No suitable agent found"}), 404

            return jsonify({
                "success": True,
                "task_id": str(task.id),
                "agent_id": str(best_agent.id),
                "message": f"Task {task_id} assigned to {best_agent.id}"
            }), 200

        except Exception as e:
            error_response = self.handle_error(e, context="assignment_handler")
            return jsonify(error_response), 500

    def handle_list(self, request) -> tuple:
        """
        Handle request to list all assignments.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not ASSIGNMENT_SERVICE_AVAILABLE:
            return jsonify({"success": False, "error": "AssignmentService not available"}), 503

        try:
            # Get all tasks with assignments
            deps = get_dependencies()
            task_repo = deps.get("task_repository")

            if not task_repo:
                return jsonify({"success": False, "error": "Task repository not available"}), 503

            tasks = list(task_repo.list_all())
            assignments = []

            for task in tasks:
                if task.is_assigned:
                    assignments.append({
                        "task_id": str(task.id),
                        "task_title": task.title,
                        "agent_id": task.assigned_agent_id,
                        "assigned_at": task.assigned_at.isoformat() if task.assigned_at else None,
                        "status": "in_progress" if not task.is_completed else "completed"
                    })

            response_data = self.format_response({
                "assignments": assignments,
                "total": len(assignments)
            }, success=True)
            return jsonify(response_data), 200

        except Exception as e:
            error_response = self.handle_error(e, "handle_list")
            return jsonify(error_response), 500

    def handle_get_status(self, request) -> tuple:
        """
        Handle request to get assignment service status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not ASSIGNMENT_SERVICE_AVAILABLE:
            return jsonify({"success": False, "error": "AssignmentService not available"}), 503

        try:
            # Get statistics
            deps = get_dependencies()
            task_repo = deps.get("task_repository")
            agent_repo = deps.get("agent_repository")

            if not task_repo or not agent_repo:
                return jsonify({"success": False, "error": "Repositories not available"}), 503

            tasks = list(task_repo.list_all())
            agents = list(agent_repo.list_all())

            assigned_tasks = [t for t in tasks if t.is_assigned and not t.is_completed]
            pending_tasks = [t for t in tasks if not t.is_assigned and not t.is_completed]
            completed_tasks = [t for t in tasks if t.is_completed]

            status = {
                "service": "assignment_service",
                "status": "operational",
                "total_tasks": len(tasks),
                "assigned_tasks": len(assigned_tasks),
                "pending_tasks": len(pending_tasks),
                "completed_tasks": len(completed_tasks),
                "total_agents": len(agents),
                "available_agents": len([a for a in agents if a.is_active])
            }

            response_data = self.format_response(status, success=True)
            return jsonify(response_data), 200

        except Exception as e:
            error_response = self.handle_error(e, "handle_get_status")
            return jsonify(error_response), 500



