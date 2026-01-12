#!/usr/bin/env python3
"""
Event Metrics - Phase 6 Infrastructure
=====================================

Performance monitoring and metrics collection for the event bus.

<!-- SSOT Domain: event_bus_metrics -->

Features:
- Event throughput monitoring
- Delivery success/failure tracking
- Performance metrics collection

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6 - Infrastructure Optimization
"""

import time
from typing import Dict, Any
from datetime import datetime


class EventBusMetrics:
    """
    Metrics collection and monitoring for the event bus system.
    """

    def __init__(self):
        """Initialize metrics tracking."""
        self.reset()

    def reset(self):
        """Reset all metrics to initial state."""
        self.events_published = 0
        self.events_delivered = 0
        self.events_failed = 0
        self.events_retried = 0
        self.start_time = time.time()

    def record_event_published(self):
        """Record a successfully published event."""
        self.events_published += 1

    def record_event_delivered(self):
        """Record a successfully delivered event."""
        self.events_delivered += 1

    def record_event_failed(self):
        """Record a failed event delivery."""
        self.events_failed += 1

    def record_event_retry(self):
        """Record an event retry attempt."""
        self.events_retried += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        uptime = time.time() - self.start_time
        return {
            "events_published": self.events_published,
            "events_delivered": self.events_delivered,
            "events_failed": self.events_failed,
            "events_retried": self.events_retried,
            "uptime_seconds": uptime,
            "publish_rate_per_second": self.events_published / max(uptime, 1),
            "delivery_rate_per_second": self.events_delivered / max(uptime, 1),
            "failure_rate": self.events_failed / max(self.events_published, 1),
            "timestamp": datetime.now().isoformat()
        }