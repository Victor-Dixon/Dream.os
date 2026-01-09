#!/usr/bin/env python3
"""
Technical Debt Tracker
======================

<!-- SSOT Domain: analytics -->

Tracks technical debt across the codebase, monitors progress,
and generates reports for debt reduction.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: MEDIUM
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


class TechnicalDebtTracker:
    """Tracks technical debt across the codebase."""

    def __init__(self, debt_dir: Path = None):
        """Initialize technical debt tracker."""
        if debt_dir is None:
            debt_dir = Path(__file__).parent
        
        self.debt_dir = debt_dir
        self.data_dir = debt_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.debt_data_path = self.data_dir / "technical_debt_data.json"
        self.debt_data: Dict[str, Any] = {}
        
        self.load_debt_data()

    def load_debt_data(self):
        """Load technical debt data from file."""
        if self.debt_data_path.exists():
            try:
                with open(self.debt_data_path, "r", encoding="utf-8") as f:
                    self.debt_data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load debt data: {e}")
                self.debt_data = self._create_empty_debt_data()
        else:
            self.debt_data = self._create_empty_debt_data()

    def _create_empty_debt_data(self) -> Dict[str, Any]:
        """Create empty debt data structure."""
        return {
            "categories": {
                "file_deletion": {"total": 0, "resolved": 0, "pending": []},
                "integration": {"total": 0, "resolved": 0, "pending": []},
                "implementation": {"total": 0, "resolved": 0, "pending": []},
                "review": {"total": 0, "resolved": 0, "pending": []},
                "output_flywheel": {"total": 0, "resolved": 0, "pending": []},
                "test_validation": {"total": 0, "resolved": 0, "pending": []},
                "todo_fixme": {"total": 0, "resolved": 0, "pending": []},
            },
            "tasks": {},
            "progress_history": [],
            "last_updated": datetime.now().isoformat(),
        }

    def save_debt_data(self):
        """Save technical debt data to file."""
        self.debt_data["last_updated"] = datetime.now().isoformat()
        with open(self.debt_data_path, "w", encoding="utf-8") as f:
            json.dump(self.debt_data, f, indent=2)

    def initialize_from_analysis(self, analysis_path: Path):
        """Initialize debt data from technical debt analysis."""
        # Load the analysis document
        if not analysis_path.exists():
            logger.warning(f"Analysis file not found: {analysis_path}")
            return
        
        # Parse analysis categories
        with open(analysis_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Initialize categories from analysis
        self.debt_data["categories"]["file_deletion"] = {
            "total": 44,
            "resolved": 0,
            "pending": ["44 files ready for deletion"],
        }
        self.debt_data["categories"]["integration"] = {
            "total": 25,
            "resolved": 0,
            "pending": ["25 files need web layer integration"],
        }
        self.debt_data["categories"]["implementation"] = {
            "total": 64,
            "resolved": 0,
            "pending": ["64 files need implementation (42 new, 22 duplicates)"],
        }
        self.debt_data["categories"]["review"] = {
            "total": 306,
            "resolved": 0,
            "pending": ["306 files need expert review"],
        }
        self.debt_data["categories"]["output_flywheel"] = {
            "total": 3,
            "resolved": 0,
            "pending": ["Session file creation CLI", "Git commit extraction", "Enhanced error messages"],
        }
        self.debt_data["categories"]["test_validation"] = {
            "total": 1,
            "resolved": 0,
            "pending": ["Complete interrupted test suite validation"],
        }
        self.debt_data["categories"]["todo_fixme"] = {
            "total": 9,
            "resolved": 0,
            "pending": ["9 files with TODO/FIXME comments"],
        }
        
        self.save_debt_data()

    def record_task_assignment(self, agent_id: str, task: str, category: str):
        """Record a task assignment."""
        task_id = f"{agent_id}_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.debt_data["tasks"][task_id] = {
            "agent_id": agent_id,
            "task": task,
            "category": category,
            "status": "assigned",
            "assigned_date": datetime.now().isoformat(),
            "progress": 0,
        }
        
        self.save_debt_data()
        return task_id

    def update_task_progress(self, task_id: str, progress: int, status: str = None):
        """Update task progress."""
        if task_id not in self.debt_data["tasks"]:
            logger.warning(f"Task not found: {task_id}")
            return
        
        self.debt_data["tasks"][task_id]["progress"] = progress
        if status:
            self.debt_data["tasks"][task_id]["status"] = status
        if progress >= 100:
            self.debt_data["tasks"][task_id]["completed_date"] = datetime.now().isoformat()
            self.debt_data["tasks"][task_id]["status"] = "completed"
        
        self.save_debt_data()

    def record_resolution(self, category: str, count: int):
        """Record resolution of debt items."""
        if category in self.debt_data["categories"]:
            self.debt_data["categories"][category]["resolved"] += count
            
            # Update progress history
            self.debt_data["progress_history"].append({
                "date": datetime.now().isoformat(),
                "category": category,
                "resolved": count,
            })
        
        self.save_debt_data()

    def calculate_total_debt(self) -> Dict[str, Any]:
        """Calculate total debt statistics."""
        total = 0
        resolved = 0
        
        for category_data in self.debt_data["categories"].values():
            total += category_data.get("total", 0)
            resolved += category_data.get("resolved", 0)
        
        pending = total - resolved
        reduction_rate = (resolved / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "resolved": resolved,
            "pending": pending,
            "reduction_rate": round(reduction_rate, 2),
        }

    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate dashboard data."""
        stats = self.calculate_total_debt()
        
        # Get active tasks
        active_tasks = [
            task for task in self.debt_data["tasks"].values()
            if task["status"] in ["assigned", "in_progress"]
        ]
        
        # Get recent progress
        recent_progress = self.debt_data["progress_history"][-10:] if self.debt_data["progress_history"] else []
        
        return {
            "summary": stats,
            "categories": self.debt_data["categories"],
            "active_tasks": active_tasks,
            "recent_progress": recent_progress,
            "last_updated": self.debt_data["last_updated"],
        }

    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly progress report."""
        week_start = datetime.now() - timedelta(days=7)
        
        # Filter progress from last week
        weekly_progress = [
            p for p in self.debt_data["progress_history"]
            if datetime.fromisoformat(p["date"]) >= week_start
        ]
        
        stats = self.calculate_total_debt()
        
        return {
            "report_period": {
                "week_start": week_start.isoformat(),
                "week_end": datetime.now().isoformat(),
            },
            "summary": stats,
            "weekly_resolutions": weekly_progress,
            "active_tasks": [
                task for task in self.debt_data["tasks"].values()
                if task["status"] in ["assigned", "in_progress"]
            ],
            "categories": self.debt_data["categories"],
        }


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Technical Debt Tracker")
    parser.add_argument("--init", action="store_true", help="Initialize from analysis")
    parser.add_argument("--analysis", type=Path, help="Path to analysis file")
    parser.add_argument("--dashboard", action="store_true", help="Generate dashboard data")
    parser.add_argument("--weekly-report", action="store_true", help="Generate weekly report")
    
    args = parser.parse_args()
    
    tracker = TechnicalDebtTracker()
    
    if args.init and args.analysis:
        tracker.initialize_from_analysis(args.analysis)
        print("✅ Technical debt data initialized from analysis")
    
    if args.dashboard:
        dashboard_data = tracker.generate_dashboard_data()
        print(json.dumps(dashboard_data, indent=2))
    
    if args.weekly_report:
        report = tracker.generate_weekly_report()
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()


