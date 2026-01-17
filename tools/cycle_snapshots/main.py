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

# Add repository root to path for imports (needed for src/ access)
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

# Also set as default workspace root
DEFAULT_WORKSPACE_ROOT = repo_root

from tools.cycle_snapshots.data_collectors.agent_status_collector import collect_all_agent_status
from tools.cycle_snapshots.data_collectors.task_log_collector import parse_task_log
from tools.cycle_snapshots.data_collectors.git_collector import analyze_git_activity
from tools.cycle_snapshots.aggregators.snapshot_aggregator import aggregate_snapshot
from tools.cycle_snapshots.core.snapshot_models import (
    CycleSnapshot, SnapshotMetadata, AgentStatus, TaskMetrics, GitMetrics
)
from tools.cycle_snapshots.processors.report_generator import generate_markdown_report

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point for cycle snapshot system."""
    import argparse

    parser = argparse.ArgumentParser(description="Cycle Snapshot System")
    parser.add_argument("--cycle", type=int, default=1, help="Cycle number")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    parser.add_argument("--report", type=str, help="Generate markdown report to file path")
    parser.add_argument("--workspace", type=str, default=None, help="Workspace root directory (default: auto-detect repo root)")
    parser.add_argument("--since-days", type=int, default=7, help="Days to analyze git activity for")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Auto-detect workspace root if not provided
        if args.workspace is None:
            workspace_root = DEFAULT_WORKSPACE_ROOT.resolve()
        else:
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

        snapshot_dict = aggregate_snapshot(all_data, args.cycle)

        # Create proper SnapshotMetadata object
        metadata_dict = snapshot_dict["snapshot_metadata"]
        metadata = SnapshotMetadata(
            cycle_number=metadata_dict["cycle_number"],
            snapshot_version=metadata_dict.get("snapshot_version", "0.1.0"),
            generated_at=datetime.fromisoformat(metadata_dict["generated_at"]) if "generated_at" in metadata_dict else datetime.now(),
            system=metadata_dict.get("system", "Cycle Snapshot System"),
            purpose=metadata_dict.get("purpose", "Central nervous system data collection for swarm coordination"),
            reset_status=metadata_dict.get("reset_status", {})
        )

        # Convert agent status data to AgentStatus objects
        agent_status_objects = {}
        for agent_id, status_data in agent_status_data.items():
            if isinstance(status_data, dict) and "agent_id" in status_data:
                try:
                    # Convert timestamp string to datetime if needed
                    last_updated = status_data.get("last_updated")
                    if isinstance(last_updated, str):
                        last_updated = datetime.fromisoformat(last_updated)
                    elif not isinstance(last_updated, datetime):
                        last_updated = datetime.now()

                    agent_status = AgentStatus(
                        agent_id=status_data.get("agent_id", agent_id),
                        agent_name=status_data.get("agent_name", ""),
                        status=status_data.get("status", "unknown"),
                        fsm_state=status_data.get("fsm_state", "unknown"),
                        current_phase=status_data.get("current_phase", ""),
                        last_updated=last_updated,
                        current_mission=status_data.get("current_mission", ""),
                        mission_priority=status_data.get("mission_priority", "NORMAL"),
                        current_tasks=status_data.get("current_tasks", []),
                        completed_tasks=status_data.get("completed_tasks", []),
                        achievements=status_data.get("achievements", []),
                    )
                    agent_status_objects[agent_id] = agent_status
                except Exception as e:
                    logger.warning(f"Failed to convert status for {agent_id}: {e}")

        # Convert task metrics to TaskMetrics object
        task_metrics_data = snapshot_dict.get("task_metrics", {})
        if isinstance(task_metrics_data, dict):
            try:
                # Only pass fields that exist in TaskMetrics
                valid_fields = {k: v for k, v in task_metrics_data.items()
                               if k in TaskMetrics.__dataclass_fields__}
                task_metrics = TaskMetrics(**valid_fields)
            except Exception as e:
                logger.warning(f"Failed to convert task metrics: {e}")
                task_metrics = TaskMetrics()
        else:
            task_metrics = TaskMetrics()

        # Convert git metrics to GitMetrics object
        git_metrics_data = snapshot_dict.get("git_activity", {}).get("metrics", {})
        if isinstance(git_metrics_data, dict):
            try:
                # Only pass fields that exist in GitMetrics
                valid_fields = {k: v for k, v in git_metrics_data.items()
                               if k in GitMetrics.__dataclass_fields__}
                git_metrics = GitMetrics(**valid_fields)
            except Exception as e:
                logger.warning(f"Failed to convert git metrics: {e}")
                git_metrics = GitMetrics()
        else:
            git_metrics = GitMetrics()

        # Create snapshot object
        snapshot = CycleSnapshot(
            metadata=metadata,
            project_state=snapshot_dict["project_state"],
            agent_status=agent_status_objects,
            task_metrics=task_metrics,
            git_metrics=git_metrics,
            mcp_data=snapshot_dict.get("mcp_data", {}),
            collected_at=datetime.fromisoformat(snapshot_dict["collected_at"])
        )

        # Generate markdown report if requested
        if args.report:
            report_file = Path(args.report)
            report_file.parent.mkdir(parents=True, exist_ok=True)

            report_content = generate_markdown_report(snapshot.to_dict())
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)

            print(f"📊 Report saved to {report_file}")

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