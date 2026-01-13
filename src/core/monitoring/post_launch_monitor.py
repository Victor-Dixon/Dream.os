#!/usr/bin/env python3
"""
Post-Launch Monitoring Infrastructure - Agent Cellphone V2
========================================================

24/7 SYSTEM MONITORING: Real-time infrastructure health tracking
Activated immediately upon launch readiness confirmation.

PHASE: Post-Launch Operations
Status: ACTIVE - Monitoring infrastructure initialized

Author: Agent-1 (Infrastructure & Core Systems)
Date: 2026-01-12
"""

import time
import threading
import psutil
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import deque
import json
import os
from pathlib import Path

from ...core.logging_mixin import LoggingMixin


class SystemMonitor(LoggingMixin):
    """
    Real-time system monitoring for post-launch operations.

    PHASE: Post-Launch Infrastructure
    Status: ACTIVE - 24/7 monitoring initialized
    """

    def __init__(self, monitoring_interval: int = 30):
        """
        Initialize post-launch monitoring system.

        Args:
            monitoring_interval: Monitoring check interval in seconds
        """
        super().__init__()
        self.monitoring_interval = monitoring_interval
        self.is_monitoring = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_data = deque(maxlen=1000)  # Keep last 1000 readings

        # Alert thresholds
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'response_time_ms': 5000,  # 5 seconds
        }

        # Alert tracking
        self.active_alerts = []
        self.alert_history = deque(maxlen=100)

        self.logger.info("🚀 Post-launch monitoring infrastructure initialized")

    def start_monitoring(self) -> bool:
        """
        Start 24/7 monitoring operations.

        Returns:
            True if monitoring started successfully
        """
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return True

        try:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True,
                name="PostLaunchMonitor"
            )
            self.monitoring_thread.start()

            self.logger.info("✅ 24/7 Post-launch monitoring activated")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            self.is_monitoring = False
            return False

    def stop_monitoring(self):
        """Stop monitoring operations."""
        self.is_monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)

        self.logger.info("🛑 Post-launch monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop - runs continuously."""
        self.logger.info("🔄 Starting monitoring loop")

        while self.is_monitoring:
            try:
                # Collect system metrics
                metrics = self._collect_system_metrics()

                # Store metrics
                self.monitoring_data.append(metrics)

                # Check for alerts
                self._check_alerts(metrics)

                # Log summary every 5 minutes
                if len(self.monitoring_data) % (300 // self.monitoring_interval) == 0:
                    self._log_monitoring_summary()

            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")

            # Wait for next interval
            time.sleep(self.monitoring_interval)

    def _collect_system_metrics(self) -> Dict[str, Any]:
        """
        Collect comprehensive system metrics.

        Returns:
            Dictionary of current system metrics
        """
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None
            },
            'memory': {
                'total_gb': psutil.virtual_memory().total / (1024**3),
                'available_gb': psutil.virtual_memory().available / (1024**3),
                'percent': psutil.virtual_memory().percent,
                'used_gb': psutil.virtual_memory().used / (1024**3)
            },
            'disk': {
                'total_gb': psutil.disk_usage('/').total / (1024**3),
                'free_gb': psutil.disk_usage('/').free / (1024**3),
                'percent': psutil.disk_usage('/').percent
            },
            'network': self._get_network_stats(),
            'processes': {
                'total': len(psutil.pids()),
                'python_processes': len([p for p in psutil.process_iter(['name'])
                                       if p.info['name'] and 'python' in p.info['name'].lower()])
            }
        }

        return metrics

    def _get_network_stats(self) -> Dict[str, Any]:
        """Get network interface statistics."""
        net_stats = {}

        try:
            net_io = psutil.net_io_counters()
            net_stats = {
                'bytes_sent_mb': net_io.bytes_sent / (1024**2),
                'bytes_recv_mb': net_io.bytes_recv / (1024**2),
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout
            }
        except Exception as e:
            self.logger.warning(f"Failed to collect network stats: {e}")

        return net_stats

    def _check_alerts(self, metrics: Dict[str, Any]):
        """
        Check metrics against alert thresholds.

        Args:
            metrics: Current system metrics
        """
        alerts_triggered = []

        # CPU alert
        if metrics['cpu']['percent'] > self.alert_thresholds['cpu_percent']:
            alerts_triggered.append({
                'type': 'cpu_high',
                'message': f"CPU usage {metrics['cpu']['percent']:.1f}% exceeds threshold {self.alert_thresholds['cpu_percent']}%",
                'severity': 'warning',
                'value': metrics['cpu']['percent']
            })

        # Memory alert
        if metrics['memory']['percent'] > self.alert_thresholds['memory_percent']:
            alerts_triggered.append({
                'type': 'memory_high',
                'message': f"Memory usage {metrics['memory']['percent']:.1f}% exceeds threshold {self.alert_thresholds['memory_percent']}%",
                'severity': 'warning',
                'value': metrics['memory']['percent']
            })

        # Disk alert
        if metrics['disk']['percent'] > self.alert_thresholds['disk_percent']:
            alerts_triggered.append({
                'type': 'disk_high',
                'message': f"Disk usage {metrics['disk']['percent']:.1f}% exceeds threshold {self.alert_thresholds['disk_percent']}%",
                'severity': 'critical',
                'value': metrics['disk']['percent']
            })

        # Process alerts
        if metrics['processes']['total'] > 1000:  # Arbitrary high process count
            alerts_triggered.append({
                'type': 'process_count_high',
                'message': f"High process count: {metrics['processes']['total']}",
                'severity': 'info',
                'value': metrics['processes']['total']
            })

        # Trigger alerts
        for alert in alerts_triggered:
            self._trigger_alert(alert)

    def _trigger_alert(self, alert: Dict[str, Any]):
        """
        Trigger and log an alert.

        Args:
            alert: Alert information dictionary
        """
        alert_id = f"{alert['type']}_{int(time.time())}"

        # Log alert
        log_method = {
            'info': self.logger.info,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical
        }.get(alert['severity'], self.logger.warning)

        log_method(f"🚨 ALERT {alert_id}: {alert['message']}")

        # Store alert
        alert_record = {
            'id': alert_id,
            'timestamp': datetime.now().isoformat(),
            **alert
        }

        self.active_alerts.append(alert_record)
        self.alert_history.append(alert_record)

        # Keep only recent alerts
        self.active_alerts = [a for a in self.active_alerts
                            if (datetime.now() - datetime.fromisoformat(a['timestamp'])).seconds < 3600]

    def _log_monitoring_summary(self):
        """Log periodic monitoring summary."""
        if not self.monitoring_data:
            return

        latest = self.monitoring_data[-1]

        summary = {
            'cpu_percent': latest['cpu']['percent'],
            'memory_percent': latest['memory']['percent'],
            'disk_percent': latest['disk']['percent'],
            'active_alerts': len(self.active_alerts),
            'total_processes': latest['processes']['total'],
            'python_processes': latest['processes']['python_processes']
        }

        self.logger.info("📊 System Health Summary", extra=summary)

    def get_monitoring_status(self) -> Dict[str, Any]:
        """
        Get comprehensive monitoring status.

        Returns:
            Complete monitoring status report
        """
        if not self.monitoring_data:
            return {'status': 'no_data', 'message': 'Monitoring not yet started'}

        latest = self.monitoring_data[-1]

        uptime = 0
        if self.monitoring_data:
            start_time = datetime.fromisoformat(self.monitoring_data[0]['timestamp'])
            uptime = (datetime.now() - start_time).total_seconds()

        return {
            'status': 'active' if self.is_monitoring else 'inactive',
            'uptime_seconds': uptime,
            'monitoring_interval': self.monitoring_interval,
            'data_points': len(self.monitoring_data),
            'active_alerts': len(self.active_alerts),
            'alert_history_count': len(self.alert_history),
            'latest_metrics': latest,
            'alert_thresholds': self.alert_thresholds,
            'timestamp': datetime.now().isoformat()
        }

    def export_monitoring_data(self, format_type: str = "json") -> str:
        """
        Export monitoring data.

        Args:
            format_type: Export format ("json", "csv")

        Returns:
            Formatted monitoring data
        """
        if format_type == "json":
            return json.dumps(list(self.monitoring_data), indent=2, default=str)
        elif format_type == "csv":
            if not self.monitoring_data:
                return "timestamp,cpu_percent,memory_percent,disk_percent\n"

            lines = ["timestamp,cpu_percent,memory_percent,disk_percent,alerts_active"]
            for data in self.monitoring_data:
                line = ",".join([
                    data['timestamp'],
                    str(data['cpu']['percent']),
                    str(data['memory']['percent']),
                    str(data['disk']['percent']),
                    str(len(self.active_alerts))
                ])
                lines.append(line)

            return "\n".join(lines)

        return str(list(self.monitoring_data))


class PostLaunchHealthDashboard:
    """
    Health dashboard for post-launch monitoring visualization.

    PHASE: Post-Launch Operations
    Status: ACTIVE - Dashboard initialized
    """

    def __init__(self, monitor: SystemMonitor):
        """
        Initialize health dashboard.

        Args:
            monitor: SystemMonitor instance to display
        """
        self.monitor = monitor
        self.logger = logging.getLogger(self.__class__.__module__)

        self.logger.info("📊 Post-launch health dashboard initialized")

    def generate_health_report(self) -> str:
        """
        Generate comprehensive health report.

        Returns:
            Formatted health report
        """
        status = self.monitor.get_monitoring_status()

        if status.get('status') == 'no_data':
            return "📊 Health Dashboard: No monitoring data available yet"

        latest = status.get('latest_metrics', {})

        report_lines = [
            "🚀 **AGENT CELLPHONE V2 - POST-LAUNCH HEALTH DASHBOARD**",
            "=" * 60,
            "",
            f"📅 Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"⏱️  System Uptime: {status.get('uptime_seconds', 0):.0f} seconds",
            f"📊 Data Points: {status.get('data_points', 0)}",
            f"🚨 Active Alerts: {status.get('active_alerts', 0)}",
            "",
            "**🖥️  SYSTEM METRICS**",
            f"CPU Usage: {latest.get('cpu', {}).get('percent', 0):.1f}%",
            f"Memory Usage: {latest.get('memory', {}).get('percent', 0):.1f}% ({latest.get('memory', {}).get('used_gb', 0):.1f}GB used)",
            f"Disk Usage: {latest.get('disk', {}).get('percent', 0):.1f}% ({latest.get('disk', {}).get('free_gb', 0):.1f}GB free)",
            f"Processes: {latest.get('processes', {}).get('total', 0)} total, {latest.get('processes', {}).get('python_processes', 0)} Python",
            "",
            "**🌐 NETWORK ACTIVITY**",
            f"Data Sent: {latest.get('network', {}).get('bytes_sent_mb', 0):.1f} MB",
            f"Data Received: {latest.get('network', {}).get('bytes_recv_mb', 0):.1f} MB",
            "",
            "**⚠️  ALERT THRESHOLDS**",
            f"CPU > {status.get('alert_thresholds', {}).get('cpu_percent', 0)}%",
            f"Memory > {status.get('alert_thresholds', {}).get('memory_percent', 0)}%",
            f"Disk > {status.get('alert_thresholds', {}).get('disk_percent', 0)}%",
            "",
            "**🏥 SYSTEM STATUS**",
            f"Monitoring: {'✅ ACTIVE' if status.get('status') == 'active' else '❌ INACTIVE'}",
            f"Health Score: {'🟢 GOOD' if status.get('active_alerts', 0) == 0 else '🟡 WARNING' if status.get('active_alerts', 0) < 3 else '🔴 CRITICAL'}",
            "",
            "=" * 60
        ]

        return "\n".join(report_lines)

    def save_dashboard_snapshot(self, output_path: Optional[Path] = None):
        """
        Save dashboard snapshot to file.

        Args:
            output_path: Path to save snapshot (default: monitoring_snapshot.txt)
        """
        if not output_path:
            output_path = Path("monitoring_snapshot.txt")

        try:
            report = self.generate_health_report()

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
                f.write("\n\n**RAW MONITORING DATA**\n")
                f.write(self.monitor.export_monitoring_data("json"))

            self.logger.info(f"💾 Dashboard snapshot saved to {output_path}")

        except Exception as e:
            self.logger.error(f"Failed to save dashboard snapshot: {e}")


# Global monitoring instance
_monitor_instance: Optional[SystemMonitor] = None
_dashboard_instance: Optional[PostLaunchHealthDashboard] = None


def initialize_post_launch_monitoring() -> SystemMonitor:
    """
    Initialize post-launch monitoring infrastructure.

    Returns:
        Initialized SystemMonitor instance
    """
    global _monitor_instance, _dashboard_instance

    if _monitor_instance is None:
        _monitor_instance = SystemMonitor(monitoring_interval=30)
        _monitor_instance.start_monitoring()

        _dashboard_instance = PostLaunchHealthDashboard(_monitor_instance)

        logging.getLogger(__name__).info("🎯 Post-launch monitoring infrastructure ACTIVATED")
        logging.getLogger(__name__).info("📊 Health dashboard ready for 24/7 system tracking")

    return _monitor_instance


def get_monitoring_status() -> Dict[str, Any]:
    """
    Get current monitoring status.

    Returns:
        Monitoring status dictionary
    """
    if _monitor_instance:
        return _monitor_instance.get_monitoring_status()
    return {'status': 'not_initialized', 'message': 'Monitoring not initialized'}


def get_health_report() -> str:
    """
    Get current health report.

    Returns:
        Formatted health report string
    """
    if _dashboard_instance:
        return _dashboard_instance.generate_health_report()
    return "📊 Health Dashboard: Not initialized"


def save_monitoring_snapshot():
    """Save current monitoring snapshot."""
    if _dashboard_instance:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_launch_monitoring_{timestamp}.txt"
        _dashboard_instance.save_dashboard_snapshot(Path(filename))


# Initialize monitoring immediately upon import
if __name__ != "__main__":
    try:
        initialize_post_launch_monitoring()
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to initialize monitoring: {e}")


if __name__ == "__main__":
    # CLI usage for monitoring dashboard
    import argparse

    parser = argparse.ArgumentParser(description="Post-Launch Monitoring Dashboard")
    parser.add_argument("--status", action="store_true", help="Show monitoring status")
    parser.add_argument("--report", action="store_true", help="Generate health report")
    parser.add_argument("--snapshot", action="store_true", help="Save monitoring snapshot")
    parser.add_argument("--export", choices=["json", "csv"], help="Export monitoring data")

    args = parser.parse_args()

    monitor = initialize_post_launch_monitoring()

    if args.status:
        status = get_monitoring_status()
        print("📊 Monitoring Status:")
        print(json.dumps(status, indent=2, default=str))

    elif args.report:
        report = get_health_report()
        print(report)

    elif args.snapshot:
        save_monitoring_snapshot()
        print("💾 Monitoring snapshot saved")

    elif args.export:
        if monitor:
            data = monitor.export_monitoring_data(args.export)
            print(data)
        else:
            print("❌ Monitoring not initialized")

    else:
        print("🚀 Agent Cellphone V2 - Post-Launch Monitoring Active")
        print("Use --status, --report, --snapshot, or --export to interact")
        print(f"Monitoring interval: {monitor.monitoring_interval}s" if monitor else "Monitoring not active")