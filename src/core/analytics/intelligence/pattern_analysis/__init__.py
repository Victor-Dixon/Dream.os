# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: pattern analysis package initialization.
# SSOT: docs/recovery/recovery_registry.yaml

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""

<!-- SSOT Domain: core -->
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-intelligence-pattern-analysis-init
@file pattern analysis package initialization.
@summary pattern analysis package initialization.
"""

from . import anomaly_detector
from . import pattern_extractor
from . import trend_analyzer

__all__ = [
    'anomaly_detector',
    'pattern_extractor',
    'trend_analyzer',
]
