#!/usr/bin/env python3
"""
Discord Channel Messenger - Webhook-based Agent Communication
===============================================================

Uses configured Discord webhooks to send messages to agent-specific channels.
Replaces PyAutoGUI approach with direct webhook posting.

Environment Variables Used:
- DISCORD_CHANNEL_AGENT_1 through DISCORD_CHANNEL_AGENT_8
- DISCORD_WEBHOOK_AGENT_1 through DISCORD_WEBHOOK_AGENT_8

V2 Compliant: Direct webhook communication
Author: Agent-2 (Architecture & Design Specialist)
Date: 2026-01-12
"""

import json
import logging
import os
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)


class DiscordChannelMessenger:
    """
    Handles agent-to-agent communication via Discord webhooks.

    Uses the agent-specific webhook URLs configured in environment variables
    to post messages directly to dedicated Discord channels.
    """

    def __init__(self):
        """Initialize with agent webhook configuration."""
        self.agent_webhooks = self._load_agent_webhooks()
        self.agent_channels = self._load_agent_channels()
        self.max_retries = 3
        self.timeout = 10

    def _load_agent_webhooks(self) -> Dict[str, str]:
        """Load agent webhook URLs from environment variables."""
        webhooks = {}
        for i in range(1, 9):  # Agent-1 through Agent-8
            agent_id = f"Agent-{i}"
            webhook_var = f"DISCORD_WEBHOOK_AGENT_{i}"
            webhook_url = os.getenv(webhook_var)

            if webhook_url:
                webhooks[agent_id] = webhook_url
                logger.debug(f"Loaded webhook for {agent_id}")
            else:
                logger.warning(f"Missing webhook for {agent_id}: {webhook_var}")

        logger.info(f"Loaded {len(webhooks)} agent webhooks")
        return webhooks

    def _load_agent_channels(self) -> Dict[str, str]:
        """Load agent channel IDs from environment variables."""
        channels = {}
        for i in range(1, 9):  # Agent-1 through Agent-8
            agent_id = f"Agent-{i}"
            channel_var = f"DISCORD_CHANNEL_AGENT_{i}"
            channel_id = os.getenv(channel_var)

            if channel_id:
                channels[agent_id] = channel_id
                logger.debug(f"Loaded channel for {agent_id}: {channel_id}")
            else:
                logger.warning(f"Missing channel ID for {agent_id}: {channel_var}")

        logger.info(f"Loaded {len(channels)} agent channels")
        return channels

    def _post_to_webhook(self, webhook_url: str, message: str, username: str = "Swarm Commander") -> bool:
        """
        Post message to Discord webhook.

        Args:
            webhook_url: Discord webhook URL
            message: Message content
            username: Display name for the webhook

        Returns:
            True if successful, False otherwise
        """
        payload = {
            "content": message,
            "username": username,
            "allowed_mentions": {
                "parse": ["roles", "users", "everyone"]
            }
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    webhook_url,
                    json=payload,
                    timeout=self.timeout,
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 204:  # Discord success response
                    logger.info(f"Message posted successfully to webhook")
                    return True
                elif response.status_code == 429:  # Rate limited
                    retry_after = int(response.headers.get('Retry-After', 5))
                    logger.warning(f"Rate limited, retrying in {retry_after}s")
                    import time
                    time.sleep(retry_after)
                    continue
                else:
                    logger.error(f"Webhook failed: {response.status_code} - {response.text}")
                    return False

            except requests.exceptions.RequestException as e:
                logger.error(f"Webhook request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue

        return False

    async def send_message_to_agent(
        self,
        agent_id: str,
        message: str,
        priority: str = "regular",
        sender: str = "Discord Bot"
    ) -> bool:
        """
        Send message to specific agent via their Discord webhook.

        Args:
            agent_id: Target agent (e.g., "Agent-1")
            message: Message content
            priority: Message priority level
            sender: Who sent the message

        Returns:
            True if message was sent successfully
        """
        if agent_id not in self.agent_webhooks:
            logger.error(f"No webhook configured for agent: {agent_id}")
            logger.info(f"Available agents: {list(self.agent_webhooks.keys())}")
            return False

        webhook_url = self.agent_webhooks[agent_id]

        # Format message with metadata
        formatted_message = f"**{sender}** → **{agent_id}**\n" \
                           f"*Priority: {priority}*\n\n" \
                           f"{message}"

        logger.info(f"Sending message to {agent_id} via Discord webhook")

        success = self._post_to_webhook(
            webhook_url=webhook_url,
            message=formatted_message,
            username=f"Swarm Commander ({sender})"
        )

        if success:
            logger.info(f"Message successfully delivered to {agent_id}")
        else:
            logger.error(f"Failed to deliver message to {agent_id}")

        return success

    async def broadcast_to_all_agents(
        self,
        message: str,
        priority: str = "regular",
        sender: str = "Discord Bot",
        exclude_agent: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Broadcast message to all agents via their webhooks.

        Args:
            message: Message content
            priority: Message priority level
            sender: Who sent the message
            exclude_agent: Agent to exclude from broadcast (optional)

        Returns:
            Dict mapping agent_id to success status
        """
        results = {}
        broadcast_message = f"**📢 BROADCAST** from **{sender}**\n" \
                           f"*Priority: {priority}*\n\n" \
                           f"{message}"

        logger.info(f"Broadcasting message to all agents")

        for agent_id, webhook_url in self.agent_webhooks.items():
            if exclude_agent and agent_id == exclude_agent:
                logger.debug(f"Skipping {agent_id} (excluded)")
                results[agent_id] = True  # Consider skipped as successful
                continue

            success = self._post_to_webhook(
                webhook_url=webhook_url,
                message=broadcast_message,
                username=f"Swarm Broadcast ({sender})"
            )

            results[agent_id] = success

            if success:
                logger.debug(f"Broadcast delivered to {agent_id}")
            else:
                logger.error(f"Broadcast failed to {agent_id}")

        successful_count = sum(1 for success in results.values() if success)
        total_count = len(results)

        logger.info(f"Broadcast complete: {successful_count}/{total_count} agents received message")

        return results

    def get_agent_status(self) -> Dict[str, Dict[str, str]]:
        """
        Get status of all configured agents.

        Returns:
            Dict with agent status information
        """
        status = {}

        for agent_id in [f"Agent-{i}" for i in range(1, 9)]:
            agent_status = {
                "webhook_configured": agent_id in self.agent_webhooks,
                "channel_configured": agent_id in self.agent_channels,
            }

            if agent_id in self.agent_channels:
                agent_status["channel_id"] = self.agent_channels[agent_id]
            else:
                agent_status["channel_id"] = None

            status[agent_id] = agent_status

        return status

    def validate_configuration(self) -> Dict[str, any]:
        """
        Validate that all required environment variables are configured.

        Returns:
            Validation results
        """
        validation = {
            "valid": True,
            "configured_agents": [],
            "missing_webhooks": [],
            "missing_channels": [],
            "total_agents": 8
        }

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            webhook_var = f"DISCORD_WEBHOOK_AGENT_{i}"
            channel_var = f"DISCORD_CHANNEL_AGENT_{i}"

            has_webhook = os.getenv(webhook_var) is not None
            has_channel = os.getenv(channel_var) is not None

            if has_webhook and has_channel:
                validation["configured_agents"].append(agent_id)
            else:
                if not has_webhook:
                    validation["missing_webhooks"].append(agent_id)
                if not has_channel:
                    validation["missing_channels"].append(agent_id)
                validation["valid"] = False

        validation["configured_count"] = len(validation["configured_agents"])
        validation["success_rate"] = validation["configured_count"] / validation["total_agents"]

        logger.info(f"Configuration validation: {validation['configured_count']}/{validation['total_agents']} agents configured")

        return validation