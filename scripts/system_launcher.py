#!/usr/bin/env python3
"""
Agent System Launcher - One-Click Access to All Systems
=======================================================

Provides unified access to all agent systems with intelligent command routing,
usage tracking, and interactive help.

Usage:
    python scripts/system_launcher.py --system scanner
    python scripts/system_launcher.py --system debate --topic "decision"
    python scripts/system_launcher.py --list
    python scripts/system_launcher.py --help
    python scripts/system_launcher.py --train
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentSystemLauncher:
    """Unified launcher for all agent systems with usage tracking."""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.systems = self._load_system_definitions()
        self.usage_tracker = SystemUsageTracker()

    def _load_system_definitions(self):
        """Load system definitions with commands and metadata."""
        return {
            "scanner": {
                "name": "Project Scanner",
                "description": "Codebase analysis and health assessment",
                "command": "python tools/analytics/project_scanner.py",
                "examples": [
                    "python tools/analytics/project_scanner.py --target src/",
                    "python tools/analytics/project_scanner.py --target . --format json"
                ],
                "category": "analysis",
                "training_time": "5 min",
                "power_level": "HIGH"
            },
            "debate": {
                "name": "Debate System",
                "description": "Structured decision-making and consensus building",
                "command": "python -c \"from src.core.debate import DebateManager; dm = DebateManager(); print('Debate system ready')\"",
                "examples": [
                    "python -c \"from src.core.debate import DebateManager; dm = DebateManager()\"",
                    "python scripts/debate_launcher.py --topic 'architecture_decision'"
                ],
                "category": "decision_making",
                "training_time": "10 min",
                "power_level": "HIGH"
            },
            "planner": {
                "name": "Cycle Planner",
                "description": "Task planning and prioritization",
                "command": "python tools/cycle_planner/cycle_planner.py",
                "examples": [
                    "python tools/cycle_planner/cycle_planner.py --create",
                    "python tools/cycle_planner/cycle_planner.py --status"
                ],
                "category": "planning",
                "training_time": "3 min",
                "power_level": "MEDIUM"
            },
            "tasks": {
                "name": "Master Task Lists",
                "description": "Centralized task tracking and coordination",
                "command": f"code {self.base_path / 'MASTER_TASK_LIST.md'}",
                "examples": [
                    f"code {self.base_path / 'MASTER_TASK_LIST.md'}",
                    f"code {self.base_path / 'MASTER_TASK_LOG.md'}"
                ],
                "category": "coordination",
                "training_time": "2 min",
                "power_level": "MEDIUM"
            },
            "database": {
                "name": "Database QA",
                "description": "Automated database validation and testing",
                "command": "python scripts/database/database_qa_integration.py",
                "examples": [
                    "python scripts/database/database_qa_integration.py",
                    "python scripts/database/simple_database_audit.py"
                ],
                "category": "infrastructure",
                "training_time": "8 min",
                "power_level": "MEDIUM"
            },
            "config": {
                "name": "Configuration Viewer",
                "description": "View and manage agent configurations",
                "command": f"code {self.base_path / 'config' / 'agent_config.json'}",
                "examples": [
                    f"cat {self.base_path / 'config' / 'agent_config.json'} | jq",
                    f"cat {self.base_path / 'config' / 'coordination_config.json'} | jq"
                ],
                "category": "configuration",
                "training_time": "2 min",
                "power_level": "LOW"
            },
            "health": {
                "name": "System Health Monitor",
                "description": "Monitor overall system health and performance",
                "command": "python tools/health/system_health_monitor.py",
                "examples": [
                    "python tools/health/system_health_monitor.py",
                    "python tools/metrics/system_usage_dashboard.py"
                ],
                "category": "monitoring",
                "training_time": "5 min",
                "power_level": "MEDIUM"
            },
            "portal": {
                "name": "System Portal",
                "description": "Access the complete system documentation portal",
                "command": f"code {self.base_path / 'docs' / 'systems' / 'agent_system_portal.md'}",
                "examples": [
                    f"code {self.base_path / 'docs' / 'systems' / 'agent_system_portal.md'}",
                    "python scripts/system_launcher.py --train"
                ],
                "category": "documentation",
                "training_time": "1 min",
                "power_level": "LOW"
            }
        }

    def launch_system(self, system_name, args=None, agent_id="Unknown"):
        """Launch a specific system with usage tracking."""
        if system_name not in self.systems:
            print(f"❌ System '{system_name}' not found.")
            self.show_available_systems()
            return False

        system = self.systems[system_name]

        # Track usage
        self.usage_tracker.track_usage(agent_id, system_name, "launch")

        # Construct command
        command = system["command"]
        if args:
            command += f" {args}"

        print(f"🚀 Launching {system['name']}...")
        print(f"Command: {command}")
        print("-" * 50)

        try:
            # Execute command
            result = subprocess.run(command, shell=True, cwd=self.base_path)

            if result.returncode == 0:
                print(f"✅ {system['name']} completed successfully")
                return True
            else:
                print(f"⚠️ {system['name']} exited with code {result.returncode}")
                return False

        except Exception as e:
            print(f"❌ Failed to launch {system['name']}: {e}")
            return False

    def show_available_systems(self):
        """Display all available systems in a nice format."""
        print("\n🏗️ AVAILABLE AGENT SYSTEMS")
        print("=" * 60)

        categories = {}
        for name, system in self.systems.items():
            category = system["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((name, system))

        for category, systems in categories.items():
            print(f"\n📂 {category.upper()}:")
            for name, system in systems:
                power_indicator = {
                    "HIGH": "🔴",
                    "MEDIUM": "🟡",
                    "LOW": "🟢"
                }.get(system["power_level"], "⚪")

                print(f"  {power_indicator} {name:<12} | {system['description']}")
                print(f"                 | Training: {system['training_time']} | Command: {system['command'][:50]}...")

        print("
💡 Usage: python scripts/system_launcher.py --system <name>")
        print("📚 Help: python scripts/system_launcher.py --help")

    def show_system_details(self, system_name):
        """Show detailed information about a specific system."""
        if system_name not in self.systems:
            print(f"❌ System '{system_name}' not found.")
            return

        system = self.systems[system_name]

        print(f"\n🔍 {system['name']} - Detailed Information")
        print("=" * 50)
        print(f"Description: {system['description']}")
        print(f"Category: {system['category']}")
        print(f"Power Level: {system['power_level']}")
        print(f"Training Time: {system['training_time']}")
        print(f"\nBase Command:\n  {system['command']}")
        print("
Examples:"        for example in system["examples"]:
            print(f"  {example}")

    def show_training_program(self):
        """Display the training program."""
        print("\n🎓 AGENT SYSTEM TRAINING PROGRAM")
        print("=" * 50)
        print("Complete training program for system adoption:")
        print()

        training_schedule = [
            ("Day 1", "Project Scanner", "Code analysis and health assessment"),
            ("Day 2", "Master Task Lists", "Centralized coordination and tracking"),
            ("Day 3", "Cycle Planner", "Task planning and prioritization"),
            ("Day 4", "Debate System", "Structured decision-making"),
            ("Day 5", "Integration Day", "Combining all systems effectively")
        ]

        for day, system, description in training_schedule:
            print(f"📅 {day}: {system}")
            print(f"   {description}")
            if system.lower().replace(" ", "_") in self.systems:
                training_time = self.systems[system.lower().replace(" ", "_")]["training_time"]
                print(f"   ⏱️  Training time: {training_time}")
            print()

        print("🚀 Launch training: python scripts/system_launcher.py --train")

    def run_training_session(self, day=None):
        """Run an interactive training session."""
        if day:
            print(f"🎓 Starting Day {day} Training Session")
        else:
            print("🎓 Starting Interactive Training Session")

        # Simple training walkthrough
        print("\nLet's explore the available systems:")
        self.show_available_systems()

        print("
💡 Try launching a system:"        print("  python scripts/system_launcher.py --system scanner")
        print("  python scripts/system_launcher.py --system portal")


class SystemUsageTracker:
    """Track system usage for adoption metrics."""

    def __init__(self):
        self.usage_file = Path("data/system_usage.json")
        self.usage_file.parent.mkdir(exist_ok=True)

    def track_usage(self, agent_id, system_name, action):
        """Track system usage."""
        try:
            # Load existing usage data
            usage_data = {}
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    usage_data = json.load(f)

            # Update usage
            if agent_id not in usage_data:
                usage_data[agent_id] = {}

            if system_name not in usage_data[agent_id]:
                usage_data[agent_id][system_name] = []

            usage_data[agent_id][system_name].append({
                "timestamp": datetime.now().isoformat(),
                "action": action
            })

            # Save updated data
            with open(self.usage_file, 'w') as f:
                json.dump(usage_data, f, indent=2)

        except Exception as e:
            logger.warning(f"Failed to track usage: {e}")

    def get_usage_stats(self, agent_id=None):
        """Get usage statistics."""
        try:
            if not self.usage_file.exists():
                return {}

            with open(self.usage_file, 'r') as f:
                usage_data = json.load(f)

            if agent_id:
                return usage_data.get(agent_id, {})

            return usage_data

        except Exception as e:
            logger.warning(f"Failed to get usage stats: {e}")
            return {}


def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Agent System Launcher - Unified access to all agent systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/system_launcher.py --system scanner --args "--target src/"
  python scripts/system_launcher.py --system debate
  python scripts/system_launcher.py --list
  python scripts/system_launcher.py --details scanner
  python scripts/system_launcher.py --train
        """
    )

    parser.add_argument("--system", "-s", help="System to launch (scanner, debate, planner, tasks, etc.)")
    parser.add_argument("--args", "-a", help="Additional arguments to pass to the system")
    parser.add_argument("--agent", help="Agent ID for usage tracking (default: Unknown)")
    parser.add_argument("--list", "-l", action="store_true", help="List all available systems")
    parser.add_argument("--details", "-d", help="Show detailed information about a system")
    parser.add_argument("--train", "-t", action="store_true", help="Show training program")
    parser.add_argument("--usage", "-u", help="Show usage statistics for an agent")

    args = parser.parse_args()

    launcher = AgentSystemLauncher()

    # Handle different modes
    if args.list:
        launcher.show_available_systems()
    elif args.details:
        launcher.show_system_details(args.details)
    elif args.train:
        launcher.show_training_program()
    elif args.usage:
        stats = launcher.usage_tracker.get_usage_stats(args.usage)
        print(json.dumps(stats, indent=2))
    elif args.system:
        agent_id = args.agent or "Unknown"
        success = launcher.launch_system(args.system, args.args, agent_id)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()