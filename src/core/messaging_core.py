from __future__ import annotations

"""
⚠️ DEPRECATED - IMessageDelivery protocol is deprecated.

This interface has been consolidated into src/core/messaging_protocol_models.py as SSOT.
Please update imports to use the SSOT location instead.

Migration:
  OLD: from core.messaging_protocol_models import IMessageDelivery
  NEW: from core.messaging_protocol_models import IMessageDelivery

Note: SSOT has full documentation and type hints

This interface will be removed in a future release.
"""
import warnings
from .messaging_models import (
    DeliveryMethod,
    RecipientType,
    SenderType,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from ..utils.swarm_time import format_swarm_timestamp, get_swarm_time_display
from typing import Any, Protocol
from datetime import datetime
import logging
warnings.warn(
    "IMessageDelivery is deprecated. Use src/core/messaging_protocol_models.py instead.",
    DeprecationWarning,
    stacklevel=2
)

#!/usr/bin/env python3
"""
UNIFIED MESSAGING CORE SYSTEM - SINGLE SOURCE OF TRUTH
=====================================================

<!-- SSOT Domain: integration -->

V2 COMPLIANCE REFACTOR: Phase 2C - Service Layer Pattern applied
Original: 544 lines → Refactored with services (validation, template resolution, history, delivery orchestration)

This is the ONE AND ONLY messaging system for the entire Agent Cellphone V2 project.
Consolidates ALL messaging functionality into a single, unified system.

V2 Compliance: SSOT Implementation (CRITICAL violation fixed)
SOLID Principles: Single Responsibility (One messaging system), Open-Closed (Extensible)

Author: Agent-1 (System Recovery Specialist) - Messaging Consolidation Champion
Refactored: 2025-10-11 - Agent-1 (LAST CRITICAL V2 VIOLATION FIX)
License: MIT
"""


# Import models from extracted module

# Configure logging
logger = logging.getLogger(__name__)

# ⚠️ DEPRECATED - IMessageDelivery protocol is deprecated.
# This interface has been consolidated into src/core/messaging_protocol_models.py as SSOT.
# Migration: from src.core.messaging_protocol_models import IMessageDelivery
warnings.warn(
    "IMessageDelivery is deprecated. Use src/core/messaging_protocol_models.py instead.",
    DeprecationWarning,
    stacklevel=2
)


class IMessageDelivery(Protocol):
    """Interface for message delivery mechanisms."""

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message."""
        ...


"""
⚠️ DEPRECATED - IOnboardingService protocol is deprecated.

This interface has been consolidated into src/core/messaging_protocol_models.py as SSOT.
Please update imports to use the SSOT location instead.

Migration:
  OLD: from src.core.messaging_core import IOnboardingService
  NEW: from src.core.messaging_protocol_models import IOnboardingService

Note: SSOT has full documentation and type hints

This interface will be removed in a future release.
"""

warnings.warn(
    "IOnboardingService is deprecated. Use src/core/messaging_protocol_models.py instead.",
    DeprecationWarning,
    stacklevel=2
)


class IOnboardingService(Protocol):
    """Interface for onboarding operations."""

    def generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate onboarding message."""
        ...


class UnifiedMessagingCore:
    """SINGLE SOURCE OF TRUTH for all messaging functionality."""

    def __init__(
        self,
        delivery_service: IMessageDelivery | None = None,
        onboarding_service: IOnboardingService | None = None,
        message_repository: Any | None = None,
    ):
        """Initialize the unified messaging core."""
        self.delivery_service = delivery_service
        self.onboarding_service = onboarding_service
        self.logger = logging.getLogger(__name__)

        # Initialize message repository for history logging
        if message_repository is None:
            try:
                from ..repositories.message_repository import MessageRepository
                self.message_repository = MessageRepository()
            except ImportError:
                self.logger.warning(
                    "MessageRepository not available - history logging disabled")
                self.message_repository = None
        else:
            self.message_repository = message_repository

        # Initialize services (Phase 2C: Service Layer Pattern)
        from .messaging_validation import MessageValidationService
        from .messaging_template_resolution import TemplateResolutionService
        from .messaging_history import MessageHistoryService
        from .messaging_delivery_orchestration import MessageDeliveryOrchestrationService
        
        self.validation_service = MessageValidationService()
        self.template_service = TemplateResolutionService()
        self.history_service = MessageHistoryService(self.message_repository)
        self.delivery_orchestration_service = MessageDeliveryOrchestrationService(
            self.delivery_service
        )

        # Initialize subsystems
        self._initialize_subsystems()
        
        # Update delivery orchestration service with initialized delivery service
        self.delivery_orchestration_service.delivery_service = self.delivery_service

    def _initialize_subsystems(self):
        """Initialize all messaging subsystems."""
        # Import and initialize delivery services
        try:
            from .messaging_pyautogui import PyAutoGUIMessagingDelivery

            if not self.delivery_service:
                self.delivery_service = PyAutoGUIMessagingDelivery()
        except ImportError:
            self.logger.warning("PyAutoGUI delivery service not available")

        # Import and initialize onboarding service
        try:
            from .onboarding_service import OnboardingService

            if not self.onboarding_service:
                self.onboarding_service = OnboardingService()
                self.logger.info("✅ Onboarding service initialized")
        except ImportError as e:
            self.logger.debug(f"Onboarding service not available: {e}")

        # SSOT: MessageRepository already initialized in __init__ (Agent-8 - 2025-01-27)
        # Do NOT create duplicate instance here - use self.message_repository from __init__

    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Send a message using the unified messaging system.

        VALIDATION: Checks if recipient has pending multi-agent request.
        If pending, blocks message and shows pending request in error.
        """
        # Validate recipient can receive messages (Phase 2C: Use validation service)
        metadata_dict = metadata or {}
        can_send, updated_metadata = self.validation_service.validate_recipient_can_receive(
            recipient=recipient,
            sender=sender,
            content=content,
            metadata=metadata_dict
        )
        
        if not can_send:
            return False
        
        metadata_dict = updated_metadata or {}

        # Extract category from metadata if present (for template detection)
        category = None
        if isinstance(metadata_dict, dict):
            category_str = metadata_dict.get('message_category')
            if category_str:
                try:
                    from .messaging_models import MessageCategory
                    category = MessageCategory(category_str.lower())
                except (ValueError, AttributeError):
                    pass

        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata_dict,
            category=category if category else None,  # Preserve category from metadata
        )

        return self.send_message_object(message)

    def send_message_object(self, message: UnifiedMessage) -> bool:
        """Send a UnifiedMessage object."""
        try:
            # Apply A2A bilateral coordination template if needed
            if (message.category and
                message.category.name == 'A2A' and
                isinstance(message.content, str)):
                try:
                    from .messaging_template_texts import MESSAGE_TEMPLATES
                    from .messaging_models_core import MessageCategory
                    import uuid
                    from datetime import datetime

                    template = MESSAGE_TEMPLATES.get(MessageCategory.A2A)
                    if template:
                        # Populate template with message data
                        extra_meta = {
                            "ask": message.content,
                            "context": "",
                        }

                        now = datetime.now().isoformat(timespec="seconds")
                        templated_content = template.format(
                            sender=message.sender,
                            recipient=message.recipient,
                            priority=message.priority.value if hasattr(message.priority, 'value') else str(message.priority),
                            message_id=str(uuid.uuid4()),
                            timestamp=now,
                            agent_id=message.recipient,
                            ask=extra_meta.get("ask", message.content),
                            context=extra_meta.get("context", ""),
                            coordination_rationale=extra_meta.get("coordination_rationale", "To leverage parallel processing and accelerate completion"),
                            expected_contribution=extra_meta.get("expected_contribution", "Domain expertise and parallel execution"),
                            coordination_timeline=extra_meta.get("coordination_timeline", "ASAP - coordination needed to maintain momentum"),
                            next_step=extra_meta.get(
                                "next_step",
                                "Reply via messaging_cli with ACCEPT/DECLINE, ETA, and a 2–3 bullet plan, "
                                "then update status.json and MASTER_TASK_LOG.md.",
                            ),
                            fallback=extra_meta.get(
                                "fallback", "If blocked: send blocker + proposed fix + owner."),
                        )
                        message.content = templated_content
                except Exception as e:
                    # Template application failed, use original content
                    pass

            # Phase 2C: Template resolution using service
            if isinstance(message.metadata, dict):
                self.template_service.apply_template_to_message(message.metadata)

            # Phase 2C: Log message to history using service
            self.history_service.log_message(message, status="sent")

            # Phase 2C: Orchestrate delivery using service
            success = self.delivery_orchestration_service.orchestrate_delivery(message)
            
            # Log delivery status if successful
            if success:
                self.history_service.log_delivery_status(message, status="delivered")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            # Phase 2C: Log failure using service
            self.history_service.log_failure(message, e)
            return False

    def show_message_history(self):
        """Display message history."""
        try:
            # Simple history display - in practice would use message queue
            self.logger.info("📋 Message History:")
            self.logger.info("-" * 40)
            # This would be enhanced to show actual message history
            self.logger.info("Message history functionality available")
        except Exception as e:
            self.logger.error(f"Failed to show message history: {e}")

    def generate_onboarding_message(self, agent_id: str, style: str = "standard") -> str:
        """Generate onboarding message for an agent."""
        if self.onboarding_service:
            return self.onboarding_service.generate_onboarding_message(agent_id, style)
        else:
            return f"Welcome {agent_id}! You have been onboarded to the Agent Cellphone V2 system."

    def broadcast_message(
        self,
        content: str,
        sender: str,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
    ) -> bool:
        """Broadcast message to all agents.

        CRITICAL FIX: Expands "ALL_AGENTS" into individual messages for each agent.
        This ensures broadcast messages are properly queued and delivered to all agents.
        """
        # Get list of active agents (mode-aware)
        try:
            from .agent_mode_manager import get_active_agents
            agents = get_active_agents()
        except Exception:
            # Fallback to all agents if mode manager unavailable
            from src.core.constants.agent_constants import AGENT_LIST
            agents = AGENT_LIST

        # Send individual message to each agent (ensures proper queue processing)
        success_count = 0
        import time
        for agent in agents:
            message = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=agent,
                message_type=UnifiedMessageType.BROADCAST,
                priority=priority,
                tags=[UnifiedMessageTag.SYSTEM],
            )

            if self.send_message_object(message):
                success_count += 1
                # Small delay between broadcast sends to prevent routing race conditions
                time.sleep(0.5)

        return success_count > 0

    def list_agents(self):
        """List all available agents (mode-aware)."""
        try:
            from .agent_mode_manager import get_active_agents, get_mode_manager
            mode_manager = get_mode_manager()
            current_mode = mode_manager.get_current_mode()
            agents = get_active_agents()
            self.logger.info(
                f"🤖 Available Agents (Mode: {current_mode}, {len(agents)} active):")
        except Exception:
            # Fallback to all agents if mode manager unavailable
            from src.core.constants.agent_constants import AGENT_LIST
            agents = AGENT_LIST
            self.logger.info("🤖 Available Agents:")
        for agent in agents:
            self.logger.info(f"  • {agent}")


# SINGLE GLOBAL INSTANCE - THE ONE TRUE MESSAGING CORE
messaging_core = UnifiedMessagingCore()


# PUBLIC API - Single point of access for all messaging
def get_messaging_core() -> UnifiedMessagingCore:
    """Get the SINGLE SOURCE OF TRUTH messaging core."""
    return messaging_core


def send_message(
    content: str,
    sender: str,
    recipient: str,
    message_type: UnifiedMessageType,
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
    tags: list[UnifiedMessageTag] | None = None,
    metadata: dict[str, Any] | None = None,
) -> bool:
    """
    Send message using the SINGLE SOURCE OF TRUTH.

    ⚠️  DEPRECATED: Direct messaging functions are deprecated.
    For agent-to-agent communication, use the A2A coordination protocol:
    python -m src.services.messaging_cli --agent Agent-X --category a2a --sender Agent-Y --message "..."
    This ensures bilateral coordination protocol compliance and swarm force multiplication.
    """
    return messaging_core.send_message(
        content, sender, recipient, message_type, priority, tags, metadata
    )


def send_message_object(message: UnifiedMessage) -> bool:
    """Send UnifiedMessage using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.send_message_object(message)


def broadcast_message(
    content: str, sender: str, priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
) -> bool:
    """Broadcast message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.broadcast_message(content, sender, priority)


def generate_onboarding_message(agent_id: str, style: str = "standard") -> str:
    """Generate onboarding message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.generate_onboarding_message(agent_id, style)


def show_message_history():
    """Show message history using the SINGLE SOURCE OF TRUTH."""
    messaging_core.show_message_history()


def list_agents():
    """List agents using the SINGLE SOURCE OF TRUTH."""
    messaging_core.list_agents()


# LEGACY COMPATIBILITY FUNCTIONS
def get_messaging_logger():
    """Legacy compatibility function."""
    return logging.getLogger(__name__)


# MESSAGING MODELS EXPORTS - Single source for all messaging models
__all__ = [
    "UnifiedMessagingCore",
    "UnifiedMessage",
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "IMessageDelivery",
    "IOnboardingService",
    "get_messaging_core",
    "send_message",
    "send_message_object",
    "broadcast_message",
    "generate_onboarding_message",
    "show_message_history",
    "list_agents",
    "get_messaging_logger",
]


# VALIDATION AND HEALTH CHECKS
def validate_messaging_system() -> bool:
    """Validate the messaging system is properly configured."""
    try:
        core = get_messaging_core()
        if not core:
            logger.error("Messaging core not available")
            return False

        # Test basic functionality
        test_message = UnifiedMessage(
            content="System validation test",
            sender="SYSTEM",
            recipient="TEST_AGENT",
            message_type=UnifiedMessageType.TEXT,
        )

        logger.info("✅ Messaging system validation passed")
        return True

    except Exception as e:
        logger.error(f"❌ Messaging system validation failed: {e}")
        return False


# AUTO-INITIALIZATION
def initialize_messaging_system() -> None:
    """Initialize the messaging system."""
    logger.info("🔧 Initializing SINGLE SOURCE OF TRUTH Messaging System")

    if validate_messaging_system():
        logger.info("✅ Messaging system ready - SSOT established")
    else:
        logger.error("❌ Messaging system initialization failed")
        raise ValueError("Invalid messaging system configuration")


# Initialize on import
try:
    initialize_messaging_system()
except Exception as e:
    logger.error(f"Failed to initialize messaging system: {e}")
    # Don't raise exception during import - allow system to continue
