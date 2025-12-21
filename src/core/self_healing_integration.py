#!/usr/bin/env python3
"""
Self-Healing Integration
========================

External service integrations for agent self-healing:
- Rescue message sending (messaging service)
- Hard onboarding (onboarding service)
- Activity detection integration

<!-- SSOT Domain: infrastructure -->

V2 Compliance: <300 lines | Author: Agent-3 | Date: 2025-12-15
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SelfHealingIntegration:
    """External service integrations for self-healing system."""

    async def send_rescue_message(
        self,
        agent_id: str,
        stall_duration_minutes: float = 0.0
    ) -> bool:
        """Send optimized rescue message to stalled agent.

        Args:
            agent_id: Agent identifier
            stall_duration_minutes: How long agent has been stalled

        Returns:
            True if successful
        """
        try:
            # Use optimized prompt generator
            from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt

            # Generate optimized prompt
            rescue_message = generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=None,  # Will be loaded from status.json
                last_mission=None,  # Will be loaded from status.json
                stall_duration_minutes=stall_duration_minutes
            )

            # Send via messaging service
            try:
                from src.core.messaging_core import send_message
                from src.core.messaging_models_core import (
                    UnifiedMessageType,
                    UnifiedMessagePriority,
                    UnifiedMessageTag
                )

                success = send_message(
                    content=rescue_message,
                    sender="SYSTEM",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                    priority=UnifiedMessagePriority.URGENT,
                    tags=[UnifiedMessageTag.SYSTEM]
                )

                if success:
                    logger.info(
                        f"✅ Optimized rescue message sent to {agent_id}")
                    return True
                else:
                    logger.warning(
                        f"⚠️ Rescue message send failed for {agent_id}")
                    return False
            except ImportError:
                # Fallback to recovery system
                from src.orchestrators.overnight.recovery import RecoverySystem
                recovery = RecoverySystem()
                await recovery._rescue_agent(agent_id)
                return True
        except Exception as e:
            logger.error(f"Error sending rescue message to {agent_id}: {e}")
            return False

    async def hard_onboard_agent(self, agent_id: str) -> bool:
        """Hard onboard agent (complete reset).

        Args:
            agent_id: Agent identifier

        Returns:
            True if successful
        """
        try:
            from src.services.hard_onboarding_service import HardOnboardingService

            service = HardOnboardingService()

            # Get default onboarding message
            onboarding_message = (
                f"[S2A] {agent_id}: System recovery - Hard onboarding initiated. "
                f"Status: ACTIVE_AGENT_MODE. Ready for task assignment."
            )

            success = service.execute_hard_onboarding(
                agent_id=agent_id,
                onboarding_message=onboarding_message,
                role=None  # Use default role
            )

            if success:
                logger.info(f"✅ {agent_id}: Hard onboarding successful")
            else:
                logger.error(f"❌ {agent_id}: Hard onboarding failed")

            return success

        except ImportError as e:
            logger.error(f"Hard onboarding service not available: {e}")
            return False
        except Exception as e:
            logger.error(f"Error hard onboarding {agent_id}: {e}")
            return False
