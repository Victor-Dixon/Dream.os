"""
Caption Interpreter - V2 Compliant
==================================

SSOT Domain: core

V2 Compliant: <100 lines, single responsibility
OBS caption interpretation and processing.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CaptionIntent(Enum):
    """Types of caption intents"""
    COMMAND = "command"
    QUESTION = "question"
    STATEMENT = "statement"
    EMOTION = "emotion"
    UNKNOWN = "unknown"


@dataclass
class InterpretedCaption:
    """Interpreted caption data"""
    raw_caption: str
    intent: CaptionIntent
    confidence: float
    entities: Dict[str, Any]
    timestamp: float
    speaker: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.intent, CaptionIntent):
            self.intent = CaptionIntent.UNKNOWN
        self.confidence = max(0.0, min(1.0, self.confidence))


class CaptionInterpreter:
    """
    V2 Compliant Caption Interpreter

    Interprets OBS captions and extracts intent/context.
    Single responsibility: caption interpretation.
    """

    def __init__(self):
        self.logger = logging.getLogger("CaptionInterpreter")

        # Simple keyword-based intent detection
        self.intent_keywords = {
            CaptionIntent.COMMAND: ["start", "stop", "begin", "end", "run", "execute"],
            CaptionIntent.QUESTION: ["what", "how", "when", "where", "why", "who", "can you", "?"],
            CaptionIntent.EMOTION: ["great", "awesome", "terrible", "excited", "happy", "sad", "angry"],
        }

    def interpret(self, caption_text: str, speaker: Optional[str] = None) -> InterpretedCaption:
        """
        Interpret a caption and extract intent.

        Args:
            caption_text: Raw caption text
            speaker: Optional speaker identifier

        Returns:
            InterpretedCaption with analysis
        """
        try:
            # Clean and normalize text
            text = caption_text.strip().lower()

            # Detect intent
            intent, confidence = self._detect_intent(text)

            # Extract entities (simplified)
            entities = self._extract_entities(text)

            return InterpretedCaption(
                raw_caption=caption_text,
                intent=intent,
                confidence=confidence,
                entities=entities,
                timestamp=self._get_timestamp(),
                speaker=speaker
            )

        except Exception as e:
            self.logger.error(f"Caption interpretation error: {e}")
            return InterpretedCaption(
                raw_caption=caption_text,
                intent=CaptionIntent.UNKNOWN,
                confidence=0.0,
                entities={},
                timestamp=self._get_timestamp(),
                speaker=speaker
            )

    def _detect_intent(self, text: str) -> tuple[CaptionIntent, float]:
        """Detect intent from text using keyword matching."""
        best_intent = CaptionIntent.STATEMENT
        best_score = 0.1  # Base confidence

        for intent, keywords in self.intent_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > 0:
                score = min(1.0, matches / len(keywords.split()) * 0.8)
                if score > best_score:
                    best_score = score
                    best_intent = intent

        # Question mark detection
        if "?" in text or text.startswith(("what", "how", "when", "where", "why", "who")):
            best_intent = CaptionIntent.QUESTION
            best_score = max(best_score, 0.7)

        return best_intent, best_score

    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text (simplified implementation)."""
        entities = {}

        # Simple entity extraction - could be enhanced with NLP
        words = text.split()

        # Look for agent names (simplified)
        agent_names = ["agent", "bot", "system", "coordinator"]
        for word in words:
            if word in agent_names:
                entities["agent"] = word
                break

        # Look for actions
        actions = ["start", "stop", "restart", "check", "monitor"]
        for word in words:
            if word in actions:
                entities["action"] = word
                break

        return entities

    def _get_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()

    def get_supported_intents(self) -> list[CaptionIntent]:
        """Get list of supported intents."""
        return list(self.intent_keywords.keys()) + [CaptionIntent.STATEMENT, CaptionIntent.UNKNOWN]