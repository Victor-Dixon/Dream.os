#!/usr/bin/env python3
"""
Unified Monitor - Consolidated Monitoring Tool
==============================================

Consolidates all monitoring capabilities into a single unified tool.
Replaces 33+ individual monitoring tools with modular monitoring system.

Monitoring Categories:
- Service Health (GitHub Pusher, Discord, CI/CD)
- Queue Monitoring (Deferred Push Queue)
- Agent Status (Progress, Stalls, Health)
- Infrastructure (Disk, CI, System)
- Test Coverage Tracking

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
V2 Compliant: Yes (<400 lines)
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UnifiedMonitor:
    """Unified monitoring system consolidating all monitoring capabilities."""
    
    def __init__(self):
        """Initialize unified monitor."""
        self.project_root = project_root
        
    def monitor_queue_health(self) -> Dict[str, Any]:
        """Monitor deferred push queue health."""
        try:
            from src.core.deferred_push_queue import get_deferred_push_queue
            queue = get_deferred_push_queue()
            stats = queue.get_stats()
            
            total = stats.get("total", 0)
            pending = stats.get("pending", 0)
            failed = stats.get("failed", 0)
            
            if total == 0:
                health_score = 100
            else:
                failure_rate = (failed / total) * 100 if total > 0 else 0
                health_score = max(0, 100 - failure_rate)
            
            health_status = "HEALTHY" if health_score >= 80 else "DEGRADED" if health_score >= 50 else "UNHEALTHY"
            
            return {
                "category": "queue",
                "status": health_status,
                "score": health_score,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Queue health check failed: {e}")
            return {
                "category": "queue",
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def monitor_service_health(self, service_name: str) -> Dict[str, Any]:
        """Monitor a specific service health."""
        try:
            import psutil
            
            service_running = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any(service_name.lower() in str(arg).lower() for arg in cmdline):
                        service_running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                "category": "service",
                "service": service_name,
                "status": "RUNNING" if service_running else "STOPPED",
                "running": service_running,
                "timestamp": datetime.now().isoformat()
            }
        except ImportError:
            logger.warning("psutil not available - cannot check service status")
            return {
                "category": "service",
                "service": service_name,
                "status": "UNKNOWN",
                "error": "psutil not available",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Service health check failed: {e}")
            return {
                "category": "service",
                "service": service_name,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def monitor_disk_usage(self, paths: List[str] = None) -> Dict[str, Any]:
        """Monitor disk usage for specified paths."""
        if paths is None:
            paths = ["C:/", "D:/"]
        
        import shutil
        
        disk_info = []
        for path in paths:
            try:
                usage = shutil.disk_usage(path)
                total_gb = usage.total / (1024**3)
                free_gb = usage.free / (1024**3)
                used_percent = (usage.used / usage.total) * 100
                
                disk_info.append({
                    "path": path,
                    "total_gb": round(total_gb, 2),
                    "free_gb": round(free_gb, 2),
                    "used_percent": round(used_percent, 2),
                    "status": "OK" if used_percent < 90 else "WARNING" if used_percent < 95 else "CRITICAL"
                })
            except Exception as e:
                logger.error(f"Disk check failed for {path}: {e}")
                disk_info.append({
                    "path": path,
                    "status": "ERROR",
                    "error": str(e)
                })
        
        return {
            "category": "disk",
            "disks": disk_info,
            "timestamp": datetime.now().isoformat()
        }
    
    def monitor_agent_status(self) -> Dict[str, Any]:
        """Monitor agent workspace status."""
        agents_dir = self.project_root / "agent_workspaces"
        agent_statuses = []
        
        if not agents_dir.exists():
            return {
                "category": "agents",
                "status": "ERROR",
                "error": "Agent workspaces directory not found",
                "timestamp": datetime.now().isoformat()
            }
        
        for agent_dir in sorted(agents_dir.iterdir()):
            if not agent_dir.is_dir():
                continue
            
            status_file = agent_dir / "status.json"
            if not status_file.exists():
                continue
            
            try:
                status_data = json.loads(status_file.read_text())
                agent_statuses.append({
                    "agent_id": status_data.get("agent_id", agent_dir.name),
                    "status": status_data.get("status", "UNKNOWN"),
                    "last_updated": status_data.get("last_updated", "unknown"),
                    "current_mission": status_data.get("current_mission", "")[:100] + "..."
                })
            except Exception as e:
                logger.warning(f"Error reading status for {agent_dir.name}: {e}")
        
        active_count = sum(1 for a in agent_statuses if a.get("status") == "ACTIVE_AGENT_MODE")
        
        return {
            "category": "agents",
            "total_agents": len(agent_statuses),
            "active_agents": active_count,
            "agent_statuses": agent_statuses,
            "timestamp": datetime.now().isoformat()
        }
    
    def monitor_test_coverage(self) -> Dict[str, Any]:
        """Monitor test coverage status."""
        try:
            # Count test files
            tests_dir = self.project_root / "tests"
            test_files = list(tests_dir.rglob("test_*.py")) if tests_dir.exists() else []
            
            return {
                "category": "coverage",
                "total_test_files": len(test_files),
                "target_coverage": 85.0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Test coverage check failed: {e}")
            return {
                "category": "coverage",
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_full_monitoring(self) -> Dict[str, Any]:
        """Run all monitoring checks."""
        logger.info("Running full monitoring suite...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Queue health
        results["checks"]["queue"] = self.monitor_queue_health()
        
        # Service health
        results["checks"]["github_pusher"] = self.monitor_service_health("github_pusher")
        results["checks"]["discord"] = self.monitor_service_health("discord")
        
        # Disk usage
        results["checks"]["disk"] = self.monitor_disk_usage()
        
        # Agent status
        results["checks"]["agents"] = self.monitor_agent_status()
        
        # Test coverage
        results["checks"]["coverage"] = self.monitor_test_coverage()
        
        return results
    
    def print_monitoring_report(self, results: Dict[str, Any]):
        """Print formatted monitoring report."""
        print("\n" + "=" * 70)
        print("📊 UNIFIED MONITORING REPORT")
        print("=" * 70)
        
        checks = results.get("checks", {})
        
        # Queue status
        if "queue" in checks:
            queue = checks["queue"]
            status_icon = "✅" if queue.get("status") == "HEALTHY" else "⚠️" if queue.get("status") == "DEGRADED" else "❌"
            print(f"\n{status_icon} Queue Health: {queue.get('status', 'UNKNOWN')}")
            if "stats" in queue:
                stats = queue["stats"]
                print(f"   Pending: {stats.get('pending', 0)}, Failed: {stats.get('failed', 0)}")
        
        # Service status
        for service_name in ["github_pusher", "discord"]:
            if service_name in checks:
                service = checks[service_name]
                status_icon = "✅" if service.get("running") else "❌"
                print(f"\n{status_icon} {service_name.replace('_', ' ').title()}: {service.get('status', 'UNKNOWN')}")
        
        # Disk usage
        if "disk" in checks:
            disk = checks["disk"]
            print(f"\n💾 Disk Usage:")
            for disk_info in disk.get("disks", []):
                status_icon = "✅" if disk_info.get("status") == "OK" else "⚠️"
                print(f"   {status_icon} {disk_info.get('path')}: {disk_info.get('used_percent', 0):.1f}% used "
                      f"({disk_info.get('free_gb', 0):.1f} GB free)")
        
        # Agent status
        if "agents" in checks:
            agents = checks["agents"]
            print(f"\n👥 Agents: {agents.get('active_agents', 0)}/{agents.get('total_agents', 0)} active")
        
        # Test coverage
        if "coverage" in checks:
            coverage = checks["coverage"]
            print(f"\n🧪 Test Files: {coverage.get('total_test_files', 0)}")
        
        print(f"\n🕐 Timestamp: {results.get('timestamp', 'unknown')}")
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Unified Monitoring Tool - Consolidated monitoring for all systems",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--category", "-c",
        choices=["queue", "service", "disk", "agents", "coverage", "all"],
        default="all",
        help="Monitoring category to check (default: all)"
    )
    
    parser.add_argument(
        "--service", "-s",
        type=str,
        help="Service name for service monitoring"
    )
    
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch mode: continuously monitor"
    )
    
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=30,
        help="Watch interval in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    monitor = UnifiedMonitor()
    
    if args.watch:
        logger.info(f"👀 Watch mode: Checking every {args.interval}s (Ctrl+C to stop)")
        try:
            while True:
                if args.category == "all":
                    results = monitor.run_full_monitoring()
                else:
                    # Single category check
                    if args.category == "queue":
                        results = {"checks": {"queue": monitor.monitor_queue_health()}}
                    elif args.category == "service":
                        service_name = args.service or "github_pusher"
                        results = {"checks": {service_name: monitor.monitor_service_health(service_name)}}
                    elif args.category == "disk":
                        results = {"checks": {"disk": monitor.monitor_disk_usage()}}
                    elif args.category == "agents":
                        results = {"checks": {"agents": monitor.monitor_agent_status()}}
                    elif args.category == "coverage":
                        results = {"checks": {"coverage": monitor.monitor_test_coverage()}}
                
                if args.json:
                    print(json.dumps(results, indent=2))
                else:
                    monitor.print_monitoring_report(results)
                
                time.sleep(args.interval)
        except KeyboardInterrupt:
            logger.info("\n🛑 Monitoring stopped")
    else:
        # Single check
        if args.category == "all":
            results = monitor.run_full_monitoring()
        else:
            if args.category == "queue":
                results = {"checks": {"queue": monitor.monitor_queue_health()}}
            elif args.category == "service":
                service_name = args.service or "github_pusher"
                results = {"checks": {service_name: monitor.monitor_service_health(service_name)}}
            elif args.category == "disk":
                results = {"checks": {"disk": monitor.monitor_disk_usage()}}
            elif args.category == "agents":
                results = {"checks": {"agents": monitor.monitor_agent_status()}}
            elif args.category == "coverage":
                results = {"checks": {"coverage": monitor.monitor_test_coverage()}}
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            monitor.print_monitoring_report(results)


if __name__ == "__main__":
    main()

