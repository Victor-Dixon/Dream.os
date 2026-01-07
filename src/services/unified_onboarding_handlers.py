#!/usr/bin/env python3
"""
Unified Onboarding Handlers V2 - Phase 4 Consolidation
======================================================

PHASE 4 CONSOLIDATION: Consolidated onboarding handler modules
Merged from: handlers/hard_onboarding_handler.py, handlers/soft_onboarding_handler.py,
             onboarding/ directory services and templates

Reduced from 8+ separate onboarding files (~1500+ lines) to 1 consolidated module

Consolidated onboarding handlers for:
- HardOnboardingHandler: 5-step hard onboarding protocol
- SoftOnboardingHandler: 6-step soft onboarding protocol
- Onboarding templates and services integration

Features:
- Unified onboarding interface for both hard and soft protocols
- Consolidated template management and message handling
- Single responsibility principle maintained
- V2 compliance and SSOT integration

V2 Compliance: <600 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: integration -->
"""

import logging
from pathlib import Path
from typing import Optional

from ..core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class UnifiedOnboardingHandler(BaseService):
    """Unified onboarding handler for both hard and soft onboarding protocols.

    PHASE 4 CONSOLIDATION: Migrated from handlers/hard_onboarding_handler.py and handlers/soft_onboarding_handler.py
    Handles both 5-step hard onboarding and 6-step soft onboarding protocols.
    """

    def __init__(self):
        """Initialize unified onboarding handler."""
        super().__init__("UnifiedOnboardingHandler")
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            (hasattr(args, "hard_onboarding") and args.hard_onboarding) or
            (hasattr(args, "soft_onboarding") and args.soft_onboarding)
        )

    def handle(self, args) -> bool:
        """Handle onboarding commands based on type."""
        try:
            if hasattr(args, "hard_onboarding") and args.hard_onboarding:
                return self._handle_hard_onboarding(args)
            elif hasattr(args, "soft_onboarding") and args.soft_onboarding:
                return self._handle_soft_onboarding(args)
            else:
                logger.error("❌ Neither hard nor soft onboarding specified")
                self.exit_code = 1
                return True

        except Exception as e:
            logger.error(f"❌ Unified onboarding handler error: {e}", exc_info=True)
            self.exit_code = 1
            return True

    def _handle_hard_onboarding(self, args) -> bool:
        """Handle hard onboarding commands."""
        try:
            from .hard_onboarding_service import HardOnboardingService

            # Validate required arguments
            if not args.agent:
                logger.error("❌ --agent required for hard onboarding")
                self.exit_code = 1
                return True

            # Load message from file if specified, otherwise use default
            message = self._load_message_from_file(args)

            # AUTONOMY: No confirmation required - Captain's directive is authorization
            logger.info(f"🚨 HARD ONBOARDING AUTHORIZED for {args.agent}")
            logger.info("  Protocol: Clear chat → Execute → New window → Navigate → Send message")

            # Handle dry run
            if getattr(args, 'dry_run', False):
                return self._handle_dry_run(args, message, "hard")

            # Initialize service and execute
            service = HardOnboardingService()
            logger.info(f"🚨 Starting HARD ONBOARDING for {args.agent}")

            success = service.execute_hard_onboarding(
                agent_id=args.agent,
                onboarding_message=message,
                role=getattr(args, 'role', None),
            )

            if success:
                logger.info(f"🎉 Hard onboarding complete for {args.agent}!")
                self.exit_code = 0
            else:
                logger.error(f"❌ Hard onboarding failed for {args.agent}")
                self.exit_code = 1

            return True

        except ImportError as e:
            logger.error(f"❌ Hard onboarding service not available: {e}")
            self.exit_code = 1
            return True

    def _handle_soft_onboarding(self, args) -> bool:
        """Handle soft onboarding commands."""
        try:
            from .soft_onboarding_service import (
                SoftOnboardingService,
                soft_onboard_agent,
                soft_onboard_multiple_agents,
            )

            # Validate required arguments
            if not args.agent:
                logger.error("❌ --agent required for soft onboarding")
                self.exit_code = 1
                return True

            # Load message from file if specified, otherwise use default
            message = self._load_message_from_file(args)

            # AUTONOMY: No confirmation required - Captain's directive is authorization
            logger.info(f"🚀 SOFT ONBOARDING AUTHORIZED for {args.agent}")
            logger.info("  Protocol: Click chat → Save session → Cleanup → New tab → Navigate → Send message")

            # Handle dry run
            if getattr(args, 'dry_run', False):
                return self._handle_dry_run(args, message, "soft")

            # Handle multiple agents if specified
            if hasattr(args, "agents") and args.agents:
                agents_list = [a.strip() for a in args.agents.split(",") if a.strip()]
                if len(agents_list) > 1:
                    return self._handle_multiple_agents_soft_onboarding(
                        agents_list, message, args
                    )

            # Single agent onboarding
            success = soft_onboard_agent(
                agent_id=args.agent,
                message=message,
                role=getattr(args, "role", None),
                custom_cleanup_message=getattr(args, "custom_cleanup_message", None),
            )

            if success:
                logger.info(f"🎉 Soft onboarding complete for {args.agent}!")
                self.exit_code = 0
            else:
                logger.error(f"❌ Soft onboarding failed for {args.agent}")
                self.exit_code = 1

            return True

        except ImportError as e:
            logger.error(f"❌ Soft onboarding service not available: {e}")
            self.exit_code = 1
            return True

    def _handle_multiple_agents_soft_onboarding(self, agents_list, message, args) -> bool:
        """Handle soft onboarding for multiple agents."""
        try:
            from .soft_onboarding_service import soft_onboard_multiple_agents

            agents_tuples = [(agent, message) for agent in agents_list]
            results = soft_onboard_multiple_agents(
                agents_tuples,
                role=getattr(args, "role", None),
                generate_cycle_report=getattr(args, "generate_cycle_report", True),
            )

            # Check if all succeeded
            all_success = all(results.values())
            if all_success:
                logger.info(f"🎉 Soft onboarding complete for all {len(agents_list)} agents!")
                self.exit_code = 0
            else:
                failed = [agent for agent, success in results.items() if not success]
                logger.error(f"❌ Soft onboarding failed for: {', '.join(failed)}")
                self.exit_code = 1

            return True

        except Exception as e:
            logger.error(f"❌ Multiple agents soft onboarding error: {e}")
            self.exit_code = 1
            return True

    def _load_message_from_file(self, args) -> Optional[str]:
        """Load message from file if specified."""
        message = getattr(args, 'message', None)
        onboarding_file = getattr(args, 'onboarding_file', None)

        if onboarding_file:
            try:
                message_file = Path(onboarding_file)
                if not message_file.exists():
                    logger.error(f"❌ Onboarding file not found: {onboarding_file}")
                    self.exit_code = 1
                    return None
                message = message_file.read_text(encoding="utf-8")
                logger.info(f"📄 Loaded onboarding message from {onboarding_file}")
            except Exception as e:
                logger.error(f"❌ Failed to read onboarding file: {e}")
                self.exit_code = 1
                return None

        # If no message provided, use None to trigger default message
        if not message:
            logger.info("📝 No message provided - using default onboarding message")
            message = None

        return message

    def _handle_dry_run(self, args, message, onboarding_type) -> bool:
        """Handle dry run mode for onboarding."""
        logger.info("🧪 DRY RUN MODE - No actions will be executed")
        logger.info(f"Would {onboarding_type} onboard: {args.agent}")
        if message:
            logger.info(f"Message: {message[:100]}...")
        if hasattr(args, 'role') and args.role:
            logger.info(f"Role: {args.role}")
        self.exit_code = 0
        return True


class HardOnboardingHandler(UnifiedOnboardingHandler):
    """Backward compatibility alias for HardOnboardingHandler."""

    def can_handle(self, args) -> bool:
        """Check if this handler can handle hard onboarding."""
        return hasattr(args, "hard_onboarding") and args.hard_onboarding

    def handle(self, args) -> bool:
        """Handle hard onboarding."""
        return self._handle_hard_onboarding(args)


class SoftOnboardingHandler(UnifiedOnboardingHandler):
    """Backward compatibility alias for SoftOnboardingHandler."""

    def can_handle(self, args) -> bool:
        """Check if this handler can handle soft onboarding."""
        return hasattr(args, "soft_onboarding") and args.soft_onboarding

    def handle(self, args) -> bool:
        """Handle soft onboarding."""
        return self._handle_soft_onboarding(args)


# Export all unified handlers
__all__ = [
    "UnifiedOnboardingHandler",
    "HardOnboardingHandler",  # Backward compatibility
    "SoftOnboardingHandler",  # Backward compatibility
]