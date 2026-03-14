# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-ssot-unified-ssot-models
# @registry docs/recovery/recovery_registry.yaml#src-core-ssot-unified-ssot-models

"""
<!-- SSOT Domain: core -->

SSOT Unified Models
==================

Re-exports SSOT models for unified_ssot validators.

Author: Agent-1 - Testing & Quality Assurance Specialist
Created: 2025-10-14
"""

from ..ssot_models import (
    SSOTComponent,
    SSOTComponentType,
    SSOTExecutionPhase,
    SSOTIntegrationResult,
    SSOTValidationLevel,
)

__all__ = [
    "SSOTComponent",
    "SSOTComponentType",
    "SSOTExecutionPhase",
    "SSOTIntegrationResult",
    "SSOTValidationLevel",
]
