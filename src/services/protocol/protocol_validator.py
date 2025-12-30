"""
<!-- SSOT Domain: integration -->

Protocol Validator - V2 Compliant Module
========================================

Validates protocol compliance for messages and routes.
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging
from typing import Any

from ...core.base.base_service import BaseService
from ...core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
)
from .messaging_protocol_models import MessageRoute

logger = logging.getLogger(__name__)


class ProtocolValidator(BaseService):
    """Validates protocol compliance."""

    def __init__(self):
        """Initialize protocol validator."""
        super().__init__("ProtocolValidator")

    def validate_protocol(self, protocol_data: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate protocol data structure.

        Args:
            protocol_data: Protocol data to validate

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []

        # Check required fields
        required_fields = ["version", "type"]
        for field in required_fields:
            if field not in protocol_data:
                errors.append(f"Missing required field: {field}")

        # Validate version
        if "version" in protocol_data:
            version = protocol_data["version"]
            if not isinstance(version, (int, str)):
                errors.append("Version must be int or string")
            elif isinstance(version, str) and not version.isdigit():
                errors.append("Version string must be numeric")

        return len(errors) == 0, errors

    def validate_message(self, message: UnifiedMessage) -> tuple[bool, list[str]]:
        """
        Validate message protocol compliance.

        Args:
            message: Message to validate

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []

        # Check required fields
        if not message.content:
            errors.append("Message content is required")

        if not message.sender:
            errors.append("Message sender is required")

        if not message.recipient:
            errors.append("Message recipient is required")

        # Validate message type
        if not isinstance(message.message_type, UnifiedMessageType):
            errors.append("Invalid message type")

        # Validate priority
        if not isinstance(message.priority, UnifiedMessagePriority):
            errors.append("Invalid message priority")

        # Validate message ID format (should be UUID)
        if message.message_id:
            try:
                import uuid
                uuid.UUID(message.message_id)
            except (ValueError, AttributeError):
                errors.append("Invalid message ID format (must be UUID)")

        return len(errors) == 0, errors

    def validate_route(self, route: MessageRoute) -> tuple[bool, list[str]]:
        """
        Validate route protocol compliance.

        Args:
            route: Route to validate

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []

        # Check if route is valid enum value
        if not isinstance(route, MessageRoute):
            errors.append("Invalid route type")

        # Validate route value
        valid_routes = [r.value for r in MessageRoute]
        if route.value not in valid_routes:
            errors.append(f"Invalid route value: {route.value}")

        return len(errors) == 0, errors

    def validation_errors(self, errors: list[str]) -> str:
        """
        Format validation errors.

        Args:
            errors: List of error messages

        Returns:
            Formatted error string
        """
        if not errors:
            return "No errors"

        return f"Validation errors: {', '.join(errors)}"

