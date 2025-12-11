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