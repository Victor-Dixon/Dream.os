# Header-Variant: full
# Owner: Dream.os Platform
# Purpose:   init  .
# SSOT: docs/recovery/recovery_registry.yaml

"""
@file   init  .
@summary   init  .
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-config-init
"""

from . import config_manager
from . import config_enums
from . import config_dataclasses
from . import config_accessors
# SSOT Domain: core
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten


__all__ = [
    'config_accessors',
    'config_dataclasses',
    'config_enums',
    'config_manager',
]
