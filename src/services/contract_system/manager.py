#!/usr/bin/env python3
"""
Contract Manager - Agent Cellphone V2
====================================

Manages contract operations and task assignments.
Migrated to BaseService for consolidated initialization and error handling.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any, Optional

from ...core.base.base_service import BaseService
from .cycle_planner_integration import CyclePlannerIntegration
from .models import Contract
from .storage import ContractStorage

logger = logging.getLogger(__name__)


class ContractManager(BaseService):
    """Manages contract operations and task assignments."""

    def __init__(self):
        """Initialize contract manager."""
        super().__init__("ContractManager")
        self.storage = ContractStorage()
        self.cycle_planner = CyclePlannerIntegration()

    def get_system_status(self) -> dict[str, Any]:
        """Get overall system contract status."""
        try:
            contracts = self.storage.get_all_contracts()

            status = {
                "total_contracts": len(contracts),
                "active_contracts": len([c for c in contracts if c.get("status") == "active"]),
                "completed_contracts": len(
                    [c for c in contracts if c.get("status") == "completed"]
                ),
                "pending_contracts": len([c for c in contracts if c.get("status") == "pending"]),
                "last_updated": datetime.now().isoformat(),
            }

            return status

        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}

    def get_agent_status(self, agent_id: str) -> dict[str, Any]:
        """Get contract status for specific agent."""
        try:
            agent_contracts = self.storage.get_agent_contracts(agent_id)

            status = {
                "agent_id": agent_id,
                "total_contracts": len(agent_contracts),
                "active_contracts": len(
                    [c for c in agent_contracts if c.get("status") == "active"]
                ),
                "completed_contracts": len(
                    [c for c in agent_contracts if c.get("status") == "completed"]
                ),
                "contracts": agent_contracts,
                "last_updated": datetime.now().isoformat(),
            }

            return status

        except Exception as e:
            self.logger.error(f"Error getting agent status for {agent_id}: {e}")
            return {"error": str(e), "agent_id": agent_id}

    def get_next_task(self, agent_id: str) -> dict[str, Any]:
        """
        Get next available task for agent.
        
        Checks cycle planner first, then falls back to contract system.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1", "Agent-2")
            
        Returns:
            Dictionary with task information and status
        """
        try:
            # First, check cycle planner for tasks
            cycle_task = self.cycle_planner.get_next_cycle_task(agent_id)
            
            if cycle_task:
                logger.info(
                    f"✅ Found cycle planner task for {agent_id}: {cycle_task.get('title', 'Unknown')}"
                )
                
                # Mark task as assigned in cycle planner
                task_id = cycle_task.get("task_id", "")
                if task_id:
                    # Update cycle planner file to mark as active
                    self._mark_cycle_task_active(agent_id, task_id)
                
                # Return in expected format
                return {
                    "agent_id": agent_id,
                    "task": cycle_task,
                    "status": "assigned",
                    "source": "cycle_planner",
                }
            
            # Fall back to contract system
            logger.debug(f"No cycle planner tasks found for {agent_id}, checking contracts...")
            all_contracts = self.storage.get_all_contracts()
            available_tasks = [c for c in all_contracts if c.get("status") == "pending"]

            if not available_tasks:
                return {
                    "agent_id": agent_id,
                    "task": None,
                    "message": "No available tasks",
                    "status": "no_tasks",
                }

            # Assign first available task with validation
            task_data = available_tasks[0]
            
            # Validate task has actionable content (only if tasks field exists and is explicitly empty)
            if "tasks" in task_data:
                tasks_list = task_data.get("tasks", [])
                if isinstance(tasks_list, list) and len(tasks_list) == 0:
                    logger.warning(
                        f"⚠️ Contract {task_data.get('contract_id', task_data.get('id', 'unknown'))} "
                        f"has empty tasks array. Skipping assignment to {agent_id}."
                    )
                    # Try next available task if any
                    if len(available_tasks) > 1:
                        task_data = available_tasks[1]
                        if "tasks" in task_data:
                            tasks_list = task_data.get("tasks", [])
                            if isinstance(tasks_list, list) and len(tasks_list) == 0:
                                logger.warning("⚠️ All available contracts have empty tasks arrays.")
                                return {
                                    "agent_id": agent_id,
                                    "task": None,
                                    "message": "No actionable tasks available (all contracts have empty task arrays)",
                                    "status": "no_tasks",
                                }
                    else:
                        return {
                            "agent_id": agent_id,
                            "task": None,
                            "message": "No actionable tasks available (contract has empty task array)",
                            "status": "no_tasks",
                        }
            
            task_data["assigned_to"] = agent_id
            task_data["status"] = "active"
            task_data["assigned_at"] = datetime.now().isoformat()

            # Convert dict to Contract object before saving
            try:
                contract = Contract.from_dict(task_data)
                self.storage.save_contract(contract)
            except Exception as e:
                logger.warning(f"Could not convert task dict to Contract: {e}")
                # If conversion fails, skip saving (data already in storage)

            return {
                "agent_id": agent_id,
                "task": task_data,
                "status": "assigned",
                "source": "contract_system",
            }

        except Exception as e:
            self.logger.error(f"Error getting next task for {agent_id}: {e}")
            return {"error": str(e), "agent_id": agent_id}
    
    def _mark_cycle_task_active(self, agent_id: str, task_id: str) -> bool:
        """
        Mark cycle planner task as active/assigned.
        
        Args:
            agent_id: Agent ID
            task_id: Task ID to mark active
            
        Returns:
            True if task was marked active
        """
        try:
            from datetime import date
            
            # Load cycle planner tasks
            tasks = self.cycle_planner.load_cycle_planner_tasks(agent_id)
            
            # Find and update task
            for task in tasks:
                if task.get("task_id") == task_id:
                    task["status"] = "active"
                    task["assigned_at"] = datetime.now().isoformat()
                    
                    # Save back to file
                    target_date = date.today()
                    date_str = target_date.isoformat()
                    agent_dir = self.cycle_planner.agent_workspaces_dir / agent_id
                    
                    patterns = [
                        f"cycle_planner_tasks_{date_str}.json",
                        f"{date_str}_{agent_id.lower()}_pending_tasks.json",
                    ]
                    
                    for pattern in patterns:
                        task_file = agent_dir / pattern
                        if task_file.exists():
                            import json
                            with open(task_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                            
                            # Update task in data structure
                            if "pending_tasks" in data:
                                for t in data["pending_tasks"]:
                                    if t.get("task_id") == task_id:
                                        t.update(task)
                                        break
                            elif "tasks" in data:
                                for t in data["tasks"]:
                                    if t.get("task_id") == task_id:
                                        t.update(task)
                                        break
                            
                            with open(task_file, "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            
                            logger.info(f"✅ Marked cycle planner task {task_id} as active")
                            return True
            
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to mark cycle task active: {e}")
            return False

    def add_task_to_contract(self, contract_id: str, task: dict[str, Any]) -> bool:
        """Add a task to an existing contract."""
        try:
            contract = self.storage.get_contract(contract_id)
            if not contract:
                return False

            if "tasks" not in contract:
                contract["tasks"] = []

            contract["tasks"].append(task)
            contract["last_updated"] = datetime.now().isoformat()

            return self.storage.save_contract(contract)

        except Exception as e:
            self.logger.error(f"Error adding task to contract {contract_id}: {e}")
            return False
