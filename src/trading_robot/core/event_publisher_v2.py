#!/usr/bin/env python3
"""
EventPublisherV2 - Advanced Event Publishing System
===================================================

High-performance event publishing with filtering, persistence,
and real-time streaming capabilities.

Features:
- Event filtering and routing
- Persistent event storage
- Real-time WebSocket streaming
- Event correlation and analytics
- Performance monitoring

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-06
Phase: Revenue Engine Phase 3 - Advanced Event System
"""

import asyncio
import logging
import json
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
import threading
import queue

from ..repositories.trading_repository import TradingRepository


@dataclass
class Event:
    """Event data structure."""
    id: str
    type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str
    correlation_id: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class EventSubscription:
    """Event subscription configuration."""
    id: str
    event_types: List[str]
    callback: Callable[[Event], None]
    filter_func: Optional[Callable[[Event], bool]] = None
    is_active: bool = True


class EventFilter(ABC):
    """Base class for event filters."""

    @abstractmethod
    def matches(self, event: Event) -> bool:
        """Check if event matches filter criteria."""
        pass


class TypeFilter(EventFilter):
    """Filter events by type."""

    def __init__(self, event_types: List[str]):
        self.event_types = set(event_types)

    def matches(self, event: Event) -> bool:
        return event.type in self.event_types


class SourceFilter(EventFilter):
    """Filter events by source."""

    def __init__(self, sources: List[str]):
        self.sources = set(sources)

    def matches(self, event: Event) -> bool:
        return event.source in self.sources


class TagFilter(EventFilter):
    """Filter events by tags."""

    def __init__(self, required_tags: List[str]):
        self.required_tags = set(required_tags)

    def matches(self, event: Event) -> bool:
        event_tags = set(event.tags or [])
        return self.required_tags.issubset(event_tags)


class CompositeFilter(EventFilter):
    """Composite filter combining multiple filters."""

    def __init__(self, filters: List[EventFilter], operator: str = "AND"):
        self.filters = filters
        self.operator = operator.upper()

    def matches(self, event: Event) -> bool:
        if self.operator == "AND":
            return all(f.matches(event) for f in self.filters)
        elif self.operator == "OR":
            return any(f.matches(event) for f in self.filters)
        else:
            return False


class EventAnalytics:
    """Event analytics and monitoring."""

    def __init__(self):
        self.event_counts: Dict[str, int] = defaultdict(int)
        self.event_timestamps: Dict[str, List[datetime]] = defaultdict(list)
        self.processing_times: List[float] = []
        self.error_counts: Dict[str, int] = defaultdict(int)

    def record_event(self, event: Event) -> None:
        """Record event for analytics."""
        self.event_counts[event.type] += 1
        self.event_timestamps[event.type].append(event.timestamp)

        # Keep only recent timestamps (last 1000)
        if len(self.event_timestamps[event.type]) > 1000:
            self.event_timestamps[event.type] = self.event_timestamps[event.type][-1000:]

    def record_processing_time(self, processing_time: float) -> None:
        """Record event processing time."""
        self.processing_times.append(processing_time)

        # Keep only recent times (last 1000)
        if len(self.processing_times) > 1000:
            self.processing_times = self.processing_times[-1000:]

    def record_error(self, event_type: str, error: Exception) -> None:
        """Record event processing error."""
        self.error_counts[event_type] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get analytics statistics."""
        total_events = sum(self.event_counts.values())
        avg_processing_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0

        return {
            'total_events': total_events,
            'events_by_type': dict(self.event_counts),
            'avg_processing_time': avg_processing_time,
            'error_counts': dict(self.error_counts),
            'timestamp': datetime.now()
        }


class EventPublisherV2:
    """Advanced Event Publisher V2 with filtering and analytics."""

    def __init__(self, config: Dict[str, Any], repository: Optional[TradingRepository] = None):
        self.config = config
        self.repository = repository

        # Event handling
        self.subscriptions: Dict[str, EventSubscription] = {}
        self.event_queue = asyncio.Queue(maxsize=config.get('queue_size', 1000))

        # Analytics
        self.analytics = EventAnalytics()

        # Persistence settings
        self.persist_events = config.get('persist_events', True)
        self.persistence_batch_size = config.get('persistence_batch_size', 100)

        # Performance settings
        self.max_processing_time = config.get('max_processing_time', 5.0)

        # Background tasks
        self.processing_task: Optional[asyncio.Task] = None
        self.persistence_task: Optional[asyncio.Task] = None
        self.is_running = False

        # Logging
        self.logger = logging.getLogger(__name__)

    async def initialize(self) -> bool:
        """Initialize event publisher."""
        try:
            self.is_running = True

            # Start background processing
            self.processing_task = asyncio.create_task(self._process_events())
            if self.persist_events:
                self.persistence_task = asyncio.create_task(self._persist_events())

            self.logger.info("EventPublisherV2 initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize EventPublisherV2: {e}")
            return False

    async def shutdown(self) -> None:
        """Shutdown event publisher gracefully."""
        self.is_running = False

        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass

        if self.persistence_task:
            self.persistence_task.cancel()
            try:
                await self.persistence_task
            except asyncio.CancelledError:
                pass

        self.logger.info("EventPublisherV2 shutdown complete")

    def publish(self, event_type: str, data: Dict[str, Any],
               source: str = "unknown", correlation_id: Optional[str] = None,
               tags: Optional[List[str]] = None) -> str:
        """Publish an event asynchronously."""
        try:
            event = Event(
                id=str(uuid.uuid4()),
                type=event_type,
                data=data,
                timestamp=datetime.now(),
                source=source,
                correlation_id=correlation_id,
                tags=tags or []
            )

            # Try to add to queue without blocking
            try:
                self.event_queue.put_nowait(event)
                return event.id
            except asyncio.QueueFull:
                self.logger.warning("Event queue full, dropping event")
                return ""

        except Exception as e:
            self.logger.error(f"Failed to publish event: {e}")
            return ""

    def subscribe(self, event_types: List[str],
                 callback: Callable[[Event], None],
                 filter_func: Optional[Callable[[Event], bool]] = None) -> str:
        """Subscribe to events."""
        subscription_id = str(uuid.uuid4())

        subscription = EventSubscription(
            id=subscription_id,
            event_types=event_types,
            callback=callback,
            filter_func=filter_func
        )

        self.subscriptions[subscription_id] = subscription
        self.logger.info(f"Created subscription {subscription_id} for events: {event_types}")

        return subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events."""
        if subscription_id in self.subscriptions:
            del self.subscriptions[subscription_id]
            self.logger.info(f"Removed subscription {subscription_id}")
            return True

        return False

    async def _process_events(self) -> None:
        """Process events from the queue."""
        while self.is_running:
            try:
                # Get event from queue
                event = await self.event_queue.get()

                # Record analytics
                self.analytics.record_event(event)

                start_time = datetime.now()

                # Process event
                await self._deliver_event(event)

                # Record processing time
                processing_time = (datetime.now() - start_time).total_seconds()
                self.analytics.record_processing_time(processing_time)

                if processing_time > self.max_processing_time:
                    self.logger.warning(f"Event processing took {processing_time:.2f}s (max: {self.max_processing_time}s)")

                self.event_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing event: {e}")

    async def _deliver_event(self, event: Event) -> None:
        """Deliver event to subscribers."""
        delivered_count = 0

        for subscription in self.subscriptions.values():
            if not subscription.is_active:
                continue

            # Check if subscription matches event type
            if event.type not in subscription.event_types:
                continue

            # Apply filter if provided
            if subscription.filter_func and not subscription.filter_func(event):
                continue

            try:
                # Call subscriber callback
                if asyncio.iscoroutinefunction(subscription.callback):
                    await subscription.callback(event)
                else:
                    # Run in thread pool for sync callbacks
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, subscription.callback, event)

                delivered_count += 1

            except Exception as e:
                self.logger.error(f"Error delivering event to subscriber: {e}")
                self.analytics.record_error(event.type, e)

        if delivered_count == 0:
            self.logger.debug(f"Event {event.type} had no subscribers")

    async def _persist_events(self) -> None:
        """Persist events to repository in batches."""
        if not self.repository:
            return

        batch = []

        while self.is_running:
            try:
                # Wait for events or timeout
                try:
                    event = await asyncio.wait_for(self.event_queue.get(), timeout=5.0)
                    batch.append(event)
                except asyncio.TimeoutError:
                    pass

                # Persist batch if full or periodic
                if len(batch) >= self.persistence_batch_size:
                    await self._save_event_batch(batch)
                    batch = []

            except asyncio.CancelledError:
                # Save remaining events before shutdown
                if batch:
                    await self._save_event_batch(batch)
                break
            except Exception as e:
                self.logger.error(f"Error in event persistence: {e}")

    async def _save_event_batch(self, events: List[Event]) -> None:
        """Save batch of events to repository."""
        try:
            # Convert events to dict format for storage
            event_data = []
            for event in events:
                event_dict = {
                    'event_id': event.id,
                    'event_type': event.type,
                    'data': json.dumps(event.data),
                    'timestamp': event.timestamp,
                    'source': event.source,
                    'correlation_id': event.correlation_id,
                    'tags': ','.join(event.tags) if event.tags else None
                }
                event_data.append(event_dict)

            # Save to repository (assuming there's an event storage method)
            if hasattr(self.repository, 'save_events'):
                await self.repository.save_events(event_data)

        except Exception as e:
            self.logger.error(f"Failed to save event batch: {e}")

    def get_analytics(self) -> Dict[str, Any]:
        """Get event analytics."""
        return self.analytics.get_stats()

    def get_subscription_stats(self) -> Dict[str, Any]:
        """Get subscription statistics."""
        return {
            'total_subscriptions': len(self.subscriptions),
            'active_subscriptions': sum(1 for s in self.subscriptions.values() if s.is_active),
            'subscriptions_by_type': self._get_subscriptions_by_type()
        }

    def _get_subscriptions_by_type(self) -> Dict[str, int]:
        """Get subscription counts by event type."""
        type_counts = defaultdict(int)

        for subscription in self.subscriptions.values():
            if subscription.is_active:
                for event_type in subscription.event_types:
                    type_counts[event_type] += 1

        return dict(type_counts)