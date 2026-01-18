"""Contract Handler - V2 Compliant Module."""

import logging
from typing import Any

from ..unified_service_managers import UnifiedContractManager

logger = logging.getLogger(__name__)


class ContractHandler:
    """Handles contract-related commands for messaging CLI."""

    def __init__(self, manager: UnifiedContractManager | None = None) -> None:
        self.manager = manager or UnifiedContractManager()
        self._initialize_default_tasks()

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return bool(
            getattr(args, "get_next_task", False)
            or getattr(args, "check_contracts", False)
        )

    def handle(self, args) -> Any:
        """Handle the command."""
        return self.handle_contract_commands(args)

    def handle_contract_commands(self, args) -> Any:
        """Handle contract-related commands."""
        if getattr(args, "get_next_task", False):
            if not getattr(args, "agent", None):
                logger.error("Agent ID is required for --get-next-task")
                return None
            return self.get_next_task(args.agent)
        if getattr(args, "check_contracts", False):
            return self.check_contract_status()
        return None

    def get_next_task(self, agent_id: str) -> dict[str, Any] | None:
        """Get next available task for agent."""
        return self.manager.get_next_task(agent_id)

    def check_contract_status(self) -> dict[str, Any]:
        """Check overall contract status."""
        return self.manager.get_system_status()

    def assign_task(self, agent_id: str, task: dict[str, Any]) -> bool:
        """Assign task to agent."""
        task_id = task.get("task_id")
        if task_id:
            return self.manager.complete_task(task_id)
        return False

    def complete_task(self, task_id: str, completion_notes: str = "") -> bool:
        """Mark task as completed."""
        return self.manager.complete_task(task_id, completion_notes)

    def get_agent_tasks(self, agent_id: str) -> list[dict[str, Any]]:
        """Get tasks assigned to specific agent."""
        status = self.manager.get_agent_status(agent_id)
        return status.get("current_tasks", [])

    def get_contract_metrics(self) -> dict[str, Any]:
        """Get contract system metrics."""
        status = self.manager.get_system_status()
        return {
            "total_contracts": status.get("total_contracts", 0),
            "assigned_tasks": status.get("active_contracts", 0),
            "completed_tasks": status.get("completed_contracts", 0),
            "completion_rate": status.get("completion_rate", 0),
            "active_agents": len(status.get("agent_summaries", {})),
        }

    def reset_contracts(self) -> None:
        """Reset all contract data."""
        self.manager.create_default_tasks()
        self._initialize_default_tasks()

    def get_contract_status(self) -> dict[str, Any]:
        """Get contract handler status."""
        status = self.manager.get_system_status()
        return {
            "is_implemented": True,
            "contracts": status.get("total_contracts", 0),
            "assigned_tasks": status.get("active_contracts", 0),
            "completed_tasks": status.get("completed_contracts", 0),
        }

    def _initialize_default_tasks(self) -> None:
        """Initialize default tasks if none exist."""
        try:
            all_contracts = self.manager.storage.load_all_contracts()
            if not all_contracts:
                logger.info("🚀 Initializing contract system with default tasks...")
                self.manager.create_default_tasks()
                logger.info("✅ Contract system initialized successfully!")
        except Exception as exc:  # noqa: BLE001
            logger.info("❌ Error initializing default tasks: %s", exc)
