#!/usr/bin/env python3
"""
Core System CLI - Unified Entry Point
======================================

Unified CLI for core system operations.

<!-- SSOT Domain: infrastructure -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

import argparse
import sys
from typing import List


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for core CLI."""
    parser = argparse.ArgumentParser(
        description="Core System CLI - Unified Entry Point"
    )
    
    # Add subcommands here
    subparsers = parser.add_subparsers(dest="command", help="Core system commands")
    
    # Example: performance subcommand
    perf_parser = subparsers.add_parser("performance", help="Performance operations")
    perf_parser.add_argument("--status", action="store_true", help="Get performance status")
    
    return parser


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Dispatch to appropriate handler
    if args.command == "performance":
        if args.status:
            # Import and call performance CLI
            try:
                from src.core.performance.performance_cli import main as perf_main
                return perf_main()
            except ImportError:
                print("❌ Performance CLI not available")
                return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
