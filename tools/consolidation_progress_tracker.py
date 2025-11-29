#!/usr/bin/env python3
"""
Consolidation Progress Tracker
==============================

Tracks and reports GitHub consolidation progress for assigned agents.
Provides real-time status, blocker identification, and next action recommendations.

V2 Compliant: <400 lines
Author: Agent-7 (Web Development Specialist)
Date: 2025-01-27
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class ConsolidationProgressTracker:
    """Track consolidation progress for assigned repos."""

    def __init__(self, agent_id: str, assignment_file: Optional[Path] = None):
        """Initialize tracker.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            assignment_file: Path to consolidation assignment file
        """
        self.agent_id = agent_id
        self.workspace = project_root / "agent_workspaces" / agent_id
        self.consolidation_logs = project_root / "consolidation_logs"
        self.consolidation_logs.mkdir(parents=True, exist_ok=True)
        
        # Load assignment from distribution file
        if assignment_file is None:
            assignment_file = project_root / "agent_workspaces" / "Agent-4" / "CONSOLIDATION_WORK_DISTRIBUTION.md"
        
        self.assignment = self._load_assignment(assignment_file)
        self.progress_file = self.workspace / "consolidation_progress.json"
        self.progress = self._load_progress()

    def _load_assignment(self, assignment_file: Path) -> Dict:
        """Load assignment from distribution file."""
        if not assignment_file.exists():
            return {}
        
        # Parse markdown to extract agent assignments
        content = assignment_file.read_text()
        agent_section = None
        in_agent_section = False
        
        for line in content.split('\n'):
            if f"### **{self.agent_id}" in line:
                in_agent_section = True
                agent_section = {"tasks": []}
            elif in_agent_section and line.startswith("###"):
                break
            elif in_agent_section and "- Merge" in line:
                # Extract merge info: Merge `source` (Repo #X) → `target` (Repo #Y)
                parts = line.split("→")
                if len(parts) == 2:
                    source_part = parts[0].split("`")[1] if "`" in parts[0] else ""
                    target_part = parts[1].split("`")[1] if "`" in parts[1] else ""
                    agent_section["tasks"].append({
                        "source": source_part,
                        "target": target_part,
                        "status": "pending"
                    })
        
        return agent_section or {}

    def _load_progress(self) -> Dict:
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "agent_id": self.agent_id,
            "last_updated": datetime.now().isoformat(),
            "tasks": [],
            "blockers": [],
            "completed": 0,
            "total": 0
        }

    def _save_progress(self):
        """Save progress to file."""
        self.progress["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def scan_consolidation_logs(self) -> List[Dict]:
        """Scan consolidation logs for completed merges."""
        completed = []
        log_dir = self.consolidation_logs / "merge_Dadudekc"
        
        if not log_dir.exists():
            return completed
        
        for log_file in log_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    if log_data.get("status") == "success":
                        completed.append({
                            "source": log_data.get("source_repo", ""),
                            "target": log_data.get("target_repo", ""),
                            "timestamp": log_data.get("timestamp", ""),
                            "log_file": str(log_file)
                        })
            except Exception:
                continue
        
        return completed

    def update_progress(self):
        """Update progress from logs and status."""
        completed_merges = self.scan_consolidation_logs()
        
        # Update task status
        tasks = self.assignment.get("tasks", [])
        for task in tasks:
            source = task.get("source", "")
            for completed in completed_merges:
                if source in completed.get("source", ""):
                    task["status"] = "completed"
                    break
        
        self.progress["tasks"] = tasks
        self.progress["completed"] = sum(1 for t in tasks if t.get("status") == "completed")
        self.progress["total"] = len(tasks)
        self._save_progress()

    def get_status_report(self) -> Dict:
        """Generate status report."""
        self.update_progress()
        
        pending = [t for t in self.progress["tasks"] if t.get("status") != "completed"]
        completed = [t for t in self.progress["tasks"] if t.get("status") == "completed"]
        
        return {
            "agent": self.agent_id,
            "progress": f"{self.progress['completed']}/{self.progress['total']}",
            "percentage": (self.progress['completed'] / self.progress['total'] * 100) if self.progress['total'] > 0 else 0,
            "completed": completed,
            "pending": pending,
            "blockers": self.progress.get("blockers", []),
            "last_updated": self.progress["last_updated"]
        }

    def print_report(self):
        """Print formatted status report."""
        report = self.get_status_report()
        
        print("=" * 60)
        print(f"📊 CONSOLIDATION PROGRESS - {self.agent_id}")
        print("=" * 60)
        print(f"\nProgress: {report['progress']} ({report['percentage']:.1f}%)")
        
        if report['completed']:
            print(f"\n✅ Completed ({len(report['completed'])}):")
            for task in report['completed']:
                print(f"   - {task.get('source')} → {task.get('target')}")
        
        if report['pending']:
            print(f"\n⏳ Pending ({len(report['pending'])}):")
            for task in report['pending']:
                print(f"   - {task.get('source')} → {task.get('target')}")
        
        if report['blockers']:
            print(f"\n🚨 Blockers ({len(report['blockers'])}):")
            for blocker in report['blockers']:
                print(f"   - {blocker}")
        
        print(f"\nLast Updated: {report['last_updated']}")
        print("=" * 60)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Track consolidation progress for assigned agent"
    )
    parser.add_argument(
        "--agent",
        default="Agent-7",
        help="Agent ID (default: Agent-7)"
    )
    parser.add_argument(
        "--assignment",
        type=Path,
        help="Path to consolidation assignment file"
    )
    
    args = parser.parse_args()
    
    tracker = ConsolidationProgressTracker(args.agent, args.assignment)
    tracker.print_report()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

