import logging
logger = logging.getLogger(__name__)
"""
Contract Handler - V2 Compliant Module
=====================================

Handles contract-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.
Migrated to BaseService for consolidated initialization and error handling.

<!-- SSOT Domain: integration -->

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""
from typing import Any
<<<<<<< HEAD
from ...core.base.common_command_base import CommonHandlerBase
from ..unified_service_managers import UnifiedContractManager
from ..contract_system.storage import ContractStorage


class ContractHandler(CommonHandlerBase):
=======
from ...core.base.base_service import BaseService
from ..contract_system.manager import ContractManager
from ..contract_system.storage import ContractStorage


class ContractHandler(BaseService):
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    """Handles contract-related commands for messaging CLI.

    Manages contract operations like task assignment and status checking.
    """

    def can_handle(self, args) ->bool:
        """Check if this handler can handle the given arguments."""
        return hasattr(args, 'get_next_task'
            ) and args.get_next_task or hasattr(args, 'check_contracts'
            ) and args.check_contracts

<<<<<<< HEAD
    def handle(self, args) -> dict:
=======
    def handle(self, args) ->bool:
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        """Handle the command."""
        return self.handle_contract_commands(args)

    def __init__(self):
        """Initialize contract handler."""
<<<<<<< HEAD
        super().__init__("ContractHandler")  # Uses CommonHandlerBase for standardized initialization
        try:
            from ..unified_service_managers import UnifiedContractManager
            self.manager = UnifiedContractManager()
=======
        super().__init__("ContractHandler")
        try:
            from ..contract_system.manager import ContractManager
            self.manager = ContractManager()
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        except ImportError:
            self.manager = None
        self._initialize_default_tasks()

<<<<<<< HEAD
    def handle_contract_commands(self, args) -> dict:
=======
    def handle_contract_commands(self, args) ->bool:
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        """Handle contract-related commands."""
        try:
            if args.get_next_task:
                if not args.agent:
<<<<<<< HEAD
                    return {
                        'success': False,
                        'error': '--agent required for --get-next-task',
                        'command': 'get_next_task'
                    }
                task = self.manager.get_next_task(args.agent)
                if task:
                    return {
                        'success': True,
                        'command': 'get_next_task',
                        'agent': args.agent,
                        'task': task
                    }
                else:
                    return {
                        'success': True,
                        'command': 'get_next_task',
                        'agent': args.agent,
                        'task': None,
                        'message': 'No available tasks for this agent'
                    }
            if args.check_contracts:
                status = self.manager.get_system_status()
                return {
                    'success': True,
                    'command': 'check_contracts',
                    'status': status
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': getattr(args, 'command', 'unknown')
            }
        return {
            'success': False,
            'error': 'No valid command specified',
            'command': 'unknown'
        }
=======
                    logger.info('❌ Error: --agent required for --get-next-task'
                        )
                    return True
                logger.info(f'📋 Getting next task for {args.agent}...')
                task = self.manager.get_next_task(args.agent)
                if task:
                    logger.info(f"✅ Task assigned: {task['title']}")
                    logger.info(f"📝 Description: {task['description']}")
                    logger.info(f"🎯 Type: {task['task_type']}")
                    logger.info(f"⚡ Priority: {task['priority']}")
                    logger.info(f"⏱️ Duration: {task['estimated_duration']}")
                    logger.info(f"🆔 Task ID: {task['task_id']}")
                else:
                    logger.info('❌ No available tasks for this agent')
                return True
            if args.check_contracts:
                logger.info('📊 Contract Status:')
                logger.info('=' * 40)
                status = self.manager.get_system_status()
                logger.info(
                    f"📈 Total Contracts: {status.get('total_contracts', 0)}")
                logger.info(
                    f"🔄 Active Contracts: {status.get('active_contracts', 0)}")
                logger.info(
                    f"✅ Completed Contracts: {status.get('completed_contracts', 0)}"
                    )
                logger.info(f"📋 Total Tasks: {status.get('total_tasks', 0)}")
                logger.info(
                    f"✅ Completed Tasks: {status.get('completed_tasks', 0)}")
                logger.info(
                    f"📊 Completion Rate: {status.get('completion_rate', 0)}%")
                logger.info(f"🎯 Total Points: {status.get('total_points', 0)}")
                logger.info(
                    f"✅ Completed Points: {status.get('completed_points', 0)}")
                agent_summaries = status.get('agent_summaries', {})
                if agent_summaries:
                    logger.info('\n👥 Agent Status:')
                    logger.info('-' * 30)
                    for agent_id, summary in agent_summaries.items():
                        logger.info(
                            f"{agent_id}: {summary.get('completion_rate', 0)}% complete ({summary.get('completed_points', 0)}/{summary.get('total_points', 0)} pts)"
                            )
                return True
        except Exception as e:
            logger.info(f'❌ Error handling contract command: {e}')
            return False
        return False
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

    def get_next_task(self, agent_id: str) ->(dict[str, Any] | None):
        """Get next available task for agent."""
        return self.manager.get_next_task(agent_id)

    def check_contract_status(self) ->dict[str, Any]:
        """Check overall contract status."""
        return self.manager.get_system_status()

    def assign_task(self, agent_id: str, task: dict[str, Any]) ->bool:
        """Assign task to agent."""
        task_id = task.get('task_id')
        if task_id:
            return self.manager.complete_task(task_id)
        return False

    def complete_task(self, task_id: str, completion_notes: str='') ->bool:
        """Mark task as completed."""
        return self.manager.complete_task(task_id, completion_notes)

    def get_agent_tasks(self, agent_id: str) ->list[dict[str, Any]]:
        """Get tasks assigned to specific agent."""
        status = self.manager.get_agent_status(agent_id)
        return status.get('current_tasks', [])

    def get_contract_metrics(self) ->dict[str, Any]:
        """Get contract system metrics."""
        status = self.manager.get_system_status()
        return {'total_contracts': status.get('total_contracts', 0),
            'assigned_tasks': status.get('active_contracts', 0),
            'completed_tasks': status.get('completed_contracts', 0),
            'completion_rate': status.get('completion_rate', 0),
            'active_agents': len(status.get('agent_summaries', {}))}

    def reset_contracts(self):
        """Reset all contract data."""
        import os
        import shutil
        contracts_dir = 'agent_workspaces/contracts'
        if os.path.exists(contracts_dir):
            shutil.rmtree(contracts_dir)
        os.makedirs(contracts_dir, exist_ok=True)
        self.storage = ContractStorage()
<<<<<<< HEAD
        self.manager = UnifiedContractManager()
=======
        self.manager = ContractManager(self.storage)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        self._initialize_default_tasks()

    def get_contract_status(self) ->dict[str, Any]:
        """Get contract handler status."""
        status = self.manager.get_system_status()
        return {'is_implemented': True, 'contracts': status.get(
            'total_contracts', 0), 'assigned_tasks': status.get(
            'active_contracts', 0), 'completed_tasks': status.get(
            'completed_contracts', 0)}

    def _initialize_default_tasks(self):
        """Initialize default tasks if none exist."""
        try:
            if self.manager:
                all_contracts = self.manager.storage.load_all_contracts()
                if not all_contracts:
                    logger.info(
                        '🚀 Initializing contract system with default tasks...')
                    self.manager.create_default_tasks()
                    logger.info('✅ Contract system initialized successfully!')
        except Exception as e:
            logger.info(f'❌ Error initializing default tasks: {e}')
