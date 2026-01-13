#!/usr/bin/env python3
"""
Agent System Training Program
=============================

Interactive training program to help agents learn and adopt the available systems.
Provides hands-on exercises and guided learning experiences.

Usage:
    python scripts/system_training.py --day 1
    python scripts/system_training.py --system scanner
    python scripts/system_training.py --interactive
"""

import argparse
import subprocess
import time
import os
from pathlib import Path
import json

class SystemTrainer:
    """Interactive training program for agent systems."""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.training_modules = self._load_training_modules()

    def _load_training_modules(self):
        """Load training module definitions."""
        return {
            "scanner": {
                "title": "Project Scanner - Code Intelligence",
                "duration": "5 minutes",
                "objectives": [
                    "Understand codebase structure automatically",
                    "Generate dependency maps",
                    "Identify potential issues and improvements"
                ],
                "exercise": {
                    "title": "Codebase Health Assessment",
                    "steps": [
                        "Run scanner on src/core/ directory",
                        "Analyze output for unused imports",
                        "Identify circular dependencies",
                        "Create improvement action plan"
                    ],
                    "commands": [
                        "python tools/analytics/project_scanner.py --target src/core/",
                        "python tools/analytics/project_scanner.py --target src/ --format json",
                        "# Analyze the output above for issues"
                    ],
                    "success_criteria": [
                        "Scanner runs without errors",
                        "Output shows clear codebase structure",
                        "Can identify at least 3 improvement areas",
                        "Creates actionable improvement plan"
                    ]
                }
            },
            "tasks": {
                "title": "Master Task Lists - Coordination Intelligence",
                "duration": "2 minutes",
                "objectives": [
                    "Access centralized task tracking",
                    "Update task status and progress",
                    "Coordinate with other agents"
                ],
                "exercise": {
                    "title": "Task Coordination Practice",
                    "steps": [
                        "Open MASTER_TASK_LIST.md",
                        "Find your assigned tasks",
                        "Update status of completed work",
                        "Add a new task for tomorrow"
                    ],
                    "commands": [
                        "code MASTER_TASK_LIST.md",
                        "# Find tasks assigned to you",
                        "# Update status: [x] for completed, [ ] for pending",
                        "# Add new task at bottom of relevant section"
                    ],
                    "success_criteria": [
                        "Can open and navigate task list",
                        "Understands task status format",
                        "Successfully updates at least one task",
                        "Adds meaningful new task"
                    ]
                }
            },
            "planner": {
                "title": "Cycle Planner - Task Intelligence",
                "duration": "3 minutes",
                "objectives": [
                    "Create structured task plans",
                    "Set realistic priorities and deadlines",
                    "Track progress against plans"
                ],
                "exercise": {
                    "title": "Planning Cycle Creation",
                    "steps": [
                        "Create a new planning cycle",
                        "Add 3-5 tasks with priorities",
                        "Set realistic time estimates",
                        "View cycle status and progress"
                    ],
                    "commands": [
                        "python tools/cycle_planner/cycle_planner.py --create --name 'Training_Cycle'",
                        "python tools/cycle_planner/cycle_planner.py --add 'Complete system training' --priority HIGH --estimate 2h",
                        "python tools/cycle_planner/cycle_planner.py --add 'Apply learned skills' --priority MEDIUM --estimate 1h",
                        "python tools/cycle_planner/cycle_planner.py --status"
                    ],
                    "success_criteria": [
                        "Successfully creates planning cycle",
                        "Adds tasks with proper priorities",
                        "Sets realistic time estimates",
                        "Can view and understand status output"
                    ]
                }
            },
            "debate": {
                "title": "Debate System - Decision Intelligence",
                "duration": "10 minutes",
                "objectives": [
                    "Structure complex decision-making",
                    "Consider multiple perspectives",
                    "Reach consensus-based conclusions",
                    "Document decision rationale"
                ],
                "exercise": {
                    "title": "Decision Debate Practice",
                    "steps": [
                        "Initialize debate system",
                        "Create debate on a work decision",
                        "Add pro and con arguments",
                        "Resolve debate and analyze result"
                    ],
                    "commands": [
                        "python -c \"from src.core.debate import DebateManager; dm = DebateManager(); print('Debate system initialized')\"",
                        "# Create debate: 'Should we prioritize speed or quality?'",
                        "# Add pro arguments for speed",
                        "# Add con arguments for quality consideration",
                        "# Note: Full debate system integration coming soon"
                    ],
                    "success_criteria": [
                        "Understands debate system concepts",
                        "Can articulate pro/con arguments",
                        "Recognizes value of structured decisions",
                        "Understands consensus-building process"
                    ]
                }
            },
            "integration": {
                "title": "System Integration - Combined Intelligence",
                "duration": "15 minutes",
                "objectives": [
                    "Combine multiple systems effectively",
                    "Create efficient workflows",
                    "Maximize system synergies",
                    "Develop personal system usage patterns"
                ],
                "exercise": {
                    "title": "Workflow Integration Challenge",
                    "steps": [
                        "Use scanner to identify improvement area",
                        "Use planner to create improvement plan",
                        "Use task list to track progress",
                        "Document the integrated workflow"
                    ],
                    "commands": [
                        "# Step 1: Scan for issues",
                        "python tools/analytics/project_scanner.py --target scripts/ --format text",
                        "# Step 2: Plan improvements",
                        "python tools/cycle_planner/cycle_planner.py --create --name 'Improvement_Plan'",
                        "# Step 3: Track in task list",
                        "code MASTER_TASK_LIST.md",
                        "# Step 4: Document your workflow"
                    ],
                    "success_criteria": [
                        "Successfully combines multiple systems",
                        "Creates coherent improvement workflow",
                        "Documents process for future reference",
                        "Identifies at least 2 system synergies"
                    ]
                }
            }
        }

    def run_daily_training(self, day):
        """Run specific day of training program."""
        day_modules = {
            1: "scanner",
            2: "tasks",
            3: "planner",
            4: "debate",
            5: "integration"
        }

        if day not in day_modules:
            print(f"❌ Invalid day: {day}. Valid days: 1-5")
            return

        module_name = day_modules[day]
        self.run_module_training(module_name, day_context=f"Day {day}")

    def run_module_training(self, module_name, day_context=""):
        """Run training for a specific module."""
        if module_name not in self.training_modules:
            print(f"❌ Module '{module_name}' not found.")
            self.show_available_modules()
            return

        module = self.training_modules[module_name]

        print(f"\n🎓 {day_context} {module['title']}")
        print("=" * 60)
        print(f"⏱️  Duration: {module['duration']}")
        print(f"\n🎯 Learning Objectives:")
        for i, objective in enumerate(module['objectives'], 1):
            print(f"  {i}. {objective}")

        print(f"\n🛠️  Hands-On Exercise: {module['exercise']['title']}")
        print("\n📋 Steps:")
        for i, step in enumerate(module['exercise']['steps'], 1):
            print(f"  {i}. {step}")

        print("
💻 Commands to Run:"        for cmd in module['exercise']['commands']:
            if cmd.startswith('#'):
                print(f"  {cmd}")
            else:
                print(f"  $ {cmd}")

        print("
✅ Success Criteria:"        for i, criteria in enumerate(module['exercise']['success_criteria'], 1):
            print(f"  {i}. {criteria}")

        print("
🚀 Ready to begin? Follow the steps above!"        print("💡 Pro tip: Run commands in a separate terminal window"        print("📞 Need help? Check docs/systems/agent_system_portal.md"

        # Interactive mode
        if self._ask_to_run_commands():
            self._run_exercise_commands(module['exercise']['commands'])

    def show_available_modules(self):
        """Show all available training modules."""
        print("\n🎓 AVAILABLE TRAINING MODULES")
        print("=" * 40)

        for name, module in self.training_modules.items():
            print(f"📚 {name:<12} | {module['title']}")
            print(f"{'':<12}   Duration: {module['duration']}")

        print("
💡 Usage: python scripts/system_training.py --system <name>"        print("📅 Daily: python scripts/system_training.py --day <1-5>"

    def _ask_to_run_commands(self):
        """Ask user if they want to run commands interactively."""
        try:
            response = input("\n🤖 Would you like me to run the exercise commands for you? (y/N): ").strip().lower()
            return response in ['y', 'yes']
        except KeyboardInterrupt:
            print("\n👋 Training session ended.")
            return False

    def _run_exercise_commands(self, commands):
        """Run exercise commands interactively."""
        print("\n🚀 Running Exercise Commands...")
        print("=" * 40)

        for i, cmd in enumerate(commands, 1):
            print(f"\nStep {i}: {cmd}")

            if cmd.startswith('#'):
                print("💡 This is a manual step - follow the instructions above.")
                input("Press Enter to continue...")
                continue

            try:
                print(f"Executing: {cmd}")
                result = subprocess.run(cmd, shell=True, cwd=self.base_path, timeout=60)

                if result.returncode == 0:
                    print("✅ Command completed successfully")
                else:
                    print(f"⚠️ Command exited with code {result.returncode}")

            except subprocess.TimeoutExpired:
                print("⏱️ Command timed out - this is normal for interactive commands")
            except Exception as e:
                print(f"❌ Command failed: {e}")

            input("Press Enter to continue to next step...")

        print("\n🎉 Exercise completed! Review the success criteria above.")

    def show_training_program(self):
        """Show the complete 5-day training program."""
        print("\n🎓 AGENT SYSTEM TRAINING PROGRAM")
        print("=" * 50)
        print("5-Day comprehensive training to master all agent systems:")
        print()

        schedule = [
            (1, "Project Scanner", "Code Intelligence", "5 min"),
            (2, "Master Task Lists", "Coordination Intelligence", "2 min"),
            (3, "Cycle Planner", "Task Intelligence", "3 min"),
            (4, "Debate System", "Decision Intelligence", "10 min"),
            (5, "System Integration", "Combined Intelligence", "15 min")
        ]

        for day, system, focus, duration in schedule:
            print(f"📅 Day {day}: {system}")
            print(f"   🎯 Focus: {focus}")
            print(f"   ⏱️  Duration: {duration}")
            print()

        print("🚀 Start training: python scripts/system_training.py --day 1")
        print("📚 View portal: python scripts/system_launcher.py --system portal")
        print("🆘 Get help: python scripts/system_launcher.py --help")


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(
        description="Agent System Training Program",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/system_training.py --day 1
  python scripts/system_training.py --system scanner
  python scripts/system_training.py --program
  python scripts/system_training.py --interactive
        """
    )

    parser.add_argument("--day", "-d", type=int, choices=range(1, 6),
                       help="Run specific day of training program (1-5)")
    parser.add_argument("--system", "-s",
                       choices=["scanner", "tasks", "planner", "debate", "integration"],
                       help="Run training for specific system")
    parser.add_argument("--program", "-p", action="store_true",
                       help="Show complete 5-day training program")
    parser.add_argument("--modules", "-m", action="store_true",
                       help="List all available training modules")

    args = parser.parse_args()

    trainer = SystemTrainer()

    if args.day:
        trainer.run_daily_training(args.day)
    elif args.system:
        trainer.run_module_training(args.system)
    elif args.program:
        trainer.show_training_program()
    elif args.modules:
        trainer.show_available_modules()
    else:
        trainer.show_training_program()


if __name__ == "__main__":
    main()