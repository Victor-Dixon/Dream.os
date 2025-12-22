#!/usr/bin/env python3
"""
Core System CLI - DEPRECATED
=============================

⚠️ DEPRECATED: This CLI entry point has been consolidated.
Use the unified CLI instead: python -m src.cli core <command>

This file is kept for backward compatibility and redirects to the unified CLI.

<!-- SSOT Domain: infrastructure -->

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-21
Status: DEPRECATED - Redirects to src.cli
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "src.core.cli is deprecated. Use 'python -m src.cli core' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Redirect to unified CLI
if __name__ == "__main__":
    # Reconstruct command with 'core' domain prefix
    original_argv = sys.argv[:]
    try:
        # Remove 'core/cli' and add 'cli core'
        sys.argv = ["src.cli", "core"] + original_argv[1:]
        from src.cli import main

        sys.exit(main())
    except ImportError:
        print("❌ Unified CLI not available. Please use: python -m src.cli core")
        sys.exit(1)
