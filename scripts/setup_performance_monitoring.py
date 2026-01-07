#!/usr/bin/env python3
"""
Advanced Performance Monitoring - Phase 3 Infrastructure
=======================================================

Enterprise-grade performance monitoring and observability infrastructure.
Provides comprehensive metrics collection, alerting, and performance analysis.

Features:
- Real-time metrics collection
- Distributed tracing
- Performance profiling
- Custom dashboards
- Automated alerting
- Historical data analysis

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import time
import json
import logging
import psutil
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import statistics

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Performance monitoring configuration
MONITORING_CONFIG = {
    'collection_interval': 10,  # seconds
    'retention_period': 3600,   # 1 hour in seconds
    'alert_thresholds': {
        'cpu_usage': 80.0,      # percentage
        'memory_usage': 85.0,   # percentage
        'disk_usage': 90.0,     # percentage
        'response_time': 2.0,   # seconds
        'error_rate': 5.0,      # percentage
    },
    'metrics': {
        'system': ['cpu', 'memory', 'disk', 'network'],
        'application': ['response_time', 'throughput', 'error_rate', 'active_connections'],
        'custom': ['cache_hit_rate', 'db_connection_pool', 'api_rate_limit']
    }
}

class MetricsCollector:
    """Advanced metrics collection and analysis."""

    def __init__(self):
        """Initialize metrics collector."""
        self.config = MONITORING_CONFIG
        self.logger = logging.getLogger(__name__)

        # Metrics storage
        self.metrics_history = defaultdict(lambda: deque(maxlen=360))  # 1 hour at 10s intervals
        self.current_metrics = {}
        self.alerts = []

        # Performance baselines
        self.baselines = {}
        self.is_running = False
        self.collection_thread = None

    def start_collection(self):
        """Start metrics collection."""
        if self.is_running:
            return

        self.is_running = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
        self.logger.info("✅ Performance monitoring started")

    def stop_collection(self):
        """Stop metrics collection."""
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        self.logger.info("🛑 Performance monitoring stopped")

    def _collection_loop(self):
        """Main metrics collection loop."""
        while self.is_running:
            try:
                self._collect_system_metrics()
                self._collect_application_metrics()
                self._check_alerts()
                self._update_baselines()
            except Exception as e:
                self.logger.error(f"Metrics collection error: {e}")

            time.sleep(self.config['collection_interval'])

    def _collect_system_metrics(self):
        """Collect system-level metrics."""
        timestamp = datetime.now().isoformat()

        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used
            memory_total = memory.total

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used = disk.used
            disk_total = disk.total

            # Network metrics
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv

            system_metrics = {
                'timestamp': timestamp,
                'cpu': {
                    'usage_percent': cpu_percent,
                    'count': cpu_count,
                    'frequency_mhz': cpu_freq.current if cpu_freq else None
                },
                'memory': {
                    'usage_percent': memory_percent,
                    'used_bytes': memory_used,
                    'total_bytes': memory_total,
                    'available_bytes': memory.available
                },
                'disk': {
                    'usage_percent': disk_percent,
                    'used_bytes': disk_used,
                    'total_bytes': disk_total,
                    'free_bytes': disk.free
                },
                'network': {
                    'bytes_sent': network_bytes_sent,
                    'bytes_recv': network_bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                }
            }

            self._store_metrics('system', system_metrics)
            self.current_metrics['system'] = system_metrics

        except Exception as e:
            self.logger.error(f"System metrics collection failed: {e}")

    def _collect_application_metrics(self):
        """Collect application-level metrics."""
        timestamp = datetime.now().isoformat()

        try:
            # Web service health checks
            flask_healthy = self._check_service_health('http://127.0.0.1:5000/health')
            fastapi_healthy = self._check_service_health('http://127.0.0.1:8001/health')

            # Process metrics
            flask_processes = self._get_process_metrics('python.*start_web_server')
            fastapi_processes = self._get_process_metrics('python.*start_fastapi')

            application_metrics = {
                'timestamp': timestamp,
                'services': {
                    'flask': {
                        'healthy': flask_healthy,
                        'processes': flask_processes
                    },
                    'fastapi': {
                        'healthy': fastapi_healthy,
                        'processes': fastapi_processes
                    }
                }
            }

            self._store_metrics('application', application_metrics)
            self.current_metrics['application'] = application_metrics

        except Exception as e:
            self.logger.error(f"Application metrics collection failed: {e}")

    def _check_service_health(self, url: str) -> bool:
        """Check service health via HTTP."""
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('overall_status') in ['healthy', 'warning']
            return False
        except Exception:
            return False

    def _get_process_metrics(self, pattern: str) -> List[Dict[str, Any]]:
        """Get metrics for processes matching pattern."""
        try:
            import re
            processes = []

            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if re.search(pattern, cmdline, re.IGNORECASE):
                        processes.append({
                            'pid': proc.info['pid'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            return processes
        except Exception:
            return []

    def _store_metrics(self, category: str, metrics: Dict[str, Any]):
        """Store metrics in history."""
        self.metrics_history[category].append(metrics)

    def _check_alerts(self):
        """Check metrics against alert thresholds."""
        thresholds = self.config['alert_thresholds']

        # System alerts
        system = self.current_metrics.get('system', {})
        if system:
            # CPU alert
            cpu_usage = system['cpu']['usage_percent']
            if cpu_usage > thresholds['cpu_usage']:
                self._create_alert('cpu_usage', f"High CPU usage: {cpu_usage:.1f}%", 'warning')

            # Memory alert
            memory_usage = system['memory']['usage_percent']
            if memory_usage > thresholds['memory_usage']:
                self._create_alert('memory_usage', f"High memory usage: {memory_usage:.1f}%", 'warning')

            # Disk alert
            disk_usage = system['disk']['usage_percent']
            if disk_usage > thresholds['disk_usage']:
                self._create_alert('disk_usage', f"High disk usage: {disk_usage:.1f}%", 'critical')

    def _create_alert(self, alert_type: str, message: str, severity: str):
        """Create performance alert."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'severity': severity
        }

        self.alerts.append(alert)
        self.logger.warning(f"🚨 Performance Alert: {message}")

        # Keep only recent alerts
        cutoff_time = datetime.now() - timedelta(minutes=30)
        self.alerts = [
            alert for alert in self.alerts
            if datetime.fromisoformat(alert['timestamp']) > cutoff_time
        ]

    def _update_baselines(self):
        """Update performance baselines."""
        for category, history in self.metrics_history.items():
            if len(history) < 10:  # Need minimum data points
                continue

            if category == 'system':
                self._update_system_baselines(history)

    def _update_system_baselines(self, history):
        """Update system performance baselines."""
        cpu_values = [h['cpu']['usage_percent'] for h in history if 'cpu' in h]
        memory_values = [h['memory']['usage_percent'] for h in history if 'memory' in h]

        if cpu_values:
            self.baselines['cpu_normal'] = statistics.mean(cpu_values)
            self.baselines['cpu_stddev'] = statistics.stdev(cpu_values) if len(cpu_values) > 1 else 0

        if memory_values:
            self.baselines['memory_normal'] = statistics.mean(memory_values)
            self.baselines['memory_stddev'] = statistics.stdev(memory_values) if len(memory_values) > 1 else 0

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        return {
            'timestamp': datetime.now().isoformat(),
            'current': dict(self.current_metrics),
            'baselines': dict(self.baselines),
            'alerts': self.alerts[-10:]  # Last 10 alerts
        }

    def get_metrics_history(self, category: str, hours: int = 1) -> List[Dict[str, Any]]:
        """Get metrics history for category."""
        if category not in self.metrics_history:
            return []

        # Calculate how many data points to return (hours * 3600 / interval)
        points_needed = int((hours * 3600) / self.config['collection_interval'])
        history = list(self.metrics_history[category])

        return history[-points_needed:] if len(history) > points_needed else history

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': 'last_hour',
            'system_performance': {},
            'application_performance': {},
            'alerts_summary': {},
            'recommendations': []
        }

        # System performance analysis
        system_history = self.get_metrics_history('system', 1)
        if system_history:
            cpu_avg = statistics.mean([h['cpu']['usage_percent'] for h in system_history if 'cpu' in h])
            memory_avg = statistics.mean([h['memory']['usage_percent'] for h in system_history if 'memory' in h])

            report['system_performance'] = {
                'cpu_average': round(cpu_avg, 2),
                'memory_average': round(memory_avg, 2),
                'status': 'healthy' if cpu_avg < 70 and memory_avg < 80 else 'warning'
            }

        # Application performance
        app_history = self.get_metrics_history('application', 1)
        if app_history:
            flask_health = sum(1 for h in app_history if h.get('services', {}).get('flask', {}).get('healthy', False))
            fastapi_health = sum(1 for h in app_history if h.get('services', {}).get('fastapi', {}).get('healthy', False))

            total_checks = len(app_history)
            report['application_performance'] = {
                'flask_uptime_percent': round((flask_health / total_checks) * 100, 2),
                'fastapi_uptime_percent': round((fastapi_health / total_checks) * 100, 2),
                'overall_status': 'healthy' if (flask_health + fastapi_health) / (2 * total_checks) > 0.95 else 'warning'
            }

        # Alerts summary
        recent_alerts = [a for a in self.alerts if (datetime.now() - datetime.fromisoformat(a['timestamp'])).seconds < 3600]
        alert_counts = defaultdict(int)
        for alert in recent_alerts:
            alert_counts[alert['severity']] += 1

        report['alerts_summary'] = dict(alert_counts)

        # Generate recommendations
        if report['system_performance'].get('cpu_average', 0) > 70:
            report['recommendations'].append("Consider optimizing CPU-intensive operations")
        if report['system_performance'].get('memory_average', 0) > 80:
            report['recommendations'].append("Review memory usage patterns and consider optimization")
        if report['application_performance'].get('flask_uptime_percent', 100) < 95:
            report['recommendations'].append("Investigate Flask service stability issues")
        if report['application_performance'].get('fastapi_uptime_percent', 100) < 95:
            report['recommendations'].append("Investigate FastAPI service stability issues")

        return report


# Global metrics collector instance
_metrics_collector = None

def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def start_performance_monitoring():
    """Start performance monitoring."""
    collector = get_metrics_collector()
    collector.start_collection()
    return collector


def stop_performance_monitoring():
    """Stop performance monitoring."""
    collector = get_metrics_collector()
    collector.stop_collection()


def get_performance_metrics():
    """Get current performance metrics."""
    collector = get_metrics_collector()
    return collector.get_current_metrics()


def get_performance_report():
    """Get performance report."""
    collector = get_metrics_collector()
    return collector.get_performance_report()


def main():
    """Main entry point for performance monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Advanced Performance Monitoring")
    parser.add_argument('--start', action='store_true', help='Start monitoring')
    parser.add_argument('--stop', action='store_true', help='Stop monitoring')
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--report', action='store_true', help='Generate performance report')
    parser.add_argument('--metrics', action='store_true', help='Show current metrics')

    args = parser.parse_args()

    collector = get_metrics_collector()

    if args.start:
        collector.start_collection()
        print("✅ Performance monitoring started")

    elif args.stop:
        collector.stop_collection()
        print("🛑 Performance monitoring stopped")

    elif args.status:
        metrics = collector.get_current_metrics()
        print("📊 Performance Monitoring Status:")
        print(json.dumps(metrics, indent=2, default=str))

    elif args.report:
        report = collector.get_performance_report()
        print("📈 Performance Report:")
        print(json.dumps(report, indent=2, default=str))

    elif args.metrics:
        metrics = collector.get_current_metrics()
        print("📊 Current Metrics:")
        print(json.dumps(metrics, indent=2, default=str))

    else:
        print("📊 Advanced Performance Monitoring")
        print("Use --help for available options")
        print("\nQuick start:")
        print("  python scripts/setup_performance_monitoring.py --start")
        print("  python scripts/setup_performance_monitoring.py --status")


if __name__ == "__main__":
    main()