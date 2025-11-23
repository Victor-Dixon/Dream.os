"""
Captain Operations Tools - Extension
====================================

Additional Captain tools discovered in Session 2025-10-14.

New tools enable:
- Progress tracking automation
- Mission file generation
- Batch agent onboarding
- Swarm-wide status checking
- Quick agent activation

V2 Compliance: <400 lines
Author: Agent-4 (Captain) - Session 2025-10-14
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


class ProgressTrackerTool(IToolAdapter):
    """Auto-generate progress tracking report for all agents."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.track_progress",
            version="1.0.0",
            category="captain",
            summary="Generate comprehensive progress tracker for all agents",
            required_params=[],
            optional_params={"output_file": "agent_workspaces/Agent-4/AGENT_PROGRESS_TRACKER.md"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return True, []

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Generate progress tracker markdown."""
        try:
            output_file = params.get("output_file", "agent_workspaces/Agent-4/AGENT_PROGRESS_TRACKER.md")
            
            # Collect agent status
            agent_statuses = {}
            for agent_id in SWARM_AGENTS:
                status_file = Path(f"agent_workspaces/{agent_id}/status.json")
                if status_file.exists():
                    agent_statuses[agent_id] = json.loads(status_file.read_text())
                else:
                    agent_statuses[agent_id] = {"status": "unknown"}
            
            # Generate markdown
            content = f"# 🎯 Agent Progress Tracker\n\n"
            content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for agent_id in SWARM_AGENTS:
                status = agent_statuses.get(agent_id, {})
                content += f"## {agent_id}\n"
                content += f"**Status:** {status.get('status', 'unknown')}\n"
                content += f"**Last Updated:** {status.get('timestamp', 'N/A')}\n\n"
            
            # Write file
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            Path(output_file).write_text(content)
            
            return ToolResult(
                success=True,
                output={
                    "file": output_file,
                    "agents_tracked": len(SWARM_AGENTS),
                    "timestamp": datetime.now().isoformat(),
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            raise ToolExecutionError(f"Progress tracker failed: {e}")


class CreateMissionTool(IToolAdapter):
    """Create mission file for agent from template."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.create_mission",
            version="1.0.0",
            category="captain",
            summary="Generate mission file for agent from template",
            required_params=["agent_id", "mission_title", "mission_objective"],
            optional_params={
                "tools": [],
                "tasks": [],
                "value_range": "800-1,200pts",
                "complexity": "medium",
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        errors = []
        if "agent_id" not in params:
            errors.append("agent_id is required")
        if "mission_title" not in params:
            errors.append("mission_title is required")
        if "mission_objective" not in params:
            errors.append("mission_objective is required")
        return len(errors) == 0, errors

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Create mission file."""
        try:
            agent_id = params["agent_id"]
            title = params["mission_title"]
            objective = params["mission_objective"]
            tools = params.get("tools", [])
            tasks = params.get("tasks", [])
            value = params.get("value_range", "800-1,200pts")
            complexity = params.get("complexity", "medium")
            
            # Generate mission content
            content = f"# 🎯 MISSION: {title}\n\n"
            content += f"**Agent:** {agent_id}\n"
            content += f"**Estimated Value:** {value}\n"
            content += f"**Complexity:** {complexity}\n\n"
            content += f"## 📋 MISSION OBJECTIVE\n\n{objective}\n\n"
            
            if tools:
                content += f"## 🛠️ YOUR TOOLS ({len(tools)} tools)\n\n"
                for tool in tools:
                    content += f"- `{tool}`\n"
                content += "\n"
            
            if tasks:
                content += f"## 🎯 TASKS\n\n"
                for i, task in enumerate(tasks, 1):
                    content += f"{i}. {task}\n"
                content += "\n"
            
            content += f"## 🔥 ACTIVATION\n\n"
            content += f"1. CHECK INBOX ✅\n"
            content += f"2. CLEAN WORKSPACE\n"
            content += f"3. START NOW!\n\n"
            content += f"**🐝 WE. ARE. SWARM. ⚡**\n"
            
            # Write file
            mission_file = Path(f"agent_workspaces/{agent_id}/inbox/MISSION_{title.upper().replace(' ', '_')}.md")
            mission_file.parent.mkdir(parents=True, exist_ok=True)
            mission_file.write_text(content)
            
            return ToolResult(
                success=True,
                output={
                    "file": str(mission_file),
                    "agent": agent_id,
                    "title": title,
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            raise ToolExecutionError(f"Mission creation failed: {e}")


class BatchOnboardTool(IToolAdapter):
    """Onboard multiple agents at once."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.batch_onboard",
            version="1.0.0",
            category="captain",
            summary="Hard onboard multiple agents in batch",
            required_params=["agents"],
            optional_params={"roles": {}, "messages": {}},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        errors = []
        if "agents" not in params or not isinstance(params["agents"], list):
            errors.append("agents must be a list")
        return len(errors) == 0, errors

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Batch onboard agents."""
        try:
            agents = params["agents"]
            roles = params.get("roles", {})
            messages = params.get("messages", {})
            
            results = []
            for agent_id in agents:
                role = roles.get(agent_id, "Specialist")
                message = messages.get(agent_id, f"🔥 ACTIVATION! Role: {role}! Check inbox for mission!")
                
                # Run hard onboarding via CLI
                cmd = [
                    "python", "-m", "src.services.messaging_cli",
                    "--agent", agent_id,
                    "--hard-onboarding",
                    "--role", role,
                    "--message", message,
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                results.append({
                    "agent": agent_id,
                    "success": result.returncode == 0,
                    "role": role,
                })
            
            success_count = sum(1 for r in results if r["success"])
            
            return ToolResult(
                success=success_count == len(agents),
                output={
                    "total": len(agents),
                    "successful": success_count,
                    "failed": len(agents) - success_count,
                    "results": results,
                },
                exit_code=0 if success_count == len(agents) else 1,
                execution_time=0.0,
            )
        except Exception as e:
            raise ToolExecutionError(f"Batch onboarding failed: {e}")


class SwarmStatusTool(IToolAdapter):
    """Get comprehensive swarm status - all agents."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.swarm_status",
            version="1.0.0",
            category="captain",
            summary="Get comprehensive status of entire swarm",
            required_params=[],
            optional_params={"detailed": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return True, []

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Get swarm status."""
        try:
            detailed = params.get("detailed", True)
            
            statuses = {
                "active": [],
                "idle": [],
                "unknown": [],
            }
            
            agent_details = {}
            
            for agent_id in SWARM_AGENTS:
                status_file = Path(f"agent_workspaces/{agent_id}/status.json")
                
                if status_file.exists():
                    data = json.loads(status_file.read_text())
                    status = data.get("status", "unknown")
                    
                    if status == "active":
                        statuses["active"].append(agent_id)
                    elif status == "idle":
                        statuses["idle"].append(agent_id)
                    else:
                        statuses["unknown"].append(agent_id)
                    
                    if detailed:
                        agent_details[agent_id] = data
                else:
                    statuses["unknown"].append(agent_id)
                    if detailed:
                        agent_details[agent_id] = {"status": "no_status_file"}
            
            return ToolResult(
                success=True,
                output={
                    "summary": {
                        "total": len(SWARM_AGENTS),
                        "active": len(statuses["active"]),
                        "idle": len(statuses["idle"]),
                        "unknown": len(statuses["unknown"]),
                    },
                    "statuses": statuses,
                    "details": agent_details if detailed else {},
                    "timestamp": datetime.now().isoformat(),
                },
                exit_code=0,
                execution_time=0.0,
            )
        except Exception as e:
            raise ToolExecutionError(f"Swarm status check failed: {e}")


class ActivateAgentTool(IToolAdapter):
    """Combined gas delivery + mission assignment."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.activate_agent",
            version="1.0.0",
            category="captain",
            summary="Complete agent activation (gas + mission in one)",
            required_params=["agent_id", "message"],
            optional_params={"priority": "regular", "mission_file": None},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        errors = []
        if "agent_id" not in params:
            errors.append("agent_id is required")
        if "message" not in params:
            errors.append("message is required")
        return len(errors) == 0, errors

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Activate agent with gas delivery."""
        try:
            agent_id = params["agent_id"]
            message = params["message"]
            priority = params.get("priority", "regular")
            
            # Send gas via messaging CLI
            cmd = [
                "python", "-m", "src.services.messaging_cli",
                "--agent", agent_id,
                "--message", message,
                "--priority", priority,
                "--pyautogui",
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return ToolResult(
                success=result.returncode == 0,
                output={
                    "agent": agent_id,
                    "message_sent": result.returncode == 0,
                    "priority": priority,
                    "timestamp": datetime.now().isoformat(),
                },
                exit_code=result.returncode,
                execution_time=0.0,
            )
        except Exception as e:
            raise ToolExecutionError(f"Agent activation failed: {e}")


class SelfMessageTool(IToolAdapter):
    """Send self-message to Captain (Agent-4) as reminder."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.self_message",
            version="1.0.0",
            category="captain",
            summary="Send self-message to Captain (Agent-4) as reminder",
            required_params=["message"],
            optional_params={"priority": "regular"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        errors = []
        if "message" not in params:
            errors.append("message is required")
        return len(errors) == 0, errors

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Send self-message to Captain."""
        try:
            message = params["message"]
            priority = params.get("priority", "regular")

            # Send message to Agent-4 (Captain)
            cmd = [
                "python",
                "-m",
                "src.services.messaging_cli",
                "--agent",
                "Agent-4",
                "--message",
                f"[SELF-REMINDER] {message}",
                "--priority",
                priority,
                "--mode",
                "pyautogui",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            return ToolResult(
                success=result.returncode == 0,
                output={
                    "message_sent": result.returncode == 0,
                    "message": message,
                    "priority": priority,
                    "stdout": result.stdout,
                },
                exit_code=result.returncode,
                execution_time=0.0,
            )
        except Exception as e:
            logger.error(f"Error sending self-message: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.self_message")


class FindIdleAgentsTool(IToolAdapter):
    """Find agents that are idle or need new tasks."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.find_idle",
            version="1.0.0",
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
            version="1.0.0",
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


class MessageAllAgentsTool(IToolAdapter):
    """Send message to all swarm agents including Captain."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.message_all",
            version="1.0.0",
            category="captain",
            summary="Send message to all swarm agents",
            required_params=["message"],
            optional_params={
                "priority": "regular",
                "include_captain": True,
                "tags": [],
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        errors = []
        if "message" not in params:
            errors.append("message is required")
        return len(errors) == 0, errors

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Send message to all agents."""
        try:
            message = params["message"]
            priority = params.get("priority", "regular")
            include_captain = params.get("include_captain", True)
            tags = params.get("tags", [])

            agents_to_message = (
                SWARM_AGENTS if include_captain else [a for a in SWARM_AGENTS if a != "Agent-4"]
            )

            results = {}
            successful = 0
            failed = 0

            for agent_id in agents_to_message:
                cmd = [
                    "python",
                    "-m",
                    "src.services.messaging_cli",
                    "--agent",
                    agent_id,
                    "--message",
                    message,
                    "--priority",
                    priority,
                    "--mode",
                    "pyautogui",
                ]

                if tags:
                    cmd.extend(["--tags"] + tags)

                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    success = result.returncode == 0
                    results[agent_id] = {
                        "success": success,
                        "stdout": result.stdout,
                        "stderr": result.stderr if not success else None,
                    }

                    if success:
                        successful += 1
                    else:
                        failed += 1

                except Exception as e:
                    results[agent_id] = {"success": False, "error": str(e)}
                    failed += 1

            return ToolResult(
                success=successful > 0,
                output={
                    "total_agents": len(agents_to_message),
                    "successful": successful,
                    "failed": failed,
                    "results": results,
                    "message": message,
                    "priority": priority,
                },
                exit_code=0 if failed == 0 else 1,
                execution_time=0.0,
            )
        except Exception as e:
            logger.error(f"Error messaging all agents: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.message_all")


# Export all tools
__all__ = [
    "ProgressTrackerTool",
    "CreateMissionTool",
    "BatchOnboardTool",
    "SwarmStatusTool",
    "ActivateAgentTool",
    "SelfMessageTool",
    "FindIdleAgentsTool",
    "GasCheckTool",
    "MessageAllAgentsTool",
]

