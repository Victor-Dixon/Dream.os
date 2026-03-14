#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: start_twitch module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-utilities-start-twitch-py
# @registry docs/recovery/recovery_registry.yaml#tools-utilities-start-twitch-py

"""
Twitch Bot Launcher.

SSOT: tools/utilities/start_twitch.py
"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """Launch the Twitch bot service."""
    return subprocess.call([sys.executable, "main.py", "--start", "--twitch"])


if __name__ == "__main__":
    raise SystemExit(main())
