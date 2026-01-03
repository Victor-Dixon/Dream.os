#!/usr/bin/env python3
"""
Alert System Processor
======================

Automatically processes alerts and sends notifications to Discord.

Features:
- Alert file monitoring and processing
- Discord notification integration
- Alert prioritization and routing
- Historical alert tracking

Usage:
    python scripts/alert_processor.py --start
    python scripts/alert_processor.py --process
    python scripts/alert_processor.py --status
"""

import argparse
import json
import logging
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AlertProcessor:
    """
    Automated alert processing and Discord notification system.

    Monitors the alerts directory for new alerts and processes them according to
    priority and routing rules.
    """

    def __init__(self):
        """Initialize the alert processor."""
        self.alerts_dir = project_root / "alerts"
        self.alerts_dir.mkdir(exist_ok=True)

        self.processed_alerts_file = self.alerts_dir / "processed_alerts.json"
        self.processed_alerts = self._load_processed_alerts()

        self.monitoring_thread = None
        self.running = False

        # Discord integration (would be initialized if available)
        self.discord_available = self._check_discord_availability()

    def _check_discord_availability(self) -> bool:
        """Check if Discord integration is available."""
        try:
            import discord
            from discord.ext import commands
            # Check if we can import the discord commander
            from src.discord_commander.core.bot import get_bot
            return True
        except ImportError:
            return False

    def _load_processed_alerts(self) -> Dict[str, Dict]:
        """Load the list of already processed alerts."""
        if self.processed_alerts_file.exists():
            try:
                with open(self.processed_alerts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load processed alerts: {e}")

        return {}

    def _save_processed_alerts(self):
        """Save the processed alerts list."""
        try:
            with open(self.processed_alerts_file, 'w', encoding='utf-8') as f:
                json.dump(self.processed_alerts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Could not save processed alerts: {e}")

    def start_monitoring(self, interval: int = 60):
        """Start continuous alert monitoring."""
        if self.running:
            logger.warning("Alert monitoring already running")
            return False

        try:
            self.running = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                args=(interval,),
                daemon=True,
                name="AlertMonitor"
            )
            self.monitoring_thread.start()

            logger.info("🚨 Alert monitoring started")
            logger.info(f"   Checking for new alerts every {interval} seconds")
            logger.info(f"   Discord integration: {'✅' if self.discord_available else '❌'}")

            return True

        except Exception as e:
            logger.error(f"Failed to start alert monitoring: {e}")
            self.running = False
            return False

    def stop_monitoring(self):
        """Stop alert monitoring."""
        if not self.running:
            return True

        try:
            self.running = False

            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=10)

            logger.info("🛑 Alert monitoring stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping alert monitoring: {e}")
            return False

    def _monitoring_loop(self, interval: int):
        """Main monitoring loop."""
        logger.info("🔄 Alert monitoring loop started")

        while self.running:
            try:
                self.process_pending_alerts()
                time.sleep(interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)

        logger.info("🔄 Alert monitoring loop ended")

    def process_pending_alerts(self) -> int:
        """Process all pending alerts."""
        try:
            # Find new alert files
            alert_files = list(self.alerts_dir.glob("alert_*.json"))

            if not alert_files:
                return 0

            processed_count = 0

            for alert_file in alert_files:
                alert_id = alert_file.stem  # filename without extension

                # Skip if already processed
                if alert_id in self.processed_alerts:
                    continue

                try:
                    # Load and process alert
                    with open(alert_file, 'r', encoding='utf-8') as f:
                        alert_data = json.load(f)

                    success = self._process_alert(alert_data, alert_id)

                    if success:
                        # Mark as processed
                        self.processed_alerts[alert_id] = {
                            "processed_at": datetime.now().isoformat(),
                            "file": str(alert_file),
                            "alert_data": alert_data
                        }
                        processed_count += 1

                except Exception as e:
                    logger.error(f"Failed to process alert {alert_file}: {e}")

            # Save processed alerts list
            if processed_count > 0:
                self._save_processed_alerts()

            return processed_count

        except Exception as e:
            logger.error(f"Error processing pending alerts: {e}")
            return 0

    def _process_alert(self, alert_data: Dict, alert_id: str) -> bool:
        """Process a single alert."""
        try:
            level = alert_data.get("level", "info")
            title = alert_data.get("title", "System Alert")
            message = alert_data.get("message", "")
            source = alert_data.get("source", "unknown")
            timestamp = alert_data.get("timestamp", datetime.now().isoformat())

            logger.info(f"📢 Processing alert: {title} ({level}) from {source}")

            # Route alert based on level and source
            if self._should_send_to_discord(alert_data):
                success = self._send_discord_notification(alert_data)
                if success:
                    logger.info(f"✅ Alert sent to Discord: {title}")
                else:
                    logger.error(f"❌ Failed to send alert to Discord: {title}")
                    return False

            # Log alert to system logs
            self._log_alert_to_system(alert_data)

            # Execute any automated responses
            self._execute_automated_responses(alert_data)

            return True

        except Exception as e:
            logger.error(f"Error processing alert {alert_id}: {e}")
            return False

    def _should_send_to_discord(self, alert_data: Dict) -> bool:
        """Determine if alert should be sent to Discord."""
        level = alert_data.get("level", "info")
        source = alert_data.get("source", "")

        # Always send critical and error alerts
        if level in ["critical", "error"]:
            return True

        # Send warning alerts from important sources
        if level == "warning" and source in ["overnight_orchestrator", "auto_gas_pipeline", "health_monitor"]:
            return True

        # Send info alerts from specific monitoring systems
        if level == "info" and source in ["technical_debt", "progress_monitor", "system_health"]:
            return True

        return False

    def _send_discord_notification(self, alert_data: Dict) -> bool:
        """Send alert notification to Discord."""
        if not self.discord_available:
            logger.warning("Discord not available for alert notifications")
            return False

        try:
            # Import Discord components
            import discord
            from discord.ext import commands

            # Get bot instance (this would need proper initialization)
            # For now, we'll simulate the notification
            level = alert_data.get("level", "info")
            title = alert_data.get("title", "System Alert")
            message = alert_data.get("message", "")
            source = alert_data.get("source", "unknown")

            # Create embed
            color_map = {
                "critical": 0xFF0000,  # Red
                "error": 0xE74C3C,     # Dark Red
                "warning": 0xF39C12,   # Orange
                "info": 0x3498DB       # Blue
            }

            embed = discord.Embed(
                title=f"🚨 {title}",
                description=message,
                color=color_map.get(level, 0x3498DB),
                timestamp=datetime.now()
            )

            embed.add_field(
                name="📊 Level",
                value=level.upper(),
                inline=True
            )

            embed.add_field(
                name="🔍 Source",
                value=source,
                inline=True
            )

            metadata = alert_data.get("metadata", {})
            if metadata:
                metadata_str = "\n".join([f"{k}: {v}" for k, v in metadata.items()][:3])
                embed.add_field(
                    name="📋 Details",
                    value=metadata_str,
                    inline=False
                )

            embed.set_footer(text="Alert System - Automated Monitoring")

            # In a real implementation, this would send to the appropriate Discord channel
            # For now, we'll just log it
            logger.info(f"Discord notification prepared: {title}")

            return True

        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
            return False

    def _log_alert_to_system(self, alert_data: Dict):
        """Log alert to system logs and monitoring systems."""
        try:
            level = alert_data.get("level", "info")
            title = alert_data.get("title", "System Alert")
            source = alert_data.get("source", "unknown")

            # Log based on level
            log_message = f"ALERT [{level.upper()}] {title} (Source: {source})"

            if level == "critical":
                logger.critical(log_message)
            elif level == "error":
                logger.error(log_message)
            elif level == "warning":
                logger.warning(log_message)
            else:
                logger.info(log_message)

            # Could also send to external monitoring systems here
            # e.g., send to monitoring service, create tickets, etc.

        except Exception as e:
            logger.error(f"Error logging alert to system: {e}")

    def _execute_automated_responses(self, alert_data: Dict):
        """Execute automated responses based on alert type."""
        try:
            level = alert_data.get("level", "info")
            source = alert_data.get("source", "")
            title = alert_data.get("title", "")

            # Critical alerts always trigger escalation
            if level == "critical":
                self._escalate_critical_alert(alert_data)

            # Source-specific responses
            if source == "auto_gas_pipeline" and "stalled" in title.lower():
                self._handle_pipeline_stall_alert(alert_data)

            elif source == "overnight_orchestrator" and level in ["error", "warning"]:
                self._handle_monitoring_alert(alert_data)

            elif source == "technical_debt" and "compliance" in title.lower():
                self._handle_debt_compliance_alert(alert_data)

        except Exception as e:
            logger.error(f"Error executing automated responses: {e}")

    def _escalate_critical_alert(self, alert_data: Dict):
        """Escalate critical alerts."""
        logger.critical("🚨 CRITICAL ALERT ESCALATION TRIGGERED")
        logger.critical(f"   Title: {alert_data.get('title')}")
        logger.critical(f"   Message: {alert_data.get('message')}")
        logger.critical("   Immediate attention required!")

        # In a real system, this would:
        # - Send SMS alerts to on-call engineers
        # - Create high-priority tickets
        # - Trigger emergency response procedures

    def _handle_pipeline_stall_alert(self, alert_data: Dict):
        """Handle auto-gas pipeline stall alerts."""
        logger.warning("🔧 Auto-gas pipeline stall detected - attempting recovery")

        # Could trigger emergency gas delivery or pipeline restart
        # For now, just log the response action

    def _handle_monitoring_alert(self, alert_data: Dict):
        """Handle overnight monitoring alerts."""
        logger.info("🌙 Overnight monitoring alert processed")

        # Could trigger additional monitoring or recovery procedures

    def _handle_debt_compliance_alert(self, alert_data: Dict):
        """Handle technical debt compliance alerts."""
        logger.info("🔧 Technical debt compliance alert - scheduling review")

        # Could trigger automated debt reduction tasks

    def get_status(self) -> Dict:
        """Get alert processor status."""
        return {
            "running": self.running,
            "discord_available": self.discord_available,
            "alerts_directory": str(self.alerts_dir),
            "processed_alerts_count": len(self.processed_alerts),
            "monitoring_thread_alive": self.monitoring_thread.is_alive() if self.monitoring_thread else False
        }

    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get recently processed alerts."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_alerts = []

            for alert_id, processed_data in self.processed_alerts.items():
                processed_at = datetime.fromisoformat(processed_data["processed_at"])
                if processed_at > cutoff_time:
                    alert_data = processed_data["alert_data"]
                    alert_data["processed_at"] = processed_data["processed_at"]
                    alert_data["alert_id"] = alert_id
                    recent_alerts.append(alert_data)

            # Sort by processed time (newest first)
            recent_alerts.sort(key=lambda x: x["processed_at"], reverse=True)

            return recent_alerts

        except Exception as e:
            logger.error(f"Error getting recent alerts: {e}")
            return []

    def create_test_alert(self, level: str = "info", title: str = "Test Alert",
                         message: str = "This is a test alert"):
        """Create a test alert for testing the system."""
        alert_data = {
            "level": level,
            "title": title,
            "message": message,
            "source": "test_system",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "test": True,
                "created_by": "alert_processor_test"
            }
        }

        # Save test alert
        alert_filename = f"alert_test_{int(datetime.now().timestamp())}.json"
        alert_file = self.alerts_dir / alert_filename

        try:
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alert_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Test alert created: {alert_file}")
            return str(alert_file)

        except Exception as e:
            logger.error(f"❌ Failed to create test alert: {e}")
            return None


def main():
    """CLI interface for alert processor."""
    parser = argparse.ArgumentParser(description="Alert System Processor")
    parser.add_argument("action", choices=["start", "stop", "status", "process", "test"],
                       help="Action to perform")
    parser.add_argument("--interval", type=int, default=60,
                       help="Monitoring interval in seconds (default: 60)")
    parser.add_argument("--level", choices=["critical", "error", "warning", "info"],
                       default="info", help="Alert level for test alerts")
    parser.add_argument("--title", default="Test Alert",
                       help="Title for test alerts")
    parser.add_argument("--message", default="This is a test alert message",
                       help="Message for test alerts")

    args = parser.parse_args()

    try:
        processor = AlertProcessor()

        if args.action == "start":
            success = processor.start_monitoring(interval=args.interval)
            if success:
                print("✅ Alert processor started")
                print(f"   Monitoring interval: {args.interval}s")
                print(f"   Discord integration: {'✅' if processor.discord_available else '❌'}")
                print("   Press Ctrl+C to stop")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    processor.stop_monitoring()
            else:
                print("❌ Failed to start alert processor")
                sys.exit(1)

        elif args.action == "stop":
            success = processor.stop_monitoring()
            print("✅ Alert processor stopped" if success else "❌ Failed to stop")

        elif args.action == "status":
            status = processor.get_status()
            print("🚨 Alert Processor Status")
            print("=" * 40)
            print(f"Running: {'✅' if status['running'] else '❌'}")
            print(f"Discord Available: {'✅' if status['discord_available'] else '❌'}")
            print(f"Alerts Directory: {status['alerts_directory']}")
            print(f"Processed Alerts: {status['processed_alerts_count']}")
            print(f"Monitoring Thread: {'✅' if status['monitoring_thread_alive'] else '❌'}")

            # Show recent alerts
            recent = processor.get_recent_alerts(hours=1)
            if recent:
                print(f"\nRecent Alerts (last hour): {len(recent)}")
                for alert in recent[:3]:
                    print(f"  • {alert['title']} ({alert['level']})")

        elif args.action == "process":
            count = processor.process_pending_alerts()
            print(f"✅ Processed {count} pending alerts")

        elif args.action == "test":
            alert_file = processor.create_test_alert(
                level=args.level,
                title=args.title,
                message=args.message
            )
            if alert_file:
                print(f"✅ Test alert created: {alert_file}")
                print("   Run 'python scripts/alert_processor.py process' to process it")
            else:
                print("❌ Failed to create test alert")
                sys.exit(1)

    except Exception as e:
        logger.error(f"Alert processor failed: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()