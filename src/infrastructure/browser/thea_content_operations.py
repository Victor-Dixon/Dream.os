"""
@file
@summary Legacy compatibility shim for content operations.
@registry docs/recovery/recovery_registry.yaml#thea-content-operations
"""


class TheaContentOperations:
    """Minimal content operation API retained for older imports/tests."""

    def scrape(self):
        return ""

    def collect_response(self):
        return ""


__all__ = ["TheaContentOperations"]
