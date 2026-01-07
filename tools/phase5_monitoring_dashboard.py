#!/usr/bin/env python3
"""
Phase 5 Infrastructure Monitoring Dashboard
Real-time monitoring and alerting for enterprise infrastructure
"""

import asyncio
import aiohttp
import json
import time
import psycopg2
import redis
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import argparse
import sys
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MonitoringMetric:
    name: str
    value: float
    unit: str
    status: str
    timestamp: str
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None

@dataclass
class ServiceHealth:
    service: str
    status: str
    response_time: float
    uptime_percentage: float
    last_check: str
    consecutive_failures: int

@dataclass
class Alert:
    level: str  # INFO, WARNING, CRITICAL
    service: str
    message: str
    timestamp: str
    resolved: bool = False
    resolved_at: Optional[str] = None

class Phase5MonitoringDashboard:
    def __init__(self, interval: int = 30):
        self.interval = interval
        self.metrics_history = deque(maxlen=100)  # Keep last 100 data points
        self.services_health = {}
        self.alerts = []
        self.start_time = datetime.now()

    async def collect_system_metrics(self) -> List[MonitoringMetric]:
        """Collect comprehensive system metrics"""
        metrics = []

        try:
            # CPU Usage
            cpu_result = subprocess.run(
                ['bash', '-c', 'top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\\1/" | awk \'{print 100 - $1}\''],
                capture_output=True, text=True, timeout=5
            )
            if cpu_result.returncode == 0:
                cpu_usage = float(cpu_result.stdout.strip())
                status = "CRITICAL" if cpu_usage > 90 else "WARNING" if cpu_usage > 75 else "OK"
                metrics.append(MonitoringMetric(
                    name="system_cpu_usage",
                    value=round(cpu_usage, 1),
                    unit="%",
                    status=status,
                    timestamp=datetime.now().isoformat(),
                    threshold_warning=75.0,
                    threshold_critical=90.0
                ))

            # Memory Usage
            mem_result = subprocess.run(
                ['bash', '-c', 'free | grep Mem | awk \'{printf "%.1f", $3/$2 * 100.0}\''],
                capture_output=True, text=True, timeout=5
            )
            if mem_result.returncode == 0:
                mem_usage = float(mem_result.stdout.strip())
                status = "CRITICAL" if mem_usage > 90 else "WARNING" if mem_usage > 80 else "OK"
                metrics.append(MonitoringMetric(
                    name="system_memory_usage",
                    value=round(mem_usage, 1),
                    unit="%",
                    status=status,
                    timestamp=datetime.now().isoformat(),
                    threshold_warning=80.0,
                    threshold_critical=90.0
                ))

            # Disk Usage
            disk_result = subprocess.run(
                ['df', '/'],
                capture_output=True, text=True, timeout=5
            )
            if disk_result.returncode == 0:
                lines = disk_result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    disk_data = lines[1].split()
                    disk_usage = float(disk_data[4].rstrip('%'))
                    status = "CRITICAL" if disk_usage > 95 else "WARNING" if disk_usage > 85 else "OK"
                    metrics.append(MonitoringMetric(
                        name="system_disk_usage",
                        value=round(disk_usage, 1),
                        unit="%",
                        status=status,
                        timestamp=datetime.now().isoformat(),
                        threshold_warning=85.0,
                        threshold_critical=95.0
                    ))

            # Network I/O
            net_result = subprocess.run(
                ['bash', '-c', 'cat /proc/net/dev | grep eth0 | awk \'{print $2, $10}\''],
                capture_output=True, text=True, timeout=5
            )
            if net_result.returncode == 0:
                rx_bytes, tx_bytes = map(int, net_result.stdout.strip().split())
                # Convert to MB/s (rough approximation)
                rx_mbps = (rx_bytes * 8) / (1024 * 1024)  # Convert to Mbps
                tx_mbps = (tx_bytes * 8) / (1024 * 1024)
                metrics.extend([
                    MonitoringMetric(
                        name="network_rx_mbps",
                        value=round(rx_mbps, 2),
                        unit="Mbps",
                        status="OK",
                        timestamp=datetime.now().isoformat()
                    ),
                    MonitoringMetric(
                        name="network_tx_mbps",
                        value=round(tx_mbps, 2),
                        unit="Mbps",
                        status="OK",
                        timestamp=datetime.now().isoformat()
                    )
                ])

        except Exception as e:
            logger.warning(f"Failed to collect system metrics: {e}")

        return metrics

    async def collect_service_metrics(self) -> List[MonitoringMetric]:
        """Collect service-specific metrics"""
        metrics = []
        services = [
            ("fastapi", "http://localhost:8001/health"),
            ("flask", "http://localhost:5000/health"),
            ("kong", "http://localhost:8000/status"),
            ("nginx", "http://localhost:8080/health"),
            ("prometheus", "http://localhost:9090/-/healthy"),
            ("grafana", "http://localhost:3000/api/health")
        ]

        for service_name, url in services:
            try:
                start_time = time.time()
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    async with session.get(url) as response:
                        response_time = (time.time() - start_time) * 1000

                        # Update service health tracking
                        if service_name not in self.services_health:
                            self.services_health[service_name] = ServiceHealth(
                                service=service_name,
                                status="OK",
                                response_time=response_time,
                                uptime_percentage=100.0,
                                last_check=datetime.now().isoformat(),
                                consecutive_failures=0
                            )

                        health = self.services_health[service_name]
                        health.response_time = response_time
                        health.last_check = datetime.now().isoformat()

                        if response.status == 200:
                            health.status = "OK"
                            health.consecutive_failures = 0
                        else:
                            health.consecutive_failures += 1
                            if health.consecutive_failures >= 3:
                                health.status = "CRITICAL"
                            elif health.consecutive_failures >= 1:
                                health.status = "WARNING"

                        # Calculate uptime percentage
                        total_runtime = (datetime.now() - self.start_time).total_seconds()
                        uptime_runtime = total_runtime - (health.consecutive_failures * self.interval)
                        health.uptime_percentage = (uptime_runtime / total_runtime) * 100 if total_runtime > 0 else 100

                        # Add response time metric
                        status = "CRITICAL" if response_time > 5000 else "WARNING" if response_time > 2000 else "OK"
                        metrics.append(MonitoringMetric(
                            name=f"{service_name}_response_time",
                            value=round(response_time, 1),
                            unit="ms",
                            status=status,
                            timestamp=datetime.now().isoformat(),
                            threshold_warning=2000.0,
                            threshold_critical=5000.0
                        ))

                        # Add uptime metric
                        metrics.append(MonitoringMetric(
                            name=f"{service_name}_uptime",
                            value=round(health.uptime_percentage, 1),
                            unit="%",
                            status="OK" if health.uptime_percentage > 95 else "WARNING" if health.uptime_percentage > 85 else "CRITICAL",
                            timestamp=datetime.now().isoformat(),
                            threshold_warning=95.0,
                            threshold_critical=85.0
                        ))

            except Exception as e:
                logger.warning(f"Failed to check {service_name}: {e}")

                # Mark service as failing
                if service_name not in self.services_health:
                    self.services_health[service_name] = ServiceHealth(
                        service=service_name,
                        status="CRITICAL",
                        response_time=0,
                        uptime_percentage=0,
                        last_check=datetime.now().isoformat(),
                        consecutive_failures=1
                    )
                else:
                    self.services_health[service_name].consecutive_failures += 1
                    self.services_health[service_name].status = "CRITICAL"

        return metrics

    def collect_database_metrics(self) -> List[MonitoringMetric]:
        """Collect database performance metrics"""
        metrics = []

        # PostgreSQL metrics
        try:
            conn = psycopg2.connect(
                host="localhost", port=5432, database="tradingrobotplug",
                user="postgres", password="postgres"
            )
            cursor = conn.cursor()

            # Active connections
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
            active_connections = cursor.fetchone()[0]
            metrics.append(MonitoringMetric(
                name="postgres_active_connections",
                value=active_connections,
                unit="connections",
                status="WARNING" if active_connections > 50 else "OK",
                timestamp=datetime.now().isoformat(),
                threshold_warning=50.0
            ))

            # Cache hit ratio
            cursor.execute("""
                SELECT sum(blks_hit)*100/sum(blks_hit+blks_read) as cache_hit_ratio
                FROM pg_stat_database WHERE datname = 'tradingrobotplug'
            """)
            cache_hit_ratio = cursor.fetchone()[0] or 0
            metrics.append(MonitoringMetric(
                name="postgres_cache_hit_ratio",
                value=round(cache_hit_ratio, 1),
                unit="%",
                status="WARNING" if cache_hit_ratio < 95 else "OK",
                timestamp=datetime.now().isoformat(),
                threshold_warning=95.0
            ))

            cursor.close()
            conn.close()

        except Exception as e:
            logger.warning(f"Failed to collect PostgreSQL metrics: {e}")

        # Redis metrics
        try:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            info = r.info()

            # Memory usage
            used_memory = info.get('used_memory', 0) / (1024 * 1024)  # MB
            max_memory = info.get('maxmemory', 512 * 1024 * 1024) / (1024 * 1024)  # MB
            memory_usage_pct = (used_memory / max_memory) * 100 if max_memory > 0 else 0

            metrics.append(MonitoringMetric(
                name="redis_memory_usage",
                value=round(memory_usage_pct, 1),
                unit="%",
                status="CRITICAL" if memory_usage_pct > 90 else "WARNING" if memory_usage_pct > 75 else "OK",
                timestamp=datetime.now().isoformat(),
                threshold_warning=75.0,
                threshold_critical=90.0
            ))

            # Connected clients
            connected_clients = info.get('connected_clients', 0)
            metrics.append(MonitoringMetric(
                name="redis_connected_clients",
                value=connected_clients,
                unit="clients",
                status="WARNING" if connected_clients > 100 else "OK",
                timestamp=datetime.now().isoformat(),
                threshold_warning=100.0
            ))

            r.close()

        except Exception as e:
            logger.warning(f"Failed to collect Redis metrics: {e}")

        return metrics

    def check_alerts(self, metrics: List[MonitoringMetric]):
        """Check metrics against thresholds and generate alerts"""
        for metric in metrics:
            if metric.status in ["WARNING", "CRITICAL"]:
                alert = Alert(
                    level=metric.status,
                    service=metric.name,
                    message=f"{metric.name} is {metric.status}: {metric.value}{metric.unit}",
                    timestamp=datetime.now().isoformat()
                )
                self.alerts.append(alert)

                # Keep only last 100 alerts
                if len(self.alerts) > 100:
                    self.alerts.pop(0)

    def get_system_status_summary(self) -> Dict:
        """Get comprehensive system status summary"""
        total_services = len(self.services_health)
        healthy_services = len([s for s in self.services_health.values() if s.status == "OK"])
        warning_services = len([s for s in self.services_health.values() if s.status == "WARNING"])
        critical_services = len([s for s in self.services_health.values() if s.status == "CRITICAL"])

        active_alerts = len([a for a in self.alerts if not a.resolved])

        # Calculate overall system health
        if critical_services > 0:
            overall_status = "CRITICAL"
        elif warning_services > 0:
            overall_status = "WARNING"
        elif healthy_services == total_services:
            overall_status = "HEALTHY"
        else:
            overall_status = "UNKNOWN"

        return {
            "overall_status": overall_status,
            "total_services": total_services,
            "healthy_services": healthy_services,
            "warning_services": warning_services,
            "critical_services": critical_services,
            "active_alerts": active_alerts,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }

    def display_dashboard(self):
        """Display real-time monitoring dashboard"""
        print("\033[2J\033[H")  # Clear screen and move cursor to top
        print("="*100)
        print("📊 PHASE 5 INFRASTRUCTURE MONITORING DASHBOARD")
        print("="*100)

        status_summary = self.get_system_status_summary()
        status_color = {
            "HEALTHY": "\033[92m",  # Green
            "WARNING": "\033[93m",  # Yellow
            "CRITICAL": "\033[91m",  # Red
            "UNKNOWN": "\033[90m"    # Gray
        }.get(status_summary["overall_status"], "\033[0m")
        reset_color = "\033[0m"

        print(f"🟢 OVERALL STATUS: {status_color}{status_summary['overall_status']}{reset_color}")
        print(f"⏱️  UPTIME: {status_summary['uptime_seconds']:.0f} seconds")
        print(f"📈 SERVICES: {status_summary['healthy_services']}/{status_summary['total_services']} healthy")
        if status_summary['warning_services'] > 0:
            print(f"⚠️  WARNINGS: {status_summary['warning_services']} services")
        if status_summary['critical_services'] > 0:
            print(f"❌ CRITICAL: {status_summary['critical_services']} services")
        print(f"🚨 ACTIVE ALERTS: {status_summary['active_alerts']}")

        print("\n" + "-"*100)
        print("🏥 SERVICE HEALTH STATUS")
        print("-"*100)

        for service_name, health in self.services_health.items():
            status_emoji = {
                "OK": "✅",
                "WARNING": "⚠️",
                "CRITICAL": "❌"
            }.get(health.status, "❓")

            response_time_color = "\033[91m" if health.response_time > 2000 else "\033[93m" if health.response_time > 1000 else "\033[92m"
            print(f"{status_emoji} {service_name:<15} | {health.status:<8} | {response_time_color}{health.response_time:>6.0f}ms{reset_color} | {health.uptime_percentage:>5.1f}% uptime")

        # Show recent metrics if available
        if self.metrics_history:
            print("\n" + "-"*100)
            print("📊 RECENT SYSTEM METRICS")
            print("-"*100)

            latest_metrics = self.metrics_history[-1] if self.metrics_history else []
            for metric in latest_metrics:
                if "system" in metric.name or "network" in metric.name:
                    status_emoji = "✅" if metric.status == "OK" else "⚠️" if metric.status == "WARNING" else "❌"
                    print(f"{status_emoji} {metric.name:<25} | {metric.value:>8.1f} {metric.unit:<3} | {metric.status}")

        # Show recent alerts
        recent_alerts = [a for a in self.alerts[-5:] if not a.resolved]  # Last 5 unresolved alerts
        if recent_alerts:
            print("\n" + "-"*100)
            print("🚨 RECENT ALERTS")
            print("-"*100)

            for alert in recent_alerts[-3:]:  # Show last 3
                level_emoji = "ℹ️" if alert.level == "INFO" else "⚠️" if alert.level == "WARNING" else "❌"
                print(f"{level_emoji} {alert.timestamp[:19]} | {alert.service}: {alert.message}")

        print("\n" + "="*100)
        print(f"🔄 Last updated: {datetime.now().strftime('%H:%M:%S')} | Refresh: {self.interval}s")
        print("="*100)

    async def run_monitoring_loop(self):
        """Run continuous monitoring loop"""
        logger.info(f"🚀 Starting Phase 5 Infrastructure Monitoring (interval: {self.interval}s)...")

        try:
            while True:
                # Collect all metrics
                system_metrics = await self.collect_system_metrics()
                service_metrics = await self.collect_service_metrics()
                database_metrics = self.collect_database_metrics()

                all_metrics = system_metrics + service_metrics + database_metrics

                # Store in history
                self.metrics_history.append(all_metrics)

                # Check for alerts
                self.check_alerts(all_metrics)

                # Display dashboard
                self.display_dashboard()

                # Wait for next interval
                await asyncio.sleep(self.interval)

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Monitoring loop failed: {e}")

    def save_snapshot(self, filename: str = None):
        """Save current monitoring snapshot"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase5_monitoring_snapshot_{timestamp}.json"

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_system_status_summary(),
            "services": {name: asdict(health) for name, health in self.services_health.items()},
            "recent_alerts": [asdict(alert) for alert in self.alerts[-10:]],  # Last 10 alerts
            "latest_metrics": [asdict(metric) for metric in self.metrics_history[-1]] if self.metrics_history else []
        }

        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=2, default=str)

        logger.info(f"📸 Monitoring snapshot saved to: {filename}")

async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 5 Infrastructure Monitoring Dashboard')
    parser.add_argument('--interval', type=int, default=30, help='Monitoring interval in seconds')
    parser.add_argument('--snapshot', action='store_true', help='Save monitoring snapshot and exit')
    parser.add_argument('--output', type=str, help='Output filename for snapshot')

    args = parser.parse_args()

    dashboard = Phase5MonitoringDashboard(interval=args.interval)

    if args.snapshot:
        # Collect one round of data and save snapshot
        logger.info("📸 Collecting monitoring snapshot...")

        system_metrics = await dashboard.collect_system_metrics()
        service_metrics = await dashboard.collect_service_metrics()
        database_metrics = dashboard.collect_database_metrics()

        all_metrics = system_metrics + service_metrics + database_metrics
        dashboard.metrics_history.append(all_metrics)
        dashboard.check_alerts(all_metrics)

        dashboard.save_snapshot(args.output)
        print("✅ Monitoring snapshot saved")

        # Print summary
        summary = dashboard.get_system_status_summary()
        print(f"📊 System Status: {summary['overall_status']}")
        print(f"🏥 Services: {summary['healthy_services']}/{summary['total_services']} healthy")

    else:
        # Run continuous monitoring
        try:
            await dashboard.run_monitoring_loop()
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
            dashboard.save_snapshot(args.output)

if __name__ == "__main__":
    asyncio.run(main())