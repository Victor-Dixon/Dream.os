#!/usr/bin/env python3
"""
Onboarding Module - Public API Exports
=======================================

<!-- SSOT Domain: integration -->

Public API exports for unified onboarding service.
Extracted from hard_onboarding_service.py and soft_onboarding_service.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

# Handlers
from .hard_onboarding_handler import HardOnboardingHandler
from .soft_onboarding_handler import SoftOnboardingHandler

# Service Adapters
from .unified_onboarding_service import (
    UnifiedOnboardingService,
    hard_onboard_agent,
    hard_onboard_multiple_agents,
    soft_onboard_agent,
    soft_onboard_multiple_agents,
    generate_cycle_accomplishments_report,
)

__all__ = [
    # Handlers
    "HardOnboardingHandler",
    "SoftOnboardingHandler",
    # Service Adapters
    "UnifiedOnboardingService",
    "hard_onboard_agent",
    "hard_onboard_multiple_agents",
    "soft_onboard_agent",
    "soft_onboard_multiple_agents",
    "generate_cycle_accomplishments_report",
]

