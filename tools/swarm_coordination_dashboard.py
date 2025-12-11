#!/usr/bin/env python3
"""
🐝 Swarm Coordination Dashboard
A tool I wished I had - monitors parallel task execution across multiple agents

This tool provides real-time visibility into swarm coordination efforts by:
- Tracking delegated tasks across multiple agents
- Monitoring completion status via inbox messages
- Providing coordination status reports
- Alerting on blockers and dependencies

Usage:
    python tools/swarm_coordination_dashboard.py --init-session "WordPress Deployment"
    python tools/swarm_coordination_dashboard.py --status
    python tools/swarm_coordination_dashboard.py --agent Agent-3 --update "SFTP validation complete"
    python tools/swarm_coordination_dashboard.py --report
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Standalone file operations for tool compatibility
import sys
from pathlib import Path

class SwarmCoordinationDashboard:
    """Dashboard for tracking swarm coordination across multiple agents"""

    def __init__(self):
        self.dashboard_file = Path("agent_workspaces/Agent-8/swarm_coordination_dashboard.json")
        self._ensure_dashboard_exists()

    def _ensure_dashboard_exists(self):
        """Ensure dashboard file exists with proper structure"""
        if not self.dashboard_file.exists():
            initial_structure = {
                "active_sessions": {},
                "completed_sessions": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0.0"
                }
            }
            self._save_dashboard(initial_structure)

    def init_session(self, session_name: str, description: str = "") -> Dict:
        """Initialize a new coordination session"""
        dashboard = self._load_dashboard()

        if session_name in dashboard["active_sessions"]:
            raise ValueError(f"Session '{session_name}' already exists")

        session = {
            "name": session_name,
            "description": description,
            "created": datetime.now().isoformat(),
            "agents": {},
            "status": "active",
            "summary": {
                "total_tasks": 0,
                "completed_tasks": 0,
                "blocked_tasks": 0,
                "progress_percentage": 0
            }
        }

        dashboard["active_sessions"][session_name] = session
        self._save_dashboard(dashboard)

        return session

    def add_agent_task(self, session_name: str, agent_id: str, task: str, priority: str = "normal") -> bool:
        """Add a task assignment for a specific agent"""
        dashboard = self._load_dashboard()

        if session_name not in dashboard["active_sessions"]:
            raise ValueError(f"Session '{session_name}' not found")

        session = dashboard["active_sessions"][session_name]

        if agent_id not in session["agents"]:
            session["agents"][agent_id] = {
                "tasks": [],
                "status": "active"
            }

        agent_task = {
            "task": task,
            "priority": priority,
            "assigned": datetime.now().isoformat(),
            "status": "assigned",
            "updates": []
        }

        session["agents"][agent_id]["tasks"].append(agent_task)
        session["summary"]["total_tasks"] += 1

        self._update_progress(session)
        self._save_dashboard(dashboard)

        return True

    def update_task_status(self, session_name: str, agent_id: str, task_index: int, status: str, note: str = "") -> bool:
        """Update the status of a specific task"""
        dashboard = self._load_dashboard()

        if session_name not in dashboard["active_sessions"]:
            raise ValueError(f"Session '{session_name}' not found")

        session = dashboard["active_sessions"][session_name]

        if agent_id not in session["agents"]:
            raise ValueError(f"Agent '{agent_id}' not found in session")

        tasks = session["agents"][agent_id]["tasks"]
        if task_index >= len(tasks):
            raise ValueError(f"Task index {task_index} out of range")

        task = tasks[task_index]

        # Record status change
        update = {
            "timestamp": datetime.now().isoformat(),
            "old_status": task["status"],
            "new_status": status,
            "note": note
        }
        task["updates"].append(update)
        task["status"] = status

        # Update summary counters
        if status == "completed":
            session["summary"]["completed_tasks"] += 1
        elif status == "blocked":
            session["summary"]["blocked_tasks"] += 1

        self._update_progress(session)
        self._save_dashboard(dashboard)

        return True

    def get_session_status(self, session_name: str) -> Optional[Dict]:
        """Get detailed status of a coordination session"""
        dashboard = self._load_dashboard()

        if session_name not in dashboard["active_sessions"]:
            return None

        return dashboard["active_sessions"][session_name]

    def get_all_active_sessions(self) -> Dict:
        """Get overview of all active coordination sessions"""
        dashboard = self._load_dashboard()
        return dashboard["active_sessions"]

    def complete_session(self, session_name: str) -> bool:
        """Mark a session as completed and archive it"""
        dashboard = self._load_dashboard()

        if session_name not in dashboard["active_sessions"]:
            raise ValueError(f"Session '{session_name}' not found")

        session = dashboard["active_sessions"][session_name]
        session["completed"] = datetime.now().isoformat()
        session["status"] = "completed"

        # Move to completed sessions
        dashboard["completed_sessions"][session_name] = session
        del dashboard["active_sessions"][session_name]

        self._save_dashboard(dashboard)
        return True

    def generate_report(self, session_name: Optional[str] = None) -> str:
        """Generate a formatted status report"""
        if session_name:
            session = self.get_session_status(session_name)
            if not session:
                return f"Session '{session_name}' not found"

            return self._format_session_report(session_name, session)
        else:
            sessions = self.get_all_active_sessions()
            if not sessions:
                return "No active coordination sessions"

            report = "# 🐝 Swarm Coordination Dashboard Report\n\n"
            report += f"**Active Sessions:** {len(sessions)}\n\n"

            for name, session in sessions.items():
                report += self._format_session_report(name, session)
                report += "\n---\n\n"

            return report

    def _format_session_report(self, name: str, session: Dict) -> str:
        """Format a single session report"""
        report = f"## Session: {name}\n"
        report += f"**Description:** {session.get('description', 'N/A')}\n"
        report += f"**Created:** {session['created'][:19]}\n"
        report += f"**Progress:** {session['summary']['progress_percentage']}%\n"
        report += f"**Tasks:** {session['summary']['completed_tasks']}/{session['summary']['total_tasks']} completed"

        if session['summary']['blocked_tasks'] > 0:
            report += f" ({session['summary']['blocked_tasks']} blocked)"

        report += "\n\n### Agent Assignments:\n"

        for agent_id, agent_data in session["agents"].items():
            report += f"**{agent_id}:**\n"
            for i, task in enumerate(agent_data["tasks"]):
                status_icon = {"assigned": "⏳", "in_progress": "🔄", "completed": "✅", "blocked": "❌"}.get(task["status"], "❓")
                report += f"  {status_icon} Task {i+1}: {task['task'][:60]}{'...' if len(task['task']) > 60 else ''}\n"
                if task["status"] == "blocked" and task["updates"]:
                    latest_update = task["updates"][-1]
                    report += f"    *Blocked: {latest_update.get('note', 'No details')}*\n"
            report += "\n"

        return report

    def _load_dashboard(self) -> Dict:
        """Load dashboard data from file"""
        try:
            with open(self.dashboard_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "active_sessions": {},
                "completed_sessions": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0.0"
                }
            }

    def _save_dashboard(self, dashboard: Dict):
        """Save dashboard data to file"""
        self.dashboard_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)

    def _update_progress(self, session: Dict):
        """Update progress percentage for a session"""
        total = session["summary"]["total_tasks"]
        completed = session["summary"]["completed_tasks"]

        if total > 0:
            session["summary"]["progress_percentage"] = round((completed / total) * 100, 1)
        else:
            session["summary"]["progress_percentage"] = 0


def main():
    """CLI interface for the Swarm Coordination Dashboard"""
    import argparse

    parser = argparse.ArgumentParser(description="🐝 Swarm Coordination Dashboard")
    parser.add_argument("--init-session", help="Initialize new coordination session")
    parser.add_argument("--description", help="Session description")
    parser.add_argument("--add-task", help="Add task for agent (format: agent_id:task)")
    parser.add_argument("--priority", default="normal", choices=["normal", "urgent", "critical"])
    parser.add_argument("--update", help="Update task status (format: agent_id:task_index:status:note)")
    parser.add_argument("--session", default="default", help="Session name")
    parser.add_argument("--status", action="store_true", help="Show session status")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--complete", action="store_true", help="Mark session as complete")

    args = parser.parse_args()

    dashboard = SwarmCoordinationDashboard()

    try:
        if args.init_session:
            session = dashboard.init_session(args.init_session, args.description or "")
            print(f"✅ Initialized session '{args.init_session}'")
            print(f"Description: {session.get('description', 'N/A')}")

        elif args.add_task:
            agent_id, task = args.add_task.split(":", 1)
            dashboard.add_agent_task(args.session, agent_id, task, args.priority)
            print(f"✅ Added task for {agent_id}: {task}")

        elif args.update:
            parts = args.update.split(":", 3)
            if len(parts) < 3:
                print("❌ Format: agent_id:task_index:status:note")
                return
            agent_id, task_index, status, note = parts[0], int(parts[1]), parts[2], parts[3] if len(parts) > 3 else ""
            dashboard.update_task_status(args.session, agent_id, task_index, status, note)
            print(f"✅ Updated {agent_id} task {task_index} to {status}")

        elif args.status:
            session = dashboard.get_session_status(args.session)
            if session:
                print(dashboard._format_session_report(args.session, session))
            else:
                print(f"❌ Session '{args.session}' not found")

        elif args.report:
            print(dashboard.generate_report())

        elif args.complete:
            dashboard.complete_session(args.session)
            print(f"✅ Completed session '{args.session}'")

        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
