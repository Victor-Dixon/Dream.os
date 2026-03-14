# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Fsm models.
# SSOT: docs/recovery/recovery_registry.yaml

"""
<!-- SSOT Domain: core -->

FSM Models - V2 Compliance Refactored
====================================

FSM-related data models with V2 compliance standards.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-constants-fsm-models
@file Fsm models.
@summary Fsm models.
"""

from .fsm.configuration_models import FSMConfiguration

# Import modular components
from .fsm.state_models import StateDefinition
from .fsm.transition_models import TransitionDefinition
from .fsm_enums import FSMErrorType, StateStatus, TransitionStatus, TransitionType

# Re-export for backward compatibility
__all__ = [
    "StateDefinition",
    "TransitionDefinition",
    "FSMConfiguration",
    "TransitionType",
    "StateStatus",
    "TransitionStatus",
    "FSMErrorType",
]

# Backward compatibility - create aliases
StateDefinition = StateDefinition
TransitionDefinition = TransitionDefinition
FSMConfiguration = FSMConfiguration
