#!/usr/bin/env python3
"""
Repository Monitor - Phase 4 Continuous Scanning & Monitoring
===========================================================

Continuous repository scanning and monitoring system for tracking repository evolution.

<!-- SSOT Domain: monitoring -->

Navigation References:
├── Related Files:
│   ├── Project Scanner → tools/project_scanner.py
│   ├── Analytics Engine → src/core/analytics/engines/realtime_analytics_engine.py
│   ├── FastAPI Integration → src/web/fastapi_app.py
│   └── Dashboard Integration → src/web/static/js/repository-monitor.js
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Monitoring Guide → docs/monitoring/repository_monitoring.md
│   └── Analytics Spec → PHASE_5_2_ADVANCED_ANALYTICS_SPEC.md
└── Testing:
    └── Integration Tests → tests/integration/test_repository_monitor.py

Features:
- Continuous repository scanning with configurable intervals
- Trend analysis and anomaly detection
- Automated alerts for significant changes
- Historical data retention and analysis
- Integration with real-time analytics

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import threading

logger = logging.getLogger(__name__)


@dataclass
class RepositorySnapshot:
    """Represents a snapshot of repository state at a point in time."""
    timestamp: float
    total_files: int
    total_size_bytes: int
    file_type_distribution: Dict[str, int]
    directory_count: int
    largest_files: List[Dict[str, Any]]
    recent_changes: List[Dict[str, Any]]
    checksum: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RepositoryTrend:
    """Represents trends in repository evolution."""
    time_window_hours: int
    growth_rate_files_per_hour: float
    growth_rate_size_per_hour: float
    most_changed_files: List[Dict[str, Any]]
    anomaly_score: float
    recommendations: List[str]


class RepositoryMonitor:
    """
    Continuous repository monitoring system with trend analysis and alerting.

    Features:
    - Configurable scanning intervals
    - Historical trend analysis
    - Anomaly detection
    - Automated alerting
    - Performance optimization for large repositories
    """

    def __init__(self, repository_path: str, config: Dict[str, Any] = None):
        self.repository_path = Path(repository_path)
        self.config = config or self._default_config()

        # Monitoring state
        self.snapshots: List[RepositorySnapshot] = []
        self.is_monitoring = False
        self.monitoring_task = None
        self.alert_callbacks: List[Callable] = []

        # Performance optimization
        self.file_checksums: Dict[str, str] = {}
        self.last_scan_time = 0

        # Alert thresholds
        alerts_config = self.config.get("alerts", {})
        self.alert_thresholds = {
            "max_files_growth_rate": alerts_config.get("max_files_growth_rate", 100),
            "max_size_growth_rate_mb": alerts_config.get("max_size_growth_rate_mb", 50),
            "anomaly_score_threshold": alerts_config.get("anomaly_score_threshold", 2.0),
            "large_file_threshold_mb": alerts_config.get("large_file_threshold_mb", 10)
        }

        # Data retention
        self.max_snapshots = self.config.get("retention", {}).get("max_snapshots", 168)

    def _default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "scan_interval_seconds": 3600,  # 1 hour
            "retention": {
                "max_snapshots": 168,  # 1 week at 1/hour
                "max_age_days": 30
            },
            "alerts": {
                "max_files_growth_rate": 100,  # files per hour
                "max_size_growth_rate_mb": 50,  # MB per hour
                "anomaly_score_threshold": 2.0,
                "large_file_threshold_mb": 10
            },
            "performance": {
                "max_files_per_scan": 10000,
                "use_checksums": True,
                "ignore_patterns": [".git", "__pycache__", ".ruff_cache", "node_modules"]
            },
            "analysis": {
                "trend_windows": [1, 6, 24, 168],  # hours
                "anomaly_detection": True
            }
        }

    async def start_monitoring(self):
        """Start continuous repository monitoring."""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        logger.info(f"🧮 Starting repository monitoring for {self.repository_path}")

        # Initial scan
        await self._perform_scan()

        # Start monitoring loop
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())

    async def stop_monitoring(self):
        """Stop repository monitoring."""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Repository monitoring stopped")

    def add_alert_callback(self, callback: Callable):
        """Add a callback for alerts."""
        self.alert_callbacks.append(callback)

    async def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                await asyncio.sleep(self.config["scan_interval_seconds"])
                if self.is_monitoring:  # Check again in case stopped during sleep
                    await self._perform_scan()
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _perform_scan(self):
        """Perform a repository scan and analyze changes."""
        try:
            start_time = time.time()

            # Create snapshot
            snapshot = await self._create_snapshot()

            # Analyze changes
            changes = self._analyze_changes(snapshot)

            # Store snapshot
            self.snapshots.append(snapshot)

            # Cleanup old snapshots
            self._cleanup_old_snapshots()

            # Analyze trends
            if len(self.snapshots) >= 2:
                trends = self._analyze_trends()

                # Check for alerts
                alerts = self._check_alerts(snapshot, changes, trends)
                if alerts:
                    await self._trigger_alerts(alerts)

            scan_time = time.time() - start_time
            logger.info(f"📊 Repository scan completed in {scan_time:.2f}s - {snapshot.total_files} files, {snapshot.total_size_bytes / 1024 / 1024:.1f}MB")

        except Exception as e:
            logger.error(f"Failed to perform repository scan: {e}")

    async def _create_snapshot(self) -> RepositorySnapshot:
        """Create a snapshot of the current repository state."""
        total_files = 0
        total_size = 0
        file_types: Dict[str, int] = {}
        directories = 0
        largest_files = []
        recent_changes = []

        # Walk through repository
        ignore_patterns = set(self.config.get("performance", {}).get("ignore_patterns", [".git", "__pycache__", ".ruff_cache", "node_modules"]))

        for root, dirs, files in os.walk(self.repository_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            directories += 1

            for file in files:
                if total_files >= self.config.get("performance", {}).get("max_files_per_scan", 10000):
                    break

                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    file_size = stat.st_size
                    total_size += file_size
                    total_files += 1

                    # File type distribution
                    ext = file_path.suffix.lower() or 'no_extension'
                    file_types[ext] = file_types.get(ext, 0) + 1

                    # Track largest files
                    largest_files.append({
                        "path": str(file_path.relative_to(self.repository_path)),
                        "size_bytes": file_size,
                        "modified": stat.st_mtime
                    })

                    # Check for recent changes
                    if stat.st_mtime > self.last_scan_time:
                        recent_changes.append({
                            "path": str(file_path.relative_to(self.repository_path)),
                            "action": "modified",
                            "size_bytes": file_size,
                            "modified": stat.st_mtime
                        })

                    # Update checksums for change detection
                    if self.config.get("performance", {}).get("use_checksums", True):
                        file_checksum = self._calculate_file_checksum(file_path)
                        old_checksum = self.file_checksums.get(str(file_path))
                        if old_checksum and old_checksum != file_checksum:
                            recent_changes.append({
                                "path": str(file_path.relative_to(self.repository_path)),
                                "action": "content_changed",
                                "size_bytes": file_size,
                                "modified": stat.st_mtime
                            })
                        self.file_checksums[str(file_path)] = file_checksum

                except (OSError, IOError) as e:
                    logger.warning(f"Failed to process file {file_path}: {e}")

        # Sort and limit largest files
        largest_files.sort(key=lambda x: x["size_bytes"], reverse=True)
        largest_files = largest_files[:10]

        # Sort recent changes by modification time
        recent_changes.sort(key=lambda x: x["modified"], reverse=True)
        recent_changes = recent_changes[:50]

        # Create snapshot checksum
        snapshot_data = f"{total_files}_{total_size}_{len(file_types)}"
        checksum = hashlib.md5(snapshot_data.encode()).hexdigest()

        return RepositorySnapshot(
            timestamp=time.time(),
            total_files=total_files,
            total_size_bytes=total_size,
            file_type_distribution=file_types,
            directory_count=directories,
            largest_files=largest_files,
            recent_changes=recent_changes,
            checksum=checksum,
            metadata={
                "scan_duration": time.time() - self.last_scan_time if self.last_scan_time > 0 else 0,
                "repository_path": str(self.repository_path)
            }
        )

    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except (OSError, IOError):
            return ""

    def _analyze_changes(self, snapshot: RepositorySnapshot) -> Dict[str, Any]:
        """Analyze changes from the previous snapshot."""
        if len(self.snapshots) < 1:
            return {"is_initial": True}

        previous = self.snapshots[-1]

        return {
            "files_delta": snapshot.total_files - previous.total_files,
            "size_delta_bytes": snapshot.total_size_bytes - previous.total_size_bytes,
            "time_delta_hours": (snapshot.timestamp - previous.timestamp) / 3600,
            "new_files": [f for f in snapshot.recent_changes if f["action"] == "created"],
            "modified_files": [f for f in snapshot.recent_changes if f["action"] == "modified"],
            "deleted_files": [],  # Would need more complex tracking
            "large_files_added": [
                f for f in snapshot.largest_files
                if f["size_bytes"] > self.alert_thresholds["large_file_threshold_mb"] * 1024 * 1024
            ]
        }

    def _analyze_trends(self) -> Dict[int, RepositoryTrend]:
        """Analyze trends over different time windows."""
        trends = {}

        for window_hours in self.config["analysis"]["trend_windows"]:
            window_snapshots = [
                s for s in self.snapshots
                if s.timestamp > time.time() - (window_hours * 3600)
            ]

            if len(window_snapshots) < 2:
                continue

            # Calculate growth rates
            time_span = window_snapshots[-1].timestamp - window_snapshots[0].timestamp
            files_growth = window_snapshots[-1].total_files - window_snapshots[0].total_files
            size_growth = window_snapshots[-1].total_size_bytes - window_snapshots[0].total_size_bytes

            files_per_hour = files_growth / (time_span / 3600) if time_span > 0 else 0
            size_mb_per_hour = (size_growth / 1024 / 1024) / (time_span / 3600) if time_span > 0 else 0

            # Find most changed files (simplified)
            all_changes = []
            for snapshot in window_snapshots:
                all_changes.extend(snapshot.recent_changes)

            # Group by file path
            file_change_counts = {}
            for change in all_changes:
                path = change["path"]
                file_change_counts[path] = file_change_counts.get(path, 0) + 1

            most_changed = sorted(
                [{"path": path, "changes": count} for path, count in file_change_counts.items()],
                key=lambda x: x["changes"],
                reverse=True
            )[:10]

            # Calculate anomaly score (simplified)
            anomaly_score = abs(files_per_hour) / max(self.alert_thresholds["max_files_growth_rate"], 1)

            # Generate recommendations
            recommendations = []
            if files_per_hour > self.alert_thresholds["max_files_growth_rate"]:
                recommendations.append(f"High file growth rate: {files_per_hour:.1f} files/hour")
            if size_mb_per_hour > self.alert_thresholds["max_size_growth_rate_mb"]:
                recommendations.append(f"High size growth rate: {size_mb_per_hour:.1f} MB/hour")
            if anomaly_score > self.alert_thresholds["anomaly_score_threshold"]:
                recommendations.append(f"Anomaly detected (score: {anomaly_score:.2f})")

            trends[window_hours] = RepositoryTrend(
                time_window_hours=window_hours,
                growth_rate_files_per_hour=files_per_hour,
                growth_rate_size_per_hour=size_mb_per_hour,
                most_changed_files=most_changed,
                anomaly_score=anomaly_score,
                recommendations=recommendations
            )

        return trends

    def _check_alerts(self, snapshot: RepositorySnapshot, changes: Dict[str, Any],
                     trends: Dict[int, RepositoryTrend]) -> List[Dict[str, Any]]:
        """Check for alert conditions."""
        alerts = []

        # Check latest trend for alerts
        latest_trend = trends.get(1)  # 1-hour trend
        if latest_trend:
            if latest_trend.growth_rate_files_per_hour > self.alert_thresholds["max_files_growth_rate"]:
                alerts.append({
                    "type": "high_growth_rate",
                    "severity": "warning",
                    "message": f"File growth rate exceeded threshold: {latest_trend.growth_rate_files_per_hour:.1f} files/hour",
                    "data": {"growth_rate": latest_trend.growth_rate_files_per_hour}
                })

            if latest_trend.growth_rate_size_per_hour > self.alert_thresholds["max_size_growth_rate_mb"]:
                alerts.append({
                    "type": "high_size_growth",
                    "severity": "warning",
                    "message": f"Size growth rate exceeded threshold: {latest_trend.growth_rate_size_per_hour:.1f} MB/hour",
                    "data": {"growth_rate_mb": latest_trend.growth_rate_size_per_hour}
                })

            if latest_trend.anomaly_score > self.alert_thresholds["anomaly_score_threshold"]:
                alerts.append({
                    "type": "anomaly_detected",
                    "severity": "info",
                    "message": f"Anomaly detected with score: {latest_trend.anomaly_score:.2f}",
                    "data": {"anomaly_score": latest_trend.anomaly_score}
                })

        # Check for large files
        if changes.get("large_files_added"):
            alerts.append({
                "type": "large_files_added",
                "severity": "info",
                "message": f"Large files added: {len(changes['large_files_added'])} files over {self.alert_thresholds['large_file_threshold_mb']}MB",
                "data": {"large_files": changes["large_files_added"]}
            })

        return alerts

    async def _trigger_alerts(self, alerts: List[Dict[str, Any]]):
        """Trigger alert callbacks."""
        for alert in alerts:
            logger.warning(f"🚨 Repository Alert: {alert['message']}")

            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")

    def _cleanup_old_snapshots(self):
        """Clean up old snapshots based on retention policy."""
        if len(self.snapshots) <= self.max_snapshots:
            return

        # Keep most recent snapshots
        self.snapshots = self.snapshots[-self.max_snapshots:]

        # Remove snapshots older than max age
        cutoff_time = time.time() - (self.config["retention"]["max_age_days"] * 24 * 3600)
        self.snapshots = [s for s in self.snapshots if s.timestamp > cutoff_time]

    def get_current_stats(self) -> Dict[str, Any]:
        """Get current repository statistics."""
        if not self.snapshots:
            return {"error": "No snapshots available"}

        latest = self.snapshots[-1]

        return {
            "total_files": latest.total_files,
            "total_size_mb": latest.total_size_bytes / 1024 / 1024,
            "file_types": latest.file_type_distribution,
            "directories": latest.directory_count,
            "largest_files": latest.largest_files,
            "snapshots_count": len(self.snapshots),
            "monitoring_active": self.is_monitoring,
            "last_scan": latest.timestamp
        }

    def get_trends(self, window_hours: int = 24) -> Optional[RepositoryTrend]:
        """Get trend analysis for a specific time window."""
        trends = self._analyze_trends()
        return trends.get(window_hours)

    def export_data(self) -> Dict[str, Any]:
        """Export monitoring data for analysis."""
        return {
            "config": self.config,
            "snapshots": [
                {
                    "timestamp": s.timestamp,
                    "total_files": s.total_files,
                    "total_size_bytes": s.total_size_bytes,
                    "file_type_distribution": s.file_type_distribution,
                    "directory_count": s.directory_count,
                    "largest_files": s.largest_files,
                    "recent_changes": s.recent_changes,
                    "checksum": s.checksum,
                    "metadata": s.metadata
                }
                for s in self.snapshots
            ],
            "export_timestamp": time.time(),
            "export_version": "1.0"
        }


# Global instance
repository_monitor = RepositoryMonitor(
    repository_path=os.getcwd(),
    config={
        "scan_interval_seconds": 1800,  # 30 minutes for active development
        "alerts": {
            "max_files_growth_rate": 50,
            "max_size_growth_rate_mb": 25,
            "anomaly_score_threshold": 1.5,
            "large_file_threshold_mb": 5
        }
    }
)


async def start_repository_monitoring():
    """Start the global repository monitoring system."""
    await repository_monitor.start_monitoring()


async def stop_repository_monitoring():
    """Stop the global repository monitoring system."""
    await repository_monitor.stop_monitoring()


# Alert handler for integration with other systems
async def handle_repository_alert(alert: Dict[str, Any]):
    """Handle repository alerts - can be extended for notifications, etc."""
    print(f"Repository Alert: {alert}")

    # Here you could integrate with:
    # - Discord notifications
    # - Email alerts
    # - Dashboard updates
    # - Automated cleanup actions


if __name__ == "__main__":
    # Example usage
    async def demo():
        # Add alert handler
        repository_monitor.add_alert_callback(handle_repository_alert)

        # Start monitoring
        await repository_monitor.start_monitoring()

        # Run for a while
        await asyncio.sleep(10)

        # Get current stats
        stats = repository_monitor.get_current_stats()
        print("Repository Stats:", json.dumps(stats, indent=2))

        # Stop monitoring
        await repository_monitor.stop_monitoring()

    asyncio.run(demo())