#!/usr/bin/env python3
"""
Session Transition Validator - Agent-5
======================================

Validates all session transition requirements are complete.

Usage:
    python tools/session_transition_validator.py [agent_id]
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class SessionTransitionValidator:
    """Validates session transition deliverables."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.agent_workspace = project_root / "agent_workspaces" / agent_id
        self.results = {
            "agent_id": agent_id,
            "validation_date": datetime.now().isoformat(),
            "checks": {},
            "status": "UNKNOWN"
        }
    
    def validate_passdown(self) -> Tuple[bool, str]:
        """Validate passdown.json exists and is complete."""
        passdown_file = self.agent_workspace / "passdown.json"
        
        if not passdown_file.exists():
            return False, "passdown.json not found"
        
        try:
            with open(passdown_file, 'r') as f:
                data = json.load(f)
            
            required_fields = [
                "agent_id", "session_date", "session_summary",
                "completed_tasks", "key_insights", "next_session_priorities"
            ]
            
            missing = [field for field in required_fields if field not in data]
            if missing:
                return False, f"Missing fields: {', '.join(missing)}"
            
            return True, "passdown.json complete"
        except Exception as e:
            return False, f"Error reading passdown.json: {str(e)}"
    
    def validate_devlog(self) -> Tuple[bool, str]:
        """Validate devlog entry exists."""
        devlog_dir = project_root / "devlogs"
        if not devlog_dir.exists():
            return False, "devlogs directory not found"
        
        # Check for recent devlog (within last 2 days)
        today = datetime.now().date()
        found_recent = False
        
        for devlog_file in devlog_dir.glob(f"*{self.agent_id.lower()}*.md"):
            try:
                file_date = datetime.fromtimestamp(
                    devlog_file.stat().st_mtime
                ).date()
                if (today - file_date).days <= 2:
                    found_recent = True
                    break
            except Exception:
                pass
        
        if not found_recent:
            return False, "No recent devlog found (within 2 days)"
        
        return True, "Recent devlog found"
    
    def validate_state_report(self) -> Tuple[bool, str]:
        """Validate state report mentions agent."""
        state_report = project_root / "STATE_OF_THE_PROJECT_REPORT.md"
        
        if not state_report.exists():
            return False, "STATE_OF_THE_PROJECT_REPORT.md not found"
        
        try:
            content = state_report.read_text(encoding='utf-8')
            if self.agent_id in content:
                return True, "Agent mentioned in state report"
            return False, "Agent not mentioned in state report"
        except Exception as e:
            return False, f"Error reading state report: {str(e)}"
    
    def validate_cycle_planner(self) -> Tuple[bool, str]:
        """Validate cycle planner entry exists."""
        cycle_planner_dir = project_root / "agent_workspaces" / "swarm_cycle_planner" / "cycles"
        
        if not cycle_planner_dir.exists():
            return False, "cycle_planner directory not found"
        
        # Check for recent cycle planner entry
        today = datetime.now().date()
        found_recent = False
        
        for cycle_file in cycle_planner_dir.glob(f"*{self.agent_id.lower()}*.json"):
            try:
                file_date = datetime.fromtimestamp(
                    cycle_file.stat().st_mtime
                ).date()
                if (today - file_date).days <= 2:
                    found_recent = True
                    break
            except Exception:
                pass
        
        if not found_recent:
            return False, "No recent cycle planner entry found"
        
        return True, "Recent cycle planner entry found"
    
    def validate_status_json(self) -> Tuple[bool, str]:
        """Validate status.json is updated."""
        status_file = self.agent_workspace / "status.json"
        
        if not status_file.exists():
            return False, "status.json not found"
        
        try:
            with open(status_file, 'r') as f:
                data = json.load(f)
            
            if "last_updated" not in data:
                return False, "status.json missing last_updated"
            
            # Check if updated recently (within last 2 days)
            try:
                last_updated = datetime.strptime(
                    data["last_updated"], "%Y-%m-%d %H:%M:%S"
                )
                days_ago = (datetime.now() - last_updated).days
                if days_ago > 2:
                    return False, f"status.json not updated recently ({days_ago} days ago)"
            except Exception:
                pass
            
            return True, "status.json updated recently"
        except Exception as e:
            return False, f"Error reading status.json: {str(e)}"
    
    def validate_swarm_brain(self) -> Tuple[bool, str]:
        """Validate Swarm Brain contribution exists."""
        swarm_brain_dir = project_root / "swarm_brain"
        
        if not swarm_brain_dir.exists():
            return False, "swarm_brain directory not found"
        
        # Check for recent contribution (within last 2 days)
        today = datetime.now().date()
        found_recent = False
        
        for contrib_file in swarm_brain_dir.rglob(f"*{self.agent_id.lower()}*.md"):
            try:
                file_date = datetime.fromtimestamp(
                    contrib_file.stat().st_mtime
                ).date()
                if (today - file_date).days <= 2:
                    found_recent = True
                    break
            except Exception:
                pass
        
        if not found_recent:
            return False, "No recent Swarm Brain contribution found"
        
        return True, "Recent Swarm Brain contribution found"
    
    def validate_code_of_conduct_review(self) -> Tuple[bool, str]:
        """Validate Code of Conduct review exists."""
        review_file = self.agent_workspace / f"code_of_conduct_review_{datetime.now().strftime('%Y-%m-%d')}.md"
        
        # Also check for any recent review
        today = datetime.now().date()
        found_recent = False
        
        for review in self.agent_workspace.glob("code_of_conduct_review_*.md"):
            try:
                file_date = datetime.fromtimestamp(
                    review.stat().st_mtime
                ).date()
                if (today - file_date).days <= 2:
                    found_recent = True
                    break
            except Exception:
                pass
        
        if found_recent or review_file.exists():
            return True, "Code of Conduct review found"
        
        return False, "Code of Conduct review not found"
    
    def validate_all(self) -> Dict:
        """Run all validation checks."""
        checks = {
            "passdown": self.validate_passdown(),
            "devlog": self.validate_devlog(),
            "state_report": self.validate_state_report(),
            "cycle_planner": self.validate_cycle_planner(),
            "status_json": self.validate_status_json(),
            "swarm_brain": self.validate_swarm_brain(),
            "code_of_conduct": self.validate_code_of_conduct_review()
        }
        
        self.results["checks"] = {
            check: {
                "status": "PASS" if result[0] else "FAIL",
                "message": result[1]
            }
            for check, result in checks.items()
        }
        
        all_passed = all(result[0] for result in checks.values())
        self.results["status"] = "COMPLETE" if all_passed else "INCOMPLETE"
        
        return self.results
    
    def print_report(self):
        """Print validation report."""
        print("\n" + "="*70)
        print(f"SESSION TRANSITION VALIDATION - {self.agent_id}")
        print("="*70)
        
        for check, result in self.results["checks"].items():
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {check.upper()}: {result['message']}")
        
        print("\n" + "="*70)
        print(f"OVERALL STATUS: {self.results['status']}")
        print("="*70)
        
        if self.results["status"] == "COMPLETE":
            print("\n✅ All session transition requirements met!")
        else:
            print("\n⚠️  Some requirements missing. Review checklist above.")


def main():
    """Main function."""
    import argparse
    parser = argparse.ArgumentParser(
        description="Validate session transition deliverables"
    )
    parser.add_argument(
        "agent_id",
        nargs="?",
        default="Agent-5",
        help="Agent ID to validate (default: Agent-5)"
    )
    args = parser.parse_args()
    
    validator = SessionTransitionValidator(args.agent_id)
    results = validator.validate_all()
    validator.print_report()
    
    return 0 if results["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
