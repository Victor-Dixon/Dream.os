#!/usr/bin/env python3
"""
Services CLI - DEPRECATED
=========================

⚠️ DEPRECATED: This CLI entry point has been consolidated.
Use the unified CLI instead: python -m src.cli services <command>

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
    "src.services.cli is deprecated. Use 'python -m src.cli services' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Redirect to unified CLI
if __name__ == "__main__":
    # Reconstruct command with 'services' domain prefix
    original_argv = sys.argv[:]
    try:
        # Remove 'services/cli' and add 'cli services'
        sys.argv = ["src.cli", "services"] + original_argv[1:]
        from src.cli import main

        sys.exit(main())
    except ImportError:
        print("❌ Unified CLI not available. Please use: python -m src.cli services")
        sys.exit(1)
