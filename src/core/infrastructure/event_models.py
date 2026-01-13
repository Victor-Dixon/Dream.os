#!/usr/bin/env python3
"""
Event Models - Phase 6 Infrastructure
====================================

Data models for the event-driven communication system.

<!-- SSOT Domain: event_bus_models -->

Features:
- Event data structures
- Event subscription management
- Event creation utilities

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6 - Infrastructure Optimization
"""

import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Event:
    """
    Event data structure for the event bus system.

    Represents a single event in the system with all necessary metadata.
    """
    event_type: str
    source_service: str
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    event_id: Optional[str] = None
    priority: str = "normal"
    ttl: Optional[int] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())
        if self.correlation_id is None:
            self.correlation_id = self.event_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        data = asdict(self)
        # Convert datetime to ISO format string
        if isinstance(data['timestamp'], datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create event from dictionary."""
        # Convert ISO string back to datetime
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class EventSubscription:
    """
    Event subscription configuration.

    Defines how and when events are delivered to subscribers.
    """
    subscription_id: str
    event_patterns: list
    callback: Optional[callable] = None
    queue_name: Optional[str] = None
    max_retries: int = 3
    retry_delay: int = 60
    enabled: bool = True
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def matches_event(self, event: Event) -> bool:
        """
        Check if this subscription matches the given event.

        Args:
            event: Event to check against subscription patterns

        Returns:
            True if event matches any pattern
        """
        for pattern in self.event_patterns:
            if pattern == "*" or pattern == event.event_type:
                return True
            # Simple wildcard matching
            if pattern.endswith("*") and event.event_type.startswith(pattern[:-1]):
                return True
        return False


def create_event(event_type: str,
                source_service: str,
                data: Dict[str, Any],
                correlation_id: Optional[str] = None,
                priority: str = "normal",
                ttl: Optional[int] = None) -> Event:
    """
    Factory function to create standardized events.

    Args:
        event_type: Type of event (e.g., "user_created", "order_processed")
        source_service: Service that generated the event
        data: Event payload data
        correlation_id: Optional correlation ID for tracking
        priority: Event priority ("low", "normal", "high", "urgent")
        ttl: Time-to-live in seconds

    Returns:
        Configured Event instance
    """
    return Event(
        event_type=event_type,
        source_service=source_service,
        data=data,
        correlation_id=correlation_id,
        priority=priority,
        ttl=ttl
    )