#!/usr/bin/env python3
"""
🐝 UNIFIED MESSAGING CLI - SWARM COMMAND CENTER
==============================================

<!-- SSOT Domain: communication -->

V2 Compliance: Refactored to <300 lines
SOLID Principles: Single Responsibility, Open-Closed

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
"""

import logging
import sys
from pathlib import Path

from src.services.messaging import (
    create_messaging_parser,
    handle_consolidation,
    handle_coordinates,
    handle_leaderboard,
    handle_message,
    handle_save,
    handle_start_agents,
    handle_survey,
)

# Import task handler with guard to handle missing dependencies gracefully
try:
    from .handlers.task_handler import TaskHandler

    TASK_HANDLER_AVAILABLE = True
except ImportError:
    # Task handler has dependencies that may not be available
    # This is expected - task system is optional
    TaskHandler = None
    TASK_HANDLER_AVAILABLE = False

# Import hard onboarding handler
try:
    from src.services.handlers.hard_onboarding_handler import HardOnboardingHandler

    HARD_ONBOARDING_HANDLER_AVAILABLE = True
except ImportError:
    HardOnboardingHandler = None
    HARD_ONBOARDING_HANDLER_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from src.core.messaging_core import (
        UnifiedMessagePriority,
        UnifiedMessageTag,
        UnifiedMessageType,
        send_message,
    )

    MESSAGING_AVAILABLE = True
except ImportError as e:
    logger.error(f"❌ Messaging system not available: {e}")
    MESSAGING_AVAILABLE = False


class MessagingCLI:
    """Command-line interface for messaging operations."""

    def __init__(self):
        self.parser = create_messaging_parser()
        self.task_handler = TaskHandler() if TASK_HANDLER_AVAILABLE else None
        self.hard_onboarding_handler = (
            HardOnboardingHandler() if HARD_ONBOARDING_HANDLER_AVAILABLE else None
        )

    def execute(self, args=None):
        """Execute CLI command based on arguments."""
        if not MESSAGING_AVAILABLE:
            return 1

        parsed_args = self.parser.parse_args(args)

        try:
            # Check if hard onboarding handler can handle this request
            if (
                HARD_ONBOARDING_HANDLER_AVAILABLE
                and self.hard_onboarding_handler
                and self.hard_onboarding_handler.can_handle(parsed_args)
            ):
                self.hard_onboarding_handler.handle(parsed_args)
                return self.hard_onboarding_handler.exit_code
            # Check if task handler can handle this request (SSOT Blocker Fix - Agent-8)
            elif (
                TASK_HANDLER_AVAILABLE
                and self.task_handler
                and self.task_handler.can_handle(parsed_args)
            ):
                self.task_handler.handle(parsed_args)
                return self.task_handler.exit_code
            elif parsed_args.message or parsed_args.broadcast:
                return handle_message(parsed_args, self.parser)
            elif parsed_args.survey_coordination:
                return handle_survey()
            elif parsed_args.consolidation_coordination:
                return handle_consolidation(parsed_args)
            elif parsed_args.coordinates:
                return handle_coordinates()
            elif parsed_args.start:
                return handle_start_agents(parsed_args)
            elif parsed_args.save:
                return handle_save(parsed_args, self.parser)
            elif parsed_args.leaderboard:
                return handle_leaderboard()
            elif parsed_args.resend_failed:
                # Handle resend failed messages
                from src.core.message_queue import MessageQueue
                queue = MessageQueue()
                count = queue.resend_failed_messages()
                print(f"✅ Reset {count} failed messages to PENDING for retry")
                return 0 if count > 0 else 1
            elif parsed_args.infra_health:
                # Import here to avoid circular imports
                from src.infrastructure.infrastructure_health_monitor import InfrastructureHealthMonitor

                monitor = InfrastructureHealthMonitor()
                result = monitor.perform_full_health_check()
                monitor.print_health_report(result)

                # Return appropriate exit code based on health status
                if result.status == "critical":
                    return 2  # Critical health issues
                elif result.status == "warning":
                    return 1  # Health warnings
                else:
                    return 0  # Healthy
            elif parsed_args.generate_work_resume:
                # Generate work resume for agent
                if not parsed_args.agent:
                    print("❌ ERROR: --agent required for --generate-work-resume")
                    self.parser.print_help()
                    return 1
                
                from src.services.messaging.work_resume_generator import WorkResumeGenerator
                generator = WorkResumeGenerator()
                
                resume = generator.generate_work_resume(
                    parsed_args.agent,
                    include_recent_commits=True,
                    include_coordination=True,
                    include_devlogs=True,
                )
                
                print(resume)
                
                # Save to file if requested
                if parsed_args.save_resume:
                    output_file = generator.save_resume_to_file(parsed_args.agent)
                    print(f"\n✅ Work resume saved to: {output_file}")
                
                return 0
            else:
                self.parser.print_help()
                return 0
        except Exception as e:
            logger.error(f"❌ CLI execution error: {e}")
            return 1


def main() -> int:
    """Main entry point."""
    cli = MessagingCLI()
    return cli.execute()


if __name__ == "__main__":
    exit_code = main()
    print()  # Add line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
    sys.exit(exit_code)
