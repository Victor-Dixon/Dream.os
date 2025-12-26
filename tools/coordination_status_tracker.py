#!/usr/bin/env python3
"""
Coordination Status Tracker
Tool I wished I had: Track all active coordinations, their status, and next actions
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class CoordinationStatusTracker:
    """Track active coordinations across agents."""
    
    def __init__(self, status_file: str = "reports/coordination_status.json"):
        """Initialize tracker."""
        self.status_file = Path(status_file)
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        self.coordinations = self._load_status()
    
    def _load_status(self) -> Dict:
        """Load coordination status."""
        if self.status_file.exists():
            return json.loads(self.status_file.read_text())
        return {
            "last_updated": datetime.now().isoformat(),
            "active_coordinations": [],
            "completed_coordinations": [],
        }
    
    def add_coordination(self, coordination_id: str, partner: str, task: str, 
                         status: str = "active", sync_scheduled: Optional[str] = None):
        """Add or update coordination."""
        coord = {
            "coordination_id": coordination_id,
            "partner": partner,
            "task": task,
            "status": status,
            "sync_scheduled": sync_scheduled,
            "last_updated": datetime.now().isoformat(),
        }
        
        # Update or add
        existing = next((c for c in self.coordinations["active_coordinations"] 
                        if c.get("coordination_id") == coordination_id), None)
        if existing:
            existing.update(coord)
        else:
            self.coordinations["active_coordinations"].append(coord)
        
        self._save_status()
        return coord
    
    def complete_coordination(self, coordination_id: str):
        """Mark coordination as complete."""
        coord = next((c for c in self.coordinations["active_coordinations"] 
                     if c.get("coordination_id") == coordination_id), None)
        if coord:
            coord["status"] = "complete"
            coord["completed_date"] = datetime.now().isoformat()
            self.coordinations["active_coordinations"].remove(coord)
            self.coordinations["completed_coordinations"].append(coord)
            self._save_status()
    
    def get_active_coordinations(self) -> List[Dict]:
        """Get all active coordinations."""
        return self.coordinations["active_coordinations"]
    
    def get_coordination_summary(self) -> Dict:
        """Get coordination summary."""
        active = self.coordinations["active_coordinations"]
        return {
            "total_active": len(active),
            "by_partner": {},
            "by_status": {},
            "upcoming_syncs": [c for c in active if c.get("sync_scheduled")],
        }
    
    def _save_status(self):
        """Save coordination status."""
        self.coordinations["last_updated"] = datetime.now().isoformat()
        self.status_file.write_text(json.dumps(self.coordinations, indent=2))
    
    def generate_report(self) -> str:
        """Generate markdown report."""
        active = self.get_active_coordinations()
        summary = self.get_coordination_summary()
        
        report = f"# Coordination Status Report\n\n"
        report += f"**Last Updated:** {self.coordinations['last_updated']}\n\n"
        report += f"**Active Coordinations:** {summary['total_active']}\n\n"
        
        if active:
            report += "## Active Coordinations\n\n"
            for coord in active:
                report += f"### {coord['partner']} - {coord['task']}\n"
                report += f"- **ID:** {coord['coordination_id']}\n"
                report += f"- **Status:** {coord['status']}\n"
                if coord.get('sync_scheduled'):
                    report += f"- **Sync Scheduled:** {coord['sync_scheduled']}\n"
                report += f"- **Last Updated:** {coord['last_updated']}\n\n"
        
        return report

def main():
    """Main entry point."""
    tracker = CoordinationStatusTracker()
    
    # Example: Add current coordination
    tracker.add_coordination(
        coordination_id="d6aafd6d-46e2-4e96-9b37-d0ade7b1afb9",
        partner="Agent-7",
        task="Website implementation coordination",
        status="active",
        sync_scheduled="2025-12-25 12:00"
    )
    
    # Generate report
    report = tracker.generate_report()
    report_path = Path("reports/coordination_status_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    
    print("✅ Coordination Status Tracker")
    print(f"   Active coordinations: {len(tracker.get_active_coordinations())}")
    print(f"   Report: {report_path}")

if __name__ == "__main__":
    main()

