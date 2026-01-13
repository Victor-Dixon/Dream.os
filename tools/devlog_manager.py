#!/usr/bin/env python3
"""
Devlog Manager

Stable CLI entrypoint for posting/validating devlogs.

Contract-required command:
  python tools/devlog_manager.py post --agent Agent-X --file <devlog_file.md>

This wrapper is intentionally lightweight to avoid import collisions between
repo-root `tools/` scripts and `src/tools` (package-style) modules.

<!-- SSOT Domain: infrastructure -->
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _run(cmd: list[str]) -> int:
    return subprocess.call(cmd, cwd=str(_repo_root()))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="devlog_manager",
        description="Manage devlogs (post/validate).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    post_parser = subparsers.add_parser("post", help="Post a devlog to the agent-specific Discord channel")
    post_parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-3)")
    post_parser.add_argument("--file", required=True, help="Path to devlog markdown file")
    post_parser.add_argument("--title", help="Optional title override")

    validate_parser = subparsers.add_parser("validate", help="Validate devlog compliance")
    validate_parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-3)")
    validate_parser.add_argument("--file", required=True, help="Path to devlog markdown file")

    args = parser.parse_args()

    # Canonical scripts are optional in some deployments; fail with a clear error if missing.
    if args.command == "post":
        script = _repo_root() / "tools" / "devlog_poster_agent_channel.py"
        if not script.exists():
            print(f"❌ Missing tool: {script}", file=sys.stderr)
            return 2
        cmd = [sys.executable, str(script), "--agent", args.agent, "--file", args.file]
        if args.title:
            cmd += ["--title", args.title]
        return _run(cmd)

    if args.command == "validate":
        script = _repo_root() / "tools" / "devlog_compliance_validator.py"
        if not script.exists():
            print(f"❌ Missing tool: {script}", file=sys.stderr)
            return 2
        cmd = [sys.executable, str(script), "--agent", args.agent, "--file", args.file]
        return _run(cmd)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())



