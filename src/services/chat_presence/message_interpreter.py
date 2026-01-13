#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Message Interpreter
==================

Decides which agent should respond to chat messages.
Routes messages based on content, context, and agent availability.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from typing import Optional

from .agent_personality import get_personality, should_agent_respond
from .quote_generator import get_random_quote, format_quote_for_chat

logger = logging.getLogger(__name__)


class MessageInterpreter:
    """
    Interprets chat messages and determines agent response.

    Decision factors:
    - Message content (keywords, topics)
    - Agent personalities and expertise
    - Agent availability/activity
    - Message priority
    - Command prefixes (!agent1, !team)
    """

    def __init__(self):
        """Initialize message interpreter."""
        self.agent_activity = {}  # Track agent activity for rotation

    def determine_responder(
        self, message: str, username: str = "", channel: str = ""
    ) -> Optional[str]:
        """
        Determine which agent should respond.

        Args:
            message: Chat message content
            username: Message sender username
            channel: Channel name

        Returns:
            Agent ID to respond, or None if no response needed
        """
        # Check for explicit agent commands
        explicit_agent = self._check_explicit_command(message)
        if explicit_agent:
            return explicit_agent

        # Check for team/broadcast commands
        if self._is_broadcast_command(message):
            return "BROADCAST"  # Special value for all agents

        # Find best matching agent by content
        best_agent = self._find_best_agent_match(message)

        # Apply activity rotation (fair speaking time)
        if best_agent:
            best_agent = self._apply_activity_rotation(best_agent, message)

        return best_agent

    def _check_explicit_command(self, message: str) -> Optional[str]:
        """
        Check for explicit agent commands.

        Args:
            message: Message content

        Returns:
            Agent ID if explicit command found, None otherwise
        """
        message_lower = message.lower()

        # Check for status commands first (special handling)
        if message_lower.startswith("!status"):
            # Status commands are handled separately
            return None

        # Check for !agent1, !agent-1, etc.
        agent_commands = {
            "!agent1": "Agent-1",
            "!agent-1": "Agent-1",
            "!agent_one": "Agent-1",
            "!agent2": "Agent-2",
            "!agent-2": "Agent-2",
            "!agent_two": "Agent-2",
            "!agent3": "Agent-3",
            "!agent-3": "Agent-3",
            "!agent_three": "Agent-3",
            "!agent4": "Agent-4",
            "!agent-4": "Agent-4",
            "!captain": "Agent-4",
            "!agent_four": "Agent-4",
            "!agent5": "Agent-5",
            "!agent-5": "Agent-5",
            "!agent_five": "Agent-5",
            "!agent6": "Agent-6",
            "!agent-6": "Agent-6",
            "!agent_six": "Agent-6",
            "!agent7": "Agent-7",
            "!agent-7": "Agent-7",
            "!agent_seven": "Agent-7",
            "!agent8": "Agent-8",
            "!agent-8": "Agent-8",
            "!agent_eight": "Agent-8",
        }

        for command, agent_id in agent_commands.items():
            if message_lower.startswith(command):
                return agent_id

        return None

    def is_status_command(self, message: str) -> bool:
        """
        Check if message is a status command.

        Args:
            message: Message content

        Returns:
            True if status command
        """
        message_lower = message.lower().strip()
        # Core status commands
        status_commands = ["!status", "!swarm", "!agents"]
        if any(message_lower.startswith(cmd) for cmd in status_commands):
            return True
        # Aliases like "!team status" / "!swarm status"
        if message_lower.startswith("!team status") or message_lower.startswith("!swarm status"):
            return True
        return False

    def is_quote_command(self, message: str) -> bool:
        """
        Check if message is a quote command.

        Args:
            message: Message content

        Returns:
            True if quote command
        """
        message_lower = message.lower().strip()
        quote_commands = ["!quote", "!quotes", "!wisdom"]
        return any(message_lower.startswith(cmd) for cmd in quote_commands)

    def get_quote_response(self) -> str:
        """
        Get a random quote response.

        Returns:
            Formatted quote string for chat
        """
        quote = get_random_quote()
        return format_quote_for_chat(quote)

    def parse_status_command(self, message: str) -> tuple[str, Optional[str]]:
        """
        Parse status command to determine what status to show.

        Args:
            message: Status command message

        Returns:
            Tuple of (command_type, agent_id)
            command_type: "all" or "agent"
            agent_id: Specific agent ID if requesting single agent, None for all
        """
        message_lower = message.lower().strip()
        parts = message_lower.split()

        # Aliases that should show full team status
        if message_lower.startswith("!team status") or message_lower.startswith("!swarm status"):
            return ("all", None)

        if len(parts) == 1:
            # !status - show all
            return ("all", None)

        # Check for agent specification
        agent_part = parts[1] if len(parts) > 1 else None

        # Try to extract agent ID
        agent_commands = {
            "agent1": "Agent-1",
            "agent-1": "Agent-1",
            "agent_one": "Agent-1",
            "agent2": "Agent-2",
            "agent-2": "Agent-2",
            "agent_two": "Agent-2",
            "agent3": "Agent-3",
            "agent-3": "Agent-3",
            "agent_three": "Agent-3",
            "agent4": "Agent-4",
            "agent-4": "Agent-4",
            "captain": "Agent-4",
            "agent_four": "Agent-4",
            "agent5": "Agent-5",
            "agent-5": "Agent-5",
            "agent_five": "Agent-5",
            "agent6": "Agent-6",
            "agent-6": "Agent-6",
            "agent_six": "Agent-6",
            "agent7": "Agent-7",
            "agent-7": "Agent-7",
            "agent_seven": "Agent-7",
            "agent8": "Agent-8",
            "agent-8": "Agent-8",
            "agent_eight": "Agent-8",
        }

        if agent_part and agent_part in agent_commands:
            return ("agent", agent_commands[agent_part])

        # Default to all if can't parse
        return ("all", None)

    def _is_broadcast_command(self, message: str) -> bool:
        """
        Check if message is a broadcast command.

        Args:
            message: Message content

        Returns:
            True if broadcast command
        """
        message_lower = message.lower().strip()

        # Treat status aliases as pure status, not broadcast
        if message_lower.startswith("!team status") or message_lower.startswith("!swarm status"):
            return False

        broadcast_commands = ["!team", "!swarm",
                              "!all", "!everyone", "!broadcast"]
        return any(message_lower.startswith(cmd) for cmd in broadcast_commands)

    def _find_best_agent_match(self, message: str) -> Optional[str]:
        """
        Find best matching agent by content analysis.

        Args:
            message: Message content

        Returns:
            Best matching agent ID or None
        """
        best_agent = None
        best_score = 0.0

        # Check each agent's personality match
        for agent_id in [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]:
            if should_agent_respond(agent_id, message):
                # Calculate match score
                score = self._calculate_match_score(agent_id, message)

                if score > best_score:
                    best_score = score
                    best_agent = agent_id

        # Only return if score is above threshold
        if best_score > 0.3:
            return best_agent

        return None

    def _calculate_match_score(self, agent_id: str, message: str) -> float:
        """
        Calculate match score for agent and message.

        Args:
            agent_id: Agent identifier
            message: Message content

        Returns:
            Match score (0.0 to 1.0)
        """
        personality = get_personality(agent_id)
        if not personality:
            return 0.0

        message_lower = message.lower()
        score = 0.0

        # Role keyword matching
        role_keywords = {
            "Agent-1": ["integrate", "system", "core", "api"],
            "Agent-2": ["architecture", "design", "pattern"],
            "Agent-3": ["deploy", "infrastructure", "devops"],
            "Agent-4": ["captain", "coordinate", "mission"],
            "Agent-5": ["data", "analytics", "intelligence"],
            "Agent-6": ["coordinate", "team", "swarm"],
            "Agent-7": ["web", "ui", "frontend", "browser"],
            "Agent-8": ["ssot", "source of truth", "integration"],
        }

        keywords = role_keywords.get(agent_id, [])
        matches = sum(1 for keyword in keywords if keyword in message_lower)

        if keywords:
            score = matches / len(keywords)

        return score

    def _apply_activity_rotation(
        self, suggested_agent: str, message: str
    ) -> str:
        """
        Apply activity rotation for fair speaking time.

        Args:
            suggested_agent: Suggested agent from content matching
            message: Message content

        Returns:
            Final agent selection (may differ from suggested)
        """
        # Update activity tracking
        if suggested_agent not in self.agent_activity:
            self.agent_activity[suggested_agent] = 0

        self.agent_activity[suggested_agent] += 1

        # For now, return suggested agent
        # Future: Implement rotation logic based on activity counts
        return suggested_agent

    def should_respond(self, message: str) -> bool:
        """
        Determine if system should respond at all.

        Args:
            message: Message content

        Returns:
            True if response is appropriate
        """
        message_lower = message.lower().strip()

        # Don't respond to empty messages
        if not message_lower:
            return False

        # Don't respond to bot commands only (no content)
        if message_lower.startswith("!") and len(message_lower) < 10:
            return True  # Commands should be handled

        # Respond if message is substantial
        if len(message_lower) > 5:
            return True

        return False

    def get_response_count(self, message: str) -> int:
        """
        Determine how many messages to send.

        Args:
            message: Message content

        Returns:
            Number of response messages (typically 1)
        """
        # For now, always respond with 1 message
        # Future: Could analyze message complexity
        return 1


__all__ = ["MessageInterpreter"]
