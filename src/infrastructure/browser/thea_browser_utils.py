"""
@file
@summary Minimal browser utility helpers used by legacy Thea modules.
@registry docs/recovery/recovery_registry.yaml#thea-browser-utils
"""


class TheaBrowserUtils:
    """Lightweight utility holder for browser operation helpers."""

    def __init__(self, thea_config=None):
        self.thea_config = thea_config


__all__ = ["TheaBrowserUtils"]
