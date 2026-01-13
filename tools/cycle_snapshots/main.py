"""
Cycle Snapshot System - Main CLI
=================================

CLI entrypoint for cycle snapshot generation.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines where possible)

<!-- SSOT Domain: tools -->
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from .data_collectors.agent_status_collector import collect_all_agent_status
from .data_collectors.task_log_collector import parse_task_log
from .data_collectors.git_collector import analyze_git_activity
from .aggregators.snapshot_aggregator import aggregate_snapshot
from .processors.report_generator import generate_markdown_report
from .core.snapshot_models import CycleSnapshot

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_previous_snapshot_info(
    output_dir: Path
) -> tuple[Optional[int], Optional[datetime]]:
    """
    Get previous snapshot cycle number and timestamp.
    
    Args:
        output_dir: Output directory for snapshots
    
    Returns:
        Tuple of (previous_cycle, previous_timestamp)
    """
    # Look for most recent snapshot JSON file
    snapshot_files = sorted(
        output_dir.glob("cycle_snapshot_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if not snapshot_files:
        return None, None
    
    try:
        with open(snapshot_files[0], 'r', encoding='utf-8') as f:
            prev_snapshot = json.load(f)
        
        metadata = prev_snapshot.get("snapshot_metadata", {})
        prev_cycle = metadata.get("cycle")
        prev_timestamp_str = metadata.get("date")
        
        if prev_timestamp_str:
            prev_timestamp = datetime.fromisoformat(prev_timestamp_str.replace('Z', '+00:00'))
        else:
            prev_timestamp = None
        
        return prev_cycle, prev_timestamp
    
    except Exception as e:
        logger.warning(f"Error reading previous snapshot: {e}")
        return None, None


def calculate_cycle_number(
    workspace_root: Path,
    output_dir: Path
) -> int:
    """
    Calculate current cycle number.
    
    Args:
        workspace_root: Root workspace path
        output_dir: Output directory for snapshots
    
    Returns:
        Current cycle number
    """
    prev_cycle, _ = get_previous_snapshot_info(output_dir)
    
    if prev_cycle is not None:
        return prev_cycle + 1
    
    # Fallback: try to get from agent status files
    try:
        agents = collect_all_agent_status(workspace_root)
        if agents:
            # Get max cycle_count from agents
            max_cycle = max(
                (agent.get("cycle_count", 0) for agent in agents.values()),
                default=0
            )
            return max_cycle + 1
    except Exception as e:
        logger.warning(f"Error calculating cycle from agents: {e}")
    
    return 1


def save_snapshot(
    snapshot: CycleSnapshot,
    output_dir: Path
) -> tuple[Path, Path]:
    """
    Save snapshot JSON and markdown report.
    
    Args:
        snapshot: CycleSnapshot instance
        output_dir: Output directory
    
    Returns:
        Tuple of (json_path, report_path)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cycle_num = snapshot.metadata.cycle_number
    timestamp = snapshot.metadata.timestamp.strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_filename = f"cycle_snapshot_{cycle_num}_{timestamp}.json"
    json_path = output_dir / json_filename
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot.to_dict(), f, indent=2, default=str)
    
    logger.info(f"✅ Snapshot JSON saved: {json_path}")
    
    # Save Markdown report
    report_filename = f"cycle_snapshot_{cycle_num}_{timestamp}.md"
    report_path = output_dir / report_filename
    
    report_content = generate_markdown_report(snapshot.to_dict())
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    logger.info(f"✅ Snapshot report saved: {report_path}")
    
    return json_path, report_path


def main() -> int:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Generate cycle snapshot of project state"
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="Root workspace path (default: current directory)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: reports/cycle_snapshots/)"
    )
    parser.add_argument(
        "--since",
        type=str,
        default=None,
        help="Timestamp to analyze since (ISO format, defaults to 24 hours ago)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Determine output directory
    if args.output_dir is None:
        output_dir = args.workspace_root / "reports" / "cycle_snapshots"
    else:
        output_dir = Path(args.output_dir)
    
    try:
        logger.info("🚀 Starting cycle snapshot generation...")
        
        # Calculate cycle number
        cycle_num = calculate_cycle_number(args.workspace_root, output_dir)
        logger.info(f"📊 Cycle number: {cycle_num}")
        
        # Get previous snapshot info
        prev_cycle, prev_timestamp = get_previous_snapshot_info(output_dir)
        
        # Determine since timestamp
        if args.since:
            since_timestamp = datetime.fromisoformat(args.since)
        elif prev_timestamp:
            since_timestamp = prev_timestamp
        else:
            since_timestamp = datetime.now() - timedelta(hours=24)
        
        logger.info(f"📅 Analyzing since: {since_timestamp.isoformat()}")
        
        # Collect data
        logger.info("📥 Collecting agent status...")
        agent_status = collect_all_agent_status(args.workspace_root)
        
        logger.info("📋 Parsing task log...")
        task_log = parse_task_log(args.workspace_root)
        
        logger.info("🔍 Analyzing git activity...")
        git_activity = analyze_git_activity(args.workspace_root, since_timestamp)
        
        # Aggregate snapshot
        logger.info("🔗 Aggregating snapshot...")
        all_data = {
            "agent_status": agent_status,
            "task_log": task_log,
            "git_activity": git_activity,
        }
        
        snapshot = aggregate_snapshot(
            all_data=all_data,
            cycle_num=cycle_num,
            workspace_root=args.workspace_root,
            previous_cycle=prev_cycle,
            previous_timestamp=prev_timestamp,
        )
        
        # Save snapshot
        logger.info("💾 Saving snapshot...")
        json_path, report_path = save_snapshot(snapshot, output_dir)
        
        logger.info("✅ Cycle snapshot generation complete!")
        logger.info(f"   JSON: {json_path}")
        logger.info(f"   Report: {report_path}")
        
        return 0
    
    except Exception as e:
        logger.error(f"❌ Error generating snapshot: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

