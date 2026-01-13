#!/usr/bin/env python3
"""
Queue Repository Implementation - Messaging Infrastructure
===========================================================

<!-- SSOT Domain: integration -->

Repository implementation for queue operations.
Implements IQueueRepository interface using MessageQueue.

V2 Compliance | Author: Agent-1 | Date: 2025-12-22
"""

from __future__ import annotations

import logging
from typing import Dict, Any, List, Optional

from src.core.message_queue import MessageQueue
from ..domain.interfaces.queue_repository import IQueueRepository

logger = logging.getLogger(__name__)


class QueueRepository:
    """Repository implementation for queue operations."""
    
    def __init__(self, queue: Optional[MessageQueue] = None):
        """
        Initialize queue repository.
        
        Args:
            queue: MessageQueue instance (creates new if None)
        """
        if queue is None:
            from src.core.message_queue import MessageQueue
            self._queue = MessageQueue()
        else:
            self._queue = queue
    
    def enqueue(self, message: Dict[str, Any]) -> str:
        """
        Enqueue a message and return queue ID.
        
        Args:
            message: Message dictionary with recipient, content, sender, category, etc.
            
        Returns:
            queue_id: Unique identifier for the queued message
        """
        try:
            queue_id = self._queue.enqueue(message)
            logger.debug(f"Message enqueued: {queue_id}")
            return queue_id
        except Exception as e:
            logger.error(f"Failed to enqueue message: {e}")
            raise
    
    def dequeue(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """
        Dequeue messages for processing.
        
        Args:
            batch_size: Maximum number of messages to dequeue
            
        Returns:
            List of message dictionaries (converted from IQueueEntry)
        """
        try:
            # MessageQueue.dequeue() returns List[IQueueEntry]
            entries = self._queue.dequeue(batch_size=batch_size)
            
            # Convert IQueueEntry objects to dictionaries
            result = []
            for entry in entries:
                # Extract message dict and add status/metadata
                entry_dict = {
                    "queue_id": getattr(entry, 'queue_id', ''),
                    "message": getattr(entry, 'message', {}),
                    "status": getattr(entry, 'status', 'PENDING'),
                    "priority_score": getattr(entry, 'priority_score', 0.5),
                    "created_at": getattr(entry, 'created_at', None),
                    "updated_at": getattr(entry, 'updated_at', None),
                    "metadata": getattr(entry, 'metadata', {}),
                }
                result.append(entry_dict)
            
            logger.debug(f"Dequeued {len(result)} messages (batch_size={batch_size})")
            return result
        except Exception as e:
            logger.error(f"Failed to dequeue messages: {e}")
            return []
    
    def mark_delivered(self, queue_id: str) -> bool:
        """
        Mark a message as successfully delivered.
        
        Args:
            queue_id: Queue identifier
            
        Returns:
            True if marked successfully
        """
        try:
            success = self._queue.mark_delivered(queue_id)
            if success:
                logger.debug(f"Message marked as delivered: {queue_id}")
            else:
                logger.warning(f"Failed to mark message as delivered: {queue_id} (entry not found)")
            return success
        except Exception as e:
            logger.error(f"Failed to mark message as delivered: {e}")
            return False
    
    def mark_failed(self, queue_id: str, error: str) -> bool:
        """
        Mark a message as failed with error.
        
        Args:
            queue_id: Queue identifier
            error: Error message or description
            
        Returns:
            True if marked successfully
        """
        try:
            success = self._queue.mark_failed(queue_id, error)
            if success:
                logger.debug(f"Message marked as failed: {queue_id}, error: {error}")
            else:
                logger.warning(f"Failed to mark message as failed: {queue_id} (entry not found)")
            return success
        except Exception as e:
            logger.error(f"Failed to mark message as failed: {e}")
            return False
    
    def get_status(self, queue_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a queued message.
        
        Args:
            queue_id: Queue identifier
            
        Returns:
            Status dictionary with queue_id, status, message, metadata, etc. or None if not found
        """
        try:
            # Access persistence layer to find entry by ID
            entries = self._queue.persistence.load_entries()
            
            # Find entry by queue_id
            for entry in entries:
                if getattr(entry, 'queue_id', '') == queue_id:
                    # Return status dictionary
                    status_dict = {
                        "queue_id": getattr(entry, 'queue_id', ''),
                        "status": getattr(entry, 'status', 'UNKNOWN'),
                        "message": getattr(entry, 'message', {}),
                        "priority_score": getattr(entry, 'priority_score', 0.5),
                        "created_at": getattr(entry, 'created_at', None),
                        "updated_at": getattr(entry, 'updated_at', None),
                        "metadata": getattr(entry, 'metadata', {}),
                    }
                    # Add delivery attempts if available
                    if hasattr(entry, 'delivery_attempts'):
                        status_dict["delivery_attempts"] = entry.delivery_attempts
                    
                    logger.debug(f"Retrieved status for message: {queue_id} (status: {status_dict['status']})")
                    return status_dict
            
            logger.debug(f"Message not found: {queue_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to get message status: {e}")
            return None
    
    def resend_failed_messages(self) -> int:
        """
        Reset failed messages to PENDING for retry.
        
        Returns:
            Number of messages reset
        """
        try:
            count = self._queue.resend_failed_messages()
            logger.info(f"Reset {count} failed messages to PENDING")
            return count
        except Exception as e:
            logger.error(f"Failed to resend failed messages: {e}")
            return 0

