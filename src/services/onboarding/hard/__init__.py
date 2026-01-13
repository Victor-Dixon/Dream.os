"""
<!-- SSOT Domain: integration -->

Hard Onboarding Service
=======================

Hard onboarding with RESET protocol (5 steps):
1. Clear chat (Ctrl+Shift+Backspace)
2. Send/Execute (Ctrl+Enter)
3. New window (Ctrl+N)
4. Navigate to onboarding coordinates
5. Send onboarding message

V2 Compliant: Modular structure with extracted steps
"""

from .service import HardOnboardingService
from .service import execute_hard_onboarding
from .service import hard_onboard_agent
from .service import hard_onboard_multiple_agents

__all__ = [
    "HardOnboardingService",
    "execute_hard_onboarding",
    "hard_onboard_agent",
    "hard_onboard_multiple_agents",
]

