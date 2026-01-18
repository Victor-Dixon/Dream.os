#!/usr/bin/env python3
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
