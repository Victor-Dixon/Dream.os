"""
<!-- SSOT Domain: integration -->

Cleanup Defaults - Soft Onboarding
===================================

Default cleanup message for soft onboarding session closure.
Uses the canonical A++ closure prompt.
"""

from .canonical_closure_prompt import get_canonical_closure_prompt

# Default session closure prompt (A++ canonical)
DEFAULT_SESSION_CLOSURE_PROMPT = get_canonical_closure_prompt()

__all__ = ["DEFAULT_SESSION_CLOSURE_PROMPT"]

