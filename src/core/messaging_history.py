#!/usr/bin/env python3
"""
Message History Service
========================

<!-- SSOT Domain: communication -->

Service for message history logging and persistence.
Extracted from messaging_core.py as part of Phase 2C Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~150 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..utils.swarm_time import format_swarm_timestamp

logger = logging.getLogger(__name__)


class MessageHistoryService:
    """
    Service for message history logging.
    
    Handles:
    - Message logging to repository
    - Delivery status logging
    - Failure logging
    - Metadata serialization for JSON compatibility
    """
    
    def __init__(self, message_repository: Optional[Any] = None):
        """
        Initialize message history service.
        
        Args:
            message_repository: Optional message repository instance
        """
        self.message_repository = message_repository
        logger.debug("MessageHistoryService initialized")
    
    def log_message(
        self,
        message: Any,
        status: str = "sent"
    ) -> bool:
        """
        Log message to history repository.
        
        Args:
            message: UnifiedMessage object
            status: Message status (default: "sent")
            
        Returns:
            True if logged successfully, False otherwise
        """
        if not self.message_repository:
            logger.debug("MessageRepository not available - history logging skipped")
            return False
        
        try:
            # Serialize metadata to ensure JSON compatibility
            metadata_serialized = self._serialize_metadata(
                message.metadata
            ) if message.metadata else {}
            
            message_dict = {
                "from": message.sender,
                "to": message.recipient,
                "content": (
                    message.content[:200] + "..."
                    if len(message.content) > 200
                    else message.content
                ),
                "content_length": len(message.content),
                "message_type": (
                    message.message_type.value
                    if hasattr(message.message_type, "value")
                    else str(message.message_type)
                ),
                "priority": (
                    message.priority.value
                    if hasattr(message.priority, "value")
                    else str(message.priority)
                ),
                "tags": [
                    tag.value if hasattr(tag, "value") else str(tag)
                    for tag in message.tags
                ],
                "metadata": metadata_serialized,
                "timestamp": format_swarm_timestamp(),
                "status": status,
            }
            
            self.message_repository.save_message(message_dict)
            logger.debug(
                f"✅ Message logged to history: {message.sender} → {message.recipient}"
            )
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to log message to history: {e}")
            return False
    
    def log_delivery_status(
        self,
        message: Any,
        status: str = "delivered"
    ) -> bool:
        """
        Log delivery status for message.
        
        Args:
            message: UnifiedMessage object
            status: Delivery status (default: "delivered")
            
        Returns:
            True if logged successfully, False otherwise
        """
        if not self.message_repository:
            return False
        
        try:
            metadata_serialized = self._serialize_metadata(
                message.metadata
            ) if message.metadata else {}
            
            message_dict = {
                "from": message.sender,
                "to": message.recipient,
                "content": (
                    message.content[:200] + "..."
                    if len(message.content) > 200
                    else message.content
                ),
                "content_length": len(message.content),
                "message_type": (
                    message.message_type.value
                    if hasattr(message.message_type, "value")
                    else str(message.message_type)
                ),
                "priority": (
                    message.priority.value
                    if hasattr(message.priority, "value")
                    else str(message.priority)
                ),
                "tags": [
                    tag.value if hasattr(tag, "value") else str(tag)
                    for tag in message.tags
                ],
                "metadata": metadata_serialized,
                "timestamp": format_swarm_timestamp(),
                "status": status,
            }
            
            self.message_repository.save_message(message_dict)
            logger.debug(
                f"✅ Delivery status logged: {message.sender} → {message.recipient}"
            )
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to log delivery status: {e}")
            return False
    
    def log_failure(
        self,
        message: Any,
        error: Exception
    ) -> bool:
        """
        Log message failure to history.
        
        Args:
            message: UnifiedMessage object
            error: Exception that caused failure
            
        Returns:
            True if logged successfully, False otherwise
        """
        if not self.message_repository:
            return False
        
        try:
            history_entry = {
                "from": message.sender,
                "to": message.recipient,
                "content": message.content[:500],
                "timestamp": message.timestamp,
                "status": "FAILED",
                "error": str(error)[:200],
            }
            self.message_repository.save_message(history_entry)
            return True
        except Exception:
            # Non-critical failure logging
            return False
    
    def _serialize_metadata(self, metadata: Any) -> Any:
        """
        Recursively serialize metadata values for JSON compatibility.
        
        Args:
            metadata: Metadata value (dict, list, or primitive)
            
        Returns:
            Serialized metadata
        """
        if isinstance(metadata, datetime):
            return metadata.isoformat()
        elif isinstance(metadata, dict):
            return {
                k: self._serialize_metadata(v)
                for k, v in metadata.items()
            }
        elif isinstance(metadata, (list, tuple)):
            return [self._serialize_metadata(item) for item in metadata]
        elif hasattr(metadata, '__dict__'):
            return str(metadata)
        else:
            return metadata

