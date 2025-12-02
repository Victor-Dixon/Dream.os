#!/usr/bin/env python3
"""
Technical Debt Auto-Task Assigner
==================================

Automatically assigns tasks from weekly technical debt reports to agents
via the messaging system and tracks them in agent status.json files.

This creates a continuous loop: Report → Tasks → Messaging → Status → Work

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-02
Priority: HIGH
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TechnicalDebtAutoAssigner:
    """Automatically assigns technical debt tasks to agents."""

    # Agent specializations for task matching
    AGENT_SPECIALIZATIONS = {
        "Agent-1": {
            "name": "Integration & Core Systems",
            "categories": ["integration", "core", "coordination", "messaging", "system"],
            "keywords": ["integration", "core", "coordination", "messaging", "system", "service"]
        },
        "Agent-2": {
            "name": "Architecture & Design",
            "categories": ["architecture", "design", "duplicate", "review", "pattern"],
            "keywords": ["architecture", "design", "duplicate", "review", "pattern", "manager"]
        },
        "Agent-3": {
            "name": "Infrastructure & DevOps",
            "categories": ["infrastructure", "devops", "test", "validation", "deployment"],
            "keywords": ["infrastructure", "test", "validation", "deployment", "devops", "ci/cd"]
        },
        "Agent-7": {
            "name": "Web Development",
            "categories": ["web", "frontend", "api", "integration", "wiring", "discord"],
            "keywords": ["web", "frontend", "api", "integration", "wiring", "discord", "controller"]
        },
        "Agent-8": {
            "name": "SSOT & System Integration",
            "categories": ["ssot", "system", "integration", "metrics", "unified"],
            "keywords": ["ssot", "system", "integration", "metrics", "unified", "consolidation"]
        }
    }

    def __init__(self, report_path: Optional[Path] = None):
        """Initialize auto-assigner."""
        self.project_root = project_root
        self.reports_dir = project_root / "systems" / "technical_debt" / "reports"
        
        if report_path:
            self.report_path = Path(report_path)
        else:
            # Find most recent report
            self.report_path = self._find_latest_report()
        
        self.agent_workspaces = project_root / "agent_workspaces"

    def _find_latest_report(self) -> Optional[Path]:
        """Find the most recent report (daily or weekly)."""
        if not self.reports_dir.exists():
            return None
        
        # Try daily reports first (2x daily - more frequent)
        daily_reports = sorted(
            self.reports_dir.glob("daily_report_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if daily_reports:
            logger.info(f"Using latest daily report: {daily_reports[0].name}")
            return daily_reports[0]
        
        # Fallback to weekly reports
        weekly_reports = sorted(
            self.reports_dir.glob("weekly_report_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if weekly_reports:
            logger.info(f"Using latest weekly report: {weekly_reports[0].name}")
            return weekly_reports[0]
        
        logger.warning("No technical debt reports found (daily or weekly).")
        return None

    def _load_report(self) -> Dict[str, Any]:
        """Load weekly technical debt report."""
        if not self.report_path or not self.report_path.exists():
            return {}
        
        try:
            with open(self.report_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading report: {e}")
            return {}

    def _extract_actionable_tasks(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract actionable tasks from report."""
        tasks = []
        
        # Extract from categories
        categories = report.get("categories", {})
        
        for category_name, category_data in categories.items():
            # Handle pending as int or list
            pending_raw = category_data.get("pending", 0)
            if isinstance(pending_raw, list):
                pending = len(pending_raw) if pending_raw else 0
            else:
                pending = int(pending_raw) if pending_raw else 0
            
            status = category_data.get("status", "")
            
            # Only extract if there are pending items and not blocked
            if pending > 0 and "BLOCKED" not in status:
                task = {
                    "category": category_name,
                    "pending": pending,
                    "total": category_data.get("total", 0),
                    "status": status,
                    "priority": self._determine_priority(category_name, status),
                    "description": self._generate_task_description(category_name, category_data)
                }
                tasks.append(task)
        
        return tasks

    def _determine_priority(self, category: str, status: str) -> str:
        """Determine task priority based on category and status."""
        # Critical categories
        if category in ["File Deletion", "Test Validation"]:
            return "urgent"
        
        # High priority categories
        if category in ["Integration", "Implementation"]:
            return "urgent"
        
        # Medium priority
        if "ASSIGNED" in status or "ACTIVE" in status:
            return "normal"
        
        return "normal"

    def _generate_task_description(self, category: str, category_data: Dict[str, Any]) -> str:
        """Generate task description from category data."""
        pending = category_data.get("pending", 0)
        total = category_data.get("total", 0)
        status = category_data.get("status", "")
        
        description = f"📊 Technical Debt Task: {category}\n\n"
        description += f"**Status**: {status}\n"
        description += f"**Pending**: {pending} items\n"
        description += f"**Total**: {total} items\n"
        description += f"**Progress**: {category_data.get('progress', 0):.1f}%\n\n"
        
        # Add category-specific instructions
        if category == "File Deletion":
            description += "**Action**: Execute safe file deletion after test validation.\n"
        elif category == "Integration":
            description += "**Action**: Wire up integration points, connect to web layer.\n"
        elif category == "Implementation":
            description += "**Action**: Complete implementation of placeholder files.\n"
        elif category == "Review":
            description += "**Action**: Review files, categorize, and decide on action.\n"
        elif category == "Technical Debt Markers":
            description += "**Action**: Resolve TODO/FIXME/BUG markers in code.\n"
        
        description += "\n🐝 **WE. ARE. SWARM. ⚡🔥**"
        
        return description

    def _find_best_agent(self, task: Dict[str, Any]) -> str:
        """Find best agent for task based on specializations."""
        category = task["category"].lower()
        description = task["description"].lower()
        
        agent_scores = {}
        
        for agent_id, spec in self.AGENT_SPECIALIZATIONS.items():
            score = 0
            
            # Check category matches
            for cat in spec["categories"]:
                if cat in category:
                    score += 3
            
            # Check description matches
            for keyword in spec["keywords"]:
                if keyword in description:
                    score += 1
            
            agent_scores[agent_id] = score
        
        # Return agent with highest score, or Agent-1 as default
        if agent_scores:
            best_agent = max(agent_scores, key=agent_scores.get)
            if agent_scores[best_agent] > 0:
                return best_agent
        
        return "Agent-1"  # Default coordinator

    def _check_agent_availability(self, agent_id: str) -> tuple[bool, str]:
        """Check if agent is available (not blocked, has capacity)."""
        status_file = self.agent_workspaces / agent_id / "status.json"
        
        if not status_file.exists():
            return True, "no status file"  # Assume available if no status file
        
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                status = json.load(f)
            
            # Check if agent is blocked
            if status.get("status") == "BLOCKED":
                return False, "blocked"
            
            # Check current tasks count (limit to 5 active tasks - more lenient)
            current_tasks = status.get("current_tasks", [])
            task_count = len(current_tasks)
            if task_count >= 5:
                return False, f"{task_count} tasks (max 5)"
            
            # Agent is available
            return True, f"available ({task_count} tasks)"
        except Exception as e:
            return True, f"error checking: {e}"  # Assume available on error

    def _send_task_via_messaging(self, agent_id: str, task: Dict[str, Any]) -> bool:
        """Send task to agent via messaging CLI."""
        message = task["description"]
        priority = task["priority"]
        
        cmd = [
            sys.executable, "-m", "src.services.messaging_cli",
            "--agent", agent_id,
            "--message", message,
            "--priority", priority
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Task assigned to {agent_id}: {task['category']}")
                return True
            else:
                print(f"❌ Failed to assign task to {agent_id}: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error assigning task to {agent_id}: {e}")
            return False

    def _update_agent_status(self, agent_id: str, task: Dict[str, Any]) -> bool:
        """Update agent status.json with new task."""
        status_file = self.agent_workspaces / agent_id / "status.json"
        
        if not status_file.exists():
            return False
        
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                status = json.load(f)
            
            # Add task to current_tasks
            if "current_tasks" not in status:
                status["current_tasks"] = []
            
            task_entry = f"Technical Debt - {task['category']}: {task['pending']} items pending ({task['status']})"
            
            # Avoid duplicates
            if task_entry not in status["current_tasks"]:
                status["current_tasks"].append(task_entry)
            
            # Update last_updated
            status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update mission if needed
            if "Technical Debt" not in status.get("current_mission", ""):
                if status.get("current_mission"):
                    status["current_mission"] += " + Technical Debt Coordination"
                else:
                    status["current_mission"] = "Technical Debt Coordination"
            
            # Save updated status
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status, f, indent=2)
            
            return True
        except Exception as e:
            print(f"⚠️ Error updating status for {agent_id}: {e}")
            return False

    def assign_tasks_from_report(self, dry_run: bool = False) -> Dict[str, Any]:
        """Assign tasks from weekly report to agents."""
        print("🔍 Loading weekly technical debt report...")
        report = self._load_report()
        
        if not report:
            print("❌ No report found or report is empty")
            return {"assigned": 0, "skipped": 0, "errors": 0}
        
        print(f"📊 Report loaded: {self.report_path.name}")
        
        # Extract actionable tasks
        print("📋 Extracting actionable tasks...")
        tasks = self._extract_actionable_tasks(report)
        
        if not tasks:
            print("⚠️ No actionable tasks found in report")
            return {"assigned": 0, "skipped": 0, "errors": 0}
        
        print(f"✅ Found {len(tasks)} actionable tasks")
        
        # Assign tasks
        assigned = 0
        skipped = 0
        errors = 0
        
        for task in tasks:
            # Find best agent
            agent_id = self._find_best_agent(task)
            
            # Check availability
            is_available, reason = self._check_agent_availability(agent_id)
            if not is_available:
                print(f"⏭️ Skipping {task['category']} - {agent_id} not available ({reason})")
                skipped += 1
                continue
            
            if dry_run:
                print(f"🔍 [DRY RUN] Would assign {task['category']} to {agent_id}")
                assigned += 1
            else:
                # Send task via messaging
                if self._send_task_via_messaging(agent_id, task):
                    # Update agent status
                    self._update_agent_status(agent_id, task)
                    assigned += 1
                else:
                    errors += 1
        
        return {
            "assigned": assigned,
            "skipped": skipped,
            "errors": errors,
            "total": len(tasks)
        }

    def run_continuous_loop(self, interval_minutes: int = 60):
        """Run continuous task assignment loop."""
        print(f"🔄 Starting continuous task assignment loop (check every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        import time
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking for tasks...")
                
                result = self.assign_tasks_from_report(dry_run=False)
                
                print(f"📊 Assignment result: {result['assigned']} assigned, {result['skipped']} skipped, {result['errors']} errors")
                
                # Wait for next interval
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n🛑 Stopping continuous loop")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto-assign technical debt tasks to agents")
    parser.add_argument("--report", help="Path to weekly report JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't actually assign)")
    parser.add_argument("--continuous", action="store_true", help="Run continuous loop")
    parser.add_argument("--interval", type=int, default=60, help="Interval in minutes for continuous mode")
    
    args = parser.parse_args()
    
    assigner = TechnicalDebtAutoAssigner(report_path=args.report)
    
    if args.continuous:
        assigner.run_continuous_loop(interval_minutes=args.interval)
    else:
        result = assigner.assign_tasks_from_report(dry_run=args.dry_run)
        
        print("\n" + "="*70)
        print("📊 ASSIGNMENT SUMMARY")
        print("="*70)
        print(f"✅ Assigned: {result['assigned']}")
        print(f"⏭️ Skipped: {result['skipped']}")
        print(f"❌ Errors: {result['errors']}")
        print(f"📋 Total: {result['total']}")
        print("="*70)
        
        return 0 if result['errors'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

