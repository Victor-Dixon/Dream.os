#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Cycle Planner Integration - Contract System
===========================================

Integrates cycle planner tasks into the contract system.
Loads tasks from cycle planner JSON files and converts them to contract format.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CyclePlannerIntegration:
    """Integrates cycle planner tasks into contract system."""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize cycle planner integration.

        Args:
            project_root: Project root path (defaults to detecting from file location)
        """
        if project_root is None:
            # Detect project root from this file's location
            self.project_root = Path(__file__).parent.parent.parent.parent
        else:
            self.project_root = Path(project_root)

        self.agent_workspaces_dir = self.project_root / "agent_workspaces"

    def load_cycle_planner_tasks(
        self, agent_id: str, target_date: Optional[date] = None
    ) -> list[dict[str, Any]]:
        """
        Load pending tasks from cycle planner JSON file for agent.

        Args:
            agent_id: Agent ID (e.g., "Agent-1", "Agent-2")
            target_date: Target date (defaults to today)

        Returns:
            List of task dictionaries
        """
        if target_date is None:
            target_date = date.today()

        # Try multiple file name patterns
        date_str = target_date.isoformat()
        patterns = [
            f"cycle_planner_tasks_{date_str}.json",
            f"{date_str}_{agent_id.lower()}_pending_tasks.json",
        ]

        agent_dir = self.agent_workspaces_dir / agent_id

        for pattern in patterns:
            task_file = agent_dir / pattern
            if task_file.exists():
                try:
                    with open(task_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Handle different JSON structures
                    tasks = []
                    if "pending_tasks" in data:
                        tasks = data["pending_tasks"]
                    elif "tasks" in data:
                        # Filter for pending tasks
                        tasks = [
                            t
                            for t in data["tasks"]
                            if t.get("status", "").lower() in ["pending", "ready"]
                        ]
                    elif "high_priority_tasks" in data or "medium_priority_tasks" in data or "low_priority_tasks" in data:
                        # Agent-3 format: tasks organized by priority
                        all_tasks = []
                        for priority_key in ["high_priority_tasks", "medium_priority_tasks", "low_priority_tasks"]:
                            if priority_key in data:
                                for task in data[priority_key]:
                                    # Convert to standard format
                                    task["task_id"] = task.get("id", task.get("task_id", ""))
                                    task["status"] = "pending"  # All tasks in this format are pending
                                    all_tasks.append(task)
                        tasks = all_tasks
                    elif isinstance(data, list):
                        tasks = [
                            t
                            for t in data
                            if t.get("status", "").lower() in ["pending", "ready"]
                        ]

                    logger.info(
                        f"✅ Loaded {len(tasks)} cycle planner tasks for {agent_id}"
                    )
                    return tasks

                except Exception as e:
                    logger.warning(
                        f"⚠️ Failed to load cycle planner tasks from {task_file}: {e}"
                    )

        logger.debug(f"No cycle planner tasks found for {agent_id} on {date_str}")
        return []

    def convert_task_to_contract(self, task: dict[str, Any], agent_id: str) -> dict[str, Any]:
        """
        Convert cycle planner task to contract format.

        Args:
            task: Cycle planner task dictionary
            agent_id: Agent ID

        Returns:
            Contract dictionary
        """
        # Extract task fields
        task_id = task.get("task_id", f"cycle-{agent_id}-{datetime.now().timestamp()}")
        title = task.get("title", "Untitled Task")
        description = task.get("description", "")
        priority = task.get("priority", "MEDIUM").upper()
        status = task.get("status", "pending").lower()

        # Map priority to contract priority
        priority_map = {
            "HIGH": "high",
            "MEDIUM": "medium",
            "LOW": "low",
            "BLOCKED": "blocked",
            "URGENT": "urgent",
        }
        contract_priority = priority_map.get(priority, "medium")

        # Create contract dictionary
        contract = {
            "contract_id": f"cycle-{task_id}",
            "title": title,
            "description": description,
            "priority": contract_priority,
            "status": "pending" if status == "pending" else status,
            "agent_id": agent_id,
            "created_at": datetime.now().isoformat(),
            "source": "cycle_planner",
            "task_id": task_id,
            "estimated_time": task.get("estimated_time", ""),
            "dependencies": task.get("dependencies", []),
            "deliverables": task.get("deliverables", []),
            "blocker": task.get("blocker", ""),
            "owner": task.get("owner", agent_id),
        }

        return contract

    def get_next_cycle_task(
        self, agent_id: str, target_date: Optional[date] = None
    ) -> Optional[dict[str, Any]]:
        """
        Get next available task from cycle planner for agent.

        Args:
            agent_id: Agent ID
            target_date: Target date (defaults to today)

        Returns:
            Contract dictionary or None if no tasks available
        """
        tasks = self.load_cycle_planner_tasks(agent_id, target_date)

        if not tasks:
            return None

        # Find first pending task
        for task in tasks:
            status = task.get("status", "").lower()
            if status in ["pending", "ready"]:
                return self.convert_task_to_contract(task, agent_id)

        return None

    def mark_task_complete(
        self, agent_id: str, task_id: str, target_date: Optional[date] = None
    ) -> bool:
        """
        Mark cycle planner task as complete.

        Args:
            agent_id: Agent ID
            task_id: Task ID to mark complete
            target_date: Target date (defaults to today)

        Returns:
            True if task was marked complete
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.isoformat()
        patterns = [
            f"cycle_planner_tasks_{date_str}.json",
            f"{date_str}_{agent_id.lower()}_pending_tasks.json",
        ]

        agent_dir = self.agent_workspaces_dir / agent_id

        for pattern in patterns:
            task_file = agent_dir / pattern
            if task_file.exists():
                try:
                    with open(task_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Update task status
                    updated = False
                    if "pending_tasks" in data:
                        for task in data["pending_tasks"]:
                            if task.get("task_id") == task_id:
                                task["status"] = "completed"
                                task["completed_at"] = datetime.now().isoformat()
                                updated = True
                                break
                    elif "tasks" in data:
                        for task in data["tasks"]:
                            if task.get("task_id") == task_id:
                                task["status"] = "completed"
                                task["completed_at"] = datetime.now().isoformat()
                                updated = True
                                break

                    if updated:
                        with open(task_file, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        logger.info(f"✅ Marked task {task_id} complete in cycle planner")
                        return True

                except Exception as e:
                    logger.error(f"❌ Failed to mark task complete: {e}")

        return False


__all__ = ["CyclePlannerIntegration"]

