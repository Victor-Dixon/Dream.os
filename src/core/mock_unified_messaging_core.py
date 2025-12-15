#!/usr/bin/env python3
"""
Mock Unified Messaging Core - Stress Testing Module

<!-- SSOT Domain: infrastructure -->

===================================================

Simulates message delivery for stress testing with configurable latency,
success rate, and chaos mode (random failures, latency spikes).

V2 Compliance: <400 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

from __future__ import annotations

import logging
import random
import time
import threading
from datetime import datetime
from typing import Any, Optional, Dict
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class MockDeliveryConfig:
    """Configuration for mock message delivery."""
    min_latency_ms: int = 1
    max_latency_ms: int = 10
    success_rate: float = 0.95  # 95% success rate
    chaos_mode: bool = False
    chaos_crash_rate: float = 0.01  # 1% chance of crash
    chaos_latency_spike_rate: float = 0.05  # 5% chance of latency spike
    chaos_max_spike_ms: int = 500  # Max spike latency in ms
    enabled: bool = True


@dataclass
class MockDeliveryResult:
    """Result of mock message delivery."""
    success: bool
    latency_ms: float
    timestamp: datetime
    error_message: Optional[str] = None
    chaos_event: Optional[str] = None


class MockUnifiedMessagingCore:
    """
    Mock messaging core for stress testing.
    
    Simulates message delivery with:
    - Configurable latency (1-10ms default)
    - Configurable success rate (95% default)
    - Chaos mode (random crashes, latency spikes)
    - Thread-safe operation
    """
    
    def __init__(self, config: Optional[MockDeliveryConfig] = None):
        """Initialize mock messaging core.
        
        Args:
            config: Mock delivery configuration (uses defaults if None)
        """
        self.config = config or MockDeliveryConfig()
        self.logger = logging.getLogger(__name__)
        self._lock = threading.Lock()
        self._delivery_stats: Dict[str, Any] = {
            "total_deliveries": 0,
            "successful_deliveries": 0,
            "failed_deliveries": 0,
            "total_latency_ms": 0.0,
            "chaos_events": [],
            "start_time": datetime.now(),
        }
        
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: Any = None,
        priority: Any = None,
        tags: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Simulate sending a message.
        
        Args:
            content: Message content
            sender: Sender identifier
            recipient: Recipient identifier
            message_type: Message type (ignored in mock)
            priority: Message priority (ignored in mock)
            tags: Message tags (ignored in mock)
            metadata: Additional metadata (ignored in mock)
            
        Returns:
            True if delivery successful, False otherwise
        """
        if not self.config.enabled:
            return False
            
        start_time = time.time()
        
        try:
            # Chaos mode: Random crash simulation
            if self.config.chaos_mode:
                if random.random() < self.config.chaos_crash_rate:
                    latency_ms = (time.time() - start_time) * 1000
                    self._record_delivery(False, latency_ms, "CHAOS_CRASH")
                    return False
            
            # Calculate base latency (1-10ms)
            base_latency_ms = random.uniform(
                self.config.min_latency_ms,
                self.config.max_latency_ms
            )
            
            # Chaos mode: Random latency spike
            chaos_spike = 0.0
            chaos_event = None
            if self.config.chaos_mode:
                if random.random() < self.config.chaos_latency_spike_rate:
                    chaos_spike = random.uniform(0, self.config.chaos_max_spike_ms)
                    base_latency_ms += chaos_spike
                    chaos_event = f"LATENCY_SPIKE_{chaos_spike:.1f}ms"
            
            # Simulate latency
            time.sleep(base_latency_ms / 1000.0)
            
            # Determine success/failure based on success rate
            is_success = random.random() < self.config.success_rate
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Record delivery
            self._record_delivery(
                is_success,
                latency_ms,
                chaos_event=chaos_event
            )
            
            if is_success:
                self.logger.debug(
                    f"✅ Mock delivered: {sender} → {recipient} "
                    f"({latency_ms:.2f}ms)"
                )
            else:
                self.logger.debug(
                    f"❌ Mock failed: {sender} → {recipient} "
                    f"({latency_ms:.2f}ms)"
                )
            
            return is_success
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.logger.error(f"Mock delivery exception: {e}")
            self._record_delivery(False, latency_ms, str(e))
            return False
    
    def send_message_object(self, message: Any) -> bool:
        """Send a UnifiedMessage object (compatibility method).
        
        Args:
            message: UnifiedMessage object
            
        Returns:
            True if delivery successful, False otherwise
        """
        # Extract fields from message object
        content = getattr(message, 'content', '') or getattr(message, 'message', '')
        sender = getattr(message, 'sender', 'SYSTEM') or getattr(message, 'from', 'SYSTEM')
        recipient = getattr(message, 'recipient', '') or getattr(message, 'to', '')
        
        return self.send_message(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=getattr(message, 'message_type', None),
            priority=getattr(message, 'priority', None),
            tags=getattr(message, 'tags', None),
            metadata=getattr(message, 'metadata', None),
        )
    
    def _record_delivery(
        self,
        success: bool,
        latency_ms: float,
        error: Optional[str] = None,
        chaos_event: Optional[str] = None
    ) -> None:
        """Record delivery statistics.
        
        Args:
            success: Whether delivery was successful
            latency_ms: Delivery latency in milliseconds
            error: Error message if failed
            chaos_event: Chaos event type if occurred
        """
        with self._lock:
            self._delivery_stats["total_deliveries"] += 1
            self._delivery_stats["total_latency_ms"] += latency_ms
            
            if success:
                self._delivery_stats["successful_deliveries"] += 1
            else:
                self._delivery_stats["failed_deliveries"] += 1
                
            if chaos_event:
                self._delivery_stats["chaos_events"].append({
                    "event": chaos_event,
                    "timestamp": datetime.now().isoformat(),
                    "latency_ms": latency_ms,
                })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get delivery statistics.
        
        Returns:
            Dictionary with delivery statistics
        """
        with self._lock:
            total = self._delivery_stats["total_deliveries"]
            successful = self._delivery_stats["successful_deliveries"]
            
            stats = {
                "total_deliveries": total,
                "successful_deliveries": successful,
                "failed_deliveries": self._delivery_stats["failed_deliveries"],
                "success_rate": (successful / total * 100) if total > 0 else 0.0,
                "average_latency_ms": (
                    self._delivery_stats["total_latency_ms"] / total
                    if total > 0 else 0.0
                ),
                "chaos_events_count": len(self._delivery_stats["chaos_events"]),
                "chaos_events": self._delivery_stats["chaos_events"][-10:],  # Last 10
                "uptime_seconds": (
                    datetime.now() - self._delivery_stats["start_time"]
                ).total_seconds(),
            }
            
            return stats
    
    def reset_stats(self) -> None:
        """Reset delivery statistics."""
        with self._lock:
            self._delivery_stats = {
                "total_deliveries": 0,
                "successful_deliveries": 0,
                "failed_deliveries": 0,
                "total_latency_ms": 0.0,
                "chaos_events": [],
                "start_time": datetime.now(),
            }
    
    def configure(
        self,
        min_latency_ms: Optional[int] = None,
        max_latency_ms: Optional[int] = None,
        success_rate: Optional[float] = None,
        chaos_mode: Optional[bool] = None,
        chaos_crash_rate: Optional[float] = None,
        chaos_latency_spike_rate: Optional[float] = None,
    ) -> None:
        """Update configuration.
        
        Args:
            min_latency_ms: Minimum latency in milliseconds
            max_latency_ms: Maximum latency in milliseconds
            success_rate: Success rate (0.0-1.0)
            chaos_mode: Enable chaos mode
            chaos_crash_rate: Crash rate in chaos mode (0.0-1.0)
            chaos_latency_spike_rate: Latency spike rate (0.0-1.0)
        """
        if min_latency_ms is not None:
            self.config.min_latency_ms = min_latency_ms
        if max_latency_ms is not None:
            self.config.max_latency_ms = max_latency_ms
        if success_rate is not None:
            self.config.success_rate = max(0.0, min(1.0, success_rate))
        if chaos_mode is not None:
            self.config.chaos_mode = chaos_mode
        if chaos_crash_rate is not None:
            self.config.chaos_crash_rate = max(0.0, min(1.0, chaos_crash_rate))
        if chaos_latency_spike_rate is not None:
            self.config.chaos_latency_spike_rate = max(0.0, min(1.0, chaos_latency_spike_rate))


# Module-level convenience function
_mock_core_instance: Optional[MockUnifiedMessagingCore] = None


def get_mock_messaging_core(
    config: Optional[MockDeliveryConfig] = None
) -> MockUnifiedMessagingCore:
    """Get or create global mock messaging core instance.
    
    Args:
        config: Configuration (only used on first call)
        
    Returns:
        Mock messaging core instance
    """
    global _mock_core_instance
    
    if _mock_core_instance is None:
        _mock_core_instance = MockUnifiedMessagingCore(config)
    
    return _mock_core_instance

