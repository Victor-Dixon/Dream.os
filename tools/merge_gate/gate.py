#!/usr/bin/env python3
"""Merge Gate v1 orchestrator (patch-only seatbelt)."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: PyYAML is required for merge gate tasks ({exc})", file=sys.stderr)
    raise


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def dump_yaml(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False)


def merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def run_command(command: str, cwd: Path, log_path: Path) -> tuple[int, float]:
    start = time.time()
    proc = subprocess.run(
        command,
        cwd=str(cwd),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    duration = round(time.time() - start, 3)
    log_path.write_text(proc.stdout or "", encoding="utf-8")
    return proc.returncode, duration


def safe_task_id(raw: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", raw).strip("-") or "task"


def parse_numstat(output: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) < 3:
            continue
        added_raw, deleted_raw, file_path = parts
        added = 0 if added_raw == "-" else int(added_raw)
        deleted = 0 if deleted_raw == "-" else int(deleted_raw)
        rows.append({"path": file_path, "added": added, "deleted": deleted})
    return rows


def parse_name_status(output: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0]
        # Rename lines include old and new path: R100 old new
        path = parts[-1]
        rows.append({"status": status, "path": path, "raw": line})
    return rows


def collect_diff_stats(repo_root: Path, diff_range: str, artifact_dir: Path) -> dict[str, Any]:
    command = f'git diff --numstat "{diff_range}" --'
    log_path = artifact_dir / "diff_numstat.log"
    code, duration = run_command(command, repo_root, log_path)
    status_command = f'git diff --name-status "{diff_range}" --'
    status_log_path = artifact_dir / "diff_name_status.log"
    status_code, status_duration = run_command(status_command, repo_root, status_log_path)
    if code != 0:
        return {
            "ok": False,
            "name": "diff_stats",
            "duration_s": duration,
            "reason": f"git diff failed for range '{diff_range}'",
            "artifact": str(log_path),
            "stats": {},
        }
    if status_code != 0:
        return {
            "ok": False,
            "name": "diff_stats",
            "duration_s": round(duration + status_duration, 3),
            "reason": f"git diff --name-status failed for range '{diff_range}'",
            "artifact": str(status_log_path),
            "stats": {},
        }

    rows = parse_numstat(log_path.read_text(encoding="utf-8"))
    status_rows = parse_name_status(status_log_path.read_text(encoding="utf-8"))
    new_files = [r["path"] for r in status_rows if r["status"].startswith("A")]
    files_changed = len(rows)
    added = sum(r["added"] for r in rows)
    deleted = sum(r["deleted"] for r in rows)
    changed_files = [r["path"] for r in rows]
    return {
        "ok": True,
        "name": "diff_stats",
        "duration_s": round(duration + status_duration, 3),
        "reason": "ok",
        "artifact": str(log_path),
        "stats": {
            "range": diff_range,
            "files_changed": files_changed,
            "lines_added": added,
            "lines_deleted": deleted,
            "changed_files": changed_files,
            "new_files": new_files,
            "rows": rows,
            "status_rows": status_rows,
        },
    }


def enforce_diff_contract(
    diff_stats: dict[str, Any], contract: dict[str, Any], contracts_cfg: dict[str, Any]
) -> dict[str, Any]:
    start = time.time()
    if not diff_stats.get("ok"):
        return {
            "ok": False,
            "name": "diff_contract",
            "duration_s": round(time.time() - start, 3),
            "reason": "diff_stats failed; cannot enforce diff contract",
            "violations": [diff_stats.get("reason", "unknown diff error")],
        }

    stats = diff_stats["stats"]
    max_files = int(contract.get("max_files", 10))
    max_added = int(contract.get("max_added_lines", 400))
    max_deleted = int(contract.get("max_deleted_lines", 400))
    allowlist = contract.get("allowlist", []) or []
    allow_new_files = bool(contracts_cfg.get("allow_new_files", False))
    new_file_allowlist = contracts_cfg.get("new_file_allowlist", []) or []

    violations: list[str] = []
    if stats["files_changed"] > max_files:
        violations.append(
            f"files_changed {stats['files_changed']} exceeds max_files {max_files}"
        )
    if stats["lines_added"] > max_added:
        violations.append(
            f"lines_added {stats['lines_added']} exceeds max_added_lines {max_added}"
        )
    if stats["lines_deleted"] > max_deleted:
        violations.append(
            f"lines_deleted {stats['lines_deleted']} exceeds max_deleted_lines {max_deleted}"
        )

    if allowlist:
        for path in stats["changed_files"]:
            if not any(fnmatch.fnmatch(path, pattern) for pattern in allowlist):
                violations.append(f"touched file outside allowlist: {path}")

    if not allow_new_files:
        for path in stats.get("new_files", []):
            is_allowed = any(fnmatch.fnmatch(path, p) for p in new_file_allowlist)
            if not is_allowed:
                violations.append(
                    "new file blocked by policy: "
                    f"{path} (set contracts.allow_new_files=true or add "
                    "contracts.new_file_allowlist entry)"
                )

    return {
        "ok": len(violations) == 0,
        "name": "diff_contract",
        "duration_s": round(time.time() - start, 3),
        "reason": "ok" if not violations else "diff policy violations",
        "violations": violations,
    }


def enforce_required_outputs(
    run_dir: Path, repo_root: Path, contracts_cfg: dict[str, Any]
) -> dict[str, Any]:
    start = time.time()
    required = contracts_cfg.get("required_outputs", []) or []
    require_non_empty = bool(contracts_cfg.get("require_non_empty", True))
    missing: list[str] = []

    for rel_path in required:
        if rel_path.startswith("repo:"):
            target = repo_root / rel_path[len("repo:") :]
            label = rel_path
        elif rel_path.startswith("run:"):
            target = run_dir / rel_path[len("run:") :]
            label = rel_path
        else:
            # Default scope is the run directory artifacts.
            target = run_dir / rel_path
            label = f"run:{rel_path}"
        if not target.exists():
            missing.append(f"missing output: {label}")
            continue
        if require_non_empty and target.is_file() and target.stat().st_size == 0:
            missing.append(f"empty output: {label}")

    return {
        "ok": len(missing) == 0,
        "name": "required_outputs",
        "duration_s": round(time.time() - start, 3),
        "reason": "ok" if not missing else "required outputs missing",
        "violations": missing,
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Merge Gate Report",
        "",
        f"- Task: `{report['task_id']}`",
        f"- Status: **{report['status']}**",
        f"- Started: `{report['started_at']}`",
        f"- Ended: `{report['ended_at']}`",
        f"- Duration: `{report['duration_s']}s`",
        "",
        "## Checks",
    ]
    for check in report["checks"]:
        state = "PASS" if check.get("ok") else "FAIL"
        lines.append(f"- `{check['name']}`: **{state}** ({check.get('duration_s', 0)}s)")
        reason = check.get("reason")
        if reason and reason != "ok":
            lines.append(f"  - reason: {reason}")
        for violation in check.get("violations", []):
            lines.append(f"  - violation: {violation}")
        if check.get("artifact"):
            lines.append(f"  - artifact: `{check['artifact']}`")
    if report["fail_reasons"]:
        lines.append("")
        lines.append("## Fail reasons")
        for reason in report["fail_reasons"]:
            lines.append(f"- {reason}")
    return "\n".join(lines) + "\n"


def render_patch_report(
    task_id: str,
    diff_stats: dict[str, Any],
    checks: list[dict[str, Any]],
    run_dir: Path,
    status: str | None = None,
    fail_reasons: list[str] | None = None,
) -> str:
    now = datetime.now().isoformat()
    lines = [
        "# Patch Report",
        "",
        f"- Task ID: `{task_id}`",
        f"- Generated: `{now}`",
        f"- Run Dir: `{run_dir}`",
    ]
    if status:
        lines.append(f"- Gate Status: **{status}**")

    stats = diff_stats.get("stats", {}) if diff_stats.get("ok") else {}
    if stats:
        lines.extend(
            [
                "",
                "## Diff Summary",
                f"- Range: `{stats.get('range')}`",
                f"- Files changed: `{stats.get('files_changed')}`",
                f"- Lines added: `{stats.get('lines_added')}`",
                f"- Lines deleted: `{stats.get('lines_deleted')}`",
                f"- New files: `{len(stats.get('new_files', []))}`",
            ]
        )
        if stats.get("changed_files"):
            lines.append("")
            lines.append("### Files touched")
            for path in stats["changed_files"]:
                lines.append(f"- `{path}`")

    lines.extend(["", "## Checks run"])
    for check in checks:
        state = "PASS" if check.get("ok") else "FAIL"
        lines.append(f"- `{check['name']}`: **{state}**")
        reason = check.get("reason")
        if reason and reason != "ok":
            lines.append(f"  - reason: {reason}")

    lines.extend(["", "## Artifact paths"])
    # Include check-level artifacts first.
    emitted: set[str] = set()
    for check in checks:
        artifact = check.get("artifact")
        if artifact and artifact not in emitted:
            lines.append(f"- `{artifact}`")
            emitted.add(artifact)
    # Include canonical run artifacts.
    for rel in ("report.json", "report.md", "task_resolved.yaml", "patch_report.md"):
        artifact = str(run_dir / rel)
        if artifact not in emitted:
            lines.append(f"- `{artifact}`")
            emitted.add(artifact)

    if fail_reasons:
        lines.extend(["", "## Fail reasons"])
        for reason in fail_reasons:
            lines.append(f"- {reason}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge Gate v1 (patch-only)")
    parser.add_argument("--task", required=True, help="Path to task YAML")
    parser.add_argument("--contract", help="Optional contract YAML override")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    gate_root = Path(__file__).resolve().parent
    default_contract_path = gate_root / "contracts" / "default_contract.yaml"
    task_path = Path(args.task).resolve()

    if not task_path.exists():
        print(f"FAIL: task file not found: {task_path}")
        return 2
    if not default_contract_path.exists():
        print(f"FAIL: default contract not found: {default_contract_path}")
        return 2

    task_cfg = load_yaml(task_path)
    contract_cfg = load_yaml(default_contract_path)
    if args.contract:
        contract_cfg = merge_dicts(contract_cfg, load_yaml(Path(args.contract).resolve()))
    resolved = merge_dicts(contract_cfg, task_cfg)

    task_id = safe_task_id(str(resolved.get("task_id", "merge-gate-task")))
    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = gate_root / "runs" / f"{run_stamp}_{task_id}"
    artifact_dir = run_dir / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    dump_yaml(run_dir / "task_resolved.yaml", resolved)

    started_at = datetime.now().isoformat()
    checks: list[dict[str, Any]] = []

    diff_cfg = resolved.get("diff", {})
    checks_cfg = resolved.get("checks", {})
    contracts_cfg = resolved.get("contracts", {})

    diff_range = str(diff_cfg.get("range", "HEAD~1..HEAD"))
    diff_stats = collect_diff_stats(repo_root, diff_range, artifact_dir)
    checks.append(diff_stats)
    checks.append(enforce_diff_contract(diff_stats, diff_cfg, contracts_cfg))

    if checks_cfg.get("run_tests", True):
        test_cmd = str(checks_cfg.get("test_command", "python3 -m pytest -q"))
        code, duration = run_command(test_cmd, repo_root, artifact_dir / "tests.log")
        checks.append(
            {
                "ok": code == 0,
                "name": "tests",
                "duration_s": duration,
                "reason": "ok" if code == 0 else f"test command failed (exit {code})",
                "command": test_cmd,
                "artifact": str(artifact_dir / "tests.log"),
            }
        )

    if checks_cfg.get("run_lint", False):
        lint_cmd = str(checks_cfg.get("lint_command", "python3 -m ruff check ."))
        code, duration = run_command(lint_cmd, repo_root, artifact_dir / "lint.log")
        checks.append(
            {
                "ok": code == 0,
                "name": "lint",
                "duration_s": duration,
                "reason": "ok" if code == 0 else f"lint command failed (exit {code})",
                "command": lint_cmd,
                "artifact": str(artifact_dir / "lint.log"),
            }
        )

    if checks_cfg.get("run_formatter", False):
        fmt_cmd = str(
            checks_cfg.get("formatter_command", "python3 -m ruff format --check .")
        )
        code, duration = run_command(fmt_cmd, repo_root, artifact_dir / "formatter.log")
        checks.append(
            {
                "ok": code == 0,
                "name": "formatter",
                "duration_s": duration,
                "reason": "ok"
                if code == 0
                else f"formatter command failed (exit {code})",
                "command": fmt_cmd,
                "artifact": str(artifact_dir / "formatter.log"),
            }
        )

    patch_report_path = run_dir / "patch_report.md"
    try:
        patch_report_path.write_text(
            render_patch_report(task_id, diff_stats, checks, run_dir), encoding="utf-8"
        )
        checks.append(
            {
                "ok": True,
                "name": "patch_report_generation",
                "duration_s": 0.0,
                "reason": "ok",
                "artifact": str(patch_report_path),
            }
        )
    except Exception as exc:
        checks.append(
            {
                "ok": False,
                "name": "patch_report_generation",
                "duration_s": 0.0,
                "reason": f"failed to write patch report: {exc}",
                "violations": [str(exc)],
            }
        )

    checks.append(enforce_required_outputs(run_dir, repo_root, contracts_cfg))

    fail_reasons: list[str] = []
    for check in checks:
        if not check.get("ok", False):
            fail_reasons.append(f"{check['name']}: {check.get('reason', 'failed')}")
            fail_reasons.extend(check.get("violations", []))

    ended_at = datetime.now().isoformat()
    status = "PASS" if not fail_reasons else "FAIL"
    report = {
        "task_id": task_id,
        "status": status,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_s": round((datetime.fromisoformat(ended_at) - datetime.fromisoformat(started_at)).total_seconds(), 3),
        "repo_root": str(repo_root),
        "run_dir": str(run_dir),
        "checks": checks,
        "fail_reasons": fail_reasons,
    }

    (run_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (run_dir / "report.md").write_text(render_markdown_report(report), encoding="utf-8")
    patch_report_path.write_text(
        render_patch_report(
            task_id, diff_stats, checks, run_dir, status=status, fail_reasons=fail_reasons
        ),
        encoding="utf-8",
    )

    print(f"Merge Gate: {status}")
    print(f"Report: {run_dir / 'report.md'}")
    if fail_reasons:
        print("Reasons:")
        for reason in fail_reasons:
            print(f" - {reason}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
