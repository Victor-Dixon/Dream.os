"""
<!-- SSOT Domain: integration -->

Architectural Principles - V2 Compliance Module
================================================

Centralized architectural principles registry.
REFACTORED: Extracted principle data to separate module for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

from .architectural_models import ArchitecturalGuidance, ArchitecturalPrinciple
from .architectural_principles_data import (
    get_dip_guidance,
    get_dry_guidance,
    get_isp_guidance,
    get_kiss_guidance,
    get_lsp_guidance,
    get_ocp_guidance,
    get_srp_guidance,
    get_ssot_guidance,
    get_tdd_guidance,
)


class PrincipleDefinitions:
    """Centralized definitions for all architectural principles."""

    @staticmethod
    def get_all_principles() -> dict[ArchitecturalPrinciple, ArchitecturalGuidance]:
        """Get all architectural principle definitions (refactored for V2)."""
        return {
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY: get_srp_guidance(),
            ArchitecturalPrinciple.OPEN_CLOSED: get_ocp_guidance(),
            ArchitecturalPrinciple.LISKOV_SUBSTITUTION: get_lsp_guidance(),
            ArchitecturalPrinciple.INTERFACE_SEGREGATION: get_isp_guidance(),
            ArchitecturalPrinciple.DEPENDENCY_INVERSION: get_dip_guidance(),
            ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH: get_ssot_guidance(),
            ArchitecturalPrinciple.DONT_REPEAT_YOURSELF: get_dry_guidance(),
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID: get_kiss_guidance(),
            ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT: get_tdd_guidance(),
        }

    @staticmethod
    def get_principle(principle: ArchitecturalPrinciple) -> ArchitecturalGuidance:
        """Get a specific architectural principle."""
        all_principles = PrincipleDefinitions.get_all_principles()
        return all_principles.get(principle)
