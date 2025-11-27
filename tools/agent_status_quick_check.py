#!/usr/bin/env python3
"""
Agent Status Quick Check - Fast Agent Progress Verification
============================================================

Quickly check agent status.json to see current missions, points, and completion status.
Prevents "already done" confusion by showing real-time agent progress.

Usage:
    python tools/agent_status_quick_check.py --agent Agent-6
    python tools/agent_status_quick_check.py --agent Agent-6 --detail
    python tools/agent_status_quick_check.py --all

Author: Agent-6 - VSCode Forking & Quality Gates Specialist
Created: 2025-10-13
V2 Compliance: <400 lines
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class AgentStatusChecker:
    """Quick agent status verification."""

    def __init__(self, workspace_root: Path):
        """Initialize status checker."""
        self.workspace_root = workspace_root
        self.agent_workspaces = workspace_root / "agent_workspaces"

    def get_agent_status(self, agent_id: str) -> dict[str, Any] | None:
        """
        Get status.json for specific agent.

        Args:
            agent_id: Agent identifier (e.g., "Agent-6")

        Returns:
            Status data or None if not found
        """
        status_path = self.agent_workspaces / agent_id / "status.json"

        if not status_path.exists():
            return None

        try:
            with open(status_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading {agent_id} status: {e}")
            return None

    def check_devlog_created(self, agent_id: str) -> dict[str, Any]:
        """
        Check if agent has created devlog recently.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-2")
            
        Returns:
            Dict with devlog status information
        """
        from datetime import datetime, timedelta
        
        devlog_info = {
            "has_recent_devlog": False,
            "last_devlog": None,
            "devlog_age_hours": None,
            "devlog_count": 0,
        }
        
        # Check both locations: devlogs/ and agent_workspaces/{agent_id}/devlogs/
        devlog_dirs = [
            self.workspace_root / "devlogs",
            self.agent_workspaces / agent_id / "devlogs",
        ]
        
        all_devlogs = []
        for devlog_dir in devlog_dirs:
            if devlog_dir.exists():
                # Find devlogs matching agent pattern
                agent_patterns = [
                    f"*{agent_id.lower()}*",
                    f"*{agent_id.replace('-', '_').lower()}*",
                    f"*{agent_id}*",
                ]
                for pattern in agent_patterns:
                    all_devlogs.extend(list(devlog_dir.glob(f"{pattern}.md")))
        
        if all_devlogs:
            # Get most recent devlog
            latest_devlog = max(all_devlogs, key=lambda p: p.stat().st_mtime)
            devlog_info["last_devlog"] = latest_devlog.name
            devlog_info["devlog_count"] = len(all_devlogs)
            
            # Check if recent (within last 7 days)
            mtime = datetime.fromtimestamp(latest_devlog.stat().st_mtime)
            age_hours = (datetime.now() - mtime).total_seconds() / 3600
            devlog_info["devlog_age_hours"] = round(age_hours, 1)
            devlog_info["has_recent_devlog"] = age_hours <= (7 * 24)  # 7 days
        
        return devlog_info

    def format_quick_status(self, agent_id: str, status: dict[str, Any]) -> str:
        """Format quick status summary."""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"🤖 {agent_id} - Quick Status")
        output.append(f"{'='*60}")

        # Current mission
        mission = status.get("current_mission", "None")
        output.append(f"📋 Mission: {mission}")

        # Current phase
        phase = status.get("current_phase", "Unknown")
        output.append(f"🎯 Phase: {phase}")

        # Status
        agent_status = status.get("status", "Unknown")
        output.append(f"⚡ Status: {agent_status}")

        # Points
        points = status.get("total_points_earned", 0)
        output.append(f"🏆 Points: {points}")

        # Last update
        last_update = status.get("last_update", "Unknown")
        output.append(f"🕒 Last Update: {last_update}")
        
        # Devlog check (NEW FEATURE - Agent-2 implementation)
        devlog_info = self.check_devlog_created(agent_id)
        if devlog_info["has_recent_devlog"]:
            output.append(f"📝 Devlog: ✅ Recent ({devlog_info['last_devlog']}, {devlog_info['devlog_age_hours']:.1f}h ago)")
        else:
            if devlog_info["last_devlog"]:
                output.append(f"📝 Devlog: ⚠️ Stale ({devlog_info['last_devlog']}, {devlog_info['devlog_age_hours']:.1f}h ago)")
            else:
                output.append(f"📝 Devlog: ❌ None found")

        return "\n".join(output)

    def format_detailed_status(self, agent_id: str, status: dict[str, Any]) -> str:
        """Format detailed status with execution details."""
        output = [self.format_quick_status(agent_id, status)]
        output.append(f"\n{'─'*60}")
        output.append("📊 DETAILED EXECUTION STATUS")
        output.append(f"{'─'*60}")

        # Check for week execution data (common pattern)
        for key in status.keys():
            if "week" in key.lower() and "execution" in key.lower():
                week_data = status[key]
                output.append(f"\n🗓️ {key}:")

                if isinstance(week_data, dict):
                    for phase_key, phase_data in week_data.items():
                        if isinstance(phase_data, dict):
                            output.append(f"  └─ {phase_key}:")

                            # Status
                            if "status" in phase_data:
                                output.append(f"     Status: {phase_data['status']}")

                            # Completion
                            if "completed" in phase_data:
                                output.append(f"     Completed: {phase_data['completed']}")

                            # Files/Tests
                            if "files_created" in phase_data:
                                output.append(f"     Files: {phase_data['files_created']}")
                            if "tests_written" in phase_data:
                                output.append(f"     Tests: {phase_data['tests_written']}")
                            if "coverage" in phase_data:
                                output.append(f"     Coverage: {phase_data['coverage']}")

        # Tasks completed
        if "tasks_completed_this_week" in status:
            tasks = status["tasks_completed_this_week"]
            output.append(
                f"\n✅ Tasks Completed: {len(tasks) if isinstance(tasks, list) else 'N/A'}"
            )

        return "\n".join(output)

    def check_all_agents(self) -> None:
        """Check status of all agents."""
        print(f"\n{'='*60}")
        print("🐝 SWARM STATUS - All Agents")
        print(f"{'='*60}")

        if not self.agent_workspaces.exists():
            print("❌ No agent workspaces found!")
            return

        agents = []
        for agent_dir in sorted(self.agent_workspaces.iterdir()):
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                status = self.get_agent_status(agent_dir.name)
                if status:
                    agents.append((agent_dir.name, status))

        if not agents:
            print("❌ No agent status files found!")
            return

        # Summary table (with devlog check)
        print(f"\n{'Agent':<12} {'Mission':<30} {'Status':<15} {'Points':<8} {'Devlog':<10}")
        print(f"{'-'*12} {'-'*30} {'-'*15} {'-'*8} {'-'*10}")

        total_points = 0
        for agent_id, status in agents:
            mission = status.get("current_mission", "None")[:28]
            agent_status = status.get("status", "Unknown")[:13]
            points = status.get("total_points_earned", 0)
            total_points += points
            
            # Devlog check (NEW FEATURE - Agent-2 implementation)
            devlog_info = self.check_devlog_created(agent_id)
            if devlog_info["has_recent_devlog"]:
                devlog_status = "✅ Recent"
            elif devlog_info["last_devlog"]:
                devlog_status = "⚠️ Stale"
            else:
                devlog_status = "❌ None"

            print(f"{agent_id:<12} {mission:<30} {agent_status:<15} {points:<8} {devlog_status:<10}")

        print(f"{'-'*12} {'-'*30} {'-'*15} {'-'*8} {'-'*10}")
        print(f"{'TOTAL':<12} {'':<30} {'':<15} {total_points:<8} {'':<10}")
        print(f"\n🏆 Swarm Total: {total_points} points")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="🔍 Agent Status Quick Check - Fast agent progress verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick check single agent
  python tools/agent_status_quick_check.py --agent Agent-6
  
  # Detailed check with execution data
  python tools/agent_status_quick_check.py --agent Agent-6 --detail
  
  # Check all agents
  python tools/agent_status_quick_check.py --all

🐝 WE. ARE. SWARM. ⚡️🔥
        """,
    )

    parser.add_argument("--agent", type=str, help="Agent ID to check (e.g., Agent-6)")

    parser.add_argument("--detail", action="store_true", help="Show detailed execution status")

    parser.add_argument("--all", action="store_true", help="Check all agents")

    args = parser.parse_args()

    # Validate arguments
    if not args.all and not args.agent:
        parser.print_help()
        print("\n❌ Error: Must specify --agent or --all")
        sys.exit(1)

    # Initialize checker
    workspace_root = Path(__file__).parent.parent
    checker = AgentStatusChecker(workspace_root)

    # Execute check
    if args.all:
        checker.check_all_agents()
    else:
        status = checker.get_agent_status(args.agent)
        if not status:
            print(f"\n❌ No status found for {args.agent}")
            print(f"   Path: {checker.agent_workspaces / args.agent / 'status.json'}")
            sys.exit(1)

        if args.detail:
            print(checker.format_detailed_status(args.agent, status))
        else:
            print(checker.format_quick_status(args.agent, status))

    print()  # Final newline


if __name__ == "__main__":
    main()
