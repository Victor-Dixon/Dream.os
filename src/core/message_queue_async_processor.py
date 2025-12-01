#!/usr/bin/env python3
"""
Async Queue Processor - V2 Compliance Refactor
==============================================

Asynchronous queue processor extracted from message_queue.py for V2 compliance.

V2 Compliance:
- File: <400 lines ✅
- Class: <200 lines ✅
- Functions: <30 lines ✅

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-01-27
License: MIT
"""

import asyncio
from typing import Any, Callable, Optional

from .message_queue_interfaces import IMessageQueue, IQueueProcessor, IMessageQueueLogger


class AsyncQueueProcessor(IQueueProcessor):
    """SOLID-compliant asynchronous queue processor.

    Processes queued messages with retry logic and error handling.
    Follows Single Responsibility Principle with focused processing logic.
    """

    def __init__(
        self,
        queue: IMessageQueue,
        delivery_callback: Callable[[Any], bool],
        logger: Optional[IMessageQueueLogger] = None
    ):
        """Initialize queue processor with dependency injection."""
        self.queue = queue
        self.delivery_callback = delivery_callback
        self.logger = logger
        self.running = False
        self.last_cleanup = 0.0

    async def start_processing(self, interval: float = 5.0) -> None:
        """Start continuous queue processing."""
        self.running = True
        if self.logger:
            self.logger.info("Queue processor started")

        while self.running:
            try:
                await self.process_batch()
                await self._cleanup_if_needed(interval)
                await asyncio.sleep(interval)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Queue processing error: {e}")
                await asyncio.sleep(interval)

    def stop_processing(self) -> None:
        """Stop queue processing."""
        self.running = False
        if self.logger:
            self.logger.info("Queue processor stopped")

    async def process_batch(self) -> None:
        """Process a batch of queued messages."""
        entries = self.queue.dequeue()

        for entry in entries:
            try:
                message = getattr(entry, 'message', None)
                queue_id = getattr(entry, 'queue_id', '')

                if message is None:
                    if self.logger:
                        self.logger.warning(f"Entry missing message: {queue_id}")
                    continue

                success = self.delivery_callback(message)

                if success:
                    self.queue.mark_delivered(queue_id)
                else:
                    self.queue.mark_failed(
                        queue_id, 
                        "Delivery callback returned False"
                    )

            except Exception as e:
                queue_id = getattr(entry, 'queue_id', 'unknown')
                self.queue.mark_failed(queue_id, str(e))

    async def _cleanup_if_needed(self, interval: float) -> None:
        """Perform cleanup if interval has passed."""
        import time
        now = time.time()
        cleanup_interval = getattr(
            self.queue.config, 
            'cleanup_interval', 
            3600
        )

        if now - self.last_cleanup >= cleanup_interval:
            expired_count = self.queue.cleanup_expired()
            if expired_count > 0 and self.logger:
                self.logger.info(
                    f"Cleanup completed: {expired_count} expired entries removed"
                )
            self.last_cleanup = now


# Backward compatibility alias
QueueProcessor = AsyncQueueProcessor





