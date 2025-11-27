#!/usr/bin/env python3
"""
OBS Caption Interpreter
=======================

Interprets speech captions and determines:
- Which agent(s) should respond
- What action to take (task, devlog, message, tool)
- Intent classification

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class CaptionIntent(Enum):
    """Intent classification for captions."""

    AGENT_INSTRUCTION = "agent_instruction"
    TASK_ASSIGNMENT = "task_assignment"
    DEVLOG_UPDATE = "devlog_update"
    BROADCAST = "broadcast"
    TOOL_TRIGGER = "tool_trigger"
    HUMAN_CONVERSATION = "human_conversation"
    UNKNOWN = "unknown"


@dataclass
class InterpretedCaption:
    """Interpreted caption with metadata."""

    original_text: str
    intent: CaptionIntent
    target_agents: list[str]  # Empty = broadcast/all
    action_type: str  # "message", "task", "devlog", "tool"
    tool_name: Optional[str] = None
    normalized_text: str = ""
    confidence: float = 0.0


class CaptionInterpreter:
    """
    Interprets OBS captions and determines agent actions.

    Pattern matching for:
    - Agent names ("agent one", "agent-1", "agent1")
    - Commands ("check", "scan", "update", "deploy")
    - Tasks ("task", "mission", "assignment")
    - Tools ("run scanner", "check status")
    """

    # Agent name patterns
    AGENT_PATTERNS = {
        "Agent-1": [
            r"agent\s*[-\s]?one",
            r"agent\s*1",
            r"integration\s*agent",
            r"agent\s*one",
        ],
        "Agent-2": [
            r"agent\s*[-\s]?two",
            r"agent\s*2",
            r"architecture\s*agent",
            r"agent\s*two",
        ],
        "Agent-3": [
            r"agent\s*[-\s]?three",
            r"agent\s*3",
            r"devops\s*agent",
            r"infrastructure\s*agent",
            r"agent\s*three",
        ],
        "Agent-4": [
            r"agent\s*[-\s]?four",
            r"agent\s*4",
            r"captain",
            r"agent\s*four",
        ],
        "Agent-5": [
            r"agent\s*[-\s]?five",
            r"agent\s*5",
            r"business\s*intelligence",
            r"agent\s*five",
        ],
        "Agent-6": [
            r"agent\s*[-\s]?six",
            r"agent\s*6",
            r"coordination\s*agent",
            r"agent\s*six",
        ],
        "Agent-7": [
            r"agent\s*[-\s]?seven",
            r"agent\s*7",
            r"web\s*agent",
            r"web\s*development",
            r"agent\s*seven",
        ],
        "Agent-8": [
            r"agent\s*[-\s]?eight",
            r"agent\s*8",
            r"ssot\s*agent",
            r"agent\s*eight",
        ],
    }

    # Intent patterns
    INTENT_PATTERNS = {
        CaptionIntent.AGENT_INSTRUCTION: [
            r"agent\s+\w+",
            r"tell\s+agent",
            r"message\s+agent",
        ],
        CaptionIntent.TASK_ASSIGNMENT: [
            r"task",
            r"mission",
            r"assignment",
            r"assign\s+to",
        ],
        CaptionIntent.DEVLOG_UPDATE: [
            r"devlog",
            r"log\s+this",
            r"document",
            r"record",
        ],
        CaptionIntent.BROADCAST: [
            r"all\s+agents",
            r"everyone",
            r"swarm",
            r"broadcast",
        ],
        CaptionIntent.TOOL_TRIGGER: [
            r"run\s+\w+",
            r"execute\s+\w+",
            r"trigger\s+\w+",
            r"scan",
            r"check\s+status",
        ],
    }

    # Tool name extraction patterns
    TOOL_PATTERNS = [
        r"run\s+(\w+)",
        r"execute\s+(\w+)",
        r"trigger\s+(\w+)",
        r"(\w+)\s+scanner",
        r"(\w+)\s+checker",
    ]

    def __init__(self):
        """Initialize caption interpreter."""
        self.confidence_threshold = 0.5

    def interpret(self, caption_text: str) -> InterpretedCaption:
        """
        Interpret caption and determine action.

        Args:
            caption_text: Raw caption text from OBS

        Returns:
            InterpretedCaption with metadata
        """
        normalized = self._normalize_text(caption_text)
        intent = self._classify_intent(normalized)
        target_agents = self._extract_agents(normalized)
        action_type = self._determine_action_type(intent, normalized)
        tool_name = self._extract_tool_name(normalized) if intent == CaptionIntent.TOOL_TRIGGER else None
        confidence = self._calculate_confidence(intent, normalized, target_agents)

        return InterpretedCaption(
            original_text=caption_text,
            intent=intent,
            target_agents=target_agents,
            action_type=action_type,
            tool_name=tool_name,
            normalized_text=normalized,
            confidence=confidence,
        )

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for pattern matching.

        Args:
            text: Raw text

        Returns:
            Normalized text (lowercase, cleaned)
        """
        # Lowercase
        normalized = text.lower()

        # Remove extra whitespace
        normalized = re.sub(r"\s+", " ", normalized)

        # Remove punctuation (keep spaces)
        normalized = re.sub(r"[^\w\s]", "", normalized)

        return normalized.strip()

    def _classify_intent(self, normalized_text: str) -> CaptionIntent:
        """
        Classify intent from normalized text.

        Args:
            normalized_text: Normalized caption text

        Returns:
            CaptionIntent classification
        """
        # Check each intent pattern
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, normalized_text, re.IGNORECASE):
                    return intent

        # Default to human conversation if no patterns match
        return CaptionIntent.HUMAN_CONVERSATION

    def _extract_agents(self, normalized_text: str) -> list[str]:
        """
        Extract target agent IDs from text.

        Args:
            normalized_text: Normalized caption text

        Returns:
            List of agent IDs (empty = broadcast/all)
        """
        target_agents = []

        for agent_id, patterns in self.AGENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, normalized_text, re.IGNORECASE):
                    if agent_id not in target_agents:
                        target_agents.append(agent_id)

        return target_agents

    def _determine_action_type(
        self, intent: CaptionIntent, normalized_text: str
    ) -> str:
        """
        Determine action type from intent and text.

        Args:
            intent: Classified intent
            normalized_text: Normalized caption text

        Returns:
            Action type string
        """
        intent_to_action = {
            CaptionIntent.AGENT_INSTRUCTION: "message",
            CaptionIntent.TASK_ASSIGNMENT: "task",
            CaptionIntent.DEVLOG_UPDATE: "devlog",
            CaptionIntent.BROADCAST: "message",
            CaptionIntent.TOOL_TRIGGER: "tool",
            CaptionIntent.HUMAN_CONVERSATION: "message",
            CaptionIntent.UNKNOWN: "message",
        }

        return intent_to_action.get(intent, "message")

    def _extract_tool_name(self, normalized_text: str) -> Optional[str]:
        """
        Extract tool name from text.

        Args:
            normalized_text: Normalized caption text

        Returns:
            Tool name or None
        """
        for pattern in self.TOOL_PATTERNS:
            match = re.search(pattern, normalized_text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def _calculate_confidence(
        self, intent: CaptionIntent, normalized_text: str, target_agents: list[str]
    ) -> float:
        """
        Calculate confidence score for interpretation.

        Args:
            intent: Classified intent
            normalized_text: Normalized text
            target_agents: Extracted agent IDs

        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.5  # Base confidence

        # Increase confidence if agents identified
        if target_agents:
            confidence += 0.2

        # Increase confidence if intent is clear
        if intent != CaptionIntent.UNKNOWN and intent != CaptionIntent.HUMAN_CONVERSATION:
            confidence += 0.2

        # Increase confidence if text is substantial
        if len(normalized_text) > 20:
            confidence += 0.1

        return min(confidence, 1.0)


__all__ = ["CaptionInterpreter", "InterpretedCaption", "CaptionIntent"]


