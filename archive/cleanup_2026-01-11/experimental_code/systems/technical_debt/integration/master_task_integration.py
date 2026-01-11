"""
Master Task Log Integration for Technical Debt
===============================================

Connects technical debt system to MASTER_TASK_LOG.md for task visibility and tracking.

Features:
- Automatic debt task population in master log
- Priority mapping and formatting
- Task status synchronization
- Progress tracking integration

<!-- SSOT Domain: integration -->
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from ..debt_tracker import TechnicalDebtTracker

logger = logging.getLogger(__name__)


class MasterTaskDebtIntegration:
    """
    Integrates technical debt system with MASTER_TASK_LOG.md.

    Automatically populates debt reduction tasks in the master task log
    with proper formatting, priorities, and tracking.
    """

    def __init__(self, debt_tracker: Optional[TechnicalDebtTracker] = None, master_log_path: Optional[Path] = None):
        """Initialize integration."""
        self.debt_tracker = debt_tracker or TechnicalDebtTracker()
        self.master_log_path = master_log_path or Path("MASTER_TASK_LOG.md")

    def sync_debt_tasks_to_master_log(self) -> Dict[str, Any]:
        """
        Sync pending debt tasks to MASTER_TASK_LOG.md.

        Returns:
            Sync results with tasks added, updated, and removed
        """
        try:
            # Read current master log
            master_content = self._read_master_log()

            # Get current debt tasks
            debt_tasks = self._generate_debt_tasks()

            # Find existing debt tasks in master log
            existing_debt_tasks = self._extract_existing_debt_tasks(master_content)

            # Determine tasks to add, update, remove
            tasks_to_add = self._find_tasks_to_add(debt_tasks, existing_debt_tasks)
            tasks_to_update = self._find_tasks_to_update(debt_tasks, existing_debt_tasks)
            tasks_to_remove = self._find_tasks_to_remove(debt_tasks, existing_debt_tasks)

            # Update master log
            updated_content = self._update_master_log_content(
                master_content, tasks_to_add, tasks_to_update, tasks_to_remove
            )

            # Write updated content
            self._write_master_log(updated_content)

            return {
                "status": "success",
                "tasks_added": len(tasks_to_add),
                "tasks_updated": len(tasks_to_update),
                "tasks_removed": len(tasks_to_remove),
                "total_debt_tasks": len(debt_tasks)
            }

        except Exception as e:
            logger.error(f"Failed to sync debt tasks to master log: {e}")
            return {"status": "error", "message": str(e)}

    def _read_master_log(self) -> str:
        """Read the current master task log."""
        if not self.master_log_path.exists():
            # Create basic structure if file doesn't exist
            return self._create_basic_master_log_structure()

        try:
            return self.master_log_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.warning(f"Failed to read master log, using empty content: {e}")
            return self._create_basic_master_log_structure()

    def _create_basic_master_log_structure(self) -> str:
        """Create basic master log structure."""
        return """# MASTER TASK LOG

> **📋 Task Management Protocols:**
> - **No Tasks Available?** → Follow [TASK_DISCOVERY_PROTOCOL.md](docs/TASK_DISCOVERY_PROTOCOL.md) to systematically find work opportunities
> - **Creating Captain-Level Task?** → Follow [CAPTAIN_LEVEL_TASK_PROTOCOL.md](docs/CAPTAIN_LEVEL_TASK_PROTOCOL.md) - Complete Pre-Creation Checklist first
> - **Cycle Planner Integration:** Tasks may be added to cycle planner (`src/core/resume_cycle_planner_integration.py`) for automatic agent assignment
> - **Contract System:** Use `python -m src.services.messaging_cli --get-next-task --agent Agent-X` to claim tasks from cycle planner
> - **Reinforcement Learning System:** See [POINT_SYSTEM_INTEGRATION.md](docs/POINT_SYSTEM_INTEGRATION.md) - Points serve as reinforcement signals for agent training. Tasks should include point values (e.g., `**HIGH** (150 pts): Task description`)

## 📥 INBOX

## 📋 ACTIVE TASKS

## ✅ COMPLETED TASKS
"""

    def _generate_debt_tasks(self) -> List[Dict[str, Any]]:
        """Generate formatted debt tasks for master log."""
        debt_data = self.debt_tracker.debt_data
        debt_tasks = []

        for category_name, category_data in debt_data.get("categories", {}).items():
            pending_items = category_data.get("pending", [])
            total_pending = len(pending_items)

            if total_pending > 0:
                # Create a summary task for the category
                task = {
                    "id": f"debt_{category_name}_{datetime.now().strftime('%Y%m%d')}",
                    "title": f"Technical Debt: {category_name.replace('_', ' ').title()} ({total_pending} items)",
                    "description": self._generate_task_description(category_name, pending_items),
                    "priority": self._map_debt_priority(category_name),
                    "points": self._calculate_task_points(category_name, total_pending),
                    "category": "technical_debt",
                    "subcategory": category_name,
                    "pending_count": total_pending,
                    "last_updated": debt_data.get("last_updated", "")
                }
                debt_tasks.append(task)

        return debt_tasks

    def _generate_task_description(self, category: str, pending_items: List[str]) -> str:
        """Generate detailed task description."""
        descriptions = {
            "file_deletion": "Remove identified unnecessary files to reduce codebase complexity and maintenance overhead.",
            "integration": "Integrate standalone systems and components into the unified architecture.",
            "implementation": "Complete partial implementations and fill functionality gaps.",
            "review": "Conduct code reviews and validation for quality assurance.",
            "output_flywheel": "Complete Output Flywheel system integration and automation.",
            "test_validation": "Add comprehensive test coverage and validation.",
            "todo_fixme": "Address TODO and FIXME comments throughout codebase."
        }

        base_desc = descriptions.get(category, f"Address technical debt in {category} category.")
        if len(pending_items) <= 3:
            item_list = "\n".join(f"- {item}" for item in pending_items[:3])
            return f"{base_desc}\n\nSpecific items:\n{item_list}"
        else:
            item_list = "\n".join(f"- {item}" for item in pending_items[:2])
            return f"{base_desc}\n\nSample items:\n{item_list}\n- ... and {len(pending_items) - 2} more items"

    def _map_debt_priority(self, category: str) -> str:
        """Map debt category to task priority."""
        priority_map = {
            "file_deletion": "LOW",
            "integration": "HIGH",
            "implementation": "MEDIUM",
            "review": "MEDIUM",
            "output_flywheel": "HIGH",
            "test_validation": "MEDIUM",
            "todo_fixme": "LOW"
        }
        return priority_map.get(category, "MEDIUM")

    def _calculate_task_points(self, category: str, pending_count: int) -> int:
        """Calculate point value for debt task."""
        base_points = {
            "file_deletion": 25,
            "integration": 150,
            "implementation": 100,
            "review": 75,
            "output_flywheel": 200,
            "test_validation": 100,
            "todo_fixme": 50
        }

        base = base_points.get(category, 75)
        # Scale points based on complexity/quantity
        scale_factor = min(pending_count / 5, 3.0)  # Max 3x multiplier
        return int(base * scale_factor)

    def _extract_existing_debt_tasks(self, content: str) -> List[Dict[str, Any]]:
        """Extract existing debt tasks from master log."""
        existing_tasks = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            if line.strip().startswith('- [ ]') and 'technical_debt' in line.lower():
                # Extract task information
                task_text = line.strip()[5:].strip()  # Remove '- [ ] '

                # Check if it's a debt task by looking for patterns
                if '**HIGH**' in task_text or '**MEDIUM**' in task_text or '**LOW**' in task_text:
                    task = self._parse_task_line(task_text)
                    if task:
                        existing_tasks.append(task)

        return existing_tasks

    def _parse_task_line(self, task_text: str) -> Optional[Dict[str, Any]]:
        """Parse a task line from master log."""
        try:
            # Extract priority and points
            if '**HIGH**' in task_text:
                priority = "HIGH"
                points_part = task_text.split('**HIGH**')[1].strip()
            elif '**MEDIUM**' in task_text:
                priority = "MEDIUM"
                points_part = task_text.split('**MEDIUM**')[1].strip()
            elif '**LOW**' in task_text:
                priority = "LOW"
                points_part = task_text.split('**LOW**')[1].strip()
            else:
                return None

            # Extract points
            if '(' in points_part and 'pts)' in points_part:
                points_str = points_part.split('(')[1].split('pts)')[0].strip()
                points = int(points_str)
                description = points_part.split('pts)')[1].strip()
            else:
                points = 0
                description = points_part

            return {
                "priority": priority,
                "points": points,
                "description": description,
                "raw_text": task_text
            }

        except Exception as e:
            logger.warning(f"Failed to parse task line: {task_text[:100]}... Error: {e}")
            return None

    def _find_tasks_to_add(self, debt_tasks: List[Dict[str, Any]], existing_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find debt tasks that need to be added to master log."""
        existing_descriptions = {task.get("description", "") for task in existing_tasks}
        return [task for task in debt_tasks if task.get("title") not in existing_descriptions]

    def _find_tasks_to_update(self, debt_tasks: List[Dict[str, Any]], existing_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find debt tasks that need to be updated in master log."""
        # For now, we'll update all existing debt tasks to ensure they have current information
        existing_descriptions = {task.get("description", "") for task in existing_tasks}
        return [task for task in debt_tasks if task.get("title") in existing_descriptions]

    def _find_tasks_to_remove(self, debt_tasks: List[Dict[str, Any]], existing_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find debt tasks that should be removed from master log (completed ones)."""
        current_titles = {task.get("title") for task in debt_tasks}
        return [task for task in existing_tasks if task.get("description") not in current_titles]

    def _update_master_log_content(self, content: str, tasks_to_add: List[Dict[str, Any]],
                                 tasks_to_update: List[Dict[str, Any]], tasks_to_remove: List[Dict[str, Any]]) -> str:
        """Update master log content with debt tasks."""
        lines = content.split('\n')

        # Find INBOX section
        inbox_start = -1
        for i, line in enumerate(lines):
            if "## 📥 INBOX" in line:
                inbox_start = i
                break

        if inbox_start == -1:
            logger.warning("Could not find INBOX section in master log")
            return content

        # Remove old debt tasks
        updated_lines = []
        for line in lines[:inbox_start + 1]:  # Keep header and INBOX marker
            updated_lines.append(line)

        # Add new debt tasks
        all_tasks = tasks_to_add + tasks_to_update
        for task in all_tasks:
            task_line = self._format_task_line(task)
            updated_lines.append(f"- [ ] {task_line}")

        # Add any remaining content after INBOX
        for line in lines[inbox_start + 1:]:
            # Skip old debt tasks
            if line.strip().startswith('- [ ]') and 'technical_debt' in line.lower():
                continue
            updated_lines.append(line)

        return '\n'.join(updated_lines)

    def _format_task_line(self, task: Dict[str, Any]) -> str:
        """Format a task as a master log line."""
        priority = task.get("priority", "MEDIUM")
        points = task.get("points", 50)
        title = task.get("title", "Unknown debt task")

        return f"**{priority}** ({points} pts): {title}"

    def _write_master_log(self, content: str) -> None:
        """Write updated content to master log file."""
        try:
            self.master_log_path.write_text(content, encoding='utf-8')
            logger.info(f"Updated master task log with debt tasks at {self.master_log_path}")
        except Exception as e:
            logger.error(f"Failed to write master log: {e}")
            raise

    def get_debt_task_summary(self) -> Dict[str, Any]:
        """Get summary of debt tasks for reporting."""
        debt_data = self.debt_tracker.debt_data
        categories = debt_data.get("categories", {})

        total_pending = sum(len(cat.get("pending", [])) for cat in categories.values())
        total_resolved = sum(cat.get("resolved", 0) for cat in categories.values())

        return {
            "total_pending_tasks": total_pending,
            "total_resolved_tasks": total_resolved,
            "categories": {
                name: {
                    "pending": len(data.get("pending", [])),
                    "resolved": data.get("resolved", 0)
                }
                for name, data in categories.items()
            },
            "last_updated": debt_data.get("last_updated", "")
        }