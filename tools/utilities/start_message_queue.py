#!/usr/bin/env python3
"""
Message Queue Service Launcher.

SSOT: tools/utilities/start_message_queue.py
"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """Launch the message queue processor."""
    return subprocess.call([sys.executable, "main.py", "--start", "--message-queue"])


if __name__ == "__main__":
    raise SystemExit(main())
