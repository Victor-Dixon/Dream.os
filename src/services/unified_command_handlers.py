#!/usr/bin/env python3
"""
Unified Command Handlers V2 - Phase 4 Consolidation
====================================================

PHASE 4 CONSOLIDATION: Consolidated command handler modules
Merged from: handlers/command_handler.py, overnight_command_handler.py, role_command_handler.py
Reduced from 3 separate files (~500 lines) to 1 consolidated module

Consolidated command handlers for messaging CLI operations:
- MessageCommandHandler: Core messaging commands (coordinates, list_agents, send_message, etc.)
- OvernightCommandHandler: Autonomous overnight operations
- RoleCommandHandler: Role-based command operations

Features:
- Unified command processing interface
- Consolidated error handling and logging
- Single responsibility principle maintained
- V2 compliance and SSOT integration

V2 Compliance: <600 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: integration -->
"""

import logging
import time
from typing import Any
from ..core.base.base_service import BaseService

logger = logging.getLogger(__name__)

try:
    from .agent_registry import format_agent_list
    from .utils.agent_registry import list_agents as registry_list_agents
except ImportError:
    def format_agent_list(agents):
        return '\n'.join(f'• {agent}' for agent in agents)

    def registry_list_agents():
        return [f'Agent-{i}' for i in range(1, 9)]


class MessageCommandHandler(BaseService):
    """Handler for core messaging CLI commands (coordinates, list_agents, send_message, etc.).

    PHASE 4 CONSOLIDATION: Migrated from handlers/command_handler.py
    Handles all primary messaging operations with unified interface.
    """

    def __init__(self) -> None:
        """Initialize message command handler."""
        super().__init__("MessageCommandHandler")
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history: list[dict[str, Any]] = []

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return False  # Base handler doesn't handle anything specific

    async def process_command(self, command: str, args: dict[str, Any],
        coordinate_handler, message_handler, service) -> dict[str, Any]:
        """Process CLI command."""
        try:
            self.command_count += 1
            start_time = time.time()

            if command == 'coordinates':
                result = await self._handle_coordinates_command(coordinate_handler)
            elif command == 'list_agents':
                agents = registry_list_agents()
                formatted = format_agent_list(agents)
                count = formatted['data']['agent_count']
                logger.info(f'\n🤖 Available Agents ({count}):')
                for agent in formatted['data']['agents']:
                    logger.info(f'  - {agent}')
                result = formatted
            elif command == 'send_message':
                result = await self._handle_send_message_command(args, message_handler, service)
            elif command == 'bulk_message':
                result = await self._handle_bulk_message_command(args, message_handler, service)
            elif command == 'status':
                result = await self._handle_status_command()
            elif command == 'infra-health':
                result = await self._handle_infra_health_command(args)
            else:
                result = {'success': False, 'error': f'Unknown command: {command}'}

            execution_time = time.time() - start_time
            if result.get('success', False):
                self.successful_commands += 1
            else:
                self.failed_commands += 1

            self.command_history.append({
                'command': command,
                'args': args,
                'success': result.get('success', False),
                'execution_time': execution_time,
                'timestamp': time.time()
            })

            if len(self.command_history) > 100:
                self.command_history.pop(0)

            return result
        except Exception as e:
            self.failed_commands += 1
            self.logger.error(f'Error processing command {command}: {e}')
            return {'success': False, 'error': str(e)}

    async def _handle_coordinates_command(self, coordinate_handler) -> dict[str, Any]:
        """Handle coordinates command."""
        try:
            result = await coordinate_handler.load_coordinates_async()
            if result.get('success', False):
                coordinate_handler.print_coordinates_table(result['coordinates'])
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_send_message_command(self, args: dict[str, Any],
        message_handler, service) -> dict[str, Any]:
        """Handle send message command."""
        try:
            message_data = message_handler.create_message_data(
                recipient=args.get('recipient', ''),
                message=args.get('message', ''),
                sender=args.get('sender', 'Captain Agent-4'),
                message_type=args.get('message_type', 'text'),
                priority=args.get('priority', 'regular'),
                tags=args.get('tags', [])
            )
            return await message_handler.send_message_async(service, message_data)
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_bulk_message_command(self, args: dict[str, Any],
        message_handler, service) -> dict[str, Any]:
        """Handle bulk message command."""
        try:
            coordinate_handler = args.get('coordinate_handler')
            if not coordinate_handler:
                return {'success': False, 'error': 'Coordinate handler not provided'}

            coords_result = await coordinate_handler.load_coordinates_async()
            if not coords_result.get('success', False):
                return coords_result

            agents = list(coords_result['coordinates'].keys())
            results = []

            for agent in agents:
                message_data = message_handler.create_message_data(
                    recipient=agent,
                    message=args.get('message', ''),
                    sender=args.get('sender', 'Captain Agent-4'),
                    message_type=args.get('message_type', 'broadcast'),
                    priority=args.get('priority', 'regular'),
                    tags=args.get('tags', [])
                )
                result = await message_handler.send_message_async(service, message_data)
                results.append({'agent': agent, 'result': result})

            return {
                'success': True,
                'results': results,
                'total_agents': len(agents)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_status_command(self) -> dict[str, Any]:
        """Handle status command."""
        try:
            stats = self.get_command_statistics()
            logger.info('\n📊 Command Statistics:')
            logger.info(f"  Total Commands: {stats['total_commands']}")
            logger.info(f"  Successful: {stats['successful_commands']}")
            logger.info(f"  Failed: {stats['failed_commands']}")
            logger.info(f"  Success Rate: {stats['success_rate']:.1f}%")
            return {'success': True, 'statistics': stats}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_infra_health_command(self, args: dict[str, Any]) -> dict[str, Any]:
        """Handle infrastructure health command."""
        try:
            from ..infrastructure.infrastructure_health_monitor import InfrastructureHealthMonitor

            monitor = InfrastructureHealthMonitor(
                warning_threshold=args.get('warning_threshold', 85.0),
                critical_threshold=args.get('critical_threshold', 95.0)
            )

            result = monitor.perform_full_health_check()
            monitor.print_health_report(result)

            return {
                'success': True,
                'status': result.status,
                'message': result.message,
                'metrics': {
                    'disk_usage_percent': result.metrics.disk_usage_percent,
                    'disk_free_gb': result.metrics.disk_free_gb,
                    'memory_usage_percent': result.metrics.memory_usage_percent,
                    'cpu_usage_percent': result.metrics.cpu_usage_percent,
                    'browser_ready': result.metrics.browser_ready,
                },
                'recommendations': result.recommendations
            }
        except Exception as e:
            logger.error(f"Error in infra-health command: {e}")
            return {'success': False, 'error': str(e)}

    def get_command_statistics(self) -> dict[str, Any]:
        """Get command processing statistics."""
        total = self.command_count
        success_rate = (self.successful_commands / total * 100 if total > 0 else 0)
        return {
            'total_commands': total,
            'successful_commands': self.successful_commands,
            'failed_commands': self.failed_commands,
            'success_rate': success_rate,
            'recent_commands': (
                self.command_history[-10:] if len(self.command_history) > 10
                else self.command_history
            )
        }


class OvernightCommandHandler(BaseService):
    """Handles overnight autonomous operations.

    PHASE 4 CONSOLIDATION: Migrated from overnight_command_handler.py
    Manages autonomous operations during overnight periods.
    """

    def __init__(self):
        """Initialize overnight command handler."""
        super().__init__("OvernightCommandHandler")

    def can_handle(self, args: Any) -> bool:
        """Check if this handler can handle the given arguments."""
        return hasattr(args, 'overnight') and args.overnight

    def handle(self, args: Any) -> bool:
        """Handle overnight operations."""
        self.logger.info('🌙 Starting overnight autonomous work cycle...')
        self.logger.info('This feature is currently under development.')
        self.logger.info('Use messaging CLI commands for individual operations.')
        return True


class RoleCommandHandler(BaseService):
    """Handles role-related command operations.

    PHASE 4 CONSOLIDATION: Migrated from role_command_handler.py
    Manages role-based command processing and role switching.
    """

    def __init__(self):
        """Initialize role command handler."""
        super().__init__("RoleCommandHandler")

    def can_handle(self, args: Any) -> bool:
        """Check if this handler can handle the given arguments."""
        return hasattr(args, 'role_mode') and args.role_mode

    def handle(self, args: Any) -> bool:
        """Handle role operations."""
        self.logger.info(f'🎭 Setting role mode: {args.role_mode}')
        self.logger.info('Role management feature is currently under development.')
        self.logger.info('Use standard messaging CLI commands for communication.')
        return True


class TaskCommandHandler(BaseService):
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


class BatchMessageCommandHandler(BaseService):
    """Handler for batch message CLI commands (--batch-start, --batch-add, --batch-send, --batch-status, --batch-cancel).

    PHASE 4 CONSOLIDATION: Migrated from handlers/batch_message_handler.py
    Consolidated batch messaging operations with unified interface.
    """

    def __init__(self):
        """Initialize batch message command handler."""
        super().__init__("BatchMessageCommandHandler")
        self.batch_service = None
        self._init_batch_service()

    def _init_batch_service(self):
        """Initialize batch service with fallback."""
        try:
            from ..message_batching_service import MessageBatchingService
            self.batch_service = MessageBatchingService()
        except ImportError:
            logger.warning("MessageBatchingService not available for batch operations")
            self.batch_service = None

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (hasattr(args, 'batch_start') and args.batch_start) or \
               (hasattr(args, 'batch_add') and args.batch_add) or \
               (hasattr(args, 'batch_send') and args.batch_send) or \
               (hasattr(args, 'batch_status') and args.batch_status) or \
               (hasattr(args, 'batch_cancel') and args.batch_cancel) or \
               (hasattr(args, 'batch') and args.batch)

    def handle(self, args) -> bool:
        """Handle batch message commands."""
        try:
            if hasattr(args, 'batch_start') and args.batch_start:
                return self._handle_batch_start(args)
            elif hasattr(args, 'batch_add') and args.batch_add:
                return self._handle_batch_add(args)
            elif hasattr(args, 'batch_send') and args.batch_send:
                return self._handle_batch_send(args)
            elif hasattr(args, 'batch_status') and args.batch_status:
                return self._handle_batch_status(args)
            elif hasattr(args, 'batch_cancel') and args.batch_cancel:
                return self._handle_batch_cancel(args)
            elif hasattr(args, 'batch') and args.batch:
                return self._handle_batch_list(args)
            return False
        except Exception as e:
            logger.error(f"Batch message command handling error: {e}")
            return False

    def _handle_batch_start(self, args) -> bool:
        """Handle batch start command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = self.batch_service.start_batch()
            print(f"✅ Batch started with ID: {batch_id}")
            print("   Use --batch-add to add messages to this batch")
            return True
        except Exception as e:
            logger.error(f"Batch start error: {e}")
            return False

    def _handle_batch_add(self, args) -> bool:
        """Handle batch add command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            message = getattr(args, 'message', None)
            recipient = getattr(args, 'recipient', None)

            if not all([batch_id, message, recipient]):
                print("❌ Batch ID, message, and recipient required")
                return False

            success = self.batch_service.add_to_batch(batch_id, message, recipient)
            if success:
                print(f"✅ Message added to batch {batch_id}")
                return True
            else:
                print(f"❌ Failed to add message to batch {batch_id}")
                return False
        except Exception as e:
            logger.error(f"Batch add error: {e}")
            return False

    def _handle_batch_send(self, args) -> bool:
        """Handle batch send command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            if not batch_id:
                print("❌ Batch ID required")
                return False

            success = self.batch_service.send_batch(batch_id)
            if success:
                print(f"✅ Batch {batch_id} sent successfully")
                return True
            else:
                print(f"❌ Failed to send batch {batch_id}")
                return False
        except Exception as e:
            logger.error(f"Batch send error: {e}")
            return False

    def _handle_batch_status(self, args) -> bool:
        """Handle batch status command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            if batch_id:
                status = self.batch_service.get_batch_status(batch_id)
                if status:
                    print(f"📊 Batch {batch_id} Status:")
                    print(f"   🔄 Status: {status.get('status', 'unknown')}")
                    print(f"   📨 Messages: {status.get('message_count', 0)}")
                    print(f"   ✅ Sent: {status.get('sent_count', 0)}")
                    print(f"   ❌ Failed: {status.get('failed_count', 0)}")
                else:
                    print(f"❌ Batch {batch_id} not found")
                    return False
            else:
                # List all batches
                batches = self.batch_service.list_batches()
                if batches:
                    print(f"📋 Active Batches ({len(batches)}):")
                    for batch in batches:
                        print(f"   • {batch['id']}: {batch['status']} ({batch['message_count']} messages)")
                else:
                    print("ℹ️  No active batches")
            return True
        except Exception as e:
            logger.error(f"Batch status error: {e}")
            return False

    def _handle_batch_cancel(self, args) -> bool:
        """Handle batch cancel command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            if not batch_id:
                print("❌ Batch ID required")
                return False

            success = self.batch_service.cancel_batch(batch_id)
            if success:
                print(f"✅ Batch {batch_id} cancelled")
                return True
            else:
                print(f"❌ Failed to cancel batch {batch_id}")
                return False
        except Exception as e:
            logger.error(f"Batch cancel error: {e}")
            return False

    def _handle_batch_list(self, args) -> bool:
        """Handle batch list command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batches = self.batch_service.list_batches()
            if batches:
                print(f"📋 All Batches ({len(batches)}):")
                for batch in batches:
                    print(f"   • {batch['id']}: {batch['status']} ({batch['message_count']} messages)")
            else:
                print("ℹ️  No batches found")
            return True
        except Exception as e:
            logger.error(f"Batch list error: {e}")
            return False


# Backward compatibility aliases
CommandHandler = MessageCommandHandler

# Export all handlers
__all__ = [
    "MessageCommandHandler",
    "OvernightCommandHandler",
    "RoleCommandHandler",
    "TaskCommandHandler",
    "BatchMessageCommandHandler",
    "CommandHandler",  # Backward compatibility
]