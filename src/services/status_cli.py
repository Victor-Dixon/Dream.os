#!/usr/bin/env python3
"""
Status CLI Module
=================

Agent Cellphone V2 Status CLI - Swarm System Status and Monitoring
=================================================================

Provides command-line interface for checking swarm system status,
agent health, and coordination metrics.

V2 Compliant: SOLID Architecture, Modular Design, Comprehensive Monitoring

Usage:
    python -m src.services.status_cli --health
    python -m src.services.status_cli --agents
    python -m src.services.status_cli --coordination

Author: Agent-8 (QA & Publishing Coordination Lead)
Date: 2026-01-12
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StatusCLI:
    """Command-line interface for swarm status and monitoring."""

    def __init__(self):
        """Initialize the status CLI."""
        self.start_time = datetime.now()

    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health status."""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "system_status": "healthy",
            "uptime": str(datetime.now() - self.start_time),
            "components": {
                "messaging": self._check_messaging_health(),
                "agents": self._check_agents_health(),
                "coordination": self._check_coordination_health(),
            }
        }

        # Determine overall status
        component_statuses = [comp.get("status", "unknown") for comp in health_status["components"].values()]
        if "critical" in component_statuses:
            health_status["system_status"] = "critical"
        elif "warning" in component_statuses:
            health_status["system_status"] = "warning"

        return health_status

    def _check_messaging_health(self) -> Dict[str, Any]:
        """Check messaging system health."""
        try:
            # Check if message queue directory exists and has files
            queue_dir = Path("message_queue")
            if queue_dir.exists():
                queue_files = list(queue_dir.glob("*.json"))
                return {
                    "status": "healthy",
                    "queue_files": len(queue_files),
                    "message": f"Messaging system operational with {len(queue_files)} queue files"
                }
            else:
                return {
                    "status": "warning",
                    "message": "Message queue directory not found"
                }
        except Exception as e:
            return {
                "status": "critical",
                "message": f"Messaging health check failed: {e}"
            }

    def _check_agents_health(self) -> Dict[str, Any]:
        """Check agent system health."""
        try:
            # Check agent workspaces
            workspace_dir = Path("agent_workspaces")
            if workspace_dir.exists():
                agent_dirs = [d for d in workspace_dir.iterdir() if d.is_dir() and d.name.startswith("Agent-")]
                return {
                    "status": "healthy",
                    "active_agents": len(agent_dirs),
                    "agent_directories": [d.name for d in agent_dirs],
                    "message": f"Found {len(agent_dirs)} agent workspaces"
                }
            else:
                return {
                    "status": "warning",
                    "message": "Agent workspaces directory not found"
                }
        except Exception as e:
            return {
                "status": "critical",
                "message": f"Agent health check failed: {e}"
            }

    def _check_coordination_health(self) -> Dict[str, Any]:
        """Check coordination system health."""
        try:
            # Check for coordination cache
            cache_file = Path("coordination_cache.json")
            if cache_file.exists():
                cache_mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
                age_hours = (datetime.now() - cache_mtime).total_seconds() / 3600

                if age_hours < 24:  # Cache updated within 24 hours
                    return {
                        "status": "healthy",
                        "cache_age_hours": round(age_hours, 1),
                        "message": f"Coordination cache updated {round(age_hours, 1)} hours ago"
                    }
                else:
                    return {
                        "status": "warning",
                        "cache_age_hours": round(age_hours, 1),
                        "message": f"Coordination cache is {round(age_hours, 1)} hours old"
                    }
            else:
                return {
                    "status": "warning",
                    "message": "Coordination cache file not found"
                }
        except Exception as e:
            return {
                "status": "critical",
                "message": f"Coordination health check failed: {e}"
            }

    def get_agents_status(self) -> Dict[str, Any]:
        """Get detailed status of all agents."""
        agents_status = {
            "timestamp": datetime.now().isoformat(),
            "agents": []
        }

        workspace_dir = Path("agent_workspaces")
        if workspace_dir.exists():
            for agent_dir in workspace_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_status = self._get_agent_status(agent_dir)
                    agents_status["agents"].append(agent_status)

        return agents_status

    def _get_agent_status(self, agent_dir: Path) -> Dict[str, Any]:
        """Get status for a specific agent."""
        agent_name = agent_dir.name
        inbox_dir = agent_dir / "inbox"
        archive_dir = agent_dir / "archive"

        status = {
            "name": agent_name,
            "workspace_exists": True,
            "inbox_messages": 0,
            "archive_messages": 0,
            "last_activity": None
        }

        # Check inbox
        if inbox_dir.exists():
            inbox_files = list(inbox_dir.glob("*.md"))
            status["inbox_messages"] = len(inbox_files)

            if inbox_files:
                # Get most recent file modification time
                latest_file = max(inbox_files, key=lambda f: f.stat().st_mtime)
                status["last_activity"] = datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()

        # Check archive
        if archive_dir.exists():
            archive_files = list(archive_dir.glob("*.md"))
            status["archive_messages"] = len(archive_files)

        return status

    def get_coordination_status(self) -> Dict[str, Any]:
        """Get coordination system status and metrics."""
        coord_status = {
            "timestamp": datetime.now().isoformat(),
            "coordination_metrics": {}
        }

        try:
            cache_file = Path("coordination_cache.json")
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    coord_status["coordination_metrics"] = cache_data
        except Exception as e:
            coord_status["error"] = f"Failed to load coordination cache: {e}"

        return coord_status

    def execute(self, args: Optional[List[str]] = None) -> int:
        """Execute the status CLI command."""
        parser = self._create_parser()

        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        try:
            if parsed_args.health:
                status = self.check_system_health()
                self._print_health_status(status)
                return 0

            elif parsed_args.agents:
                status = self.get_agents_status()
                self._print_agents_status(status)
                return 0

            elif parsed_args.coordination:
                status = self.get_coordination_status()
                self._print_coordination_status(status)
                return 0

            elif parsed_args.all:
                health = self.check_system_health()
                agents = self.get_agents_status()
                coordination = self.get_coordination_status()

                self._print_health_status(health)
                print("\n" + "="*50)
                self._print_agents_status(agents)
                print("\n" + "="*50)
                self._print_coordination_status(coordination)
                return 0

            else:
                parser.print_help()
                return 0

        except Exception as e:
            logger.error(f"❌ Status CLI error: {e}")
            return 1

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="🐝 Agent Cellphone V2 Status CLI - Swarm System Monitoring",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
🐝 SWARM STATUS CLI - MONITOR YOUR AGENTS!
==========================================

EXAMPLES:
--------
# Check overall system health
python -m src.services.status_cli --health

# View agent status details
python -m src.services.status_cli --agents

# Check coordination metrics
python -m src.services.status_cli --coordination

# Get complete system status
python -m src.services.status_cli --all

🐝 WE. ARE. SWARM. ⚡️🔥
            """
        )

        parser.add_argument(
            "--health",
            action="store_true",
            help="Check overall system health status"
        )

        parser.add_argument(
            "--agents", "-a",
            action="store_true",
            help="Show detailed agent status information"
        )

        parser.add_argument(
            "--coordination", "-c",
            action="store_true",
            help="Display coordination system metrics"
        )

        parser.add_argument(
            "--all",
            action="store_true",
            help="Show complete system status (health + agents + coordination)"
        )

        return parser

    def _print_health_status(self, status: Dict[str, Any]) -> None:
        """Print formatted health status."""
        print("🌐 SYSTEM HEALTH STATUS")
        print("=" * 50)
        print(f"Timestamp: {status['timestamp']}")
        print(f"System Status: {status['system_status'].upper()}")
        print(f"Uptime: {status['uptime']}")

        print("\n📊 COMPONENT STATUS")
        print("-" * 30)
        for component, comp_status in status["components"].items():
            status_icon = {
                "healthy": "✅",
                "warning": "⚠️",
                "critical": "❌",
                "unknown": "❓"
            }.get(comp_status.get("status", "unknown"), "❓")

            print(f"{status_icon} {component.title()}: {comp_status.get('status', 'unknown').upper()}")
            if "message" in comp_status:
                print(f"   {comp_status['message']}")

    def _print_agents_status(self, status: Dict[str, Any]) -> None:
        """Print formatted agents status."""
        print("🤖 AGENTS STATUS")
        print("=" * 50)
        print(f"Timestamp: {status['timestamp']}")
        print(f"Total Agents: {len(status['agents'])}")

        print("\n👥 AGENT DETAILS")
        print("-" * 30)
        for agent in status["agents"]:
            print(f"📂 {agent['name']}")
            print(f"   Workspace: {'✅' if agent['workspace_exists'] else '❌'}")
            print(f"   Inbox Messages: {agent['inbox_messages']}")
            print(f"   Archive Messages: {agent['archive_messages']}")
            if agent['last_activity']:
                print(f"   Last Activity: {agent['last_activity']}")
            print()

    def _print_coordination_status(self, status: Dict[str, Any]) -> None:
        """Print formatted coordination status."""
        print("🔗 COORDINATION STATUS")
        print("=" * 50)
        print(f"Timestamp: {status['timestamp']}")

        if "error" in status:
            print(f"❌ Error: {status['error']}")
        else:
            metrics = status.get("coordination_metrics", {})
            if metrics:
                print("\n📈 COORDINATION METRICS")
                print("-" * 30)
                for key, value in metrics.items():
                    print(f"{key}: {value}")
            else:
                print("ℹ️  No coordination metrics available")


def main() -> int:
    """Main entry point."""
    cli = StatusCLI()
    return cli.execute()


if __name__ == "__main__":
    exit_code = main()
    print("\n🐝 WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)