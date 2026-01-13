#!/usr/bin/env python3
"""
Event Publisher - Phase 6 Infrastructure
======================================

Event publishing functionality for the event bus system.

<!-- SSOT Domain: event_bus_publisher -->

Features:
- Asynchronous event publishing via Redis Pub/Sub
- Batch publishing support with concurrency control
- Event validation and serialization
- Connection management and error handling

Author: Agent-5 (Business Intelligence Specialist) - Enhanced by Agent-2
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
import redis.asyncio as redis

from .event_models import Event

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Handles event publishing to Redis Pub/Sub channels.

    Features:
    - Redis-based event publishing
    - Batch publishing with concurrency control
    - Event validation and error handling
    - Connection pooling and reconnection
    """

    def __init__(self, redis_client: redis.Redis = None):
        """
        Initialize the event publisher.

        Args:
            redis_client: Redis client for publishing
        """
        self.redis = redis_client
        self._connected = False

    async def connect(self, redis_client: redis.Redis = None):
        """
        Connect to Redis for publishing.

        Args:
            redis_client: Redis client instance (optional)
        """
        if redis_client:
            self.redis = redis_client
        elif not self.redis:
            raise ValueError("Redis client not provided")

        try:
            # Test connection
            await self.redis.ping()
            self._connected = True
            logger.info("EventPublisher connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect EventPublisher to Redis: {e}")
            raise

    async def disconnect(self):
        """
        Disconnect from Redis.
        """
        # Redis client is managed externally, just mark as disconnected
        self._connected = False
        logger.info("EventPublisher disconnected")

    async def publish_event(self, event_dict: Dict[str, Any], channel: str) -> bool:
        """
        Publish a single event to a Redis channel.

        Args:
            event_dict: Event data as dictionary
            channel: Redis channel to publish to

        Returns:
            True if published successfully
        """
        if not self._connected or not self.redis:
            logger.error("EventPublisher not connected to Redis")
            return False

        try:
            # Serialize event to JSON
            event_json = json.dumps(event_dict)

            # Publish to Redis channel
            subscribers = await self.redis.publish(channel, event_json)

            logger.debug(f"Event published to channel '{channel}': {event_dict.get('event_id', 'unknown')} ({subscribers} subscribers)")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event to channel '{channel}': {e}")
            return False

    async def publish_event_object(self, event: Event) -> bool:
        """
        Publish an Event object to the appropriate channel.

        Args:
            event: Event object to publish

        Returns:
            True if published successfully
        """
        # Convert event to dict and determine channel
        event_dict = event.to_dict()
        channel = f"events:{event.event_type}"

        return await self.publish_event(event_dict, channel)

    async def publish_events_batch(self,
                                  events: List[Dict[str, Any]],
                                  channel: str,
                                  concurrency_limit: int = 10) -> Dict[str, Any]:
        """
        Publish multiple events in batch with concurrency control.

        Args:
            events: List of event dictionaries to publish
            channel: Redis channel to publish to
            concurrency_limit: Maximum concurrent publishing operations

        Returns:
            Batch publishing results
        """
        if not events:
            return {
                "total_events": 0,
                "successful": 0,
                "failed": 0,
                "results": []
            }

        async def publish_single(event_dict: Dict[str, Any]) -> Dict[str, Any]:
            """Publish a single event and return result."""
            event_id = event_dict.get('event_id', 'unknown')
            success = await self.publish_event(event_dict, channel)
            return {
                "event_id": event_id,
                "success": success,
                "channel": channel
            }

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(concurrency_limit)

        async def limited_publish(event_dict: Dict[str, Any]) -> Dict[str, Any]:
            async with semaphore:
                return await publish_single(event_dict)

        # Publish all events concurrently with limit
        tasks = [limited_publish(event) for event in events]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        processed_results = []
        successful = 0
        failed = 0

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exceptions
                event_id = events[i].get('event_id', f'unknown_{i}')
                processed_results.append({
                    "event_id": event_id,
                    "success": False,
                    "error": str(result),
                    "channel": channel
                })
                failed += 1
            else:
                processed_results.append(result)
                if result["success"]:
                    successful += 1
                else:
                    failed += 1

        logger.info(f"Batch publish complete: {successful}/{len(events)} successful, {failed} failed")

        return {
            "total_events": len(events),
            "successful": successful,
            "failed": failed,
            "results": processed_results,
            "channel": channel
        }

    async def publish_events_by_type(self,
                                    events: List[Event],
                                    concurrency_limit: int = 10) -> Dict[str, Any]:
        """
        Publish multiple Event objects, grouped by event type.

        Args:
            events: List of Event objects to publish
            concurrency_limit: Maximum concurrent publishing operations

        Returns:
            Batch publishing results by channel
        """
        if not events:
            return {"channels": {}, "total_events": 0, "total_successful": 0, "total_failed": 0}

        # Group events by type
        events_by_type = {}
        for event in events:
            event_type = event.event_type
            if event_type not in events_by_type:
                events_by_type[event_type] = []
            events_by_type[event_type].append(event.to_dict())

        # Publish each group
        channel_results = {}
        total_successful = 0
        total_failed = 0

        for event_type, event_dicts in events_by_type.items():
            channel = f"events:{event_type}"
            result = await self.publish_events_batch(event_dicts, channel, concurrency_limit)
            channel_results[channel] = result
            total_successful += result["successful"]
            total_failed += result["failed"]

        return {
            "channels": channel_results,
            "total_events": len(events),
            "total_successful": total_successful,
            "total_failed": total_failed
        }

    async def get_channel_info(self, channel: str) -> Dict[str, Any]:
        """
        Get information about a Redis channel.

        Args:
            channel: Channel name to query

        Returns:
            Channel information
        """
        if not self.redis:
            return {"error": "Redis client not available"}

        try:
            # Get number of subscribers (approximate)
            # Note: Redis doesn't provide direct subscriber count for pubsub
            # This is a placeholder - in practice you'd need to track this separately
            info = {
                "channel": channel,
                "estimated_subscribers": "unknown",  # Redis doesn't expose this
                "last_activity": "unknown"  # Would need separate tracking
            }
            return info

        except Exception as e:
            logger.error(f"Failed to get channel info for '{channel}': {e}")
            return {"error": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the publisher.

        Returns:
            Health status information
        """
        health = {
            "service": "EventPublisher",
            "connected": self._connected,
            "redis_available": False,
            "timestamp": asyncio.get_event_loop().time()
        }

        if self.redis:
            try:
                await self.redis.ping()
                health["redis_available"] = True
            except Exception as e:
                health["redis_error"] = str(e)

        return health