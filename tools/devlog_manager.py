#!/usr/bin/env python3
"""
Devlog Manager
==============

Thin wrapper around existing devlog posting tooling.

This script exists to provide a stable interface for posting completion reports
to Discord using the required command:

  python tools/devlog_manager.py post --agent Agent-7 --file devlogs/<file>.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def post(agent_id: str, file_path: str, title: str | None) -> int:
    project_root = _project_root()
    sys.path.insert(0, str(project_root))

    from tools.devlog_poster import post_devlog

    ok = post_devlog(agent_id=agent_id, devlog_path=file_path, title=title)
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="devlog_manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    post_parser = subparsers.add_parser("post", help="Post a devlog to Discord")
    post_parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-7)")
    post_parser.add_argument("--file", required=True, help="Path to devlog markdown file")
    post_parser.add_argument("--title", help="Optional title override")

    args = parser.parse_args()

    if args.command == "post":
        return post(agent_id=args.agent, file_path=args.file, title=args.title)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())


