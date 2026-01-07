"""
Captain Monitoring & Reporting Tools V2
========================================

Consolidated monitoring and reporting tool adapters for Captain operations: gas delivery,
leaderboard updates, cycle reporting, and morning briefings.

PHASE 4 CONSOLIDATION: Combined captain_tools_monitoring.py + MorningBriefingTool from captain_tools_coordination.py
Reduced from 2 files (400+ lines, 4 classes) to 1 consolidated file

V2 Compliance: <500 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: tools -->
"""

import json
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolResult, ToolSpec
from ..adapters.error_types import ToolExecutionError

logger = logging.getLogger(__name__)

# Swarm agents list
SWARM_AGENTS = [f"Agent-{i}" for i in range(1, 9)]


class GasDeliveryTool(IToolAdapter):
    """Send PyAutoGUI activation messages to agents ("Prompts Are Gas")."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.deliver_gas",
            version="2.0.0",
            category="captain",
            summary="Send PyAutoGUI activation message to agent",
            required_params=["agent_id", "message"],
            optional_params={"priority": "regular"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute gas delivery (PyAutoGUI message)."""
        try:
            agent_id = params["agent_id"]
            message = params["message"]
            priority = params.get("priority", "regular")

            # Use messaging_cli to send PyAutoGUI message
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
                "--pyautogui",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    output={"error": result.stderr},
                    exit_code=result.returncode,
                    error_message=f"Gas delivery failed: {result.stderr}",
                )

            return ToolResult(
                success=True,
                output={
                    "agent_id": agent_id,
                    "message_sent": True,
                    "delivery_method": "PyAutoGUI",
                    "gas_type": "activation",
                    "stdout": result.stdout,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error delivering gas: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.deliver_gas")


class LeaderboardUpdateTool(IToolAdapter):
    """
    Update agent leaderboard with new points, achievements, and session tracking.

    Consolidated from captain_tools.py and captain_coordination_tools.py (Agent-8 - 2025-01-27)
    Single source of truth for all leaderboard operations.
    """

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.update_leaderboard",
            version="2.0.0",
            category="captain",
            summary="Update agent leaderboard with points, achievements, and session tracking",
            required_params=[],
            optional_params={
                "updates": {},  # Dict: {agent_id: points} - batch update mode
                "agent_id": None,  # Single agent update mode
                "points": 0,  # Points to add (single agent mode)
                "achievement": None,  # Achievement name (optional)
                "session_date": None,  # Session date (defaults to today)
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        # Either batch mode (updates dict) or single agent mode (agent_id + points)
        has_batch = "updates" in params and params["updates"]
        has_single = "agent_id" in params and params["agent_id"] and "points" in params

        if not has_batch and not has_single:
            return (False, ["Either 'updates' dict or 'agent_id' + 'points' required"])

        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute leaderboard update."""
        try:
            session_date = params.get("session_date", datetime.now().strftime("%Y-%m-%d"))
            leaderboard_file = Path("runtime/leaderboard.json")
            leaderboard_file.parent.mkdir(parents=True, exist_ok=True)

            # Load existing leaderboard
            if leaderboard_file.exists():
                leaderboard = json.loads(leaderboard_file.read_text())
            else:
                leaderboard = {"version": "2.0.0", "last_updated": session_date, "agents": {}}

            updates_applied = 0

            # Batch update mode
            if "updates" in params and params["updates"]:
                updates = params["updates"]
                for agent_id, points in updates.items():
                    self._update_agent_entry(leaderboard, agent_id, points, session_date, None)
                    updates_applied += 1

            # Single agent update mode
            elif "agent_id" in params and params["agent_id"]:
                agent_id = params["agent_id"]
                points = params.get("points", 0)
                achievement = params.get("achievement")
                self._update_agent_entry(leaderboard, agent_id, points, session_date, achievement)
                updates_applied += 1

            # Sort by total points
            sorted_agents = sorted(
                leaderboard["agents"].items(), key=lambda x: x[1]["total_points"], reverse=True
            )

            leaderboard["last_updated"] = session_date
            leaderboard["ranking"] = [agent_id for agent_id, _ in sorted_agents]

            # Save leaderboard
            leaderboard_file.write_text(json.dumps(leaderboard, indent=2))

            return ToolResult(
                success=True,
                output={
                    "leaderboard_file": str(leaderboard_file),
                    "updates_applied": updates_applied,
                    "ranking": leaderboard["ranking"][:5],  # Top 5
                    "last_updated": session_date,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error updating leaderboard: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.update_leaderboard")

    def _update_agent_entry(
        self, leaderboard: dict, agent_id: str, points: int, session_date: str, achievement: str | None
    ):
        """Update individual agent entry in leaderboard."""
        if agent_id not in leaderboard["agents"]:
            leaderboard["agents"][agent_id] = {
                "total_points": 0,
                "sessions": [],
                "achievements": [],
            }

        # Update points
        leaderboard["agents"][agent_id]["total_points"] += points

        # Add session tracking
        if "sessions" not in leaderboard["agents"][agent_id]:
            leaderboard["agents"][agent_id]["sessions"] = []

        leaderboard["agents"][agent_id]["sessions"].append(
            {"date": session_date, "points": points}
        )

        # Add achievement if provided
        if achievement:
            if "achievements" not in leaderboard["agents"][agent_id]:
                leaderboard["agents"][agent_id]["achievements"] = []

            leaderboard["agents"][agent_id]["achievements"].append(
                {
                    "achievement": achievement,
                    "points": points,
                    "timestamp": datetime.now().isoformat(),
                }
            )


class CycleReportTool(IToolAdapter):
    """Generate Captain's cycle report."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.cycle_report",
            version="2.0.0",
            category="captain",
            summary="Generate Captain's cycle activity report",
            required_params=["cycle_number"],
            optional_params={
                "missions_assigned": 0,
                "messages_sent": 0,
                "agents_activated": [],
                "points_awarded": 0,
                "notes": "",
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute cycle report generation."""
        try:
            cycle_num = params["cycle_number"]
            missions = params.get("missions_assigned", 0)
            messages = params.get("messages_sent", 0)
            agents = params.get("agents_activated", [])
            points = params.get("points_awarded", 0)
            notes = params.get("notes", "")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_file = Path(f"agent_workspaces/Agent-4/CAPTAIN_CYCLE_{cycle_num}_{timestamp}.md")
            report_file.parent.mkdir(parents=True, exist_ok=True)

            content = f"""# 🎯 CAPTAIN'S CYCLE REPORT #{cycle_num}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Cycle:** {cycle_num}

---

## 📊 CYCLE METRICS

- **Missions Assigned:** {missions}
- **Messages Sent:** {messages}
- **Agents Activated:** {len(agents)}
- **Points Awarded:** {points}

---

## 🤖 AGENTS ACTIVATED

{chr(10).join(f'- {agent}' for agent in agents) if agents else 'None this cycle'}

---

## 📝 CYCLE NOTES

{notes if notes else 'No additional notes this cycle.'}

---

## 🎯 NEXT CYCLE PRIORITIES

- Monitor agent progress
- Check for idle agents
- Review completed work
- Update leaderboard

---

**🐝 WE. ARE. SWARM.** ⚡🔥
"""

            report_file.write_text(content, encoding="utf-8")

            return ToolResult(
                success=True,
                output={
                    "cycle_number": cycle_num,
                    "report_file": str(report_file),
                    "missions_assigned": missions,
                    "messages_sent": messages,
                    "agents_activated": agents,
                    "points_awarded": points,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error generating cycle report: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.cycle_report")


class MorningBriefingTool(IToolAdapter):
    """Generate Captain's morning briefing with swarm status and priorities."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.morning_briefing",
            version="2.0.0",
            category="captain",
            summary="Generate Captain's morning briefing with swarm status",
            required_params=[],
            optional_params={"output_file": None, "detailed": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute morning briefing generation."""
        try:
            output_file = params.get("output_file")
            detailed = params.get("detailed", True)

            briefing = {
                "timestamp": datetime.now().isoformat(),
                "agents": {},
                "active_count": 0,
                "idle_count": 0,
                "recent_completions": [],
                "pending_tasks": [],
            }

            # Get agent status
            for agent_id in SWARM_AGENTS:
                workspace = Path(f"agent_workspaces/{agent_id}")
                if workspace.exists():
                    inbox = workspace / "inbox"
                    if inbox.exists():
                        messages = list(inbox.glob("*.md"))
                        if messages:
                            latest = max(messages, key=lambda p: p.stat().st_mtime)
                            last_activity = datetime.fromtimestamp(latest.stat().st_mtime)
                            minutes_ago = (datetime.now() - last_activity).total_seconds() / 60

                            status = "active" if minutes_ago < 60 else "idle"
                            briefing["agents"][agent_id] = {
                                "status": status,
                                "last_activity": last_activity.isoformat(),
                                "minutes_ago": round(minutes_ago, 1),
                            }

                            if status == "active":
                                briefing["active_count"] += 1
                            else:
                                briefing["idle_count"] += 1

            # Get recent completions (last 24 hours)
            for agent_dir in Path("agent_workspaces").iterdir():
                if not agent_dir.is_dir():
                    continue

                inbox = agent_dir / "inbox"
                if inbox.exists():
                    for msg_file in inbox.glob("*.md"):
                        mtime = datetime.fromtimestamp(msg_file.stat().st_mtime)
                        if (datetime.now() - mtime) < timedelta(hours=24):
                            content = msg_file.read_text(encoding="utf-8", errors="ignore")
                            if "COMPLETE" in content.upper() or "DONE" in content.upper():
                                briefing["recent_completions"].append(
                                    {
                                        "agent": agent_dir.name,
                                        "file": msg_file.name,
                                        "time": mtime.isoformat(),
                                    }
                                )

            # Get pending tasks
            for agent_dir in Path("agent_workspaces").iterdir():
                if not agent_dir.is_dir():
                    continue

                for order_file in agent_dir.glob("*EXECUTION_ORDER*.md"):
                    mtime = datetime.fromtimestamp(order_file.stat().st_mtime)
                    briefing["pending_tasks"].append(
                        {
                            "agent": agent_dir.name,
                            "file": order_file.name,
                            "assigned": mtime.isoformat(),
                            "age_hours": round((datetime.now() - mtime).total_seconds() / 3600, 1),
                        }
                    )

            # Sort completions and tasks
            briefing["recent_completions"].sort(key=lambda x: x["time"], reverse=True)
            briefing["pending_tasks"].sort(key=lambda x: x["assigned"], reverse=True)

            # Generate markdown if output file specified
            if output_file:
                self._generate_markdown_briefing(briefing, Path(output_file))

            return ToolResult(
                success=True,
                output={
                    "briefing": briefing,
                    "summary": {
                        "active_agents": briefing["active_count"],
                        "idle_agents": briefing["idle_count"],
                        "recent_completions": len(briefing["recent_completions"]),
                        "pending_tasks": len(briefing["pending_tasks"]),
                    },
                    "output_file": output_file,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error generating morning briefing: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.morning_briefing")

    def _generate_markdown_briefing(self, briefing: dict, output_file: Path):
        """Generate markdown briefing file."""
        output_file.parent.mkdir(parents=True, exist_ok=True)

        content = f"# ☀️ CAPTAIN'S MORNING BRIEFING\n\n"
        content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += f"## 🤖 AGENT STATUS\n\n"
        content += f"**Active:** {briefing['active_count']}/8  |  **Idle:** {briefing['idle_count']}/8\n\n"

        for agent_id, info in briefing["agents"].items():
            emoji = "🟢" if info["status"] == "active" else "🟡"
            content += f"{emoji} **{agent_id}**: {info['status'].upper()} "
            content += f"(last activity: {info['minutes_ago']:.0f}m ago)\n"

        content += f"\n## ✅ RECENT COMPLETIONS (Last 24h)\n\n"
        for comp in briefing["recent_completions"][:5]:
            content += f"- **{comp['agent']}**: {comp['file']}\n"

        content += f"\n## 📋 PENDING TASKS\n\n"
        for task in briefing["pending_tasks"][:5]:
            content += f"- **{task['agent']}**: {task['file']} ({task['age_hours']:.1f}h ago)\n"

        content += f"\n**🐝 WE. ARE. SWARM.** ⚡\n"

        output_file.write_text(content, encoding="utf-8")


# Export all tools
__all__ = [
    "GasDeliveryTool",
    "LeaderboardUpdateTool",
    "CycleReportTool",
    "MorningBriefingTool",
]