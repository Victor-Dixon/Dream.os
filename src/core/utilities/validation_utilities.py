# Header-Variant: utility
# Owner: @dreamos/platform
# Purpose: Export legacy validation helper compatibility shims.
# @registry docs/recovery/recovery_registry.yaml#validation-utilities-compat


def get_virtual_screen_bounds() -> tuple[int, int, int, int]:
    """Return a conservative default virtual screen rectangle."""
    return (0, 0, 1920, 1080)


__all__ = ["get_virtual_screen_bounds"]
