#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: start_message_queue module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-utilities-start-message-queue-py
# @registry docs/recovery/recovery_registry.yaml#tools-utilities-start-message-queue-py

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
