"""
Data Redactor for DreamVault AI Training Pipeline
================================================

SSOT Domain: ai_training

V2 Compliant: <100 lines, single responsibility
PII and sensitive data redaction for training data privacy.
"""

import re
import logging
from typing import Dict, Any, List, Optional, Pattern


class Redactor:
    """
    V2 Compliant Data Redactor

    Removes sensitive information from training data to ensure privacy.
    Single responsibility: data sanitization.
    """

    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger("Redactor")
        self.config = config

        # Default patterns for sensitive data
        self._patterns = self._build_patterns()

        # Custom patterns from config
        if "custom_patterns" in config:
            for pattern_name, pattern_str in config["custom_patterns"].items():
                try:
                    self._patterns[pattern_name] = re.compile(pattern_str, re.IGNORECASE)
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern {pattern_name}: {e}")

    def redact(self, text: str) -> str:
        """
        Redact sensitive information from text.

        Args:
            text: Input text to redact

        Returns:
            Redacted text with sensitive data removed/replaced
        """
        if not text:
            return text

        redacted = text

        # Apply redaction patterns
        for pattern_name, pattern in self._patterns.items():
            replacement = self._get_replacement(pattern_name)
            redacted = pattern.sub(replacement, redacted)

        return redacted

    def redact_batch(self, texts: List[str]) -> List[str]:
        """
        Redact multiple texts.

        Args:
            texts: List of texts to redact

        Returns:
            List of redacted texts
        """
        return [self.redact(text) for text in texts]

    def _build_patterns(self) -> Dict[str, Pattern]:
        """Build default redaction patterns."""
        patterns = {}

        # Email addresses
        patterns["email"] = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )

        # Phone numbers (various formats)
        patterns["phone"] = re.compile(
            r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        )

        # Social Security Numbers
        patterns["ssn"] = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

        # Credit card numbers (basic pattern)
        patterns["credit_card"] = re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b')

        # IP addresses
        patterns["ip_address"] = re.compile(
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        )

        # API keys (generic pattern for common formats)
        patterns["api_key"] = re.compile(
            r'\b[A-Za-z0-9]{20,}\b'  # Generic long alphanumeric strings
        )

        return patterns

    def _get_replacement(self, pattern_name: str) -> str:
        """Get replacement string for a pattern."""
        replacements = {
            "email": "[EMAIL_REDACTED]",
            "phone": "[PHONE_REDACTED]",
            "ssn": "[SSN_REDACTED]",
            "credit_card": "[CARD_REDACTED]",
            "ip_address": "[IP_REDACTED]",
            "api_key": "[API_KEY_REDACTED]"
        }

        return replacements.get(pattern_name, "[REDACTED]")

    def add_pattern(self, name: str, pattern: str) -> bool:
        """
        Add a custom redaction pattern.

        Args:
            name: Pattern name
            pattern: Regex pattern string

        Returns:
            True if pattern was added successfully
        """
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            self._patterns[name] = compiled_pattern
            return True
        except re.error as e:
            self.logger.error(f"Invalid regex pattern {name}: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get redaction statistics.

        Returns:
            Dict with pattern counts and configuration info
        """
        return {
            "patterns_count": len(self._patterns),
            "pattern_names": list(self._patterns.keys()),
            "config_enabled": bool(self.config)
        }