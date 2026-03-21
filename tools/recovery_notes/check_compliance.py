# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: Enforce phased recovery-notes protocol compliance and emit reports.
# SSOT: docs/recovery/recovery_registry.yaml#recovery-notes-compliance-checker
# @registry docs/recovery/recovery_registry.yaml#recovery-notes-compliance-checker

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "docs/recovery/recovery_protocol.yaml"
REGISTRY_PATH = ROOT / "docs/recovery/recovery_registry.yaml"
BASELINE_PATH = ROOT / "docs/recovery/recovery_compliance_baseline.json"
JSON_REPORT = ROOT / "runtime/compliance/recovery_notes_compliance.json"
MD_REPORT = ROOT / "runtime/compliance/recovery_notes_compliance.md"

ENTRY_REQUIRED_FIELDS = {
    "id",
    "file",
    "purpose",
    "owns",
    "does_not_own",
    "inputs",
    "outputs",
    "dependencies",
    "used_by",
    "status",
    "last_updated",
    "recovery_notes",
}

PHASES = {
    "phase_1_report_only",
    "phase_2_touched_file_enforcement",
    "phase_3_new_file_full_enforcement",
    "phase_4_repo_baseline_ratchet",
    "phase_5_full_repo_enforcement",
}

REGISTRY_PTR = re.compile(r"@registry\s+docs/recovery/recovery_registry\.yaml#([a-z0-9-]+)")
SUMMARY_PTR = re.compile(r"@summary\s+(.+)")


@dataclass
class FileResult:
    path: str
    in_scope: bool
    level: str
    registry_id: str | None
    issues: list[str]


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_registry() -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    data = load_yaml(REGISTRY_PATH)
    entries = data.get("files", [])
    if not isinstance(entries, list):
        return [], ["Registry must contain top-level 'files' list"]

    ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Registry entry must be an object")
            continue
        missing = sorted(ENTRY_REQUIRED_FIELDS - set(entry.keys()))
        if missing:
            errors.append(f"Entry '{entry.get('id', '<missing-id>')}' missing: {', '.join(missing)}")
        entry_id = entry.get("id")
        if not entry_id:
            errors.append("Entry missing required 'id'")
        elif entry_id in ids:
            errors.append(f"Duplicate registry id '{entry_id}'")
        else:
            ids.add(entry_id)

    return entries, errors


def load_baseline() -> dict[str, Any]:
    if not BASELINE_PATH.exists():
        return {"compliance_floor_percent": 0.0, "per_file_levels": {}}
    with BASELINE_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def is_excluded(path: Path) -> bool:
    banned_parts = {
        ".git",
        ".venv",
        "vendor",
        "generated",
        "dist",
        "build",
        "cache",
        "node_modules",
        "archives",
        "archive",
        "__pycache__",
    }
    text = str(path).lower()
    if "lock" in path.name.lower():
        return True
    return any(part in banned_parts for part in path.parts) or text.endswith((".pyc", ".min.js"))


def is_in_scope(path: Path) -> bool:
    if is_excluded(path):
        return False
    if path.suffix not in {".py", ".sh", ".js", ".ts"}:
        return False
    if path.as_posix().startswith(("src/", "tools/", "scripts/")):
        return True
    return path.as_posix() in {"main.py"}


def discover_in_scope_files() -> list[str]:
    files: list[str] = []
    for candidate in ROOT.rglob("*"):
        if not candidate.is_file():
            continue
        rel = candidate.relative_to(ROOT)
        if is_in_scope(rel):
            files.append(rel.as_posix())
    return sorted(files)


def extract_header_metadata(file_path: Path) -> tuple[str | None, str | None, bool]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")[:1200]
    ptr_match = REGISTRY_PTR.search(text)
    summary_match = SUMMARY_PTR.search(text)
    summary_ok = bool(summary_match and summary_match.group(1).strip().endswith("."))
    return (ptr_match.group(1) if ptr_match else None, summary_match.group(1).strip() if summary_match else None, summary_ok)


def compliance_for_file(path: str, registry_map: dict[str, dict[str, Any]]) -> FileResult:
    rel = Path(path)
    full = ROOT / rel
    pointer_id, _, summary_ok = extract_header_metadata(full)
    issues: list[str] = []

    if not pointer_id:
        return FileResult(path, True, "level_0_untracked", None, ["missing @registry header pointer"])
    if not summary_ok:
        issues.append("invalid or non-sentence @summary")

    entry = registry_map.get(pointer_id)
    if not entry:
        issues.append(f"header pointer '{pointer_id}' not found in registry")
        return FileResult(path, True, "level_1_pointer_only", pointer_id, issues)

    missing = sorted(ENTRY_REQUIRED_FIELDS - set(entry.keys()))
    if missing:
        issues.append(f"registry entry '{pointer_id}' incomplete: {', '.join(missing)}")
        return FileResult(path, True, "level_2_partial_registry", pointer_id, issues)

    if entry.get("file") != path:
        issues.append(f"registry file mismatch: entry has '{entry.get('file')}'")
        return FileResult(path, True, "level_2_partial_registry", pointer_id, issues)

    return FileResult(path, True, "level_3_compliant", pointer_id, issues)


def git_changed_files(base_ref: str | None, head_ref: str | None) -> tuple[list[str], list[str]]:
    if not base_ref:
        return [], []
    head = head_ref or "HEAD"
    cmd = ["git", "diff", "--name-status", f"{base_ref}..{head}"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=False)
    touched: list[str] = []
    added: list[str] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, file_path = parts[0], parts[-1]
        if not Path(ROOT / file_path).exists():
            continue
        touched.append(file_path)
        if status.strip() == "A":
            added.append(file_path)
    return touched, added


def calculate_metrics(results: list[FileResult]) -> dict[str, Any]:
    total = len(results)
    counts = {
        "level_0_untracked": 0,
        "level_1_pointer_only": 0,
        "level_2_partial_registry": 0,
        "level_3_compliant": 0,
    }
    for item in results:
        counts[item.level] += 1
    compliant = counts["level_3_compliant"]
    percent = round((compliant / total) * 100, 2) if total else 100.0
    return {
        "total_in_scope_files": total,
        "compliant_files": compliant,
        "partial_files": counts["level_2_partial_registry"],
        "pointer_only_files": counts["level_1_pointer_only"],
        "untracked_files": counts["level_0_untracked"],
        "compliance_percent": percent,
        "counts": counts,
    }


def evaluate_phase_failures(
    phase: str,
    results_map: dict[str, FileResult],
    touched_files: list[str],
    new_files: list[str],
    baseline: dict[str, Any],
    metrics: dict[str, Any],
    registry_errors: list[str],
) -> list[str]:
    failures: list[str] = []
    if phase == "phase_1_report_only":
        if registry_errors:
            failures.extend(registry_errors)
        return failures

    scoped_touched = [f for f in touched_files if f in results_map]
    scoped_new = [f for f in new_files if f in results_map]

    if phase in {"phase_2_touched_file_enforcement", "phase_3_new_file_full_enforcement", "phase_4_repo_baseline_ratchet", "phase_5_full_repo_enforcement"}:
        for file_path in scoped_touched:
            result = results_map[file_path]
            if result.level == "level_0_untracked":
                failures.append(f"Touched file lacks valid header pointer: {file_path}")
            if result.level in {"level_1_pointer_only", "level_2_partial_registry"}:
                failures.append(f"Touched file is not compliant: {file_path}")

    if phase in {"phase_3_new_file_full_enforcement", "phase_4_repo_baseline_ratchet", "phase_5_full_repo_enforcement"}:
        for file_path in scoped_new:
            if results_map[file_path].level != "level_3_compliant":
                failures.append(f"New in-scope file is not fully compliant: {file_path}")

    if phase in {"phase_4_repo_baseline_ratchet", "phase_5_full_repo_enforcement"}:
        floor = float(baseline.get("compliance_floor_percent", 0.0))
        if metrics["compliance_percent"] < floor:
            failures.append(
                f"Compliance percent {metrics['compliance_percent']} below baseline floor {floor}"
            )

    if phase == "phase_5_full_repo_enforcement" and metrics["compliant_files"] != metrics["total_in_scope_files"]:
        failures.append("Phase 5 requires 100% in-scope files at level_3_compliant")

    return failures


def write_reports(report: dict[str, Any]) -> None:
    JSON_REPORT.parent.mkdir(parents=True, exist_ok=True)
    JSON_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Recovery Notes Compliance Report",
        "",
        f"- Phase: `{report['phase']}`",
        f"- Compliance: **{report['metrics']['compliance_percent']}%**",
        f"- Total in-scope files: {report['metrics']['total_in_scope_files']}",
        f"- Compliant files: {report['metrics']['compliant_files']}",
        f"- Pointer-only files: {report['metrics']['pointer_only_files']}",
        f"- Partial-registry files: {report['metrics']['partial_files']}",
        f"- Untracked files: {report['metrics']['untracked_files']}",
        "",
        "## Failures",
    ]
    if report["failures"]:
        lines.extend([f"- ❌ {f}" for f in report["failures"]])
    else:
        lines.append("- ✅ No enforcement failures")

    lines.extend(["", "## File Levels"])
    for row in report["files"]:
        issue_text = "; ".join(row["issues"]) if row["issues"] else "none"
        lines.append(f"- `{row['path']}`: {row['level']} (issues: {issue_text})")

    MD_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recovery notes compliance checker")
    parser.add_argument("--phase", default="phase_1_report_only", choices=sorted(PHASES))
    parser.add_argument("--base-ref", default=None)
    parser.add_argument("--head-ref", default="HEAD")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        _ = load_yaml(PROTOCOL_PATH)
    except Exception as exc:
        print(f"❌ Failed to read protocol: {exc}")
        return 1

    entries, registry_errors = load_registry()
    registry_map = {e.get("id"): e for e in entries if isinstance(e, dict) and e.get("id")}

    files = discover_in_scope_files()
    results = [compliance_for_file(path, registry_map) for path in files]
    results_map = {r.path: r for r in results}

    touched_files, new_files = git_changed_files(args.base_ref, args.head_ref)
    baseline = load_baseline()
    metrics = calculate_metrics(results)

    failures = evaluate_phase_failures(
        args.phase,
        results_map,
        touched_files,
        new_files,
        baseline,
        metrics,
        registry_errors,
    )

    report = {
        "phase": args.phase,
        "protocol_file": str(PROTOCOL_PATH.relative_to(ROOT)),
        "registry_file": str(REGISTRY_PATH.relative_to(ROOT)),
        "baseline_file": str(BASELINE_PATH.relative_to(ROOT)),
        "touched_files": touched_files,
        "new_files": new_files,
        "registry_errors": registry_errors,
        "metrics": metrics,
        "files": [
            {
                "path": r.path,
                "level": r.level,
                "registry_id": r.registry_id,
                "issues": r.issues,
            }
            for r in results
        ],
        "failures": failures,
    }
    write_reports(report)

    if failures:
        print("❌ Recovery notes compliance failed")
        for fail in failures:
            print(f"  - {fail}")
        return 1

    print("✅ Recovery notes compliance passed")
    print(f"Report: {JSON_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
