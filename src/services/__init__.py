# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: services package initialization.
# SSOT: docs/recovery/recovery_registry.yaml#unregistered-src-services-init
# @registry docs/recovery/recovery_registry.yaml#unregistered-src-services-init

"""Services package.

Import side effects are intentionally minimized so lightweight commands can
import specific service modules without bootstrapping all onboarding/runtime
dependencies.
"""

__all__: list[str] = []
