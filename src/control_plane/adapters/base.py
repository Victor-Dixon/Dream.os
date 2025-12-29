"""
<!-- SSOT Domain: core -->

Control Plane Adapter Contracts
===============================

Defines the narrow interfaces for site/service adapters. Adapters expose
read-only health and last-deploy info, plus strictly allowlisted operations
through `run_allowed`.
"""

from typing import Dict, Any, Protocol


class SiteAdapter(Protocol):
    """Adapter contract for a site/service under control plane management."""

    def health(self) -> Dict[str, Any]:
        """Return a lightweight health payload (no secrets)."""
        ...

    def last_deploy(self) -> Dict[str, Any]:
        """Return last deploy metadata (timestamps, artifact versions, status)."""
        ...

    def run_allowed(self, op: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Execute an allowlisted operation.

        Args:
            op: Operation key (must be on allowlist)
            payload: Optional parameters for the op

        Returns:
            Result dict with status and message/details.
        """
        ...


