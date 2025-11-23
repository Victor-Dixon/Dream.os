#!/usr/bin/env python3
"""Session Transition Helper - Productivity Tool.
================================================

CLI tool to help agents complete session transition deliverables efficiently.
Checks completion status, provides templates, and validates deliverables.

V2 Compliance: <400 lines, type hints, documented
Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-23
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class DeliverableStatus(Enum):
    """Deliverable completion status."""
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    NOT_STARTED = "not_started"


class SessionTransitionHelper:
    """Helper for session transition deliverables."""
    
    REQUIRED_DELIVERABLES = [
        "passdown",
        "devlog",
        "discord",
        "swarm_brain",
        "code_of_conduct",
        "thread_review",
        "state_report",
        "cycle_planner",
        "productivity_tool"
    ]
    
    def __init__(self, agent_id: str, workspace_path: Optional[Path] = None):
        """Initialize helper.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-8")
            workspace_path: Path to agent workspace (optional)
        """
        self.agent_id = agent_id
        if workspace_path is None:
            workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.workspace_path = Path(workspace_path)
        self.status_file = self.workspace_path / "session_transition_status.json"
        self.status: Dict[str, str] = {}
        self.load_status()
    
    def load_status(self) -> None:
        """Load transition status from file."""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.status = data.get('status', {})
            except Exception:
                self.status = {}
        else:
            self.status = {deliverable: DeliverableStatus.NOT_STARTED.value 
                          for deliverable in self.REQUIRED_DELIVERABLES}
    
    def save_status(self) -> None:
        """Save transition status to file."""
        data = {
            'agent_id': self.agent_id,
            'last_updated': datetime.utcnow().isoformat(),
            'status': self.status
        }
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def check_deliverable(self, deliverable: str) -> DeliverableStatus:
        """Check if deliverable is complete.
        
        Args:
            deliverable: Deliverable name
            
        Returns:
            DeliverableStatus
        """
        if deliverable not in self.REQUIRED_DELIVERABLES:
            return DeliverableStatus.NOT_STARTED
        
        # Check file existence
        if deliverable == "passdown":
            file_path = self.workspace_path / "passdown.json"
        elif deliverable == "devlog":
            devlog_dir = self.workspace_path / "devlogs"
            if devlog_dir.exists():
                devlogs = list(devlog_dir.glob("*.md"))
                if devlogs:
                    return DeliverableStatus.COMPLETE
            return DeliverableStatus.NOT_STARTED
        elif deliverable == "code_of_conduct":
            file_path = self.workspace_path / f"code_of_conduct_review_{datetime.now().strftime('%Y-%m-%d')}.md"
        elif deliverable == "state_report":
            file_path = Path("STATE_OF_THE_PROJECT_REPORT.md")
        else:
            # For other deliverables, check status file
            return DeliverableStatus(self.status.get(deliverable, DeliverableStatus.NOT_STARTED.value))
        
        if file_path.exists():
            return DeliverableStatus.COMPLETE
        return DeliverableStatus.NOT_STARTED
    
    def get_completion_summary(self) -> Dict[str, any]:
        """Get completion summary.
        
        Returns:
            Dictionary with completion statistics
        """
        statuses = {deliverable: self.check_deliverable(deliverable) 
                   for deliverable in self.REQUIRED_DELIVERABLES}
        
        complete = sum(1 for s in statuses.values() if s == DeliverableStatus.COMPLETE)
        total = len(self.REQUIRED_DELIVERABLES)
        percentage = (complete / total * 100) if total > 0 else 0
        
        return {
            'agent_id': self.agent_id,
            'total_deliverables': total,
            'complete': complete,
            'in_progress': sum(1 for s in statuses.values() 
                             if s == DeliverableStatus.IN_PROGRESS),
            'pending': sum(1 for s in statuses.values() 
                          if s == DeliverableStatus.PENDING),
            'not_started': sum(1 for s in statuses.values() 
                              if s == DeliverableStatus.NOT_STARTED),
            'completion_percentage': percentage,
            'status_by_deliverable': {k: v.value for k, v in statuses.items()}
        }
    
    def mark_complete(self, deliverable: str) -> None:
        """Mark deliverable as complete.
        
        Args:
            deliverable: Deliverable name
        """
        if deliverable in self.REQUIRED_DELIVERABLES:
            self.status[deliverable] = DeliverableStatus.COMPLETE.value
            self.save_status()
    
    def get_template(self, deliverable: str) -> Optional[str]:
        """Get template for deliverable.
        
        Args:
            deliverable: Deliverable name
            
        Returns:
            Template string or None
        """
        templates = {
            "passdown": """{
  "agent_id": "{agent_id}",
  "session_date": "{date}",
  "session_summary": "Brief summary",
  "status": "SESSION TRANSITION COMPLETE",
  "completed_tasks": [],
  "key_insights": [],
  "patterns_learned": [],
  "recommendations": [],
  "blockers": "NONE",
  "next_session_priorities": [],
  "gas_pipeline": {
    "status": "ACTIVE",
    "fuel_received": "",
    "fuel_provided": ""
  }
}""",
            "devlog": """# Agent-{agent_id} Devlog: Session Title

**Date**: {date}
**Agent**: {agent_id}
**Session Type**: [Type]

## ✅ Accomplishments
- 

## 🧠 Challenges & Solutions
- 

## 📚 Learnings
- 

## 🔄 Next Actions
- 
"""
        }
        
        template = templates.get(deliverable)
        if template:
            return template.format(
                agent_id=self.agent_id,
                date=datetime.now().strftime("%Y-%m-%d")
            )
        return None


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Session Transition Helper')
    parser.add_argument('--agent', type=str, default='Agent-8',
                       help='Agent ID')
    parser.add_argument('--check', action='store_true',
                       help='Check completion status')
    parser.add_argument('--summary', action='store_true',
                       help='Show completion summary')
    parser.add_argument('--template', type=str,
                       help='Get template for deliverable')
    parser.add_argument('--mark-complete', type=str,
                       help='Mark deliverable as complete')
    
    args = parser.parse_args()
    
    helper = SessionTransitionHelper(args.agent)
    
    if args.summary or args.check:
        summary = helper.get_completion_summary()
        print(json.dumps(summary, indent=2))
    elif args.template:
        template = helper.get_template(args.template)
        if template:
            print(template)
        else:
            print(f"No template available for: {args.template}")
    elif args.mark_complete:
        helper.mark_complete(args.mark_complete)
        print(f"✅ Marked {args.mark_complete} as complete")
    else:
        # Default: show summary
        summary = helper.get_completion_summary()
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
