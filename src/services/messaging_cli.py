#!/usr/bin/env python3
"""
🐝 UNIFIED MESSAGING CLI - SWARM COMMAND CENTER
==============================================

<!-- SSOT Domain: communication -->

V2 Compliance: Refactored to <300 lines
SOLID Principles: Single Responsibility, Open-Closed
SSOT: A2A Coordination Protocol is the single source of truth for agent communication

⚠️  DEPRECATION NOTICE: Legacy messaging methods are deprecated.
   Use --category a2a --sender Agent-X for all agent-to-agent communication.
   This ensures bilateral coordination protocol compliance and force multiplication.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
Updated: Agent-1 - Integration & Core Systems (A2A SSOT Implementation)
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
    handle_robinhood_stats,
    handle_save,
    handle_start_agents,
    handle_survey,
)

# V3 Enhanced imports
try:
    from src.services.messaging_cli_handlers import (
        handle_verify_delivery,
        handle_clean_queue,
        handle_reset_stuck,
        handle_queue_stats,
        handle_health_check,
        handle_process_workspaces,
        handle_archive_old,
    )
    V3_HANDLERS_AVAILABLE = True
except ImportError:
    V3_HANDLERS_AVAILABLE = False

# Import task handler with guard to handle missing dependencies gracefully
try:
    from .unified_cli_handlers import TaskHandler

    TASK_HANDLER_AVAILABLE = True
except ImportError:
    # Task handler has dependencies that may not be available
    # This is expected - task system is optional
    TaskHandler = None
    TASK_HANDLER_AVAILABLE = False

# Import hard onboarding handler
try:
    from src.services.unified_onboarding_handlers import HardOnboardingHandler

    HARD_ONBOARDING_HANDLER_AVAILABLE = True
except ImportError:
    HardOnboardingHandler = None
    HARD_ONBOARDING_HANDLER_AVAILABLE = False

# Import soft onboarding handler
try:
    from src.services.unified_onboarding_handlers import SoftOnboardingHandler

    SOFT_ONBOARDING_HANDLER_AVAILABLE = True
except ImportError:
    SoftOnboardingHandler = None
    SOFT_ONBOARDING_HANDLER_AVAILABLE = False

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

    def _send_simple_s2a(self, agent_id: str, body: str, tags: list[str]):
        """Send a simple S2A message via messaging bus."""
        send_message(
            recipient=agent_id,
            content=body,
            category='s2a',
            sender='SYSTEM',
            tags=tags,
        )
        logger.info(f"✅ Sent onboarding message to {agent_id} via lite pathway")
        return 0

    def _ensure_queue_processor_running(self) -> None:
        """Ensure the message queue processor is running, start it if not."""
        try:
            # Check if processor is already running
            import subprocess
            result = subprocess.run(['python', '-c', 'import psutil; print("available")'],
                                  capture_output=True, timeout=2, text=True)
            psutil_available = result.returncode == 0

            if psutil_available:
                import psutil
                processor_running = any('message_queue_processor' in ' '.join(proc.info.get('cmdline', []))
                                      for proc in psutil.process_iter(['cmdline']))

                if not processor_running:
                    print("🔄 Queue processor not running - starting automatically...")
                    # Start processor in background
                    import os
                    if os.name == 'nt':  # Windows
                        subprocess.Popen(['python', '-c',
                                        'from src.core.message_queue_processor.core.processor import main; main()'],
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                    else:  # Unix-like
                        subprocess.Popen(['python', '-c',
                                        'from src.core.message_queue_processor.core.processor import main; main()'],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    print("✅ Queue processor started in background")
                else:
                    logger.debug("Queue processor already running")
            else:
                logger.debug("Cannot check processor status (psutil not available)")

        except Exception as e:
            logger.warning(f"Could not check/start queue processor: {e}")

    def _handle_soft_onboard_lite(self, agent_id: str) -> int:
        """Handle --soft-onboard-lite flag: send template-based soft onboarding message."""
        from uuid import uuid4
        from datetime import datetime
        from pathlib import Path
        t_path = Path('src/services/onboarding/soft/templates/soft_onboard_template.md')
        if t_path.exists():
            templ = t_path.read_text(encoding='utf-8')
            body = (
                templ.replace('{{AGENT}}', agent_id)
                .replace('{{UUID}}', str(uuid4()))
                .replace('{{TIMESTAMP}}', datetime.utcnow().isoformat())
            )
        else:
            # Fallback to default message constants
            from src.services.onboarding.soft.default_message import get_default_soft_onboarding_message
            ctx, actions = get_default_soft_onboarding_message(agent_id)
            body = (
                f"[HEADER] S2A ONBOARDING (SOFT)\nFrom: SYSTEM\nTo: {agent_id}\n"
                f"Priority: regular\nMessage ID: {uuid4()}\nTimestamp: {datetime.utcnow().isoformat()}\n\n"
                f"{ctx}\n\n{actions}"
            )
        return self._send_simple_s2a(agent_id, body, ['onboarding'])

    def _handle_hard_onboard_lite(self, agent_id: str) -> int:
        """Handle --hard-onboard-lite flag: send template-based hard onboarding message."""
        from uuid import uuid4
        from datetime import datetime
        from pathlib import Path
        t_path = Path('src/services/onboarding/hard/templates/hard_onboard_template.md')
        if t_path.exists():
            templ = t_path.read_text(encoding='utf-8')
            body = (
                templ.replace('{{AGENT}}', agent_id)
                .replace('{{UUID}}', str(uuid4()))
                .replace('{{TIMESTAMP}}', datetime.utcnow().isoformat())
            )
        else:
            from src.services.onboarding.hard.default_message import get_default_hard_onboarding_message
            ctx, actions = get_default_hard_onboarding_message(agent_id)
            body = (
                f"[HEADER] S2A ONBOARDING (HARD)\nFrom: SYSTEM\nTo: {agent_id}\n"
                f"Priority: regular\nMessage ID: {uuid4()}\nTimestamp: {datetime.utcnow().isoformat()}\n\n"
                f"{ctx}\n\n{actions}"
            )
        return self._send_simple_s2a(agent_id, body, ['onboarding','hard'])

    def __init__(self):
        self.parser = create_messaging_parser()
        self.task_handler = TaskHandler() if TASK_HANDLER_AVAILABLE else None
        self.hard_onboarding_handler = (
            HardOnboardingHandler() if HARD_ONBOARDING_HANDLER_AVAILABLE else None
        )
        self.soft_onboarding_handler = (
            SoftOnboardingHandler() if SOFT_ONBOARDING_HANDLER_AVAILABLE else None
        )

    def execute(self, args=None):
        """Execute CLI command based on arguments."""
        if not MESSAGING_AVAILABLE:
            return 1

        parsed_args = self.parser.parse_args(args)

        # Lite onboarding shortcuts (template render only) - check FIRST before handlers
        if getattr(parsed_args, 'soft_onboard_lite', None):
            return self._handle_soft_onboard_lite(parsed_args.soft_onboard_lite)
        if getattr(parsed_args, 'hard_onboard_lite', None):
            return self._handle_hard_onboard_lite(parsed_args.hard_onboard_lite)

        try:
            # Check if soft onboarding handler can handle this request
            if (
                SOFT_ONBOARDING_HANDLER_AVAILABLE
                and self.soft_onboarding_handler
                and self.soft_onboarding_handler.can_handle(parsed_args)
            ):
                self.soft_onboarding_handler.handle(parsed_args)
                return self.soft_onboarding_handler.exit_code
            # Check if hard onboarding handler can handle this request
            elif (
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
                # Check if queue processor is running and start it if needed
                self._ensure_queue_processor_running()
                return handle_message(parsed_args, self.parser)
            elif parsed_args.survey_coordination:
                return handle_survey()
            elif parsed_args.consolidation_coordination:
                return handle_consolidation(parsed_args)
            elif parsed_args.coordinates:
                return handle_coordinates()
            elif parsed_args.delivery_status:
                return handle_delivery_status(parsed_args, self.parser)
            elif parsed_args.start:
                return handle_start_agents(parsed_args)
            elif parsed_args.save:
                return handle_save(parsed_args, self.parser)
            elif parsed_args.leaderboard:
                return handle_leaderboard()
            elif parsed_args.robinhood_stats:
                # Handle Robinhood statistics command
                return handle_robinhood_stats()
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
            # V3 Enhanced Messaging Features
            elif parsed_args.verify_delivery:
                return handle_verify_delivery(parsed_args)
            elif parsed_args.clean_queue:
                return handle_clean_queue(parsed_args)
            elif parsed_args.reset_stuck:
                return handle_reset_stuck(parsed_args)
            elif parsed_args.queue_stats:
                return handle_queue_stats(parsed_args)
            elif parsed_args.health_check:
                return handle_health_check(parsed_args)
            elif parsed_args.process_workspaces:
                return handle_process_workspaces(parsed_args)
            elif parsed_args.archive_old:
                return handle_archive_old(parsed_args)
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
