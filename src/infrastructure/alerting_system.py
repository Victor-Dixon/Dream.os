#!/usr/bin/env python3
"""
Infrastructure Alerting System
==============================

Provides alerting capabilities for critical infrastructure issues.
Supports multiple alert channels: Discord, logging, file-based alerts.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
V2 Compliant: <300 lines
"""

import logging
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertChannel(Enum):
    """Available alert channels."""
    LOG = "log"
    FILE = "file"
    DISCORD = "discord"


@dataclass
class Alert:
    """Alert data structure."""
    level: AlertLevel
    title: str
    message: str
    source: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convert alert to dictionary."""
        return {
            "level": self.level.value,
            "title": self.title,
            "message": self.message,
            "source": self.source,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }


class AlertingSystem:
    """Infrastructure alerting system."""
    
    def __init__(
        self,
        alert_dir: Optional[Path] = None,
        enable_discord: bool = False,
        discord_webhook: Optional[str] = None
    ):
        """
        Initialize alerting system.
        
        Args:
            alert_dir: Directory for file-based alerts
            enable_discord: Enable Discord alerts
            discord_webhook: Discord webhook URL
        """
        self.alert_dir = alert_dir or Path("alerts")
        self.alert_dir.mkdir(parents=True, exist_ok=True)
        self.enable_discord = enable_discord
        self.discord_webhook = discord_webhook
        self.alert_history: List[Alert] = []
        
    def send_alert(
        self,
        level: AlertLevel,
        title: str,
        message: str,
        source: str = "infrastructure",
        metadata: Optional[Dict[str, Any]] = None,
        channels: Optional[List[AlertChannel]] = None
    ) -> bool:
        """
        Send alert through specified channels.
        
        Args:
            level: Alert severity level
            title: Alert title
            message: Alert message
            source: Alert source system
            metadata: Additional metadata
            channels: Alert channels (default: all enabled)
            
        Returns:
            True if alert sent successfully
        """
        if channels is None:
            channels = [AlertChannel.LOG, AlertChannel.FILE]
            if self.enable_discord:
                channels.append(AlertChannel.DISCORD)
        
        alert = Alert(
            level=level,
            title=title,
            message=message,
            source=source,
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata or {}
        )
        
        self.alert_history.append(alert)
        
        success = True
        for channel in channels:
            try:
                if channel == AlertChannel.LOG:
                    self._send_log_alert(alert)
                elif channel == AlertChannel.FILE:
                    self._send_file_alert(alert)
                elif channel == AlertChannel.DISCORD:
                    self._send_discord_alert(alert)
            except Exception as e:
                logger.error(f"Failed to send alert via {channel.value}: {e}")
                success = False
        
        return success
    
    def _send_log_alert(self, alert: Alert) -> None:
        """Send alert to logging system."""
        log_level = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.CRITICAL: logging.CRITICAL
        }.get(alert.level, logging.INFO)
        
        log_message = f"[{alert.level.value.upper()}] {alert.title}: {alert.message}"
        logger.log(log_level, log_message)
    
    def _send_file_alert(self, alert: Alert) -> None:
        """Send alert to file system."""
        alert_file = self.alert_dir / f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        alert_file.write_text(json.dumps(alert.to_dict(), indent=2), encoding='utf-8')
        
        # Also append to history file
        history_file = self.alert_dir / "alert_history.jsonl"
        with history_file.open("a", encoding='utf-8') as f:
            f.write(json.dumps(alert.to_dict()) + "\n")
    
    def _send_discord_alert(self, alert: Alert) -> None:
        """Send alert to Discord webhook."""
        if not self.discord_webhook:
            logger.warning("Discord webhook not configured")
            return
        
        try:
            import requests
            
            color_map = {
                AlertLevel.INFO: 0x3498db,      # Blue
                AlertLevel.WARNING: 0xf39c12,   # Orange
                AlertLevel.CRITICAL: 0xe74c3c   # Red
            }
            
            embed = {
                "title": alert.title,
                "description": alert.message,
                "color": color_map.get(alert.level, 0x95a5a6),
                "timestamp": alert.timestamp,
                "fields": [
                    {"name": "Level", "value": alert.level.value.upper(), "inline": True},
                    {"name": "Source", "value": alert.source, "inline": True}
                ]
            }
            
            if alert.metadata:
                for key, value in alert.metadata.items():
                    embed["fields"].append({
                        "name": key,
                        "value": str(value),
                        "inline": True
                    })
            
            payload = {"embeds": [embed]}
            response = requests.post(self.discord_webhook, json=payload, timeout=10)
            response.raise_for_status()
        except ImportError:
            logger.warning("requests library not available for Discord alerts")
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")
            raise
    
    def alert_disk_space(
        self,
        usage_percent: float,
        free_gb: float,
        threshold: float = 85.0,
        critical_threshold: float = 95.0
    ) -> bool:
        """Alert on disk space issues."""
        if usage_percent >= critical_threshold:
            level = AlertLevel.CRITICAL
            title = "🚨 CRITICAL: Disk Space Critical"
            message = f"Disk usage at {usage_percent:.1f}% - {free_gb:.1f} GB free"
        elif usage_percent >= threshold:
            level = AlertLevel.WARNING
            title = "⚠️ WARNING: Disk Space High"
            message = f"Disk usage at {usage_percent:.1f}% - {free_gb:.1f} GB free"
        else:
            return False
        
        return self.send_alert(
            level=level,
            title=title,
            message=message,
            source="disk_monitor",
            metadata={
                "usage_percent": usage_percent,
                "free_gb": free_gb,
                "threshold": threshold
            }
        )
    
    def alert_memory_usage(
        self,
        usage_percent: float,
        free_gb: float,
        threshold: float = 85.0,
        critical_threshold: float = 95.0
    ) -> bool:
        """Alert on memory usage issues."""
        if usage_percent >= critical_threshold:
            level = AlertLevel.CRITICAL
            title = "🚨 CRITICAL: Memory Usage Critical"
            message = f"Memory usage at {usage_percent:.1f}% - {free_gb:.1f} GB free"
        elif usage_percent >= threshold:
            level = AlertLevel.WARNING
            title = "⚠️ WARNING: Memory Usage High"
            message = f"Memory usage at {usage_percent:.1f}% - {free_gb:.1f} GB free"
        else:
            return False
        
        return self.send_alert(
            level=level,
            title=title,
            message=message,
            source="memory_monitor",
            metadata={
                "usage_percent": usage_percent,
                "free_gb": free_gb,
                "threshold": threshold
            }
        )
    
    def alert_cpu_usage(
        self,
        usage_percent: float,
        threshold: float = 90.0,
        critical_threshold: float = 95.0
    ) -> bool:
        """Alert on CPU usage issues."""
        if usage_percent >= critical_threshold:
            level = AlertLevel.CRITICAL
            title = "🚨 CRITICAL: CPU Usage Critical"
            message = f"CPU usage at {usage_percent:.1f}%"
        elif usage_percent >= threshold:
            level = AlertLevel.WARNING
            title = "⚠️ WARNING: CPU Usage High"
            message = f"CPU usage at {usage_percent:.1f}%"
        else:
            return False
        
        return self.send_alert(
            level=level,
            title=title,
            message=message,
            source="cpu_monitor",
            metadata={
                "usage_percent": usage_percent,
                "threshold": threshold
            }
        )
    
    def get_recent_alerts(self, limit: int = 10) -> List[Alert]:
        """Get recent alerts."""
        return self.alert_history[-limit:]
    
    def get_critical_alerts(self) -> List[Alert]:
        """Get all critical alerts."""
        return [a for a in self.alert_history if a.level == AlertLevel.CRITICAL]


def main():
    """CLI interface for alerting system."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Infrastructure Alerting System")
    parser.add_argument("--test", action="store_true", help="Send test alert")
    parser.add_argument("--level", choices=["info", "warning", "critical"], default="info")
    parser.add_argument("--title", default="Test Alert")
    parser.add_argument("--message", default="This is a test alert")
    
    args = parser.parse_args()
    
    alerting = AlertingSystem()
    
    if args.test:
        level = AlertLevel[args.level.upper()]
        alerting.send_alert(
            level=level,
            title=args.title,
            message=args.message,
            source="cli_test"
        )
        print(f"✅ Test alert sent: {args.level.upper()}")
    else:
        print("Infrastructure Alerting System")
        print("Use --test to send a test alert")


if __name__ == "__main__":
    main()

