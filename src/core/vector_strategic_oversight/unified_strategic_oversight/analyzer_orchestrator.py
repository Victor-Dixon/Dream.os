#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Strategic Oversight Analyzer Orchestrator - V2 Compliant Redirect
=================================================================

V2 compliance redirect to modular strategic oversight system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular strategic oversight
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .analyzer_core import StrategicOversightAnalyzer
from .models import StrategicOversightModels

# Optional imports - stub if not available
try:
    from .engine import StrategicOversightEngine
except ImportError:
    StrategicOversightEngine = None

try:
    from .orchestrator import StrategicOversightOrchestrator
except ImportError:
    StrategicOversightOrchestrator = None

# Re-export for backward compatibility
__all__ = [
    "StrategicOversightOrchestrator",
    "StrategicOversightModels",
    "StrategicOversightEngine",
    "StrategicOversightAnalyzer",
]
