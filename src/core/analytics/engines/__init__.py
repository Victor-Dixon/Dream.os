# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: engines package initialization.
# SSOT: docs/recovery/recovery_registry.yaml

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
<!-- SSOT Domain: core -->

Analytics Engines Module

# SSOT Domain: core
<!-- SSOT Domain: analytics -->
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-engines-init
@file engines package initialization.
@summary engines package initialization.
"""

from . import batch_analytics_engine
from . import caching_engine_fixed
from . import coordination_analytics_engine
from . import metrics_engine
from . import realtime_analytics_engine

__all__ = [
    'batch_analytics_engine',
    'caching_engine_fixed',
    'coordination_analytics_engine',
    'metrics_engine',
    'realtime_analytics_engine',
]
