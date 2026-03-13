#!/usr/bin/env python3
"""Source File Header Compliance Protocol v1.3.0 validator."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

RULES = {
    "HDR001": "missing-header",
    "HDR002": "missing-required-field",
    "HDR003": "invalid-placeholder-value",
    "HDR004": "invalid-pre-header-order",
    "HDR005": "unsupported-comment-style",
    "HDR006": "invalid-utility-variant",
    "HDR007": "exception-config-invalid",
    "HDRW001": "file-out-of-scope-type",
}

LANGUAGE_DIRECTIVE_RE = re.compile(r"^(['\"])use\s+\w+\1;?$")
ENCODING_RE = re.compile(r"^#.*coding[:=]\s*([\w.-]+)")
HEADER_FIELD_RE = re.compile(r"^([A-Za-z-]+):\s*(.+)$")


@dataclass
class Violation:
    path: str
    rule_id: str
    message: str


@dataclass
class ExceptionRecord:
    path: str
    owner: str
    expires_on: dt.date
    suppressed_checks: set[str]


class HeaderValidator:
    def __init__(self, root: Path, protocol_path: Path, mode: str, changed_only: bool) -> None:
        self.root = root
        self.protocol = yaml.safe_load(protocol_path.read_text(encoding="utf-8"))
        self.mode = mode
        self.changed_only = changed_only
        self.violations: list[Violation] = []
        self.warnings: list[Violation] = []
        self.utility_files: list[str] = []
        self.exception_usage: dict[str, list[str]] = {}
        self.expired_exceptions: list[str] = []

    def normalized_path(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def in_scope(self, rel_path: str) -> bool:
        included = any(fnmatch.fnmatch(rel_path, g) for g in self.protocol["scope_globs"])
        excluded = any(fnmatch.fnmatch(rel_path, g) for g in self.protocol.get("exclude_globs", []))
        return included and not excluded

    def load_exceptions(self) -> dict[str, ExceptionRecord]:
        cfg = self.root / self.protocol["exceptions"]["file"]
        if not cfg.exists():
            return {}
        raw = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
        allowed = set(self.protocol["exceptions"]["valid_suppressed_checks"])
        today = dt.date.today()
        result: dict[str, ExceptionRecord] = {}
        for item in raw.get("exceptions", []):
            path = item.get("path", "")
            checks = set(item.get("suppressed_checks", []))
            invalid = sorted(checks - allowed)
            if invalid:
                self.violations.append(Violation(path, "HDR007", f"invalid suppressed_checks: {invalid}"))
                continue
            raw_expiry = item["expires_on"]
            expires_on = raw_expiry if isinstance(raw_expiry, dt.date) else dt.date.fromisoformat(str(raw_expiry))
            if expires_on < today:
                self.expired_exceptions.append(path)
                self.violations.append(Violation(path, "HDR007", "exception expired"))
            result[path] = ExceptionRecord(
                path=path,
                owner=item.get("owner", "unknown"),
                expires_on=expires_on,
                suppressed_checks=checks,
            )
        return result

    def changed_paths(self) -> set[str]:
        env = os.environ
        base = env.get("GITHUB_BASE_REF")
        if base:
            target = f"origin/{base}"
            cmd = ["git", "diff", "--name-status", f"{target}...HEAD"]
        else:
            cmd = ["git", "diff", "--name-status", "HEAD~1...HEAD"]
        proc = subprocess.run(cmd, cwd=self.root, check=False, capture_output=True, text=True)
        changed: set[str] = set()
        for line in proc.stdout.splitlines():
            cols = line.split("\t")
            if not cols:
                continue
            status = cols[0]
            if status.startswith("R") and len(cols) >= 3:
                changed.add(cols[2])
            elif len(cols) >= 2 and status in {"A", "M"}:
                changed.add(cols[1])
        return {p.replace("\\", "/") for p in changed}

    def parse_prefix(self, lines: list[str], suffix: str) -> tuple[int, dict[str, Any]]:
        idx = 0
        meta: dict[str, Any] = {"shebang": False, "encoding": False, "directive": False, "license": False}
        if suffix == ".py" and idx < len(lines) and lines[idx].startswith("#!"):
            meta["shebang"] = True
            idx += 1
        if suffix == ".py" and idx < len(lines) and ENCODING_RE.match(lines[idx]):
            meta["encoding"] = True
            idx += 1
        if suffix in {".js", ".ts"} and idx < len(lines) and LANGUAGE_DIRECTIVE_RE.match(lines[idx].strip()):
            meta["directive"] = True
            idx += 1
        start = idx
        keywords = self.protocol["license_detection"]["required_keywords"]
        min_lines = self.protocol["license_detection"]["min_lines"]
        while idx < len(lines):
            stripped = lines[idx].strip().lower()
            if not stripped.startswith(("#", "//", "/*", "*", "*/")):
                break
            if not any(k in stripped for k in keywords) and stripped not in {"/*", "*/", "*"}:
                break
            idx += 1
        if (idx - start) >= min_lines:
            meta["license"] = True
        else:
            idx = start
        return idx, meta

    def extract_header(self, lines: list[str], start: int, suffix: str) -> tuple[dict[str, str], int]:
        fields: dict[str, str] = {}
        idx = start
        while idx < len(lines):
            raw = lines[idx].strip()
            if not raw:
                idx += 1
                continue
            token = raw
            if suffix == ".py" and token.startswith("#"):
                token = token[1:].strip()
            elif suffix in {".js", ".ts"}:
                token = token.removeprefix("//").strip().strip("/*").strip("*/").strip("*").strip()
            else:
                break
            m = HEADER_FIELD_RE.match(token)
            if not m:
                break
            fields[m.group(1)] = m.group(2)
            idx += 1
        return fields, idx

    def validate_file(self, file_path: Path, exceptions: dict[str, ExceptionRecord]) -> None:
        rel = self.normalized_path(file_path)
        suffix = file_path.suffix
        spec = self.protocol["supported_file_types"].get(suffix)
        if not spec:
            self.warnings.append(Violation(rel, "HDRW001", "supported extension required"))
            return

        lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        start, meta = self.parse_prefix(lines, suffix)
        next_line = lines[start].strip() if start < len(lines) else ""
        if next_line and next_line.startswith(("#", "//", "/*")) and not next_line.startswith((spec["line_prefix"], "/*")):
            self.violations.append(Violation(rel, "HDR005", "comment style mismatch for file type"))
        if next_line and not next_line.startswith((spec["line_prefix"], "/*")):
            self.violations.append(Violation(rel, "HDR004", "header does not follow parser order"))
        fields, _ = self.extract_header(lines, start, suffix)
        if not fields:
            self.violations.append(Violation(rel, "HDR001", "missing header block"))
            return

        variant = fields.get("Header-Variant", "full")
        req_fields = self.protocol["required_header_fields"].get(variant)
        if not req_fields:
            self.violations.append(Violation(rel, "HDR006", f"unknown header variant: {variant}"))
            return
        if variant == "utility":
            self.utility_files.append(rel)
            non_comment = [ln for ln in lines if ln.strip() and not ln.strip().startswith(("#", "//", "/*", "*", "*/"))]
            max_lines = self.protocol["utility_constraints"]["max_non_comment_non_blank_lines"]
            if len(non_comment) > max_lines:
                self.violations.append(Violation(rel, "HDR006", f"utility variant exceeds {max_lines} lines"))

        missing = [f for f in req_fields if f not in fields]
        for f in missing:
            self.violations.append(Violation(rel, "HDR002", f"missing field: {f}"))
        blocked = set(self.protocol["placeholder_blocklist"])
        for key, value in fields.items():
            if value.strip().upper() in blocked:
                self.violations.append(Violation(rel, "HDR003", f"placeholder value for {key}"))

        exc = exceptions.get(rel)
        if exc:
            self.exception_usage.setdefault(exc.owner, []).append(rel)
            self.violations = [v for v in self.violations if not (v.path == rel and v.rule_id in exc.suppressed_checks)]

    def inventory(self) -> list[str]:
        files: list[str] = []
        for path in self.root.rglob("*"):
            if path.is_file():
                rel = self.normalized_path(path)
                if self.in_scope(rel):
                    files.append(rel)
        return sorted(files)

    def run(self) -> dict[str, Any]:
        exceptions = self.load_exceptions()
        changed = self.changed_paths() if self.changed_only else None
        for rel in self.inventory():
            if changed is not None and rel not in changed:
                continue
            self.validate_file(self.root / rel, exceptions)
        return {
            "mode": self.mode,
            "violations": [v.__dict__ for v in self.violations],
            "warnings": [w.__dict__ for w in self.warnings],
            "metrics": {
                "violation_count": len(self.violations),
                "warning_count": len(self.warnings),
                "utility_variant_files": self.utility_files,
                "exception_usage_by_owner": self.exception_usage,
                "expired_exceptions": self.expired_exceptions,
            },
        }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        f"# File Header Compliance Report ({report['mode']})",
        "",
        f"- Violations: {report['metrics']['violation_count']}",
        f"- Warnings: {report['metrics']['warning_count']}",
        "",
        "## Utility Variant Usage",
    ]
    utility = report["metrics"]["utility_variant_files"]
    lines.extend([f"- {p}" for p in utility] or ["- none"])
    lines.extend(["", "## Active Exceptions by Owner"])
    exc = report["metrics"]["exception_usage_by_owner"]
    if exc:
        for owner, paths in sorted(exc.items()):
            lines.append(f"- {owner}: {', '.join(sorted(paths))}")
    else:
        lines.append("- none")
    lines.extend(["", "## Expired Exceptions"])
    expired = report["metrics"]["expired_exceptions"]
    lines.extend([f"- {p}" for p in expired] or ["- none"])
    lines.extend(["", "## Warnings by Rule ID"])
    counts: dict[str, int] = {}
    for warning in report["warnings"]:
        counts[warning["rule_id"]] = counts.get(warning["rule_id"], 0) + 1
    lines.extend([f"- {k}: {v}" for k, v in sorted(counts.items())] or ["- none"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_baseline(root: Path, protocol: dict[str, Any], output: Path) -> None:
    validator = HeaderValidator(root, root / "config/file_header_protocol_v1.3.0.yaml", "audit_only", False)
    inventory = [p for p in validator.inventory() if Path(p).suffix in protocol["supported_file_types"]]
    baseline = {"version": protocol["version"], "generated_at": dt.datetime.utcnow().isoformat(), "files": inventory}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "baseline"])
    parser.add_argument("--mode", default="audit_only", choices=["audit_only", "touched_file_enforcement"])
    parser.add_argument("--protocol", default="config/file_header_protocol_v1.3.0.yaml")
    args = parser.parse_args()

    root = Path.cwd()
    protocol_path = root / args.protocol
    protocol = yaml.safe_load(protocol_path.read_text(encoding="utf-8"))

    if args.command == "baseline":
        generate_baseline(root, protocol, root / protocol["baseline"]["file"])
        print("baseline generated")
        return 0

    changed_only = args.mode == "touched_file_enforcement"
    validator = HeaderValidator(root, protocol_path, args.mode, changed_only)
    report = validator.run()
    json_path = root / protocol["reports"]["json"]
    md_path = root / protocol["reports"]["markdown"]
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(md_path, report)

    print(json.dumps(report["metrics"], indent=2))
    if args.mode == "audit_only":
        return 0
    return 1 if report["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
