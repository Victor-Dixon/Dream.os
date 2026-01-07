"""
Captain Utilities & Validation Tools V2
=========================================

Consolidated utility and validation tool adapters for Captain operations: idle detection,
gas checking, logging, help, and file validation.

PHASE 4 CONSOLIDATION: Combined captain_tools_utilities.py + captain_tools_validation.py
Reduced from 2 files (500+ lines, 7 classes) to 1 consolidated file

V2 Compliance: <600 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: tools -->
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolResult, ToolSpec
from ..adapters.error_types import ToolExecutionError

logger = logging.getLogger(__name__)

# Swarm agents list
SWARM_AGENTS = [f"Agent-{i}" for i in range(1, 9)]


class FindIdleAgentsTool(IToolAdapter):
    """Find agents that are idle or need new tasks."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.find_idle",
            version="2.0.0",
            category="captain",
            summary="Find agents that are idle or need new tasks",
            required_params=[],
            optional_params={"hours_threshold": 1},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Find idle agents."""
        try:
            hours_threshold = params.get("hours_threshold", 1)

            idle_agents = []
            active_agents = []

            for agent_id in SWARM_AGENTS:
                status_file = Path(f"agent_workspaces/{agent_id}/status.json")

                if not status_file.exists():
                    idle_agents.append(
                        {"agent": agent_id, "reason": "No status.json", "urgency": "HIGH"}
                    )
                    continue

                try:
                    with open(status_file) as f:
                        status = json.load(f)

                    current_task = status.get("current_task", "")
                    agent_status = status.get("status", "").lower()

                    # Check if idle
                    if not current_task or current_task == "None" or "idle" in agent_status:
                        idle_agents.append(
                            {
                                "agent": agent_id,
                                "reason": f"Status: {agent_status}, Task: {current_task}",
                                "urgency": "HIGH",
                            }
                        )
                    else:
                        active_agents.append(agent_id)

                except Exception as e:
                    idle_agents.append(
                        {"agent": agent_id, "reason": f"Error: {e}", "urgency": "MEDIUM"}
                    )

            return ToolResult(
                success=True,
                output={
                    "idle_agents": idle_agents,
                    "active_agents": active_agents,
                    "idle_count": len(idle_agents),
                    "active_count": len(active_agents),
                    "total_agents": len(SWARM_AGENTS),
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            logger.error(f"Error finding idle agents: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.find_idle")


class GasCheckTool(IToolAdapter):
    """Check when agents last received messages (GAS levels)."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.gas_check",
            version="2.0.0",
            category="captain",
            summary="Check when agents last received messages (GAS levels)",
            required_params=[],
            optional_params={"hours_threshold": 2},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Check agent gas levels."""
        try:
            hours_threshold = params.get("hours_threshold", 2)

            low_gas = []
            good_gas = []
            gas_levels = {}

            for agent_id in SWARM_AGENTS:
                inbox_path = Path(f"agent_workspaces/{agent_id}/inbox")

                if not inbox_path.exists():
                    low_gas.append(agent_id)
                    gas_levels[agent_id] = {"status": "NO_INBOX", "age_hours": None}
                    continue

                # Find most recent message
                message_files = list(inbox_path.glob("*.md")) + list(inbox_path.glob("*.txt"))

                if not message_files:
                    low_gas.append(agent_id)
                    gas_levels[agent_id] = {"status": "EMPTY_INBOX", "age_hours": None}
                    continue

                # Get most recent
                most_recent = max(message_files, key=lambda p: p.stat().st_mtime)
                modified_time = datetime.fromtimestamp(most_recent.st_mtime)
                age_hours = (datetime.now() - modified_time).total_seconds() / 3600

                gas_levels[agent_id] = {
                    "status": "GOOD" if age_hours <= hours_threshold else "LOW",
                    "age_hours": round(age_hours, 1),
                    "last_message": most_recent.name,
                }

                if age_hours > hours_threshold:
                    low_gas.append(agent_id)
                else:
                    good_gas.append(agent_id)

            return ToolResult(
                success=True,
                output={
                    "low_gas_agents": low_gas,
                    "good_gas_agents": good_gas,
                    "low_gas_count": len(low_gas),
                    "good_gas_count": len(good_gas),
                    "gas_levels": gas_levels,
                    "threshold_hours": hours_threshold,
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            logger.error(f"Error checking gas levels: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.gas_check")


class UpdateLogTool(IToolAdapter):
    """Update Captain's log with key events."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.update_log",
            version="2.0.0",
            category="captain",
            summary="Update Captain's log with key events",
            required_params=["cycle", "event"],
            optional_params={"points": 0, "agent": None},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        errors = []
        if "cycle" not in params:
            errors.append("cycle is required")
        if "event" not in params:
            errors.append("event is required")
        return len(errors) == 0, errors

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Update Captain's log."""
        try:
            cycle = params["cycle"]
            event = params["event"]
            points = params.get("points", 0)
            agent = params.get("agent")

            log_file = Path(f"agent_workspaces/Agent-4/CAPTAINS_LOG_CYCLE_{cycle:03d}.md")
            timestamp = datetime.now().strftime("%H:%M:%S")

            entry = f"\n## [{timestamp}] {event}\n"
            if agent:
                entry += f"**Agent**: {agent}\n"
            if points > 0:
                entry += f"**Points**: {points}\n"
            entry += f"**Logged**: {datetime.now().isoformat()}\n"

            if log_file.exists():
                with open(log_file, "a") as f:
                    f.write(entry)
            else:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                with open(log_file, "w") as f:
                    f.write(f"# 📓 CAPTAIN'S LOG - CYCLE {cycle:03d}\n")
                    f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n")
                    f.write("**Captain**: Agent-4\n\n")
                    f.write(entry)

            return ToolResult(
                success=True,
                output={
                    "log_file": str(log_file),
                    "cycle": cycle,
                    "event": event,
                    "entry": entry,
                    "created": not log_file.exists() or log_file.stat().st_size == len(entry),
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            logger.error(f"Error updating log: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.update_log")


class ToolbeltHelpTool(IToolAdapter):
    """Display Captain's toolbelt quick reference."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.toolbelt_help",
            version="2.0.0",
            category="captain",
            summary="Display Captain's toolbelt quick reference",
            required_params=[],
            optional_params={"category": None},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return True, []

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Display toolbelt help."""
        try:
            tools_info = {
                "Message All Agents": {
                    "tool": "msg.broadcast",
                    "when": "Need to activate all 8 agents at once",
                    "key": "Don't forget to include Agent-4 (Captain)!",
                },
                "Check Agent Status": {
                    "tool": "captain.status_check",
                    "when": "Want to see who's active vs idle",
                    "key": "Idle = needs tasks!",
                },
                "ROI Calculator": {
                    "tool": "captain.calculate_roi",
                    "when": "Need to calculate task ROI quickly",
                    "key": "ROI = (points + v2*100 + autonomy*200) / complexity",
                },
                "Update Log": {
                    "tool": "captain.update_log",
                    "when": "Captain needs to log an event",
                    "key": "Include cycle number and points earned",
                },
                "Gas Check": {
                    "tool": "captain.gas_check",
                    "when": "Need to see which agents need messages",
                    "key": "Low gas = agents need activation!",
                },
                "Find Idle Agents": {
                    "tool": "captain.find_idle",
                    "when": "Need to assign tasks to idle agents",
                    "key": "Idle agents are ready for work!",
                },
            }

            category = params.get("category")
            if category:
                filtered = {k: v for k, v in tools_info.items() if category.lower() in k.lower()}
                if not filtered:
                    return ToolResult(
                        success=False,
                        output={"error": f"No tools found for category '{category}'"},
                        exit_code=1,
                    )
                tools_info = filtered

            help_text = "# 🛠️ CAPTAIN'S TOOLBELT\n\n"
            help_text += f"**Total Tools**: {len(tools_info)}\n"
            help_text += "**Category**: " + (category if category else "All") + "\n\n"

            for tool_name, info in tools_info.items():
                help_text += f"## {tool_name}\n"
                help_text += f"**Tool**: `{info['tool']}`\n"
                help_text += f"**When**: {info['when']}\n"
                help_text += f"**Key**: {info['key']}\n\n"

            return ToolResult(
                success=True,
                output={
                    "tools_displayed": len(tools_info),
                    "category": category,
                    "help_text": help_text,
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            logger.error(f"Error displaying toolbelt help: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.toolbelt_help")


class FileExistenceValidator(IToolAdapter):
    """Validate file existence before task assignment (prevents phantom tasks)."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.validate_file_exists",
            version="2.0.0",
            category="captain",
            summary="Verify file exists before assigning as task (prevents phantom tasks)",
            required_params=["file_path"],
            optional_params={"check_size": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute file existence validation."""
        try:
            file_path = params["file_path"]
            check_size = params.get("check_size", True)

            file = Path(file_path)
            exists = file.exists()

            validation = {
                "file_path": file_path,
                "exists": exists,
                "is_phantom": not exists,
                "verdict": "VALID" if exists else "PHANTOM_TASK",
            }

            if exists and check_size:
                validation["size"] = file.stat().st_size
                validation["lines"] = len(
                    file.read_text(encoding="utf-8", errors="ignore").splitlines()
                )

            return ToolResult(success=True, output=validation, exit_code=0 if exists else 1)
        except Exception as e:
            logger.error(f"Error validating file existence: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.validate_file_exists")


class ProjectScanRunner(IToolAdapter):
    """Run fresh project scan to update violation data."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.run_project_scan",
            version="2.0.0",
            category="captain",
            summary="Execute fresh project scan to update violation data",
            required_params=[],
            optional_params={"output_file": "project_analysis.json"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute project scan."""
        try:
            output_file = params.get("output_file", "project_analysis.json")

            # Run the project scanner
            result = subprocess.run(
                ["python", "-m", "src.core.project_scanner"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    output={"error": result.stderr, "stdout": result.stdout},
                    exit_code=result.returncode,
                    error_message=f"Project scan failed: {result.stderr}",
                )

            # Check if output file was created
            output_path = Path(output_file)
            if output_path.exists():
                with open(output_path) as f:
                    scan_data = json.load(f)

                return ToolResult(
                    success=True,
                    output={
                        "scan_completed": True,
                        "output_file": str(output_path),
                        "files_scanned": len(scan_data),
                        "stdout": result.stdout,
                    },
                    exit_code=0,
                )
            else:
                return ToolResult(
                    success=False,
                    output={
                        "scan_completed": False,
                        "error": "Output file not created",
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    },
                    exit_code=1,
                    error_message="Project scan did not create output file",
                )
        except Exception as e:
            logger.error(f"Error running project scan: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.run_project_scan")


class PhantomTaskDetector(IToolAdapter):
    """Detect phantom tasks (files in task pool that don't exist)."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.detect_phantoms",
            version="2.0.0",
            category="captain",
            summary="Detect phantom tasks in project_analysis.json",
            required_params=[],
            optional_params={"analysis_file": "project_analysis.json"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute phantom detection."""
        try:
            analysis_file = Path(params.get("analysis_file", "project_analysis.json"))

            if not analysis_file.exists():
                return ToolResult(
                    success=False,
                    output={"error": "project_analysis.json not found"},
                    exit_code=1,
                    error_message="Analysis file does not exist",
                )

            with open(analysis_file) as f:
                data = json.load(f)

            phantom_tasks = []
            valid_tasks = []

            for file_path in data.keys():
                file = Path(file_path)
                if file.exists():
                    valid_tasks.append(file_path)
                else:
                    phantom_tasks.append(file_path)

            return ToolResult(
                success=True,
                output={
                    "total_files_in_analysis": len(data),
                    "valid_files": len(valid_tasks),
                    "phantom_files": len(phantom_tasks),
                    "phantom_list": phantom_tasks[:10],  # First 10 only
                    "phantom_percentage": (
                        round((len(phantom_tasks) / len(data)) * 100, 2) if data else 0
                    ),
                    "recommendation": (
                        "Run fresh project scan" if phantom_tasks else "Task pool is clean"
                    ),
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error detecting phantoms: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.detect_phantoms")


# Export all tools
__all__ = [
    "FindIdleAgentsTool",
    "GasCheckTool",
    "UpdateLogTool",
    "ToolbeltHelpTool",
    "FileExistenceValidator",
    "ProjectScanRunner",
    "PhantomTaskDetector",
]