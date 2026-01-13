"""
<!-- SSOT Domain: integration -->

Soft Onboarding Service - Backward Compatibility Shim
======================================================

This module maintains backward compatibility while delegating to refactored modules.
All functionality has been extracted to src/services/onboarding/soft/

V2 Compliant: < 100 lines (shim)
"""

# Import from refactored module
from src.services.onboarding.soft.service import (
    SoftOnboardingService,
    execute_soft_onboarding,
    soft_onboard_agent,
    soft_onboard_multiple_agents,
)

# Re-export for backward compatibility
__all__ = [
    "SoftOnboardingService",
    "execute_soft_onboarding",
    "soft_onboard_agent",
    "soft_onboard_multiple_agents",
]

# Note: generate_cycle_accomplishments_report function moved to tools/generate_cycle_accomplishments_report.py
