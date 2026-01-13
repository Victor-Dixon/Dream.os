"""
Task Handler - V2 Compliant Module
===================================

Handles task system commands for messaging CLI.
Implements --get-next-task, --list-tasks, --task-status, --complete-task.

V2 Compliance: < 300 lines, single responsibility
Migrated to UnifiedHandler for consolidated initialization and error handling.

<!-- SSOT Domain: integration -->

Author: Agent-1 (Integration & Core Systems Specialist)
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from ...core.base.common_command_base import CommonHandlerBase

logger = logging.getLogger(__name__)


class TaskHandler(CommonHandlerBase):
    """Handles task system commands for messaging CLI."""

    def __init__(self):
        """Initialize task handler."""
        super().__init__("TaskHandler")  # Uses CommonHandlerBase for standardized initialization
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists for task database."""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            hasattr(args, "get_next_task")
            and args.get_next_task
            or hasattr(args, "list_tasks")
            and args.list_tasks
            or hasattr(args, "task_status")
            and args.task_status
            or hasattr(args, "complete_task")
            and args.complete_task
        )

    def handle(self, args) -> dict:
        """Handle task system commands."""
        # Determine command type for tracking
        command_type = self._get_command_type(args)

        # Use unified tracking and error handling
        result = self.execute_with_tracking(command_type, args)
        return result

    async def _execute_command(self, command: str, args) -> dict:
        """Execute the actual command logic (required by UnifiedHandler)."""
        # Individual handlers now return dict results for consistency
        # Enhanced error handling with categorization and recovery suggestions
        try:
            # Import lightweight task repository (avoids heavy infrastructure dependencies)
            from ..helpers.task_repo_loader import SimpleTaskRepository

            # Initialize repository with error handling
            try:
                repo = SimpleTaskRepository()
            except Exception as repo_error:
                logger.error(f"Failed to initialize task repository: {repo_error}")
                return self._create_error_result(
                    command,
                    "repository_initialization_failed",
                    str(repo_error),
                    "Check database connectivity and task repository configuration"
                )

            # Get current agent ID (from args or environment)
            try:
                current_agent = self._get_current_agent(args)
            except Exception as agent_error:
                logger.error(f"Failed to determine agent ID: {agent_error}")
                return self._create_error_result(
                    command,
                    "agent_identification_failed",
                    str(agent_error),
                    "Set AGENT_ID environment variable or pass --agent flag"
                )

            # Route to appropriate handler (now returns dict results)
            try:
                if command == "get_next_task":
                    result = self._handle_get_next_task_sync(args, repo, current_agent)
                elif command == "list_tasks":
                    result = self._handle_list_tasks_sync(args, repo)
                elif command == "task_status":
                    result = self._handle_task_status_sync(args, repo)
                elif command == "complete_task":
                    result = self._handle_complete_task_sync(args, repo, current_agent)
                else:
                    return self._create_error_result(
                        command,
                        "unknown_command",
                        f"Unknown command: {command}",
                        f"Supported commands: get_next_task, list_tasks, task_status, complete_task"
                    )
            except ValueError as validation_error:
                logger.error(f"Validation error in {command}: {validation_error}")
                return self._create_error_result(
                    command,
                    "validation_error",
                    str(validation_error),
                    "Check command arguments and parameters"
                )
            except PermissionError as permission_error:
                logger.error(f"Permission error in {command}: {permission_error}")
                return self._create_error_result(
                    command,
                    "permission_denied",
                    str(permission_error),
                    "Check agent permissions for task operations"
                )
            except ConnectionError as connection_error:
                logger.error(f"Connection error in {command}: {connection_error}")
                return self._create_error_result(
                    command,
                    "connection_failed",
                    str(connection_error),
                    "Check database and service connectivity"
                )
            except Exception as handler_error:
                logger.error(f"Handler error in {command}: {handler_error}")
                return self._create_error_result(
                    command,
                    "handler_execution_failed",
                    str(handler_error),
                    "Check handler implementation and dependencies"
                )

            # Ensure result includes command type
            result['command'] = command
            return result

        except Exception as e:
            logger.error(f"Unexpected error executing {command}: {e}")
            return self._create_error_result(
                command,
                "unexpected_error",
                str(e),
                "Contact system administrator - unexpected error occurred"
            )

    def _get_command_type(self, args) -> str:
        """Get command type string for tracking."""
        if hasattr(args, "get_next_task") and args.get_next_task:
            return "get_next_task"
        elif hasattr(args, "list_tasks") and args.list_tasks:
            return "list_tasks"
        elif hasattr(args, "task_status") and args.task_status:
            return "task_status"
        elif hasattr(args, "complete_task") and args.complete_task:
            return "complete_task"
        else:
            return "unknown"

    def _get_current_agent(self, args) -> str:
        """Get current agent ID from args or environment with validation."""
        # Check if --agent flag was passed
        if hasattr(args, "agent") and args.agent:
            agent_id = args.agent
        else:
            # Check environment variable
            agent_id = os.getenv("AGENT_ID")

        # Validate agent ID format
        if agent_id:
            # Basic validation - should start with "Agent-" and have a number
            if not (agent_id.startswith("Agent-") and len(agent_id) > 6):
                logger.warning(f"⚠️ Agent ID format may be invalid: {agent_id}")
            return agent_id

        # Default to Agent-1 for testing
        logger.warning("⚠️ No agent ID specified, using Agent-1 as default")
        return "Agent-1"

    def _validate_task_id(self, task_id: str) -> bool:
        """Validate task ID format.

        Args:
            task_id: Task ID to validate

        Returns:
            True if valid, False otherwise
        """
        if not task_id or not isinstance(task_id, str):
            return False

        # Task IDs should be non-empty strings, typically UUIDs or simple identifiers
        # For now, just check it's not empty and contains valid characters
        import re
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', task_id))

    def _handle_get_next_task_sync(self, args, repo, agent_id: str) -> dict:
        """Handle --get-next-task command."""
        logger.info(f"🎯 Getting next task for {agent_id}...")

        try:
            # First, try contract system with cycle planner integration
            try:
                from src.services.handlers.contract_handler import ContractHandler
                contract_handler = ContractHandler()
                if contract_handler.manager:
                    task_result = contract_handler.manager.get_next_task(agent_id)

                    if task_result and task_result.get("task"):
                        task = task_result["task"]
                        source = task_result.get("source", "contract_system")

                        logger.info(f"✅ Task found from {source}")
                        print("\n" + "=" * 60)
                        print("📋 TASK ASSIGNED")
                        print("=" * 60)
                        print(f"Title: {task.get('title', 'Unknown')}")
                        print(f"Description: {task.get('description', 'No description')}")
                        print(f"Priority: {task.get('priority', 'MEDIUM')}")
                        print(f"Source: {source}")
                        if task.get('task_id'):
                            print(f"Task ID: {task.get('task_id')}")
                        if task.get('estimated_time'):
                            print(f"Estimated Time: {task.get('estimated_time')}")
                        print("=" * 60)
                        print("\n🐝 WE. ARE. SWARM. ⚡⚡")
                        return {
                            'success': True,
                            'task_found': True,
                            'source': source,
                            'task': {
                                'title': task.get('title', 'Unknown'),
                                'description': task.get('description', 'No description'),
                                'priority': task.get('priority', 'MEDIUM'),
                                'task_id': task.get('task_id'),
                                'estimated_time': task.get('estimated_time')
                            }
                        }
            except Exception as e:
                logger.debug(f"Contract system check failed: {e}, trying task repository...")

            # Fall back to task repository
            pending_tasks = list(repo.get_pending(limit=1))

            if not pending_tasks:
                logger.info("ℹ️ No tasks available in queue")
                print("\n" + "=" * 60)
                print("📭 NO TASKS AVAILABLE")
                print("=" * 60)
                print("Status: Queue is empty")
                print("Action: Check back later or create new tasks")
                print("=" * 60 + "\n")
                self.exit_code = 0
                return {
                    'success': True,
                    'task_found': False,
                    'reason': 'no_tasks_available',
                    'message': 'Queue is empty'
                }

            # Get the highest priority task
            task = pending_tasks[0]

            # Claim the task by assigning it
            task.assign_to(agent_id)
            repo.save(task)

            # Display task details
            print("\n" + "=" * 60)
            print("🎯 TASK CLAIMED SUCCESSFULLY!")
            print("=" * 60)
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            if task.description:
                print(f"Description: {task.description}")
            print(f"Priority: {self._priority_name(task.priority)}")
            print(f"Assigned to: {agent_id}")
            print(f"Claimed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            print("\n💡 Use --complete-task <task-id> when finished")
            print("=" * 60 + "\n")

            logger.info(f"✅ Task {task.id} claimed by {agent_id}")
            self.exit_code = 0
            return {
                'success': True,
                'task_found': True,
                'task_claimed': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': self._priority_name(task.priority),
                    'assigned_to': agent_id,
                    'claimed_at': datetime.now().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"❌ Failed to get next task: {e}")
            self.exit_code = 1
            return {
                'success': False,
                'error': str(e),
                'agent_id': agent_id
            }

    def _handle_list_tasks_sync(self, args, repo) -> dict:
        """Handle --list-tasks command."""
        logger.info("📋 Listing all tasks...")

        try:
            tasks = list(repo.list_all(limit=100))

            if not tasks:
                print("\n📭 No tasks in system\n")
                self.exit_code = 0
                return {
                    'success': True,
                    'total_tasks': 0,
                    'message': 'No tasks in system'
                }

            # Categorize tasks
            pending = [t for t in tasks if t.is_pending]
            assigned = [t for t in tasks if t.is_assigned and not t.is_completed]
            completed = [t for t in tasks if t.is_completed]

            print("\n" + "=" * 60)
            print("📋 TASK LIST")
            print("=" * 60)
            print(
                f"Total: {len(tasks)} | Pending: {len(pending)} | "
                + f"Assigned: {len(assigned)} | Completed: {len(completed)}"
            )
            print("=" * 60 + "\n")

            if pending:
                print("🆕 PENDING TASKS:")
                for task in pending:
                    print(f"  [{task.id}] {task.title}")
                    print(f"    Priority: {self._priority_name(task.priority)}")
                    print()

            if assigned:
                print("🔄 ASSIGNED TASKS:")
                for task in assigned:
                    print(f"  [{task.id}] {task.title}")
                    print(f"    Assigned to: {task.assigned_agent_id}")
                    print(f"    Priority: {self._priority_name(task.priority)}")
                    print()

            if completed:
                print("✅ COMPLETED TASKS (recent 5):")
                for task in completed[:5]:
                    print(f"  [{task.id}] {task.title}")
                    print(f"    Completed by: {task.assigned_agent_id}")
                    print()

            print("=" * 60 + "\n")

            self.exit_code = 0
            return {
                'success': True,
                'total_tasks': len(tasks),
                'pending_count': len(pending),
                'assigned_count': len(assigned),
                'completed_count': len(completed),
                'pending_tasks': [{'id': t.id, 'title': t.title, 'priority': self._priority_name(t.priority)} for t in pending],
                'assigned_tasks': [{'id': t.id, 'title': t.title, 'assigned_to': t.assigned_agent_id, 'priority': self._priority_name(t.priority)} for t in assigned],
                'completed_tasks': [{'id': t.id, 'title': t.title, 'completed_by': t.assigned_agent_id} for t in completed[:5]]
            }

        except Exception as e:
            logger.error(f"❌ Failed to list tasks: {e}")
            self.exit_code = 1
            return {
                'success': False,
                'error': str(e),
                'operation': 'list_tasks'
            }

    def _handle_task_status_sync(self, args, repo) -> dict:
        """Handle --task-status command."""
        task_id = args.task_status
        logger.info(f"📊 Checking status of task {task_id}...")

        # Validate task ID format
        if not self._validate_task_id(task_id):
            logger.error(f"❌ Invalid task ID format: {task_id}")
            return self._create_error_result(
                "task_status",
                "invalid_task_id",
                f"Invalid task ID format: {task_id}",
                "Task IDs should contain only alphanumeric characters, hyphens, and underscores"
            )

        try:
            task = repo.get(task_id)

            if not task:
                logger.error(f"❌ Task {task_id} not found")
                self.exit_code = 1
                return self._create_error_result(
                    "task_status",
                    "task_not_found",
                    f'Task {task_id} not found',
                    "Verify the task ID is correct and the task exists"
                )

            # Display task status
            print("\n" + "=" * 60)
            print("📊 TASK STATUS")
            print("=" * 60)
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            if task.description:
                print(f"Description: {task.description}")
            print(f"Priority: {self._priority_name(task.priority)}")
            print(f"Status: {self._task_status(task)}")
            if task.assigned_agent_id:
                print(f"Assigned to: {task.assigned_agent_id}")
                print(f"Assigned at: {task.assigned_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.completed_at:
                print(f"Completed at: {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Created at: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60 + "\n")

            self.exit_code = 0
            return {
                'success': True,
                'task_id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': self._priority_name(task.priority),
                'status': self._task_status(task),
                'assigned_to': task.assigned_agent_id,
                'assigned_at': task.assigned_at.isoformat() if task.assigned_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'created_at': task.created_at.isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Failed to check task status: {e}")
            self.exit_code = 1
            return {
                'success': False,
                'error': str(e),
                'task_id': task_id,
                'operation': 'task_status'
            }

    def _handle_complete_task_sync(self, args, repo, agent_id: str) -> dict:
        """Handle --complete-task command."""
        task_id = args.complete_task
        logger.info(f"✅ Completing task {task_id}...")

        # Validate task ID format
        if not self._validate_task_id(task_id):
            logger.error(f"❌ Invalid task ID format: {task_id}")
            return self._create_error_result(
                "complete_task",
                "invalid_task_id",
                f"Invalid task ID format: {task_id}",
                "Task IDs should contain only alphanumeric characters, hyphens, and underscores"
            )

        try:
            task = repo.get(task_id)

            if not task:
                logger.error(f"❌ Task {task_id} not found")
                self.exit_code = 1
                return self._create_error_result(
                    "complete_task",
                    "task_not_found",
                    f'Task {task_id} not found',
                    "Verify the task ID is correct and the task exists"
                )

            # Verify task is assigned to this agent
            if task.assigned_agent_id != agent_id:
                logger.error(f"❌ Task {task_id} is not assigned to {agent_id}")
                logger.info(f"💡 Task is assigned to: {task.assigned_agent_id}")
                self.exit_code = 1
                return self._create_error_result(
                    "complete_task",
                    "task_not_assigned_to_agent",
                    f'Task {task_id} is not assigned to {agent_id}',
                    f"Task is assigned to {task.assigned_agent_id}. Only the assigned agent can complete it."
                )

            # Complete the task
            task.complete()
            repo.save(task)

            print("\n" + "=" * 60)
            print("✅ TASK COMPLETED!")
            print("=" * 60)
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Completed by: {agent_id}")
            print(f"Completed at: {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60 + "\n")

            result = {
                'success': True,
                'task_id': task.id,
                'title': task.title,
                'completed_by': agent_id,
                'completed_at': task.completed_at.isoformat()
            }

            # 🔗 INTEGRATION: Trigger Output Flywheel for completed tasks
            try:
                from systems.output_flywheel.integration.agent_session_hooks import end_of_session_hook

                # Determine session type based on task content
                task_content = f"{task.title} {task.description or ''}".lower()
                if any(keyword in task_content for keyword in ['trade', 'trading', 'market', 'stock', 'financial']):
                    session_type = "trade"
                elif any(keyword in task_content for keyword in ['game', 'gaming', 'aria', 'website', 'life']):
                    session_type = "life_aria"
                else:
                    session_type = "build"  # Default for code/development tasks

                # Trigger Output Flywheel
                artifacts = end_of_session_hook(
                    agent_id=agent_id,
                    session_type=session_type,
                    metadata={
                        "task_id": task_id,
                        "task_title": task.title,
                        "task_priority": self._priority_name(task.priority),
                        "completed_at": task.completed_at.isoformat(),
                        "duration_minutes": None,  # Could be calculated if task has start time
                    },
                    auto_trigger=True
                )

                if artifacts:
                    print(f"\n🔗 Output Flywheel Integration:")
                    generated_artifacts = artifacts.get('artifacts', {})
                    if generated_artifacts:
                        for artifact_type, artifact_path in generated_artifacts.items():
                            print(f"   📄 Generated {artifact_type}: {artifact_path}")
                        print(f"   ✅ Artifacts published to publication queue")
                        result['output_flywheel'] = {
                            'triggered': True,
                            'artifacts': generated_artifacts,
                            'session_type': session_type
                        }
                    else:
                        print(f"   ⚠️  No artifacts generated (may still be processing)")
                        result['output_flywheel'] = {
                            'triggered': True,
                            'artifacts': None,
                            'status': 'processing'
                        }
                else:
                    print(f"   ⚠️  Output Flywheel integration skipped (session may be in progress)")
                    result['output_flywheel'] = {
                        'triggered': False,
                        'reason': 'session_in_progress'
                    }

            except ImportError as e:
                logger.warning(f"⚠️ Output Flywheel not available: {e}")
                print(f"   💡 Output Flywheel integration requires systems/output_flywheel")
                result['output_flywheel'] = {
                    'triggered': False,
                    'error': str(e),
                    'reason': 'import_error'
                }
            except Exception as e:
                logger.error(f"❌ Output Flywheel integration failed: {e}")
                print(f"   ⚠️  Output Flywheel integration failed, but task completion succeeded")
                result['output_flywheel'] = {
                    'triggered': False,
                    'error': str(e),
                    'reason': 'integration_error'
                }

            logger.info(f"✅ Task {task_id} completed by {agent_id}")
            self.exit_code = 0
            return result

        except Exception as e:
            logger.error(f"❌ Failed to complete task: {e}")
            self.exit_code = 1
            return {
                'success': False,
                'error': str(e),
                'task_id': task_id,
                'agent_id': agent_id,
                'operation': 'complete_task'
            }

    def _priority_name(self, priority: int) -> str:
        """Convert priority number to name."""
        priority_names = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
        return priority_names.get(priority, "Unknown")

    def _task_status(self, task) -> str:
        """Get human-readable task status."""
        if task.is_completed:
            return "✅ Completed"
        elif task.is_assigned:
            return "🔄 In Progress"
        else:
            return "🆕 Pending"

    def _create_error_result(self, command: str, error_type: str, error_message: str,
                           recovery_suggestion: str) -> dict:
        """Create a standardized error result dict with categorization and recovery guidance.

        Args:
            command: The command that failed
            error_type: Categorized error type (e.g., 'validation_error', 'permission_denied')
            error_message: Detailed error message
            recovery_suggestion: User-friendly recovery guidance

        Returns:
            Standardized error result dictionary
        """
        return {
            'success': False,
            'command': command,
            'error': {
                'type': error_type,
                'message': error_message,
                'recovery_suggestion': recovery_suggestion,
                'timestamp': datetime.now().isoformat()
            }
        }
