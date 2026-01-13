#!/usr/bin/env python3
"""
Event Delivery Service - Phase 6 Infrastructure
==============================================

Handles event delivery with retry logic and dead letter queues.

<!-- SSOT Domain: event_bus_delivery -->

Features:
- Retry logic with exponential backoff
- Dead letter queue management
- Redis-based event delivery tracking
- Circuit breaker pattern for failed deliveries
- Delivery metrics and monitoring

Author: Agent-5 (Business Intelligence Specialist) - Enhanced by Agent-2
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
import redis.asyncio as redis

logger = logging.getLogger(__name__)


class EventDeliveryService:
    """
    Handles event delivery with retry logic, dead letter queues, and monitoring.

    Features:
    - Exponential backoff retry logic
    - Dead letter queue for failed deliveries
    - Redis-based delivery tracking
    - Circuit breaker pattern
    - Delivery metrics collection
    """

    def __init__(self,
                 redis_client: redis.Redis = None,
                 metrics=None,
                 max_retry_delay: int = 300,
                 dead_letter_ttl: int = 3600 * 24 * 30):
        """
        Initialize the delivery service.

        Args:
            redis_client: Redis client for persistence
            metrics: Metrics collection service
            max_retry_delay: Maximum delay between retries in seconds
            dead_letter_ttl: TTL for dead letter queue items in seconds
        """
        self.redis = redis_client
        self.metrics = metrics
        self.max_retry_delay = max_retry_delay
        self.dead_letter_ttl = dead_letter_ttl

        # Retry configuration
        self.retry_delays = [1, 5, 15, 60, 300]  # seconds (5 retries max)

        # Circuit breaker state
        self.failure_threshold = 5
        self.recovery_timeout = 60  # seconds
        self.circuit_breaker_state = {}  # event_type -> {'failures': int, 'last_failure': datetime}

        # Redis keys
        self.dead_letter_key = "events:dead_letter"
        self.delivery_attempts_key = "events:delivery_attempts"

    async def deliver_event(self,
                           event: Dict[str, Any],
                           callback: Optional[Callable] = None) -> bool:
        """
        Attempt to deliver an event with circuit breaker protection.

        Args:
            event: Event data to deliver
            callback: Optional callback function for delivery

        Returns:
            True if delivery successful
        """
        event_type = event.get('event_type', 'unknown')
        event_id = event.get('event_id', 'unknown')

        # Check circuit breaker
        if self._is_circuit_open(event_type):
            logger.warning(f"Circuit breaker open for {event_type}, skipping delivery")
            await self._send_to_dead_letter(event, "circuit_breaker_open")
            return False

        try:
            # Execute delivery
            if callback:
                success = await callback(event)
            else:
                success = await self._execute_delivery(event)

            if success:
                # Reset circuit breaker on success
                self._reset_circuit_breaker(event_type)
                logger.debug(f"Event delivered successfully: {event_id}")
                if self.metrics:
                    self.metrics.record_delivery_success(event_type)
                return True
            else:
                # Record failure for circuit breaker
                self._record_delivery_failure(event_type)
                logger.warning(f"Event delivery failed: {event_id}")
                if self.metrics:
                    self.metrics.record_delivery_failure(event_type)
                return False

        except Exception as e:
            # Record failure for circuit breaker
            self._record_delivery_failure(event_type)
            logger.error(f"Event delivery error for {event_id}: {e}")
            if self.metrics:
                self.metrics.record_delivery_error(event_type, type(e).__name__)
            await self._send_to_dead_letter(event, f"delivery_error: {str(e)}")
            return False

    async def retry_delivery(self,
                            event: Dict[str, Any],
                            attempt: int,
                            callback: Optional[Callable] = None) -> bool:
        """
        Retry event delivery with exponential backoff.

        Args:
            event: Event data to retry
            attempt: Retry attempt number (0-based)
            callback: Optional delivery callback

        Returns:
            True if delivery successful
        """
        event_id = event.get('event_id', 'unknown')

        if attempt >= len(self.retry_delays):
            logger.error(f"Max retries ({len(self.retry_delays)}) exceeded for event: {event_id}")
            await self._send_to_dead_letter(event, "max_retries_exceeded")
            return False

        delay = min(self.retry_delays[attempt], self.max_retry_delay)
        logger.info(f"Retrying delivery for event {event_id} (attempt {attempt + 1}) in {delay}s")

        # Record retry attempt
        await self._record_retry_attempt(event, attempt)

        await asyncio.sleep(delay)
        return await self.deliver_event(event, callback)

    async def deliver_with_retry(self,
                                event: Dict[str, Any],
                                callback: Optional[Callable] = None,
                                max_attempts: int = None) -> bool:
        """
        Deliver event with full retry logic and dead letter handling.

        Args:
            event: Event data to deliver
            callback: Optional delivery callback
            max_attempts: Maximum delivery attempts (defaults to retry_delays length)

        Returns:
            True if delivery successful
        """
        if max_attempts is None:
            max_attempts = len(self.retry_delays) + 1  # +1 for initial attempt

        for attempt in range(max_attempts):
            try:
                if attempt == 0:
                    # Initial delivery attempt
                    success = await self.deliver_event(event, callback)
                else:
                    # Retry attempt
                    success = await self.retry_delivery(event, attempt - 1, callback)

                if success:
                    return True

            except Exception as e:
                logger.error(f"Delivery attempt {attempt + 1} failed for event {event.get('event_id')}: {e}")
                continue

        # All attempts failed
        logger.error(f"All delivery attempts failed for event {event.get('event_id')}")
        return False

    async def _execute_delivery(self, event: Dict[str, Any]) -> bool:
        """
        Execute the actual event delivery logic.

        Args:
            event: Event data to deliver

        Returns:
            True if delivery successful
        """
        # This is where the actual delivery logic would go
        # For now, we'll simulate successful delivery
        # In a real implementation, this would:
        # - Send to webhook endpoints
        # - Publish to message queues
        # - Call registered callbacks
        # - Execute business logic

        event_type = event.get('event_type', 'unknown')
        logger.debug(f"Executing delivery for event type: {event_type}")

        # Simulate processing time
        await asyncio.sleep(0.01)  # 10ms processing

        # For now, always succeed (this would be replaced with real delivery logic)
        return True

    async def _send_to_dead_letter(self,
                                  event: Dict[str, Any],
                                  reason: str) -> None:
        """
        Send failed event to dead letter queue.

        Args:
            event: Failed event data
            reason: Reason for failure
        """
        if not self.redis:
            logger.warning("Redis not available, cannot send to dead letter queue")
            return

        try:
            dead_letter_item = {
                'event': event,
                'reason': reason,
                'timestamp': datetime.now().isoformat(),
                'attempts': event.get('delivery_attempts', 0) + 1
            }

            # Add to dead letter queue
            await self.redis.lpush(self.dead_letter_key, json.dumps(dead_letter_item))

            # Set TTL on the list (extend if already exists)
            await self.redis.expire(self.dead_letter_key, self.dead_letter_ttl)

            logger.info(f"Event {event.get('event_id')} sent to dead letter queue: {reason}")

        except Exception as e:
            logger.error(f"Failed to send event to dead letter queue: {e}")

    async def _record_retry_attempt(self,
                                   event: Dict[str, Any],
                                   attempt: int) -> None:
        """
        Record retry attempt in Redis.

        Args:
            event: Event data
            attempt: Retry attempt number
        """
        if not self.redis:
            return

        try:
            attempt_data = {
                'event_id': event.get('event_id'),
                'event_type': event.get('event_type'),
                'attempt': attempt + 1,
                'timestamp': datetime.now().isoformat()
            }

            await self.redis.lpush(
                f"{self.delivery_attempts_key}:{event.get('event_id')}",
                json.dumps(attempt_data)
            )

        except Exception as e:
            logger.error(f"Failed to record retry attempt: {e}")

    def _is_circuit_open(self, event_type: str) -> bool:
        """
        Check if circuit breaker is open for event type.

        Args:
            event_type: Type of event

        Returns:
            True if circuit breaker is open
        """
        state = self.circuit_breaker_state.get(event_type, {'failures': 0, 'last_failure': None})

        if state['failures'] >= self.failure_threshold:
            # Check if recovery timeout has passed
            if state['last_failure']:
                time_since_failure = (datetime.now() - state['last_failure']).total_seconds()
                if time_since_failure < self.recovery_timeout:
                    return True  # Circuit still open
                else:
                    # Recovery timeout passed, reset circuit
                    self._reset_circuit_breaker(event_type)
                    return False

        return False

    def _record_delivery_failure(self, event_type: str) -> None:
        """
        Record delivery failure for circuit breaker.

        Args:
            event_type: Type of event that failed
        """
        if event_type not in self.circuit_breaker_state:
            self.circuit_breaker_state[event_type] = {'failures': 0, 'last_failure': None}

        state = self.circuit_breaker_state[event_type]
        state['failures'] += 1
        state['last_failure'] = datetime.now()

    def _reset_circuit_breaker(self, event_type: str) -> None:
        """
        Reset circuit breaker for event type.

        Args:
            event_type: Type of event to reset
        """
        if event_type in self.circuit_breaker_state:
            self.circuit_breaker_state[event_type] = {'failures': 0, 'last_failure': None}

    async def get_dead_letter_queue(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get items from dead letter queue.

        Args:
            limit: Maximum number of items to return

        Returns:
            List of dead letter queue items
        """
        if not self.redis:
            return []

        try:
            items = await self.redis.lrange(self.dead_letter_key, 0, limit - 1)
            return [json.loads(item) for item in items]
        except Exception as e:
            logger.error(f"Failed to get dead letter queue: {e}")
            return []

    async def replay_dead_letter_event(self,
                                      event_id: str,
                                      callback: Optional[Callable] = None) -> bool:
        """
        Replay a specific event from dead letter queue.

        Args:
            event_id: ID of event to replay
            callback: Optional delivery callback

        Returns:
            True if replay successful
        """
        if not self.redis:
            return False

        try:
            # Find event in dead letter queue
            items = await self.redis.lrange(self.dead_letter_key, 0, -1)
            for item_json in items:
                item = json.loads(item_json)
                if item['event'].get('event_id') == event_id:
                    # Remove from dead letter queue
                    await self.redis.lrem(self.dead_letter_key, 1, item_json)

                    # Attempt redelivery
                    return await self.deliver_with_retry(item['event'], callback)

            logger.warning(f"Event {event_id} not found in dead letter queue")
            return False

        except Exception as e:
            logger.error(f"Failed to replay dead letter event: {e}")
            return False

    async def get_delivery_stats(self) -> Dict[str, Any]:
        """
        Get delivery statistics and metrics.

        Returns:
            Dictionary with delivery statistics
        """
        stats = {
            'circuit_breaker_state': self.circuit_breaker_state.copy(),
            'dead_letter_queue_size': 0,
            'retry_delays': self.retry_delays,
            'max_retry_delay': self.max_retry_delay
        }

        if self.redis:
            try:
                stats['dead_letter_queue_size'] = await self.redis.llen(self.dead_letter_key)
            except Exception as e:
                logger.error(f"Failed to get dead letter queue size: {e}")

        return stats