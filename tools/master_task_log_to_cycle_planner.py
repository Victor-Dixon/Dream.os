#!/usr/bin/env python3
"""
MASTER_TASK_LOG → Cycle Planner Bridge
=====================================

Seeds `agent_workspaces/{Agent-X}/cycle_planner_tasks_YYYY-MM-DD.json` from
`MASTER_TASK_LOG.md` tasks.

This tool exists because the contract system can fall back to seeding cycle
planner tasks from MASTER_TASK_LOG when both queues are empty.

<!-- SSOT Domain: infrastructure -->
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone, date
from pathlib import Path
from typing import Iterable, List


REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_TASK_LOG_PATH = REPO_ROOT / "MASTER_TASK_LOG.md"


_SECTION_HEADER_RE = re.compile(r"^##\s+(?P<header>.+?)\s*$")
_TASK_LINE_RE = re.compile(r"^\s*-\s+\[(?P<checked>[ xX])\]\s+(?P<body>.+?)\s*$")
_AGENT_TAG_RE = re.compile(r"\[(Agent-\d+)\]\s*$")
_PRIORITY_RE = re.compile(r"\*\*(CRITICAL|HIGH|MEDIUM|LOW)\*\*", re.IGNORECASE)
_POINTS_RE = re.compile(r"\((\d+)\s*pts\)", re.IGNORECASE)


@dataclass(frozen=True)
class MasterTask:
    """Normalized representation of a task line from MASTER_TASK_LOG.md."""

    raw_line: str
    section: str
    assigned_agent: str
    priority: str
    points: int


def _normalize_section(header: str) -> str:
    h = header.strip().upper()
    if h in {"INBOX", "THIS WEEK", "THIS_WEEK"}:
        return "THIS_WEEK" if h in {"THIS WEEK", "THIS_WEEK"} else "INBOX"
    return h.replace(" ", "_")


def _priority_from_text(text: str) -> str:
    m = _PRIORITY_RE.search(text)
    if not m:
        return "medium"
    return m.group(1).lower()


def _points_from_text(text: str) -> int:
    m = _POINTS_RE.search(text)
    if not m:
        return 50
    try:
        return int(m.group(1))
    except ValueError:
        return 50


def parse_master_task_log(path: Path) -> List[MasterTask]:
    """
    Parse `MASTER_TASK_LOG.md` into tasks.

    Only returns tasks that are:
    - Unchecked (`- [ ] ...`)
    - Assigned to a specific agent at end of line: `[Agent-X]`
    - In sections that have an active section context
    """
    if not path.exists():
        return []

    tasks: List[MasterTask] = []
    current_section = "UNKNOWN"
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        header_m = _SECTION_HEADER_RE.match(raw)
        if header_m:
            current_section = _normalize_section(header_m.group("header"))
            continue

        task_m = _TASK_LINE_RE.match(raw)
        if not task_m:
            continue

        if task_m.group("checked").strip():
            # Completed task
            continue

        body = task_m.group("body")
        agent_m = _AGENT_TAG_RE.search(body)
        if not agent_m:
            continue

        assigned_agent = agent_m.group(1)
        tasks.append(
            MasterTask(
                raw_line=raw.strip(),
                section=current_section,
                assigned_agent=assigned_agent,
                priority=_priority_from_text(body),
                points=_points_from_text(body),
            )
        )

    return tasks


def build_cycle_planner_payload(agent_id: str, tasks: Iterable[MasterTask], priority: str) -> dict:
    """
    Build cycle planner JSON payload compatible with `CyclePlannerIntegration`.
    """
    today = date.today().isoformat()
    created = datetime.now(timezone.utc).isoformat()

    out_tasks = []
    for idx, t in enumerate(tasks, start=1):
        out_tasks.append(
            {
                "task_id": f"MTL-{t.section}-{idx}",
                "title": t.raw_line[:240],
                "description": f"Imported from MASTER_TASK_LOG.md [{t.section}] on {today}",
                "priority": (priority or t.priority or "medium").lower(),
                "status": "pending",
                "assigned_to": agent_id,
                "category": "master_task_log",
                "estimated_points": int(t.points),
                "created_from": "MASTER_TASK_LOG",
                "section": t.section,
            }
        )

    payload = {
        "created": created,
        "agent_id": agent_id,
        "date": today,
        "tasks": out_tasks,
        "pending_tasks": [t for t in out_tasks if t.get("status") in {"pending", "ready"}],
        "total_tasks": len(out_tasks),
        "pending_count": len([t for t in out_tasks if t.get("status") in {"pending", "ready"}]),
        "source": "master_task_log_to_cycle_planner",
    }
    return payload


def write_cycle_planner_file(agent_id: str, payload: dict) -> Path:
    agent_dir = REPO_ROOT / "agent_workspaces" / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)

    day = payload.get("date") or date.today().isoformat()
    out_path = agent_dir / f"cycle_planner_tasks_{day}.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def _filter_tasks_for_agent(tasks: Iterable[MasterTask], agent_id: str, section: str) -> List[MasterTask]:
    return [t for t in tasks if t.assigned_agent == agent_id and t.section == section]


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed cycle planner tasks from MASTER_TASK_LOG.md")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-3)")
    parser.add_argument("--section", default="INBOX", help="Section to import (INBOX or THIS_WEEK)")
    parser.add_argument("--priority", default="medium", help="Priority to apply (high/medium/low)")
    parser.add_argument("--max-tasks", type=int, default=25, help="Max tasks to import")
    parser.add_argument("--dry-run", action="store_true", help="Print payload summary without writing file")
    args = parser.parse_args()

    section = _normalize_section(args.section)
    parsed = parse_master_task_log(MASTER_TASK_LOG_PATH)
    selected = _filter_tasks_for_agent(parsed, args.agent, section)[: max(args.max_tasks, 0)]

    # Fallback: if requested section empty, try INBOX
    if not selected and section != "INBOX":
        selected = _filter_tasks_for_agent(parsed, args.agent, "INBOX")[: max(args.max_tasks, 0)]

    payload = build_cycle_planner_payload(agent_id=args.agent, tasks=selected, priority=args.priority)

    if args.dry_run:
        print(f"agent={args.agent} section={section} total_tasks={payload.get('total_tasks', 0)}")
        return 0

    out = write_cycle_planner_file(args.agent, payload)
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


