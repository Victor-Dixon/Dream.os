#!/usr/bin/env python3
"""
Coordination Status Checker Utility
A simple tool to check agent coordination status and pending tasks.
Created as closure improvement for session 2026-01-11.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class CoordinationStatusChecker:
    """Utility for checking agent coordination and task status."""

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = Path(repo_root or os.getcwd())

    def check_passdown_status(self) -> Dict[str, any]:
        """Check the current passdown.json status."""
        passdown_path = self.repo_root / "passdown.json"
        if not passdown_path.exists():
            return {"status": "missing", "error": "passdown.json not found"}

        try:
            with open(passdown_path, 'r') as f:
                data = json.load(f)
            return {
                "status": "present",
                "agent": data.get("agent", "unknown"),
                "session": data.get("session_completed", "unknown"),
                "timestamp": data.get("timestamp", "unknown")
            }
        except json.JSONDecodeError as e:
            return {"status": "invalid", "error": f"JSON parse error: {e}"}

    def check_pending_tasks(self) -> List[str]:
        """Check for common pending task indicators."""
        pending_indicators = []

        # Check for TODO/FIXME in recent files
        todo_files = []
        for py_file in self.repo_root.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    if "TODO" in content or "FIXME" in content:
                        todo_files.append(str(py_file.relative_to(self.repo_root)))
            except:
                continue

        if todo_files:
            pending_indicators.append(f"Found TODO/FIXME in {len(todo_files)} files")

        # Check for unstaged changes
        git_status = os.popen("git status --porcelain").read()
        if git_status.strip():
            pending_indicators.append("Uncommitted changes in working directory")

        return pending_indicators

    def get_coordination_summary(self) -> Dict[str, any]:
        """Get a summary of coordination status."""
        return {
            "passdown": self.check_passdown_status(),
            "pending_tasks": self.check_pending_tasks(),
            "repo_root": str(self.repo_root)
        }


def main():
    """Main entry point."""
    checker = CoordinationStatusChecker()
    summary = checker.get_coordination_summary()

    print("🤖 Agent Coordination Status Check")
    print("=" * 40)

    print(f"📁 Repository: {summary['repo_root']}")

    passdown = summary['passdown']
    print(f"📋 Passdown Status: {passdown['status']}")
    if passdown['status'] == 'present':
        print(f"   Agent: {passdown['agent']}")
        print(f"   Session: {passdown['session']}")
        print(f"   Timestamp: {passdown['timestamp']}")

    pending = summary['pending_tasks']
    print(f"⏳ Pending Tasks: {len(pending)}")
    for task in pending:
        print(f"   • {task}")

    if not pending and passdown['status'] == 'present':
        print("✅ Coordination status: Ready for next session")
    else:
        print("⚠️  Coordination status: Items need attention")


if __name__ == "__main__":
    main()