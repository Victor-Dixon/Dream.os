#!/usr/bin/env python3
"""
FastAPI Monitoring and Alerting
================================

Provides monitoring and alerting capabilities for FastAPI deployment.
Integrates with existing infrastructure alerting system.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
V2 Compliant: <300 lines
"""

import logging
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from .alerting_system import AlertingSystem, AlertLevel

logger = logging.getLogger(__name__)


class FastAPIMonitoring:
    """FastAPI-specific monitoring and alerting."""
    
    def __init__(self, alerting_system: Optional[AlertingSystem] = None):
        """
        Initialize FastAPI monitoring.
        
        Args:
            alerting_system: AlertingSystem instance (creates new if None)
        """
        self.alerting = alerting_system or AlertingSystem()
        self.error_count = 0
        self.error_threshold = 10
        self.error_window = timedelta(minutes=5)
        self.error_timestamps = []
        self.slow_response_threshold = 2.0  # seconds
    
    def _get_health_alert_level(self, consecutive_failures: int) -> AlertLevel:
        """Get alert level based on consecutive failures."""
        return (
            AlertLevel.CRITICAL if consecutive_failures >= 3
            else AlertLevel.WARNING
        )
    
    def _get_health_alert_title(self, consecutive_failures: int) -> str:
        """Get alert title based on consecutive failures."""
        return (
            "FastAPI Health Check CRITICAL" if consecutive_failures >= 3
            else "FastAPI Health Check WARNING"
        )
    
    def alert_health_check_failure(
        self,
        status_code: int,
        consecutive_failures: int
    ) -> bool:
        """Alert on health check failures."""
        level = self._get_health_alert_level(consecutive_failures)
        title = self._get_health_alert_title(consecutive_failures)
        message = (
            f"Health check returned HTTP {status_code} "
            f"({consecutive_failures} consecutive failures)"
        )
        
        metadata = {
            "status_code": status_code,
            "consecutive_failures": consecutive_failures
        }
        
        return self.alerting.send_alert(
            level=level,
            title=title,
            message=message,
            source="fastapi_health_monitor",
            metadata=metadata
        )
    
    def alert_high_error_rate(
        self,
        error_count: int,
        time_window: str = "5 minutes"
    ) -> bool:
        """
        Alert on high error rate.
        
        Args:
            error_count: Number of errors detected
            time_window: Time window description
            
        Returns:
            True if alert sent successfully
        """
        return self.alerting.send_alert(
            level=AlertLevel.WARNING,
            title="FastAPI High Error Rate",
            message=f"{error_count} errors detected in {time_window}",
            source="fastapi_error_monitor",
            metadata={
                "error_count": error_count,
                "time_window": time_window
            }
        )
    
    def alert_slow_response(
        self,
        endpoint: str,
        duration: float,
        threshold: Optional[float] = None
    ) -> bool:
        """Alert on slow response times."""
        threshold = threshold or self.slow_response_threshold
        
        if duration <= threshold:
            return False
        
        message = f"Endpoint {endpoint} took {duration:.2f}s (threshold: {threshold}s)"
        metadata = {
            "endpoint": endpoint,
            "duration": duration,
            "threshold": threshold
        }
        
        return self.alerting.send_alert(
            level=AlertLevel.WARNING,
            title="FastAPI Slow Response",
            message=message,
            source="fastapi_performance_monitor",
            metadata=metadata
        )
    
    def alert_websocket_connection_issue(
        self,
        active_connections: int,
        max_connections: int = 1000
    ) -> bool:
        """Alert on WebSocket connection issues."""
        threshold_percent = 0.9
        threshold_value = max_connections * threshold_percent
        
        if active_connections < threshold_value:
            return False
        
        message = (
            f"WebSocket connections at {active_connections}/{max_connections} "
            f"({threshold_percent*100:.0f}% threshold)"
        )
        metadata = {
            "active_connections": active_connections,
            "max_connections": max_connections
        }
        
        return self.alerting.send_alert(
            level=AlertLevel.WARNING,
            title="FastAPI WebSocket Connection Limit",
            message=message,
            source="fastapi_websocket_monitor",
            metadata=metadata
        )
    
    def record_error(self) -> None:
        """Record an error occurrence."""
        now = datetime.utcnow()
        self.error_timestamps.append(now)
        
        # Clean old timestamps outside window
        cutoff = now - self.error_window
        self.error_timestamps = [
            ts for ts in self.error_timestamps if ts > cutoff
        ]
        
        # Check if threshold exceeded
        if len(self.error_timestamps) >= self.error_threshold:
            self.alert_high_error_rate(
                len(self.error_timestamps),
                f"{self.error_window.total_seconds()/60:.0f} minutes"
            )
    
    def get_error_count(self) -> int:
        """Get current error count in time window."""
        now = datetime.utcnow()
        cutoff = now - self.error_window
        self.error_timestamps = [
            ts for ts in self.error_timestamps if ts > cutoff
        ]
        return len(self.error_timestamps)


def _handle_request_monitoring(
    monitoring: FastAPIMonitoring,
    request_path: str,
    duration: float,
    status_code: Optional[int] = None
) -> None:
    """Handle request monitoring checks."""
    monitoring.alert_slow_response(
        endpoint=request_path,
        duration=duration
    )
    
    if status_code and status_code >= 500:
        monitoring.record_error()


def create_monitoring_middleware(monitoring: FastAPIMonitoring):
    """Create FastAPI middleware for request monitoring."""
    from fastapi import Request
    from starlette.middleware.base import BaseHTTPMiddleware
    
    class MonitoringMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            start_time = time.time()
            
            try:
                response = await call_next(request)
                duration = time.time() - start_time
                
                _handle_request_monitoring(
                    monitoring,
                    str(request.url.path),
                    duration,
                    response.status_code
                )
                
                return response
            except Exception as e:
                monitoring.record_error()
                logger.error(f"Request error: {e}")
                raise
    
    return MonitoringMiddleware


def _test_health_alert(monitoring: FastAPIMonitoring, status_code: int) -> None:
    """Test health check alert."""
    monitoring.alert_health_check_failure(
        status_code=status_code,
        consecutive_failures=3
    )
    print(f"✅ Test health alert sent (status: {status_code})")


def _test_slow_response_alert(monitoring: FastAPIMonitoring, duration: float) -> None:
    """Test slow response alert."""
    monitoring.alert_slow_response(
        endpoint="/api/v1/test",
        duration=duration
    )
    print(f"✅ Test slow response alert sent (duration: {duration}s)")


def main():
    """CLI interface for FastAPI monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FastAPI Monitoring and Alerting"
    )
    parser.add_argument(
        "--test-health",
        type=int,
        help="Test health check alert (status code)"
    )
    parser.add_argument(
        "--test-slow",
        type=float,
        help="Test slow response alert (duration in seconds)"
    )
    
    args = parser.parse_args()
    monitoring = FastAPIMonitoring()
    
    if args.test_health:
        _test_health_alert(monitoring, args.test_health)
    elif args.test_slow:
        _test_slow_response_alert(monitoring, args.test_slow)
    else:
        print("FastAPI Monitoring System")
        print("Use --test-health <status_code> or --test-slow <duration> to test")


if __name__ == "__main__":
    main()

