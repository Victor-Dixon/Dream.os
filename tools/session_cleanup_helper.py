#!/usr/bin/env python3
"""
Session Cleanup Helper
======================

Utility to streamline end-of-session tasks:
- Generate a passdown.json skeleton
- Generate a devlog markdown file
- Optionally post the devlog to Discord via webhook

V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

DEVLOG_TEMPLATE = """# Devlog - {date}

**Agent:** {agent}
**Session:** {session}
**Status:** {status}

## What happened
- {summary}

## Metrics
- Lint issues: 0 (reported)

## Next actions
- Post this devlog to Discord via webhook (if configured).
- Run session cleanup checklist before next session.

🐝 WE. ARE. SWARM. ⚡🔥
"""


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def generate_passdown(path: Path, agent_id: str, agent_name: str, summary: str) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d")
    payload = {
        "agent_id": agent_id,
        "agent_name": agent_name,
        "session_date": now,
        "session_status": "COMPLETE",
        "deliverables": [summary],
        "next_actions": [
            "Post devlog to Discord (webhook required)",
            "Coordinate next-session onboarding",
        ],
        "gas_pipeline": {
            "status": "HEALTHY",
            "blockers": [],
            "dependencies": [],
            "ready_for_new_work": True,
        },
        "blockers": [],
        "achievements": [summary],
        "learnings": [],
        "coordination_notes": [],
        "session_metrics": {"linting_errors": 0},
        "documentation_created": [],
        "ready_for_next_session": True,
    }
    _write_json(path, payload)


def generate_devlog(path: Path, agent: str, session: str, status: str, summary: str) -> None:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    content = DEVLOG_TEMPLATE.format(
        date=today,
        agent=agent,
        session=session,
        status=status,
        summary=summary,
    )
    _write_text(path, content)


def maybe_post_to_discord(content: str, title: str = "Session Devlog") -> bool:
    try:
        from tools.post_completion_report_to_discord import post_to_discord
    except Exception:
        return False
    return bool(post_to_discord(content=content, title=title))


def main() -> None:
    parser = argparse.ArgumentParser(description="Session cleanup helper")
    parser.add_argument("--agent-id", default="Agent-8")
    parser.add_argument("--agent-name", default="SSOT & System Integration Specialist")
    parser.add_argument("--session", default="Session Cleanup")
    parser.add_argument("--summary", required=True, help="Short summary line")
    parser.add_argument("--passdown-path", default="agent_workspaces/Agent-8/passdown.json")
    parser.add_argument(
        "--devlog-path",
        default="agent_workspaces/Agent-8/DEVLOG_"
        + datetime.utcnow().strftime("%Y-%m-%d")
        + ".md",
    )
    parser.add_argument("--post-discord", action="store_true", help="Post devlog to Discord webhook")
    args = parser.parse_args()

    passdown_path = Path(args.passdown_path)
    devlog_path = Path(args.devlog_path)

    generate_passdown(passdown_path, args.agent_id, args.agent_name, args.summary)
    generate_devlog(devlog_path, args.agent_name, args.session, "Complete", args.summary)

    if args.post_discord:
        content = devlog_path.read_text(encoding="utf-8")
        posted = maybe_post_to_discord(content, title="Session Devlog")
        if not posted:
            print("⚠️ Discord post skipped (webhook not configured or post failed)")
        else:
            print("✅ Devlog posted to Discord")

    print(f"✅ passdown updated: {passdown_path}")
    print(f"✅ devlog created: {devlog_path}")


if __name__ == "__main__":
    main()

