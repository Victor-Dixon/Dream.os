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
