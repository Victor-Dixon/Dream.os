#!/usr/bin/env python3
"""
Consolidation Monitoring and Tracking System

This script implements comprehensive monitoring and reporting for consolidation
operations across the repository. It provides:

1. Real-time consolidation progress tracking
2. Automated status reporting and alerts
3. Performance metrics and analytics
4. Integration with agent workspaces
5. Web-based dashboard generation

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import os
import sys
import json
import time
import psutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@dataclass
class ConsolidationMetrics:
    """Metrics for consolidation operations"""
    timestamp: str
    phase: str
    operation: str
    agent_id: str
    files_processed: int = 0
    files_removed: int = 0
    space_saved_bytes: int = 0
    space_saved_mb: float = 0.0
    duration_seconds: float = 0.0
    success_rate: float = 0.0
    error_count: int = 0
    performance_score: float = 0.0  # 0-100 scale

@dataclass
class SystemHealthMetrics:
    """System health metrics during consolidation"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_io: Dict[str, int]
    active_processes: int
    consolidation_impact: str  # "low", "medium", "high"

@dataclass
class ConsolidationDashboard:
    """Consolidation dashboard data"""
    last_updated: str
    total_space_saved_mb: float
    total_files_removed: int
    active_operations: int
    completed_operations: int
    error_rate: float
    performance_trend: List[float]
    agent_performance: Dict[str, Dict]
    phase_progress: Dict[str, Dict]
    alerts: List[str]
    recommendations: List[str]

class ConsolidationMonitor:
    """Monitors consolidation operations and generates reports"""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.monitoring_dir = self.base_path / "monitoring" / "consolidation"
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)

        self.metrics_file = self.monitoring_dir / "consolidation_metrics.jsonl"
        self.health_file = self.monitoring_dir / "system_health.jsonl"
        self.dashboard_file = self.monitoring_dir / "dashboard.json"

        # Initialize data structures
        self.metrics_history: List[ConsolidationMetrics] = []
        self.health_history: List[SystemHealthMetrics] = []
        self.current_dashboard: Optional[ConsolidationDashboard] = None

        self.load_existing_data()

    def load_existing_data(self):
        """Load existing monitoring data"""
        # Load metrics
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            metric = ConsolidationMetrics(**data)
                            self.metrics_history.append(metric)
            except Exception as e:
                print(f"Warning: Could not load metrics: {e}")

        # Load health data
        if self.health_file.exists():
            try:
                with open(self.health_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            health = SystemHealthMetrics(**data)
                            self.health_history.append(health)
            except Exception as e:
                print(f"Warning: Could not load health data: {e}")

    def record_operation_metrics(self, phase: str, operation: str, agent_id: str,
                               files_processed: int, files_removed: int,
                               space_saved_bytes: int, duration_seconds: float,
                               error_count: int = 0):
        """Record metrics for a consolidation operation"""

        space_saved_mb = space_saved_bytes / (1024 * 1024)
        success_rate = (files_processed - error_count) / files_processed if files_processed > 0 else 0
        performance_score = min(100, (success_rate * 100) - (error_count * 5) + (space_saved_mb * 2))

        metric = ConsolidationMetrics(
            timestamp=datetime.now().isoformat(),
            phase=phase,
            operation=operation,
            agent_id=agent_id,
            files_processed=files_processed,
            files_removed=files_removed,
            space_saved_bytes=space_saved_bytes,
            space_saved_mb=round(space_saved_mb, 2),
            duration_seconds=round(duration_seconds, 2),
            success_rate=round(success_rate, 2),
            error_count=error_count,
            performance_score=round(performance_score, 1)
        )

        self.metrics_history.append(metric)
        self._append_to_file(self.metrics_file, metric)

        print(f"📊 Recorded metrics for {operation}: {files_removed} files removed, "
              f"{space_saved_mb:.2f} MB saved, performance score: {performance_score:.1f}")

    def record_system_health(self):
        """Record current system health metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()

            # Determine consolidation impact
            if cpu_percent > 80 or memory.percent > 85:
                impact = "high"
            elif cpu_percent > 50 or memory.percent > 70:
                impact = "medium"
            else:
                impact = "low"

            health = SystemHealthMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=round(cpu_percent, 1),
                memory_percent=round(memory.percent, 1),
                disk_usage_percent=round(disk.percent, 1),
                network_io={
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv
                },
                active_processes=len(psutil.pids()),
                consolidation_impact=impact
            )

            self.health_history.append(health)
            self._append_to_file(self.health_file, health)

        except Exception as e:
            print(f"Warning: Could not record system health: {e}")

    def _append_to_file(self, file_path: Path, data):
        """Append data to a JSON Lines file"""
        try:
            with open(file_path, 'a') as f:
                json.dump(asdict(data), f)
                f.write('\n')
        except Exception as e:
            print(f"Error appending to {file_path}: {e}")

    def generate_dashboard(self) -> ConsolidationDashboard:
        """Generate the current consolidation dashboard"""

        if not self.metrics_history:
            return ConsolidationDashboard(
                last_updated=datetime.now().isoformat(),
                total_space_saved_mb=0.0,
                total_files_removed=0,
                active_operations=0,
                completed_operations=0,
                error_rate=0.0,
                performance_trend=[],
                agent_performance={},
                phase_progress={},
                alerts=["No consolidation data available"],
                recommendations=["Run initial consolidation operations"]
            )

        # Calculate summary metrics
        total_space_saved_mb = sum(m.space_saved_mb for m in self.metrics_history)
        total_files_removed = sum(m.files_removed for m in self.metrics_history)
        completed_operations = len(self.metrics_history)
        active_operations = 0  # Would be calculated from task status in real implementation

        # Calculate error rate
        total_operations = len(self.metrics_history)
        error_operations = len([m for m in self.metrics_history if m.error_count > 0])
        error_rate = (error_operations / total_operations) if total_operations > 0 else 0

        # Calculate performance trend (last 10 operations)
        recent_metrics = self.metrics_history[-10:]
        performance_trend = [m.performance_score for m in recent_metrics]

        # Calculate agent performance
        agent_performance = defaultdict(lambda: {
            "total_operations": 0,
            "avg_performance": 0.0,
            "total_space_saved": 0.0,
            "total_files_removed": 0
        })

        for metric in self.metrics_history:
            agent_performance[metric.agent_id]["total_operations"] += 1
            agent_performance[metric.agent_id]["total_space_saved"] += metric.space_saved_mb
            agent_performance[metric.agent_id]["total_files_removed"] += metric.files_removed

        # Calculate averages
        for agent_data in agent_performance.values():
            if agent_data["total_operations"] > 0:
                agent_data["avg_performance"] = sum(
                    m.performance_score for m in self.metrics_history
                    if m.agent_id in agent_performance
                ) / agent_data["total_operations"]

        # Calculate phase progress
        phase_progress = defaultdict(lambda: {
            "total_operations": 0,
            "completed_operations": 0,
            "total_space_saved": 0.0,
            "avg_performance": 0.0
        })

        for metric in self.metrics_history:
            phase_progress[metric.phase]["total_operations"] += 1
            phase_progress[metric.phase]["completed_operations"] += 1
            phase_progress[metric.phase]["total_space_saved"] += metric.space_saved_mb

        # Calculate phase averages
        for phase_data in phase_progress.values():
            if phase_data["completed_operations"] > 0:
                phase_data["avg_performance"] = sum(
                    m.performance_score for m in self.metrics_history
                    if m.phase in phase_progress
                ) / phase_data["completed_operations"]

        # Generate alerts and recommendations
        alerts = []
        recommendations = []

        if error_rate > 0.1:
            alerts.append(f"High error rate detected: {error_rate:.1%}")
            recommendations.append("Review error patterns and improve operation reliability")

        if total_space_saved_mb < 50:
            alerts.append("Low space savings detected")
            recommendations.append("Verify consolidation operations are running correctly")

        # Check for system health issues
        recent_health = self.health_history[-5:] if self.health_history else []
        high_impact_count = len([h for h in recent_health if h.consolidation_impact == "high"])
        if high_impact_count > 2:
            alerts.append("High system impact detected during consolidation")
            recommendations.append("Consider running consolidation during off-peak hours")

        dashboard = ConsolidationDashboard(
            last_updated=datetime.now().isoformat(),
            total_space_saved_mb=round(total_space_saved_mb, 2),
            total_files_removed=total_files_removed,
            active_operations=active_operations,
            completed_operations=completed_operations,
            error_rate=round(error_rate, 3),
            performance_trend=performance_trend,
            agent_performance=dict(agent_performance),
            phase_progress=dict(phase_progress),
            alerts=alerts,
            recommendations=recommendations
        )

        self.current_dashboard = dashboard
        return dashboard

    def save_dashboard(self):
        """Save the current dashboard to file"""
        if self.current_dashboard:
            try:
                with open(self.dashboard_file, 'w') as f:
                    json.dump(asdict(self.current_dashboard), f, indent=2)
                print(f"Dashboard saved to {self.dashboard_file}")
            except Exception as e:
                print(f"Error saving dashboard: {e}")

    def generate_html_report(self) -> str:
        """Generate an HTML report for the dashboard"""
        if not self.current_dashboard:
            self.generate_dashboard()

        dashboard = self.current_dashboard
        if not dashboard:
            return "<h1>No dashboard data available</h1>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Consolidation Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .metric {{ background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .alert {{ background: #ffebee; border-left: 5px solid #f44336; padding: 10px; margin: 10px 0; }}
                .recommendation {{ background: #e8f5e8; border-left: 5px solid #4caf50; padding: 10px; margin: 10px 0; }}
                .performance {{ color: #2196f3; font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>🔄 Consolidation Dashboard</h1>
            <p><strong>Last Updated:</strong> {dashboard.last_updated}</p>

            <div class="metric">
                <h2>📊 Summary Metrics</h2>
                <ul>
                    <li><strong>Total Space Saved:</strong> {dashboard.total_space_saved_mb} MB</li>
                    <li><strong>Files Removed:</strong> {dashboard.total_files_removed}</li>
                    <li><strong>Completed Operations:</strong> {dashboard.completed_operations}</li>
                    <li><strong>Error Rate:</strong> {dashboard.error_rate:.1%}</li>
                </ul>
            </div>

            <div class="metric">
                <h2>👥 Agent Performance</h2>
                <table>
                    <tr><th>Agent</th><th>Operations</th><th>Avg Performance</th><th>Space Saved (MB)</th><th>Files Removed</th></tr>
        """

        for agent_id, data in dashboard.agent_performance.items():
            html += f"""
                    <tr>
                        <td>{agent_id}</td>
                        <td>{data['total_operations']}</td>
                        <td class="performance">{data['avg_performance']:.1f}</td>
                        <td>{data['total_space_saved']:.1f}</td>
                        <td>{data['total_files_removed']}</td>
                    </tr>
            """

        html += """
                </table>
            </div>

            <div class="metric">
                <h2>📈 Phase Progress</h2>
                <table>
                    <tr><th>Phase</th><th>Operations</th><th>Space Saved (MB)</th><th>Avg Performance</th></tr>
        """

        for phase, data in dashboard.phase_progress.items():
            html += f"""
                    <tr>
                        <td>{phase.upper()}</td>
                        <td>{data['completed_operations']}</td>
                        <td>{data['total_space_saved']:.1f}</td>
                        <td class="performance">{data['avg_performance']:.1f}</td>
                    </tr>
            """

        html += """
                </table>
            </div>
        """

        # Add alerts
        if dashboard.alerts:
            html += '<div class="alert"><h3>🚨 Alerts</h3><ul>'
            for alert in dashboard.alerts:
                html += f"<li>{alert}</li>"
            html += "</ul></div>"

        # Add recommendations
        if dashboard.recommendations:
            html += '<div class="recommendation"><h3>💡 Recommendations</h3><ul>'
            for rec in dashboard.recommendations:
                html += f"<li>{rec}</li>"
            html += "</ul></div>"

        html += """
        </body>
        </html>
        """

        return html

    def save_html_report(self):
        """Save the HTML report to file"""
        html_content = self.generate_html_report()
        html_file = self.monitoring_dir / "consolidation_dashboard.html"

        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML report saved to {html_file}")
        except Exception as e:
            print(f"Error saving HTML report: {e}")

    def run_monitoring_cycle(self):
        """Run a complete monitoring cycle"""
        print("🔍 Running Consolidation Monitoring Cycle")
        print("=" * 50)

        # Record system health
        print("📊 Recording system health...")
        self.record_system_health()

        # Generate dashboard
        print("📈 Generating dashboard...")
        dashboard = self.generate_dashboard()
        self.save_dashboard()

        # Generate HTML report
        print("🌐 Generating HTML report...")
        self.save_html_report()

        print("\n✅ Monitoring cycle complete!")
        print(f"📊 Total space saved: {dashboard.total_space_saved_mb} MB")
        print(f"📁 Files removed: {dashboard.total_files_removed}")
        print(f"⚡ Completed operations: {dashboard.completed_operations}")
        print(f"🚨 Alerts: {len(dashboard.alerts)}")
        print(f"💡 Recommendations: {len(dashboard.recommendations)}")

        return dashboard

    def simulate_operation_data(self):
        """Simulate operation data for testing"""
        operations = [
            ("phase1", "quickstart_deduplication", "Agent-7"),
            ("phase1", "cache_cleanup", "Agent-3"),
            ("phase1", "archive_consolidation", "Agent-8"),
            ("phase1", "status_standardization", "Agent-1"),
        ]

        import random
        for phase, operation, agent in operations:
            files_processed = random.randint(10, 100)
            files_removed = random.randint(1, files_processed)
            space_saved = random.randint(100000, 10000000)  # 0.1-10 MB
            duration = random.uniform(1.0, 60.0)
            errors = random.randint(0, 3)

            self.record_operation_metrics(
                phase, operation, agent,
                files_processed, files_removed, space_saved, duration, errors
            )


def main():
    """Main entry point for consolidation monitoring"""
    print("Consolidation Monitoring and Tracking System")
    print("This script monitors consolidation operations and generates reports.")
    print()

    monitor = ConsolidationMonitor()

    # For testing: simulate some operation data
    print("🧪 Adding simulated operation data...")
    monitor.simulate_operation_data()

    # Run monitoring cycle
    dashboard = monitor.run_monitoring_cycle()

    print("\n📊 Dashboard Summary:")
    print(f"  Space Saved: {dashboard.total_space_saved_mb} MB")
    print(f"  Files Removed: {dashboard.total_files_removed}")
    print(f"  Error Rate: {dashboard.error_rate:.1%}")

    if dashboard.alerts:
        print("\n🚨 Alerts:")
        for alert in dashboard.alerts:
            print(f"  - {alert}")

    if dashboard.recommendations:
        print("\n💡 Recommendations:")
        for rec in dashboard.recommendations:
            print(f"  - {rec}")

    print("\n✅ Monitoring system ready!")


if __name__ == "__main__":
    main()