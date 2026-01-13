#!/usr/bin/env python3
"""
Unified CLI Entry Point
=======================

Unified command-line interface for all system operations.
Consolidates services and core CLI entry points into a single access point.

<!-- SSOT Domain: infrastructure -->

V2 Compliance: <300 lines, single responsibility
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-21
Consolidation: Merged src/services/cli and src/core/cli
"""

import argparse
import sys
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    """Create unified argument parser."""
    parser = argparse.ArgumentParser(
        description="Unified CLI - Single Entry Point for All Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.cli messaging --help
  python -m src.cli core performance --status
  python -m src.cli services messaging --send "Hello"
        """,
    )

    subparsers = parser.add_subparsers(
        dest="domain", help="Domain commands", metavar="DOMAIN"
    )

    # Services subcommands
    services_parser = subparsers.add_parser("services", help="Service operations")
    services_subparsers = services_parser.add_subparsers(
        dest="command", help="Service commands"
    )

    # Messaging command
    msg_parser = services_subparsers.add_parser(
        "messaging", help="Messaging operations"
    )
    msg_parser.add_argument("--send", help="Send message")
    # Pass through remaining args to messaging CLI
    msg_parser.add_argument("args", nargs=argparse.REMAINDER, help="Messaging CLI args")

    # Contract command
    contract_parser = services_subparsers.add_parser(
        "contract", help="Contract operations"
    )
    contract_parser.add_argument("--list", action="store_true", help="List contracts")

    # Core subcommands
    core_parser = subparsers.add_parser("core", help="Core system operations")
    core_subparsers = core_parser.add_subparsers(
        dest="command", help="Core system commands"
    )

    # Performance command
    perf_parser = core_subparsers.add_parser(
        "performance", help="Performance operations"
    )
    perf_parser.add_argument("--status", action="store_true", help="Get performance status")

    return parser


def handle_services_command(args: argparse.Namespace) -> int:
    """Handle services domain commands."""
    if args.command == "messaging":
        try:
            # Import messaging CLI and pass through args
            from src.services.messaging_cli import main as msg_main

            # Reconstruct sys.argv for messaging CLI
            original_argv = sys.argv[:]
            try:
                # Remove 'services messaging' from args
                sys.argv = ["messaging_cli"] + (args.args or [])
                return msg_main()
            finally:
                sys.argv = original_argv
        except ImportError as e:
            print(f"❌ Messaging CLI not available: {e}")
            return 1
    elif args.command == "contract":
        if args.list:
            try:
                from src.services.contract_service import ContractService

                service = ContractService()
                contracts = service.list_contracts()
                print("\n📋 Active Contracts:")
                for contract in contracts:
                    print(f"  - {contract}")
                return 0
            except ImportError:
                print("❌ Contract service not available")
                return 1
        else:
            print("💡 Use --list to list contracts")
            return 1
    else:
        print(f"❌ Unknown services command: {args.command}")
        return 1


def handle_core_command(args: argparse.Namespace) -> int:
    """Handle core domain commands."""
    if args.command == "performance":
        if args.status:
            try:
                from src.core.performance.performance_cli import main as perf_main

                return perf_main()
            except ImportError as e:
                print(f"❌ Performance CLI not available: {e}")
                return 1
        else:
            print("💡 Use --status to get performance status")
            return 1
    else:
        print(f"❌ Unknown core command: {args.command}")
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.domain:
        parser.print_help()
        return 1

    try:
        if args.domain == "services":
            return handle_services_command(args)
        elif args.domain == "core":
            return handle_core_command(args)
        else:
            print(f"❌ Unknown domain: {args.domain}")
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


