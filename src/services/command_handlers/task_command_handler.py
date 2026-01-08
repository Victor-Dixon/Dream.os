#!/usr/bin/env python3
"""
Task Command Handler - V2 Compliance
=====================================

Handler for task-related CLI commands (--get-next-task, --list-tasks, --task-status, --complete-task).

PHASE 4 CONSOLIDATION: Migrated from handlers/task_handler.py
Consolidated task management operations with unified interface.

V2 Compliance: <400 lines, modular design
Author: Agent-7 (Modularization)
<!-- SSOT Domain: integration -->
"""

import logging
from typing import Any
from src.core.unified_service_base import UnifiedServiceBase

logger = logging.getLogger(__name__)


class TaskCommandHandler(UnifiedServiceBase):
    """Handler for task-related CLI commands (--get-next-task, --list-tasks, --task-status, --complete-task).

    PHASE 4 CONSOLIDATION: Migrated from handlers/task_handler.py
    Consolidated task management operations with unified interface.
    """

    def __init__(self):
        """Initialize task command handler."""
        super().__init__("TaskCommandHandler")
        self.task_manager = None
        self._init_task_manager()

    def _init_task_manager(self):
        """Initialize task manager with fallback."""
        try:
            from .unified_service_managers import UnifiedContractManager
            self.task_manager = UnifiedContractManager()
        except ImportError:
            logger.warning("UnifiedContractManager not available for task operations")
            self.task_manager = None

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (hasattr(args, 'get_next_task') and args.get_next_task) or \
               (hasattr(args, 'list_tasks') and args.list_tasks) or \
               (hasattr(args, 'task_status') and args.task_status) or \
               (hasattr(args, 'complete_task') and args.complete_task)

    def handle(self, args) -> bool:
        """Handle task-related commands."""
        try:
            if hasattr(args, 'get_next_task') and args.get_next_task:
                return self._handle_get_next_task(args)
            elif hasattr(args, 'list_tasks') and args.list_tasks:
                return self._handle_list_tasks(args)
            elif hasattr(args, 'task_status') and args.task_status:
                return self._handle_task_status(args)
            elif hasattr(args, 'complete_task') and args.complete_task:
                return self._handle_complete_task(args)
            return False
        except Exception as e:
            logger.error(f"Task command handling error: {e}")
            return False

    def _handle_get_next_task(self, args) -> bool:
        """Handle get next task command."""
        try:
            if not self.task_manager:
                print("❌ Task manager not available")
                return False

            agent_id = getattr(args, 'agent', None)
            if not agent_id:
                print("❌ Agent ID required for task assignment")
                return False

            task = self.task_manager.get_next_task(agent_id)
            if task:
                print(f"✅ Task assigned to {agent_id}:")
                print(f"   📋 {task.get('title', 'No title')}")
                print(f"   📝 {task.get('description', 'No description')}")
                if task.get('priority'):
                    print(f"   🔥 Priority: {priority}")
                return True
            else:
                print(f"ℹ️  No tasks available for {agent_id}")
                return True
        except Exception as e:
            logger.error(f"Get next task error: {e}")
            return False

    def _handle_list_tasks(self, args) -> bool:
        """Handle list tasks command."""
        try:
            if not self.task_manager:
                print("❌ Task manager not available")
                return False

            agent_id = getattr(args, 'agent', None)
            tasks = self.task_manager.list_tasks(agent_id) if agent_id else self.task_manager.list_all_tasks()

            if tasks:
                print(f"📋 Tasks ({len(tasks)}):")
                for i, task in enumerate(tasks, 1):
                    status = task.get('status', 'unknown')
                    priority = task.get('priority', 'normal')
                    print(f"   {i}. [{status.upper()}] {task.get('title', 'No title')}")
                    if priority != 'normal':
                        print(f"      🔥 Priority: {priority}")
            else:
                print("ℹ️  No tasks found")
            return True
        except Exception as e:
            logger.error(f"List tasks error: {e}")
            return False

    def _handle_task_status(self, args) -> bool:
        """Handle task status command."""
        try:
            if not self.task_manager:
                print("❌ Task manager not available")
                return False

            task_id = getattr(args, 'task_id', None)
            if not task_id:
                print("❌ Task ID required")
                return False

            status = self.task_manager.get_task_status(task_id)
            if status:
                print(f"📊 Task {task_id} Status:")
                print(f"   📋 Title: {status.get('title', 'Unknown')}")
                print(f"   🔄 Status: {status.get('status', 'unknown')}")
                print(f"   👤 Assigned to: {status.get('assigned_to', 'unassigned')}")
                if status.get('progress'):
                    print(f"   📈 Progress: {status['progress']}%")
                return True
            else:
                print(f"❌ Task {task_id} not found")
                return False
        except Exception as e:
            logger.error(f"Task status error: {e}")
            return False

    def _handle_complete_task(self, args) -> bool:
        """Handle complete task command."""
        try:
            if not self.task_manager:
                print("❌ Task manager not available")
                return False

            task_id = getattr(args, 'task_id', None)
            if not task_id:
                print("❌ Task ID required")
                return False

            success = self.task_manager.complete_task(task_id)
            if success:
                print(f"✅ Task {task_id} marked as completed")
                return True
            else:
                print(f"❌ Failed to complete task {task_id}")
                return False
        except Exception as e:
            logger.error(f"Complete task error: {e}")
            return False