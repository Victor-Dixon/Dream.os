<<<<<<< HEAD
#!/usr/bin/env python3
"""
Core Delivery for Message Queue Processing
==========================================

Handles direct delivery via core messaging system.
"""

import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)


def deliver_via_core(recipient: str, content: str, metadata: dict, message_type_str: str, sender: str, priority_str: str, tags_list: list) -> bool:
    """
    Deliver message via core messaging system (direct PyAutoGUI delivery).

    Args:
        recipient: Target agent ID
        content: Message content
        metadata: Message metadata
        message_type_str: Message type string
        sender: Sender identifier
        priority_str: Priority string
        tags_list: Tags list

    Returns:
        True if delivery successful, False otherwise
    """
    try:
        # Direct PyAutoGUI delivery - no CLI, no fallback simulation
        from src.core.messaging_pyautogui import send_message_pyautogui

        # Check if PyAutoGUI delivery is requested
        use_pyautogui = True
        if isinstance(metadata, dict):
            use_pyautogui = metadata.get("use_pyautogui", True)

        if not use_pyautogui:
            # Fall back to inbox delivery
            from .delivery_inbox import deliver_fallback_inbox
            return deliver_fallback_inbox(recipient, content, metadata, message_type_str, sender, priority_str, tags_list)

        # Direct PyAutoGUI delivery
        success = send_message_pyautogui(recipient, content)

        if success:
            logger.info(f"✅ Message delivered via PyAutoGUI to {recipient}")
            return True
        else:
            logger.error(f"❌ PyAutoGUI delivery failed for {recipient}")
            return False

    except Exception as e:
        logger.error(f"❌ Core delivery error: {e}")
        return False
=======
#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Delivery Core - Primary PyAutoGUI Delivery
==========================================

Primary delivery path via unified messaging core (PyAutoGUI or injected mock).
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def deliver_via_core(
    recipient: str,
    content: str,
    metadata: dict,
    message_type_str: Optional[str],
    sender: str,
    priority_str: str,
    tags_list: list,
    messaging_core: Optional[Any] = None,
) -> bool:
    """
    Primary path: Unified messaging core (PyAutoGUI delivery or injected mock).

    Args:
        recipient: Agent ID to deliver to
        content: Message content
        metadata: Message metadata
        message_type_str: Message type string
        sender: Sender identifier
        priority_str: Priority string
        tags_list: Tags list
        messaging_core: Optional injected messaging core (for testing)

    Returns:
        True if delivery successful, False otherwise
    """
    try:
        from ...messaging_models_core import (
            UnifiedMessageType,
            UnifiedMessagePriority,
            UnifiedMessageTag,
        )

        # Parse message_type
        if message_type_str:
            try:
                message_type = UnifiedMessageType(message_type_str)
            except (ValueError, TypeError):
                message_type_map = {
                    "captain_to_agent": UnifiedMessageType.CAPTAIN_TO_AGENT,
                    "agent_to_agent": UnifiedMessageType.AGENT_TO_AGENT,
                    "agent_to_captain": UnifiedMessageType.AGENT_TO_AGENT,
                    "system_to_agent": UnifiedMessageType.SYSTEM_TO_AGENT,
                    "human_to_agent": UnifiedMessageType.HUMAN_TO_AGENT,
                    "onboarding": UnifiedMessageType.ONBOARDING,
                    "text": UnifiedMessageType.TEXT,
                    "broadcast": UnifiedMessageType.BROADCAST,
                }
                message_type = message_type_map.get(
                    message_type_str.lower(), UnifiedMessageType.SYSTEM_TO_AGENT
                )
        else:
            if sender and recipient:
                if sender.startswith("Agent-") and recipient.startswith("Agent-"):
                    message_type = UnifiedMessageType.AGENT_TO_AGENT
                elif sender.startswith("Agent-") and recipient.upper() in ["CAPTAIN", "AGENT-4"]:
                    message_type = UnifiedMessageType.AGENT_TO_AGENT
                elif sender.upper() in ["CAPTAIN", "AGENT-4"]:
                    message_type = UnifiedMessageType.CAPTAIN_TO_AGENT
                else:
                    message_type = UnifiedMessageType.SYSTEM_TO_AGENT
            else:
                message_type = UnifiedMessageType.SYSTEM_TO_AGENT

        # Parse priority
        try:
            priority = UnifiedMessagePriority(priority_str.lower())
        except (ValueError, TypeError):
            priority = UnifiedMessagePriority.REGULAR

        # Parse tags
        tags = []
        if tags_list:
            for tag_str in tags_list:
                try:
                    if isinstance(tag_str, str):
                        tags.append(UnifiedMessageTag(tag_str.lower()))
                    else:
                        tags.append(tag_str)
                except (ValueError, TypeError):
                    pass
        if not tags:
            tags = [UnifiedMessageTag.SYSTEM]

        # Use injected messaging core if provided
        if messaging_core is not None:
            ok = messaging_core.send_message(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                tags=tags,
                metadata=metadata or {},
            )
        else:
            from ...messaging_core import send_message
            from ...keyboard_control_lock import keyboard_control

            # Preserve message category in metadata
            delivery_metadata = dict(metadata) if metadata else {}
            if isinstance(metadata, dict):
                category_str = metadata.get('message_category')
                if category_str:
                    try:
                        from ...messaging_models_core import MessageCategory
                        category_from_meta = MessageCategory(
                            category_str.lower())
                        delivery_metadata['message_category'] = category_from_meta.value
                    except (ValueError, AttributeError):
                        pass

            with keyboard_control(f"queue_delivery::{recipient}"):
                ok = send_message(
                    content=content,
                    sender=sender,
                    recipient=recipient,
                    message_type=message_type,
                    priority=priority,
                    tags=tags,
                    metadata=delivery_metadata,
                )

        return ok

    except ImportError as e:
        logger.error(f"Import error in deliver_via_core: {e}")
        return False
    except Exception as e:
        logger.error(f"Error in deliver_via_core: {e}", exc_info=True)
        return False
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
