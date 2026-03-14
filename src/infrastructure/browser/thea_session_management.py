"""
@file
@summary Legacy compatibility shim for session management.
@registry docs/recovery/recovery_registry.yaml#thea-session-management
"""


class TheaSessionManagement:
    """Minimal session manager retained for compatibility imports."""

    def __init__(self):
        self._session = None
        self._cookies = []

    def get_session(self):
        return self._session

    def get_cookies(self):
        return list(self._cookies)

    def check_rate_limit(self):
        return True


__all__ = ["TheaSessionManagement"]
