"""
Messaging Fallback for Soft Onboarding
=======================================

Fallback messaging operations when PyAutoGUI is unavailable.
Uses messaging system to send cleanup and onboarding messages.

V2 Compliant: < 150 lines
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OnboardingMessagingFallback:
    """Fallback messaging for onboarding when PyAutoGUI unavailable."""
    
    def _get_default_cleanup_message(self) -> str:
        """Get default cleanup/passdown message."""
        return """🎯 SESSION CLEANUP REQUIRED!

Before starting your next session, please complete these tasks:

1. Create/Update passdown.json
2. Create Final Devlog
3. Post Devlog to Discord
4. Update Swarm Brain Database
5. Create a Tool You Wished You Had

Press Enter when complete to proceed to next session onboarding!

📝 Remember: Quality documentation ensures civilization-building!
🐝 WE. ARE. SWARM. ⚡"""
    
    def send_cleanup_via_messaging(self, agent_id: str, custom_message: Optional[str] = None) -> bool:
        """
        Send cleanup via messaging system (S2A template, no-ack).
        
        Args:
            agent_id: Target agent ID
            custom_message: Optional custom cleanup message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from src.services.messaging_infrastructure import MessageCoordinator
            from src.core.messaging_models import (
                MessageCategory,
                UnifiedMessage,
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
            )
            from src.core.messaging_templates import render_message
            
            message = custom_message or self._get_default_cleanup_message()
            msg = UnifiedMessage(
                content=message,
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.WRAPUP],
                category=MessageCategory.S2A,
            )
            
            rendered = render_message(
                msg,
                template_key="PASSDOWN",
                context="Passdown/Cleanup",
                actions=message,
                fallback="If blocked, escalate to Captain with blockers and partial status.",
            )
            
            return MessageCoordinator.send_to_agent(
                agent=agent_id,
                message=rendered,
                priority=UnifiedMessagePriority.REGULAR,
                use_pyautogui=True,
                sender="SYSTEM",
                message_category=MessageCategory.S2A,
            )
        except Exception as e:
            logger.error(f"❌ Failed to send cleanup via messaging: {e}")
            return False
    
    def send_onboarding_via_messaging(self, agent_id: str, message: Optional[str] = None) -> bool:
        """
        Send onboarding via messaging system (S2A SOFT_ONBOARDING template, no-ack).
        
        Args:
            agent_id: Target agent ID
            message: Onboarding message (if provided, used as actions; otherwise uses default)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from src.services.messaging_infrastructure import MessageCoordinator
            from src.core.messaging_models import (
                MessageCategory,
                UnifiedMessage,
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
            )
            from src.core.messaging_templates import render_message
            from .default_message import get_default_soft_onboarding_message
            
            # Use default message if none provided, otherwise use provided message as actions
            if message and message.strip():
                context = "🚀 SOFT ONBOARD - Agent activation initiated."
                actions = message
            else:
                context, actions = get_default_soft_onboarding_message(agent_id)
            
            msg = UnifiedMessage(
                content=actions,  # Content used for message body
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.SYSTEM],  # Use SYSTEM tag for S2A
                category=MessageCategory.S2A,
            )
            
            rendered = render_message(
                msg,
                template_key="SOFT_ONBOARDING",
                context=context,
                actions=actions,
                fallback="If blocked, escalate to Captain.",
            )
            
            return MessageCoordinator.send_to_agent(
                agent=agent_id,
                message=rendered,
                priority=UnifiedMessagePriority.REGULAR,
                use_pyautogui=True,
                sender="SYSTEM",
                message_category=MessageCategory.S2A,
            )
        except Exception as e:
            logger.error(f"❌ Failed to send onboarding via messaging: {e}")
            return False

