#!/usr/bin/env python3
"""Analytics validation readiness scheduler.

Checks GA4/Pixel readiness for P0 sites, persists last snapshot, and writes a
report when status changes.

Usage:
  python tools/analytics_validation_scheduler.py --once
  python tools/analytics_validation_scheduler.py --watch --interval 900
  python tools/analytics_validation_scheduler.py --once --validate-on-ready

SSOT: analytics
SSOT_DOMAIN: analytics
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
STATE_FILE_DEFAULT = PROJECT_ROOT / "tools" / ".analytics_validation_scheduler_state.json"

P0_SITES = [
    "freerideinvestor.com",
    "tradingrobotplug.com",
    "dadudekc.com",
    "crosbyultimateevents.com",
]


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "sites": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"schema_version": 1, "sites": {}}


def save_state(path: Path, snapshot: Dict[str, Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "last_updated": now_iso(),
        "sites": snapshot,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def snapshot() -> Dict[str, Dict[str, Any]]:
    sys.path.insert(0, str(PROJECT_ROOT))
    from tools.check_ga4_pixel_configuration import check_site_configuration

    out: Dict[str, Dict[str, Any]] = {}
    for site in P0_SITES:
        s = check_site_configuration(site)
        out[site] = {
            "status": str(s.get("status", "UNKNOWN")),
            "ready_for_validation": bool(s.get("ready_for_validation", False)),
        }
    return out


def diff(old: Dict[str, Dict[str, Any]], new: Dict[str, Dict[str, Any]]) -> List[Tuple[str, str, str]]:
    changes: List[Tuple[str, str, str]] = []
    for site in P0_SITES:
        if site not in old:
            continue
        o = str(old.get(site, {}).get("status", ""))
        n = str(new.get(site, {}).get("status", ""))
        if o != n:
            changes.append((site, o, n))
    return changes


def write_report(snapshot_data: Dict[str, Dict[str, Any]], changes: List[Tuple[str, str, str]]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"analytics_validation_scheduler_{now_stamp()}.md"

    ready = [s for s, v in snapshot_data.items() if v.get("ready_for_validation")]

    lines: List[str] = []
    lines.append("# Analytics Validation Scheduler Report")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("Agent: Agent-5")
    lines.append("")
    lines.append(f"Ready sites: {len(ready)}/{len(P0_SITES)}")
    if ready:
        lines.append(", ".join(sorted(ready)))
    lines.append("")
    lines.append("## Status Changes")
    if not changes:
        lines.append("- No changes")
    else:
        for site, old_status, new_status in changes:
            lines.append(f"- {site}: {old_status} -> {new_status}")
    lines.append("")
    lines.append("Tool: tools/analytics_validation_scheduler.py")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def maybe_run_validation(validate_on_ready: bool, snapshot_data: Dict[str, Dict[str, Any]]) -> bool:
    if not validate_on_ready:
        return False
    if not any(v.get("ready_for_validation") for v in snapshot_data.values()):
        return False

    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "automated_p0_analytics_validation.py"),
        "--validate-ready",
    ]
    subprocess.run(cmd, check=False)
    return True


def run_once(state_file: Path, validate_on_ready: bool) -> None:
    state = load_state(state_file)
    old = state.get("sites", {}) if isinstance(state.get("sites"), dict) else {}
    new = snapshot()
    changes = diff(old, new)
    if changes:
        report_path = write_report(new, changes)
        print(f"report={report_path}")
    maybe_run_validation(validate_on_ready, new)
    save_state(state_file, new)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analytics validation scheduler")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=int, default=900)
    parser.add_argument("--state-file", type=str, default=str(STATE_FILE_DEFAULT))
    parser.add_argument("--validate-on-ready", action="store_true")

    args = parser.parse_args()
    if not args.once and not args.watch:
        parser.error("Must specify either --once or --watch")

    state_file = Path(args.state_file)

    if args.once:
        run_once(state_file, args.validate_on_ready)
        return 0

    try:
        while True:
            run_once(state_file, args.validate_on_ready)
            time.sleep(max(1, int(args.interval)))
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
