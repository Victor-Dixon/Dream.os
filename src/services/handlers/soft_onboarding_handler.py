"""
Soft Onboarding Handler - V2 Compliant Module
=============================================

Handles soft onboarding commands for messaging CLI.
Integrates with soft_onboarding_service for 6-step protocol.

V2 Compliance: < 300 lines, single responsibility
Migrated to BaseService for consolidated initialization and error handling.

<!-- SSOT Domain: integration -->
"""

import logging
from pathlib import Path

from ...core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class SoftOnboardingHandler(BaseService):
    """Handles soft onboarding commands for messaging CLI."""

    def __init__(self):
        """Initialize soft onboarding handler."""
        super().__init__("SoftOnboardingHandler")
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return hasattr(args, "soft_onboarding") and args.soft_onboarding

    def handle(self, args) -> bool:
        """Handle soft onboarding commands."""
        try:
            from ..soft_onboarding_service import (
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
            message = args.message
            if args.onboarding_file:
                try:
                    message_file = Path(args.onboarding_file)
                    if not message_file.exists():
                        logger.error(f"❌ Onboarding file not found: {args.onboarding_file}")
                        self.exit_code = 1
                        return True
                    message = message_file.read_text(encoding="utf-8")
                    logger.info(f"📄 Loaded onboarding message from {args.onboarding_file}")
                except Exception as e:
                    logger.error(f"❌ Failed to read onboarding file: {e}")
                    self.exit_code = 1
                    return True
            # If no message provided, use None to trigger default message
            if not message:
                logger.info("📝 No message provided - using default S2A SOFT_ONBOARDING message")
                message = None

            # AUTONOMY: No confirmation required - Captain's directive is authorization
            logger.info(f"🚀 SOFT ONBOARDING AUTHORIZED for {args.agent}")
            logger.info("  Protocol: Click chat → Save session → Cleanup → New tab → Navigate → Send message")

            # Handle dry run
            if args.dry_run:
                logger.info("🧪 DRY RUN MODE - No actions will be executed")
                logger.info(f"Would soft onboard: {args.agent}")
                if message:
                    logger.info(f"Message: {message[:100]}...")
                if args.role:
                    logger.info(f"Role: {args.role}")
                self.exit_code = 0
                return True

            # Handle multiple agents if specified
            if hasattr(args, "agents") and args.agents:
                agents_list = [a.strip() for a in args.agents.split(",") if a.strip()]
                if len(agents_list) > 1:
                    # Multiple agents - use soft_onboard_multiple_agents
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

            # Single agent - use soft_onboard_agent
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
        except Exception as e:
            logger.error(f"❌ Soft onboarding handler error: {e}", exc_info=True)
            self.exit_code = 1
            return True

