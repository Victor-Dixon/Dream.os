#!/usr/bin/env python3
"""
Technical Debt Marker Tracker
==============================

<!-- SSOT Domain: analytics -->

Tracks and manages technical debt markers (TODO/FIXME/etc) across the codebase.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: LOW - Documentation & Cleanup
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class TechnicalDebtMarkerTracker:
    """Tracks technical debt markers and their resolution."""

    def __init__(self, data_file: Path = None):
        """Initialize tracker."""
        if data_file is None:
            data_file = Path(__file__).parent / "data" / "markers_tracking.json"
        
        self.data_file = data_file
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.markers_data: Dict[str, Any] = {}
        
        self.load_data()

    def load_data(self):
        """Load marker tracking data."""
        if self.data_file.exists():
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.markers_data = json.load(f)
            except Exception:
                self.markers_data = self._create_empty_data()
        else:
            self.markers_data = self._create_empty_data()

    def _create_empty_data(self) -> Dict[str, Any]:
        """Create empty tracking data structure."""
        return {
            "markers": {},
            "resolution_history": [],
            "last_updated": datetime.now().isoformat(),
        }

    def save_data(self):
        """Save marker tracking data."""
        self.markers_data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.markers_data, f, indent=2)

    def import_analysis_results(self, analysis_file: Path):
        """Import markers from analysis results."""
        with open(analysis_file, "r", encoding="utf-8") as f:
            analysis = json.load(f)
        
        markers = analysis.get("markers", [])
        
        for marker in markers:
            marker_id = self._generate_marker_id(marker)
            
            if marker_id not in self.markers_data["markers"]:
                self.markers_data["markers"][marker_id] = {
                    **marker,
                    "status": "open",
                    "created_date": datetime.now().isoformat(),
                    "resolved_date": None,
                    "assigned_to": None,
                    "notes": [],
                }
        
        self.save_data()
        print(f"✅ Imported {len(markers)} markers from analysis")

    def _generate_marker_id(self, marker: Dict[str, Any]) -> str:
        """Generate unique ID for marker."""
        file_path = marker.get("relative_path", "")
        line_num = marker.get("line_number", 0)
        marker_type = marker.get("marker_type", "")
        return f"{file_path}:{line_num}:{marker_type}"

    def mark_resolved(self, marker_id: str, notes: str = None):
        """Mark a marker as resolved."""
        if marker_id in self.markers_data["markers"]:
            marker = self.markers_data["markers"][marker_id]
            marker["status"] = "resolved"
            marker["resolved_date"] = datetime.now().isoformat()
            
            if notes:
                marker["notes"].append({
                    "date": datetime.now().isoformat(),
                    "note": notes,
                })
            
            self.markers_data["resolution_history"].append({
                "marker_id": marker_id,
                "resolved_date": datetime.now().isoformat(),
                "marker": marker,
            })
            
            self.save_data()

    def assign_marker(self, marker_id: str, agent_id: str):
        """Assign marker to an agent."""
        if marker_id in self.markers_data["markers"]:
            self.markers_data["markers"][marker_id]["assigned_to"] = agent_id
            self.save_data()

    def get_open_markers(self, priority: str = None) -> List[Dict[str, Any]]:
        """Get all open markers, optionally filtered by priority."""
        open_markers = [
            marker for marker in self.markers_data["markers"].values()
            if marker["status"] == "open"
        ]
        
        if priority:
            open_markers = [
                m for m in open_markers if m.get("priority") == priority
            ]
        
        return sorted(open_markers, key=lambda x: (
            x.get("priority", ""),
            x.get("relative_path", ""),
            x.get("line_number", 0)
        ))

    def get_statistics(self) -> Dict[str, Any]:
        """Get tracking statistics."""
        markers = self.markers_data["markers"]
        
        total = len(markers)
        open_count = len([m for m in markers.values() if m["status"] == "open"])
        resolved_count = len([m for m in markers.values() if m["status"] == "resolved"])
        
        by_priority = {}
        by_type = {}
        
        for marker in markers.values():
            priority = marker.get("priority", "unknown")
            marker_type = marker.get("marker_type", "unknown")
            
            by_priority[priority] = by_priority.get(priority, 0) + 1
            by_type[marker_type] = by_type.get(marker_type, 0) + 1
        
        return {
            "total": total,
            "open": open_count,
            "resolved": resolved_count,
            "resolution_rate": (resolved_count / total * 100) if total > 0 else 0,
            "by_priority": by_priority,
            "by_type": by_type,
        }


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Technical Debt Marker Tracker")
    parser.add_argument("--import-analysis", type=Path, help="Import from analysis JSON")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--open", action="store_true", help="List open markers")
    parser.add_argument("--priority", type=str, help="Filter by priority")
    
    args = parser.parse_args()
    
    tracker = TechnicalDebtMarkerTracker()
    
    if args.import_analysis:
        tracker.import_analysis_results(args.import_analysis)
    
    if args.stats:
        stats = tracker.get_statistics()
        print(json.dumps(stats, indent=2))
    
    if args.open:
        open_markers = tracker.get_open_markers(priority=args.priority)
        print(f"Open markers: {len(open_markers)}")
        if args.priority:
            print(f"Filtered by priority: {args.priority}")
        
        for marker in open_markers[:20]:  # Show first 20
            print(f"\n{marker['relative_path']}:{marker['line_number']}")
            print(f"  Type: {marker['marker_type']} | Priority: {marker['priority']}")
            print(f"  Text: {marker['marker_text'][:100]}...")


if __name__ == "__main__":
    main()


