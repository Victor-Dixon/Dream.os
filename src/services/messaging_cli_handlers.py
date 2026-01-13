"""
Messaging CLI Handlers Module
Handles command execution logic

<!-- SSOT Domain: communication -->
"""

import logging
import time

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None


from src.core.coordinate_loader import get_coordinate_loader
from src.core.gamification.autonomous_competition_system import get_competition_system
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)
from src.core.config.timeout_constants import TimeoutConstants

from .messaging_cli_formatters import (
    AGENT_ASSIGNMENTS,
    ASSIGNMENT_MESSAGE_TEMPLATE,
    CONSOLIDATION_MESSAGE_TEMPLATE,
    SURVEY_MESSAGE_TEMPLATE,
)

from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS

# Import V3 enhanced messaging features
try:
    from .messaging.v3 import MessagingV3Processor
    V3_AVAILABLE = True
except ImportError:
    MessagingV3Processor = None
    V3_AVAILABLE = False

logger = logging.getLogger(__name__)


# Stubs for PyAutoGUI messaging now routed through core messaging
def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send a message via PyAutoGUI using unified messaging core."""
    return send_message(
        content=message,
        sender="CAPTAIN",
        recipient=agent_id,
        message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.SYSTEM],
    )


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Alias for send_message_pyautogui to handle onboarding messaging."""
    return send_message_pyautogui(agent_id, message, timeout)


class MessageCoordinator:
    """Unified message coordination system."""

    @staticmethod
    def send_to_agent(
        agent: str, message: str, priority=UnifiedMessagePriority.REGULAR, use_pyautogui=False
    ):
        try:
            # Use unified messaging system (PyAutoGUI delivery)
            return send_message(
                content=message,
                sender="CAPTAIN",
                recipient=agent,
                message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
                priority=priority,
                tags=[UnifiedMessageTag.SYSTEM],
            )
        except Exception:
            return False

    @staticmethod
    def broadcast_to_all(message: str, priority=UnifiedMessagePriority.REGULAR):
        return sum(
            1
            for agent in AGENT_LIST
            if send_message(
                content=message,
                sender="CAPTAIN",
                recipient=agent,
                message_type=UnifiedMessageType.BROADCAST,
                priority=priority,
                tags=[UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION],
            )
        )

    @staticmethod
    def coordinate_survey():
        logger.info("🐝 INITIATING SWARM SURVEY COORDINATION...")
        success_count = MessageCoordinator.broadcast_to_all(
            SURVEY_MESSAGE_TEMPLATE, UnifiedMessagePriority.URGENT
        )
        if success_count > 0:
            for agent, assignment in AGENT_ASSIGNMENTS.items():
                msg = ASSIGNMENT_MESSAGE_TEMPLATE.format(agent=agent, assignment=assignment)
                send_message_pyautogui(agent, msg, timeout=TimeoutConstants.HTTP_MEDIUM)
        return success_count

    # Consolidation coordination moved to messaging_infrastructure.py (SSOT)
    # Import from MessageCoordinator.coordinate_consolidation instead
    @staticmethod
    def coordinate_consolidation(batch: str, status: str):
        """Delegate to MessageCoordinator.coordinate_consolidation (SSOT)."""
        from .messaging_infrastructure import MessageCoordinator
        return MessageCoordinator.coordinate_consolidation(batch, status)


def handle_message(args, parser):
    """Handle message sending."""
    if not args.message and not args.broadcast:
        return 1
    # Normalize "normal" to "regular" for consistency
    normalized_priority = "regular" if args.priority == "normal" else args.priority
    
    priority = (
        UnifiedMessagePriority.URGENT
        if normalized_priority == "urgent"
        else UnifiedMessagePriority.REGULAR
    )
    if args.broadcast:
        from src.core.agent_mode_manager import get_active_agents
        active_count = len(get_active_agents())
        success = MessageCoordinator.broadcast_to_all(args.message, priority)
        logger.info(
            f"📢 Broadcast successful to {success}/{active_count} agents"
            if success > 0
            else "❌ Broadcast failed"
        )
        return 0 if success > 0 else 1
    elif args.agent:
        success = MessageCoordinator.send_to_agent(
            args.agent, args.message, priority, args.pyautogui
        )
        return 0 if success else 1
    return 1


def handle_survey():
    """Handle survey coordination."""
    success = MessageCoordinator.coordinate_survey()
    return 0 if success > 0 else 1


def handle_consolidation(args):
    """Handle consolidation coordination."""
    if not (args.consolidation_batch and args.consolidation_status):
        return 1
    success = MessageCoordinator.coordinate_consolidation(
        args.consolidation_batch, args.consolidation_status
    )
    return 0 if success > 0 else 1


def handle_coordinates():
    """Display agent coordinates."""
    try:
        coord_loader = get_coordinate_loader()
        agents = coord_loader.get_all_agents()
        if not agents:
            return 1
        print("\n🐝 AGENT COORDINATES & CONFIGURATION\n" + "=" * 50)
        for agent_id in sorted(agents):
            try:
                coords = coord_loader.get_chat_coordinates(agent_id)
                desc = coord_loader.get_agent_description(agent_id) or "No description"
                status = "✅ ACTIVE" if coord_loader.is_agent_active(agent_id) else "❌ INACTIVE"
                coord_info = (
                    f"🤖 {agent_id}\n   📍 Coordinates: {coords}\n"
                    f"   📝 {desc}\n   🔄 {status}\n"
                )
                print(coord_info)
            except Exception as e:
                logger.debug(f"Could not display {agent_id}: {e}")
        print("🎯 COORDINATE SYSTEM READY FOR SWARM COORDINATION!")
        return 0
    except Exception:
        return 1


def handle_start_agents(args):
    """Send start message to specified agents via onboarding coordinates (mode-aware)."""
    from src.core.agent_mode_manager import get_active_agents, is_agent_active
    
    # Get active agents for current mode
    active_agents_list = get_active_agents()
    
    valid_agents = []
    for num in args.start:
        agent_id = f"Agent-{num}"
        if not is_agent_active(agent_id):
            logger.warning(f"⚠️ Agent {agent_id} is not active in current mode (skipping)")
            continue
        valid_agents.append(agent_id)

    if not valid_agents:
        logger.error(f"❌ No valid active agents specified. Active agents: {', '.join(active_agents_list)}")
        return 1

    start_msg = "🚀 START: Begin your assigned work cycle. Review your workspace and inbox."
    success_count = 0

    logger.info(f"🚀 Starting {len(valid_agents)} active agent(s) via onboarding coordinates...")
    logger.info(f"📋 Mode-aware: Active agents: {', '.join(active_agents_list)}")
    for agent_id in valid_agents:
        try:
            if send_message_to_onboarding_coords(agent_id, start_msg, timeout=TimeoutConstants.HTTP_DEFAULT):
                success_count += 1
                logger.info(f"  ✅ {agent_id} (onboarding coordinates)")
            else:
                logger.warning(f"  ❌ {agent_id}")
        except Exception as e:
            logger.error(f"  ❌ {agent_id}: {e}")

    logger.info(
        f"✅ Started {success_count}/{len(valid_agents)} agents " "via onboarding coordinates"
    )
    return 0 if success_count > 0 else 1


def handle_save(args, parser):
    """Handle save command - send to all agents and press Ctrl+Enter."""
    if not PYAUTOGUI_AVAILABLE:
        logger.error("❌ PyAutoGUI not available - cannot execute save command")
        return 1
        
    if not args.message:
        parser.error("--save requires --message MESSAGE")
    coords_loader = get_coordinate_loader()
    for agent in SWARM_AGENTS:
        x, y = coords_loader.get_chat_coordinates(agent)
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)
        if args.pyautogui:
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1.0)
        else:
            pyautogui.write(args.message, interval=0.01)
        pyautogui.hotkey("ctrl", "enter")
        time.sleep(1.0)
    return 0


def handle_leaderboard():
    """Display competition leaderboard."""
    system = get_competition_system()
    leaderboard = system.get_leaderboard()
    for score in leaderboard:
        print(f"#{score.rank} {score.agent_name}: {score.total_points} pts")
    return 0


# V3 Enhanced Messaging Features
def handle_verify_delivery(args):
    """Handle delivery verification command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    try:
        processor = MessagingV3Processor()
        results = processor.verify_all_deliveries()

        print("🔍 DELIVERY VERIFICATION RESULTS")
        print("=" * 50)
        print(f"Agents verified: {len(results['verified_agents'])}")
        print(f"Total messages checked: {results['total_verified']}")
        print(f"Queue/inbox mismatches: {len(results['queue_inbox_mismatches'])}")
        print(f"Stuck messages: {sum(msg['count'] for msg in results['stuck_messages'])}")

        if results['queue_inbox_mismatches']:
            print("\n⚠️ Agents with mismatches:")
            for agent in results['queue_inbox_mismatches']:
                print(f"  - {agent}")

        if results['stuck_messages']:
            print("\n⚠️ Agents with stuck messages:")
            for msg in results['stuck_messages']:
                print(f"  - {msg['agent_id']}: {msg['count']} stuck")

        return 0

    except Exception as e:
        logger.error(f"❌ Delivery verification failed: {e}")
        return 1


def handle_clean_queue(args):
    """Handle queue cleaning command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    try:
        processor = MessagingV3Processor()
        results = processor.clean_system_messages()

        print("🧹 QUEUE CLEANUP RESULTS")
        print("=" * 50)
        print(f"Status: {results.get('status', 'unknown')}")
        print(f"Original messages: {results.get('original_count', 0)}")
        print(f"System messages removed: {results.get('removed_count', 0)}")
        print(f"Messages remaining: {results.get('remaining_count', 0)}")

        if results.get('message'):
            print(f"Message: {results['message']}")

        return 0

    except Exception as e:
        logger.error(f"❌ Queue cleanup failed: {e}")
        return 1


def handle_reset_stuck(args):
    """Handle stuck message reset command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    try:
        processor = MessagingV3Processor()
        results = processor.reset_stuck_messages()

        print("🔄 STUCK MESSAGE RESET RESULTS")
        print("=" * 50)
        print(f"Status: {results.get('status', 'unknown')}")
        print(f"Messages reset: {results.get('reset_count', 0)}")

        if results.get('message'):
            print(f"Message: {results['message']}")

        return 0

    except Exception as e:
        logger.error(f"❌ Stuck message reset failed: {e}")
        return 1


def handle_queue_stats(args):
    """Handle queue statistics command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    try:
        processor = MessagingV3Processor()
        stats = processor.get_system_stats()

        print("📊 QUEUE STATISTICS")
        print("=" * 50)

        queue_stats = stats.get('queue_stats', {})
        print(f"Total messages: {queue_stats.get('total_messages', 0)}")
        print("Status breakdown:")
        for status, count in queue_stats.get('status_breakdown', {}).items():
            print(f"  {status}: {count}")

        delivery_stats = stats.get('delivery_stats', {})
        print(f"Delivery success rate: {delivery_stats.get('delivery_success_rate', 0):.2%}")

        return 0

    except Exception as e:
        logger.error(f"❌ Queue stats failed: {e}")
        return 1


def handle_health_check(args):
    """Handle health check command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    try:
        processor = MessagingV3Processor()
        health = processor.perform_health_check()

        print("🏥 MESSAGING SYSTEM HEALTH CHECK")
        print("=" * 50)
        print(f"Overall status: {health.get('overall_status', 'unknown').upper()}")
        print(f"Timestamp: {health.get('timestamp', 'unknown')}")

        print("\nComponent Status:")
        for component, check in health.get('checks', {}).items():
            status = check.get('status', 'unknown')
            message = check.get('message', '')
            status_icon = "✅" if status == "healthy" else "⚠️" if status == "warning" else "❌"
            print(f"  {status_icon} {component}: {message}")

        if health.get('recommendations'):
            print("\n💡 Recommendations:")
            for rec in health['recommendations']:
                print(f"  • {rec}")

        return 0

    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return 1


def handle_process_workspaces(args):
    """Handle workspace processing command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    try:
        processor = MessagingV3Processor()
        results = processor.process_all_workspaces()

        print("🧹 WORKSPACE PROCESSING RESULTS")
        print("=" * 50)
        print(f"Agents processed: {len(results.get('agents_processed', []))}")
        print(f"Total messages processed: {results.get('total_processed', 0)}")
        print(f"Errors: {len(results.get('errors', []))}")

        for agent_result in results.get('agents_processed', []):
            agent_id = agent_result.get('agent_id')
            result = agent_result.get('result', {})
            processed = result.get('processed', 0)
            archived = result.get('archived', 0)
            print(f"  {agent_id}: {processed} processed, {archived} archived")

        if results.get('errors'):
            print("\n❌ Errors:")
            for error in results['errors']:
                print(f"  • {error}")

        return 0

    except Exception as e:
        logger.error(f"❌ Workspace processing failed: {e}")
        return 1


def handle_archive_old(args):
    """Handle old message archiving command."""
    if not V3_AVAILABLE:
        logger.error("❌ V3 messaging features not available")
        return 1

    days = args.archive_old or 30

    try:
        from .messaging.v3.archival_service import ArchivalService
        from pathlib import Path

        archival = ArchivalService(Path(__file__).resolve().parent.parent.parent.parent)
        results = archival.rotate_archives(days_to_keep=days)

        print(f"🗂️ ARCHIVE ROTATION RESULTS (>{days} days)")
        print("=" * 50)
        print(f"Files processed: {results.get('processed', 0)}")
        print(f"Files deleted: {results.get('deleted', 0)}")
        print(f"Space freed: {results.get('total_space_freed', 0)} bytes")
        print(f"Errors: {results.get('errors', 0)}")

        return 0

    except Exception as e:
        logger.error(f"❌ Archive rotation failed: {e}")
        return 1


# SWARM INTELLIGENCE CLI COMMANDS
def handle_swarm_vote(args):
    """Handle swarm consensus voting commands."""
    try:
        if not args.topic:
            print("❌ Error: --topic is required for swarm voting")
            return 1

        if not args.options:
            print("❌ Error: --options is required for swarm voting")
            return 1

        options_list = [opt.strip() for opt in args.options.split(',')]

        if len(options_list) < 2:
            print("❌ Error: At least 2 voting options required")
            return 1

        # Import consensus engine
        from examples.consensus_demo import ConsensusEngine

        engine = ConsensusEngine()
        consensus_id = engine.initiate_consensus_process(
            args.topic,
            options_list,
            deadline_minutes=getattr(args, 'deadline', 30)
        )

        if consensus_id:
            print(f"🐝 SWARM CONSENSUS INITIATED")
            print(f"Consensus ID: {consensus_id}")
            print(f"Topic: {args.topic}")
            print(f"Options: {', '.join(options_list)}")
            print(f"Deadline: {getattr(args, 'deadline', 30)} minutes")
            print("\n📊 Agents will vote through the messaging system")
            return 0
        else:
            print("❌ Failed to initiate swarm consensus")
            return 1

    except Exception as e:
        logger.error(f"Error in swarm voting: {e}")
        print(f"❌ Error in swarm voting: {e}")
        return 1


def handle_swarm_conflict(args):
    """Handle swarm conflict resolution commands."""
    try:
        if not args.description:
            print("❌ Error: --description is required for conflict resolution")
            return 1

        conflict_message = f"""🐝 SWARM CONFLICT DETECTED

Description: {args.description}
Severity: {getattr(args, 'severity', 'medium')}
Agents Involved: {getattr(args, 'agents', 'All agents')}

CONFLICT RESOLUTION PROTOCOL ACTIVATED:
1. All agents acknowledge the conflict
2. Technical analysis phase begins
3. Consensus-driven resolution
4. Implementation of agreed solution

🐝 WE. ARE. SWARM. Conflict resolution in progress."""

        # Broadcast conflict to all agents
        success = send_message(
            content=conflict_message,
            sender="SYSTEM",
            recipient="all",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )

        if success:
            print("🚨 SWARM CONFLICT RESOLUTION INITIATED")
            print(f"Description: {args.description}")
            print("All agents notified - resolution protocol active")
            return 0
        else:
            print("❌ Failed to initiate conflict resolution")
            return 1

    except Exception as e:
        logger.error(f"Error in conflict resolution: {e}")
        print(f"❌ Error in conflict resolution: {e}")
        return 1


def handle_swarm_profile(args):
    """Handle swarm profiling and performance analysis."""
    try:
        if args.agent:
            # Profile specific agent
            agents_to_profile = [args.agent]
        else:
            # Profile all agents
            from src.core.constants.agent_constants import AGENT_LIST
            agents_to_profile = AGENT_LIST

        print(f"📊 PROFILING {len(agents_to_profile)} AGENT(S)")

        for agent in agents_to_profile:
            profile_message = f"""SYSTEM: Performance profile analysis requested for {agent}.

PROFILING METRICS REQUESTED:
- Response time analysis
- Task completion rate
- Error frequency
- Collaboration effectiveness
- Resource utilization

Please provide current performance metrics."""

            success = send_message(
                content=profile_message,
                sender="SYSTEM",
                recipient=agent,
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.HIGH
            )

            if success:
                print(f"✅ Profile request sent to {agent}")
            else:
                print(f"❌ Failed to profile {agent}")

        print(f"\n📈 Swarm profiling initiated for {len(agents_to_profile)} agent(s)")
        return 0

    except Exception as e:
        logger.error(f"Error in swarm profiling: {e}")
        print(f"❌ Error in swarm profiling: {e}")
        return 1


def handle_swarm_prove(args):
    """Handle swarm validation and proof requests."""
    try:
        if not args.claim:
            print("❌ Error: --claim is required for proof validation")
            return 1

        proof_message = f"""🐝 SWARM VALIDATION REQUEST

Claim to validate: {args.claim}
Validation Level: {getattr(args, 'level', 'standard')}
Evidence Required: {getattr(args, 'evidence', 'Technical analysis and testing')}

VALIDATION PROTOCOL:
1. Independent verification by multiple agents
2. Cross-validation of results
3. Consensus on validation outcome
4. Documentation of proof

🐝 WE. ARE. SWARM. Validation in progress."""

        # Send to all agents or specific agent
        recipient = args.agent if args.agent else "all"
        priority = UnifiedMessagePriority.URGENT if not args.agent else UnifiedMessagePriority.HIGH

        success = send_message(
            content=proof_message,
            sender="SYSTEM",
            recipient=recipient,
            message_type=UnifiedMessageType.TEXT,
            priority=priority
        )

        if success:
            print("🔍 SWARM VALIDATION INITIATED")
            print(f"Claim: {args.claim}")
            print(f"Target: {recipient}")
            print("Multi-agent validation protocol active")
            return 0
        else:
            print("❌ Failed to initiate validation")
            return 1

    except Exception as e:
        logger.error(f"Error in swarm proof validation: {e}")
        print(f"❌ Error in swarm proof validation: {e}")
        return 1


def handle_swarm_patterns(args):
    """Handle swarm pattern analysis and intelligence gathering."""
    try:
        pattern_message = f"""🐝 SWARM PATTERN ANALYSIS ACTIVATED

Analysis Type: {getattr(args, 'type', 'comprehensive')}
Time Window: {getattr(args, 'window', '24 hours')}
Focus Areas: {getattr(args, 'focus', 'All patterns')}

PATTERN ANALYSIS PROTOCOL:
1. Data collection from all agents
2. Pattern identification algorithms
3. Correlation analysis
4. Predictive modeling
5. Intelligence report generation

🐝 WE. ARE. SWARM. Pattern recognition active."""

        # Send to all agents for pattern contribution
        success = send_message(
            content=pattern_message,
            sender="SYSTEM",
            recipient="all",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.HIGH
        )

        if success:
            print("🔬 SWARM PATTERN ANALYSIS INITIATED")
            print(f"Type: {getattr(args, 'type', 'comprehensive')}")
            print(f"Window: {getattr(args, 'window', '24 hours')}")
            print("All agents engaged in pattern analysis")
            return 0
        else:
            print("❌ Failed to initiate pattern analysis")
            return 1

    except Exception as e:
        logger.error(f"Error in swarm pattern analysis: {e}")
        print(f"❌ Error in swarm pattern analysis: {e}")
        return 1
