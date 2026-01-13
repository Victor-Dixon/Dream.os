#!/usr/bin/env python3
"""
Template Resolution Service
============================

<!-- SSOT Domain: communication -->

Service for template resolution logic, including channel and role-based resolution.
Extracted from messaging_core.py as part of Phase 2C Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~100 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TemplateResolutionService:
    """
    Service for template resolution logic.
    
    Handles:
    - Channel-based template resolution
    - Role-based template resolution
    - Template policy loading
    """
    
    def __init__(self):
        """Initialize template resolution service."""
        logger.debug("TemplateResolutionService initialized")
    
    def resolve_template(
        self,
        message_metadata: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Resolve template for message based on metadata.
        
        Uses channel-based resolution first, then falls back to role-based resolution.
        
        Args:
            message_metadata: Message metadata dict
            
        Returns:
            Resolved template name or None
        """
        if not message_metadata:
            return None
        
        # Check if template already specified
        template = message_metadata.get("template")
        if template:
            return template
        
        # Try to load template policy
        try:
            from ..services.messaging.policy_loader import (
                load_template_policy,
                resolve_template_by_channel,
                resolve_template_by_roles,
            )
        except Exception:
            # Policy loader not available
            logger.debug("Template policy loader not available")
            return None
        
        # Get channel and roles from metadata
        channel = message_metadata.get("channel", "standard")
        sender_role = message_metadata.get("sender_role", "AGENT")
        receiver_role = message_metadata.get("receiver_role", "AGENT")
        
        # Load policy
        policy = load_template_policy()
        if not policy:
            return None
        
        # Channel overrides first
        if channel in ("onboarding", "passdown", "standard"):
            template = resolve_template_by_channel(policy, channel)
        
        # If not forced by channel, resolve by roles
        if not template or template == "compact":
            template = resolve_template_by_roles(
                policy, str(sender_role), str(receiver_role)
            )
        
        return template
    
    def apply_template_to_message(
        self,
        message_metadata: Dict[str, Any]
    ) -> None:
        """
        Apply resolved template to message metadata.
        
        Args:
            message_metadata: Message metadata dict (modified in place)
        """
        template = self.resolve_template(message_metadata)
        if template:
            message_metadata["template"] = template

