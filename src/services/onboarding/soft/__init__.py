"""
<!-- SSOT Domain: integration -->

Soft Onboarding Service
========================

Soft onboarding with 6-step protocol:
1. Click chat input
2. Save session (Ctrl+Enter)
3. Send cleanup prompt (A++ canonical closure prompt)
4. Open new tab (Ctrl+T)
5. Navigate to onboarding coordinates
6. Paste onboarding message

V2 Compliant: Modular structure with extracted steps
"""

from .service import SoftOnboardingService
from .service import execute_soft_onboarding
from .service import soft_onboard_agent
from .service import soft_onboard_multiple_agents
from .canonical_closure_prompt import (
    CANONICAL_CLOSURE_PROMPT,
    get_canonical_closure_prompt,
)

__all__ = [
    "SoftOnboardingService",
    "execute_soft_onboarding",
    "soft_onboard_agent",
    "soft_onboard_multiple_agents",
    "CANONICAL_CLOSURE_PROMPT",
    "get_canonical_closure_prompt",
]

