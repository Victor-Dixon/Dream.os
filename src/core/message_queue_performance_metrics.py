#!/usr/bin/env python3
"""
Message Queue Performance Metrics
==================================

<!-- SSOT Domain: communication -->

Performance metrics collection and baseline tracking for message queue system.
Tracks delivery times, success rates, throughput, and provides before/after comparison.

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-13
V2 Compliant: Yes
"""

import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DeliveryMetric:
    """Single message delivery metric."""
    queue_id: str
    recipient: str
    delivery_method: str  # 'pyautogui' or 'inbox'
    success: bool
    delivery_time_seconds: float
    attempt_number: int
    timestamp: str
    content_length: int
    retry_delay: Optional[float] = None


@dataclass
class PerformanceBaseline:
    """Baseline performance metrics for comparison."""
    timestamp: str
    total_messages: int
    successful_deliveries: int
    failed_deliveries: int
    success_rate: float
    avg_delivery_time_seconds: float
    median_delivery_time_seconds: float
    p95_delivery_time_seconds: float
    p99_delivery_time_seconds: float
    messages_per_second: float
    pyautogui_success_rate: float
    inbox_success_rate: float
    avg_retry_count: float
    delivery_method_distribution: Dict[str, int]


class MessageQueuePerformanceMetrics:
    """
    Collects and analyzes performance metrics for message queue system.
    
    Tracks:
    - Delivery times per message
    - Success/failure rates
    - Queue processing throughput
    - Delivery method performance
    - Retry statistics
    """
    
    def __init__(self, metrics_file: Optional[Path] = None, baseline_file: Optional[Path] = None):
        """Initialize performance metrics collector.
        
        Args:
            metrics_file: Path to store historical metrics (default: message_queue/metrics.json)
            baseline_file: Path to store baseline metrics (default: message_queue/baseline.json)
        """
        project_root = Path(__file__).resolve().parent.parent.parent
        queue_dir = project_root / "message_queue"
        queue_dir.mkdir(exist_ok=True)
        
        self.metrics_file = metrics_file or (queue_dir / "metrics.json")
        self.baseline_file = baseline_file or (queue_dir / "baseline.json")
        
        # In-memory metrics storage
        self._delivery_metrics: List[DeliveryMetric] = []
        self._session_start_time: Optional[float] = None
        self._session_message_count: int = 0
        
    def start_delivery_tracking(self, queue_id: str) -> float:
        """Start tracking delivery time for a message.
        
        Args:
            queue_id: Unique queue entry ID
            
        Returns:
            Start timestamp for later use with end_delivery_tracking
        """
        return time.time()
    
    def end_delivery_tracking(
        self,
        queue_id: str,
        recipient: str,
        delivery_method: str,
        success: bool,
        start_time: float,
        attempt_number: int = 1,
        content_length: int = 0,
        retry_delay: Optional[float] = None
    ) -> None:
        """End tracking and record delivery metric.
        
        Args:
            queue_id: Unique queue entry ID
            recipient: Message recipient
            delivery_method: 'pyautogui' or 'inbox'
            success: Whether delivery succeeded
            start_time: Start timestamp from start_delivery_tracking
            attempt_number: Delivery attempt number (1, 2, 3, etc.)
            content_length: Message content length in characters
            retry_delay: Delay before retry (if applicable)
        """
        delivery_time = time.time() - start_time
        
        metric = DeliveryMetric(
            queue_id=queue_id,
            recipient=recipient,
            delivery_method=delivery_method,
            success=success,
            delivery_time_seconds=delivery_time,
            attempt_number=attempt_number,
            timestamp=datetime.now().isoformat(),
            content_length=content_length,
            retry_delay=retry_delay
        )
        
        self._delivery_metrics.append(metric)
        self._session_message_count += 1
        
        # Persist metrics periodically (every 10 messages)
        if len(self._delivery_metrics) % 10 == 0:
            self._persist_metrics()
    
    def start_session(self) -> None:
        """Start a new metrics collection session."""
        self._session_start_time = time.time()
        self._session_message_count = 0
        logger.info("📊 Performance metrics session started")
    
    def end_session(self) -> Dict[str, Any]:
        """End current session and return session summary.
        
        Returns:
            Dictionary with session summary metrics
        """
        if self._session_start_time is None:
            return {}
        
        session_duration = time.time() - self._session_start_time
        messages_per_second = (
            self._session_message_count / session_duration
            if session_duration > 0 else 0.0
        )
        
        summary = {
            "session_duration_seconds": session_duration,
            "messages_processed": self._session_message_count,
            "messages_per_second": messages_per_second,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(
            f"📊 Performance metrics session ended: "
            f"{self._session_message_count} messages in {session_duration:.2f}s "
            f"({messages_per_second:.2f} msg/s)"
        )
        
        return summary
    
    def calculate_baseline(self, sample_size: Optional[int] = None) -> PerformanceBaseline:
        """Calculate baseline performance metrics from collected data.
        
        Args:
            sample_size: Number of recent metrics to use (None = all)
            
        Returns:
            PerformanceBaseline with calculated metrics
        """
        metrics = self._delivery_metrics
        if sample_size:
            metrics = metrics[-sample_size:]
        
        if not metrics:
            logger.warning("No metrics available for baseline calculation")
            return self._get_empty_baseline()
        
        total = len(metrics)
        successful = sum(1 for m in metrics if m.success)
        failed = total - successful
        success_rate = successful / total if total > 0 else 0.0
        
        # Delivery time statistics
        delivery_times = [m.delivery_time_seconds for m in metrics if m.success]
        if delivery_times:
            delivery_times_sorted = sorted(delivery_times)
            avg_time = sum(delivery_times) / len(delivery_times)
            median_time = delivery_times_sorted[len(delivery_times_sorted) // 2]
            p95_idx = int(len(delivery_times_sorted) * 0.95)
            p99_idx = int(len(delivery_times_sorted) * 0.99)
            p95_time = delivery_times_sorted[min(p95_idx, len(delivery_times_sorted) - 1)]
            p99_time = delivery_times_sorted[min(p99_idx, len(delivery_times_sorted) - 1)]
        else:
            avg_time = median_time = p95_time = p99_time = 0.0
        
        # Throughput calculation
        if metrics:
            first_time = datetime.fromisoformat(metrics[0].timestamp)
            last_time = datetime.fromisoformat(metrics[-1].timestamp)
            duration = (last_time - first_time).total_seconds()
            messages_per_second = total / duration if duration > 0 else 0.0
        else:
            messages_per_second = 0.0
        
        # Delivery method statistics
        pyautogui_metrics = [m for m in metrics if m.delivery_method == 'pyautogui']
        inbox_metrics = [m for m in metrics if m.delivery_method == 'inbox']
        
        pyautogui_success_rate = (
            sum(1 for m in pyautogui_metrics if m.success) / len(pyautogui_metrics)
            if pyautogui_metrics else 0.0
        )
        inbox_success_rate = (
            sum(1 for m in inbox_metrics if m.success) / len(inbox_metrics)
            if inbox_metrics else 0.0
        )
        
        # Retry statistics
        avg_retry_count = sum(m.attempt_number for m in metrics) / total if total > 0 else 0.0
        
        # Delivery method distribution
        method_dist = defaultdict(int)
        for m in metrics:
            method_dist[m.delivery_method] += 1
        
        baseline = PerformanceBaseline(
            timestamp=datetime.now().isoformat(),
            total_messages=total,
            successful_deliveries=successful,
            failed_deliveries=failed,
            success_rate=success_rate,
            avg_delivery_time_seconds=avg_time,
            median_delivery_time_seconds=median_time,
            p95_delivery_time_seconds=p95_time,
            p99_delivery_time_seconds=p99_time,
            messages_per_second=messages_per_second,
            pyautogui_success_rate=pyautogui_success_rate,
            inbox_success_rate=inbox_success_rate,
            avg_retry_count=avg_retry_count,
            delivery_method_distribution=dict(method_dist)
        )
        
        return baseline
    
    def save_baseline(self, baseline: Optional[PerformanceBaseline] = None) -> None:
        """Save baseline metrics to file.
        
        Args:
            baseline: Baseline to save (None = calculate from current metrics)
        """
        if baseline is None:
            baseline = self.calculate_baseline()
        
        try:
            with open(self.baseline_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(baseline), f, indent=2)
            logger.info(f"✅ Baseline metrics saved to {self.baseline_file}")
        except Exception as e:
            logger.error(f"Failed to save baseline: {e}", exc_info=True)
    
    def load_baseline(self) -> Optional[PerformanceBaseline]:
        """Load baseline metrics from file.
        
        Returns:
            PerformanceBaseline if file exists, None otherwise
        """
        if not self.baseline_file.exists():
            logger.debug(f"Baseline file not found: {self.baseline_file}")
            return None
        
        try:
            with open(self.baseline_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return PerformanceBaseline(**data)
        except Exception as e:
            logger.error(f"Failed to load baseline: {e}", exc_info=True)
            return None
    
    def compare_to_baseline(
        self,
        current_baseline: Optional[PerformanceBaseline] = None
    ) -> Dict[str, Any]:
        """Compare current metrics to saved baseline.
        
        Args:
            current_baseline: Current baseline to compare (None = calculate from current metrics)
            
        Returns:
            Dictionary with comparison results
        """
        saved_baseline = self.load_baseline()
        if saved_baseline is None:
            logger.warning("No saved baseline found for comparison")
            return {"error": "No baseline available for comparison"}
        
        if current_baseline is None:
            current_baseline = self.calculate_baseline()
        
        comparison = {
            "baseline_timestamp": saved_baseline.timestamp,
            "current_timestamp": current_baseline.timestamp,
            "success_rate": {
                "baseline": saved_baseline.success_rate,
                "current": current_baseline.success_rate,
                "delta": current_baseline.success_rate - saved_baseline.success_rate,
                "delta_percent": (
                    (current_baseline.success_rate - saved_baseline.success_rate) / saved_baseline.success_rate * 100
                    if saved_baseline.success_rate > 0 else 0.0
                )
            },
            "avg_delivery_time": {
                "baseline": saved_baseline.avg_delivery_time_seconds,
                "current": current_baseline.avg_delivery_time_seconds,
                "delta": current_baseline.avg_delivery_time_seconds - saved_baseline.avg_delivery_time_seconds,
                "delta_percent": (
                    (current_baseline.avg_delivery_time_seconds - saved_baseline.avg_delivery_time_seconds) / saved_baseline.avg_delivery_time_seconds * 100
                    if saved_baseline.avg_delivery_time_seconds > 0 else 0.0
                )
            },
            "throughput": {
                "baseline": saved_baseline.messages_per_second,
                "current": current_baseline.messages_per_second,
                "delta": current_baseline.messages_per_second - saved_baseline.messages_per_second,
                "delta_percent": (
                    (current_baseline.messages_per_second - saved_baseline.messages_per_second) / saved_baseline.messages_per_second * 100
                    if saved_baseline.messages_per_second > 0 else 0.0
                )
            }
        }
        
        return comparison
    
    def get_current_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of current metrics.
        
        Returns:
            Dictionary with current metrics summary
        """
        if not self._delivery_metrics:
            return {"message": "No metrics collected yet"}
        
        baseline = self.calculate_baseline()
        return {
            "total_messages": baseline.total_messages,
            "success_rate": baseline.success_rate,
            "avg_delivery_time_seconds": baseline.avg_delivery_time_seconds,
            "messages_per_second": baseline.messages_per_second,
            "timestamp": datetime.now().isoformat()
        }
    
    def _persist_metrics(self) -> None:
        """Persist metrics to file."""
        try:
            # Load existing metrics
            existing = []
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            
            # Append new metrics
            new_metrics = [asdict(m) for m in self._delivery_metrics[-10:]]
            existing.extend(new_metrics)
            
            # Keep only last 1000 metrics to prevent file bloat
            if len(existing) > 1000:
                existing = existing[-1000:]
            
            # Save
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            logger.debug(f"Failed to persist metrics: {e}")
    
    def _get_empty_baseline(self) -> PerformanceBaseline:
        """Get empty baseline with zero values."""
        return PerformanceBaseline(
            timestamp=datetime.now().isoformat(),
            total_messages=0,
            successful_deliveries=0,
            failed_deliveries=0,
            success_rate=0.0,
            avg_delivery_time_seconds=0.0,
            median_delivery_time_seconds=0.0,
            p95_delivery_time_seconds=0.0,
            p99_delivery_time_seconds=0.0,
            messages_per_second=0.0,
            pyautogui_success_rate=0.0,
            inbox_success_rate=0.0,
            avg_retry_count=0.0,
            delivery_method_distribution={}
        )





