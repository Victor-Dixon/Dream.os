#!/usr/bin/env python3
"""
Message Queue Error Monitor
============================

<!-- SSOT Domain: communication -->

Monitors message queue for errors, stuck messages, and processing issues.
Detects and alerts on stuck messages, high failure rates, and processing problems.

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-13
V2 Compliant: Yes
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class StuckMessageAlert:
    """Alert for a stuck message."""
    queue_id: str
    recipient: str
    status: str
    stuck_duration_seconds: float
    first_processing_time: str
    current_time: str
    severity: str  # 'warning' or 'critical'


@dataclass
class ErrorAlert:
    """General error alert."""
    alert_type: str
    severity: str  # 'info', 'warning', 'critical'
    message: str
    timestamp: str
    details: Dict[str, Any]


class MessageQueueErrorMonitor:
    """
    Monitors message queue for errors and stuck messages.
    
    Detects:
    - Stuck messages (PROCESSING status for extended period)
    - High failure rates
    - Processing bottlenecks
    - Queue health issues
    """
    
    # Thresholds (in seconds)
    STUCK_WARNING_THRESHOLD = 60  # 1 minute
    STUCK_CRITICAL_THRESHOLD = 300  # 5 minutes
    
    def __init__(self, queue_file: Optional[Path] = None, alerts_file: Optional[Path] = None):
        """Initialize error monitor.
        
        Args:
            queue_file: Path to queue.json file
            alerts_file: Path to store alerts (default: message_queue/alerts.json)
        """
        project_root = Path(__file__).resolve().parent.parent.parent
        queue_dir = project_root / "message_queue"
        queue_dir.mkdir(exist_ok=True)
        
        self.queue_file = queue_file or (queue_dir / "queue.json")
        self.alerts_file = alerts_file or (queue_dir / "alerts.json")
        
    def check_stuck_messages(self) -> List[StuckMessageAlert]:
        """Check for messages stuck in PROCESSING status.
        
        Returns:
            List of stuck message alerts
        """
        alerts = []
        
        if not self.queue_file.exists():
            return alerts
        
        try:
            # Load queue entries
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            if not isinstance(entries, list):
                return alerts
            
            current_time = time.time()
            
            for entry in entries:
                status = entry.get('status', 'UNKNOWN')
                
                # Only check PROCESSING status
                if status != 'PROCESSING':
                    continue
                
                # Get processing start time
                updated_at = entry.get('updated_at')
                if not updated_at:
                    # Fall back to created_at if updated_at missing
                    updated_at = entry.get('created_at')
                
                if not updated_at:
                    # Can't determine age, skip
                    continue
                
                # Parse timestamp
                try:
                    if isinstance(updated_at, str):
                        # Try ISO format
                        if 'T' in updated_at:
                            dt = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                        else:
                            # Try other formats
                            dt = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                    else:
                        # Assume Unix timestamp
                        dt = datetime.fromtimestamp(updated_at)
                    
                    processing_start = dt.timestamp()
                    stuck_duration = current_time - processing_start
                    
                    # Check thresholds
                    if stuck_duration >= self.STUCK_CRITICAL_THRESHOLD:
                        severity = 'critical'
                    elif stuck_duration >= self.STUCK_WARNING_THRESHOLD:
                        severity = 'warning'
                    else:
                        continue  # Not stuck yet
                    
                    alert = StuckMessageAlert(
                        queue_id=entry.get('queue_id', 'unknown'),
                        recipient=entry.get('message', {}).get('recipient', 'unknown'),
                        status=status,
                        stuck_duration_seconds=stuck_duration,
                        first_processing_time=updated_at,
                        current_time=datetime.now().isoformat(),
                        severity=severity
                    )
                    alerts.append(alert)
                    
                except (ValueError, TypeError) as e:
                    logger.debug(f"Error parsing timestamp for entry {entry.get('queue_id')}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error checking stuck messages: {e}", exc_info=True)
        
        return alerts
    
    def check_failure_rate(self, window_size: int = 100) -> Optional[ErrorAlert]:
        """Check for high failure rate in recent messages.
        
        Args:
            window_size: Number of recent messages to analyze
            
        Returns:
            ErrorAlert if failure rate exceeds threshold, None otherwise
        """
        if not self.queue_file.exists():
            return None
        
        try:
            # Load queue entries
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            if not isinstance(entries, list):
                return None
            
            # Get recent entries (last N)
            recent_entries = entries[-window_size:] if len(entries) > window_size else entries
            
            if not recent_entries:
                return None
            
            # Count failures
            total = len(recent_entries)
            failed = sum(1 for e in recent_entries if e.get('status') == 'FAILED')
            failure_rate = failed / total if total > 0 else 0.0
            
            # Check thresholds
            if failure_rate >= 0.10:  # 10%
                severity = 'critical'
            elif failure_rate >= 0.05:  # 5%
                severity = 'warning'
            else:
                return None  # Within acceptable range
            
            alert = ErrorAlert(
                alert_type='high_failure_rate',
                severity=severity,
                message=f"Failure rate {failure_rate:.1%} exceeds threshold",
                timestamp=datetime.now().isoformat(),
                details={
                    'failure_rate': failure_rate,
                    'failed_messages': failed,
                    'total_messages': total,
                    'window_size': window_size
                }
            )
            
            return alert
            
        except Exception as e:
            logger.error(f"Error checking failure rate: {e}", exc_info=True)
            return None
    
    def check_queue_health(self) -> Optional[ErrorAlert]:
        """Check overall queue health.
        
        Returns:
            ErrorAlert if health issues detected, None otherwise
        """
        if not self.queue_file.exists():
            return None
        
        try:
            # Load queue entries
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            if not isinstance(entries, list):
                return None
            
            total = len(entries)
            pending = sum(1 for e in entries if e.get('status') == 'PENDING')
            processing = sum(1 for e in entries if e.get('status') == 'PROCESSING')
            failed = sum(1 for e in entries if e.get('status') == 'FAILED')
            
            # Check queue size
            if total > 1000:
                severity = 'critical'
                message = f"Queue size critically high: {total} messages"
            elif total > 500:
                severity = 'warning'
                message = f"Queue size elevated: {total} messages"
            else:
                return None  # Queue size acceptable
            
            alert = ErrorAlert(
                alert_type='queue_size',
                severity=severity,
                message=message,
                timestamp=datetime.now().isoformat(),
                details={
                    'total_messages': total,
                    'pending': pending,
                    'processing': processing,
                    'failed': failed
                }
            )
            
            return alert
            
        except Exception as e:
            logger.error(f"Error checking queue health: {e}", exc_info=True)
            return None
    
    def run_checks(self) -> Dict[str, Any]:
        """Run all monitoring checks.
        
        Returns:
            Dictionary with check results and alerts
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'stuck_messages': [],
            'alerts': []
        }
        
        # Check for stuck messages
        stuck_alerts = self.check_stuck_messages()
        results['stuck_messages'] = [asdict(alert) for alert in stuck_alerts]
        
        # Add stuck message alerts
        for alert in stuck_alerts:
            error_alert = ErrorAlert(
                alert_type='stuck_message',
                severity=alert.severity,
                message=f"Message {alert.queue_id} stuck in PROCESSING for {alert.stuck_duration_seconds:.1f}s",
                timestamp=alert.current_time,
                details=asdict(alert)
            )
            results['alerts'].append(asdict(error_alert))
        
        # Check failure rate
        failure_alert = self.check_failure_rate()
        if failure_alert:
            results['alerts'].append(asdict(failure_alert))
        
        # Check queue health
        health_alert = self.check_queue_health()
        if health_alert:
            results['alerts'].append(asdict(health_alert))
        
        # Save alerts
        if results['alerts']:
            self._save_alerts(results['alerts'])
        
        return results
    
    def reset_stuck_messages(self, stuck_alerts: Optional[List[StuckMessageAlert]] = None) -> int:
        """Reset stuck messages back to PENDING status.
        
        Args:
            stuck_alerts: List of stuck message alerts (None = auto-detect)
            
        Returns:
            Number of messages reset
        """
        if stuck_alerts is None:
            stuck_alerts = self.check_stuck_messages()
        
        if not stuck_alerts:
            return 0
        
        if not self.queue_file.exists():
            return 0
        
        try:
            # Load queue entries
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            if not isinstance(entries, list):
                return 0
            
            # Create lookup for stuck message IDs
            stuck_ids = {alert.queue_id for alert in stuck_alerts}
            
            # Reset stuck messages
            reset_count = 0
            for entry in entries:
                if entry.get('queue_id') in stuck_ids:
                    entry['status'] = 'PENDING'
                    entry['updated_at'] = datetime.now().isoformat()
                    reset_count += 1
                    logger.info(f"Reset stuck message {entry.get('queue_id')} to PENDING")
            
            # Save updated entries
            if reset_count > 0:
                # Create backup
                backup_file = self.queue_file.with_suffix('.json.backup')
                if self.queue_file.exists():
                    import shutil
                    shutil.copy2(self.queue_file, backup_file)
                
                # Save updated queue
                with open(self.queue_file, 'w', encoding='utf-8') as f:
                    json.dump(entries, f, indent=2, default=str)
                
                logger.info(f"Reset {reset_count} stuck messages to PENDING")
            
            return reset_count
            
        except Exception as e:
            logger.error(f"Error resetting stuck messages: {e}", exc_info=True)
            return 0
    
    def _save_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """Save alerts to file.
        
        Args:
            alerts: List of alert dictionaries
        """
        try:
            # Load existing alerts
            existing = []
            if self.alerts_file.exists():
                with open(self.alerts_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            
            # Append new alerts
            existing.extend(alerts)
            
            # Keep only last 1000 alerts
            if len(existing) > 1000:
                existing = existing[-1000:]
            
            # Save
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error saving alerts: {e}", exc_info=True)





