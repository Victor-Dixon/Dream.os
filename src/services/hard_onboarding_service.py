"""
<!-- SSOT Domain: integration -->

Hard Onboarding Service - Backward Compatibility Shim
======================================================

This module maintains backward compatibility while delegating to refactored modules.
All functionality has been extracted to src/services/onboarding/hard/

V2 Compliant: < 100 lines (shim)
"""

# Import from refactored module
from src.services.onboarding.hard.service import (
    HardOnboardingService,
    execute_hard_onboarding,
    hard_onboard_agent,
    hard_onboard_multiple_agents,
)

# Re-export for backward compatibility
__all__ = [
    "HardOnboardingService",
    "execute_hard_onboarding",
    "hard_onboard_agent",
    "hard_onboard_multiple_agents",
]
