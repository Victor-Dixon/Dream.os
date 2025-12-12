"""
Sites Health Snapshot
=====================

Read-only utility that loads the sites registry and prints health + last_deploy
info via the configured adapters. This is intended as a "wish we had" tool to
quickly see site status without touching deploy/post behavior.

<!-- SSOT Domain: infrastructure -->
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from src.control_plane.adapters.loader import load_adapter


def load_registry(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Registry not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot(registry: Dict[str, Any]) -> None:
    sites = registry.get("sites", [])
    if not sites:
        print("No sites in registry.")
        return
    for site in sites:
        adapter_key = site.get("adapter")
        adapter = load_adapter(adapter_key) if adapter_key else load_adapter("noop")
        health = {}
        last = {}
        try:
            health = adapter.health()  # type: ignore[arg-type]
        except Exception as exc:  # pragma: no cover
            health = {"ok": False, "error": str(exc)}
        try:
            last = adapter.last_deploy()  # type: ignore[arg-type]
        except Exception as exc:  # pragma: no cover
            last = {"ok": False, "error": str(exc)}
        caps = site.get("capabilities", {})
        print(
            f"{site.get('id')} ({site.get('domain')}) "
            f"adapter={adapter_key} ok={health.get('ok')} "
            f"health_status={health.get('status_code', health.get('error'))} "
            f"deploy_ok={last.get('ok')}"
        )
        if caps:
            print(f"  capabilities: {caps}")
        if not health.get("ok"):
            print(f"  health details: {health}")
        if not last.get("ok"):
            print(f"  last_deploy details: {last}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Print health snapshot for sites registry (read-only).")
    parser.add_argument(
        "--registry",
        default="runtime/control_plane/sites_registry.json",
        help="Path to registry JSON (default: runtime/control_plane/sites_registry.json)",
    )
    args = parser.parse_args()
    registry = load_registry(Path(args.registry))
    snapshot(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

