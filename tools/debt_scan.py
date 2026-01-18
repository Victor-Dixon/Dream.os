"""
SSOT Technical Debt Scanner.

Scans repository content for duplicate files, syntax errors, and basic SSOT
signals. Configuration is sourced from config/debt_scan.yaml (SSOT).
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

CONFIG_PATH = Path("config/debt_scan.yaml")
REPORTS_DIR = Path("reports")
REPORT_JSON = REPORTS_DIR / "debt_scan.json"
REPORT_MD = REPORTS_DIR / "debt_scan.md"

LIST_KEYS = {"scan_dirs", "exclude_dirs", "exclude_files", "check_extensions", "ssot_doc_allowlist"}
DICT_KEYS = {"fail_if", "reporting", "performance"}


@dataclass
class ScanConfig:
    scan_dirs: List[str]
    exclude_dirs: List[str]
    exclude_files: List[str]
    check_extensions: List[str]
    ssot_doc_allowlist: List[str]
    fail_if: Dict[str, int]
    reporting: Dict[str, object]
    performance: Dict[str, object]


@dataclass
class DuplicateGroup:
    hash_value: str
    files: List[str]
    size_bytes: int
    extension: str


@dataclass
class ScanResults:
    total_files: int
    total_lines: int
    largest_file_kb: float
    avg_file_size_kb: float
    duplicate_groups: List[DuplicateGroup]
    syntax_errors: List[Dict[str, str]]
    ssot_violations: List[Dict[str, str]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SSOT technical debt scan")
    parser.add_argument("--ci", action="store_true", help="Enable CI thresholds")
    parser.add_argument(
        "--baseline",
        type=str,
        default=None,
        help="Baseline JSON path for duplicate comparison",
    )
    return parser.parse_args()


def parse_scalar(value: str):
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    return value.strip('"').strip("'")


def parse_simple_yaml(text: str) -> Dict[str, object]:
    config: Dict[str, object] = {}
    current_key: Optional[str] = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0 and line.endswith(":"):
            key = line[:-1].strip()
            current_key = key
            if key in LIST_KEYS:
                config[key] = []
            elif key in DICT_KEYS:
                config[key] = {}
            else:
                config[key] = {}
            continue
        if current_key is None:
            continue
        if line.lstrip().startswith("- "):
            item = line.lstrip()[2:].strip()
            if isinstance(config.get(current_key), list):
                config[current_key].append(item.strip('"').strip("'"))
            continue
        if ":" in line:
            key, value = line.lstrip().split(":", 1)
            value = value.strip()
            if isinstance(config.get(current_key), dict):
                config[current_key][key.strip()] = parse_scalar(value)
    return config


def load_config(path: Path) -> ScanConfig:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    content = path.read_text(encoding="utf-8")
    yaml_spec = importlib.util.find_spec("yaml")
    if yaml_spec:
        yaml = importlib.import_module("yaml")
        raw = yaml.safe_load(content)
    else:
        raw = parse_simple_yaml(content)
    for key in LIST_KEYS:
        raw.setdefault(key, [])
    for key in DICT_KEYS:
        raw.setdefault(key, {})
    return ScanConfig(
        scan_dirs=list(raw.get("scan_dirs", [])),
        exclude_dirs=list(raw.get("exclude_dirs", [])),
        exclude_files=list(raw.get("exclude_files", [])),
        check_extensions=list(raw.get("check_extensions", [])),
        ssot_doc_allowlist=list(raw.get("ssot_doc_allowlist", [])),
        fail_if={k: int(v) for k, v in raw.get("fail_if", {}).items()},
        reporting=dict(raw.get("reporting", {})),
        performance=dict(raw.get("performance", {})),
    )


def iter_files(scan_dirs: List[str], exclude_dirs: List[str]) -> Iterable[Path]:
    for scan_dir in scan_dirs:
        base = Path(scan_dir)
        if not base.exists():
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for name in files:
                yield Path(root) / name


def is_excluded_file(path: Path, exclude_files: List[str]) -> bool:
    path_str = path.as_posix()
    return any(path_str == entry for entry in exclude_files)


def is_allowed_doc(path: Path, allowlist: List[str]) -> bool:
    path_str = path.as_posix()
    return any(path_str.startswith(entry.rstrip("/")) for entry in allowlist)


def check_python_syntax(path: Path) -> Optional[str]:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        return f"read_error: {exc}"
    try:
        ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return f"{exc.msg} (line {exc.lineno})"
    return None


def hash_file(path: Path, buffer_size: int) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(buffer_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_repo(config: ScanConfig) -> ScanResults:
    max_file_size_mb = float(config.performance.get("max_file_size_mb", 100))
    hash_buffer_size = int(config.performance.get("hash_buffer_size", 8192))
    duplicate_map: Dict[str, List[Path]] = {}
    total_files = 0
    total_lines = 0
    largest_bytes = 0
    total_bytes = 0
    syntax_errors: List[Dict[str, str]] = []
    ssot_violations: List[Dict[str, str]] = []

    for path in iter_files(config.scan_dirs, config.exclude_dirs):
        if is_excluded_file(path, config.exclude_files):
            continue
        total_files += 1
        try:
            size_bytes = path.stat().st_size
        except OSError:
            continue
        total_bytes += size_bytes
        largest_bytes = max(largest_bytes, size_bytes)
        if size_bytes > max_file_size_mb * 1024 * 1024:
            continue

        if path.suffix in config.check_extensions:
            file_hash = hash_file(path, hash_buffer_size)
            duplicate_map.setdefault(file_hash, []).append(path)

        if path.suffix == ".py":
            error = check_python_syntax(path)
            if error:
                syntax_errors.append({"file": path.as_posix(), "error": error})

        if path.suffix in {".md", ".txt"} and not is_allowed_doc(
            path, config.ssot_doc_allowlist
        ):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if "SSOT" in text and "deprecated" in text:
                ssot_violations.append(
                    {
                        "file": path.as_posix(),
                        "detail": "Document mentions SSOT and deprecated together",
                    }
                )

        if path.suffix in {".py", ".md", ".txt"}:
            try:
                total_lines += sum(1 for _ in path.open("r", encoding="utf-8"))
            except OSError:
                continue

    duplicate_groups: List[DuplicateGroup] = []
    for hash_value, paths in duplicate_map.items():
        if len(paths) <= 1:
            continue
        first = paths[0]
        extension = first.suffix
        try:
            size_bytes = first.stat().st_size
        except OSError:
            size_bytes = 0
        duplicate_groups.append(
            DuplicateGroup(
                hash_value=hash_value,
                files=[p.as_posix() for p in sorted(paths)],
                size_bytes=size_bytes,
                extension=extension,
            )
        )

    avg_file_size_kb = (total_bytes / 1024 / total_files) if total_files else 0
    return ScanResults(
        total_files=total_files,
        total_lines=total_lines,
        largest_file_kb=largest_bytes / 1024,
        avg_file_size_kb=avg_file_size_kb,
        duplicate_groups=duplicate_groups,
        syntax_errors=syntax_errors,
        ssot_violations=ssot_violations,
    )


def load_baseline(path: Optional[str]) -> Dict[str, object]:
    if not path:
        return {}
    baseline_path = Path(path)
    if not baseline_path.exists():
        return {}
    return json.loads(baseline_path.read_text(encoding="utf-8"))


def build_report(config: ScanConfig, results: ScanResults, baseline: Dict[str, object]):
    duplicate_hashes = sorted({group.hash_value for group in results.duplicate_groups})
    baseline_hashes = set(baseline.get("duplicate_hashes", []))
    new_duplicate_hashes = sorted([h for h in duplicate_hashes if h not in baseline_hashes])
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "config": {
            "scan_dirs": config.scan_dirs,
            "exclude_dirs": config.exclude_dirs,
            "exclude_files": config.exclude_files,
            "check_extensions": config.check_extensions,
            "ssot_doc_allowlist": config.ssot_doc_allowlist,
            "max_syntax_errors": config.fail_if.get("syntax_errors", 0),
            "max_new_duplicate_groups": config.fail_if.get("new_duplicate_groups", 0),
            "max_ssot_violations": config.fail_if.get("ssot_violations", 0),
        },
        "total_files": results.total_files,
        "total_lines": results.total_lines,
        "largest_file_kb": round(results.largest_file_kb, 2),
        "avg_file_size_kb": round(results.avg_file_size_kb, 2),
        "duplicate_groups": [
            {
                "hash_value": group.hash_value,
                "files": group.files,
                "size_bytes": group.size_bytes,
                "extension": group.extension,
            }
            for group in results.duplicate_groups
        ],
        "new_duplicate_groups": new_duplicate_hashes,
        "syntax_errors": results.syntax_errors,
        "ssot_violations": results.ssot_violations,
    }
    return report


def write_reports(report: Dict[str, object]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_lines = [
        "# Technical Debt Scan",
        "",
        f"Timestamp: {report['timestamp']}",
        "",
        f"Total files: {report['total_files']}",
        f"Total lines: {report['total_lines']}",
        f"Largest file (KB): {report['largest_file_kb']}",
        f"Average file size (KB): {report['avg_file_size_kb']}",
        "",
        f"Duplicate groups: {len(report['duplicate_groups'])}",
        f"New duplicate groups: {len(report['new_duplicate_groups'])}",
        f"Syntax errors: {len(report['syntax_errors'])}",
        f"SSOT violations: {len(report['ssot_violations'])}",
    ]
    REPORT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def evaluate_ci(config: ScanConfig, report: Dict[str, object]) -> Tuple[bool, List[str]]:
    failures = []
    max_syntax = config.fail_if.get("syntax_errors", 0)
    max_new_dupes = config.fail_if.get("new_duplicate_groups", 0)
    max_ssot = config.fail_if.get("ssot_violations", 0)

    if len(report.get("syntax_errors", [])) > max_syntax:
        failures.append("syntax_errors")
    if len(report.get("new_duplicate_groups", [])) > max_new_dupes:
        failures.append("new_duplicate_groups")
    if len(report.get("ssot_violations", [])) > max_ssot:
        failures.append("ssot_violations")

    return not failures, failures


def main() -> int:
    args = parse_args()
    config = load_config(CONFIG_PATH)
    baseline = load_baseline(args.baseline)
    results = scan_repo(config)
    report = build_report(config, results, baseline)
    write_reports(report)

    if args.ci:
        ok, failures = evaluate_ci(config, report)
        if not ok:
            print(f"CI thresholds exceeded: {', '.join(failures)}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
