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
- Subscription and processing metrics
- Circuit breaker and retry tracking

Author: Agent-5 (Business Intelligence Specialist) - Enhanced by Agent-2
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import time
import threading
from typing import Dict, Any, Optional
from datetime import datetime
from collections import defaultdict, deque


class EventBusMetrics:
    """
    Comprehensive metrics collection and monitoring for the event bus system.

    Features:
    - Event lifecycle tracking (publish → deliver → process)
    - Performance timing and throughput metrics
    - Error tracking and failure analysis
    - Subscription and processing statistics
    - Circuit breaker and retry metrics
    - Thread-safe operations for concurrent access
    """

    def __init__(self, max_history_size: int = 1000):
        """
        Initialize metrics tracking.

        Args:
            max_history_size: Maximum number of historical events to keep
        """
        self.max_history_size = max_history_size
        self._lock = threading.RLock()
        self.reset()

    def reset(self):
        """Reset all metrics to initial state."""
        with self._lock:
            self.start_time = time.time()

            # Event counters
            self.events_published = 0
            self.events_delivered = 0
            self.events_failed = 0
            self.events_retried = 0
            self.events_processed = 0
            self.events_timed_out = 0

            # Subscription metrics
            self.subscriptions_active = 0
            self.subscriptions_added = 0
            self.subscriptions_removed = 0

            # Processing metrics
            self.processing_errors = 0
            self.processing_timeouts = 0

            # Circuit breaker metrics
            self.circuit_breaker_trips = 0
            self.circuit_breaker_resets = 0

            # Dead letter queue metrics
            self.dead_letter_additions = 0
            self.dead_letter_replays = 0

            # Event type breakdown
            self.events_by_type = defaultdict(int)
            self.failures_by_type = defaultdict(int)
            self.processing_times_by_type = defaultdict(list)

            # Subscription performance
            self.subscription_processing_times = defaultdict(list)

            # Historical data (sliding windows)
            self.recent_events = deque(maxlen=self.max_history_size)
            self.recent_errors = deque(maxlen=self.max_history_size)

    def record_event_published(self, event_type: str):
        """Record a successfully published event."""
        with self._lock:
            self.events_published += 1
            self.events_by_type[event_type] += 1
            self.recent_events.append({
                'type': 'published',
                'event_type': event_type,
                'timestamp': time.time()
            })

    def record_event_delivered(self, event_type: str, processing_time: Optional[float] = None):
        """Record a successfully delivered event."""
        with self._lock:
            self.events_delivered += 1
            if processing_time is not None:
                self.processing_times_by_type[event_type].append(processing_time)

    def record_event_failed(self, event_type: str, error_type: Optional[str] = None):
        """Record a failed event delivery."""
        with self._lock:
            self.events_failed += 1
            self.failures_by_type[event_type] += 1
            self.recent_errors.append({
                'type': 'delivery_failed',
                'event_type': event_type,
                'error_type': error_type,
                'timestamp': time.time()
            })

    def record_delivery_success(self, event_type: str):
        """Record a successful delivery."""
        with self._lock:
            self.record_event_delivered(event_type)

    def record_delivery_failure(self, event_type: str):
        """Record a delivery failure."""
        with self._lock:
            self.record_event_failed(event_type, 'delivery_failure')

    def record_delivery_error(self, event_type: str, error_type: str):
        """Record a delivery error with specific error type."""
        with self._lock:
            self.record_event_failed(event_type, error_type)

    def record_event_retry(self, event_type: str):
        """Record an event retry attempt."""
        with self._lock:
            self.events_retried += 1

    def record_event_processed(self, event_type: str, subscription_id: str):
        """Record a successfully processed event."""
        with self._lock:
            self.events_processed += 1

    def record_event_processing_error(self, event_type: str, subscription_id: str):
        """Record an event processing error."""
        with self._lock:
            self.processing_errors += 1
            self.recent_errors.append({
                'type': 'processing_error',
                'event_type': event_type,
                'subscription_id': subscription_id,
                'timestamp': time.time()
            })

    def record_event_processing_timeout(self, event_type: str, subscription_id: str):
        """Record an event processing timeout."""
        with self._lock:
            self.events_timed_out += 1
            self.processing_timeouts += 1

    def record_subscription_added(self, subscription_id: str):
        """Record a subscription being added."""
        with self._lock:
            self.subscriptions_added += 1
            self.subscriptions_active += 1

    def record_subscription_removed(self, subscription_id: str):
        """Record a subscription being removed."""
        with self._lock:
            self.subscriptions_removed += 1
            self.subscriptions_active -= 1

    def record_circuit_breaker_trip(self, event_type: str):
        """Record a circuit breaker trip."""
        with self._lock:
            self.circuit_breaker_trips += 1
            self.recent_errors.append({
                'type': 'circuit_breaker_trip',
                'event_type': event_type,
                'timestamp': time.time()
            })

    def record_circuit_breaker_reset(self, event_type: str):
        """Record a circuit breaker reset."""
        with self._lock:
            self.circuit_breaker_resets += 1

    def record_dead_letter_addition(self, event_id: str, reason: str):
        """Record an event being added to dead letter queue."""
        with self._lock:
            self.dead_letter_additions += 1
            self.recent_errors.append({
                'type': 'dead_letter',
                'event_id': event_id,
                'reason': reason,
                'timestamp': time.time()
            })

    def record_dead_letter_replay(self, event_id: str):
        """Record an event being replayed from dead letter queue."""
        with self._lock:
            self.dead_letter_replays += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        with self._lock:
            uptime = time.time() - self.start_time

            # Calculate rates
            publish_rate = self.events_published / max(uptime, 1)
            delivery_rate = self.events_delivered / max(uptime, 1)
            processing_rate = self.events_processed / max(uptime, 1)

            # Calculate percentages
            delivery_success_rate = (
                self.events_delivered / max(self.events_published, 1)
            ) if self.events_published > 0 else 0

            processing_success_rate = (
                self.events_processed / max(self.events_delivered, 1)
            ) if self.events_delivered > 0 else 0

            # Calculate average processing times
            avg_processing_times = {}
            for event_type, times in self.processing_times_by_type.items():
                if times:
                    avg_processing_times[event_type] = sum(times) / len(times)

            # Calculate failure rates by type
            failure_rates_by_type = {}
            for event_type in self.events_by_type:
                total = self.events_by_type[event_type]
                failures = self.failures_by_type[event_type]
                if total > 0:
                    failure_rates_by_type[event_type] = failures / total

            return {
                # Basic counters
                "events_published": self.events_published,
                "events_delivered": self.events_delivered,
                "events_failed": self.events_failed,
                "events_processed": self.events_processed,
                "events_retried": self.events_retried,
                "events_timed_out": self.events_timed_out,

                # Subscription metrics
                "subscriptions_active": self.subscriptions_active,
                "subscriptions_added": self.subscriptions_added,
                "subscriptions_removed": self.subscriptions_removed,

                # Error tracking
                "processing_errors": self.processing_errors,
                "processing_timeouts": self.processing_timeouts,
                "circuit_breaker_trips": self.circuit_breaker_trips,
                "circuit_breaker_resets": self.circuit_breaker_resets,
                "dead_letter_additions": self.dead_letter_additions,
                "dead_letter_replays": self.dead_letter_replays,

                # Rates and percentages
                "uptime_seconds": uptime,
                "publish_rate_per_second": publish_rate,
                "delivery_rate_per_second": delivery_rate,
                "processing_rate_per_second": processing_rate,
                "delivery_success_rate": delivery_success_rate,
                "processing_success_rate": processing_success_rate,

                # Breakdowns
                "events_by_type": dict(self.events_by_type),
                "failure_rates_by_type": failure_rates_by_type,
                "average_processing_times_ms": {
                    k: v * 1000 for k, v in avg_processing_times.items()
                },

                # Recent activity (last 10 items each)
                "recent_events": list(self.recent_events)[-10:],
                "recent_errors": list(self.recent_errors)[-10:],

                "timestamp": datetime.now().isoformat()
            }

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get system health status based on metrics.

        Returns:
            Health status information
        """
        with self._lock:
            metrics = self.get_metrics()

            # Determine health based on various thresholds
            delivery_rate = metrics['delivery_success_rate']
            processing_rate = metrics['processing_success_rate']
            error_rate = metrics['events_failed'] / max(metrics['events_published'], 1)

            if delivery_rate > 0.95 and processing_rate > 0.95 and error_rate < 0.05:
                health = "healthy"
            elif delivery_rate > 0.80 and processing_rate > 0.80 and error_rate < 0.15:
                health = "warning"
            else:
                health = "unhealthy"

            return {
                "status": health,
                "delivery_success_rate": delivery_rate,
                "processing_success_rate": processing_rate,
                "error_rate": error_rate,
                "uptime_seconds": metrics['uptime_seconds'],
                "active_subscriptions": metrics['subscriptions_active'],
                "timestamp": metrics['timestamp']
            }

    def export_metrics(self, format_type: str = "json") -> str:
        """
        Export metrics in various formats.

        Args:
            format_type: Export format ("json", "prometheus", etc.)

        Returns:
            Formatted metrics string
        """
        metrics = self.get_metrics()

        if format_type == "json":
            import json
            return json.dumps(metrics, indent=2, default=str)
        elif format_type == "prometheus":
            # Basic Prometheus format
            lines = []
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    lines.append(f"eventbus_{key} {value}")
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (int, float)):
                            lines.append(f"eventbus_{key}_{sub_key} {sub_value}")
            return "\n".join(lines)
        else:
            return str(metrics)