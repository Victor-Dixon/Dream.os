#!/usr/bin/env python3
"""MASTER_TASK_LOG → Cycle Planner Bridge

Reads `MASTER_TASK_LOG.md` and writes a per-agent cycle planner JSON file.

This tool is loaded by `src/services/contract_system/manager.py` via file-path
import to avoid package-name collisions.

Exports (expected by ContractManager):
- MASTER_TASK_LOG_PATH
- parse_master_task_log(path)
- build_cycle_planner_payload(agent_id, tasks, priority)
- write_cycle_planner_file(agent_id, payload)

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_TASK_LOG_PATH = REPO_ROOT / "MASTER_TASK_LOG.md"

SECTION_INBOX_RE = re.compile(r"^##\s+.*INBOX", re.IGNORECASE)
SECTION_THIS_WEEK_RE = re.compile(r"^##\s+.*THIS WEEK", re.IGNORECASE)
TASK_LINE_RE = re.compile(r"^\s*-\s*\[(?P<checked>[ xX])\]\s*(?P<body>.+?)\s*$")
AGENT_TAG_RE = re.compile(r"\[(Agent-\d+)\]")
POINTS_RE = re.compile(r"\(\s*(\d+)\s*pts\s*\)", re.IGNORECASE)
PRIORITY_RE = re.compile(r"\*\*(CRITICAL|HIGH|MEDIUM|LOW)\*\*", re.IGNORECASE)


@dataclass(frozen=True)
class MasterTask:
    section: str
    raw: str
    title: str
    priority: str
    points: Optional[int]
    assigned_agents: List[str]
    checked: bool


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _detect_section(line: str, current: str) -> str:
    if SECTION_INBOX_RE.match(line):
        return "INBOX"
    if SECTION_THIS_WEEK_RE.match(line):
        return "THIS_WEEK"
    return current


def _extract_priority(body: str) -> str:
    m = PRIORITY_RE.search(body)
    return m.group(1).lower() if m else "medium"


def _extract_points(body: str) -> Optional[int]:
    m = POINTS_RE.search(body)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def _extract_assigned_agents(body: str) -> List[str]:
    return sorted(set(AGENT_TAG_RE.findall(body)))


def _strip_agent_tags(text: str) -> str:
    return AGENT_TAG_RE.sub("", text).strip()


def parse_master_task_log(path: Path) -> List[MasterTask]:
    """Parse MASTER_TASK_LOG.md and return structured tasks."""

    tasks: List[MasterTask] = []
    section = "UNKNOWN"

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        section = _detect_section(line, section)
        m = TASK_LINE_RE.match(line)
        if not m:
            continue
        if section not in {"INBOX", "THIS_WEEK"}:
            continue

        body = m.group("body").strip()
        checked = m.group("checked").strip().lower() == "x"
        agents = _extract_assigned_agents(body)
        tasks.append(
            MasterTask(
                section=section,
                raw=line,
                title=_strip_agent_tags(body),
                priority=_extract_priority(body),
                points=_extract_points(body),
                assigned_agents=agents,
                checked=checked,
            )
        )

    return tasks


def _filter_tasks_for_agent(agent_id: str, tasks: Iterable[MasterTask]) -> List[MasterTask]:
    out: List[MasterTask] = []
    for t in tasks:
        if t.checked:
            continue
        if agent_id in (t.assigned_agents or []):
            out.append(t)
    return out


def build_cycle_planner_payload(agent_id: str, tasks: List[MasterTask], priority: str) -> dict:
    """Build the JSON payload expected by CyclePlanner/ContractSystem."""

    today = date.today().isoformat()
    filtered = _filter_tasks_for_agent(agent_id, tasks)

    normalized = []
    for idx, t in enumerate(filtered, start=1):
        normalized.append(
            {
                "task_id": f"MTL-{t.section}-{idx}",
                "title": t.title[:180],
                "description": f"Imported from MASTER_TASK_LOG.md [{t.section}] on {today}",
                "priority": (priority or t.priority or "medium"),
                "status": "pending",
                "assigned_to": agent_id,
                "category": "master_task_log",
                "estimated_points": t.points or 0,
                "created_from": "MASTER_TASK_LOG_AUTOMATION",
                "source_line": t.raw,
            }
        )

    return {
        "created": _now_iso(),
        "agent_id": agent_id,
        "date": today,
        "tasks": normalized,
        "pending_tasks": list(normalized),
        "total_tasks": len(normalized),
        "pending_count": len(normalized),
        "source": "master_task_log_to_cycle_planner",
    }


def write_cycle_planner_file(agent_id: str, payload: dict) -> Path:
    agent_dir = REPO_ROOT / "agent_workspaces" / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out_path = agent_dir / f"cycle_planner_tasks_{today}.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Bridge MASTER_TASK_LOG.md into per-agent cycle planner JSON.")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-3)")
    parser.add_argument("--section", choices=["THIS_WEEK", "INBOX"], default="THIS_WEEK")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--max-tasks", type=int, default=10)

    args = parser.parse_args()

    all_tasks = parse_master_task_log(MASTER_TASK_LOG_PATH)
    section_tasks = [t for t in all_tasks if t.section == args.section]
    payload = build_cycle_planner_payload(agent_id=args.agent, tasks=section_tasks, priority=args.priority)

    payload["tasks"] = payload["tasks"][: args.max_tasks]
    payload["pending_tasks"] = payload["pending_tasks"][: args.max_tasks]
    payload["total_tasks"] = len(payload["tasks"])
    payload["pending_count"] = len(payload["pending_tasks"])

    out_path = write_cycle_planner_file(args.agent, payload)
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
