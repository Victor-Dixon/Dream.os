"""
Agent Status Snapshot Tool

Generates comprehensive status snapshots for agents from their status.json files.
Useful for quick status checks, reporting, and coordination.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


PROJECT_ROOT = Path(__file__).parent.parent
AGENT_WORKSPACES = PROJECT_ROOT / "agent_workspaces"


def load_agent_status(agent_id: str) -> Optional[Dict]:
    """Load status.json for a specific agent."""
    status_file = AGENT_WORKSPACES / f"Agent-{agent_id[-1]}" / "status.json"
    if not status_file.exists():
        return None
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def generate_snapshot(agent_id: str, include_tasks: bool = True, 
                     include_achievements: bool = True) -> Optional[str]:
    """Generate a formatted status snapshot for an agent."""
    status = load_agent_status(agent_id)
    if not status:
        return None
    
    lines = [
        f"# 📊 Status Snapshot - {status.get('agent_name', agent_id)}",
        "",
        f"**Agent ID**: {agent_id}",
        f"**Status**: {status.get('status', 'UNKNOWN')}",
        f"**Phase**: {status.get('current_phase', 'UNKNOWN')}",
        f"**Last Updated**: {status.get('last_updated', 'UNKNOWN')}",
        "",
        f"**Mission**: {status.get('current_mission', 'No mission set')}",
        f"**Priority**: {status.get('mission_priority', 'UNKNOWN')}",
        "",
        "---",
        ""
    ]
    
    if include_tasks and status.get('current_tasks'):
        lines.extend([
            "## ✅ Current Tasks",
            ""
        ])
        # Show top 10 tasks
        for task in status['current_tasks'][:10]:
            lines.append(f"- {task}")
        if len(status['current_tasks']) > 10:
            lines.append(f"- *... and {len(status['current_tasks']) - 10} more*")
        lines.append("")
    
    if include_achievements and status.get('achievements'):
        lines.extend([
            "## 🏆 Recent Achievements",
            ""
        ])
        # Show top 5 achievements
        for achievement in status['achievements'][:5]:
            lines.append(f"- {achievement}")
        if len(status['achievements']) > 5:
            lines.append(f"- *... and {len(status['achievements']) - 5} more*")
        lines.append("")
    
    if status.get('next_actions'):
        lines.extend([
            "## 🔄 Next Actions",
            ""
        ])
        for action in status['next_actions'][:5]:
            lines.append(f"- {action}")
        if len(status['next_actions']) > 5:
            lines.append(f"- *... and {len(status['next_actions']) - 5} more*")
        lines.append("")
    
    return "\n".join(lines)


def snapshot_all_agents(output_dir: Optional[Path] = None) -> Dict[str, str]:
    """Generate snapshots for all agents."""
    output_dir = output_dir or PROJECT_ROOT / "docs" / "agent_snapshots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    snapshots = {}
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    for agent_num in range(1, 9):
        agent_id = f"Agent-{agent_num}"
        snapshot = generate_snapshot(agent_id)
        
        if snapshot:
            snapshots[agent_id] = snapshot
            output_file = output_dir / f"{agent_id}_snapshot_{timestamp}.md"
            output_file.write_text(snapshot, encoding='utf-8')
    
    return snapshots


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate agent status snapshots")
    parser.add_argument("--agent", type=str, help="Agent ID (e.g., Agent-7)")
    parser.add_argument("--all", action="store_true", help="Generate snapshots for all agents")
    parser.add_argument("--output-dir", type=Path, help="Output directory for snapshots")
    parser.add_argument("--no-tasks", action="store_true", help="Exclude current tasks")
    parser.add_argument("--no-achievements", action="store_true", help="Exclude achievements")
    
    args = parser.parse_args()
    
    if args.all:
        snapshots = snapshot_all_agents(args.output_dir)
        print(f"✅ Generated {len(snapshots)} agent snapshots")
        for agent_id, snapshot in snapshots.items():
            print(f"   {agent_id}: {len(snapshot)} characters")
    elif args.agent:
        snapshot = generate_snapshot(
            args.agent,
            include_tasks=not args.no_tasks,
            include_achievements=not args.no_achievements
        )
        if snapshot:
            print(snapshot)
        else:
            print(f"❌ Could not generate snapshot for {args.agent}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

