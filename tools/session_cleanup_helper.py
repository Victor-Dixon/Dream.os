"""Session cleanup helper to generate passdown/devlog/Swarm Brain templates.

Usage:
  python tools/session_cleanup_helper.py --agent Agent-2 --summary "End-of-day" \
    --output-passdown agent_workspaces/Agent-2/passdown_draft.json \
    --output-devlog devlogs/2025-12-11_agent-2_session_cleanup_draft.md \
    --output-swarm swarm_brain/entries/2025-12-11_agent2_session_cleanup_draft.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def build_passdown(agent: str, summary: str, date: str) -> str:
    content = {
        "session_date": date,
        "agent_id": agent,
        "session_summary": summary,
        "status": "ACTIVE_AGENT_MODE",
        "current_phase": "SESSION_CLEANUP",
        "completed_work": {},
        "in_progress": {},
        "progress_metrics": {},
        "key_documents": {},
        "next_session_priorities": {"high": [], "medium": []},
        "blockers": [],
        "notes": [],
        "tools_created": [],
        "lessons_learned": [],
    }
    return json.dumps(content, indent=2)


def build_devlog(agent: str, summary: str, date: str) -> str:
    lines = [
        f"# Session Cleanup ({agent})",
        "",
        f"- Date: {date}",
        "- Status: ✅ complete",
        "",
        "## Summary",
        summary,
        "",
        "## Actions",
        "- Passdown refreshed",
        "- Swarm Brain entry drafted",
        "- Discord devlog ready",
        "- Helper tool available: tools/session_cleanup_helper.py",
        "",
        "## Next Steps",
        "- Post devlog to Discord",
        "- Capture any blockers and update passdown",
    ]
    return "\n".join(lines)


def build_swarm_entry(agent: str, summary: str, date: str) -> str:
    content = {
        "date": date,
        "agent": agent,
        "topic": "session_cleanup_template",
        "insights": [summary],
        "patterns": [
            "Bundle passdown + devlog + Swarm Brain entry for each session cleanup.",
            "Keep blockers explicit (deploy windows, approvals) to avoid hidden stalls.",
        ],
        "actions": [
            "Generated session cleanup templates for reuse.",
            "Pre-seeded evidence paths for devlog/Swarm Brain/passdown drafts.",
        ],
        "next_steps": ["Fill templates with real data and post devlog to Discord."],
        "evidence": [],
    }
    return json.dumps(content, indent=2)


def write_file(path: Optional[str], content: str) -> Optional[Path]:
    if not path:
        return None
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate session cleanup templates for passdown/devlog/Swarm Brain entries."
    )
    parser.add_argument("--agent", required=True, help="Agent id (e.g., Agent-2).")
    parser.add_argument("--summary", required=True, help="Short session summary.")
    parser.add_argument(
        "--date", default=datetime.utcnow().strftime("%Y-%m-%d"), help="ISO date."
    )
    parser.add_argument("--output-passdown", help="Path to write passdown JSON draft.")
    parser.add_argument("--output-devlog", help="Path to write devlog markdown draft.")
    parser.add_argument("--output-swarm", help="Path to write Swarm Brain JSON draft.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    passdown = build_passdown(args.agent, args.summary, args.date)
    devlog = build_devlog(args.agent, args.summary, args.date)
    swarm_entry = build_swarm_entry(args.agent, args.summary, args.date)

    written: List[Path] = []
    for path, content in (
        (args.output_passdown, passdown),
        (args.output_devlog, devlog),
        (args.output_swarm, swarm_entry),
    ):
        target = write_file(path, content)
        if target:
            written.append(target)

    if written:
        print("Generated templates:", ", ".join(str(p) for p in written))
    else:
        print(passdown)
        print()
        print(devlog)
        print()
        print(swarm_entry)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Session Cleanup Helper

Generates lightweight passdown/devlog scaffolds to reduce wrap-up friction.
Usage:
  python tools/session_cleanup_helper.py --summary "One-liner" --blockers "auth,theme"

Outputs a markdown snippet with summary, blockers, next-actions, and artifacts.
"""
import argparse
import json
from datetime import datetime
from typing import List, Dict


def parse_list(raw: str) -> List[str]:
  if not raw:
    return []
  return [item.strip() for item in raw.split(",") if item.strip()]


def build_payload(args: argparse.Namespace) -> Dict[str, object]:
  now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
  return {
      "generated_at": now,
      "summary": args.summary or "No summary provided.",
      "blockers": parse_list(args.blockers),
      "next_actions": parse_list(args.next_actions),
      "artifacts": parse_list(args.artifacts),
      "notes": args.notes or "",
  }


def to_markdown(payload: Dict[str, object]) -> str:
  lines = [
      f"### Session Wrap ({payload['generated_at']})",
      f"- Summary: {payload['summary']}",
      f"- Blockers: {', '.join(payload['blockers']) if payload['blockers'] else 'None'}",
      f"- Next actions: {', '.join(payload['next_actions']) if payload['next_actions'] else 'None'}",
      f"- Artifacts: {', '.join(payload['artifacts']) if payload['artifacts'] else 'None'}",
  ]
  if payload["notes"]:
    lines.append(f"- Notes: {payload['notes']}")
  return "\n".join(lines)


def main() -> None:
  parser = argparse.ArgumentParser(description="Generate session wrap scaffolds.")
  parser.add_argument("--summary", help="Short summary line.", default="")
  parser.add_argument("--blockers", help="Comma list of blockers.", default="")
  parser.add_argument("--next-actions", dest="next_actions", help="Comma list of next actions.", default="")
  parser.add_argument("--artifacts", help="Comma list of artifact paths.", default="")
  parser.add_argument("--notes", help="Optional notes.", default="")
  parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format.")
  args = parser.parse_args()

  payload = build_payload(args)
  if args.format == "json":
    print(json.dumps(payload, indent=2))
  else:
    print(to_markdown(payload))


if __name__ == "__main__":
  main()
"""Helper to generate a ready-to-post Discord summary from passdown + devlog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_PASSDOWN = Path("agent_workspaces/Agent-7/passdown.json")


def load_json(path: Path) -> Dict[str, Any]:
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def summarize_devlog(path: Optional[Path]) -> str:
  if not path or not path.exists():
    return "Devlog: pending upload. 📝 DISCORD DEVLOG REMINDER: Create a Discord devlog."
  lines = path.read_text(encoding="utf-8").splitlines()
  head = [line for line in lines if line and not line.startswith("#")][:3]
  summary = " ".join(head) if head else path.name
  return f"Devlog: {summary}"


def build_discord_message(passdown: Dict[str, Any], devlog_line: str) -> str:
  summary = passdown.get("session_summary", {})
  blockers = passdown.get("blockers", [])
  next_actions = passdown.get("next_actions", [])
  coordination = passdown.get("coordination_needs", [])

  lines = [
    "[A2A] Agent-7",
    f"Session: {summary.get('session_type', 'n/a')}",
    f"Mission: {summary.get('primary_mission', 'n/a')}",
    f"Status: {summary.get('status', 'n/a')} | Progress: {summary.get('progress', '')}",
    f"Blockers: {', '.join(blockers) if blockers else 'None'}",
    f"Next: {', '.join(next_actions[:3]) if next_actions else 'None'}",
    f"Coordination: {', '.join(coordination[:3]) if coordination else 'None'}",
    devlog_line,
    "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory",
  ]
  return "\n".join(lines)


def main() -> None:
  parser = argparse.ArgumentParser(description="Generate Discord summary from passdown + devlog.")
  parser.add_argument("--passdown", type=Path, default=DEFAULT_PASSDOWN, help="Path to passdown.json")
  parser.add_argument("--devlog", type=Path, default=None, help="Optional devlog markdown path")
  args = parser.parse_args()

  passdown = load_json(args.passdown)
  devlog_line = summarize_devlog(args.devlog)
  print(build_discord_message(passdown, devlog_line))


if __name__ == "__main__":
  main()