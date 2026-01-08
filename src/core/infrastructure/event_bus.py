#!/usr/bin/env python3
"""
Event Bus Implementation - Phase 6 Infrastructure
===============================================

Asynchronous event-driven communication system for microservices architecture.

<!-- SSOT Domain: event_bus -->

Navigation References:
├── Related Services → src/services/ai_context_engine.py
├── WebSocket Integration → src/services/ai_context_websocket.py
├── FastAPI Integration → src/web/fastapi_app.py
├── Documentation → docs/PHASE6_INFRASTRUCTURE_OPTIMIZATION_ROADMAP.md

Features:
- Redis Pub/Sub based event distribution
- Async event publishing and subscription
- Event persistence and replay capabilities
- Dead letter queue for failed deliveries
- Event filtering and routing
- Performance monitoring and metrics

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6 - Infrastructure Optimization
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Callable, Optional, Set, Union
from datetime import datetime, timedelta
import redis.asyncio as redis
from contextlib import asynccontextmanager

# Import extracted modules
from .event_models import Event, EventSubscription, create_event
from .event_metrics import EventBusMetrics
from .event_publisher import EventPublisher
from .event_subscriber import EventSubscriber

logger = logging.getLogger(__name__)

    def record_event_delivered(self, event_type: str):
        """Record successful event delivery."""
        self.events_delivered += 1

    def record_event_failed(self, event_type: str, error: Exception):
        """Record event delivery failure."""
        self.events_failed += 1
        error_type = type(error).__name__
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        self.error_counts[error_type] += 1

    def record_event_retried(self, event_type: str):
        """Record event retry attempt."""
        self.events_retried += 1

    def update_processing_time(self, processing_time: float):
        """Update average processing time using exponential moving average."""
        alpha = 0.1  # Smoothing factor
        self.average_processing_time = (
            alpha * processing_time +
            (1 - alpha) * self.average_processing_time
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        return {
            "events_published": self.events_published,
            "events_delivered": self.events_delivered,
            "events_failed": self.events_failed,
            "events_retried": self.events_retried,
            "delivery_rate": (
                self.events_delivered / max(1, self.events_published) * 100
            ),
            "failure_rate": (
                self.events_failed / max(1, self.events_published) * 100
            ),
            "average_processing_time_ms": self.average_processing_time * 1000,
            "error_counts": self.error_counts.copy(),
            "subscription_counts": self.subscription_counts.copy()
        }


class EventBus:
    """
    Asynchronous event bus using Redis Pub/Sub for microservices communication.

    Features:
    - Event publishing and subscription
    - Pattern-based event filtering
    - Retry logic with exponential backoff
    - Dead letter queues for failed deliveries
    - Event persistence for replay capabilities
    - Performance monitoring and metrics
    """

    def __init__(self,
                 redis_url: str = "redis://localhost:6379/0",
                 max_connections: int = 20,
                 enable_persistence: bool = True):
        self.redis_url = redis_url
        self.max_connections = max_connections
        self.enable_persistence = enable_persistence

        # Core components
        self.redis = None
        self.metrics = EventBusMetrics()
        self.publisher = EventPublisher()
        self.subscriber = EventSubscriber(metrics=self.metrics)

        # Configuration
        self.event_ttl = 3600 * 24 * 7  # 7 days
        self.max_retry_delay = 300  # 5 minutes
        self.dead_letter_ttl = 3600 * 24 * 30  # 30 days

        # State
        self._running = False
        self._startup_time = None

    async def initialize(self):
        """Initialize the event bus connection and setup."""
        try:
            # Create Redis connection pool
            self.redis = redis.Redis.from_url(
                self.redis_url,
                max_connections=self.max_connections,
                decode_responses=True,
                retry_on_timeout=True,
                socket_timeout=5,
                health_check_interval=30
            )

            # Test connection
            await self.redis.ping()

            # Connect EventPublisher
            self.publisher.redis = self.redis
            await self.publisher.connect()

            # Connect EventSubscriber
            self.subscriber.redis = self.redis
            await self.subscriber.connect()

            self._startup_time = datetime.now()
            logger.info("Event Bus initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Event Bus: {e}")
            raise

    async def shutdown(self):
        """Gracefully shutdown the event bus."""
        logger.info("Shutting down Event Bus...")

        # Cancel all active subscribers
        for task in self.active_subscribers.values():
            task.cancel()

        # Wait for tasks to complete
        if self.active_subscribers:
            await asyncio.gather(
                *self.active_subscribers.values(),
                return_exceptions=True
            )

        # Close Redis connection
        if self.redis:
            await self.redis.close()

        self._running = False
        logger.info("Event Bus shutdown complete")

    @asynccontextmanager
    async def lifecycle(self):
        """Context manager for event bus lifecycle."""
        await self.initialize()
        try:
            yield self
        finally:
            await self.shutdown()

    async def publish_event(self, event: Event) -> str:
        """
        Publish an event to all subscribers.

        Delegates to EventPublisher for V2 compliance.
        """
        start_time = asyncio.get_event_loop().time()

        try:
            # Convert event to dict for publishing
            event_dict = event.to_dict()

            # Publish using EventPublisher
            channel = f"events:{event.event_type}"
            success = await self.publisher.publish_event(event_dict, channel)

            if not success:
                raise Exception("Failed to publish event via EventPublisher")

            # Persist event if enabled
            if self.enable_persistence:
                await self._persist_event(event)

            # Record metrics
            self.metrics.record_event_published(event.event_type)

            processing_time = asyncio.get_event_loop().time() - start_time
            self.metrics.record_event_delivered(event.event_type, processing_time)

            logger.debug(f"Published event {event.event_id} of type {event.event_type}")
            return event.event_id

        except Exception as e:
            logger.error(f"Failed to publish event {event.event_id}: {e}")
            self.metrics.record_event_failed(event.event_type, type(e).__name__)
            raise

    async def subscribe_to_events(self,
                                 subscription: EventSubscription) -> str:
        """
        Subscribe to events with specified configuration.

        Delegates to EventSubscriber for V2 compliance.
        """
        return await self.subscriber.add_subscription(subscription)

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events.

        Delegates to EventSubscriber for V2 compliance.
        """
        return await self.subscriber.remove_subscription(subscription_id)

    async def _subscriber_loop(self, subscription: EventSubscription):
        """Main subscriber loop for processing events."""
        try:
            # Create pubsub instance
            pubsub = self.redis.pubsub()

            # Subscribe to channels
            channels = [f"events:{event_type}" for event_type in subscription.event_types]
            await pubsub.subscribe(*channels)

            async for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        # Parse event
                        event_dict = json.loads(message['data'])
                        event = Event(**event_dict)

                        # Apply filters
                        if self._matches_filters(event, subscription.filter_conditions):
                            # Deliver event with retry logic
                            await self._deliver_event_with_retry(event, subscription)

                    except Exception as e:
                        logger.error(f"Failed to process message: {e}")
                        continue

        except asyncio.CancelledError:
            logger.info(f"Subscriber {subscription.subscription_id} cancelled")
        except Exception as e:
            logger.error(f"Subscriber {subscription.subscription_id} failed: {e}")

    def _matches_filters(self, event: Event, filters: Dict[str, Any]) -> bool:
        """Check if event matches subscription filters."""
        if not filters:
            return True

        for key, expected_value in filters.items():
            if key == "source_service" and event.source_service != expected_value:
                return False
            elif key == "priority" and event.priority != expected_value:
                return False
            elif key == "correlation_id" and event.correlation_id != expected_value:
                return False
            elif key.startswith("data.") and event.data:
                data_key = key[5:]  # Remove "data." prefix
                if data_key not in event.data or event.data[data_key] != expected_value:
                    return False
            elif key.startswith("metadata.") and event.metadata:
                meta_key = key[9:]  # Remove "metadata." prefix
                if meta_key not in event.metadata or event.metadata[meta_key] != expected_value:
                    return False

        return True

    async def _deliver_event_with_retry(self, event: Event, subscription: EventSubscription):
        """Deliver event with retry logic and dead letter queue."""
        retry_policy = subscription.retry_policy
        max_retries = retry_policy.get("max_retries", 3)
        backoff_multiplier = retry_policy.get("backoff_multiplier", 2.0)
        initial_delay = retry_policy.get("initial_delay", 1.0)

        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                # Attempt delivery
                await subscription.callback(event)

                # Success - record metrics
                self.metrics.record_event_delivered(event.event_type)
                return

            except Exception as e:
                last_exception = e
                logger.warning(f"Event delivery attempt {attempt + 1} failed: {e}")

                if attempt < max_retries:
                    # Calculate delay with exponential backoff
                    delay = initial_delay * (backoff_multiplier ** attempt)
                    delay = min(delay, self.max_retry_delay)

                    self.metrics.record_event_retried(event.event_type)
                    await asyncio.sleep(delay)

        # All retries exhausted - send to dead letter queue
        await self._send_to_dead_letter_queue(event, subscription, last_exception)
        self.metrics.record_event_failed(event.event_type, last_exception)

    async def _send_to_dead_letter_queue(self,
                                        event: Event,
                                        subscription: EventSubscription,
                                        error: Exception):
        """Send failed event to dead letter queue."""
        if not subscription.dead_letter_queue:
            logger.warning(f"No dead letter queue configured for subscription {subscription.subscription_id}")
            return

        try:
            dlq_event = Event(
                event_id=str(uuid.uuid4()),
                event_type="dead_letter",
                source_service="event_bus",
                timestamp=datetime.now().isoformat(),
                correlation_id=event.event_id,
                data={
                    "original_event": asdict(event),
                    "subscription_id": subscription.subscription_id,
                    "error_message": str(error),
                    "error_type": type(error).__name__,
                    "failed_at": datetime.now().isoformat()
                },
                metadata={
                    "dlq_name": subscription.dead_letter_queue,
                    "retry_count": subscription.retry_policy.get("max_retries", 3)
                }
            )

            # Store in dead letter queue (Redis sorted set with timestamp)
            dlq_key = f"dlq:{subscription.dead_letter_queue}"
            score = datetime.now().timestamp()

            await self.redis.zadd(dlq_key, {json.dumps(asdict(dlq_event)): score})

            # Set TTL on DLQ
            await self.redis.expire(dlq_key, self.dead_letter_ttl)

            logger.info(f"Event {event.event_id} sent to dead letter queue")

        except Exception as dlq_error:
            logger.error(f"Failed to send event to dead letter queue: {dlq_error}")

    async def _persist_event(self, event: Event):
        """Persist event for replay capabilities."""
        try:
            event_key = f"event:{event.event_id}"
            event_data = json.dumps(asdict(event))

            # Store event data
            await self.redis.set(event_key, event_data, ex=self.event_ttl)

            # Add to event type index for replay
            type_index_key = f"events_by_type:{event.event_type}"
            await self.redis.zadd(type_index_key, {event.event_id: datetime.now().timestamp()})
            await self.redis.expire(type_index_key, self.event_ttl)

            # Add to correlation index if present
            if event.correlation_id:
                corr_index_key = f"events_by_correlation:{event.correlation_id}"
                await self.redis.zadd(corr_index_key, {event.event_id: datetime.now().timestamp()})
                await self.redis.expire(corr_index_key, self.event_ttl)

        except Exception as e:
            logger.error(f"Failed to persist event {event.event_id}: {e}")

    async def replay_events(self,
                           event_type: str,
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None,
                           correlation_id: Optional[str] = None) -> List[Event]:
        """
        Replay events for debugging or catch-up scenarios.

        Args:
            event_type: Type of events to replay
            start_time: Start time for replay (optional)
            end_time: End time for replay (optional)
            correlation_id: Correlation ID to filter by (optional)

        Returns:
            List of replayed events
        """
        events = []

        try:
            if correlation_id:
                # Replay by correlation ID
                corr_index_key = f"events_by_correlation:{correlation_id}"
                event_ids = await self.redis.zrange(corr_index_key, 0, -1)
            else:
                # Replay by event type
                type_index_key = f"events_by_type:{event_type}"
                start_score = start_time.timestamp() if start_time else 0
                end_score = end_time.timestamp() if end_time else float('inf')

                event_ids = await self.redis.zrangebyscore(
                    type_index_key, start_score, end_score
                )

            # Retrieve and reconstruct events
            for event_id in event_ids:
                event_key = f"event:{event_id}"
                event_data = await self.redis.get(event_key)

                if event_data:
                    event_dict = json.loads(event_data)
                    event = Event(**event_dict)
                    events.append(event)

        except Exception as e:
            logger.error(f"Failed to replay events: {e}")

        return events

    async def get_queue_status(self) -> Dict[str, Any]:
        """Get current status of event queues and subscriptions."""
        status = {
            "active_subscriptions": len(self.subscriptions),
            "active_subscribers": len(self.active_subscribers),
            "uptime_seconds": (
                datetime.now() - self._startup_time
            ).total_seconds() if self._startup_time else 0,
            "metrics": self.metrics.get_metrics()
        }

        # Get Redis info
        try:
            redis_info = await self.redis.info()
            status["redis_connected_clients"] = redis_info.get("connected_clients", 0)
            status["redis_used_memory"] = redis_info.get("used_memory_human", "unknown")
        except:
            status["redis_status"] = "disconnected"

        return status

    def create_event(self,
                    event_type: str,
                    source_service: str,
                    data: Dict[str, Any] = None,
                    correlation_id: Optional[str] = None,
                    priority: str = "normal",
                    metadata: Dict[str, Any] = None) -> Event:
        """
        Helper method to create standardized events.

        Delegates to the extracted create_event function for V2 compliance.
        """
        return create_event(
            event_type=event_type,
            source_service=source_service,
            data=data,
            correlation_id=correlation_id,
            priority=priority,
            metadata=metadata
        )


# Global event bus instance for the application
_event_bus_instance: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = EventBus()
    return _event_bus_instance


async def initialize_event_bus():
    """Initialize the global event bus."""
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = EventBus()
        await _event_bus_instance.initialize()
    return _event_bus_instance


async def shutdown_event_bus():
    """Shutdown the global event bus."""
    global _event_bus_instance
    if _event_bus_instance:
        await _event_bus_instance.shutdown()
        _event_bus_instance = None


# Example usage and testing functions
async def example_event_bus_usage():
    """Example of how to use the event bus."""
    async with EventBus().lifecycle() as event_bus:

        # Create a subscription
        async def handle_context_events(event: Event):
            print(f"Received context event: {event.event_type} from {event.source_service}")
            print(f"Event data: {event.data}")

        subscription = EventSubscription(
            subscription_id="context_handler",
            event_types=["context_update", "suggestion_generated"],
            callback=handle_context_events
        )

        await event_bus.subscribe_to_events(subscription)

        # Publish some events
        event1 = event_bus.create_event(
            event_type="context_update",
            source_service="ai_context_engine",
            data={"user_id": "user123", "action": "page_view"},
            correlation_id="session_abc123"
        )

        event2 = event_bus.create_event(
            event_type="suggestion_generated",
            source_service="ai_service",
            data={"suggestion_id": "sugg_456", "confidence": 0.95},
            correlation_id="session_abc123"
        )

        await event_bus.publish_event(event1)
        await event_bus.publish_event(event2)

        # Let events be processed
        await asyncio.sleep(2)

        # Get status
        status = await event_bus.get_queue_status()
        print(f"Event bus status: {status}")


if __name__ == "__main__":
    # Run example when executed directly
    asyncio.run(example_event_bus_usage())