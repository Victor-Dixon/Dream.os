#!/usr/bin/env python3
"""
Service Adapters Module - Messaging Infrastructure
==================================================

<!-- SSOT Domain: integration -->

Extracted from messaging_infrastructure.py for V2 compliance.
Handles service adapters for Discord bot integration and external service wrappers.

V2 Compliance | Author: Agent-1 | Date: 2025-12-13
"""

from __future__ import annotations

import logging
import re
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.config.timeout_constants import TimeoutConstants
from src.core.messaging_core import UnifiedMessagePriority, UnifiedMessageType
from src.core.messaging_models_core import MessageCategory
from ...core.base.base_service import BaseService

from .message_formatters import _apply_template

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService(BaseService):
    """
    Consolidated messaging service adapter for Discord bot.

    CRITICAL UPDATE (2025-01-27): Uses message queue for synchronization
    Prevents race conditions when Discord + computer + agents send messages.
    All messages go through queue for sequential delivery with global lock.
    """

    def __init__(self):
        """Initialize messaging service."""
        super().__init__("ConsolidatedMessagingService")
        self.project_root = Path(__file__).parent.parent.parent
        self.messaging_cli = self.project_root / \
            "src" / "services" / "messaging_cli.py"

        # CRITICAL: Initialize message queue for synchronization
        try:
            from src.core.message_queue import MessageQueue

            self.queue = MessageQueue()
            self.logger.info(
                "✅ ConsolidatedMessagingService initialized with message queue")
        except Exception as e:
            self.logger.error(f"⚠️ Failed to initialize message queue: {e}")
            self.queue = None

    def send_message(
        self,
        agent: str,
        message: str,
        priority: str = "regular",
        use_pyautogui: bool = True,
        wait_for_delivery: bool = False,
        timeout: float = 30.0,
        discord_user_id: str | None = None,
        stalled: bool = False,
        apply_template: bool = False,
        message_category: MessageCategory | None = None,
        sender: str | None = None,
    ) -> dict[str, Any]:
        """
        Send message to agent via message queue (synchronized delivery).

        VALIDATION: Checks if agent has pending multi-agent request.
        If pending, blocks message and returns error with pending request details.

        CRITICAL: All messages go through queue to prevent race conditions.
        Discord + computer + agents synchronized through global keyboard lock.

        Args:
            agent: Target agent ID (e.g., "Agent-1")
            message: Message content
            priority: Message priority ("regular" or "urgent")
            use_pyautogui: Whether to use PyAutoGUI delivery (default: True)
            wait_for_delivery: Wait for message to be delivered before returning (default: False)
            timeout: Maximum time to wait for delivery in seconds (default: 30.0)
            discord_user_id: Discord user ID for username resolution (optional)
            stalled: Whether to use stalled delivery mode
            apply_template: Apply SSOT messaging template before sending (default: False)
            message_category: Explicit template category (defaults to D2A when templating)
            sender: Override sender name when templating (Discord user display name)

        Returns:
            Dictionary with success status and queue ID, or blocked status with error message
        """
        try:
            priority_value = (priority or "regular").lower()
            priority_enum = (
                UnifiedMessagePriority.URGENT
                if priority_value == "urgent"
                else UnifiedMessagePriority.REGULAR
            )

            resolved_sender = sender or (
                self._resolve_discord_sender(discord_user_id)
                if discord_user_id
                else "DISCORD"
            )

            templated_message = message
            if apply_template:
                category = message_category or MessageCategory.D2A
                templated_message = _apply_template(
                    category=category,
                    message=message,
                    sender=resolved_sender,
                    recipient=agent,
                    priority=priority_enum,
                    message_id=str(uuid.uuid4()),
                    extra={},
                )
                # CRITICAL FIX: If templated message ends with original message, it was appended incorrectly
                message_count = templated_message.count(message)
                if templated_message.endswith(message) and message_count > 1:
                    # Message was appended - remove it
                    templated_message = templated_message[:-len(message)].rstrip()

            # Validate agent can receive messages (check for pending multi-agent requests)
            from ..core.multi_agent_request_validator import get_multi_agent_validator

            validator = get_multi_agent_validator()
            can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                agent_id=agent,
                target_recipient=None,  # Not checking recipient, just blocking if pending
                message_content=message
            )

            if not can_send:
                # Agent has pending request - block and return error
                self.logger.warning(
                    f"❌ Message blocked for {agent} - pending multi-agent request"
                )
                return {
                    "success": False,
                    "blocked": True,
                    "reason": "pending_multi_agent_request",
                    "error_message": error_message,
                    "agent": agent,
                    "pending_request_message": error_message,
                    "pending_info": pending_info
                }

            # CRITICAL: Use message queue for PyAutoGUI delivery (synchronized delivery)
            if self.queue and use_pyautogui:
                # Determine message type explicitly for Discord messages
                # CRITICAL FIX: Always use HUMAN_TO_AGENT for Discord messages (never ONBOARDING)
                # Only onboarding commands (!hard onboard, !soft onboard, !start) should use ONBOARDING type
                message_lower = message.lower().strip()

                # More specific matching: only match "start" when followed by agent identifier
                is_onboarding_command = (
                    "hard onboard" in message_lower or
                    "soft onboard" in message_lower or
                    message_lower.startswith("!start") or
                    bool(re.match(r'^start\s+(agent-)?[1-8](\s|$)', message_lower, re.IGNORECASE))
                )

                # Set message_type explicitly: ONBOARDING only for onboarding commands, HUMAN_TO_AGENT for all others
                if is_onboarding_command:
                    explicit_message_type = UnifiedMessageType.ONBOARDING.value
                else:
                    # CRITICAL: Regular Discord messages ALWAYS use HUMAN_TO_AGENT (routes to chat input coords)
                    explicit_message_type = UnifiedMessageType.HUMAN_TO_AGENT.value

                # Enqueue message for sequential processing
                queue_id = self.queue.enqueue(
                    message={
                        "type": "agent_message",
                        "sender": resolved_sender,
                        "discord_username": self._get_discord_username(discord_user_id) if discord_user_id else None,
                        "discord_user_id": discord_user_id if discord_user_id else None,
                        "recipient": agent,
                        "content": templated_message,
                        "priority": priority,
                        "source": "discord",
                        "message_type": explicit_message_type,
                        "tags": [],
                        "metadata": {
                            "source": "discord",
                            "sender": resolved_sender,
                            "discord_username": self._get_discord_username(discord_user_id) if discord_user_id else None,
                            "discord_user_id": discord_user_id if discord_user_id else None,
                            "use_pyautogui": True,
                            "stalled": stalled,
                            "raw_message": message,
                            "message_category": (message_category or MessageCategory.D2A).value if apply_template else None,
                        },
                    }
                )

                self.logger.info(
                    f"✅ Message queued for {agent} (ID: {queue_id}): {message[:50]}..."
                )

                # CRITICAL: Wait for delivery if requested (blocking mode)
                if wait_for_delivery:
                    self.logger.debug(
                        f"⏳ Waiting for message {queue_id} delivery...")
                    delivered = self.queue.wait_for_delivery(
                        queue_id, timeout=timeout)
                    if delivered:
                        self.logger.info(
                            f"✅ Message {queue_id} delivered successfully")
                        return {
                            "success": True,
                            "message": f"Message delivered to {agent}",
                            "agent": agent,
                            "queue_id": queue_id,
                            "delivered": True,
                        }
                    else:
                        self.logger.warning(
                            f"⚠️ Message {queue_id} delivery failed or timeout")
                        return {
                            "success": False,
                            "message": f"Message delivery failed or timeout for {agent}",
                            "agent": agent,
                            "queue_id": queue_id,
                            "delivered": False,
                        }

                # Non-blocking: return immediately after enqueue
                return {
                    "success": True,
                    "message": f"Message queued for {agent}",
                    "agent": agent,
                    "queue_id": queue_id,
                }

            # Fallback to subprocess if queue not available
            cmd = [
                "python",
                str(self.messaging_cli),
                "--agent",
                agent,
                "--message",
                templated_message,
                "--priority",
                priority,
            ]

            if use_pyautogui:
                cmd.append("--pyautogui")

            # Set PYTHONPATH
            env = {"PYTHONPATH": str(self.project_root)}

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=TimeoutConstants.HTTP_DEFAULT, env=env, cwd=str(self.project_root)
            )

            if result.returncode == 0:
                self.logger.info(f"Message sent to {agent}: {message[:50]}...")
                return {"success": True, "message": f"Message sent to {agent}", "agent": agent}
            else:
                error_msg = result.stderr or "Unknown error"
                self.logger.error(
                    f"Failed to send message to {agent}: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to send message: {error_msg}",
                    "agent": agent,
                }

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout sending message to {agent}")
            return {"success": False, "message": "Message timeout", "agent": agent}
        except Exception as e:
            logger.error(f"Error sending message to {agent}: {e}")
            return {"success": False, "message": str(e), "agent": agent}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        """
        Broadcast message to all agents.

        CRITICAL: Wraps entire operation in keyboard lock to prevent conflicts.
        All 8 messages must complete before other operations can proceed.

        Args:
            message: Message content
            priority: Message priority

        Returns:
            Dictionary with success status
        """
        from ..core.keyboard_control_lock import keyboard_control

        # Get list of all agents (SSOT)
        from src.core.constants.agent_constants import AGENT_LIST
        agents = AGENT_LIST

        # CRITICAL: Wrap entire broadcast in keyboard lock
        with keyboard_control("broadcast_operation"):
            results = []
            for agent in agents:
                # CRITICAL: Wait for each message to be delivered before sending next
                result = self.send_message(
                    agent,
                    message,
                    priority,
                    use_pyautogui=True,
                    wait_for_delivery=True,  # Block until delivered
                    timeout=TimeoutConstants.HTTP_DEFAULT  # 30 second timeout per message
                )
                results.append(result)

                # Small delay between agents for stability
                time.sleep(0.5)

            success_count = sum(1 for r in results if r.get("success"))
            delivered_count = sum(
                1 for r in results if r.get("delivered", False))

            logger.info(
                f"✅ Broadcast complete: {success_count}/{len(agents)} queued, "
                f"{delivered_count}/{len(agents)} delivered "
                f"(locked during entire operation to prevent conflicts)"
            )

            return {
                "success": success_count > 0,
                "message": f"Broadcast to {success_count}/{len(agents)} agents ({delivered_count} delivered)",
                "results": results,
            }

    def _resolve_discord_sender(self, discord_user_id: str | None) -> str:
        """Resolve Discord user ID to sender name."""
        if not discord_user_id:
            return "DISCORD"
        # For now, return DISCORD
        # In production, this could resolve to actual Discord username via API
        return "DISCORD"

    def _get_discord_username(self, discord_user_id: str | None) -> str | None:
        """
        Get Discord username from user ID.

        Args:
            discord_user_id: Discord user ID

        Returns:
            Username string or None
        """
        if not discord_user_id:
            return None
        # For now, return None
        # In production, this could resolve to actual Discord username via API
        return None


# Discord integration adapter functions
def send_discord_message(agent: str, message: str, priority: str = "regular") -> bool:
    """Send message via Discord integration (wraps ConsolidatedMessagingService)."""
    service = ConsolidatedMessagingService()
    result = service.send_message(
        agent, message, priority, use_pyautogui=False)
    return result.get("success", False)


def broadcast_discord_message(message: str, priority: str = "regular") -> dict[str, Any]:
    """Broadcast message via Discord integration."""
    service = ConsolidatedMessagingService()
    return service.broadcast_message(message, priority)

