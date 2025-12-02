"""
Task Management Handlers
========================

Handler classes for task management operations.
Wires use cases to web layer with dependency injection.

V2 Compliance: < 300 lines, handler pattern.
"""

import json
from typing import Any, Dict

from flask import jsonify, request

from src.application.use_cases.assign_task_uc import (
    AssignTaskRequest,
    AssignTaskResponse,
    AssignTaskUseCase,
)
from src.application.use_cases.complete_task_uc import (
    CompleteTaskRequest,
    CompleteTaskResponse,
    CompleteTaskUseCase,
)
from src.domain.ports.agent_repository import AgentRepository
from src.domain.ports.logger import Logger
from src.domain.ports.message_bus import MessageBus
from src.domain.ports.task_repository import TaskRepository
from src.domain.services.assignment_service import AssignmentService
from src.infrastructure.dependency_injection import get_dependencies


class TaskHandlers:
    """Handler class for task management operations."""

    @staticmethod
    def _get_use_case_dependencies() -> Dict[str, Any]:
        """Get dependencies for use cases."""
        return get_dependencies()

    @staticmethod
    def handle_assign_task(request) -> tuple:
        """
        Handle task assignment request.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Parse request data
            data = request.get_json() or {}
            task_id = data.get("task_id")
            agent_id = data.get("agent_id")  # Optional for auto-assignment

            if not task_id:
                return jsonify({"error": "task_id is required"}), 400

            # Get dependencies
            deps = TaskHandlers._get_use_case_dependencies()
            task_repo: TaskRepository = deps["task_repository"]
            agent_repo: AgentRepository = deps["agent_repository"]
            message_bus: MessageBus = deps["message_bus"]
            logger: Logger = deps["logger"]
            assignment_service: AssignmentService = deps["assignment_service"]

            # Create use case
            use_case = AssignTaskUseCase(
                tasks=task_repo,
                agents=agent_repo,
                message_bus=message_bus,
                logger=logger,
                assignment_service=assignment_service,
            )

            # Execute use case
            uc_request = AssignTaskRequest(task_id=task_id, agent_id=agent_id)
            response: AssignTaskResponse = use_case.execute(uc_request)

            # Return response
            if response.success:
                return (
                    jsonify(
                        {
                            "success": True,
                            "task_id": str(response.task.id) if response.task else None,
                            "agent_id": str(response.agent.id) if response.agent else None,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"success": False, "error": response.error_message}), 400

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_complete_task(request) -> tuple:
        """
        Handle task completion request.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Parse request data
            data = request.get_json() or {}
            task_id = data.get("task_id")
            agent_id = data.get("agent_id")

            if not task_id or not agent_id:
                return (
                    jsonify({"error": "task_id and agent_id are required"}),
                    400,
                )

            # Get dependencies
            deps = TaskHandlers._get_use_case_dependencies()
            task_repo: TaskRepository = deps["task_repository"]
            agent_repo: AgentRepository = deps["agent_repository"]
            message_bus: MessageBus = deps["message_bus"]
            logger: Logger = deps["logger"]

            # Create use case
            use_case = CompleteTaskUseCase(
                tasks=task_repo,
                agents=agent_repo,
                message_bus=message_bus,
                logger=logger,
            )

            # Execute use case
            uc_request = CompleteTaskRequest(task_id=task_id, agent_id=agent_id)
            response: CompleteTaskResponse = use_case.execute(uc_request)

            # Return response
            if response.success:
                return (
                    jsonify(
                        {
                            "success": True,
                            "task_id": str(response.task.id) if response.task else None,
                            "agent_id": str(response.agent.id) if response.agent else None,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"success": False, "error": response.error_message}), 400

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

