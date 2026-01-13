#!/usr/bin/env python3
"""
Event Persistence Service - Phase 6 Infrastructure
================================================

Event persistence and replay capabilities.

<!-- SSOT Domain: event_bus_persistence -->

Features:
- Redis-based event storage and retrieval
- Event replay functionality with time-based filtering
- Event indexing for efficient querying
- TTL-based automatic cleanup
- Event deduplication and versioning

Author: Agent-5 (Business Intelligence Specialist) - Enhanced by Agent-2
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import redis.asyncio as redis

from .event_models import Event

logger = logging.getLogger(__name__)


class EventPersistenceService:
    """
    Handles event persistence and replay using Redis.

    Features:
    - Redis-based event storage with TTL
    - Time-based event replay
    - Event type indexing for efficient querying
    - Correlation ID tracking for event chains
    - Automatic cleanup of expired events
    """

    def __init__(self,
                 redis_client: redis.Redis = None,
                 event_ttl: int = 3600 * 24 * 7,
                 enable_persistence: bool = True):
        """
        Initialize the persistence service.

        Args:
            redis_client: Redis client for persistence
            event_ttl: Time-to-live for events in seconds (default: 7 days)
            enable_persistence: Whether to enable event persistence
        """
        self.redis = redis_client
        self.event_ttl = event_ttl
        self.enable_persistence = enable_persistence

        # Redis keys
        self.events_key_prefix = "events:stored:"
        self.events_by_type_key_prefix = "events:by_type:"
        self.events_by_correlation_key_prefix = "events:by_correlation:"
        self.event_index_key = "events:index"
        self.event_metadata_key = "events:metadata"

    async def persist_event(self, event: Event) -> bool:
        """
        Store an event for persistence.

        Args:
            event: Event object to store

        Returns:
            True if stored successfully
        """
        if not self.enable_persistence or not self.redis:
            return True  # No-op if persistence disabled

        try:
            event_dict = event.to_dict()
            event_id = event.event_id
            event_type = event.event_type
            correlation_id = event.correlation_id or event_id

            # Store the full event
            event_key = f"{self.events_key_prefix}{event_id}"
            await self.redis.setex(
                event_key,
                self.event_ttl,
                json.dumps(event_dict)
            )

            # Index by event type
            type_key = f"{self.events_by_type_key_prefix}{event_type}"
            await self.redis.lpush(type_key, event_id)
            await self.redis.expire(type_key, self.event_ttl)

            # Index by correlation ID
            if correlation_id != event_id:
                correlation_key = f"{self.events_by_correlation_key_prefix}{correlation_id}"
                await self.redis.lpush(correlation_key, event_id)
                await self.redis.expire(correlation_key, self.event_ttl)

            # Add to global event index with timestamp
            index_entry = {
                'event_id': event_id,
                'event_type': event_type,
                'correlation_id': correlation_id,
                'timestamp': event.timestamp.isoformat() if event.timestamp else datetime.now().isoformat(),
                'source_service': event.source_service
            }

            await self.redis.zadd(
                self.event_index_key,
                {json.dumps(index_entry): event.timestamp.timestamp() if event.timestamp else datetime.now().timestamp()}
            )

            # Clean up old index entries (keep last 100k entries)
            await self.redis.zremrangebyrank(self.event_index_key, 0, -100001)

            logger.debug(f"Event persisted: {event_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to persist event {event.event_id}: {e}")
            return False

    async def replay_events(self,
                           event_type: Optional[str] = None,
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None,
                           correlation_id: Optional[str] = None,
                           source_service: Optional[str] = None,
                           limit: int = 1000) -> List[Event]:
        """
        Replay events based on various filters.

        Args:
            event_type: Filter by event type
            start_time: Start time for replay
            end_time: End time for replay
            correlation_id: Filter by correlation ID
            source_service: Filter by source service
            limit: Maximum number of events to return

        Returns:
            List of Event objects
        """
        if not self.enable_persistence or not self.redis:
            return []

        try:
            events = []

            # If correlation_id is specified, get events by correlation
            if correlation_id:
                correlation_key = f"{self.events_by_correlation_key_prefix}{correlation_id}"
                event_ids = await self.redis.lrange(correlation_key, 0, limit - 1)

                for event_id in event_ids:
                    event = await self._get_event_by_id(event_id)
                    if event:
                        events.append(event)

            # If event_type is specified, get events by type
            elif event_type:
                type_key = f"{self.events_by_type_key_prefix}{event_type}"
                event_ids = await self.redis.lrange(type_key, 0, limit - 1)

                for event_id in event_ids:
                    event = await self._get_event_by_id(event_id)
                    if event:
                        events.append(event)

            # Otherwise, get events from global index with time filtering
            else:
                # Prepare time range
                min_score = start_time.timestamp() if start_time else '-inf'
                max_score = end_time.timestamp() if end_time else '+inf'

                # Get event entries from index
                index_entries = await self.redis.zrangebyscore(
                    self.event_index_key,
                    min_score,
                    max_score,
                    start=0,
                    num=limit,
                    withscores=False
                )

                for entry_json in index_entries:
                    entry = json.loads(entry_json)

                    # Apply additional filters
                    if source_service and entry.get('source_service') != source_service:
                        continue

                    event = await self._get_event_by_id(entry['event_id'])
                    if event:
                        events.append(event)

            # Sort events by timestamp
            events.sort(key=lambda e: e.timestamp or datetime.min)

            return events[:limit]

        except Exception as e:
            logger.error(f"Failed to replay events: {e}")
            return []

    async def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """
        Get a specific event by ID.

        Args:
            event_id: Event ID to retrieve

        Returns:
            Event object if found, None otherwise
        """
        return await self._get_event_by_id(event_id)

    async def _get_event_by_id(self, event_id: str) -> Optional[Event]:
        """
        Internal method to get event by ID.

        Args:
            event_id: Event ID to retrieve

        Returns:
            Event object if found, None otherwise
        """
        if not self.redis:
            return None

        try:
            event_key = f"{self.events_key_prefix}{event_id}"
            event_json = await self.redis.get(event_key)

            if event_json:
                event_dict = json.loads(event_json)
                return Event.from_dict(event_dict)

        except Exception as e:
            logger.error(f"Failed to get event {event_id}: {e}")

        return None

    async def delete_event(self, event_id: str) -> bool:
        """
        Delete a persisted event.

        Args:
            event_id: Event ID to delete

        Returns:
            True if deleted successfully
        """
        if not self.enable_persistence or not self.redis:
            return True

        try:
            event_key = f"{self.events_key_prefix}{event_id}"
            deleted = await self.redis.delete(event_key)

            # Note: Index cleanup would require scanning all indices
            # For simplicity, we'll rely on TTL for cleanup

            logger.debug(f"Event deleted: {event_id}")
            return deleted > 0

        except Exception as e:
            logger.error(f"Failed to delete event {event_id}: {e}")
            return False

    async def get_event_types(self) -> List[str]:
        """
        Get list of all event types that have been stored.

        Returns:
            List of event types
        """
        if not self.redis:
            return []

        try:
            # Get all type keys
            pattern = f"{self.events_by_type_key_prefix}*"
            keys = await self.redis.keys(pattern)

            event_types = []
            for key in keys:
                # Extract event type from key
                event_type = key.decode().replace(self.events_by_type_key_prefix, '')
                event_types.append(event_type)

            return sorted(event_types)

        except Exception as e:
            logger.error(f"Failed to get event types: {e}")
            return []

    async def get_event_stats(self) -> Dict[str, Any]:
        """
        Get persistence statistics.

        Returns:
            Dictionary with persistence statistics
        """
        if not self.redis:
            return {'enabled': False}

        try:
            # Count events by type
            type_counts = {}
            pattern = f"{self.events_by_type_key_prefix}*"
            keys = await self.redis.keys(pattern)

            for key in keys:
                event_type = key.decode().replace(self.events_by_type_key_prefix, '')
                count = await self.redis.llen(key)
                type_counts[event_type] = count

            # Get total events in index
            total_events = await self.redis.zcount(self.event_index_key, '-inf', '+inf')

            return {
                'enabled': self.enable_persistence,
                'total_events': total_events,
                'events_by_type': type_counts,
                'event_ttl_seconds': self.event_ttl
            }

        except Exception as e:
            logger.error(f"Failed to get event stats: {e}")
            return {'enabled': False, 'error': str(e)}

    async def cleanup_expired_events(self) -> int:
        """
        Manually cleanup expired events (normally handled by Redis TTL).

        Returns:
            Number of events cleaned up
        """
        if not self.redis:
            return 0

        try:
            # This is a maintenance operation
            # In practice, Redis TTL handles most cleanup automatically
            # This method could be used for custom cleanup logic

            cleaned_count = 0

            # Clean up empty type index lists
            pattern = f"{self.events_by_type_key_prefix}*"
            keys = await self.redis.keys(pattern)

            for key in keys:
                length = await self.redis.llen(key)
                if length == 0:
                    await self.redis.delete(key)
                    cleaned_count += 1

            logger.info(f"Cleaned up {cleaned_count} expired event indices")
            return cleaned_count

        except Exception as e:
            logger.error(f"Failed to cleanup expired events: {e}")
            return 0