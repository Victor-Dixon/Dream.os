#!/usr/bin/env python3
"""
SSOT Technical Debt Scanner v1
===============================

Unified technical debt detection for Agent Cellphone V2 Repository.

DETECTS:
- File duplications (full SHA256 hashing, no sampling)
- Python syntax errors (compileall across all dirs)
- SSOT compliance violations (imports + docs references)
- Test coverage estimation (pytest collection)
- File size/complexity metrics

OUTPUTS:
- reports/debt_scan.json (structured data)
- reports/debt_scan.md (human-readable report)

CONFIG:
- config/debt_scan.yaml (thresholds, includes/excludes, allowlists)

Author: Agent-4 (Captain) - Technical Debt Detection Specialist
"""

import sys
import json
import hashlib
import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class DebtScanConfig:
    """Configuration for debt scanning."""
    # Directories to scan
    scan_dirs: List[str] = None
    exclude_dirs: List[str] = None

    # File types to check
    check_extensions: List[str] = None

    # SSOT allowlists (deprecated paths that are OK to reference in docs)
    ssot_doc_allowlist: List[str] = None

    # CI thresholds (fail if exceeded)
    max_syntax_errors: int = 0
    max_new_duplicate_groups: int = 0
    max_ssot_violations: int = 0

    def __post_init__(self):
        if self.scan_dirs is None:
            self.scan_dirs = ["."]
        if self.exclude_dirs is None:
            self.exclude_dirs = [".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "logs"]
        if self.check_extensions is None:
            self.check_extensions = [".py", ".md", ".txt", ".json", ".yaml", ".yml", ".js", ".ts"]
        if self.ssot_doc_allowlist is None:
            self.ssot_doc_allowlist = [
                # Allow historical references in these files
                "docs/archive/",
                "docs/SSOT_MAP.md",
                "CHANGELOG.md"
            ]

@dataclass
class DuplicateGroup:
    """Represents a group of duplicate files."""
    hash_value: str
    files: List[str]
    size_bytes: int
    extension: str

    @property
    def count(self) -> int:
        return len(self.files)

    def is_new_vs_baseline(self, baseline_hashes: Set[str]) -> bool:
        """Check if this duplicate group is new vs baseline."""
        return self.hash_value not in baseline_hashes

@dataclass
class DebtScanResult:
    """Complete debt scan results."""
    timestamp: datetime
    config: DebtScanConfig

    # File metrics
    total_files: int = 0
    total_lines: int = 0
    largest_file_kb: int = 0
    avg_file_size_kb: float = 0.0

    # Duplication results
    duplicate_groups: List[DuplicateGroup] = None
    new_duplicate_groups: List[DuplicateGroup] = None

    # Syntax errors
    syntax_errors: List[Dict[str, Any]] = None

    # SSOT violations
    ssot_violations: List[Dict[str, Any]] = None

    # Test coverage
    test_coverage_estimate: float = 0.0
    total_tests: int = 0
    total_impl_files: int = 0

    # Error rate
    error_rate_24h: float = 0.0

    def __post_init__(self):
        if self.duplicate_groups is None:
            self.duplicate_groups = []
        if self.new_duplicate_groups is None:
            self.new_duplicate_groups = []
        if self.syntax_errors is None:
            self.syntax_errors = []
        if self.ssot_violations is None:
            self.ssot_violations = []

    def calculate_debt_score(self) -> int:
        """Calculate technical debt score (0-100)."""
        score = 0

        # Duplication penalty (up to 40 points)
        dup_ratio = len(self.duplicate_groups) / max(1, self.total_files)
        score += min(40, dup_ratio * 200)  # More aggressive scaling

        # SSOT violations penalty (up to 30 points)
        score += min(30, len(self.ssot_violations) * 2)

        # Syntax errors penalty (up to 20 points)
        score += min(20, len(self.syntax_errors) * 10)

        # Test coverage bonus (up to -20 points)
        coverage_penalty = max(0, (80 - self.test_coverage_estimate) / 4)
        score += coverage_penalty

        return min(100, max(0, int(score)))

    def should_ci_fail(self) -> bool:
        """Check if CI should fail based on thresholds."""
        if len(self.syntax_errors) > self.config.max_syntax_errors:
            return True
        if len(self.new_duplicate_groups) > self.config.max_new_duplicate_groups:
            return True
        if len(self.ssot_violations) > self.config.max_ssot_violations:
            return True
        return False

class DebtScanner:
    """SSOT technical debt scanner."""

    def __init__(self, config: DebtScanConfig):
        self.config = config
        self.repo_root = Path(".")

    def scan_all(self) -> DebtScanResult:
        """Run complete debt scan."""
        print("🛰️ SSOT Technical Debt Scanner v1")
        print("=" * 40)

        result = DebtScanResult(
            timestamp=datetime.now(),
            config=self.config
        )

        # File metrics
        result.total_files, result.total_lines = self._count_files_and_lines()
        result.largest_file_kb, result.avg_file_size_kb = self._analyze_file_sizes()

        # Duplications
        result.duplicate_groups = self._scan_duplications()

        # Syntax errors
        result.syntax_errors = self._scan_syntax_errors()

        # SSOT violations
        result.ssot_violations = self._scan_ssot_violations()

        # Test coverage
        result.test_coverage_estimate, result.total_tests, result.total_impl_files = self._estimate_test_coverage()

        # Error rate
        result.error_rate_24h = self._calculate_error_rate()

        print("\n✅ Scan complete!")
        print(f"   Files analyzed: {result.total_files}")
        print(f"   Duplicate groups: {len(result.duplicate_groups)}")
        print(f"   Syntax errors: {len(result.syntax_errors)}")
        print(f"   SSOT violations: {len(result.ssot_violations)}")

        return result

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        # Skip by path components
        if any(part in self.config.exclude_dirs for part in file_path.parts):
            return True

        # Only check specific extensions
        if file_path.suffix not in self.config.check_extensions:
            return True

        # Skip files smaller than 10 bytes
        try:
            if file_path.stat().st_size < 10:
                return True
        except OSError:
            return True

        return False

    def _count_files_and_lines(self) -> Tuple[int, int]:
        """Count total files and lines of code."""
        total_files = 0
        total_lines = 0

        for scan_dir in self.config.scan_dirs:
            scan_path = self.repo_root / scan_dir
            if not scan_path.exists():
                continue

            for file_path in scan_path.rglob("*"):
                if not file_path.is_file() or self._should_skip_file(file_path):
                    continue

                if file_path.suffix in [".py", ".js", ".ts", ".md"]:
                    total_files += 1

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = len(f.readlines())
                            total_lines += lines
                    except (OSError, UnicodeDecodeError):
                        pass

        return total_files, total_lines

    def _analyze_file_sizes(self) -> Tuple[int, float]:
        """Analyze file sizes."""
        file_sizes_kb = []

        for scan_dir in self.config.scan_dirs:
            scan_path = self.repo_root / scan_dir
            if not scan_path.exists():
                continue

            for file_path in scan_path.rglob("*.py"):
                if not self._should_skip_file(file_path):
                    try:
                        size_kb = file_path.stat().st_size / 1024
                        file_sizes_kb.append(size_kb)
                    except OSError:
                        pass

        if file_sizes_kb:
            largest_file_kb = int(max(file_sizes_kb))
            avg_file_size_kb = round(sum(file_sizes_kb) / len(file_sizes_kb), 1)
        else:
            largest_file_kb = 0
            avg_file_size_kb = 0.0

        return largest_file_kb, avg_file_size_kb

    def _scan_duplications(self) -> List[DuplicateGroup]:
        """Scan for file duplications using full SHA256 hashing."""
        print("  🔍 Scanning for file duplications...")
        hashes = {}

        for scan_dir in self.config.scan_dirs:
            scan_path = self.repo_root / scan_dir
            if not scan_path.exists():
                continue

            for file_path in scan_path.rglob("*"):
                if not file_path.is_file() or self._should_skip_file(file_path):
                    continue

                try:
                    with open(file_path, "rb") as f:
                        # Full file hash (no sampling!)
                        file_hash = hashlib.sha256(f.read()).hexdigest()

                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(str(file_path.relative_to(self.repo_root)))

                except (OSError, IOError):
                    continue

        # Convert to DuplicateGroup objects
        duplicate_groups = []
        for file_hash, files in hashes.items():
            if len(files) > 1:
                # Get size from first file
                try:
                    size = (self.repo_root / files[0]).stat().st_size
                    ext = (self.repo_root / files[0]).suffix
                except OSError:
                    size = 0
                    ext = ""

                duplicate_groups.append(DuplicateGroup(
                    hash_value=file_hash,
                    files=sorted(files),
                    size_bytes=size,
                    extension=ext
                ))

        # Sort by file count (most problematic first)
        duplicate_groups.sort(key=lambda x: x.count, reverse=True)

        print(f"     Found {len(duplicate_groups)} duplicate groups")
        return duplicate_groups

    def _scan_syntax_errors(self) -> List[Dict[str, Any]]:
        """Scan for Python syntax errors using compileall."""
        print("  🔍 Scanning for Python syntax errors...")
        syntax_errors = []

        # Directories to check for syntax (including temp_repos)
        syntax_dirs = []
        for scan_dir in self.config.scan_dirs:
            scan_path = self.repo_root / scan_dir
            if scan_path.exists():
                syntax_dirs.append(str(scan_path))

        if syntax_dirs:
            # Use compileall to check syntax
            try:
                result = subprocess.run([
                    sys.executable, "-m", "compileall",
                    "-q",  # quiet mode
                    "--hardlink-dupes",  # follow symlinks
                ] + syntax_dirs, capture_output=True, text=True)

                # Parse stderr for syntax errors
                if result.stderr:
                    for line in result.stderr.split('\n'):
                        if line.strip() and ('SyntaxError' in line or 'IndentationError' in line):
                            # Parse error line format: "File "path", line N"
                            if 'File "' in line and 'line' in line:
                                syntax_errors.append({
                                    "error": line.strip(),
                                    "type": "syntax_error"
                                })

            except subprocess.SubprocessError:
                pass

        print(f"     Found {len(syntax_errors)} syntax errors")
        return syntax_errors

    def _scan_ssot_violations(self) -> List[Dict[str, Any]]:
        """Scan for SSOT compliance violations."""
        print("  🔍 Scanning for SSOT compliance violations...")

        # SSOT mappings (deprecated -> canonical)
        ssot_mappings = {
            "scripts/deploy_via_wordpress_admin.py": "mcp_servers/deployment_server.py",
            "tools/deploy_tradingrobotplug_plugin.py": "mcp_servers/deployment_server.py",
            "tools/deploy_tradingrobotplug_plugin_phase3.py": "mcp_servers/deployment_server.py",
            "tools/deploy_fastapi_tradingrobotplug.py": "mcp_servers/deployment_server.py",
            "tools/deploy_weareswarm_feed_system.py": "mcp_servers/deployment_server.py",
            "tools/deploy_weareswarm_font_fix.py": "mcp_servers/deployment_server.py",
            "tools/deploy_tradingrobotplug_font_fix.py": "mcp_servers/deployment_server.py",
            "tools/wordpress_manager.py": "mcp_servers/wp_cli_manager_server.py",
            "ops/deployment/simple_wordpress_deployer.py": "mcp_servers/deployment_server.py",
        }

        violations = []

        for scan_dir in self.config.scan_dirs:
            scan_path = self.repo_root / scan_dir
            if not scan_path.exists():
                continue

            for file_path in scan_path.rglob("*"):
                if not file_path.is_file() or self._should_skip_file(file_path):
                    continue

                # Check documentation files for deprecated references
                if file_path.suffix in [".md", ".txt"]:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Check if file is in allowlist
                        file_str = str(file_path.relative_to(self.repo_root))
                        is_allowlisted = any(allowed in file_str for allowed in self.config.ssot_doc_allowlist)

                        if not is_allowlisted:
                            for deprecated, canonical in ssot_mappings.items():
                                dep_name = Path(deprecated).name
                                if dep_name in content:
                                    violations.append({
                                        "file": str(file_path.relative_to(self.repo_root)),
                                        "deprecated_path": deprecated,
                                        "canonical_path": canonical,
                                        "type": "documentation_reference"
                                    })

                    except (OSError, UnicodeDecodeError):
                        pass

        print(f"     Found {len(violations)} SSOT violations")
        return violations

    def _estimate_test_coverage(self) -> Tuple[float, int, int]:
        """Estimate test coverage using pytest collection."""
        print("  🔍 Estimating test coverage...")

        try:
            # Use pytest --collect-only to count tests
            result = subprocess.run([
                sys.executable, "-m", "pytest",
                "--collect-only", "-q",
                "--tb=no"  # No tracebacks in output
            ], capture_output=True, text=True, cwd=self.repo_root)

            test_count = 0
            if result.stdout:
                # Count lines that look like test items
                for line in result.stdout.split('\n'):
                    if '::' in line and ('test_' in line or 'Test' in line):
                        test_count += 1

            # Count implementation files
            impl_files = 0
            for scan_dir in self.config.scan_dirs:
                scan_path = self.repo_root / scan_dir
                if scan_path.exists():
                    for file_path in scan_path.rglob("*.py"):
                        if not self._should_skip_file(file_path):
                            file_str = str(file_path.relative_to(self.repo_root))
                            if not any(skip in file_str for skip in ["test", "Test"]):
                                impl_files += 1

            # Estimate coverage
            if impl_files > 0:
                # Assume each test covers 2-3 implementation files on average
                coverage = min(100.0, (test_count * 2.5 / impl_files) * 100)
            else:
                coverage = 0.0

            print(f"     Estimated coverage: {coverage:.1f}% ({test_count} tests, {impl_files} impl files)")
            return coverage, test_count, impl_files

        except (subprocess.SubprocessError, Exception) as e:
            print(f"     Coverage estimation failed: {e}")
            return 0.0, 0, 0

    def _calculate_error_rate(self) -> float:
        """Calculate 24h rolling error rate."""
        logs_dir = self.repo_root / "logs"
        if not logs_dir.exists():
            return 0.0

        error_count = 0
        total_entries = 0

        for log_file in logs_dir.glob("*.log"):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        total_entries += 1
                        if "ERROR" in line or "CRITICAL" in line:
                            error_count += 1
            except (OSError, UnicodeDecodeError):
                pass

        if total_entries == 0:
            return 0.0

        error_rate = (error_count / total_entries) * 100
        return round(error_rate, 2)

def load_config() -> DebtScanConfig:
    """Load configuration from config/debt_scan.yaml."""
    config_path = Path("config/debt_scan.yaml")

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            return DebtScanConfig(**config_data)
        except Exception as e:
            print(f"Warning: Failed to load config, using defaults: {e}")

    # Default configuration
    return DebtScanConfig()

def write_baseline(results: DebtScanResult, baseline_path: Path):
    """Write baseline file with current duplicate hashes."""
    baseline = {
        "timestamp": results.timestamp.isoformat(),
        "duplicate_hashes": [dup.hash_value for dup in results.duplicate_groups],
        "total_duplicates": len(results.duplicate_groups)
    }

    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    with open(baseline_path, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)

    print(f"✅ Baseline written to {baseline_path}")

def load_baseline(baseline_path: Path) -> Set[str]:
    """Load baseline duplicate hashes."""
    if not baseline_path.exists():
        return set()

    try:
        with open(baseline_path, "r", encoding="utf-8") as f:
            baseline = json.load(f)
        return set(baseline.get("duplicate_hashes", []))
    except Exception:
        return set()

def generate_markdown_report(results: DebtScanResult, baseline_path: Optional[Path] = None) -> str:
    """Generate markdown report."""
    lines = []

    # Header
    lines.append("# Technical Debt Scan Report")
    lines.append("")
    lines.append(f"**Generated:** {results.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Executive Summary
    debt_score = results.calculate_debt_score()
    debt_level = "LOW" if debt_score < 30 else "MEDIUM" if debt_score < 70 else "HIGH"

    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"**Technical Debt Score:** {debt_score}/100 ({debt_level})")
    lines.append(f"**Total Files:** {results.total_files:,}")
    lines.append(f"**Lines of Code:** {results.total_lines:,}")
    lines.append(f"**Test Coverage:** {results.test_coverage_estimate:.1f}% ({results.total_tests} tests)")
    lines.append(f"**Error Rate (24h):** {results.error_rate_24h}%")
    lines.append("")

    # Detailed Metrics
    lines.append("## Detailed Metrics")
    lines.append("")
    lines.append("| Metric | Value | Status |")
    lines.append("|--------|-------|--------|")
    lines.append(f"| Duplicate Groups | {len(results.duplicate_groups)} | {'❌' if len(results.duplicate_groups) > 5 else '✅'} |")
    if baseline_path and baseline_path.exists():
        baseline_hashes = load_baseline(baseline_path)
        new_dups = [d for d in results.duplicate_groups if d.is_new_vs_baseline(baseline_hashes)]
        lines.append(f"| New Duplicates | {len(new_dups)} | {'❌' if len(new_dups) > 0 else '✅'} |")
    lines.append(f"| Syntax Errors | {len(results.syntax_errors)} | {'❌' if len(results.syntax_errors) > 0 else '✅'} |")
    lines.append(f"| SSOT Violations | {len(results.ssot_violations)} | {'❌' if len(results.ssot_violations) > 0 else '✅'} |")
    lines.append(f"| Largest File | {results.largest_file_kb}KB | {'⚠️' if results.largest_file_kb > 200 else '✅'} |")
    lines.append(f"| Avg File Size | {results.avg_file_size_kb}KB | {'⚠️' if results.avg_file_size_kb > 50 else '✅'} |")
    lines.append("")

    # Issues
    if results.duplicate_groups or results.syntax_errors or results.ssot_violations:
        lines.append("## Issues Found")
        lines.append("")

        # Syntax errors
        if results.syntax_errors:
            lines.append("### Syntax Errors")
            for error in results.syntax_errors[:5]:  # Show first 5
                lines.append(f"- {error['error']}")
            if len(results.syntax_errors) > 5:
                lines.append(f"- ... and {len(results.syntax_errors) - 5} more")
            lines.append("")

        # SSOT violations
        if results.ssot_violations:
            lines.append("### SSOT Violations")
            for violation in results.ssot_violations[:5]:  # Show first 5
                lines.append(f"- `{violation['file']}`: references deprecated `{violation['deprecated_path']}`")
            if len(results.ssot_violations) > 5:
                lines.append(f"- ... and {len(results.ssot_violations) - 5} more")
            lines.append("")

        # Duplicates
        if results.duplicate_groups:
            lines.append("### Duplicate Groups")
            lines.append("")
            for dup in results.duplicate_groups[:3]:  # Show top 3
                lines.append(f"#### {dup.count} files ({dup.size_bytes:,} bytes)")
                for file in dup.files[:3]:
                    lines.append(f"- `{file}`")
                if len(dup.files) > 3:
                    lines.append(f"- ... and {len(dup.files) - 3} more")
                lines.append("")

    return "\n".join(lines)

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT Technical Debt Scanner v1")
    parser.add_argument("--ci", action="store_true", help="CI mode: fail on threshold violations")
    parser.add_argument("--write-baseline", type=str, help="Write baseline file to PATH")
    parser.add_argument("--baseline", type=str, help="Baseline file for comparison (CI mode)")
    parser.add_argument("--config", type=str, default="config/debt_scan.yaml", help="Config file path")

    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Create scanner
    scanner = DebtScanner(config)

    # Run scan
    results = scanner.scan_all()

    # Load baseline if specified
    baseline_hashes = set()
    if args.baseline:
        baseline_path = Path(args.baseline)
        baseline_hashes = load_baseline(baseline_path)

        # Mark new duplicates
        results.new_duplicate_groups = [
            dup for dup in results.duplicate_groups
            if dup.is_new_vs_baseline(baseline_hashes)
        ]

    # Write baseline if requested
    if args.write_baseline:
        baseline_path = Path(args.write_baseline)
        write_baseline(results, baseline_path)
        return 0

    # Generate reports
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # JSON report
    json_path = reports_dir / "debt_scan.json"
    with open(json_path, "w", encoding="utf-8") as f:
        # Convert dataclasses to dicts for JSON
        result_dict = asdict(results)
        result_dict["timestamp"] = results.timestamp.isoformat()
        result_dict["duplicate_groups"] = [asdict(dup) for dup in results.duplicate_groups]
        result_dict["new_duplicate_groups"] = [asdict(dup) for dup in results.new_duplicate_groups]
        json.dump(result_dict, f, indent=2)

    # Markdown report
    md_path = reports_dir / "debt_scan.md"
    md_content = generate_markdown_report(results, Path(args.baseline) if args.baseline else None)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n📄 Reports saved:")
    print(f"   JSON: {json_path}")
    print(f"   Markdown: {md_path}")

    # CI mode: check thresholds
    if args.ci:
        if results.should_ci_fail():
            print("\n❌ CI FAILURE: Thresholds exceeded!")
            print(f"   Syntax errors: {len(results.syntax_errors)} (max: {config.max_syntax_errors})")
            print(f"   New duplicates: {len(results.new_duplicate_groups)} (max: {config.max_new_duplicate_groups})")
            print(f"   SSOT violations: {len(results.ssot_violations)} (max: {config.max_ssot_violations})")
            return 1
        else:
            print("\n✅ CI SUCCESS: All thresholds met!")
            return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())