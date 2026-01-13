#!/usr/bin/env python3
"""
Message Validation Service
============================

<!-- SSOT Domain: communication -->

Service for message validation logic, including multi-agent request validation.
Extracted from messaging_core.py as part of Phase 2C Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~120 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class MessageValidationService:
    """
    Service for message validation logic.
    
    Handles:
    - Multi-agent request validation
    - Recipient availability checking
    - Auto-routing responses to collectors
    """
    
    def __init__(self):
        """Initialize message validation service."""
        logger.debug("MessageValidationService initialized")
    
    def validate_recipient_can_receive(
        self,
        recipient: str,
        sender: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate that recipient can receive messages.
        
        Checks for pending multi-agent requests and blocks if recipient
        has a pending request (unless responding to request sender).
        
        Args:
            recipient: Message recipient agent ID
            sender: Message sender agent ID
            content: Message content
            metadata: Optional metadata dict (will be modified if blocked)
            
        Returns:
            Tuple of (can_send: bool, updated_metadata: Optional[Dict])
            - If blocked, metadata will contain blocked reason and error message
        """
        # Only validate if recipient is an agent (not system/captain)
        if not (recipient.startswith("Agent-") and sender.startswith("Agent-")):
            return True, metadata
        
        try:
            from ..core.multi_agent_request_validator import get_multi_agent_validator
            
            validator = get_multi_agent_validator()
            can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                agent_id=recipient,
                target_recipient=sender,  # Allow if responding to request sender
                message_content=content
            )
            
            if not can_send:
                # Recipient has pending request - block and show error
                logger.warning(
                    f"❌ Message blocked - {recipient} has pending multi-agent request"
                )
                # Store error in metadata for caller to access
                if metadata is None:
                    metadata = {}
                metadata["blocked"] = True
                metadata["blocked_reason"] = "pending_multi_agent_request"
                metadata["blocked_error_message"] = error_message
                return False, metadata
            
            # If responding to request sender, auto-route to collector
            if pending_info and sender == pending_info["sender"]:
                self._auto_route_response(pending_info, recipient, content)
            
            return True, metadata
            
        except ImportError:
            # Validator not available, proceed normally
            logger.debug("Multi-agent validator not available, skipping validation")
            return True, metadata
        except Exception as e:
            logger.debug(f"Error validating recipient: {e}")
            # Continue with normal flow
            return True, metadata
    
    def _auto_route_response(
        self,
        pending_info: Dict[str, Any],
        recipient: str,
        content: str
    ) -> None:
        """
        Auto-route response to collector if responding to request sender.
        
        Args:
            pending_info: Pending request information
            recipient: Response sender agent ID
            content: Response content
        """
        try:
            from ..core.multi_agent_responder import get_multi_agent_responder
            responder = get_multi_agent_responder()
            
            # Auto-submit response to collector
            collector_id = pending_info["collector_id"]
            responder.submit_response(collector_id, recipient, content)
            
            logger.info(
                f"✅ Auto-routed response from {recipient} to collector {collector_id}"
            )
        except Exception as e:
            logger.debug(f"Error auto-routing response: {e}")
            # Continue with normal message send

