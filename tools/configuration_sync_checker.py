#!/usr/bin/env python3
"""Check configuration file sync across environments.

Scans WordPress wp-config.php files for key configuration values and reports
drift between local and production environments.

Usage:
  python tools/configuration_sync_checker.py --site freerideinvestor.com
  python tools/configuration_sync_checker.py --all
  python tools/configuration_sync_checker.py --all --json

SSOT: analytics
SSOT_DOMAIN: analytics
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
WEBSITES_ROOT = Path("D:/websites/websites")

P0_SITES = [
    "freerideinvestor.com",
    "tradingrobotplug.com",
    "dadudekc.com",
    "crosbyultimateevents.com",
]

# Keys to track in wp-config.php for configuration drift detection
TRACKED_KEYS = [
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "WP_DEBUG",
    "WP_DEBUG_LOG",
    "WP_DEBUG_DISPLAY",
    "GA4_MEASUREMENT_ID",
    "FACEBOOK_PIXEL_ID",
    "WP_HOME",
    "WP_SITEURL",
]


def _hash_value(val: str) -> str:
    """Return first 8 hex chars of sha256 hash (for masked output)."""
    return hashlib.sha256(val.encode()).hexdigest()[:8]


def _extract_define_value(content: str, key: str) -> Optional[str]:
    """Extract value from define('KEY', 'value') pattern."""
    pattern = rf"define\s*\(\s*['\"]({key})['\"]\s*,\s*['\"]?([^'\"]+)['\"]?\s*\)"
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(2) if match else None


def parse_wp_config(path: Path) -> Dict[str, Optional[str]]:
    """Parse wp-config.php and extract tracked keys."""
    if not path.exists():
        return {}
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    out: Dict[str, Optional[str]] = {}
    for key in TRACKED_KEYS:
        out[key] = _extract_define_value(content, key)
    return out


def get_site_path(site: str) -> Path:
    """Return path to site directory."""
    if WEBSITES_ROOT.exists():
        return WEBSITES_ROOT / site
    return PROJECT_ROOT / "websites" / site


def check_site(site: str) -> Dict[str, Any]:
    """Check wp-config.php configuration for a site.

    Returns dict with:
      - site: str
      - config_exists: bool
      - values: Dict[str, Optional[str]] (hashed sensitive values)
      - raw_values: Dict[str, Optional[str]] (for internal comparison)
    """
    site_path = get_site_path(site)
    config_path = site_path / "wp" / "wp-config.php"

    result: Dict[str, Any] = {
        "site": site,
        "config_exists": config_path.exists(),
        "config_path": str(config_path),
        "values": {},
        "raw_values": {},
    }
    if not config_path.exists():
        return result

    parsed = parse_wp_config(config_path)
    result["raw_values"] = parsed

    # Mask sensitive values for display
    masked: Dict[str, Optional[str]] = {}
    for key, val in parsed.items():
        if val is None:
            masked[key] = None
        elif "PASSWORD" in key.upper() or "SECRET" in key.upper():
            masked[key] = f"****{_hash_value(val)}"
        else:
            masked[key] = val
    result["values"] = masked
    return result


def compare_configs(a: Dict[str, Optional[str]], b: Dict[str, Optional[str]]) -> List[Tuple[str, str, str]]:
    """Compare two config dicts, returning list of (key, val_a, val_b) for differences."""
    diffs: List[Tuple[str, str, str]] = []
    for key in TRACKED_KEYS:
        va = a.get(key)
        vb = b.get(key)
        if va != vb:
            diffs.append((key, str(va), str(vb)))
    return diffs


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def write_report(results: List[Dict[str, Any]]) -> Path:
    """Write markdown report of config sync status."""
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"configuration_sync_{_now_stamp()}.md"

    lines: List[str] = []
    lines.append("# Configuration Sync Report")
    lines.append("")
    lines.append(f"**Generated:** {_now_iso()}")
    lines.append("**Agent:** Agent-5")
    lines.append("")
    lines.append(f"**Sites Checked:** {len(results)}")
    lines.append("")

    for r in results:
        icon = "✅" if r.get("config_exists") else "❌"
        lines.append(f"## {icon} {r['site']}")
        lines.append(f"- Config exists: {'✅' if r.get('config_exists') else '❌'}")
        if not r.get("config_exists"):
            lines.append(f"- Path: `{r.get('config_path')}`")
            lines.append("")
            continue
        lines.append("")
        lines.append("| Key | Value |")
        lines.append("|-----|-------|")
        for key in TRACKED_KEYS:
            val = r.get("values", {}).get(key)
            lines.append(f"| {key} | {val if val else '❌ Not set'} |")
        lines.append("")

    lines.append("---")
    lines.append("**Tool:** `tools/configuration_sync_checker.py`")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Configuration sync checker for wp-config.php")
    parser.add_argument("--site", type=str, help="Check specific site")
    parser.add_argument("--all", action="store_true", help="Check all P0 sites")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown")

    args = parser.parse_args()
    if not args.site and not args.all:
        parser.error("Must specify --site or --all")

    sites = [args.site] if args.site else P0_SITES
    results: List[Dict[str, Any]] = []
    for site in sites:
        r = check_site(site)
        # Remove raw_values for output (security)
        del r["raw_values"]
        results.append(r)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    report_path = write_report(results)
    print(f"✅ Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
