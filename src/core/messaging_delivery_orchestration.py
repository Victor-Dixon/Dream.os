#!/usr/bin/env python3
"""
Message Delivery Orchestration Service
========================================

<!-- SSOT Domain: communication -->

Service for message delivery orchestration and fallback queuing.
Extracted from messaging_core.py as part of Phase 2C Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~120 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class MessageDeliveryOrchestrationService:
    """
    Service for message delivery orchestration.
    
    Handles:
    - Delivery service coordination
    - Fallback queuing on delivery failure
    - Queue management
    """
    
    def __init__(self, delivery_service: Optional[Any] = None):
        """
        Initialize delivery orchestration service.
        
        Args:
            delivery_service: Optional delivery service instance
        """
        self.delivery_service = delivery_service
        logger.debug("MessageDeliveryOrchestrationService initialized")
    
    def orchestrate_delivery(
        self,
        message: Any
    ) -> bool:
        """
        Orchestrate message delivery with fallback queuing.
        
        Attempts direct delivery first, then queues if delivery fails.
        
        Args:
            message: UnifiedMessage object
            
        Returns:
            True if message was handled (delivered or queued), False otherwise
        """
        if self.delivery_service:
            success = self.delivery_service.send_message(message)
            
            if success:
                return True
            
            # Delivery failed - try to queue message
            return self._queue_message_on_failure(message)
        else:
            # No delivery service - try to queue message
            return self._queue_message_on_failure(message)
    
    def _queue_message_on_failure(
        self,
        message: Any
    ) -> bool:
        """
        Queue message for later processing when delivery fails.
        
        Args:
            message: UnifiedMessage object
            
        Returns:
            True if queued successfully, False otherwise
        """
        try:
            from .message_queue import MessageQueue
            queue = MessageQueue()
            queue_id = queue.enqueue(message)
            
            logger.info(
                f"📬 Message queued for later processing: {queue_id} "
                f"({message.sender} → {message.recipient})"
            )
            return True
            
        except Exception as queue_error:
            logger.error(
                f"❌ Failed to queue message after delivery failure: {queue_error}"
            )
            return False
    
    def should_use_delivery_service(self) -> bool:
        """
        Check if delivery service is available.
        
        Returns:
            True if delivery service is available, False otherwise
        """
        return self.delivery_service is not None

