# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: coordinators package initialization.
# SSOT: docs/recovery/recovery_registry.yaml

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""

<!-- SSOT Domain: core -->
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-coordinators-init
@file coordinators package initialization.
@summary coordinators package initialization.
"""

from . import analytics_coordinator
from . import processing_coordinator

__all__ = [
    'analytics_coordinator',
    'processing_coordinator',
]
