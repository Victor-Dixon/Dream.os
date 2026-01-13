#!/usr/bin/env python3
"""
Trader Replay CLI - Dream.OS Trading Replay Journal
====================================================

Command-line interface for trading replay and journaling system.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: <400 lines, CLI pattern
Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from src.core.unified_logging_system import get_logger

from .trader_replay_orchestrator import TraderReplayOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Dream.OS Trading Replay Journal CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create session command
    create_parser = subparsers.add_parser(
        "create", help="Create a new replay session"
    )
    create_parser.add_argument(
        "--symbol", required=True, help="Trading symbol (e.g., AAPL)"
    )
    create_parser.add_argument(
        "--date", required=True, help="Session date (YYYY-MM-DD)"
    )
    create_parser.add_argument(
        "--timeframe", default="1m", help="Candle timeframe (default: 1m)"
    )
    create_parser.add_argument(
        "--agent", help="Agent ID for workspace integration"
    )

    # List sessions command
    list_parser = subparsers.add_parser(
        "list", help="List all replay sessions"
    )
    list_parser.add_argument(
        "--symbol", help="Filter by symbol"
    )

    # Start replay command
    start_parser = subparsers.add_parser(
        "start", help="Start a replay session"
    )
    start_parser.add_argument(
        "--session-id", type=int, required=True, help="Session ID"
    )

    # Step replay command
    step_parser = subparsers.add_parser(
        "step", help="Step replay forward or backward"
    )
    step_parser.add_argument(
        "--session-id", type=int, required=True, help="Session ID"
    )
    step_parser.add_argument(
        "--direction",
        choices=["forward", "backward"],
        default="forward",
        help="Step direction (default: forward)",
    )

    # Pause replay command
    pause_parser = subparsers.add_parser(
        "pause", help="Pause a replay session"
    )
    pause_parser.add_argument(
        "--session-id", type=int, required=True, help="Session ID"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Get session status"
    )
    status_parser.add_argument(
        "--session-id", type=int, required=True, help="Session ID"
    )

    # Database path option
    parser.add_argument(
        "--db-path",
        type=Path,
        help="Path to SQLite database (default: agent_workspaces/data/trader_replay.db)",
    )

    return parser


def handle_create(args, orchestrator: TraderReplayOrchestrator) -> int:
    """Handle create session command."""
    try:
        session_id = orchestrator.create_session(
            symbol=args.symbol,
            session_date=args.date,
            timeframe=args.timeframe,
            agent_id=args.agent,
        )
        print(f"✅ Created replay session {session_id}")
        print(f"   Symbol: {args.symbol}")
        print(f"   Date: {args.date}")
        print(f"   Timeframe: {args.timeframe}")
        if args.agent:
            print(f"   Agent: {args.agent}")
        return 0
    except Exception as e:
        logger.error(f"Failed to create session: {e}", exc_info=True)
        print(f"❌ Failed to create session: {e}")
        return 1


def handle_list(args, orchestrator: TraderReplayOrchestrator) -> int:
    """Handle list sessions command."""
    try:
        # Note: This requires repository implementation
        print("📋 Replay Sessions:")
        print("=" * 60)
        print("⚠️  List functionality requires repository integration")
        print("    Use status command with session ID for now")
        return 0
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}", exc_info=True)
        print(f"❌ Failed to list sessions: {e}")
        return 1


def handle_start(args, orchestrator: TraderReplayOrchestrator) -> int:
    """Handle start replay command."""
    try:
        state = orchestrator.start_replay(args.session_id)
        print(f"✅ Started replay session {args.session_id}")
        print(f"   Current index: {state.get('current_index', 0)}")
        print(f"   Total candles: {state.get('total_candles', 0)}")
        print(f"   Progress: {state.get('progress', 0.0):.1%}")
        return 0
    except Exception as e:
        logger.error(f"Failed to start replay: {e}", exc_info=True)
        print(f"❌ Failed to start replay: {e}")
        return 1


def handle_step(args, orchestrator: TraderReplayOrchestrator) -> int:
    """Handle step replay command."""
    try:
        state = orchestrator.step_replay(
            args.session_id, direction=args.direction
        )
        print(
            f"✅ Stepped replay {args.direction} (session {args.session_id})"
        )
        print(f"   Current index: {state.get('current_index', 0)}")
        print(f"   Progress: {state.get('progress', 0.0):.1%}")
        return 0
    except Exception as e:
        logger.error(f"Failed to step replay: {e}", exc_info=True)
        print(f"❌ Failed to step replay: {e}")
        return 1


def handle_pause(args, orchestrator: TraderReplayOrchestrator) -> int:
    """Handle pause replay command."""
    try:
        orchestrator.pause_replay(args.session_id)
        print(f"✅ Paused replay session {args.session_id}")
        return 0
    except Exception as e:
        logger.error(f"Failed to pause replay: {e}", exc_info=True)
        print(f"❌ Failed to pause replay: {e}")
        return 1


def handle_status(args, orchestrator: TraderReplayOrchestrator) -> int:
    """Handle status command."""
    try:
        status = orchestrator.get_session_status(args.session_id)
        if not status:
            print(f"❌ Session {args.session_id} not found")
            return 1

        print(f"📊 Session Status: {args.session_id}")
        print("=" * 60)
        for key, value in status.items():
            print(f"   {key}: {value}")
        return 0
    except Exception as e:
        logger.error(f"Failed to get status: {e}", exc_info=True)
        print(f"❌ Failed to get status: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Initialize orchestrator
    try:
        orchestrator = TraderReplayOrchestrator(db_path=args.db_path)
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}", exc_info=True)
        print(f"❌ Failed to initialize orchestrator: {e}")
        return 1

    # Route to appropriate handler
    handlers = {
        "create": handle_create,
        "list": handle_list,
        "start": handle_start,
        "step": handle_step,
        "pause": handle_pause,
        "status": handle_status,
    }

    handler = handlers.get(args.command)
    if not handler:
        parser.print_help()
        return 1

    return handler(args, orchestrator)


if __name__ == "__main__":
    exit_code = main()
    print()  # Line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡🔥")  # Completion indicator
    sys.exit(exit_code)



