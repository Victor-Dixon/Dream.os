#!/usr/bin/env python3
"""
Event Subscriber - Phase 6 Infrastructure
=======================================

Event subscription and consumption functionality.

<!-- SSOT Domain: event_bus_subscriber -->

Features:
- Event subscription management
- Asynchronous event consumption
- Redis Pub/Sub integration
- Callback-based event handling
- Subscription lifecycle management
- Event filtering and routing

Author: Agent-5 (Business Intelligence Specialist) - Enhanced by Agent-2
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import asyncio
import json
import logging
from typing import Dict, Any, Callable, Optional, List, Set
from datetime import datetime
import redis.asyncio as redis

from .event_models import EventSubscription, Event

logger = logging.getLogger(__name__)


class EventSubscriber:
    """
    Handles event subscription and consumption with Redis Pub/Sub.

    Features:
    - Redis-based event subscription
    - Asynchronous event processing
    - Callback-based event handling
    - Subscription filtering and routing
    - Connection management and reconnection
    - Performance monitoring
    """

    def __init__(self, metrics=None):
        """
        Initialize the event subscriber.

        Args:
            metrics: Metrics collection service
        """
        self.redis = None
        self.metrics = metrics
        self.subscriptions = {}  # subscription_id -> EventSubscription
        self.active_tasks = {}   # subscription_id -> asyncio.Task
        self.pubsub_connections = {}  # subscription_id -> redis.PubSub

        # Configuration
        self.reconnect_delay = 5  # seconds
        self.max_reconnect_attempts = 10
        self.processing_timeout = 30  # seconds

    async def connect(self, redis_client: redis.Redis = None):
        """
        Connect to Redis for event subscription.

        Args:
            redis_client: Redis client instance
        """
        if redis_client:
            self.redis = redis_client
        elif not self.redis:
            raise ValueError("Redis client not provided and not previously set")

        logger.info("EventSubscriber connected to Redis")

    async def disconnect(self):
        """
        Disconnect from Redis and cleanup resources.
        """
        # Cancel all active subscription tasks
        for task in self.active_tasks.values():
            if not task.done():
                task.cancel()

        # Wait for tasks to complete
        if self.active_tasks:
            await asyncio.gather(*self.active_tasks.values(), return_exceptions=True)

        # Close pubsub connections
        for pubsub in self.pubsub_connections.values():
            try:
                await pubsub.close()
            except Exception as e:
                logger.error(f"Error closing pubsub connection: {e}")

        self.active_tasks.clear()
        self.pubsub_connections.clear()
        logger.info("EventSubscriber disconnected")

    async def add_subscription(self, subscription: EventSubscription) -> str:
        """
        Register a new event subscription and start consuming events.

        Args:
            subscription: Event subscription configuration

        Returns:
            Subscription ID
        """
        if not self.redis:
            raise RuntimeError("Redis client not connected")

        subscription_id = subscription.subscription_id

        # Store subscription
        self.subscriptions[subscription_id] = subscription
        logger.info(f"Subscription registered: {subscription_id}")

        # Start subscription task
        task = asyncio.create_task(self._subscription_loop(subscription))
        self.active_tasks[subscription_id] = task

        if self.metrics:
            self.metrics.record_subscription_added(subscription_id)

        return subscription_id

    async def remove_subscription(self, subscription_id: str) -> bool:
        """
        Remove an event subscription and stop consuming events.

        Args:
            subscription_id: ID of subscription to remove

        Returns:
            True if subscription was removed
        """
        if subscription_id not in self.subscriptions:
            return False

        # Cancel and cleanup task
        if subscription_id in self.active_tasks:
            task = self.active_tasks[subscription_id]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_tasks[subscription_id]

        # Close pubsub connection
        if subscription_id in self.pubsub_connections:
            try:
                await self.pubsub_connections[subscription_id].close()
            except Exception as e:
                logger.error(f"Error closing pubsub for {subscription_id}: {e}")
            del self.pubsub_connections[subscription_id]

        # Remove subscription
        del self.subscriptions[subscription_id]
        logger.info(f"Subscription removed: {subscription_id}")

        if self.metrics:
            self.metrics.record_subscription_removed(subscription_id)

        return True

    async def _subscription_loop(self, subscription: EventSubscription):
        """
        Main subscription loop for processing events.

        Args:
            subscription: Subscription configuration
        """
        subscription_id = subscription.subscription_id
        reconnect_attempts = 0

        while reconnect_attempts < self.max_reconnect_attempts:
            try:
                # Create pubsub instance
                pubsub = self.redis.pubsub()
                self.pubsub_connections[subscription_id] = pubsub

                # Subscribe to channels based on event patterns
                channels = []
                for pattern in subscription.event_patterns:
                    if pattern == "*":
                        # Subscribe to all events channel
                        channels.append("events:*")
                    elif pattern.endswith("*"):
                        # Pattern subscription (Redis supports glob patterns)
                        channels.append(f"events:{pattern}")
                    else:
                        # Exact event type
                        channels.append(f"events:{pattern}")

                if channels:
                    await pubsub.subscribe(*channels)
                    logger.info(f"Subscribed {subscription_id} to channels: {channels}")
                else:
                    logger.warning(f"No channels to subscribe for {subscription_id}")
                    await asyncio.sleep(1)
                    continue

                # Process messages
                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            await self._process_message(message, subscription)
                        except Exception as e:
                            logger.error(f"Failed to process message for {subscription_id}: {e}")
                            if self.metrics:
                                self.metrics.record_message_processing_error(subscription_id)

                # Reset reconnect attempts on successful connection
                reconnect_attempts = 0

            except asyncio.CancelledError:
                logger.info(f"Subscription {subscription_id} cancelled")
                break
            except Exception as e:
                reconnect_attempts += 1
                logger.error(f"Subscription {subscription_id} failed (attempt {reconnect_attempts}): {e}")

                if reconnect_attempts < self.max_reconnect_attempts:
                    await asyncio.sleep(self.reconnect_delay * reconnect_attempts)
                else:
                    logger.error(f"Max reconnect attempts reached for {subscription_id}")
                    break

        # Cleanup on exit
        if subscription_id in self.pubsub_connections:
            del self.pubsub_connections[subscription_id]

    async def _process_message(self, message: Dict[str, Any], subscription: EventSubscription):
        """
        Process a received message.

        Args:
            message: Redis pubsub message
            subscription: Subscription configuration
        """
        try:
            # Parse event data
            event_data = json.loads(message['data'])
            event = Event.from_dict(event_data)

            # Check if event matches subscription patterns
            if not subscription.matches_event(event):
                return

            # Record metrics
            if self.metrics:
                self.metrics.record_event_received(event.event_type, subscription.subscription_id)

            # Execute callback with timeout
            if subscription.callback:
                try:
                    await asyncio.wait_for(
                        subscription.callback(event),
                        timeout=self.processing_timeout
                    )

                    if self.metrics:
                        self.metrics.record_event_processed(event.event_type, subscription.subscription_id)

                except asyncio.TimeoutError:
                    logger.error(f"Event processing timeout for {event.event_id}")
                    if self.metrics:
                        self.metrics.record_event_processing_timeout(event.event_type, subscription.subscription_id)

                except Exception as e:
                    logger.error(f"Event processing error for {event.event_id}: {e}")
                    if self.metrics:
                        self.metrics.record_event_processing_error(event.event_type, subscription.subscription_id)
            else:
                logger.warning(f"No callback defined for subscription {subscription.subscription_id}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse event message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing message: {e}")

    async def consume_events(self, subscription_id: Optional[str] = None) -> List[Event]:
        """
        Manually consume available events from subscriptions.

        Args:
            subscription_id: Optional specific subscription ID

        Returns:
            List of consumed events
        """
        # This method is for manual consumption/polling
        # In the pubsub model, events are consumed asynchronously via callbacks
        # This could be used for testing or fallback scenarios

        events = []

        if subscription_id and subscription_id in self.subscriptions:
            # Get events for specific subscription
            subscription = self.subscriptions[subscription_id]
            # In a real implementation, this might check a queue or buffer
            logger.debug(f"Manual consumption requested for {subscription_id}")
        else:
            # Get events for all subscriptions
            logger.debug("Manual consumption requested for all subscriptions")

        return events

    async def get_subscription_status(self) -> Dict[str, Any]:
        """
        Get status of all subscriptions.

        Returns:
            Dictionary with subscription status information
        """
        status = {
            'total_subscriptions': len(self.subscriptions),
            'active_tasks': len([t for t in self.active_tasks.values() if not t.done()]),
            'pubsub_connections': len(self.pubsub_connections),
            'subscriptions': {}
        }

        for subscription_id, subscription in self.subscriptions.items():
            task_active = False
            if subscription_id in self.active_tasks:
                task = self.active_tasks[subscription_id]
                task_active = not task.done()

            status['subscriptions'][subscription_id] = {
                'active': task_active,
                'patterns': subscription.event_patterns,
                'has_callback': subscription.callback is not None,
                'enabled': subscription.enabled,
                'created_at': subscription.created_at.isoformat() if subscription.created_at else None
            }

        return status

    async def get_active_subscriptions(self) -> List[str]:
        """
        Get list of active subscription IDs.

        Returns:
            List of active subscription IDs
        """
        return list(self.subscriptions.keys())

    async def update_subscription(self,
                                 subscription_id: str,
                                 **updates) -> bool:
        """
        Update an existing subscription.

        Args:
            subscription_id: ID of subscription to update
            **updates: Fields to update

        Returns:
            True if subscription was updated
        """
        if subscription_id not in self.subscriptions:
            return False

        subscription = self.subscriptions[subscription_id]

        # Update fields
        for key, value in updates.items():
            if hasattr(subscription, key):
                setattr(subscription, key, value)

        logger.info(f"Subscription updated: {subscription_id}")
        return True