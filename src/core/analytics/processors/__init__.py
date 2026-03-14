# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: processors package initialization.
# SSOT: docs/recovery/recovery_registry.yaml

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
<!-- SSOT Domain: core -->

<!-- SSOT Domain: analytics -->
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-processors-init
@file processors package initialization.
@summary processors package initialization.
"""

from . import insight_processor
from . import prediction_processor

__all__ = [
    'insight_processor',
    'prediction_processor',
]
