"""
<!-- SSOT Domain: integration -->

Policy Enforcer - V2 Compliant Module
=====================================

Enforces policies on messages and routes.
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging
from typing import Any

from ...core.base.base_service import BaseService
from ...core.messaging_models_core import UnifiedMessage
from ..messaging.policy_loader import load_template_policy

logger = logging.getLogger(__name__)


class PolicyEnforcer(BaseService):
    """Enforces policies on messages and routes."""

    def __init__(self, policy_path: str | None = None):
        """Initialize policy enforcer."""
        super().__init__("PolicyEnforcer")
        self.policy = load_template_policy(policy_path) if policy_path else load_template_policy()

    def enforce_policy(self, message: UnifiedMessage) -> bool:
        """
        Enforce policy on a message.

        Args:
            message: Message to enforce policy on

        Returns:
            True if policy allows the message
        """
        try:
            # Check message priority policies
            if message.priority.value == "urgent":
                # Urgent messages may have special policies
                if not self._check_urgent_policy(message):
                    self.logger.warning(f"Urgent message {message.message_id} blocked by policy")
                    return False

            # Check message type policies
            if not self._check_type_policy(message):
                self.logger.warning(f"Message {message.message_id} blocked by type policy")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Policy enforcement error: {e}")
            return False

    def validate_policy(self, policy_data: dict[str, Any]) -> bool:
        """
        Validate policy data structure.

        Args:
            policy_data: Policy data to validate

        Returns:
            True if policy is valid
        """
        required_keys = ["version", "roles", "channels"]
        for key in required_keys:
            if key not in policy_data:
                self.logger.error(f"Policy missing required key: {key}")
                return False
        return True

    def check_permissions(
        self, sender: str, recipient: str, message_type: str
    ) -> bool:
        """
        Check if sender has permission to send to recipient.

        Args:
            sender: Sender identifier
            recipient: Recipient identifier
            message_type: Type of message

        Returns:
            True if permission granted
        """
        # Basic permission check based on roles
        sender_role = sender.upper() if sender else "UNKNOWN"
        recipient_role = recipient.upper() if recipient else "UNKNOWN"

        # Captain can send to anyone
        if sender_role == "CAPTAIN":
            return True

        # Agents can send to other agents
        if sender_role.startswith("AGENT") and recipient_role.startswith("AGENT"):
            return True

        # Default: allow
        return True

    def _check_urgent_policy(self, message: UnifiedMessage) -> bool:
        """Check urgent message policy."""
        # Urgent messages from captain are always allowed
        if message.sender_type.value == "captain":
            return True

        # Check policy for urgent messages
        urgent_policy = self.policy.get("urgent", {})
        if urgent_policy.get("require_captain_approval", False):
            return message.sender_type.value == "captain"

        return True

    def _check_type_policy(self, message: UnifiedMessage) -> bool:
        """Check message type policy."""
        type_policies = self.policy.get("message_types", {})
        message_type = message.message_type.value

        if message_type in type_policies:
            policy = type_policies[message_type]
            if policy.get("enabled", True) is False:
                return False

        return True

