#!/usr/bin/env python3
"""
Services CLI - Unified Entry Point
===================================

Unified CLI for service operations.

<!-- SSOT Domain: infrastructure -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

import argparse
import sys
from typing import List


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for services CLI."""
    parser = argparse.ArgumentParser(
        description="Services CLI - Unified Entry Point"
    )
    
    # Add subcommands here
    subparsers = parser.add_subparsers(dest="command", help="Service commands")
    
    # Example: messaging subcommand
    msg_parser = subparsers.add_parser("messaging", help="Messaging operations")
    msg_parser.add_argument("--send", help="Send message")
    
    # Example: contract subcommand
    contract_parser = subparsers.add_parser("contract", help="Contract operations")
    contract_parser.add_argument("--list", action="store_true", help="List contracts")
    
    return parser


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Dispatch to appropriate handler
    if args.command == "messaging":
        try:
            from src.services.messaging_cli import main as msg_main
            return msg_main()
        except ImportError:
            print("❌ Messaging CLI not available")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
