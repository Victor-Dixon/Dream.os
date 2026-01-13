#!/usr/bin/env python3
"""
Discord Event Bridge - Hybrid System Integration
===============================================

Event-driven bridge between Discord messaging and the event bus system.
Enables the hybrid architecture: PyAutoGUI autonomous execution + Discord swarm coordination.

<!-- SSOT Domain: discord_event_bridge -->

Features:
- Publishes Discord messages as events to the event bus
- Subscribes to events and posts responses to Discord
- Event-driven command processing
- Real-time swarm coordination via events

Author: Agent-2 (Architecture & Design Specialist)
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from ..core.infrastructure.event_models import Event, create_event
from ..core.infrastructure.event_bus import get_event_bus
from .discord_channel_messenger import DiscordChannelMessenger

logger = logging.getLogger(__name__)


class DiscordEventBridge:
    """
    Event-driven bridge between Discord and the event bus system.

    Enables the hybrid architecture where:
    - Discord provides swarm visibility and coordination
    - Event bus enables autonomous execution coordination
    - PyAutoGUI handles actual execution tasks
    """

    def __init__(self, discord_bot=None):
        """
        Initialize the Discord event bridge.

        Args:
            discord_bot: Discord bot instance for bidirectional communication
        """
        self.discord_bot = discord_bot
        self.event_bus = get_event_bus()
        self.channel_messenger = DiscordChannelMessenger()

        # Event subscriptions
        self.active_subscriptions = []

        # Message processing callbacks
        self.message_processors = {}

        # Bridge configuration
        self.event_prefix = "discord"
        self.bridge_enabled = True

    async def initialize(self):
        """
        Initialize the event bridge and register subscriptions.
        """
        if not self.bridge_enabled:
            logger.info("Discord event bridge disabled")
            return

        try:
            # Initialize event bus if needed
            await self.event_bus.initialize()

            # Register event subscriptions for Discord responses
            await self._register_event_subscriptions()

            logger.info("Discord event bridge initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Discord event bridge: {e}")
            raise

    async def shutdown(self):
        """
        Shutdown the event bridge and cleanup subscriptions.
        """
        # Remove all subscriptions
        for subscription_id in self.active_subscriptions:
            try:
                await self.event_bus.unsubscribe(subscription_id)
            except Exception as e:
                logger.error(f"Error removing subscription {subscription_id}: {e}")

        self.active_subscriptions.clear()
        logger.info("Discord event bridge shutdown complete")

    async def _register_event_subscriptions(self):
        """
        Register event subscriptions for Discord responses.
        """
        # Subscribe to Discord response events
        subscription = await self.event_bus.subscribe_to_events({
            'subscription_id': f"discord_bridge_{datetime.now().isoformat()}",
            'event_patterns': [f"{self.event_prefix}:response:*"],
            'callback': self._handle_discord_response_event
        })
        self.active_subscriptions.append(subscription)

        # Subscribe to system status events
        subscription = await self.event_bus.subscribe_to_events({
            'subscription_id': f"discord_system_status_{datetime.now().isoformat()}",
            'event_patterns': ["system:status:*"],
            'callback': self._handle_system_status_event
        })
        self.active_subscriptions.append(subscription)

        # Subscribe to agent coordination events
        subscription = await self.event_bus.subscribe_to_events({
            'subscription_id': f"discord_agent_coord_{datetime.now().isoformat()}",
            'event_patterns': ["agent:coordination:*", "swarm:coordination:*"],
            'callback': self._handle_agent_coordination_event
        })
        self.active_subscriptions.append(subscription)

        logger.info(f"Registered {len(self.active_subscriptions)} event subscriptions")

    async def publish_discord_message_event(self,
                                           message_content: str,
                                           author: str,
                                           channel: str,
                                           message_id: Optional[str] = None,
                                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Publish a Discord message as an event to the event bus.

        Args:
            message_content: The message content
            author: Message author identifier
            channel: Discord channel identifier
            message_id: Optional Discord message ID
            metadata: Additional metadata

        Returns:
            Event ID of the published event
        """
        if not self.bridge_enabled:
            return None

        try:
            # Create event data
            event_data = {
                'content': message_content,
                'author': author,
                'channel': channel,
                'message_id': message_id,
                'timestamp': datetime.now().isoformat(),
                'source': 'discord'
            }

            if metadata:
                event_data.update(metadata)

            # Determine event type based on message content
            event_type = self._classify_message_event(message_content)

            # Create and publish event
            event = create_event(
                event_type=f"{self.event_prefix}:{event_type}",
                source_service="discord_bridge",
                data=event_data,
                correlation_id=message_id
            )

            event_id = await self.event_bus.publish_event(event)
            logger.debug(f"Published Discord message event: {event_id}")
            return event_id

        except Exception as e:
            logger.error(f"Failed to publish Discord message event: {e}")
            return None

    def _classify_message_event(self, message_content: str) -> str:
        """
        Classify Discord message to determine event type.

        Args:
            message_content: Message content to classify

        Returns:
            Event type classification
        """
        content_lower = message_content.lower().strip()

        # Check for coordination messages
        if any(keyword in content_lower for keyword in ['coordination', 'a2a', 'swarm', 'bilateral']):
            return 'coordination'

        # Check for commands
        if content_lower.startswith('!'):
            return 'command'

        # Check for status requests
        if any(keyword in content_lower for keyword in ['status', 'health', 'ping']):
            return 'status'

        # Check for coordination responses
        if 'accept' in content_lower or 'decline' in content_lower:
            return 'coordination_response'

        # Default to general message
        return 'message'

    async def _handle_discord_response_event(self, event: Event):
        """
        Handle events that should trigger Discord responses.

        Args:
            event: Event containing response data
        """
        try:
            event_data = event.data

            # Extract target information
            target_agent = event_data.get('target_agent')
            response_content = event_data.get('response')
            channel = event_data.get('channel', 'general')

            if not target_agent or not response_content:
                logger.warning(f"Missing target_agent or response in event: {event.event_id}")
                return

            # Send response via Discord
            success = await self._send_discord_response(target_agent, response_content, channel)

            if success:
                logger.info(f"Discord response sent to {target_agent} for event {event.event_id}")
            else:
                logger.error(f"Failed to send Discord response to {target_agent}")

        except Exception as e:
            logger.error(f"Error handling Discord response event: {e}")

    async def _handle_system_status_event(self, event: Event):
        """
        Handle system status events by posting to Discord.

        Args:
            event: System status event
        """
        try:
            status_data = event.data

            # Create status message
            status_message = f"🖥️ **System Status Update**\n"
            status_message += f"• Service: {status_data.get('service', 'unknown')}\n"
            status_message += f"• Status: {status_data.get('status', 'unknown')}\n"
            status_message += f"• Timestamp: {status_data.get('timestamp', 'unknown')}\n"

            if 'metrics' in status_data:
                metrics = status_data['metrics']
                status_message += f"• Active: {metrics.get('active_subscriptions', 0)} subscriptions\n"
                status_message += f"• Events: {metrics.get('events_published', 0)} published\n"

            # Send to general coordination channel (could be configurable)
            await self._send_discord_response('general', status_message, 'coordination')

        except Exception as e:
            logger.error(f"Error handling system status event: {e}")

    async def _handle_agent_coordination_event(self, event: Event):
        """
        Handle agent coordination events by posting coordination updates.

        Args:
            event: Agent coordination event
        """
        try:
            coord_data = event.data

            # Create coordination message
            coord_message = f"🤝 **Agent Coordination Update**\n"
            coord_message += f"• Event: {event.event_type}\n"
            coord_message += f"• Agents: {coord_data.get('agents', 'unknown')}\n"
            coord_message += f"• Action: {coord_data.get('action', 'unknown')}\n"

            if 'timeline' in coord_data:
                coord_message += f"• Timeline: {coord_data.get('timeline')}\n"

            if 'status' in coord_data:
                coord_message += f"• Status: {coord_data.get('status')}\n"

            # Send to coordination channel
            await self._send_discord_response('coordination', coord_message, 'coordination')

        except Exception as e:
            logger.error(f"Error handling agent coordination event: {e}")

    async def _send_discord_response(self, target: str, content: str, channel: str = 'general') -> bool:
        """
        Send a response to Discord via the appropriate channel.

        Args:
            target: Target agent or channel identifier
            content: Response content
            channel: Target channel

        Returns:
            True if successful
        """
        try:
            # Format the response with bridge metadata
            formatted_content = f"🔄 **Event Bridge Response**\n{content}"

            # Use channel messenger to send to appropriate agent/channel
            if target.startswith('Agent-'):
                # Send to specific agent channel
                success = await self.channel_messenger.send_to_agent(target, formatted_content)
            else:
                # Send to general channel (would need channel mapping)
                logger.info(f"Would send to {channel} channel: {formatted_content[:100]}...")
                success = True  # Placeholder - would implement channel-specific sending

            return success

        except Exception as e:
            logger.error(f"Failed to send Discord response: {e}")
            return False

    def register_message_processor(self, event_type: str, processor: Callable):
        """
        Register a message processor for specific event types.

        Args:
            event_type: Event type to process
            processor: Async callable that processes the event
        """
        self.message_processors[event_type] = processor
        logger.info(f"Registered message processor for event type: {event_type}")

    async def process_incoming_discord_message(self,
                                             message_content: str,
                                             author: str,
                                             channel: str,
                                             message_id: str = None) -> Optional[str]:
        """
        Process an incoming Discord message through the event bridge.

        Args:
            message_content: The Discord message content
            author: Message author
            channel: Discord channel
            message_id: Discord message ID

        Returns:
            Event ID if processed, None otherwise
        """
        # Publish as event
        event_id = await self.publish_discord_message_event(
            message_content=message_content,
            author=author,
            channel=channel,
            message_id=message_id
        )

        # Check if we have a specific processor for this message type
        event_type = self._classify_message_event(message_content)
        if event_type in self.message_processors:
            try:
                # Create event object for processing
                event_data = {
                    'content': message_content,
                    'author': author,
                    'channel': channel,
                    'message_id': message_id,
                    'event_type': f"{self.event_prefix}:{event_type}"
                }

                event = Event(
                    event_type=f"{self.event_prefix}:{event_type}",
                    source_service="discord_bridge",
                    data=event_data,
                    event_id=event_id
                )

                # Process with registered processor
                await self.message_processors[event_type](event)

            except Exception as e:
                logger.error(f"Error in message processor for {event_type}: {e}")

        return event_id

    async def publish_system_event(self,
                                  event_type: str,
                                  event_data: Dict[str, Any],
                                  correlation_id: Optional[str] = None) -> str:
        """
        Publish a system event through the bridge.

        Args:
            event_type: Type of system event
            event_data: Event data payload
            correlation_id: Optional correlation ID

        Returns:
            Event ID
        """
        event = create_event(
            event_type=f"system:{event_type}",
            source_service="discord_bridge",
            data=event_data,
            correlation_id=correlation_id
        )

        event_id = await self.event_bus.publish_event(event)
        logger.debug(f"Published system event: {event_id}")
        return event_id

    async def get_bridge_status(self) -> Dict[str, Any]:
        """
        Get the current status of the event bridge.

        Returns:
            Bridge status information
        """
        return {
            'enabled': self.bridge_enabled,
            'active_subscriptions': len(self.active_subscriptions),
            'registered_processors': len(self.message_processors),
            'event_bus_connected': self.event_bus is not None,
            'discord_bot_connected': self.discord_bot is not None,
            'timestamp': datetime.now().isoformat()
        }

    async def enable_bridge(self):
        """Enable the event bridge."""
        self.bridge_enabled = True
        logger.info("Discord event bridge enabled")

    async def disable_bridge(self):
        """Disable the event bridge."""
        self.bridge_enabled = False
        logger.info("Discord event bridge disabled")


# Global bridge instance
_discord_bridge_instance = None


def get_discord_event_bridge(discord_bot=None) -> DiscordEventBridge:
    """
    Get the global Discord event bridge instance.

    Args:
        discord_bot: Optional Discord bot instance

    Returns:
        DiscordEventBridge instance
    """
    global _discord_bridge_instance
    if _discord_bridge_instance is None:
        _discord_bridge_instance = DiscordEventBridge(discord_bot)
    return _discord_bridge_instance


async def initialize_discord_event_bridge(discord_bot=None):
    """
    Initialize the global Discord event bridge.

    Args:
        discord_bot: Optional Discord bot instance

    Returns:
        Initialized DiscordEventBridge
    """
    bridge = get_discord_event_bridge(discord_bot)
    await bridge.initialize()
    return bridge


async def shutdown_discord_event_bridge():
    """Shutdown the global Discord event bridge."""
    global _discord_bridge_instance
    if _discord_bridge_instance:
        await _discord_bridge_instance.shutdown()
        _discord_bridge_instance = None