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

            # Convert Contract objects to dicts for status checking
            contracts_data = [c.to_dict() if hasattr(c, 'to_dict') else c.__dict__ if hasattr(c, '__dict__') else {} for c in contracts]
            
            status = {
                "total_contracts": len(contracts),
                "active_contracts": len([c for c in contracts_data if c.get("status") == "active"]),
                "completed_contracts": len(
                    [c for c in contracts_data if c.get("status") == "completed"]
                ),
                "pending_contracts": len([c for c in contracts_data if c.get("status") == "pending"]),
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

            # Convert Contract objects to dicts for status checking
            contracts_data = [c.to_dict() if hasattr(c, 'to_dict') else c.__dict__ if hasattr(c, '__dict__') else {} for c in agent_contracts]

            status = {
                "agent_id": agent_id,
                "total_contracts": len(agent_contracts),
                "active_contracts": len(
                    [c for c in contracts_data if c.get("status") == "active"]
                ),
                "completed_contracts": len(
                    [c for c in contracts_data if c.get("status") == "completed"]
                ),
                "contracts": contracts_data,
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
                # No contracts either – attempt to bootstrap from MASTER_TASK_LOG
                bootstrapped = self._bootstrap_tasks_from_master_log(agent_id)
                if bootstrapped:
                    # Try cycle planner again after seeding from MASTER_TASK_LOG
                    cycle_task = self.cycle_planner.get_next_cycle_task(agent_id)
                    if cycle_task:
                        logger.info(
                            f"✅ Bootstrapped cycle planner task for {agent_id} from MASTER_TASK_LOG: "
                            f"{cycle_task.get('title', 'Unknown')}"
                        )
                        task_id = cycle_task.get("task_id", "")
                        if task_id:
                            self._mark_cycle_task_active(agent_id, task_id)
                        return {
                            "agent_id": agent_id,
                            "task": cycle_task,
                            "status": "assigned",
                            "source": "cycle_planner_master_task_log",
                        }

                # Still nothing – notify captain so they can refill the queue
                self._notify_captain_no_tasks(agent_id)
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

    def _bootstrap_tasks_from_master_log(self, agent_id: str) -> bool:
        """
        Seed cycle planner tasks for an agent from MASTER_TASK_LOG.md.

        This gives the system a way to fall back to the global task log when
        both cycle planner and contract system are empty.
        """
        # Import lazily, but avoid package-name collisions between `src/tools` (package)
        # and repo-root `tools/` (scripts directory) by loading via file path.
        try:
            import importlib.util

            tool_path = self.cycle_planner.project_root / "tools" / "master_task_log_to_cycle_planner.py"
            if not tool_path.exists():
                logger.debug(f"master_task_log_to_cycle_planner not available at {tool_path}")
                return False

            spec = importlib.util.spec_from_file_location(
                "master_task_log_to_cycle_planner", tool_path
            )
            if spec is None or spec.loader is None:
                logger.debug("master_task_log_to_cycle_planner import spec unavailable")
                return False

            mtl2cp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mtl2cp)  # type: ignore[attr-defined]
        except Exception as e:  # pragma: no cover - defensive guard
            logger.debug(f"master_task_log_to_cycle_planner not available: {e}")
            return False

        try:
            # Avoid re-seeding multiple times per day for the same agent
            from datetime import date

            today = date.today().isoformat()
            agent_dir = self.cycle_planner.agent_workspaces_dir / agent_id
            task_file = agent_dir / f"cycle_planner_tasks_{today}.json"
            if task_file.exists():
                # File already exists; assume it has been seeded/used
                logger.debug(
                    f"Cycle planner file already exists for {agent_id} on {today}, "
                    f"skipping MASTER_TASK_LOG bootstrap."
                )
                return False

            # Parse tasks from MASTER_TASK_LOG.md
            parsed_tasks = mtl2cp.parse_master_task_log(mtl2cp.MASTER_TASK_LOG_PATH)
            # Prefer THIS_WEEK, then INBOX
            section_tasks = [t for t in parsed_tasks if t.section == "THIS_WEEK"]
            if not section_tasks:
                section_tasks = [t for t in parsed_tasks if t.section == "INBOX"]

            if not section_tasks:
                logger.debug("No tasks found in MASTER_TASK_LOG to bootstrap from.")
                return False

            payload = mtl2cp.build_cycle_planner_payload(
                agent_id=agent_id,
                tasks=section_tasks,
                priority="medium",
            )
            out_path = mtl2cp.write_cycle_planner_file(agent_id, payload)
            logger.info(
                f"✅ Seeded {payload.get('total_tasks', 0)} tasks for {agent_id} "
                f"from MASTER_TASK_LOG into {out_path}"
            )

            # Also create a gentle captain task for awareness (one per day)
            self._ensure_captain_refill_task(agent_id)

            return True
        except Exception as e:  # pragma: no cover - defensive guard
            logger.warning(f"⚠️ Failed to bootstrap tasks from MASTER_TASK_LOG: {e}")
            return False
    
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

    def _ensure_captain_refill_task(self, requesting_agent: str) -> None:
        """
        Ensure the captain has a cycle planner task to refill the master task log.

        This avoids situations where agents silently run out of work without
        the captain being nudged to add more tasks.
        """
        try:
            from datetime import date
            import json

            captain_id = "Agent-4"
            today = date.today().isoformat()
            agent_dir = self.cycle_planner.agent_workspaces_dir / captain_id
            agent_dir.mkdir(parents=True, exist_ok=True)
            task_file = agent_dir / f"cycle_planner_tasks_{today}.json"

            # If file exists, check if a refill task is already present
            data: Dict[str, Any] = {}
            if task_file.exists():
                try:
                    data = json.loads(task_file.read_text(encoding="utf-8"))
                except Exception:
                    data = {}

            tasks = data.get("tasks", [])
            if any(
                "MASTER_TASK_LOG" in (t.get("description") or "")
                for t in tasks
            ):
                return  # Refill task already exists

            refill_task = {
                "task_id": f"CAP-REFILL-{today}",
                "title": "Review and refill MASTER_TASK_LOG tasks",
                "description": (
                    f"Agent {requesting_agent} requested next task but none were available. "
                    "Review MASTER_TASK_LOG.md, add/prioritize tasks, and run the "
                    "MASTER_TASK_LOG → cycle planner bridge if needed."
                ),
                "priority": "high",
                "status": "pending",
                "assigned_to": captain_id,
                "category": "technical_debt",
                "estimated_points": 100,
                "created_from": "MASTER_TASK_LOG_AUTOMATION",
            }

            if not tasks:
                # Initialize new file structure
                data = {
                    "created": datetime.now().isoformat(),
                    "agent_id": captain_id,
                    "date": today,
                    "tasks": [refill_task],
                    "pending_tasks": [refill_task],
                    "total_tasks": 1,
                    "pending_count": 1,
                    "source": "master_task_log_to_cycle_planner",
                }
            else:
                tasks.append(refill_task)
                pending = data.get("pending_tasks", [])
                pending.append(refill_task)
                data["tasks"] = tasks
                data["pending_tasks"] = pending
                data["total_tasks"] = len(tasks)
                data["pending_count"] = len(pending)

            task_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(
                f"✅ Added captain refill task to cycle planner for {captain_id} "
                f"because {requesting_agent} had no tasks."
            )
        except Exception as e:  # pragma: no cover
            logger.debug(f"Failed to ensure captain refill task: {e}")

    def _notify_captain_no_tasks(self, agent_id: str) -> None:
        """
        Send an S2A-style message to the captain when an agent has no tasks.

        This is a backstop in addition to the captain's cycle planner task.
        """
        try:
            from src.core.messaging_core import (
                UnifiedMessagingCore,
                UnifiedMessagePriority,
                UnifiedMessageType,
                UnifiedMessageTag,
            )

            core = UnifiedMessagingCore()
            content = (
                f"[TECH-DEBT CAPTAIN ALERT] {agent_id} requested a next task, "
                "but no cycle planner or contract tasks were available.\n\n"
                "- MASTER_TASK_LOG automation attempted (seeded cycle planner from log if possible).\n"
                "- Please review MASTER_TASK_LOG.md, update priorities, and, if needed, "
                "run the master_task_log_to_cycle_planner bridge for specific agents."
            )
            core.send_message(
                content=content,
                sender="Agent-TECH-DEBT-CAPTAIN",
                recipient="Agent-4",
                message_type=UnifiedMessageType.S2A,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.SYSTEM],
                metadata={
                    "message_category": "s2a",
                    "channel": "standard",
                    "sender_role": "SYSTEM",
                    "receiver_role": "AGENT",
                },
            )
        except Exception as e:  # pragma: no cover
            logger.debug(f"Failed to notify captain about no-tasks state: {e}")

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
