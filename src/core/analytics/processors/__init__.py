# Header-Variant: full
# Owner: Dream.os Platform
# Purpose:   init  .
# SSOT: docs/recovery/recovery_registry.yaml

"""
@file   init  .
@summary   init  .
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-processors-init
"""

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
<!-- SSOT Domain: core -->

<!-- SSOT Domain: analytics -->
"""

from . import insight_processor
from . import prediction_processor

__all__ = [
    'insight_processor',
    'prediction_processor',
]
