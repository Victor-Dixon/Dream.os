"""
@file
@summary Legacy compatibility exports for validation utilities.
@registry docs/recovery/recovery_registry.yaml#validation-utilities-compat
"""


def get_virtual_screen_bounds() -> tuple[int, int, int, int]:
    """Return a conservative default virtual screen rectangle."""
    return (0, 0, 1920, 1080)


__all__ = ["get_virtual_screen_bounds"]
