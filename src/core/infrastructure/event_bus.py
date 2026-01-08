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
from .event_delivery import EventDeliveryService
from .event_persistence import EventPersistenceService
from .event_filtering import EventFilterService

logger = logging.getLogger(__name__)

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

        # Extracted services for V2 compliance
        self.delivery_service = None
        self.persistence_service = None
        self.filter_service = EventFilterService()

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

            # Initialize extracted services
            self.delivery_service = EventDeliveryService(
                redis_client=self.redis,
                metrics=self.metrics,
                max_retry_delay=self.max_retry_delay,
                dead_letter_ttl=self.dead_letter_ttl
            )

            self.persistence_service = EventPersistenceService(
                redis_client=self.redis,
                event_ttl=self.event_ttl,
                enable_persistence=self.enable_persistence
            )

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

            # Persist event using persistence service
            await self.persistence_service.persist_event(event)

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





    async def replay_events(self,
                           event_type: Optional[str] = None,
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None,
                           correlation_id: Optional[str] = None) -> List[Event]:
        """
        Replay events for debugging or catch-up scenarios.

        Delegates to EventPersistenceService for V2 compliance.
        """
        return await self.persistence_service.replay_events(
            event_type=event_type,
            start_time=start_time,
            end_time=end_time,
            correlation_id=correlation_id
        )

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

