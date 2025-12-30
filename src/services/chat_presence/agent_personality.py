#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Agent Chat Personality System
=============================

Defines personality profiles for all 8 agents in chat contexts.
Each agent has a unique voice, tone, and response style.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class PersonalityTone(Enum):
    """Personality tone categories."""

    TECHNICAL = "technical"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    ENTHUSIASTIC = "enthusiastic"
    ANALYTICAL = "analytical"
    COORDINATING = "coordinating"


@dataclass
class AgentPersonality:
    """Personality profile for an agent."""

    agent_id: str
    agent_name: str
    role: str
    tone: PersonalityTone
    greeting_style: str
    response_prefixes: list[str]
    response_suffixes: list[str]
    emoji_usage: str  # "heavy", "moderate", "light", "none"
    technical_depth: str  # "high", "medium", "low"
    max_response_length: int
    personality_traits: list[str]


# Agent Personality Definitions
AGENT_PERSONALITIES: dict[str, AgentPersonality] = {
    "Agent-1": AgentPersonality(
        agent_id="Agent-1",
        agent_name="Integration Specialist",
        role="Integration & Core Systems",
        tone=PersonalityTone.TECHNICAL,
        greeting_style="Direct and efficient",
        response_prefixes=["🔧", "⚙️", "✅"],
        response_suffixes=["Let me integrate that.", "System ready."],
        emoji_usage="moderate",
        technical_depth="high",
        max_response_length=200,
        personality_traits=["precise", "systematic", "integration-focused"],
    ),
    "Agent-2": AgentPersonality(
        agent_id="Agent-2",
        agent_name="Architecture Specialist",
        role="Architecture & Design",
        tone=PersonalityTone.ANALYTICAL,
        greeting_style="Thoughtful and structured",
        response_prefixes=["🏗️", "📐", "💡"],
        response_suffixes=["Architecture optimized.", "Design pattern applied."],
        emoji_usage="light",
        technical_depth="high",
        max_response_length=250,
        personality_traits=["analytical", "design-focused", "pattern-oriented"],
    ),
    "Agent-3": AgentPersonality(
        agent_id="Agent-3",
        agent_name="DevOps Specialist",
        role="Infrastructure & DevOps",
        tone=PersonalityTone.PROFESSIONAL,
        greeting_style="Reliable and infrastructure-focused",
        response_prefixes=["🚀", "🔐", "📊"],
        response_suffixes=["Infrastructure stable.", "Deployment ready."],
        emoji_usage="moderate",
        technical_depth="high",
        max_response_length=200,
        personality_traits=["reliable", "infrastructure-focused", "automation-driven"],
    ),
    "Agent-4": AgentPersonality(
        agent_id="Agent-4",
        agent_name="Captain",
        role="Strategic Oversight",
        tone=PersonalityTone.PROFESSIONAL,
        greeting_style="Authoritative and strategic",
        response_prefixes=["🎯", "⚡", "📋"],
        response_suffixes=["Mission assigned.", "Swarm coordinated."],
        emoji_usage="moderate",
        technical_depth="medium",
        max_response_length=300,
        personality_traits=["strategic", "coordinating", "decision-making"],
    ),
    "Agent-5": AgentPersonality(
        agent_id="Agent-5",
        agent_name="Business Intelligence",
        role="Business Intelligence",
        tone=PersonalityTone.ANALYTICAL,
        greeting_style="Data-driven and insightful",
        response_prefixes=["📈", "📊", "🔍"],
        response_suffixes=["Data analyzed.", "Insights generated."],
        emoji_usage="light",
        technical_depth="medium",
        max_response_length=250,
        personality_traits=["data-focused", "analytical", "insight-driven"],
    ),
    "Agent-6": AgentPersonality(
        agent_id="Agent-6",
        agent_name="Coordination Specialist",
        role="Coordination & Communication",
        tone=PersonalityTone.FRIENDLY,
        greeting_style="Warm and coordinating",
        response_prefixes=["🐝", "🤝", "💬"],
        response_suffixes=["Team coordinated!", "Swarm united!"],
        emoji_usage="heavy",
        technical_depth="low",
        max_response_length=200,
        personality_traits=["friendly", "coordinating", "team-focused"],
    ),
    "Agent-7": AgentPersonality(
        agent_id="Agent-7",
        agent_name="Web Development Specialist",
        role="Web Development",
        tone=PersonalityTone.ENTHUSIASTIC,
        greeting_style="Energetic and web-focused",
        response_prefixes=["🌐", "⚡", "✨"],
        response_suffixes=["UI updated!", "Feature deployed!"],
        emoji_usage="heavy",
        technical_depth="medium",
        max_response_length=200,
        personality_traits=["enthusiastic", "web-focused", "user-experience-driven"],
    ),
    "Agent-8": AgentPersonality(
        agent_id="Agent-8",
        agent_name="SSOT Specialist",
        role="SSOT & System Integration",
        tone=PersonalityTone.TECHNICAL,
        greeting_style="Precise and SSOT-focused",
        response_prefixes=["🔗", "📚", "✅"],
        response_suffixes=["SSOT maintained.", "Integration verified."],
        emoji_usage="moderate",
        technical_depth="high",
        max_response_length=200,
        personality_traits=["precise", "ssot-focused", "integration-verified"],
    ),
}


def get_personality(agent_id: str) -> AgentPersonality | None:
    """
    Get personality profile for an agent.

    Args:
        agent_id: Agent identifier (e.g., "Agent-1")

    Returns:
        AgentPersonality instance or None if not found
    """
    return AGENT_PERSONALITIES.get(agent_id)


def format_chat_message(
    agent_id: str, base_message: str, context: dict | None = None
) -> str:
    """
    Format a message with agent personality applied.

    Args:
        agent_id: Agent identifier
        base_message: Base message content
        context: Optional context (channel, user, etc.)

    Returns:
        Formatted message with personality applied
    """
    personality = get_personality(agent_id)
    if not personality:
        return base_message

    # Select prefix/suffix based on personality
    import random

    prefix = random.choice(personality.response_prefixes) if personality.response_prefixes else ""
    suffix = random.choice(personality.response_suffixes) if personality.response_suffixes else ""

    # Build message with personality
    parts = []
    if prefix:
        parts.append(prefix)

    parts.append(base_message)

    if suffix:
        parts.append(suffix)

    message = " ".join(parts)

    # Apply emoji usage based on personality
    if personality.emoji_usage == "none":
        # Remove emojis
        import re

        message = re.sub(r"[^\w\s.,!?;:-]", "", message)
    elif personality.emoji_usage == "light":
        # Keep only prefix emoji
        pass
    # "moderate" and "heavy" keep all emojis

    # Truncate to max length
    if len(message) > personality.max_response_length:
        message = message[: personality.max_response_length - 3] + "..."

    return message


def should_agent_respond(agent_id: str, message_content: str) -> bool:
    """
    Determine if an agent should respond to a message based on personality.

    Args:
        agent_id: Agent identifier
        message_content: Message content to analyze

    Returns:
        True if agent should respond, False otherwise
    """
    personality = get_personality(agent_id)
    if not personality:
        return False

    # Check if message matches agent's expertise
    message_lower = message_content.lower()

    # Role-based keyword matching
    role_keywords = {
        "Agent-1": ["integrate", "system", "core", "api", "connection"],
        "Agent-2": ["architecture", "design", "pattern", "structure"],
        "Agent-3": ["deploy", "infrastructure", "devops", "ci/cd", "server"],
        "Agent-4": ["captain", "coordinate", "mission", "strategy", "assign"],
        "Agent-5": ["data", "analytics", "intelligence", "metrics", "report"],
        "Agent-6": ["coordinate", "team", "swarm", "communication"],
        "Agent-7": ["web", "ui", "frontend", "browser", "interface"],
        "Agent-8": ["ssot", "source of truth", "integration", "consolidate"],
    }

    keywords = role_keywords.get(agent_id, [])
    return any(keyword in message_lower for keyword in keywords)


__all__ = [
    "AgentPersonality",
    "PersonalityTone",
    "AGENT_PERSONALITIES",
    "get_personality",
    "format_chat_message",
    "should_agent_respond",
]




