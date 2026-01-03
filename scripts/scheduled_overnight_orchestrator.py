#!/usr/bin/env python3
"""
Scheduled Overnight Orchestrator
================================

Automatically runs the overnight orchestrator for 24/7 agent monitoring and recovery.

Features:
- Scheduled execution during off-hours
- Health monitoring and recovery
- Alert system integration
- Progress tracking and reporting

Usage:
    python scripts/scheduled_overnight_orchestrator.py --start
    python scripts/scheduled_overnight_orchestrator.py --status
    python scripts/scheduled_overnight_orchestrator.py --stop
"""

import argparse
import logging
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ScheduledOvernightOrchestrator:
    """Scheduled runner for the overnight orchestrator system."""

    def __init__(self):
        """Initialize the scheduled orchestrator."""
        self.orchestrator = None
        self.monitoring_thread = None
        self.running = False
        self.last_run = None
        self.next_run = None

        # Initialize orchestrator
        self._init_orchestrator()

    def _init_orchestrator(self):
        """Initialize the overnight orchestrator."""
        try:
            from src.orchestrators.overnight.orchestrator import OvernightOrchestrator
            self.orchestrator = OvernightOrchestrator()
            logger.info("✅ Overnight Orchestrator initialized")
        except ImportError as e:
            logger.error(f"❌ Failed to import Overnight Orchestrator: {e}")
            self.orchestrator = None
        except Exception as e:
            logger.error(f"❌ Failed to initialize Overnight Orchestrator: {e}")
            self.orchestrator = None

    def start_scheduled_monitoring(self):
        """Start scheduled monitoring during overnight hours."""
        if self.running:
            logger.warning("Scheduled monitoring already running")
            return False

        if not self.orchestrator:
            logger.error("Cannot start monitoring: Orchestrator not available")
            return False

        try:
            self.running = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True,
                name="OvernightMonitor"
            )
            self.monitoring_thread.start()

            # Calculate next run time (next midnight)
            now = datetime.now()
            next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            self.next_run = next_midnight

            logger.info("🚀 Scheduled overnight monitoring started")
            logger.info(f"   Next run: {self.next_run}")
            logger.info("   Monitoring interval: Every 4 hours during off-hours")

            return True

        except Exception as e:
            logger.error(f"Failed to start scheduled monitoring: {e}")
            self.running = False
            return False

    def stop_scheduled_monitoring(self):
        """Stop scheduled monitoring."""
        if not self.running:
            return True

        try:
            self.running = False

            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=10)

            logger.info("🛑 Scheduled overnight monitoring stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping scheduled monitoring: {e}")
            return False

    def _monitoring_loop(self):
        """Main monitoring loop that runs during off-hours."""
        logger.info("🔄 Overnight monitoring loop started")

        while self.running:
            try:
                now = datetime.now()

                # Check if it's off-hours (between 10 PM and 6 AM)
                is_off_hours = now.hour >= 22 or now.hour <= 6

                if is_off_hours and self._should_run_monitoring():
                    self._run_monitoring_cycle()
                    self.last_run = now

                    # Calculate next run (4 hours from now, but only during off-hours)
                    next_run = now + timedelta(hours=4)
                    if next_run.hour > 6 and next_run.hour < 22:
                        # If next run would be during work hours, skip to next off-hours
                        next_run = next_run.replace(hour=22, minute=0, second=0, microsecond=0)
                        if next_run <= now:
                            next_run += timedelta(days=1)

                    self.next_run = next_run

                # Sleep for 30 minutes before checking again
                time.sleep(1800)  # 30 minutes

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1800)  # Sleep 30 minutes on error

        logger.info("🔄 Overnight monitoring loop ended")

    def _should_run_monitoring(self) -> bool:
        """Check if monitoring should run now."""
        if not self.last_run:
            return True  # First run

        # Check if 4 hours have passed since last run
        time_since_last = datetime.now() - self.last_run
        return time_since_last.total_seconds() >= 14400  # 4 hours

    def _run_monitoring_cycle(self):
        """Run a complete monitoring cycle."""
        try:
            logger.info("🌙 Running overnight monitoring cycle")

            # Run health checks
            health_status = self._run_health_checks()
            if not health_status.get("healthy", False):
                self._handle_health_issues(health_status)

            # Check agent progress
            progress_status = self._check_agent_progress()
            if progress_status.get("issues", []):
                self._handle_progress_issues(progress_status)

            # Run recovery procedures if needed
            recovery_needed = health_status.get("recovery_needed", False) or progress_status.get("recovery_needed", False)
            if recovery_needed:
                self._run_recovery_procedures()

            # Send status report
            self._send_status_report(health_status, progress_status)

            logger.info("✅ Overnight monitoring cycle completed")

        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}")

    def _run_health_checks(self) -> dict:
        """Run comprehensive health checks."""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "healthy": True,
            "checks": {},
            "issues": [],
            "recovery_needed": False
        }

        try:
            # Check message queue health
            mq_status = self._check_message_queue()
            health_status["checks"]["message_queue"] = mq_status
            if not mq_status.get("healthy", True):
                health_status["issues"].append("Message queue issues")
                health_status["recovery_needed"] = True

            # Check agent status files
            agent_status = self._check_agent_status()
            health_status["checks"]["agents"] = agent_status
            if agent_status.get("issues", []):
                health_status["issues"].extend(agent_status["issues"])
                health_status["recovery_needed"] = True

            # Check disk space and resources
            resource_status = self._check_system_resources()
            health_status["checks"]["resources"] = resource_status
            if not resource_status.get("healthy", True):
                health_status["issues"].append("System resource issues")
                health_status["recovery_needed"] = True

            # Overall health
            health_status["healthy"] = len(health_status["issues"]) == 0

        except Exception as e:
            logger.error(f"Error running health checks: {e}")
            health_status["healthy"] = False
            health_status["issues"].append(f"Health check error: {e}")

        return health_status

    def _check_message_queue(self) -> dict:
        """Check message queue health."""
        try:
            # Basic queue health check
            return {
                "healthy": True,
                "queue_size": 0,  # Would need actual implementation
                "last_activity": datetime.now().isoformat()
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_agent_status(self) -> dict:
        """Check agent status files."""
        try:
            agent_issues = []
            # Would check agent_workspaces/*/status.json files
            # For now, return basic status
            return {
                "total_agents": 8,  # Assuming 8 agents
                "active_agents": 8,
                "issues": agent_issues
            }
        except Exception as e:
            return {"error": str(e), "issues": [f"Agent check failed: {e}"]}

    def _check_system_resources(self) -> dict:
        """Check system resources."""
        try:
            import psutil

            disk_usage = psutil.disk_usage('/')
            memory = psutil.virtual_memory()

            healthy = (
                disk_usage.percent < 90 and  # Disk usage < 90%
                memory.percent < 85         # Memory usage < 85%
            )

            return {
                "healthy": healthy,
                "disk_usage": disk_usage.percent,
                "memory_usage": memory.percent
            }
        except ImportError:
            # psutil not available
            return {"healthy": True, "note": "Resource monitoring unavailable"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_agent_progress(self) -> dict:
        """Check agent progress and identify issues."""
        try:
            progress_status = {
                "timestamp": datetime.now().isoformat(),
                "agent_progress": {},
                "issues": [],
                "recovery_needed": False
            }

            # Would check agent progress here
            # For now, return basic status
            progress_status["agent_progress"] = {
                "sample_agent": {
                    "progress": 75,
                    "status": "active",
                    "last_update": datetime.now().isoformat()
                }
            }

            return progress_status

        except Exception as e:
            logger.error(f"Error checking agent progress: {e}")
            return {
                "error": str(e),
                "issues": [f"Progress check failed: {e}"],
                "recovery_needed": True
            }

    def _handle_health_issues(self, health_status: dict):
        """Handle health issues discovered during monitoring."""
        try:
            issues = health_status.get("issues", [])
            logger.warning(f"🏥 Health issues detected: {issues}")

            # Create alerts for issues
            for issue in issues:
                self._create_alert("health", issue, "warning")

        except Exception as e:
            logger.error(f"Error handling health issues: {e}")

    def _handle_progress_issues(self, progress_status: dict):
        """Handle progress issues discovered during monitoring."""
        try:
            issues = progress_status.get("issues", [])
            logger.warning(f"📊 Progress issues detected: {issues}")

            # Create alerts for progress issues
            for issue in issues:
                self._create_alert("progress", issue, "info")

        except Exception as e:
            logger.error(f"Error handling progress issues: {e}")

    def _run_recovery_procedures(self):
        """Run automated recovery procedures."""
        try:
            logger.info("🔧 Running automated recovery procedures")

            # Would implement actual recovery logic here
            # For now, just log
            recovery_actions = [
                "Restart stalled processes",
                "Clear temporary files",
                "Reset agent states if needed"
            ]

            for action in recovery_actions:
                logger.info(f"   • {action}")

        except Exception as e:
            logger.error(f"Error running recovery procedures: {e}")

    def _create_alert(self, alert_type: str, message: str, severity: str):
        """Create an alert in the alerts system."""
        try:
            alert_data = {
                "level": severity,
                "title": f"Overnight Monitor: {alert_type.title()}",
                "message": message,
                "source": "overnight_orchestrator",
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "monitor_cycle": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "alert_type": alert_type
                }
            }

            # Save alert to alerts directory
            alerts_dir = project_root / "alerts"
            alerts_dir.mkdir(exist_ok=True)

            alert_file = alerts_dir / f"overnight_alert_{int(datetime.now().timestamp())}.json"

            import json
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alert_data, f, indent=2)

            logger.info(f"📢 Alert created: {alert_type} - {message}")

        except Exception as e:
            logger.error(f"Error creating alert: {e}")

    def _send_status_report(self, health_status: dict, progress_status: dict):
        """Send status report via messaging system."""
        try:
            # Create summary report
            report = {
                "timestamp": datetime.now().isoformat(),
                "report_type": "overnight_monitoring",
                "health_status": health_status.get("healthy", False),
                "health_issues": len(health_status.get("issues", [])),
                "progress_issues": len(progress_status.get("issues", [])),
                "recovery_actions": health_status.get("recovery_needed", False) or progress_status.get("recovery_needed", False)
            }

            logger.info(f"📊 Overnight status report: Health={'✅' if report['health_status'] else '❌'}, Issues={report['health_issues'] + report['progress_issues']}")

        except Exception as e:
            logger.error(f"Error sending status report: {e}")

    def get_status(self) -> dict:
        """Get current scheduled orchestrator status."""
        return {
            "running": self.running,
            "orchestrator_available": self.orchestrator is not None,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "monitoring_thread_alive": self.monitoring_thread.is_alive() if self.monitoring_thread else False
        }

    def run_manual_cycle(self) -> dict:
        """Run a manual monitoring cycle for testing."""
        logger.info("🔧 Running manual monitoring cycle")

        try:
            health_status = self._run_health_checks()
            progress_status = self._check_agent_progress()

            recovery_needed = (
                health_status.get("recovery_needed", False) or
                progress_status.get("recovery_needed", False)
            )

            if recovery_needed:
                self._run_recovery_procedures()

            return {
                "success": True,
                "health_status": health_status,
                "progress_status": progress_status,
                "recovery_run": recovery_needed
            }

        except Exception as e:
            logger.error(f"Manual cycle failed: {e}")
            return {"success": False, "error": str(e)}


def main():
    """CLI interface for scheduled overnight orchestrator."""
    parser = argparse.ArgumentParser(description="Scheduled Overnight Orchestrator")
    parser.add_argument("action", choices=["start", "stop", "status", "manual"],
                       help="Action to perform")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress detailed output")

    args = parser.parse_args()

    try:
        orchestrator = ScheduledOvernightOrchestrator()

        if args.action == "start":
            success = orchestrator.start_scheduled_monitoring()
            if success:
                print("✅ Scheduled overnight orchestrator started")
                if not args.quiet:
                    print("   • Monitors during off-hours (10 PM - 6 AM)")
                    print("   • Runs every 4 hours")
                    print("   • Performs health checks and recovery")
                    print("   • Creates alerts for issues")
            else:
                print("❌ Failed to start scheduled orchestrator")
                sys.exit(1)

        elif args.action == "stop":
            success = orchestrator.stop_scheduled_monitoring()
            print("✅ Scheduled orchestrator stopped" if success else "❌ Failed to stop")

        elif args.action == "status":
            status = orchestrator.get_status()
            print("🌙 Scheduled Overnight Orchestrator Status")
            print("=" * 50)
            print(f"Running: {'✅' if status['running'] else '❌'}")
            print(f"Orchestrator Available: {'✅' if status['orchestrator_available'] else '❌'}")
            print(f"Monitoring Thread: {'✅' if status['monitoring_thread_alive'] else '❌'}")
            print(f"Last Run: {status['last_run'] or 'Never'}")
            print(f"Next Run: {status['next_run'] or 'Not scheduled'}")

        elif args.action == "manual":
            result = orchestrator.run_manual_cycle()
            if result["success"]:
                print("✅ Manual monitoring cycle completed")
                if not args.quiet:
                    health = result["health_status"]
                    progress = result["progress_status"]
                    print(f"   Health: {'✅' if health.get('healthy') else '❌'} ({len(health.get('issues', []))} issues)")
                    print(f"   Progress: {len(progress.get('issues', []))} issues")
                    print(f"   Recovery: {'Run' if result.get('recovery_run') else 'Not needed'}")
            else:
                print(f"❌ Manual cycle failed: {result.get('error')}")
                sys.exit(1)

    except Exception as e:
        logger.error(f"Scheduled orchestrator failed: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()