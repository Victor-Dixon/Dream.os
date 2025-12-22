#!/usr/bin/env python3
"""
Queue Repository Interface - Messaging Infrastructure
=====================================================

<!-- SSOT Domain: integration -->

Interface definition for queue repository operations.
Abstracts queue operations for testability and flexibility.

V2 Compliance | Author: Agent-1 | Date: 2025-12-22
"""

from __future__ import annotations

from typing import List, Protocol, Optional, Dict, Any


class IQueueRepository(Protocol):
    """Interface for queue repository operations."""
    
    def enqueue(self, message: Dict[str, Any]) -> str:
        """
        Enqueue a message and return queue ID.
        
        Args:
            message: Message dictionary with recipient, content, sender, category, etc.
            
        Returns:
            queue_id: Unique identifier for the queued message
        """
        ...
    
    def dequeue(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """
        Dequeue messages for processing.
        
        Args:
            batch_size: Maximum number of messages to dequeue
            
        Returns:
            List of message dictionaries
        """
        ...
    
    def mark_delivered(self, queue_id: str) -> bool:
        """
        Mark a message as successfully delivered.
        
        Args:
            queue_id: Queue identifier
            
        Returns:
            True if marked successfully
        """
        ...
    
    def mark_failed(self, queue_id: str, error: str) -> bool:
        """
        Mark a message as failed with error.
        
        Args:
            queue_id: Queue identifier
            error: Error message or description
            
        Returns:
            True if marked successfully
        """
        ...
    
    def get_status(self, queue_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a queued message.
        
        Args:
            queue_id: Queue identifier
            
        Returns:
            Status dictionary or None if not found
        """
        ...
    
    def resend_failed_messages(self) -> int:
        """
        Reset failed messages to PENDING for retry.
        
        Returns:
            Number of messages reset
        """
        ...

