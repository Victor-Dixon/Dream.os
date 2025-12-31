#!/usr/bin/env python3
"""
Cycle Accomplishments Report Generator - Convenience Wrapper
=============================================================

This is a convenience wrapper that redirects to the modular implementation.
Use this for backward compatibility or simpler command-line access.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
Protocol Status: ACTIVE
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-30
V2 Compliant: Yes

Usage:
    python tools/generate_cycle_accomplishments.py [options]

For full documentation, see:
- tools/cycle_accomplishments/README.md
- docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md

<!-- SSOT Domain: tools -->
"""

import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir.parent))

# Import and run main
from tools.cycle_accomplishments.main import main

if __name__ == "__main__":
    sys.exit(main())

