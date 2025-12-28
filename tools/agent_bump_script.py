#!/usr/bin/env python3
"""
Agent Bump Script
=================

Bumps agent versions and updates status across the swarm.

Purpose: Coordinate agent version updates and status synchronization
Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-28
Usage: python tools/agent_bump_script.py --agent Agent-X --action bump|status|sync
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class AgentBumpScript:
    """Handles agent version bumping and status coordination."""

    def __init__(self):
        """Initialize the bump script."""
        self.agent_workspaces = Path("agent_workspaces")
        self.agents = [f"Agent-{i}" for i in range(1, 9)]  # Agent-1 through Agent-8

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current status for an agent."""
        status_file = self.agent_workspaces / agent_id / "status.json"
        if not status_file.exists():
            return None

        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {agent_id} status: {e}")
            return None

    def update_agent_status(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update agent status with new information."""
        status_file = self.agent_workspaces / agent_id / "status.json"
        if not status_file.exists():
            print(f"Status file not found for {agent_id}")
            return False

        try:
            # Read current status
            with open(status_file, 'r') as f:
                current_status = json.load(f)

            # Apply updates
            current_status.update(updates)
            current_status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Write back
            with open(status_file, 'w') as f:
                json.dump(current_status, f, indent=2)

            print(f"✅ Updated {agent_id} status")
            return True

        except Exception as e:
            print(f"❌ Error updating {agent_id} status: {e}")
            return False

    def bump_agent_version(self, agent_id: str, bump_type: str = "patch") -> bool:
        """Bump agent version number."""
        status = self.get_agent_status(agent_id)
        if not status:
            print(f"❌ No status found for {agent_id}")
            return False

        # Get current version
        current_version = status.get("version", "1.0.0")

        try:
            major, minor, patch = map(int, current_version.split('.'))

            # Apply bump
            if bump_type == "major":
                major += 1
                minor = 0
                patch = 0
            elif bump_type == "minor":
                minor += 1
                patch = 0
            else:  # patch
                patch += 1

            new_version = f"{major}.{minor}.{patch}"

            # Update status
            updates = {
                "version": new_version,
                "last_bump": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "bump_type": bump_type
            }

            return self.update_agent_status(agent_id, updates)

        except ValueError:
            print(f"❌ Invalid version format: {current_version}")
            return False

    def sync_agent_status(self, agent_id: str) -> bool:
        """Sync agent status with current state."""
        status = self.get_agent_status(agent_id)
        if not status:
            return False

        # Update timestamp and sync markers
        updates = {
            "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sync_status": "completed"
        }

        return self.update_agent_status(agent_id, updates)

    def get_swarm_status(self) -> Dict[str, Any]:
        """Get overall swarm status."""
        swarm_status = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "agents": {},
            "summary": {
                "total_agents": len(self.agents),
                "active_agents": 0,
                "inactive_agents": 0,
                "latest_versions": []
            }
        }

        for agent_id in self.agents:
            status = self.get_agent_status(agent_id)
            if status:
                swarm_status["agents"][agent_id] = {
                    "status": status.get("fsm_state", "unknown"),
                    "version": status.get("version", "unknown"),
                    "last_updated": status.get("last_updated", "never")
                }

                if status.get("fsm_state") == "ACTIVE":
                    swarm_status["summary"]["active_agents"] += 1
                else:
                    swarm_status["summary"]["inactive_agents"] += 1

                version = status.get("version", "0.0.0")
                swarm_status["summary"]["latest_versions"].append(f"{agent_id}: {version}")
            else:
                swarm_status["agents"][agent_id] = {"status": "missing", "error": "status file not found"}

        return swarm_status

    def print_swarm_status(self) -> None:
        """Print formatted swarm status."""
        status = self.get_swarm_status()

        print("🐝 SWARM STATUS REPORT")
        print("=" * 50)
        print(f"Timestamp: {status['timestamp']}")
        print()

        print("AGENT STATUS:")
        for agent_id, agent_status in status["agents"].items():
            status_icon = "✅" if agent_status.get("status") == "ACTIVE" else "❌"
            version = agent_status.get("version", "unknown")
            last_updated = agent_status.get("last_updated", "never")
            print(f"  {status_icon} {agent_id}: {agent_status.get('status', 'unknown')} (v{version}) - {last_updated}")

        print()
        print("SUMMARY:")
        summary = status["summary"]
        print(f"  Total Agents: {summary['total_agents']}")
        print(f"  Active: {summary['active_agents']}")
        print(f"  Inactive: {summary['inactive_agents']}")
        print()
        print("LATEST VERSIONS:")
        for version_info in summary["latest_versions"][:5]:  # Show first 5
            print(f"  {version_info}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Bump agent versions and manage swarm status"
    )
    parser.add_argument(
        "--agent",
        help="Specific agent to operate on (e.g., Agent-5)"
    )
    parser.add_argument(
        "--action",
        choices=["bump", "status", "sync", "report"],
        default="report",
        help="Action to perform"
    )
    parser.add_argument(
        "--bump-type",
        choices=["patch", "minor", "major"],
        default="patch",
        help="Type of version bump"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Apply action to all agents"
    )

    args = parser.parse_args()

    script = AgentBumpScript()

    if args.action == "report":
        script.print_swarm_status()

    elif args.action == "status":
        if args.agent:
            status = script.get_agent_status(args.agent)
            if status:
                print(f"Status for {args.agent}:")
                print(json.dumps(status, indent=2))
            else:
                print(f"No status found for {args.agent}")
        else:
            print("Use --agent to specify which agent status to check")

    elif args.action == "bump":
        if args.all:
            print("Bumping all agents...")
            success_count = 0
            for agent_id in script.agents:
                if script.bump_agent_version(agent_id, args.bump_type):
                    success_count += 1
            print(f"✅ Bumped {success_count}/{len(script.agents)} agents")
        elif args.agent:
            if script.bump_agent_version(args.agent, args.bump_type):
                print(f"✅ Bumped {args.agent} {args.bump_type} version")
            else:
                print(f"❌ Failed to bump {args.agent}")
        else:
            print("Use --agent or --all to specify which agents to bump")

    elif args.action == "sync":
        if args.all:
            print("Syncing all agents...")
            success_count = 0
            for agent_id in script.agents:
                if script.sync_agent_status(agent_id):
                    success_count += 1
            print(f"✅ Synced {success_count}/{len(script.agents)} agents")
        elif args.agent:
            if script.sync_agent_status(args.agent):
                print(f"✅ Synced {args.agent} status")
            else:
                print(f"❌ Failed to sync {args.agent}")
        else:
            print("Use --agent or --all to specify which agents to sync")


if __name__ == "__main__":
    main()
