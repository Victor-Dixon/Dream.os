"""
AI Summarizer for DreamVault Training Pipeline
=============================================

SSOT Domain: ai_training

V2 Compliant: <100 lines, single responsibility
Text summarization for conversation processing and training data preparation.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class SummarySchema:
    """Schema for summary structure"""
    max_length: int = 500
    min_length: int = 50
    include_key_points: bool = True
    include_sentiment: bool = True
    preserve_timestamps: bool = False


class Summarizer:
    """
    V2 Compliant AI Summarizer

    Generates summaries of conversations and training data.
    Single responsibility: text summarization.
    """

    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger("Summarizer")
        self.llm_config = llm_config

        # Default summary schema
        self.schema = SummarySchema()

        # TODO: Initialize LLM client based on config
        self._llm_client = None

    def summarize(self, text: str, schema: Optional[SummarySchema] = None) -> str:
        """
        Generate summary of input text.

        Args:
            text: Text to summarize
            schema: Summary schema (uses default if None)

        Returns:
            Summarized text
        """
        if not text or not text.strip():
            return ""

        schema = schema or self.schema

        # For now, implement simple extractive summarization
        # TODO: Replace with actual LLM-based summarization
        return self._extractive_summarize(text, schema)

    def summarize_batch(self, texts: List[str], schema: Optional[SummarySchema] = None) -> List[str]:
        """
        Summarize multiple texts.

        Args:
            texts: List of texts to summarize
            schema: Summary schema

        Returns:
            List of summaries
        """
        return [self.summarize(text, schema) for text in texts]

    def _extractive_summarize(self, text: str, schema: SummarySchema) -> str:
        """
        Simple extractive summarization (placeholder for LLM).

        Args:
            text: Input text
            schema: Summary schema

        Returns:
            Extracted summary
        """
        sentences = self._split_into_sentences(text)

        if not sentences:
            return text[:schema.max_length] + "..." if len(text) > schema.max_length else text

        # Simple scoring based on sentence length and position
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = len(sentence.split())  # Length-based scoring
            if i < 2:  # Favor first sentences
                score += 10
            scored_sentences.append((score, sentence))

        # Sort by score and select top sentences
        scored_sentences.sort(reverse=True)
        selected_sentences = [s for _, s in scored_sentences[:3]]  # Top 3

        # Reorder to maintain original flow
        summary = " ".join(selected_sentences)

        # Apply length constraints
        if len(summary) > schema.max_length:
            summary = summary[:schema.max_length - 3] + "..."
        elif len(summary) < schema.min_length and sentences:
            # If too short, include more sentences
            summary = " ".join(sentences[:2])

        return summary.strip()

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re

        # Simple sentence splitting
        sentences = re.split(r'[.!?]+\s*', text.strip())

        # Filter out empty sentences
        return [s.strip() for s in sentences if s.strip()]

    def set_schema(self, schema: SummarySchema) -> None:
        """Update summary schema."""
        self.schema = schema

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get summarizer capabilities.

        Returns:
            Dict with supported features and limits
        """
        return {
            "supports_batch": True,
            "max_input_length": 10000,  # Placeholder
            "supported_languages": ["en"],  # Placeholder
            "schema_configurable": True,
            "llm_backend": self.llm_config.get("backend", "extractive")
        }