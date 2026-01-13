#!/usr/bin/env python3
"""
Output Flywheel Usage Tracker
==============================

<!-- SSOT Domain: analytics -->

Tracks agent usage of Output Flywheel system and gathers feedback for v1.1.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: HIGH
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Handle both relative and absolute imports
try:
    from .metrics_client import MetricsClient
except ImportError:
    from metrics_client import MetricsClient


class OutputFlywheelUsageTracker:
    """Tracks Output Flywheel usage and gathers feedback."""

    def __init__(self, metrics_dir: Path = None):
        """Initialize usage tracker."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent
        
        self.metrics_dir = metrics_dir
        self.sessions_dir = metrics_dir / "outputs" / "sessions"
        self.feedback_dir = metrics_dir / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        
        self.usage_data_path = self.feedback_dir / "usage_data.json"
        self.feedback_path = self.feedback_dir / "v1.1_feedback.json"
        
        self.tracker = MetricsClient(metrics_dir)
        self._load_usage_data()

    def _load_usage_data(self):
        """Load usage tracking data."""
        if self.usage_data_path.exists():
            with open(self.usage_data_path, "r", encoding="utf-8") as f:
                self.usage_data = json.load(f)
        else:
            self.usage_data = {
                "sessions_tracked": [],
                "artifacts_created": [],
                "usage_stats": {
                    "total_sessions": 0,
                    "sessions_by_agent": {},
                    "sessions_by_type": {},
                    "artifacts_by_type": {},
                },
                "last_updated": datetime.now().isoformat(),
            }
            self._save_usage_data()

    def _save_usage_data(self):
        """Save usage tracking data."""
        self.usage_data["last_updated"] = datetime.now().isoformat()
        with open(self.usage_data_path, "w", encoding="utf-8") as f:
            json.dump(self.usage_data, f, indent=2)

    def track_session(self, session_file: Path):
        """Track a work session from Output Flywheel."""
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            session_id = session_data.get("session_id", session_file.stem)
            agent_id = session_data.get("agent_id", "unknown")
            session_type = session_data.get("session_type", "unknown")
            
            if session_id in self.usage_data["sessions_tracked"]:
                return
            
            self.usage_data["sessions_tracked"].append(session_id)
            self.usage_data["usage_stats"]["total_sessions"] += 1
            
            # Track by agent
            if agent_id not in self.usage_data["usage_stats"]["sessions_by_agent"]:
                self.usage_data["usage_stats"]["sessions_by_agent"][agent_id] = 0
            self.usage_data["usage_stats"]["sessions_by_agent"][agent_id] += 1
            
            # Track by type
            if session_type not in self.usage_data["usage_stats"]["sessions_by_type"]:
                self.usage_data["usage_stats"]["sessions_by_type"][session_type] = 0
            self.usage_data["usage_stats"]["sessions_by_type"][session_type] += 1
            
            # Track artifacts
            artifacts = session_data.get("artifacts", {})
            for artifact_type, artifact_info in artifacts.items():
                if artifact_info.get("generated"):
                    if artifact_type not in self.usage_data["usage_stats"]["artifacts_by_type"]:
                        self.usage_data["usage_stats"]["artifacts_by_type"][artifact_type] = 0
                    self.usage_data["usage_stats"]["artifacts_by_type"][artifact_type] += 1
                    
                    # Record in metrics tracker
                    artifact_id = f"{session_id}_{artifact_type}"
                    self.tracker.record_artifact(
                        artifact_id=artifact_id,
                        artifact_type=artifact_type,
                        creation_date=datetime.now().isoformat(),
                        metadata={"session_id": session_id, "agent_id": agent_id}
                    )
            
            self._save_usage_data()
            
        except Exception as e:
            print(f"⚠️ Error tracking session {session_file}: {e}")

    def scan_sessions(self):
        """Scan sessions directory and track all sessions."""
        if not self.sessions_dir.exists():
            return
        
        for session_file in self.sessions_dir.glob("*.json"):
            self.track_session(session_file)

    def submit_feedback(
        self,
        agent_id: str,
        feedback_type: str,
        category: str,
        feedback: str,
        priority: str = "medium",
        suggested_fix: str = None,
    ):
        """Submit feedback for v1.1 improvements."""
        feedback_entry = {
            "agent_id": agent_id,
            "feedback_type": feedback_type,  # "feature_request", "bug", "improvement", "question"
            "category": category,  # "usability", "documentation", "pipeline", "monitoring", etc.
            "feedback": feedback,
            "priority": priority,  # "low", "medium", "high", "critical"
            "suggested_fix": suggested_fix,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
        }
        
        if not self.feedback_path.exists():
            feedback_data = {"entries": []}
        else:
            with open(self.feedback_path, "r", encoding="utf-8") as f:
                feedback_data = json.load(f)
        
        feedback_data["entries"].append(feedback_entry)
        
        with open(self.feedback_path, "w", encoding="utf-8") as f:
            json.dump(feedback_data, f, indent=2)
        
        return feedback_entry

    def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary statistics."""
        return {
            "total_sessions": self.usage_data["usage_stats"]["total_sessions"],
            "sessions_by_agent": self.usage_data["usage_stats"]["sessions_by_agent"],
            "sessions_by_type": self.usage_data["usage_stats"]["sessions_by_type"],
            "artifacts_by_type": self.usage_data["usage_stats"]["artifacts_by_type"],
            "last_updated": self.usage_data["last_updated"],
        }

    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get feedback summary for v1.1."""
        if not self.feedback_path.exists():
            return {"total_feedback": 0, "entries": []}
        
        with open(self.feedback_path, "r", encoding="utf-8") as f:
            feedback_data = json.load(f)
        
        entries = feedback_data.get("entries", [])
        
        # Group by category and priority
        by_category = {}
        by_priority = {}
        
        for entry in entries:
            category = entry.get("category", "other")
            priority = entry.get("priority", "medium")
            
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(entry)
            
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(entry)
        
        return {
            "total_feedback": len(entries),
            "by_category": {k: len(v) for k, v in by_category.items()},
            "by_priority": {k: len(v) for k, v in by_priority.items()},
            "entries": entries,
        }


def main():
    """CLI interface for usage tracking."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Output Flywheel Usage Tracker & Feedback Collector"
    )
    parser.add_argument(
        "action",
        choices=["scan", "summary", "feedback", "feedback-summary"],
        help="Action to perform"
    )
    parser.add_argument("--agent", type=str, help="Agent ID for feedback")
    parser.add_argument("--type", type=str, help="Feedback type")
    parser.add_argument("--category", type=str, help="Feedback category")
    parser.add_argument("--feedback", type=str, help="Feedback text")
    parser.add_argument("--priority", type=str, default="medium", help="Priority")
    
    args = parser.parse_args()
    
    tracker = OutputFlywheelUsageTracker()
    
    if args.action == "scan":
        tracker.scan_sessions()
        print("✅ Sessions scanned and tracked")
    
    elif args.action == "summary":
        summary = tracker.get_usage_summary()
        print("\n📊 OUTPUT FLYWHEEL USAGE SUMMARY")
        print("=" * 60)
        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"\nBy Agent:")
        for agent, count in summary["sessions_by_agent"].items():
            print(f"  {agent}: {count}")
        print(f"\nBy Type:")
        for stype, count in summary["sessions_by_type"].items():
            print(f"  {stype}: {count}")
        print(f"\nArtifacts Created:")
        for atype, count in summary["artifacts_by_type"].items():
            print(f"  {atype}: {count}")
    
    elif args.action == "feedback":
        if not all([args.agent, args.type, args.category, args.feedback]):
            print("❌ ERROR: --agent, --type, --category, and --feedback required")
            return
        
        entry = tracker.submit_feedback(
            agent_id=args.agent,
            feedback_type=args.type,
            category=args.category,
            feedback=args.feedback,
            priority=args.priority,
        )
        print(f"✅ Feedback submitted: {entry['timestamp']}")
    
    elif args.action == "feedback-summary":
        summary = tracker.get_feedback_summary()
        print("\n📋 FEEDBACK SUMMARY FOR v1.1")
        print("=" * 60)
        print(f"Total Feedback Entries: {summary['total_feedback']}")
        print(f"\nBy Category:")
        for category, count in summary["by_category"].items():
            print(f"  {category}: {count}")
        print(f"\nBy Priority:")
        for priority, count in summary["by_priority"].items():
            print(f"  {priority}: {count}")


if __name__ == "__main__":
    main()

