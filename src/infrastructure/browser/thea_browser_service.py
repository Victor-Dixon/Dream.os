"""
@file
@summary Legacy compatibility shim for browser service.
@registry docs/recovery/recovery_registry.yaml#thea-browser-service
"""


class TheaBrowserService:
    """Minimal service facade kept for legacy import compatibility."""

    def __init__(self):
        self.driver = None

    def get_driver(self):
        return self.driver

    def navigate(self, url: str) -> bool:
        return bool(url)

    def cleanup(self) -> None:
        self.driver = None


__all__ = ["TheaBrowserService"]
