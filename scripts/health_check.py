"""
Health check CLI wrapper.

SSOT: src/core/health_check.py
"""

from __future__ import annotations

import argparse
import json
import time
from typing import Any, Dict

from src.core.health_check import check_system_health


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run system health checks.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run a single health check and exit (default).",
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run health checks continuously.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Interval in seconds for continuous checks (default: 60).",
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Include performance metrics in the health check output.",
    )
    return parser.parse_args()


def _run_check(include_metrics: bool) -> Dict[str, Any]:
    return check_system_health(include_services=True, include_metrics=include_metrics)


def main() -> None:
    args = _parse_args()
    run_once = args.check or not args.continuous

    if run_once:
        health = _run_check(include_metrics=args.metrics)
        print(json.dumps(health, indent=2, sort_keys=True))
        return

    while True:
        health = _run_check(include_metrics=args.metrics)
        print(json.dumps(health, indent=2, sort_keys=True))
        time.sleep(max(args.interval, 1))


if __name__ == "__main__":
    main()
