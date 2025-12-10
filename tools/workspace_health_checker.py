#!/usr/bin/env python3
"""
Workspace Health Checker
========================

Validates agent workspace structure, checks for invalid directories,
and provides health report for all agent workspaces.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-10
Priority: HIGH
V2 Compliant: Yes
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

VALID_AGENT_IDS = {f"Agent-{i}" for i in range(1, 9)}


def check_workspace_structure(workspace_root: Path) -> Dict[str, Any]:
    """
    Check workspace structure health.
    
    Returns:
        Health report dictionary
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "workspace_root": str(workspace_root),
        "valid_agents": [],
        "invalid_directories": [],
        "missing_structures": {},
        "statistics": {
            "total_agents": 0,
            "valid_agents": 0,
            "invalid_directories": 0,
            "missing_inboxes": 0,
            "missing_status": 0
        }
    }
    
    if not workspace_root.exists():
        report["error"] = "Workspace root does not exist"
        return report
    
    # Check each agent workspace
    for item in workspace_root.iterdir():
        if not item.is_dir():
            continue
        
        agent_id = item.name
        
        # Skip non-agent directories
        if agent_id in ("agent_registry.json", "contracts", "meeting", "swarm_cycle_planner", 
                        "archive", "AutoGasPipeline", "GaslineHub"):
            continue
        
        # Check if valid agent ID
        if is_valid_agent_id(agent_id):
            report["statistics"]["total_agents"] += 1
            report["statistics"]["valid_agents"] += 1
            
            agent_health = check_agent_workspace(item, agent_id)
            report["valid_agents"].append(agent_health)
            
            if not agent_health["has_inbox"]:
                report["statistics"]["missing_inboxes"] += 1
            if not agent_health["has_status"]:
                report["statistics"]["missing_status"] += 1
        else:
            # Invalid directory
            report["statistics"]["invalid_directories"] += 1
            report["invalid_directories"].append({
                "name": agent_id,
                "type": "invalid_agent_id",
                "recommendation": f"Remove or archive (valid IDs: {', '.join(sorted(VALID_AGENT_IDS))})"
            })
    
    return report


def is_valid_agent_id(agent_id: str) -> bool:
    """Check if agent ID is valid."""
    return agent_id in VALID_AGENT_IDS


def check_agent_workspace(workspace_dir: Path, agent_id: str) -> Dict[str, Any]:
    """Check individual agent workspace health."""
    health = {
        "agent_id": agent_id,
        "workspace_path": str(workspace_dir),
        "has_inbox": (workspace_dir / "inbox").exists(),
        "has_status": (workspace_dir / "status.json").exists(),
        "has_passdown": (workspace_dir / "passdown.json").exists(),
        "inbox_message_count": 0,
        "issues": []
    }
    
    # Count inbox messages
    inbox_dir = workspace_dir / "inbox"
    if inbox_dir.exists():
        health["inbox_message_count"] = len(list(inbox_dir.glob("*.md"))) + len(list(inbox_dir.glob("*.json")))
    
    # Check for required structures
    if not health["has_inbox"]:
        health["issues"].append("Missing inbox directory")
    
    if not health["has_status"]:
        health["issues"].append("Missing status.json file")
    
    # Check status.json validity
    if health["has_status"]:
        try:
            status_file = workspace_dir / "status.json"
            with open(status_file, 'r', encoding='utf-8') as f:
                status_data = json.load(f)
                if status_data.get("agent_id") != agent_id:
                    health["issues"].append(f"status.json agent_id mismatch: {status_data.get('agent_id')} != {agent_id}")
        except Exception as e:
            health["issues"].append(f"Invalid status.json: {str(e)}")
    
    health["health_status"] = "healthy" if not health["issues"] else "unhealthy"
    
    return health


def print_health_report(report: Dict[str, Any]) -> None:
    """Print formatted health report."""
    print("=" * 70)
    print("🏥 WORKSPACE HEALTH CHECK REPORT")
    print("=" * 70)
    print(f"\nTimestamp: {report['timestamp']}")
    print(f"Workspace Root: {report['workspace_root']}\n")
    
    # Statistics
    stats = report["statistics"]
    print("📊 STATISTICS")
    print("-" * 70)
    print(f"  Total Agents: {stats['total_agents']}")
    print(f"  Valid Agents: {stats['valid_agents']}")
    print(f"  Invalid Directories: {stats['invalid_directories']}")
    print(f"  Missing Inboxes: {stats['missing_inboxes']}")
    print(f"  Missing Status Files: {stats['missing_status']}\n")
    
    # Valid agents
    if report["valid_agents"]:
        print("✅ VALID AGENTS")
        print("-" * 70)
        for agent in report["valid_agents"]:
            status_icon = "✅" if agent["health_status"] == "healthy" else "⚠️"
            print(f"  {status_icon} {agent['agent_id']}")
            print(f"     Inbox: {'✅' if agent['has_inbox'] else '❌'} ({agent['inbox_message_count']} messages)")
            print(f"     Status: {'✅' if agent['has_status'] else '❌'}")
            print(f"     Passdown: {'✅' if agent['has_passdown'] else '⚠️'}")
            if agent["issues"]:
                for issue in agent["issues"]:
                    print(f"     ⚠️ {issue}")
            print()
    
    # Invalid directories
    if report["invalid_directories"]:
        print("❌ INVALID DIRECTORIES")
        print("-" * 70)
        for invalid in report["invalid_directories"]:
            print(f"  ❌ {invalid['name']}")
            print(f"     Type: {invalid['type']}")
            print(f"     Recommendation: {invalid['recommendation']}")
            print()
    
    # Overall health
    print("=" * 70)
    if stats["invalid_directories"] == 0 and stats["missing_inboxes"] == 0 and stats["missing_status"] == 0:
        print("✅ WORKSPACE HEALTH: EXCELLENT")
    elif stats["invalid_directories"] == 0:
        print("⚠️ WORKSPACE HEALTH: GOOD (some minor issues)")
    else:
        print("❌ WORKSPACE HEALTH: NEEDS ATTENTION")
    print("=" * 70)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check agent workspace health",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--workspace-root",
        type=str,
        default="agent_workspaces",
        help="Path to agent workspaces directory (default: agent_workspaces)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of formatted text"
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Save report to file (JSON format)"
    )
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace_root)
    report = check_workspace_structure(workspace_root)
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_health_report(report)
    
    if args.save:
        with open(args.save, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Report saved to: {args.save}")


if __name__ == "__main__":
    main()

