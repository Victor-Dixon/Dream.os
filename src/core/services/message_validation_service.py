#!/usr/bin/env python3
"""
Message Validation Service - Service Layer Architecture
====================================================

<!-- SSOT Domain: integration -->

Service for validating message content and structure.

Author: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-16
Refactored from messaging_core.py for V2 compliance (file size limits)
"""

import json
import logging
from typing import Tuple, List

# Use relative imports for V2 compliance
from ..messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
)

logger = logging.getLogger(__name__)


class MessageValidationService:
    """Service for validating message content and structure."""

    def __init__(self):
        self.max_content_length = 10000
        self.max_metadata_size = 5000

    def validate_message(self, message: UnifiedMessage) -> Tuple[bool, List[str]]:
        """Validate message structure and content."""
        errors = []

        # Basic structure validation
        if not message.content:
            errors.append("Message content cannot be empty")

        if not message.sender:
            errors.append("Message sender cannot be empty")

        if not message.recipient:
            errors.append("Message recipient cannot be empty")

        # Content validation
        if len(message.content) > self.max_content_length:
            errors.append(f"Message content too long ({len(message.content)} > {self.max_content_length})")

        # Metadata validation
        if message.metadata:
            metadata_size = len(json.dumps(message.metadata))
            if metadata_size > self.max_metadata_size:
                errors.append(f"Message metadata too large ({metadata_size} > {self.max_metadata_size})")

        # Type validation
        if not isinstance(message.message_type, UnifiedMessageType):
            errors.append("Invalid message type")

        if not isinstance(message.priority, UnifiedMessagePriority):
            errors.append("Invalid message priority")

        # Tag validation
        for tag in message.tags:
            if not isinstance(tag, UnifiedMessageTag):
                errors.append(f"Invalid message tag: {tag}")

        return len(errors) == 0, errors

    def sanitize_content(self, content: str) -> str:
        """Sanitize message content for security."""
        if not content:
            return ""

        # Basic sanitization - remove potentially harmful content
        # This is a simplified version; production would need more robust sanitization
        sanitized = content.replace('\x00', '')  # Remove null bytes

        return sanitized[:self.max_content_length]  # Truncate if too long