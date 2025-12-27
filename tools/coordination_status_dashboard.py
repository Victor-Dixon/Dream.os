#!/usr/bin/env python3
"""
Coordination Status Dashboard Tool

Real-time dashboard showing all active coordinations, blockers, and progress across agents
with filtering and status indicators.

Usage:
    python tools/coordination_status_dashboard.py [--agent Agent-X] [--status STATUS] [--format FORMAT]
    
Examples:
    # Show all coordinations
    python tools/coordination_status_dashboard.py
    
    # Show coordinations for Agent-4
    python tools/coordination_status_dashboard.py --agent Agent-4
    
    # Show only active coordinations
    python tools/coordination_status_dashboard.py --status ACTIVE
    
    # Export to JSON
    python tools/coordination_status_dashboard.py --format json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Load .env
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class CoordinationStatusDashboard:
    """Dashboard for viewing coordination status across all agents."""
    
    def __init__(self):
        """Initialize dashboard."""
        self.project_root = project_root
        self.workspaces_dir = project_root / "agent_workspaces"
        self.coordinations: List[Dict] = []
        self.agents_data: Dict[str, Dict] = {}
    
    def load_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Load agent status.json file.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1")
        
        Returns:
            Status dict or None if not found
        """
        status_file = self.workspaces_dir / agent_id / "status.json"
        if not status_file.exists():
            return None
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load {agent_id} status: {e}")
            return None
    
    def collect_coordinations(self, agent_filter: Optional[str] = None):
        """Collect all coordinations from agent status files.
        
        Args:
            agent_filter: Optional agent ID to filter by
        """
        self.coordinations = []
        self.agents_data = {}
        
        # Get all agent directories
        agent_dirs = [d for d in self.workspaces_dir.iterdir() 
                     if d.is_dir() and d.name.startswith("Agent-")]
        
        for agent_dir in agent_dirs:
            agent_id = agent_dir.name
            
            # Apply filter
            if agent_filter and agent_id != agent_filter:
                continue
            
            # Load status
            status = self.load_agent_status(agent_id)
            if not status:
                continue
            
            self.agents_data[agent_id] = status
            
            # Extract coordinations
            coordinations = status.get("active_coordinations", [])
            for coord in coordinations:
                # Skip if not a dict
                if not isinstance(coord, dict):
                    continue
                
                coord_data = {
                    "task": coord.get("task", "Unknown Task"),
                    "status": coord.get("status", "UNKNOWN"),
                    "agents": coord.get("agents", []),
                    "progress": coord.get("progress", ""),
                    "blockers": coord.get("blockers", []),
                    "notes": coord.get("notes", ""),
                    "source_agent": agent_id,
                    "last_updated": status.get("last_updated", "")
                }
                self.coordinations.append(coord_data)
    
    def filter_coordinations(
        self,
        agent_filter: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> List[Dict]:
        """Filter coordinations by agent and/or status.
        
        Args:
            agent_filter: Optional agent ID to filter by
            status_filter: Optional status to filter by (e.g., "ACTIVE", "IN_PROGRESS")
        
        Returns:
            Filtered list of coordinations
        """
        filtered = self.coordinations
        
        if agent_filter:
            filtered = [c for c in filtered if agent_filter in c["agents"]]
        
        if status_filter:
            filtered = [c for c in filtered if c["status"].upper() == status_filter.upper()]
        
        return filtered
    
    def get_statistics(self) -> Dict:
        """Get coordination statistics.
        
        Returns:
            Dict with statistics
        """
        stats = {
            "total_coordinations": len(self.coordinations),
            "by_status": defaultdict(int),
            "by_agent": defaultdict(int),
            "total_blockers": 0,
            "agents_with_coordinations": set()
        }
        
        for coord in self.coordinations:
            status = coord["status"]
            stats["by_status"][status] += 1
            
            stats["total_blockers"] += len(coord.get("blockers", []))
            
            for agent in coord["agents"]:
                stats["by_agent"][agent] += 1
                stats["agents_with_coordinations"].add(agent)
        
        stats["agents_with_coordinations"] = len(stats["agents_with_coordinations"])
        
        return stats
    
    def format_status_indicator(self, status: str) -> str:
        """Format status with indicator emoji.
        
        Args:
            status: Status string
        
        Returns:
            Formatted status with emoji
        """
        indicators = {
            "ACTIVE": "🟢",
            "IN_PROGRESS": "🟡",
            "COMPLETE": "✅",
            "READY_FOR_DEPLOYMENT": "🚀",
            "BLOCKED": "🔴",
            "COORDINATED": "🔵",
            "PENDING": "⏳"
        }
        
        emoji = indicators.get(status.upper(), "⚪")
        return f"{emoji} {status}"
    
    def format_blockers(self, blockers: List) -> str:
        """Format blockers list.
        
        Args:
            blockers: List of blockers
        
        Returns:
            Formatted blockers string
        """
        if not blockers:
            return "None"
        
        return "\n   ".join([f"🔴 {b}" if isinstance(b, str) else f"🔴 {json.dumps(b)}" 
                            for b in blockers])
    
    def display_console(self, coordinations: List[Dict], show_details: bool = True):
        """Display coordinations in console format.
        
        Args:
            coordinations: List of coordinations to display
            show_details: Whether to show detailed information
        """
        if not coordinations:
            print("📭 No coordinations found")
            return
        
        print("\n" + "="*80)
        print("COORDINATION STATUS DASHBOARD")
        print("="*80)
        print(f"Total Coordinations: {len(coordinations)}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
        
        # Group by status
        by_status = defaultdict(list)
        for coord in coordinations:
            by_status[coord["status"]].append(coord)
        
        # Display by status
        for status in ["ACTIVE", "IN_PROGRESS", "READY_FOR_DEPLOYMENT", "COORDINATED", 
                      "BLOCKED", "PENDING", "COMPLETE"]:
            if status not in by_status:
                continue
            
            coords = by_status[status]
            print(f"\n{self.format_status_indicator(status)} ({len(coords)} coordinations)")
            print("-" * 80)
            
            for i, coord in enumerate(coords, 1):
                print(f"\n{i}. {coord['task']}")
                print(f"   Agents: {', '.join(coord['agents'])}")
                print(f"   Source: {coord['source_agent']}")
                
                if coord.get("progress"):
                    print(f"   Progress: {coord['progress']}")
                
                blockers = coord.get("blockers", [])
                if blockers:
                    print(f"   Blockers: {self.format_blockers(blockers)}")
                
                if show_details and coord.get("notes"):
                    notes = coord["notes"]
                    if len(notes) > 200:
                        notes = notes[:200] + "..."
                    print(f"   Notes: {notes}")
        
        # Statistics
        stats = self.get_statistics()
        print("\n" + "="*80)
        print("STATISTICS")
        print("="*80)
        print(f"Total Coordinations: {stats['total_coordinations']}")
        print(f"Agents with Coordinations: {stats['agents_with_coordinations']}")
        print(f"Total Blockers: {stats['total_blockers']}")
        print("\nBy Status:")
        for status, count in sorted(stats['by_status'].items()):
            print(f"  {self.format_status_indicator(status)}: {count}")
        print("\nBy Agent:")
        for agent, count in sorted(stats['by_agent'].items()):
            print(f"  {agent}: {count}")
        print("="*80 + "\n")
    
    def export_json(self, coordinations: List[Dict], output_file: Optional[str] = None) -> str:
        """Export coordinations to JSON.
        
        Args:
            coordinations: List of coordinations to export
            output_file: Optional output file path
        
        Returns:
            JSON string
        """
        data = {
            "generated": datetime.now().isoformat(),
            "total_coordinations": len(coordinations),
            "statistics": self.get_statistics(),
            "coordinations": coordinations
        }
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"✅ Exported to {output_file}")
        
        return json_str


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coordination Status Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show all coordinations
  python tools/coordination_status_dashboard.py
  
  # Show coordinations for Agent-4
  python tools/coordination_status_dashboard.py --agent Agent-4
  
  # Show only active coordinations
  python tools/coordination_status_dashboard.py --status ACTIVE
  
  # Export to JSON
  python tools/coordination_status_dashboard.py --format json --output coordinations.json
        """
    )
    
    parser.add_argument(
        "--agent",
        type=str,
        help="Filter by agent ID (e.g., Agent-4)"
    )
    parser.add_argument(
        "--status",
        type=str,
        help="Filter by status (e.g., ACTIVE, IN_PROGRESS, COMPLETE)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["console", "json"],
        default="console",
        help="Output format (default: console)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (for JSON format)"
    )
    parser.add_argument(
        "--no-details",
        action="store_true",
        help="Hide detailed notes in console output"
    )
    
    args = parser.parse_args()
    
    # Initialize dashboard
    dashboard = CoordinationStatusDashboard()
    
    # Collect coordinations
    dashboard.collect_coordinations(agent_filter=args.agent)
    
    # Filter coordinations
    coordinations = dashboard.filter_coordinations(
        agent_filter=args.agent,
        status_filter=args.status
    )
    
    # Display or export
    if args.format == "json":
        json_str = dashboard.export_json(coordinations, output_file=args.output)
        if not args.output:
            print(json_str)
    else:
        dashboard.display_console(coordinations, show_details=not args.no_details)


if __name__ == "__main__":
    main()
