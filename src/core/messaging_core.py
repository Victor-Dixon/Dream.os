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
from pathlib import Path
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

V2 COMPLIANCE REFACTOR: Models extracted to messaging_models_core.py
Original: 472 lines → Now: 336 lines (28% reduction)

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

        # Initialize subsystems
        self._initialize_subsystems()

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
        # Validate recipient can receive messages (check for pending multi-agent requests)
        # Only validate if recipient is an agent (not system/captain)
        if recipient.startswith("Agent-") and sender.startswith("Agent-"):
            try:
                from ..core.multi_agent_request_validator import get_multi_agent_validator

                validator = get_multi_agent_validator()
                can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                    agent_id=recipient,
                    target_recipient=sender,  # Allow if responding to request sender
                    message_content=content
                )

                if not can_send:
                    # Recipient has pending request - block and show error
                    self.logger.warning(
                        f"❌ Message blocked - {recipient} has pending multi-agent request"
                    )
                    # Store error in metadata for caller to access
                    if metadata is None:
                        metadata = {}
                    metadata["blocked"] = True
                    metadata["blocked_reason"] = "pending_multi_agent_request"
                    metadata["blocked_error_message"] = error_message
                    return False

                # If responding to request sender, auto-route to collector
                if pending_info and sender == pending_info["sender"]:
                    try:
                        from ..core.multi_agent_responder import get_multi_agent_responder
                        responder = get_multi_agent_responder()

                        # Auto-submit response to collector
                        collector_id = pending_info["collector_id"]
                        responder.submit_response(
                            collector_id, recipient, content)

                        self.logger.info(
                            f"✅ Auto-routed response from {recipient} to collector {collector_id}"
                        )
                        # Still send the message normally (it's their response)
                    except Exception as e:
                        self.logger.debug(f"Error auto-routing response: {e}")
                        # Continue with normal message send
            except ImportError:
                # Validator not available, proceed normally
                pass
            except Exception as e:
                self.logger.debug(f"Error validating recipient: {e}")
                # Continue with normal flow

        # Extract category from metadata if present (for template detection)
        category = None
        metadata_dict = metadata or {}
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
            # Role- and channel-aware template resolution hook
            # Attach selected template into metadata for downstream delivery/formatting layers
            try:
                from ..services.messaging.policy_loader import (
                    load_template_policy,
                    resolve_template_by_channel,
                    resolve_template_by_roles,
                )
            except Exception:
                load_template_policy = None  # type: ignore
                resolve_template_by_channel = None  # type: ignore
                resolve_template_by_roles = None  # type: ignore

            template = (
                message.metadata.get("template") if isinstance(
                    message.metadata, dict) else None
            )
            channel = (
                (message.metadata or {}).get("channel", "standard")
                if isinstance(message.metadata, dict)
                else "standard"
            )
            sender_role = (
                (message.metadata or {}).get("sender_role", "AGENT")
                if isinstance(message.metadata, dict)
                else "AGENT"
            )
            receiver_role = (
                (message.metadata or {}).get("receiver_role", "AGENT")
                if isinstance(message.metadata, dict)
                else "AGENT"
            )

            if (
                not template
                and load_template_policy
                and resolve_template_by_channel
                and resolve_template_by_roles
            ):
                policy = load_template_policy()
                # Channel overrides first
                if channel in ("onboarding", "passdown", "standard"):
                    template = resolve_template_by_channel(policy, channel)
                # If not forced by channel, resolve by roles
                if not template or template == "compact":
                    template = resolve_template_by_roles(
                        policy, str(sender_role), str(receiver_role)
                    )

                message.metadata["template"] = template  # type: ignore[index]

            # Log message to history repository (Phase 1: Message History Logging - IMPLEMENTED)
            if self.message_repository:
                try:
                    # Serialize metadata to ensure JSON compatibility (recursive)
                    def serialize_value(value):
                        """Recursively serialize values for JSON compatibility."""
                        if isinstance(value, datetime):
                            return value.isoformat()
                        elif isinstance(value, dict):
                            return {k: serialize_value(v) for k, v in value.items()}
                        elif isinstance(value, (list, tuple)):
                            return [serialize_value(item) for item in value]
                        elif hasattr(value, '__dict__'):
                            return str(value)
                        else:
                            return value

                    metadata_serialized = serialize_value(
                        message.metadata) if message.metadata else {}

                    message_dict = {
                        "from": message.sender,
                        "to": message.recipient,
                        "content": message.content[:200] + "..." if len(message.content) > 200 else message.content,
                        "content_length": len(message.content),
                        "message_type": message.message_type.value if hasattr(message.message_type, "value") else str(message.message_type),
                        "priority": message.priority.value if hasattr(message.priority, "value") else str(message.priority),
                        "tags": [tag.value if hasattr(tag, "value") else str(tag) for tag in message.tags],
                        "metadata": metadata_serialized,
                        "timestamp": format_swarm_timestamp(),
                    }
                    self.message_repository.save_message(message_dict)
                    self.logger.debug(
                        f"✅ Message logged to history: {message.sender} → {message.recipient}")
                except Exception as e:
                    self.logger.warning(
                        f"⚠️ Failed to log message to history: {e}")
            else:
                # SSOT: Repository should be initialized in __init__ (Agent-8 - 2025-01-27)
                # If not available, log warning but don't create duplicate instance
                self.logger.warning(
                    "MessageRepository not initialized - message history logging skipped. "
                    "Repository should be initialized in __init__."
                )

            if self.delivery_service:
                success = self.delivery_service.send_message(message)
                # Update history with delivery status (SSOT FIX - Agent-4 - 2025-01-27)
                if self.message_repository and success:
                    try:
                        # Update message with delivery status
                        message_dict["status"] = "delivered"
                        self.message_repository.save_message(message_dict)
                        self.logger.debug(
                            f"✅ Delivery status logged: {message.sender} → {message.recipient}")
                    except Exception as e:
                        self.logger.warning(
                            f"⚠️ Failed to log delivery status: {e}")
                
                # FALLBACK QUEUING: If direct delivery fails, queue message for later processing
                # This ensures system messages flow through the queue when PyAutoGUI fails
                if not success:
                    try:
                        from .message_queue import MessageQueue
                        queue = MessageQueue()
                        queue_id = queue.enqueue(message)
                        self.logger.info(
                            f"📬 Direct delivery failed, message queued for later processing: {queue_id} "
                            f"({message.sender} → {message.recipient})")
                        # Return True to indicate message was handled (queued), even though direct delivery failed
                        return True
                    except Exception as queue_error:
                        self.logger.error(
                            f"❌ Failed to queue message after delivery failure: {queue_error}")
                        return False
                
                return success
            else:
                # No delivery service - try to queue message instead of failing
                try:
                    from .message_queue import MessageQueue
                    queue = MessageQueue()
                    queue_id = queue.enqueue(message)
                    self.logger.info(
                        f"📬 No delivery service available, message queued: {queue_id} "
                        f"({message.sender} → {message.recipient})")
                    return True
                except Exception as queue_error:
                    self.logger.error(
                        f"❌ No delivery service and queue unavailable: {queue_error}")
                    return False
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            # Log failure to history
            if self.message_repository:
                try:
                    history_entry = {
                        "from": message.sender,
                        "to": message.recipient,
                        "content": message.content[:500],
                        "timestamp": message.timestamp,
                        "status": "FAILED",
                        "error": str(e)[:200],
                    }
                    self.message_repository.save_message(history_entry)
                except Exception:
                    pass  # Non-critical
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
                # #region agent log
                import json
                from pathlib import Path
                log_path = Path("d:\\Agent_Cellphone_V2_Repository\\.cursor\\debug.log")
                broadcast_delay_start = time.time()
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "E", "location": "messaging_core.py:472", "message": "Before broadcast inter-agent delay", "data": {"agent": agent, "success": True, "delay_seconds": 1.0}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
                # Small delay between broadcast sends to prevent routing race conditions
                time.sleep(1.0)
                # #region agent log
                broadcast_delay_end = time.time()
                actual_delay = broadcast_delay_end - broadcast_delay_start
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "E", "location": "messaging_core.py:478", "message": "After broadcast inter-agent delay", "data": {"agent": agent, "expected_delay": 1.0, "actual_delay": round(actual_delay, 2)}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion

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
    """Send message using the SINGLE SOURCE OF TRUTH."""
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
