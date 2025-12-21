
"""
⚠️ DEPRECATED - IOnboardingService protocol is deprecated.

This interface has been consolidated into src/core/messaging_protocol_models.py as SSOT.
Please update imports to use the SSOT location instead.

Migration:
  OLD: from core.messaging_protocol_models import IOnboardingService
  NEW: from core.messaging_protocol_models import IOnboardingService

Note: SSOT has full documentation and type hints

This interface will be removed in a future release.
"""

import warnings
warnings.warn(
    "IOnboardingService is deprecated. Use src/core/messaging_protocol_models.py instead.",
    DeprecationWarning,
    stacklevel=2
)

#!/usr/bin/env python3
"""
Onboarding Service - Core Implementation

<!-- SSOT Domain: infrastructure -->

========================================

Implements IOnboardingService protocol for messaging core.
Delegates to services layer for actual onboarding operations.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-26
License: MIT
"""

import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class IOnboardingService(Protocol):
    """Interface for onboarding operations."""

    def generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate onboarding message."""
        ...


class OnboardingService:
    """Onboarding service implementation for messaging core."""

    def __init__(self):
        """Initialize onboarding service."""
        self.logger = logging.getLogger(__name__)
        self._template_loader = None
        logger.info("OnboardingService initialized")

    @property
    def template_loader(self):
        """Lazy-load template loader to avoid circular imports."""
        if self._template_loader is None:
            try:
                from ..services.onboarding_template_loader import OnboardingTemplateLoader
                self._template_loader = OnboardingTemplateLoader()
            except ImportError:
                self.logger.warning("OnboardingTemplateLoader not available")
                self._template_loader = None
        return self._template_loader

    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """
        Generate onboarding message for an agent.

        Args:
            agent_id: Target agent ID
            style: Message style (friendly, professional, etc.)

        Returns:
            Generated onboarding message
        """
        try:
            # Try to use template loader if available
            if self.template_loader:
                return self.template_loader.load_onboarding_template(agent_id, style)
            
            # Fallback to default message
            return self._default_onboarding_message(agent_id, style)
        except Exception as e:
            self.logger.error(f"Error generating onboarding message: {e}")
            return self._default_onboarding_message(agent_id, style)

    def _default_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate default onboarding message."""
        if style == "friendly":
            return f"🚀 Welcome {agent_id}! Ready to get started? Check your inbox and begin autonomous operations."
        else:
            return f"🚀 {agent_id} - Activation initiated. Check your inbox and begin autonomous operations."

