#!/usr/bin/env python3
"""
GitHub Token Status Helper
==========================

Quickly verify GitHub token availability without consuming rate limit by default.

Usage:
    python tools/github_token_status.py
    python tools/github_token_status.py --rate-limit   # optional single rate_limit call
"""

import argparse
import sys

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from src.core.utils.github_utils import get_github_token


def check_token_detected() -> tuple[bool, int]:
    """Return whether a token is detected and its length."""
    token = get_github_token()
    return bool(token), len(token) if token else 0


def check_rate_limit(token: str) -> tuple[int, int | None]:
    """Perform a lightweight rate_limit check; returns (status_code, core_remaining|None)."""
    if not REQUESTS_AVAILABLE:
        return 0, None
    resp = requests.get(
        "https://api.github.com/rate_limit",
        headers={"Authorization": f"token {token}"},
        timeout=10,
    )
    remaining = None
    try:
        data = resp.json()
        remaining = data.get("resources", {}).get("core", {}).get("remaining")
    except Exception:
        remaining = None
    return resp.status_code, remaining


def main() -> int:
    parser = argparse.ArgumentParser(description="GitHub token status helper")
    parser.add_argument(
        "--rate-limit",
        action="store_true",
        help="Perform a single /rate_limit call (uses one API request)",
    )
    args = parser.parse_args()

    detected, length = check_token_detected()
    print(f"token_detected {detected}")
    print(f"token_length {length}")

    if args.rate_limit:
        if not detected:
            print("rate_limit_check_skipped (no token)")
            return 1
        status, remaining = check_rate_limit(get_github_token() or "")
        print(f"rate_limit_status {status}")
        print(f"core_remaining {remaining}")

    return 0


if __name__ == "__main__":
    sys.exit(main())





