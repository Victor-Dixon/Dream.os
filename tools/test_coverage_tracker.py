#!/usr/bin/env python3
"""
Test Coverage Tracker - Productivity Tool
==========================================

Tracks test coverage progress for assigned files.
Helps agents monitor test creation progress and identify gaps.

V2 Compliance: <400 lines, single responsibility
Created: 2025-11-27
Author: Agent-8 (SSOT & System Integration Specialist)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class TestCoverageStatus:
    """Test coverage status for a file."""
    source_file: str
    test_file: Optional[str]
    status: str  # "PENDING", "IN_PROGRESS", "COMPLETE"
    priority: str  # "HIGH", "MEDIUM", "LOW"
    test_count: int = 0
    notes: str = ""


class TestCoverageTracker:
    """Tracks test coverage progress for assigned files."""

    def __init__(self, agent_id: str, workspace_path: Optional[str] = None):
        """Initialize tracker for an agent."""
        self.agent_id = agent_id
        self.workspace_path = workspace_path or f"agent_workspaces/{agent_id}"
        self.status_file = Path(self.workspace_path) / "test_coverage_status.json"
        self.statuses: Dict[str, TestCoverageStatus] = {}

    def load_status(self) -> None:
        """Load test coverage status from file."""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                data = json.load(f)
                self.statuses = {
                    k: TestCoverageStatus(**v)
                    for k, v in data.items()
                }

    def save_status(self) -> None:
        """Save test coverage status to file."""
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.status_file, 'w') as f:
            data = {
                k: asdict(v)
                for k, v in self.statuses.items()
            }
            json.dump(data, f, indent=2)

    def add_file(self, source_file: str, priority: str = "MEDIUM") -> None:
        """Add a file to track."""
        if source_file not in self.statuses:
            self.statuses[source_file] = TestCoverageStatus(
                source_file=source_file,
                test_file=None,
                status="PENDING",
                priority=priority
            )

    def update_status(
        self,
        source_file: str,
        test_file: Optional[str] = None,
        status: Optional[str] = None,
        test_count: Optional[int] = None,
        notes: Optional[str] = None
    ) -> None:
        """Update status for a file."""
        if source_file not in self.statuses:
            self.add_file(source_file)

        status_obj = self.statuses[source_file]
        if test_file:
            status_obj.test_file = test_file
        if status:
            status_obj.status = status
        if test_count is not None:
            status_obj.test_count = test_count
        if notes:
            status_obj.notes = notes

    def get_progress(self) -> Dict[str, int]:
        """Get progress statistics."""
        total = len(self.statuses)
        complete = sum(1 for s in self.statuses.values() if s.status == "COMPLETE")
        in_progress = sum(1 for s in self.statuses.values() if s.status == "IN_PROGRESS")
        pending = sum(1 for s in self.statuses.values() if s.status == "PENDING")

        high_priority = sum(1 for s in self.statuses.values() if s.priority == "HIGH")
        high_complete = sum(
            1 for s in self.statuses.values()
            if s.priority == "HIGH" and s.status == "COMPLETE"
        )

        medium_priority = sum(1 for s in self.statuses.values() if s.priority == "MEDIUM")
        medium_complete = sum(
            1 for s in self.statuses.values()
            if s.priority == "MEDIUM" and s.status == "COMPLETE"
        )

        return {
            "total": total,
            "complete": complete,
            "in_progress": in_progress,
            "pending": pending,
            "high_priority": high_priority,
            "high_complete": high_complete,
            "medium_priority": medium_priority,
            "medium_complete": medium_complete,
            "completion_percentage": (complete / total * 100) if total > 0 else 0
        }

    def generate_report(self) -> str:
        """Generate a progress report."""
        progress = self.get_progress()
        report = f"""
# Test Coverage Progress - {self.agent_id}

**Total Files**: {progress['total']}
**Complete**: {progress['complete']} ({progress['completion_percentage']:.1f}%)
**In Progress**: {progress['in_progress']}
**Pending**: {progress['pending']}

## Priority Breakdown

**HIGH PRIORITY**: {progress['high_complete']}/{progress['high_priority']} complete
**MEDIUM PRIORITY**: {progress['medium_complete']}/{progress['medium_priority']} complete

## Status by File

"""
        for source_file, status in sorted(self.statuses.items()):
            test_file_str = status.test_file or "Not created"
            report += f"- **{source_file}** ({status.priority}): {status.status}\n"
            report += f"  - Test file: {test_file_str}\n"
            if status.test_count > 0:
                report += f"  - Tests: {status.test_count}\n"
            if status.notes:
                report += f"  - Notes: {status.notes}\n"
            report += "\n"

        return report


def main():
    """CLI interface for test coverage tracker."""
    import argparse

    parser = argparse.ArgumentParser(description="Track test coverage progress")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-8)")
    parser.add_argument("--add", help="Add source file to track")
    parser.add_argument("--priority", choices=["HIGH", "MEDIUM", "LOW"], default="MEDIUM")
    parser.add_argument("--update", help="Update status for source file")
    parser.add_argument("--test-file", help="Test file path")
    parser.add_argument("--status", choices=["PENDING", "IN_PROGRESS", "COMPLETE"])
    parser.add_argument("--test-count", type=int, help="Number of tests")
    parser.add_argument("--notes", help="Notes about the file")
    parser.add_argument("--report", action="store_true", help="Generate progress report")
    parser.add_argument("--workspace", help="Workspace path (default: agent_workspaces/{agent})")

    args = parser.parse_args()

    tracker = TestCoverageTracker(args.agent, args.workspace)
    tracker.load_status()

    if args.add:
        tracker.add_file(args.add, args.priority)
        print(f"✅ Added {args.add} to tracking")

    if args.update:
        tracker.update_status(
            args.update,
            test_file=args.test_file,
            status=args.status,
            test_count=args.test_count,
            notes=args.notes
        )
        print(f"✅ Updated {args.update}")

    if args.report:
        print(tracker.generate_report())

    tracker.save_status()


if __name__ == "__main__":
    main()



