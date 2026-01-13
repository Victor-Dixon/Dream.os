#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->
Stress Test Metrics Collector
==============================

Comprehensive metrics collection for stress testing:
- Latency metrics (p50, p95, p99)
- Throughput (messages/sec)
- Failure rates
- Queue depth tracking
- Per-agent metrics
- Per-message-type metrics
- Chaos mode metrics
- Comparison metrics (real vs mock)

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
License: MIT
"""

import json
import logging
import statistics
import time
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class StressTestMetricsCollector:
    """Comprehensive metrics collector for stress testing."""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize metrics collector."""
        self.config = config or {}
        self.logger = logger
        
        # Latency tracking (in milliseconds)
        self.latencies: list[float] = []
        self.latencies_by_agent: dict[str, list[float]] = defaultdict(list)
        self.latencies_by_type: dict[str, list[float]] = defaultdict(list)
        
        # Throughput tracking
        self.message_timestamps: deque = deque(maxlen=10000)
        self.throughput_window_size = 60  # seconds
        
        # Failure tracking
        self.total_messages = 0
        self.failed_messages = 0
        self.failures_by_agent: dict[str, int] = defaultdict(int)
        self.failures_by_type: dict[str, int] = defaultdict(int)
        self.failure_reasons: dict[str, int] = defaultdict(int)
        
        # Queue depth tracking
        self.queue_depths: list[int] = []
        self.queue_depth_timestamps: deque = deque(maxlen=10000)
        self.max_queue_depth = 0
        self.avg_queue_depth = 0
        
        # Chaos mode metrics
        self.chaos_events: list[dict[str, Any]] = []
        self.crash_recovery_times: list[float] = []
        self.spike_handling_metrics: dict[str, Any] = {
            "spikes_detected": 0,
            "spikes_handled": 0,
            "avg_spike_latency": 0.0,
        }
        
        # Comparison metrics (real vs mock)
        self.mock_delivery_times: list[float] = []
        self.real_delivery_times: list[float] = []
        self.comparison_metrics: dict[str, Any] = {}
        
        # Test metadata
        self.test_start_time: Optional[float] = None
        self.test_end_time: Optional[float] = None
        self.test_config: dict[str, Any] = {}

    def start_test(self, test_config: dict[str, Any]) -> None:
        """Start stress test and initialize tracking."""
        self.test_start_time = time.time()
        self.test_config = test_config
        self.logger.info("Stress test started - metrics collection initialized")

    def stop_test(self) -> None:
        """Stop stress test and finalize metrics."""
        self.test_end_time = time.time()
        self._calculate_final_metrics()
        self.logger.info("Stress test stopped - metrics finalized")

    def record_latency(
        self,
        latency_ms: float,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
    ) -> None:
        """Record latency for a message delivery."""
        try:
            self.latencies.append(latency_ms)
            
            if agent_id:
                self.latencies_by_agent[agent_id].append(latency_ms)
            
            if message_type:
                self.latencies_by_type[message_type].append(latency_ms)
                
        except Exception as e:
            self.logger.error(f"Error recording latency: {e}")

    def record_message_sent(
        self,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
    ) -> None:
        """Record a message being sent."""
        try:
            self.total_messages += 1
            self.message_timestamps.append(time.time())
            
        except Exception as e:
            self.logger.error(f"Error recording message sent: {e}")

    def record_message_delivered(
        self,
        latency_ms: float,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
        delivery_mode: str = "real",
    ) -> None:
        """Record successful message delivery."""
        try:
            self.record_latency(latency_ms, agent_id, message_type)
            
            if delivery_mode == "mock":
                self.mock_delivery_times.append(latency_ms)
            else:
                self.real_delivery_times.append(latency_ms)
                
        except Exception as e:
            self.logger.error(f"Error recording message delivered: {e}")

    def record_message_failed(
        self,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> None:
        """Record failed message delivery."""
        try:
            self.failed_messages += 1
            
            if agent_id:
                self.failures_by_agent[agent_id] += 1
            
            if message_type:
                self.failures_by_type[message_type] += 1
            
            if reason:
                self.failure_reasons[reason] += 1
                
        except Exception as e:
            self.logger.error(f"Error recording message failed: {e}")

    def record_queue_depth(self, depth: int) -> None:
        """Record current queue depth."""
        try:
            self.queue_depths.append(depth)
            self.queue_depth_timestamps.append(time.time())
            
            if depth > self.max_queue_depth:
                self.max_queue_depth = depth
                
        except Exception as e:
            self.logger.error(f"Error recording queue depth: {e}")

    def record_chaos_event(
        self,
        event_type: str,
        details: dict[str, Any],
        recovery_time_ms: Optional[float] = None,
    ) -> None:
        """Record a chaos engineering event."""
        try:
            event = {
                "type": event_type,
                "timestamp": datetime.now().isoformat(),
                "details": details,
            }
            self.chaos_events.append(event)
            
            if recovery_time_ms is not None:
                self.crash_recovery_times.append(recovery_time_ms)
            
            # Update spike handling metrics
            if event_type == "spike":
                self.spike_handling_metrics["spikes_detected"] += 1
                if recovery_time_ms:
                    self.spike_handling_metrics["spikes_handled"] += 1
                    
        except Exception as e:
            self.logger.error(f"Error recording chaos event: {e}")

    def _calculate_percentiles(self, values: list[float]) -> dict[str, float]:
        """Calculate p50, p95, p99 percentiles."""
        if not values:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0}
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return {
            "p50": sorted_values[int(n * 0.50)],
            "p95": sorted_values[int(n * 0.95)],
            "p99": sorted_values[int(n * 0.99)] if n > 1 else sorted_values[-1],
        }

    def _calculate_throughput(self) -> float:
        """Calculate current throughput (messages/second)."""
        if not self.message_timestamps:
            return 0.0
        
        current_time = time.time()
        window_start = current_time - self.throughput_window_size
        
        # Count messages in window
        messages_in_window = sum(
            1 for ts in self.message_timestamps
            if ts >= window_start
        )
        
        return messages_in_window / self.throughput_window_size

    def _calculate_failure_rate(self) -> float:
        """Calculate failure rate percentage."""
        if self.total_messages == 0:
            return 0.0
        return (self.failed_messages / self.total_messages) * 100

    def _calculate_avg_queue_depth(self) -> float:
        """Calculate average queue depth."""
        if not self.queue_depths:
            return 0.0
        return statistics.mean(self.queue_depths)

    def _calculate_final_metrics(self) -> None:
        """Calculate final metrics after test completion."""
        # Average queue depth
        self.avg_queue_depth = self._calculate_avg_queue_depth()
        
        # Spike handling average latency
        if self.spike_handling_metrics["spikes_handled"] > 0:
            spike_recovery_times = [
                event.get("details", {}).get("recovery_time_ms", 0)
                for event in self.chaos_events
                if event.get("type") == "spike" and event.get("details", {}).get("recovery_time_ms")
            ]
            if spike_recovery_times:
                self.spike_handling_metrics["avg_spike_latency"] = statistics.mean(spike_recovery_times)
        
        # Comparison metrics
        if self.mock_delivery_times and self.real_delivery_times:
            self.comparison_metrics = {
                "mock_avg_latency": statistics.mean(self.mock_delivery_times),
                "real_avg_latency": statistics.mean(self.real_delivery_times),
                "performance_diff_percent": (
                    (statistics.mean(self.real_delivery_times) - statistics.mean(self.mock_delivery_times))
                    / statistics.mean(self.mock_delivery_times)
                    * 100
                ),
            }

    def get_per_agent_metrics(self) -> dict[str, dict[str, Any]]:
        """Get metrics broken down by agent."""
        agent_metrics = {}
        
        for agent_id, latencies in self.latencies_by_agent.items():
            if not latencies:
                continue
                
            failures = self.failures_by_agent.get(agent_id, 0)
            total_agent_messages = len(latencies) + failures
            failure_rate = (failures / total_agent_messages * 100) if total_agent_messages > 0 else 0.0
            
            agent_metrics[agent_id] = {
                "latency_percentiles": self._calculate_percentiles(latencies),
                "avg_latency": statistics.mean(latencies),
                "total_messages": total_agent_messages,
                "successful_deliveries": len(latencies),
                "failed_deliveries": failures,
                "failure_rate_percent": failure_rate,
            }
        
        return agent_metrics

    def get_per_message_type_metrics(self) -> dict[str, dict[str, Any]]:
        """Get metrics broken down by message type."""
        type_metrics = {}
        
        for msg_type, latencies in self.latencies_by_type.items():
            if not latencies:
                continue
                
            failures = self.failures_by_type.get(msg_type, 0)
            total_type_messages = len(latencies) + failures
            failure_rate = (failures / total_type_messages * 100) if total_type_messages > 0 else 0.0
            
            type_metrics[msg_type] = {
                "latency_percentiles": self._calculate_percentiles(latencies),
                "avg_latency": statistics.mean(latencies),
                "total_messages": total_type_messages,
                "successful_deliveries": len(latencies),
                "failed_deliveries": failures,
                "failure_rate_percent": failure_rate,
            }
        
        return type_metrics

    def generate_dashboard_json(self, output_path: Optional[Path] = None) -> dict[str, Any]:
        """Generate comprehensive JSON dashboard."""
        if self.test_end_time is None:
            self._calculate_final_metrics()
        
        test_duration = (
            self.test_end_time - self.test_start_time
            if self.test_start_time and self.test_end_time
            else 0.0
        )
        
        dashboard = {
            "test_metadata": {
                "start_time": datetime.fromtimestamp(self.test_start_time).isoformat()
                if self.test_start_time else None,
                "end_time": datetime.fromtimestamp(self.test_end_time).isoformat()
                if self.test_end_time else None,
                "duration_seconds": test_duration,
                "config": self.test_config,
            },
            "overall_metrics": {
                "latency_percentiles": self._calculate_percentiles(self.latencies),
                "avg_latency_ms": statistics.mean(self.latencies) if self.latencies else 0.0,
                "throughput_msg_per_sec": self._calculate_throughput(),
                "total_messages": self.total_messages,
                "failed_messages": self.failed_messages,
                "failure_rate_percent": self._calculate_failure_rate(),
                "queue_depth": {
                    "max": self.max_queue_depth,
                    "avg": self.avg_queue_depth,
                    "current": self.queue_depths[-1] if self.queue_depths else 0,
                },
            },
            "per_agent_metrics": self.get_per_agent_metrics(),
            "per_message_type_metrics": self.get_per_message_type_metrics(),
            "chaos_mode_metrics": {
                "total_chaos_events": len(self.chaos_events),
                "crash_recovery": {
                    "count": len(self.crash_recovery_times),
                    "avg_recovery_time_ms": statistics.mean(self.crash_recovery_times)
                    if self.crash_recovery_times else 0.0,
                    "max_recovery_time_ms": max(self.crash_recovery_times)
                    if self.crash_recovery_times else 0.0,
                },
                "spike_handling": self.spike_handling_metrics,
                "chaos_events": self.chaos_events[-10:],  # Last 10 events
            },
            "comparison_metrics": self.comparison_metrics,
            "failure_analysis": {
                "failure_reasons": dict(self.failure_reasons),
                "top_failure_reasons": sorted(
                    self.failure_reasons.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5],
            },
        }
        
        # Save to file if path provided
        if output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = output_path / f"stress_test_results_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(dashboard, f, indent=2)
            self.logger.info(f"Dashboard JSON saved to {filename}")
        
        return dashboard


class StressTestAnalyzer:
    """Analyze stress test results to identify bottlenecks and failure patterns."""
    
    @staticmethod
    def identify_bottlenecks(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
        """Identify performance bottlenecks from dashboard data."""
        bottlenecks = []
        
        # Check latency bottlenecks
        overall_metrics = dashboard.get("overall_metrics", {})
        latency_p95 = overall_metrics.get("latency_percentiles", {}).get("p95", 0)
        if latency_p95 > 1000:  # p95 > 1 second
            bottlenecks.append({
                "type": "high_latency",
                "severity": "high" if latency_p95 > 5000 else "medium",
                "metric": "p95_latency",
                "value": latency_p95,
                "threshold": 1000,
                "recommendation": "Investigate message delivery pipeline for performance issues",
            })
        
        # Check throughput bottlenecks
        throughput = overall_metrics.get("throughput_msg_per_sec", 0)
        if throughput < 10:  # Less than 10 msg/sec
            bottlenecks.append({
                "type": "low_throughput",
                "severity": "high" if throughput < 1 else "medium",
                "metric": "throughput",
                "value": throughput,
                "threshold": 10,
                "recommendation": "Consider batch processing or parallel delivery",
            })
        
        # Check queue depth bottlenecks
        queue_depth = overall_metrics.get("queue_depth", {})
        max_depth = queue_depth.get("max", 0)
        if max_depth > 100:
            bottlenecks.append({
                "type": "queue_depth",
                "severity": "high" if max_depth > 500 else "medium",
                "metric": "max_queue_depth",
                "value": max_depth,
                "threshold": 100,
                "recommendation": "Increase processing capacity or optimize delivery rate",
            })
        
        # Check per-agent bottlenecks
        per_agent = dashboard.get("per_agent_metrics", {})
        for agent_id, metrics in per_agent.items():
            agent_p95 = metrics.get("latency_percentiles", {}).get("p95", 0)
            if agent_p95 > latency_p95 * 1.5:  # 50% worse than average
                bottlenecks.append({
                    "type": "agent_bottleneck",
                    "severity": "medium",
                    "agent_id": agent_id,
                    "metric": "p95_latency",
                    "value": agent_p95,
                    "recommendation": f"Investigate delivery mechanism for {agent_id}",
                })
        
        return bottlenecks
    
    @staticmethod
    def analyze_failure_patterns(dashboard: dict[str, Any]) -> dict[str, Any]:
        """Analyze failure patterns from dashboard data."""
        failure_analysis = {
            "overall_failure_rate": dashboard.get("overall_metrics", {}).get("failure_rate_percent", 0),
            "patterns": [],
        }
        
        # Analyze per-agent failure patterns
        per_agent = dashboard.get("per_agent_metrics", {})
        agent_failures = []
        for agent_id, metrics in per_agent.items():
            failure_rate = metrics.get("failure_rate_percent", 0)
            if failure_rate > 5:  # More than 5% failure rate
                agent_failures.append({
                    "agent_id": agent_id,
                    "failure_rate": failure_rate,
                    "failed_deliveries": metrics.get("failed_deliveries", 0),
                })
        
        if agent_failures:
            failure_analysis["patterns"].append({
                "type": "agent_failures",
                "agents": sorted(agent_failures, key=lambda x: x["failure_rate"], reverse=True),
                "recommendation": "Review agent delivery mechanisms and error handling",
            })
        
        # Analyze per-message-type failure patterns
        per_type = dashboard.get("per_message_type_metrics", {})
        type_failures = []
        for msg_type, metrics in per_type.items():
            failure_rate = metrics.get("failure_rate_percent", 0)
            if failure_rate > 5:
                type_failures.append({
                    "message_type": msg_type,
                    "failure_rate": failure_rate,
                    "failed_deliveries": metrics.get("failed_deliveries", 0),
                })
        
        if type_failures:
            failure_analysis["patterns"].append({
                "type": "message_type_failures",
                "message_types": sorted(type_failures, key=lambda x: x["failure_rate"], reverse=True),
                "recommendation": "Review message type handling and validation",
            })
        
        # Analyze failure reasons
        failure_reasons = dashboard.get("failure_analysis", {}).get("failure_reasons", {})
        if failure_reasons:
            failure_analysis["patterns"].append({
                "type": "failure_reasons",
                "reasons": failure_reasons,
                "recommendation": "Address top failure reasons to improve reliability",
            })
        
        return failure_analysis


# Factory function
def create_stress_test_metrics_collector(
    config: Optional[dict[str, Any]] = None
) -> StressTestMetricsCollector:
    """Create a stress test metrics collector."""
    return StressTestMetricsCollector(config)


__all__ = [
    "StressTestMetricsCollector",
    "StressTestAnalyzer",
    "create_stress_test_metrics_collector",
]

