#!/usr/bin/env python3
"""
🎯 UNIFIED MESSAGING SSOT - SINGLE SOURCE OF TRUTH
==================================================

The ONE AND ONLY messaging system for Agent Cellphone V2.

CONSOLIDATES ALL MESSAGING FUNCTIONALITY:
- PyAutoGUI agent control
- Discord webhooks
- Devlog coordination
- Message queuing
- Bilateral coordination
- Swarm broadcasting

SSOT Principle: One system, one truth, zero confusion.

Author: Agent-4 (Messaging SSOT Consolidation Specialist)
Date: 2026-01-15
"""

import logging
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Protocol
from dataclasses import dataclass, field
from enum import Enum

# Remove all the broken imports and conflicting dependencies
# This SSOT system is self-contained

logger = logging.getLogger(__name__)

class MessagePriority(Enum):
    """Unified message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class MessageType(Enum):
    """Unified message types."""
    COORDINATION = "coordination"
    TASK = "task"
    STATUS = "status"
    BROADCAST = "broadcast"
    ALERT = "alert"

class DeliveryMethod(Enum):
    """Supported delivery methods."""
    PYAUTOGUI = "pyautogui"
    DEVLOG = "devlog"
    DISCORD = "discord"
    WORKSPACE = "workspace"
    HYBRID = "hybrid"

@dataclass
class UnifiedMessage:
    """Single source of truth message format."""
    message_id: str
    sender: str
    recipient: str
    content: str
    priority: MessagePriority = MessagePriority.NORMAL
    message_type: MessageType = MessageType.COORDINATION
    delivery_methods: List[DeliveryMethod] = field(default_factory=lambda: [DeliveryMethod.HYBRID])
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "priority": self.priority.value,
            "message_type": self.message_type.value,
            "delivery_methods": [dm.value for dm in self.delivery_methods],
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "tags": self.tags
        }

class MessageDeliveryResult:
    """Result of message delivery attempt."""
    def __init__(self, method: DeliveryMethod, success: bool, error: Optional[str] = None):
        self.method = method
        self.success = success
        self.error = error
        self.timestamp = datetime.now()

class IMessageDelivery(Protocol):
    """SSOT Message delivery interface."""
    def deliver_message(self, message: UnifiedMessage) -> MessageDeliveryResult:
        """Deliver a message via this method."""
        ...

class PyAutoGUIDeliveryService:
    """PyAutoGUI-based agent control delivery."""

    def __init__(self):
        self.agent_coordinates = self._load_agent_coordinates()

    def _load_agent_coordinates(self) -> Dict[str, Dict[str, int]]:
        """Load agent screen coordinates."""
        coords_file = Path("cursor_agent_coords.json")
        if coords_file.exists():
            try:
                with open(coords_file, 'r') as f:
                    data = json.load(f)
                    # Convert from the actual file format to expected format
                    coords = {}
                    for agent_name, agent_data in data.get("agents", {}).items():
                        if "chat_input_coordinates" in agent_data:
                            coords[agent_name] = {
                                "x": agent_data["chat_input_coordinates"][0],
                                "y": agent_data["chat_input_coordinates"][1]
                            }
                    if coords:  # Only return if we found coordinates
                        return coords
            except Exception as e:
                logger.warning(f"Could not load coordinates: {e}")

        # Default coordinates if file not found or parsing failed
        return {
            "Agent-1": {"x": -1269, "y": 481},
            "Agent-2": {"x": -308, "y": 480},
            "Agent-3": {"x": -1269, "y": 1001},
            "Agent-4": {"x": -308, "y": 1000},
            "Agent-5": {"x": 652, "y": 421},
            "Agent-6": {"x": 1619, "y": 420},
            "Agent-7": {"x": 653, "y": 940},
            "Agent-8": {"x": 1611, "y": 941}
        }

    def deliver_message(self, message: UnifiedMessage) -> MessageDeliveryResult:
        """Deliver message via PyAutoGUI agent control."""
        try:
            # Import PyAutoGUI only when needed to avoid dependency issues
            import pyautogui
            import pyperclip

            agent = message.recipient
            if agent not in self.agent_coordinates:
                return MessageDeliveryResult(
                    DeliveryMethod.PYAUTOGUI,
                    False,
                    f"No coordinates found for agent {agent}"
                )

            coords = self.agent_coordinates[agent]

            # Copy message to clipboard
            pyperclip.copy(message.content)

            # Move to agent position and paste
            pyautogui.moveTo(coords["x"], coords["y"], duration=0.5)
            pyautogui.click()

            # Small delay for focus
            time.sleep(0.2)

            # Paste message
            pyautogui.hotkey('ctrl', 'v')

            # Send message
            pyautogui.press('enter')

            logger.info(f"✅ PyAutoGUI delivery successful to {agent}")
            return MessageDeliveryResult(DeliveryMethod.PYAUTOGUI, True)

        except ImportError:
            return MessageDeliveryResult(
                DeliveryMethod.PYAUTOGUI,
                False,
                "PyAutoGUI not available"
            )
        except Exception as e:
            logger.error(f"❌ PyAutoGUI delivery failed: {e}")
            return MessageDeliveryResult(
                DeliveryMethod.PYAUTOGUI,
                False,
                str(e)
            )

class DevlogDeliveryService:
    """Devlog-based message delivery."""

    def __init__(self):
        self.devlogs_dir = Path("../../../agent-tools/devlogs")

    def deliver_message(self, message: UnifiedMessage) -> MessageDeliveryResult:
        """Deliver message via devlog system."""
        try:
            self.devlogs_dir.mkdir(exist_ok=True)

            # Create devlog filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}_{message.sender}_to_{message.recipient}_{message.message_type.value}.md"

            devlog_path = self.devlogs_dir / filename

            # Format message content
            content = f"""# 📬 MESSAGE DELIVERY: {message.sender} → {message.recipient}

**Message ID:** {message.message_id}
**Priority:** {message.priority.value.upper()}
**Type:** {message.message_type.value.title()}
**Timestamp:** {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

## Content

{message.content}

## Metadata

- **Correlation ID:** {message.correlation_id or 'N/A'}
- **Tags:** {', '.join(message.tags) if message.tags else 'None'}
- **Delivery Methods:** {', '.join(dm.value for dm in message.delivery_methods)}

---
*Delivered via Unified Messaging SSOT - Devlog System*
"""

            with open(devlog_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ Devlog delivery successful: {filename}")
            return MessageDeliveryResult(DeliveryMethod.DEVLOG, True)

        except Exception as e:
            logger.error(f"❌ Devlog delivery failed: {e}")
            return MessageDeliveryResult(
                DeliveryMethod.DEVLOG,
                False,
                str(e)
            )

class WorkspaceDeliveryService:
    """Agent workspace inbox delivery."""

    def __init__(self):
        self.workspace_base = Path("agent_workspaces")

    def deliver_message(self, message: UnifiedMessage) -> MessageDeliveryResult:
        """Deliver message to agent workspace inbox."""
        try:
            agent_workspace = self.workspace_base / message.recipient
            inbox_dir = agent_workspace / "inbox"

            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create inbox message filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"MESSAGE_{timestamp}_{message.sender}_{message.message_type.value.upper()}.md"

            inbox_path = inbox_dir / filename

            # Format message content
            content = f"""# 📨 WORKSPACE MESSAGE: {message.sender} → {message.recipient}

**Message ID:** {message.message_id}
**Priority:** {message.priority.value.upper()}
**Type:** {message.message_type.value.title()}
**Timestamp:** {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

## Message Content

{message.content}

## Message Details

- **Sender:** {message.sender}
- **Recipient:** {message.recipient}
- **Correlation ID:** {message.correlation_id or 'N/A'}
- **Tags:** {', '.join(message.tags) if message.tags else 'None'}

## Action Required

Please review this message and take appropriate action based on priority and content.

---
*Delivered via Unified Messaging SSOT - Workspace Inbox*
*File: {filename}*
"""

            with open(inbox_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ Workspace delivery successful: {message.recipient}/inbox/{filename}")
            return MessageDeliveryResult(DeliveryMethod.WORKSPACE, True)

        except Exception as e:
            logger.error(f"❌ Workspace delivery failed: {e}")
            return MessageDeliveryResult(
                DeliveryMethod.WORKSPACE,
                False,
                str(e)
            )

class DiscordDeliveryService:
    """Discord webhook delivery service."""

    def __init__(self):
        self.webhooks = self._load_discord_webhooks()

    def _load_discord_webhooks(self) -> Dict[str, str]:
        """Load Discord webhooks from environment."""
        webhooks = {}

        # Try to load from .env.discord file
        env_discord = Path(".env.discord")
        if env_discord.exists():
            try:
                import dotenv
                dotenv.load_dotenv(env_discord)
            except ImportError:
                pass

        # Load webhook URLs from environment
        for agent in ["Agent-1", "Agent-2", "Agent-5", "Agent-6", "Agent-8"]:
            webhook_env = f"{agent.upper()}_WEBHOOK_URL"
            webhook_url = os.getenv(webhook_env)
            if webhook_url:
                webhooks[agent] = webhook_url

        return webhooks

    def deliver_message(self, message: UnifiedMessage) -> MessageDeliveryResult:
        """Deliver message via Discord webhook."""
        try:
            agent = message.recipient
            if agent not in self.webhooks:
                return MessageDeliveryResult(
                    DeliveryMethod.DISCORD,
                    False,
                    f"No Discord webhook configured for {agent}"
                )

            webhook_url = self.webhooks[agent]

            # Prepare Discord message payload
            payload = {
                "content": f"📬 **Message from {message.sender}**\n\n{message.content}",
                "embeds": [{
                    "title": f"{message.message_type.value.title()} Message",
                    "description": f"Priority: {message.priority.value.upper()}",
                    "color": self._get_priority_color(message.priority),
                    "fields": [
                        {
                            "name": "Message ID",
                            "value": message.message_id,
                            "inline": True
                        },
                        {
                            "name": "Timestamp",
                            "value": message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "Unified Messaging SSOT"
                    }
                }]
            }

            # Send via webhook
            import requests
            response = requests.post(webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                logger.info(f"✅ Discord delivery successful to {agent}")
                return MessageDeliveryResult(DeliveryMethod.DISCORD, True)
            else:
                return MessageDeliveryResult(
                    DeliveryMethod.DISCORD,
                    False,
                    f"Discord API error: {response.status_code}"
                )

        except ImportError:
            return MessageDeliveryResult(
                DeliveryMethod.DISCORD,
                False,
                "requests library not available for Discord webhooks"
            )
        except Exception as e:
            logger.error(f"❌ Discord delivery failed: {e}")
            return MessageDeliveryResult(
                DeliveryMethod.DISCORD,
                False,
                str(e)
            )

    def _get_priority_color(self, priority: MessagePriority) -> int:
        """Get Discord embed color based on priority."""
        colors = {
            MessagePriority.LOW: 0x00FF00,      # Green
            MessagePriority.NORMAL: 0xFFFF00,   # Yellow
            MessagePriority.HIGH: 0xFFA500,    # Orange
            MessagePriority.URGENT: 0xFF0000   # Red
        }
        return colors.get(priority, 0x0000FF)  # Blue default

class UnifiedMessagingSSOT:
    """Single Source of Truth for all messaging operations."""

    def __init__(self):
        self.delivery_services = {
            DeliveryMethod.PYAUTOGUI: PyAutoGUIDeliveryService(),
            DeliveryMethod.DEVLOG: DevlogDeliveryService(),
            DeliveryMethod.WORKSPACE: WorkspaceDeliveryService(),
            DeliveryMethod.DISCORD: DiscordDeliveryService(),
        }

        # Initialize message queue for reliability
        self.message_queue = []
        self.delivery_history = []

        logger.info("🎯 Unified Messaging SSOT initialized")

    def send_message(
        self,
        recipient: str,
        content: str,
        sender: str = "SYSTEM",
        priority: MessagePriority = MessagePriority.NORMAL,
        message_type: MessageType = MessageType.COORDINATION,
        delivery_methods: Optional[List[DeliveryMethod]] = None,
        correlation_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a message using the unified SSOT system.

        This is the ONE method to send messages in Agent Cellphone V2.
        All other messaging methods are deprecated.
        """
        import uuid

        # Create unified message
        message = UnifiedMessage(
            message_id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            content=content,
            priority=priority,
            message_type=message_type,
            delivery_methods=delivery_methods or [DeliveryMethod.HYBRID],
            correlation_id=correlation_id,
            tags=tags or [],
            metadata=metadata or {}
        )

        # Deliver message via specified methods
        delivery_results = []
        overall_success = False

        for method in message.delivery_methods:
            if method == DeliveryMethod.HYBRID:
                # Hybrid means try all available methods
                for service_method, service in self.delivery_services.items():
                    result = service.deliver_message(message)
                    delivery_results.append(result)
                    if result.success:
                        overall_success = True
            else:
                # Use specific delivery method
                if method in self.delivery_services:
                    result = self.delivery_services[method].deliver_message(message)
                    delivery_results.append(result)
                    if result.success:
                        overall_success = True

        # Record delivery history
        self.delivery_history.append({
            "message": message.to_dict(),
            "results": [{"method": r.method.value, "success": r.success, "error": r.error, "timestamp": r.timestamp.isoformat()} for r in delivery_results],
            "overall_success": overall_success
        })

        # Return comprehensive result
        result = {
            "message_id": message.message_id,
            "overall_success": overall_success,
            "delivery_results": [
                {
                    "method": r.method.value,
                    "success": r.success,
                    "error": r.error
                } for r in delivery_results
            ],
            "timestamp": message.timestamp.isoformat()
        }

        if overall_success:
            logger.info(f"✅ Message {message.message_id} delivered successfully to {recipient}")
        else:
            logger.warning(f"⚠️ Message {message.message_id} delivery failed to {recipient}")

        return result

    def broadcast_message(
        self,
        content: str,
        sender: str = "SYSTEM",
        recipients: Optional[List[str]] = None,
        priority: MessagePriority = MessagePriority.NORMAL,
        message_type: MessageType = MessageType.BROADCAST,
        **kwargs
    ) -> Dict[str, Any]:
        """Broadcast message to multiple recipients."""
        if recipients is None:
            recipients = ["Agent-1", "Agent-2", "Agent-5", "Agent-6", "Agent-8"]

        results = []
        for recipient in recipients:
            result = self.send_message(
                recipient=recipient,
                content=content,
                sender=sender,
                priority=priority,
                message_type=message_type,
                **kwargs
            )
            results.append({
                "recipient": recipient,
                "result": result
            })

        overall_success = any(r["result"]["overall_success"] for r in results)

        return {
            "broadcast_id": f"broadcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "recipients": recipients,
            "individual_results": results,
            "overall_success": overall_success,
            "successful_deliveries": sum(1 for r in results if r["result"]["overall_success"]),
            "total_recipients": len(recipients)
        }

    def get_delivery_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent delivery history."""
        return self.delivery_history[-limit:] if self.delivery_history else []

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics."""
        if not self.delivery_history:
            return {"total_messages": 0, "success_rate": 0.0}

        total_messages = len(self.delivery_history)
        successful_messages = sum(1 for h in self.delivery_history if h["overall_success"])
        success_rate = successful_messages / total_messages if total_messages > 0 else 0

        # Method-specific stats
        method_stats = {}
        for history in self.delivery_history:
            for result in history["results"]:
                method = result["method"]
                if method not in method_stats:
                    method_stats[method] = {"attempts": 0, "successes": 0}
                method_stats[method]["attempts"] += 1
                if result["success"]:
                    method_stats[method]["successes"] += 1

        return {
            "total_messages": total_messages,
            "successful_messages": successful_messages,
            "success_rate": round(success_rate * 100, 2),
            "method_stats": method_stats
        }

# Global SSOT instance
_messaging_ssot = None

def get_messaging_ssot() -> UnifiedMessagingSSOT:
    """Get the global messaging SSOT instance (Singleton pattern)."""
    global _messaging_ssot
    if _messaging_ssot is None:
        _messaging_ssot = UnifiedMessagingSSOT()
    return _messaging_ssot

# Convenience functions for easy usage
def send_message(*args, **kwargs) -> Dict[str, Any]:
    """Convenience function to send a message via SSOT."""
    return get_messaging_ssot().send_message(*args, **kwargs)

def broadcast_message(*args, **kwargs) -> Dict[str, Any]:
    """Convenience function to broadcast a message via SSOT."""
    return get_messaging_ssot().broadcast_message(*args, **kwargs)

# Export the core classes and enums for external usage
__all__ = [
    "UnifiedMessagingSSOT",
    "get_messaging_ssot",
    "send_message",
    "broadcast_message",
    "MessagePriority",
    "MessageType",
    "DeliveryMethod",
    "UnifiedMessage"
]