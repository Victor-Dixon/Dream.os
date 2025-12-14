#!/usr/bin/env python3
"""
Infrastructure Health Monitor
============================

Monitors critical infrastructure health metrics to prevent automation failures.
Includes disk space monitoring, browser automation readiness, and system diagnostics.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
import os
import platform
import psutil
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import alerting system
try:
    from src.infrastructure.alerting_system import AlertingSystem, AlertLevel
    ALERTING_AVAILABLE = True
except ImportError:
    ALERTING_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Alerting system not available")

if ALERTING_AVAILABLE:
    logger = logging.getLogger(__name__)


@dataclass
class HealthMetrics:
    """Container for health monitoring metrics."""
    disk_usage_percent: float
    disk_free_gb: float
    disk_total_gb: float
    memory_usage_percent: float
    memory_free_gb: float
    cpu_usage_percent: float
    system_load: Optional[List[float]] = None
    browser_ready: bool = False
    automation_ready: bool = False


@dataclass
class HealthCheckResult:
    """Result of a health check."""
    status: str  # "healthy", "warning", "critical"
    message: str
    metrics: HealthMetrics
    recommendations: List[str]


class InfrastructureHealthMonitor:
    """Monitors infrastructure health for automation reliability."""

    def __init__(
        self,
        warning_threshold: float = 85.0,
        critical_threshold: float = 95.0,
        enable_alerting: bool = True
    ):
        """
        Initialize health monitor.

        Args:
            warning_threshold: Percentage threshold for warnings (default: 85%)
            critical_threshold: Percentage threshold for critical alerts (default: 95%)
            enable_alerting: Enable alerting system integration
        """
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.enable_alerting = enable_alerting and ALERTING_AVAILABLE
        if self.enable_alerting:
            self.alerting = AlertingSystem()
        else:
            self.alerting = None

    def check_disk_space(self, path: str = "/") -> Dict[str, Any]:
        """
        Check disk space for a given path.

        Args:
            path: Path to check (defaults to root)

        Returns:
            Dictionary with disk space information
        """
        try:
            # Handle Windows vs Unix paths
            if platform.system() == "Windows":
                # Use C: drive for Windows
                usage = psutil.disk_usage("C:")
            else:
                usage = psutil.disk_usage(path)

            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            usage_percent = usage.percent

            return {
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "usage_percent": round(usage_percent, 2),
                "status": self._get_status_from_percent(usage_percent)
            }
        except Exception as e:
            logger.error(f"Failed to check disk space: {e}")
            return {
                "error": str(e),
                "status": "unknown"
            }

    def check_memory_usage(self) -> Dict[str, Any]:
        """Check system memory usage."""
        try:
            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024**3)
            used_gb = memory.used / (1024**3)
            free_gb = memory.available / (1024**3)
            usage_percent = memory.percent

            return {
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "usage_percent": round(usage_percent, 2),
                "status": self._get_status_from_percent(usage_percent)
            }
        except Exception as e:
            logger.error(f"Failed to check memory usage: {e}")
            return {
                "error": str(e),
                "status": "unknown"
            }

    def check_cpu_usage(self) -> Dict[str, Any]:
        """Check CPU usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return {
                "usage_percent": round(cpu_percent, 2),
                "status": self._get_status_from_percent(cpu_percent)
            }
        except Exception as e:
            logger.error(f"Failed to check CPU usage: {e}")
            return {
                "error": str(e),
                "status": "unknown"
            }

    def check_system_load(self) -> Dict[str, Any]:
        """Check system load average."""
        try:
            if platform.system() != "Windows":
                load_avg = os.getloadavg()
                return {
                    "load_1m": round(load_avg[0], 2),
                    "load_5m": round(load_avg[1], 2),
                    "load_15m": round(load_avg[2], 2),
                    "status": "healthy"  # Load averages don't have simple thresholds
                }
            else:
                # Windows doesn't have load averages
                return {
                    "load_1m": None,
                    "load_5m": None,
                    "load_15m": None,
                    "status": "not_applicable"
                }
        except Exception as e:
            logger.error(f"Failed to check system load: {e}")
            return {
                "error": str(e),
                "status": "unknown"
            }

    def check_browser_automation_readiness(self) -> Dict[str, Any]:
        """
        Check if browser automation is ready.

        Returns:
            Dictionary with browser readiness information
        """
        try:
            # Check if selenium/geckodriver/chromedriver are available
            browser_ready = True
            issues = []

            # Check for Chrome/Chromium
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            ]

            chrome_found = any(Path(path).exists() for path in chrome_paths)
            if not chrome_found:
                browser_ready = False
                issues.append("Chrome/Chromium browser not found")

            # Check for undetected-chromedriver
            try:
                import undetected_chromedriver as uc
                uc_available = uc is not None
            except ImportError:
                uc_available = False
                browser_ready = False
                issues.append("undetected-chromedriver not available")

            # Check for selenium
            try:
                import selenium
                selenium_available = True
            except ImportError:
                selenium_available = False
                browser_ready = False
                issues.append("selenium not available")

            return {
                "browser_ready": browser_ready,
                "chrome_available": chrome_found,
                "uc_available": uc_available,
                "selenium_available": selenium_available,
                "issues": issues,
                "status": "healthy" if browser_ready else "critical"
            }
        except Exception as e:
            logger.error(f"Failed to check browser automation readiness: {e}")
            return {
                "error": str(e),
                "browser_ready": False,
                "status": "critical"
            }

    def perform_full_health_check(self) -> HealthCheckResult:
        """
        Perform a comprehensive health check.

        Returns:
            HealthCheckResult with status, message, metrics, and recommendations
        """
        logger.info("🔍 Performing comprehensive infrastructure health check...")

        # Gather all metrics
        disk_info = self.check_disk_space()
        memory_info = self.check_memory_usage()
        cpu_info = self.check_cpu_usage()
        load_info = self.check_system_load()
        browser_info = self.check_browser_automation_readiness()

        # Create metrics object
        metrics = HealthMetrics(
            disk_usage_percent=disk_info.get("usage_percent", 0),
            disk_free_gb=disk_info.get("free_gb", 0),
            disk_total_gb=disk_info.get("total_gb", 0),
            memory_usage_percent=memory_info.get("usage_percent", 0),
            memory_free_gb=memory_info.get("free_gb", 0),
            cpu_usage_percent=cpu_info.get("usage_percent", 0),
            system_load=load_info.get("load_1m"),
            browser_ready=browser_info.get("browser_ready", False),
            automation_ready=browser_info.get("browser_ready", False)
        )

        # Determine overall status
        status_levels = [
            disk_info.get("status", "unknown"),
            memory_info.get("status", "unknown"),
            cpu_info.get("status", "unknown"),
            browser_info.get("status", "unknown")
        ]

        if "critical" in status_levels:
            overall_status = "critical"
        elif "warning" in status_levels:
            overall_status = "warning"
        elif all(s == "healthy" for s in status_levels if s != "unknown"):
            overall_status = "healthy"
        else:
            overall_status = "unknown"

        # Generate message
        if overall_status == "healthy":
            message = "✅ Infrastructure health check passed - all systems operational"
        elif overall_status == "warning":
            message = "⚠️ Infrastructure health check warning - monitor resource usage"
        else:
            message = "🚨 Infrastructure health check critical - immediate action required"
        
        # Send alerts if enabled
        if self.enable_alerting and self.alerting:
            # Alert on disk space
            if disk_info.get("usage_percent", 0) >= self.warning_threshold:
                self.alerting.alert_disk_space(
                    disk_info.get("usage_percent", 0),
                    disk_info.get("free_gb", 0),
                    self.warning_threshold,
                    self.critical_threshold
                )
            
            # Alert on memory usage
            if memory_info.get("usage_percent", 0) >= self.warning_threshold:
                self.alerting.alert_memory_usage(
                    memory_info.get("usage_percent", 0),
                    memory_info.get("free_gb", 0),
                    self.warning_threshold,
                    self.critical_threshold
                )
            
            # Alert on CPU usage
            if cpu_info.get("usage_percent", 0) >= 90.0:
                self.alerting.alert_cpu_usage(
                    cpu_info.get("usage_percent", 0),
                    90.0,
                    95.0
                )
            
            # Send overall status alert if critical
            if overall_status == "critical":
                self.alerting.send_alert(
                    AlertLevel.CRITICAL,
                    "Infrastructure Health Critical",
                    message,
                    source="health_monitor",
                    metadata={
                        "disk_usage": disk_info.get("usage_percent", 0),
                        "memory_usage": memory_info.get("usage_percent", 0),
                        "cpu_usage": cpu_info.get("usage_percent", 0)
                    }
                )

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, disk_info, browser_info)

        return HealthCheckResult(
            status=overall_status,
            message=message,
            metrics=metrics,
            recommendations=recommendations
        )

    def _get_status_from_percent(self, percent: float) -> str:
        """Get status based on percentage thresholds."""
        if percent >= self.critical_threshold:
            return "critical"
        elif percent >= self.warning_threshold:
            return "warning"
        else:
            return "healthy"

    def _generate_recommendations(self, metrics: HealthMetrics, disk_info: Dict, browser_info: Dict) -> List[str]:
        """Generate recommendations based on health metrics."""
        recommendations = []

        # Disk space recommendations
        if metrics.disk_usage_percent >= self.critical_threshold:
            recommendations.append("🚨 CRITICAL: Clear disk space immediately to prevent system failures")
            recommendations.append("   - Delete temporary files and cache")
            recommendations.append("   - Move large files to external storage")
            recommendations.append("   - Check for disk space hogs: du -sh /*")
        elif metrics.disk_usage_percent >= self.warning_threshold:
            recommendations.append("⚠️ WARNING: Disk usage high - monitor and plan cleanup")
            recommendations.append("   - Schedule disk cleanup maintenance")

        # Memory recommendations
        if metrics.memory_usage_percent >= self.critical_threshold:
            recommendations.append("🚨 CRITICAL: High memory usage - restart memory-intensive processes")
        elif metrics.memory_usage_percent >= self.warning_threshold:
            recommendations.append("⚠️ WARNING: Memory usage elevated - monitor for leaks")

        # Browser automation recommendations
        if not metrics.browser_ready:
            recommendations.append("🚨 CRITICAL: Browser automation not ready")
            if browser_info.get("issues"):
                for issue in browser_info["issues"]:
                    recommendations.append(f"   - Fix: {issue}")

        # General recommendations
        if metrics.disk_free_gb < 1.0:
            recommendations.append("🚨 CRITICAL: Less than 1GB free disk space - immediate action required")

        return recommendations

    def print_health_report(self, result: HealthCheckResult) -> None:
        """Print a formatted health report."""
        print(f"\n{'='*60}")
        print("🏥 INFRASTRUCTURE HEALTH REPORT")
        print(f"{'='*60}")
        print(f"Status: {result.status.upper()}")
        print(f"Message: {result.message}")
        print()

        print("📊 METRICS:")
        print(f"  Disk Usage: {result.metrics.disk_usage_percent:.1f}% ({result.metrics.disk_free_gb:.1f} GB free / {result.metrics.disk_total_gb:.1f} GB total)")
        print(f"  Memory Usage: {result.metrics.memory_usage_percent:.1f}% ({result.metrics.memory_free_gb:.1f} GB free)")
        print(f"  CPU Usage: {result.metrics.cpu_usage_percent:.1f}%")
        if result.metrics.system_load:
            print(f"  System Load: {result.metrics.system_load:.2f}")
        print(f"  Browser Ready: {'✅ Yes' if result.metrics.browser_ready else '❌ No'}")
        print(f"  Automation Ready: {'✅ Yes' if result.metrics.automation_ready else '❌ No'}")
        print()

        if result.recommendations:
            print("💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"  {rec}")
            print()

        print(f"{'='*60}")


# CLI interface
def main():
    """CLI interface for infrastructure health monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Infrastructure Health Monitor")
    parser.add_argument("--check", action="store_true", help="Perform full health check")
    parser.add_argument("--disk", action="store_true", help="Check disk space only")
    parser.add_argument("--memory", action="store_true", help="Check memory usage only")
    parser.add_argument("--cpu", action="store_true", help="Check CPU usage only")
    parser.add_argument("--browser", action="store_true", help="Check browser automation readiness only")
    parser.add_argument("--warning-threshold", type=float, default=85.0, help="Warning threshold percentage")
    parser.add_argument("--critical-threshold", type=float, default=95.0, help="Critical threshold percentage")

    args = parser.parse_args()

    monitor = InfrastructureHealthMonitor(
        warning_threshold=args.warning_threshold,
        critical_threshold=args.critical_threshold
    )

    if args.check:
        result = monitor.perform_full_health_check()
        monitor.print_health_report(result)
    elif args.disk:
        disk_info = monitor.check_disk_space()
        print("Disk Space:", disk_info)
    elif args.memory:
        memory_info = monitor.check_memory_usage()
        print("Memory Usage:", memory_info)
    elif args.cpu:
        cpu_info = monitor.check_cpu_usage()
        print("CPU Usage:", cpu_info)
    elif args.browser:
        browser_info = monitor.check_browser_automation_readiness()
        print("Browser Automation:", browser_info)
    else:
        # Default to full check
        result = monitor.perform_full_health_check()
        monitor.print_health_report(result)


if __name__ == "__main__":
    main()
