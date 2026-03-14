# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: prediction package initialization.
# SSOT: docs/recovery/recovery_registry.yaml

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
<!-- SSOT Domain: core -->

<!-- SSOT Domain: analytics -->
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-analytics-processors-prediction-init
@file prediction package initialization.
@summary prediction package initialization.
"""

from . import prediction_analyzer
from . import prediction_calculator
from . import prediction_validator

__all__ = [
    'prediction_analyzer',
    'prediction_calculator',
    'prediction_validator',
]
