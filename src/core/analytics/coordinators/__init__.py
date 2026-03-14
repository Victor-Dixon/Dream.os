# Header-Variant: full
# Owner: Dream.os Platform
# Purpose:   init  .
# SSOT: docs/recovery/recovery_registry.yaml

"""
@file   init  .
@summary   init  .
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-coordinators-init
"""

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""

<!-- SSOT Domain: core -->
"""

from . import analytics_coordinator
from . import processing_coordinator

__all__ = [
    'analytics_coordinator',
    'processing_coordinator',
]
