#!/usr/bin/env python3
"""Audit Harness - Reproducible Codebase Audit Tool (SSOT CLI entrypoint)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.audit_harness_archive import analyze_archive
from tools.audit_harness_dead_code import find_dead_code
from tools.audit_harness_duplication import analyze_duplication
from tools.audit_harness_imports import analyze_imports
from tools.audit_harness_inventory import inventory_files
from tools.audit_harness_report import generate_report


class AuditHarness:
    """Reproducible codebase audit harness (SSOT)."""

    def __init__(self) -> None:
        self.project_root = Path(__file__).parent.parent
        self.timestamp = datetime.now().isoformat()

    def inventory_files(self, roots: List[str], output_file: str) -> Dict[str, Any]:
        return inventory_files(self.project_root, self.timestamp, roots, output_file)

    def analyze_duplication(self, roots: List[str], output_file: str) -> Dict[str, Any]:
        return analyze_duplication(self.project_root, self.timestamp, roots, output_file)

    def find_dead_code(self, root: str, output_file: str) -> Dict[str, Any]:
        return find_dead_code(self.project_root, self.timestamp, root, output_file)

    def analyze_imports(self, root: str, output_file: str) -> Dict[str, Any]:
        return analyze_imports(self.project_root, self.timestamp, root, output_file)

    def analyze_archive(self, root: str, output_file: str) -> Dict[str, Any]:
        return analyze_archive(self.project_root, self.timestamp, root, output_file)

    def generate_report(self, inputs_dir: str, output_file: str) -> str:
        return generate_report(inputs_dir, output_file)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Audit Harness - Reproducible Codebase Audit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    inventory_parser = subparsers.add_parser("inventory", help="Generate file inventory")
    inventory_parser.add_argument("--roots", nargs="+", required=True, help="Directory roots to inventory")
    inventory_parser.add_argument("--out", required=True, help="Output JSON file")

    dup_parser = subparsers.add_parser("dup", help="Analyze code duplication")
    dup_parser.add_argument("--roots", nargs="+", required=True, help="Directory roots to analyze")
    dup_parser.add_argument(
        "--out",
        default="audit_outputs/duplication_report.json",
        help="Output JSON file (default: audit_outputs/duplication_report.json)",
    )

    dead_parser = subparsers.add_parser("dead", help="Find dead code candidates")
    dead_parser.add_argument("--root", required=True, help="Directory root to analyze")
    dead_parser.add_argument("--out", required=True, help="Output text file")

    imports_parser = subparsers.add_parser("imports", help="Analyze import relationships")
    imports_parser.add_argument("--root", required=True, help="Directory root to analyze")
    imports_parser.add_argument("--out", required=True, help="Output text file")

    archive_parser = subparsers.add_parser("archive", help="Analyze archive contents")
    archive_parser.add_argument("--root", required=True, help="Archive directory root")
    archive_parser.add_argument("--out", required=True, help="Output CSV file")

    report_parser = subparsers.add_parser("report", help="Generate Captain-ready report")
    report_parser.add_argument("--inputs", required=True, help="Directory with audit outputs")
    report_parser.add_argument("--out", required=True, help="Report output file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    harness = AuditHarness()

    try:
        if args.command == "inventory":
            harness.inventory_files(args.roots, args.out)
        elif args.command == "dup":
            harness.analyze_duplication(args.roots, args.out)
        elif args.command == "dead":
            harness.find_dead_code(args.root, args.out)
        elif args.command == "imports":
            harness.analyze_imports(args.root, args.out)
        elif args.command == "archive":
            harness.analyze_archive(args.root, args.out)
        elif args.command == "report":
            harness.generate_report(args.inputs, args.out)
        else:
            parser.print_help()

    except Exception as exc:
        print(f"❌ Audit failed: {exc}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
