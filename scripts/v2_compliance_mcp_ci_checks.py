#!/usr/bin/env python3
"""
CI helper for running v2_compliance_server checks against MCP servers
and core orchestrator modules.

This is intentionally small and self-contained so it can be invoked
directly from GitHub Actions or local scripts without requiring the
full MCP JSON-RPC protocol.
"""

from __future__ import annotations
from mcp_servers import v2_compliance_server as vc

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ensure project root is importable so `mcp_servers` and friends can be resolved
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# High-priority MCP server entrypoints
MCP_FILES: List[str] = [
    "mcp_servers/task_manager_server.py",
    "mcp_servers/website_manager_server.py",
    "mcp_servers/swarm_brain_server.py",
    "mcp_servers/git_operations_server.py",
    "mcp_servers/v2_compliance_server.py",
]

# Core orchestrators and orchestrator-like modules that are central to runtime
ORCHESTRATOR_FILES: List[str] = [
    "src/orchestrators/overnight/orchestrator.py",
    "src/core/orchestration/base_orchestrator.py",
    "src/core/agent_self_healing_system.py",
    "src/core/message_queue_processor.py",
    "src/services/chat_presence/chat_presence_orchestrator.py",
]


def run_v2_checks(relative_paths: List[str]) -> Dict[str, Any]:
    """Run v2_compliance_server.check_v2_compliance against each path."""
    summary: Dict[str, Any] = {
        "project_root": str(PROJECT_ROOT),
        "total_files": len(relative_paths),
        "files_with_violations": 0,
        "total_violations": 0,
        "exceptions": 0,
        "files": [],
    }

    for rel_path in relative_paths:
        abs_path = PROJECT_ROOT / rel_path

        result = vc.check_v2_compliance(str(abs_path))
        file_entry: Dict[str, Any] = {"path": rel_path}

        if not result.get("success"):
            file_entry["error"] = result.get("error", "Unknown error")
            summary["files"].append(file_entry)
            continue

        line_count = result.get("line_count")
        violations = int(result.get("violations_count", 0))
        is_exception = bool(result.get("is_exception", False))

        file_entry.update(
            {
                "line_count": line_count,
                "violations": violations,
                "is_exception": is_exception,
                "is_compliant": bool(result.get("is_compliant", False)),
            }
        )

        if violations and not is_exception:
            summary["files_with_violations"] += 1
            summary["total_violations"] += violations
        if is_exception:
            summary["exceptions"] += 1

        summary["files"].append(file_entry)

    return summary


def print_human_summary(summary: Dict[str, Any]) -> None:
    """Print a compact, human-readable summary for CI logs."""
    print("🔍 V2 compliance check (MCP servers + core orchestrators)")
    print(f"- Project root: {summary.get('project_root')}")
    print(f"- Files checked: {summary.get('total_files')}")
    print(
        f"- Files with violations (non-exception): "
        f"{summary.get('files_with_violations')} "
        f"(total violations: {summary.get('total_violations')})"
    )
    print(f"- Files marked as V2 exceptions: {summary.get('exceptions')}")
    print()
    print("Per-file status:")

    for entry in summary.get("files", []):
        path = entry["path"]
        if "error" in entry:
            print(f"  - {path}: ERROR - {entry['error']}")
            continue

        status = "OK"
        if entry["violations"] and not entry["is_exception"]:
            status = "HAS VIOLATIONS"
        elif entry["is_exception"]:
            status = "EXCEPTION"

        print(
            f"  - {path}: {status} "
            f"(lines={entry['line_count']}, "
            f"violations={entry['violations']}, "
            f"exception={entry['is_exception']})"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run v2_compliance_server checks for MCP + core orchestrators."
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=PROJECT_ROOT
        / "reports"
        / "v2_compliance"
        / "mcp_and_orchestrators_ci_summary.json",
        help="Where to write a machine-readable JSON summary.",
    )
    parser.add_argument(
        "--no-human-summary",
        action="store_true",
        help="If set, do not print the human-readable summary to stdout.",
    )
    args = parser.parse_args()

    all_paths = MCP_FILES + ORCHESTRATOR_FILES
    summary = run_v2_checks(all_paths)

    output_path: Path = args.output_json
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"✅ Wrote V2 compliance CI summary to {output_path}")

    if not args.no_human_summary:
        print()
        print_human_summary(summary)


if __name__ == "__main__":
    main()

