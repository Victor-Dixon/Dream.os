"""
Captain Operations Tools V2
===========================

Consolidated operations tool adapters for Captain operations: multi-agent coordination,
ROI optimization, status dashboards, and messaging tools.

PHASE 4 CONSOLIDATION: Combined coordination and messaging tools
Reduced from 2 files (500+ lines, 5 classes) to 1 consolidated file

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


class MultiFuelDelivery(IToolAdapter):
    """Send fuel (gas) to multiple agents at once."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.multi_fuel",
            version="2.0.0",
            category="captain",
            summary="Send activation messages to multiple agents at once",
            required_params=["agent_ids", "message"],
            optional_params={"priority": "regular", "use_pyautogui": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute multi-agent fuel delivery."""
        try:
            agent_ids = params["agent_ids"]
            message = params["message"]
            priority = params.get("priority", "regular")
            use_pyautogui = params.get("use_pyautogui", True)

            delivery_results = {}
            success_count = 0

            for agent_id in agent_ids:
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
                ]

                if use_pyautogui:
                    cmd.append("--pyautogui")

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

                delivery_results[agent_id] = {"success": result.returncode == 0}
                if result.returncode == 0:
                    success_count += 1

            return ToolResult(
                success=success_count > 0,
                output={
                    "agents_targeted": len(agent_ids),
                    "deliveries_successful": success_count,
                    "success_rate": (
                        round((success_count / len(agent_ids)) * 100, 2) if agent_ids else 0
                    ),
                    "delivery_results": delivery_results,
                },
                exit_code=0 if success_count == len(agent_ids) else 1,
            )
        except Exception as e:
            logger.error(f"Error delivering multi-agent fuel: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.multi_fuel")


class MarkovROIRunner(IToolAdapter):
    """Run Markov ROI optimizer and return optimal assignments."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.markov_roi",
            version="2.0.0",
            category="captain",
            summary="Execute Markov ROI optimizer for optimal task assignments",
            required_params=[],
            optional_params={"agent_count": 8},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute Markov ROI optimization."""
        try:
            result = subprocess.run(
                ["python", "tools/markov_8agent_roi_optimizer.py"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            markov_output = {"optimization_completed": result.returncode == 0}

            # Load results
            results_file = Path("agent_workspaces/Agent-4/8agent_roi_assignments.json")
            if results_file.exists():
                with open(results_file) as f:
                    assignments = json.load(f)
                    markov_output.update(
                        {
                            "total_agents": assignments.get("total_agents", 0),
                            "total_points": assignments.get("total_points", 0),
                            "avg_roi": assignments.get("avg_roi", 0),
                            "top_3_tasks": assignments.get("assignments", [])[:3],
                        }
                    )

            return ToolResult(
                success=result.returncode == 0, output=markov_output, exit_code=result.returncode
            )
        except Exception as e:
            logger.error(f"Error running Markov ROI: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.markov_roi")


class SwarmStatusDashboard(IToolAdapter):
    """Generate comprehensive swarm status dashboard."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.swarm_status",
            version="2.0.0",
            category="captain",
            summary="Generate swarm status overview",
            required_params=[],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute swarm dashboard generation."""
        try:
            dashboard = {"timestamp": datetime.now().isoformat(), "agents": {}, "active_count": 0}

            for agent_id in SWARM_AGENTS:
                workspace = Path(f"agent_workspaces/{agent_id}")
                if workspace.exists():
                    status_file = workspace / "status.json"
                    if status_file.exists():
                        status = json.loads(status_file.read_text())
                        dashboard["agents"][agent_id] = {
                            "status": status.get("status", "UNKNOWN"),
                            "mission": status.get("current_mission"),
                        }
                        if status.get("status") in ["ACTIVE", "EXECUTING"]:
                            dashboard["active_count"] += 1

            dashboard["swarm_health"] = "EXCELLENT" if dashboard["active_count"] >= 5 else "GOOD"
            return ToolResult(success=True, output=dashboard, exit_code=0)
        except Exception as e:
            raise ToolExecutionError(str(e), tool_name="captain.swarm_status")


class SelfMessageTool(IToolAdapter):
    """Send self-message to Captain (Agent-4) as reminder."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.self_message",
            version="2.0.0",
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


class MessageAllAgentsTool(IToolAdapter):
    """Send message to all swarm agents including Captain."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.message_all",
            version="2.0.0",
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
    "MultiFuelDelivery",
    "MarkovROIRunner",
    "SwarmStatusDashboard",
    "SelfMessageTool",
    "MessageAllAgentsTool",
]