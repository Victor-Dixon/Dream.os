#!/usr/bin/env python3
"""
Tool Metrics - Execution Time and Success Rate Tracking
========================================================

Tracks performance metrics for tool execution including:
- Execution time
- Success/failure rates
- Usage patterns
- Performance trends

Usage:
    python tools/metrics.py --record tool_name success 2.34
    python tools/metrics.py --stats tool_name
    python tools/metrics.py --report
"""

import json
import time
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta


@dataclass
class ToolExecution:
    """Record of a single tool execution"""
    tool_name: str
    timestamp: str
    status: str  # "success", "error", "timeout"
    execution_time: float
    error_message: Optional[str] = None
    command_line: Optional[str] = None


@dataclass
class ToolMetrics:
    """Aggregated metrics for a tool"""
    tool_name: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    min_execution_time: float = float('inf')
    max_execution_time: float = 0.0
    success_rate: float = 0.0
    last_execution: Optional[str] = None
    first_execution: Optional[str] = None

    def update(self, execution: ToolExecution):
        """Update metrics with new execution data"""
        self.total_executions += 1

        if execution.status == "success":
            self.successful_executions += 1
        else:
            self.failed_executions += 1

        self.total_execution_time += execution.execution_time
        self.average_execution_time = self.total_execution_time / self.total_executions

        self.min_execution_time = min(self.min_execution_time, execution.execution_time)
        self.max_execution_time = max(self.max_execution_time, execution.execution_time)

        self.success_rate = (self.successful_executions / self.total_executions) * 100

        if not self.first_execution:
            self.first_execution = execution.timestamp
        self.last_execution = execution.timestamp


class ToolMetricsTracker:
    """Tracks and analyzes tool execution metrics"""

    def __init__(self):
        self.metrics_dir = Path(__file__).parent
        self.metrics_file = self.metrics_dir / "metrics.json"
        self.executions_file = self.metrics_dir / "executions.json"
        self.metrics: Dict[str, ToolMetrics] = {}
        self.executions: List[ToolExecution] = []
        self._load_data()

    def _load_data(self):
        """Load metrics and execution data from files"""
        # Load executions
        if self.executions_file.exists():
            try:
                with open(self.executions_file, 'r') as f:
                    executions_data = json.load(f)
                    self.executions = [ToolExecution(**data) for data in executions_data]
            except Exception as e:
                print(f"Warning: Could not load executions: {e}")

        # Rebuild metrics from executions
        self.metrics = {}
        for execution in self.executions:
            if execution.tool_name not in self.metrics:
                self.metrics[execution.tool_name] = ToolMetrics(execution.tool_name)

            self.metrics[execution.tool_name].update(execution)

    def _save_data(self):
        """Save metrics and execution data to files"""
        # Save executions
        executions_data = [asdict(exec) for exec in self.executions]
        with open(self.executions_file, 'w') as f:
            json.dump(executions_data, f, indent=2, default=str)

        # Save metrics summary
        metrics_data = {name: asdict(metric) for name, metric in self.metrics.items()}
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics_data, f, indent=2, default=str)

    def record_execution(self, tool_name: str, status: str, execution_time: float,
                        error_message: Optional[str] = None, command_line: Optional[str] = None):
        """Record a tool execution"""
        execution = ToolExecution(
            tool_name=tool_name,
            timestamp=datetime.now().isoformat(),
            status=status,
            execution_time=execution_time,
            error_message=error_message,
            command_line=command_line
        )

        self.executions.append(execution)

        if tool_name not in self.metrics:
            self.metrics[tool_name] = ToolMetrics(tool_name)

        self.metrics[tool_name].update(execution)
        self._save_data()

    def get_tool_metrics(self, tool_name: str) -> Optional[ToolMetrics]:
        """Get metrics for a specific tool"""
        return self.metrics.get(tool_name)

    def get_all_metrics(self) -> Dict[str, ToolMetrics]:
        """Get metrics for all tools"""
        return self.metrics

    def get_recent_executions(self, tool_name: Optional[str] = None, days: int = 7) -> List[ToolExecution]:
        """Get recent executions within specified days"""
        cutoff = datetime.now() - timedelta(days=days)

        recent = []
        for execution in self.executions:
            if datetime.fromisoformat(execution.timestamp) > cutoff:
                if tool_name is None or execution.tool_name == tool_name:
                    recent.append(execution)

        return recent

    def generate_report(self, tool_name: Optional[str] = None) -> str:
        """Generate a comprehensive metrics report"""
        report = "# Tool Metrics Report\n"
        report += f"**Generated:** {datetime.now().isoformat()}\n\n"

        if tool_name:
            metrics = self.get_tool_metrics(tool_name)
            if not metrics:
                return f"No metrics found for tool: {tool_name}"

            report += f"## {tool_name} Metrics\n\n"
            report += f"- **Total Executions:** {metrics.total_executions}\n"
            report += f"- **Success Rate:** {metrics.success_rate:.1f}%\n"
            report += f"- **Successful:** {metrics.successful_executions}\n"
            report += f"- **Failed:** {metrics.failed_executions}\n"
            report += f"- **Avg Execution Time:** {metrics.average_execution_time:.2f}s\n"
            report += f"- **Min Execution Time:** {metrics.min_execution_time:.2f}s\n"
            report += f"- **Max Execution Time:** {metrics.max_execution_time:.2f}s\n"
            report += f"- **First Execution:** {metrics.first_execution}\n"
            report += f"- **Last Execution:** {metrics.last_execution}\n"

            # Recent executions
            recent = self.get_recent_executions(tool_name, days=7)
            if recent:
                report += f"\n### Recent Executions (Last 7 days)\n"
                for execution in recent[-5:]:  # Show last 5
                    status_emoji = "✅" if execution.status == "success" else "❌"
                    report += f"- {execution.timestamp}: {status_emoji} {execution.status} ({execution.execution_time:.2f}s)\n"

        else:
            # Overall report
            total_executions = sum(m.total_executions for m in self.metrics.values())
            total_successful = sum(m.successful_executions for m in self.metrics.values())
            avg_success_rate = statistics.mean(m.success_rate for m in self.metrics.values()) if self.metrics else 0

            report += "## Overall Statistics\n\n"
            report += f"- **Total Tools Tracked:** {len(self.metrics)}\n"
            report += f"- **Total Executions:** {total_executions}\n"
            report += f"- **Average Success Rate:** {avg_success_rate:.1f}%\n"
            report += f"- **Successful Executions:** {total_successful}\n"

            report += "\n## Tool Performance Summary\n\n"
            report += "| Tool | Executions | Success Rate | Avg Time |\n"
            report += "|------|------------|--------------|----------|\n"

            for name, metrics in sorted(self.metrics.items(), key=lambda x: x[1].total_executions, reverse=True):
                report += f"| {name} | {metrics.total_executions} | {metrics.success_rate:.1f}% | {metrics.average_execution_time:.2f}s |\n"

        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Tool Metrics - Execution Tracking")
    parser.add_argument("--record", nargs=3, metavar=("TOOL", "STATUS", "TIME"),
                       help="Record tool execution (tool_name status execution_time)")
    parser.add_argument("--stats", metavar="TOOL", help="Show statistics for specific tool")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("--recent", nargs="?", const=7, type=int, metavar="DAYS",
                       help="Show recent executions (default: 7 days)")

    args = parser.parse_args()

    tracker = ToolMetricsTracker()

    if args.record:
        tool_name, status, time_str = args.record
        try:
            execution_time = float(time_str)
            tracker.record_execution(tool_name, status, execution_time)
            print(f"✅ Recorded execution: {tool_name} {status} {execution_time}s")
        except ValueError:
            print("❌ Invalid execution time. Must be a number.")

    elif args.stats:
        report = tracker.generate_report(args.stats)
        print(report)

    elif args.report:
        report = tracker.generate_report()
        print(report)

    elif args.recent is not None:
        executions = tracker.get_recent_executions(days=args.recent)
        print(f"Recent executions (last {args.recent} days):\n")
        for execution in executions[-10:]:  # Show last 10
            print(f"{execution.timestamp}: {execution.tool_name} {execution.status} ({execution.execution_time:.2f}s)")

    else:
        print("Use --record, --stats, --report, or --recent")


if __name__ == "__main__":
    main()