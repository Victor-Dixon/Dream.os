#!/usr/bin/env python3
"""
Cycle Snapshot System - Main CLI
================================

Central nervous system for collecting, aggregating, and distributing
swarm state across all systems.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines)
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add tools directory to path for imports
tools_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tools_dir))

from cycle_snapshots.data_collectors.agent_status_collector import collect_all_agent_status
from cycle_snapshots.data_collectors.task_log_collector import parse_task_log
from cycle_snapshots.data_collectors.git_collector import analyze_git_activity
from cycle_snapshots.aggregators.snapshot_aggregator import aggregate_snapshot
from cycle_snapshots.core.snapshot_models import CycleSnapshot

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point for cycle snapshot system."""
    import argparse

    parser = argparse.ArgumentParser(description="Cycle Snapshot System")
    parser.add_argument("--cycle", type=int, default=1, help="Cycle number")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace root directory")
    parser.add_argument("--since-days", type=int, default=7, help="Days to analyze git activity for")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        workspace_root = Path(args.workspace).resolve()

        # Collect data from all sources
        print("🔄 Collecting agent status data...")
        agent_status_data = collect_all_agent_status(workspace_root)

        print("📋 Analyzing task log...")
        task_data = parse_task_log(workspace_root)

        print("🔍 Analyzing git activity...")
        since_timestamp = datetime.now() - timedelta(days=args.since_days)
        git_data = analyze_git_activity(workspace_root, since_timestamp)

        # Aggregate all data
        print("⚡ Aggregating snapshot data...")
        all_data = {
            "agent_status": agent_status_data,
            "task_metrics": task_data,
            "git_activity": git_data,
            "metrics": {
                "agent_status": agent_status_data,
                "task_metrics": task_data,
                "git_metrics": git_data.get("metrics", {})
            }
        }

        snapshot_dict = aggregate_snapshot(all_data)

        # Create snapshot object
        snapshot = CycleSnapshot(
            metadata=snapshot_dict["snapshot_metadata"],
            project_state=snapshot_dict["project_state"],
            agent_status={},  # Would be populated from agent_status_data
            task_metrics=snapshot_dict.get("task_metrics", {}),
            git_metrics=snapshot_dict.get("git_activity", {}).get("metrics", {}),
            mcp_data=snapshot_dict.get("mcp_data", {})
        )

        # Output result
        if args.output:
            output_file = Path(args.output)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot.to_dict(), f, indent=2, ensure_ascii=False)

            print(f"✅ Snapshot saved to {output_file}")
        else:
            print(json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False))

    except Exception as e:
        logger.error(f"Snapshot generation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()