"""
<!-- SSOT Domain: core -->

Adapter Loader
==============

Resolves adapters by key from the sites registry. Provides a NoOp adapter when
an adapter key is unknown to avoid runtime crashes during gradual adoption.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from src.control_plane.adapters.base import SiteAdapter
from src.control_plane.adapters.hostinger.freeride_adapter import get_freeride_adapter
from src.control_plane.adapters.hostinger.prismblossom_adapter import get_prismblossom_adapter
from src.control_plane.adapters.hostinger.weareswarm_adapter import (
    get_weareswarm_adapter,
    get_weareswarm_site_adapter,
)
from src.control_plane.adapters.hostinger.tradingrobotplug_adapter import get_tradingrobotplug_adapter
from src.control_plane.adapters.hostinger.ariajet_adapter import get_ariajet_adapter
from src.control_plane.adapters.hostinger.southwestsecret_adapter import get_southwestsecret_adapter
from src.control_plane.adapters.hostinger.dadudekc_adapter import get_dadudekc_adapter


class NoOpAdapter:
    """NoOp adapter that matches SiteAdapter Protocol for safe fallback."""
    key = "noop"

    def __init__(self, reason: str = "adapter not found"):
        self.reason = reason

    def health(self) -> Dict[str, Any]:
        """Return health check failure for missing adapter."""
        return {"ok": False, "error": self.reason}

    def last_deploy(self) -> Dict[str, Any]:
        """Return last deploy failure for missing adapter."""
        return {"ok": False, "error": self.reason}

    def run_allowed(self, op: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return operation failure for missing adapter."""
        return {"ok": False, "error": self.reason}


ADAPTERS: Dict[str, callable] = {
    "hostinger.freerideinvestor": get_freeride_adapter,
    "hostinger.prismblossom": get_prismblossom_adapter,
    "hostinger.weareswarm_online": get_weareswarm_adapter,
    "hostinger.weareswarm_site": get_weareswarm_site_adapter,
    "hostinger.tradingrobotplug": get_tradingrobotplug_adapter,
    "hostinger.ariajet": get_ariajet_adapter,
    "hostinger.southwestsecret": get_southwestsecret_adapter,
    "hostinger.dadudekc": get_dadudekc_adapter,
}


def load_adapter(adapter_key: str) -> SiteAdapter:
    factory = ADAPTERS.get(adapter_key)
    if not factory:
        return NoOpAdapter(reason=f"adapter '{adapter_key}' not registered")
    return factory()

