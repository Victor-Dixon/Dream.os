#!/usr/bin/env python3
"""
Multi-Agent Request Validator - Blocks Messaging Until Response

<!-- SSOT Domain: infrastructure -->

================================================================

Validates that agents have responded to pending multi-agent requests
before allowing them to send other messages.

If agent has pending request, shows the message in validation error
so they can respond even if they haven't received it from Cursor queue yet.

Author: Agent-4 (Captain) - Autonomous Implementation
Date: 2025-11-27
Status: 🚀 ACTIVE - Ensuring Response Compliance
"""

from __future__ import annotations

import logging
from typing import Optional
from datetime import datetime

from .multi_agent_responder import get_multi_agent_responder, ResponseStatus

logger = logging.getLogger(__name__)


class MultiAgentRequestValidator:
    """Validates agents have responded to pending multi-agent requests."""
    
    def __init__(self):
        """Initialize validator."""
        self.responder = get_multi_agent_responder()
    
    def check_pending_request(self, agent_id: str) -> Optional[dict]:
        """
        Check if agent has pending multi-agent request.
        
        Args:
            agent_id: Agent ID to check
            
        Returns:
            Dictionary with pending request info, or None if no pending request
        """
        try:
            # Get all active collectors
            with self.responder.lock:
                collectors = self.responder.collectors.values()
            
            # Find collectors where this agent is a recipient and hasn't responded
            for collector in collectors:
                if collector.status in [ResponseStatus.PENDING, ResponseStatus.COLLECTING]:
                    if agent_id in collector.recipients:
                        # Check if agent has responded
                        if agent_id not in collector.responses:
                            # Agent has pending request!
                            return {
                                "collector_id": collector.collector_id,
                                "request_id": collector.request_id,
                                "sender": collector.sender,
                                "original_message": collector.original_message,
                                "recipient_count": len(collector.recipients),
                                "responses_received": collector.get_response_count(),
                                "timeout_seconds": collector.timeout_seconds,
                                "created_at": collector.created_at,
                                "is_pending": True
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking pending request for {agent_id}: {e}")
            return None
    
    def validate_agent_can_send_message(
        self,
        agent_id: str,
        target_recipient: Optional[str] = None,
        message_content: Optional[str] = None
    ) -> tuple[bool, Optional[str], Optional[dict]]:
        """
        Validate agent can send message (no pending multi-agent requests).
        
        Args:
            agent_id: Agent trying to send message
            target_recipient: Optional recipient (allow if responding to request sender)
            message_content: Optional message content (for auto-detection)
            
        Returns:
            Tuple of (can_send: bool, error_message: Optional[str], pending_info: Optional[dict])
            If can_send is False, error_message contains the pending request details
            pending_info contains the pending request data if available
        """
        pending = self.check_pending_request(agent_id)
        
        if not pending:
            # No pending request, agent can send
            return True, None, None
        
        # Agent has pending request
        # Allow if they're responding to the request sender
        if target_recipient and target_recipient == pending["sender"]:
            # They're responding to the request sender, allow it
            # Return pending info so system can auto-route to collector
            return True, None, pending
        
        # Block the message and show pending request
        error_message = self._format_pending_request_error(agent_id, pending)
        return False, error_message, pending
    
    def _format_pending_request_error(self, agent_id: str, pending: dict) -> str:
        """Format error message showing pending request."""
        elapsed = (datetime.now() - pending["created_at"]).total_seconds()
        elapsed_minutes = int(elapsed // 60)
        
        return f"""❌ **MESSAGING BLOCKED** - Pending Multi-Agent Request

**Agent**: {agent_id}
**Status**: You have a pending multi-agent request that requires your response.

---

## 📋 **PENDING REQUEST DETAILS**

**From**: {pending["sender"]}
**Request ID**: `{pending["request_id"]}`
**Collector ID**: `{pending["collector_id"]}`
**Created**: {pending["created_at"].strftime('%Y-%m-%d %H:%M:%S')}
**Elapsed**: {elapsed_minutes} minutes
**Responses Received**: {pending["responses_received"]}/{pending["recipient_count"]}
**Timeout**: {pending["timeout_seconds"] // 60} minutes

---

## 📨 **ORIGINAL MESSAGE** (Respond to this)

{pending["original_message"]}

---

## ✅ **HOW TO RESPOND**

1. **Respond to the pending request above** (even if you haven't received it in Cursor queue yet)
2. Your response will be collected and combined with other agents
3. Once you respond, you can send other messages normally

**To respond, send your message to**: `{pending["sender"]}`

**Note**: This message is shown here so you can respond even if it hasn't appeared in your Cursor queue yet!

🐝 WE. ARE. SWARM. ⚡🔥"""
    
    def get_pending_request_message(self, agent_id: str) -> Optional[str]:
        """
        Get the pending request message for an agent.
        
        Useful for showing in type hints or UI.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Formatted pending request message, or None if no pending request
        """
        pending = self.check_pending_request(agent_id)
        if not pending:
            return None
        
        return self._format_pending_request_error(agent_id, pending)


# Global instance
_validator_instance: Optional[MultiAgentRequestValidator] = None


def get_multi_agent_validator() -> MultiAgentRequestValidator:
    """Get global multi-agent request validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = MultiAgentRequestValidator()
    return _validator_instance

