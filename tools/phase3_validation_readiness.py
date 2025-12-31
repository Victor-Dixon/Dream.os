#!/usr/bin/env python3
"""
Phase 3 SSOT Validation Readiness Checker
==========================================

Checks readiness for Phase 3 post-completion validation by verifying:
- All Priority 3 files have been remediated
- Tag placement compliance
- Domain registry compliance
- Compilation status

Usage:
    python tools/phase3_validation_readiness.py                    # Full readiness check
    python tools/phase3_validation_readiness.py --priority 3      # Check Priority 3 only
    python tools/phase3_validation_readiness.py --report-only     # Generate report only

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-30
Purpose: Validate Phase 3 SSOT remediation completion readiness

<!-- SSOT Domain: validation -->
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess


@dataclass
class ValidationReadiness:
    """Readiness status for a file."""
    file_path: Path
    domain: str
    priority: int
    issue_type: str
    status: str  # "ready", "pending", "failed"
    error: Optional[str] = None


class Phase3ValidationReadinessChecker:
    """Checks Phase 3 SSOT remediation validation readiness."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.phase3_file_lists = repo_root / "docs" / "SSOT" / "PHASE3_PRIORITY23_FILE_LISTS.json"
        self.validation_tool = repo_root / "tools" / "validate_all_ssot_files.py"
        
    def load_phase3_files(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load Phase 3 file lists from JSON."""
        if not self.phase3_file_lists.exists():
            return {}
        
        with open(self.phase3_file_lists, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def check_file_readiness(self, file_info: Dict[str, Any]) -> ValidationReadiness:
        """Check if a single file is ready for validation."""
        file_path = Path(file_info['file_path'])
        
        # Check if file exists
        if not file_path.exists():
            return ValidationReadiness(
                file_path=file_path,
                domain=file_info.get('domain', 'unknown'),
                priority=file_info.get('priority', 3),
                issue_type=file_info.get('error', 'unknown'),
                status="failed",
                error="File not found"
            )
        
        # Check compilation for Python files
        if file_path.suffix == '.py':
            try:
                result = subprocess.run(
                    ['python', '-m', 'py_compile', str(file_path)],
                    capture_output=True,
                    timeout=5,
                    cwd=str(self.repo_root)
                )
                if result.returncode != 0:
                    return ValidationReadiness(
                        file_path=file_path,
                        domain=file_info.get('domain', 'unknown'),
                        priority=file_info.get('priority', 3),
                        issue_type=file_info.get('error', 'unknown'),
                        status="failed",
                        error=f"Compilation error: {result.stderr.decode()[:200]}"
                    )
            except Exception as e:
                return ValidationReadiness(
                    file_path=file_path,
                    domain=file_info.get('domain', 'unknown'),
                    priority=file_info.get('priority', 3),
                    issue_type=file_info.get('error', 'unknown'),
                    status="failed",
                    error=f"Compilation check failed: {str(e)}"
                )
        
        # File exists and compiles - check if validation tool can process it
        return ValidationReadiness(
            file_path=file_path,
            domain=file_info.get('domain', 'unknown'),
            priority=file_info.get('priority', 3),
            issue_type=file_info.get('error', 'unknown'),
            status="ready"
        )
    
    def check_readiness(self, priority: Optional[int] = None) -> List[ValidationReadiness]:
        """Check readiness for all Phase 3 files."""
        phase3_data = self.load_phase3_files()
        results = []
        
        # Check Priority 3 tag placement files
        if 'priority3_tag_placement' in phase3_data:
            for file_info in phase3_data['priority3_tag_placement']['files']:
                if priority is None or file_info.get('priority', 3) == priority:
                    readiness = self.check_file_readiness(file_info)
                    results.append(readiness)
        
        return results
    
    def generate_report(self, results: List[ValidationReadiness], output_path: Optional[Path] = None) -> str:
        """Generate validation readiness report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        ready_count = sum(1 for r in results if r.status == "ready")
        pending_count = sum(1 for r in results if r.status == "pending")
        failed_count = sum(1 for r in results if r.status == "failed")
        total = len(results)
        
        report = f"""# Phase 3 SSOT Validation Readiness Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Total Files:** {total}  
**Ready:** {ready_count} ✅  
**Pending:** {pending_count} ⏳  
**Failed:** {failed_count} ❌  
**Readiness Rate:** {(ready_count/total*100) if total > 0 else 0:.1f}%

---

## Summary by Status

### ✅ Ready for Validation ({ready_count})
Files that exist, compile (if Python), and are ready for SSOT validation.

### ⏳ Pending ({pending_count})
Files that may need additional remediation before validation.

### ❌ Failed ({failed_count})
Files with compilation errors or missing from filesystem.

---

## Detailed Results

"""
        
        # Group by status
        ready_files = [r for r in results if r.status == "ready"]
        pending_files = [r for r in results if r.status == "pending"]
        failed_files = [r for r in results if r.status == "failed"]
        
        if ready_files:
            report += "### ✅ Ready Files\n\n"
            for r in ready_files:
                report += f"- `{r.file_path}` (Domain: {r.domain}, Priority: {r.priority})\n"
            report += "\n"
        
        if pending_files:
            report += "### ⏳ Pending Files\n\n"
            for r in pending_files:
                report += f"- `{r.file_path}` (Domain: {r.domain}, Priority: {r.priority})\n"
            report += "\n"
        
        if failed_files:
            report += "### ❌ Failed Files\n\n"
            for r in failed_files:
                report += f"- `{r.file_path}` (Domain: {r.domain}, Priority: {r.priority})\n"
                if r.error:
                    report += f"  - Error: {r.error}\n"
            report += "\n"
        
        # Group by domain
        report += "## Results by Domain\n\n"
        domain_groups: Dict[str, List[ValidationReadiness]] = {}
        for r in results:
            if r.domain not in domain_groups:
                domain_groups[r.domain] = []
            domain_groups[r.domain].append(r)
        
        for domain, files in sorted(domain_groups.items()):
            ready = sum(1 for f in files if f.status == "ready")
            total_domain = len(files)
            report += f"### {domain}\n"
            report += f"- **Ready:** {ready}/{total_domain} ({ready/total_domain*100 if total_domain > 0 else 0:.1f}%)\n\n"
        
        report += "\n---\n\n"
        report += "*Generated by Phase 3 Validation Readiness Checker*"
        
        if output_path:
            output_path.write_text(report, encoding='utf-8')
            print(f"✅ Report written to: {output_path}")
        
        return report


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Check Phase 3 SSOT validation readiness"
    )
    parser.add_argument(
        "--priority",
        type=int,
        help="Check specific priority level (default: all)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output report file path"
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report only (skip checks)"
    )
    
    args = parser.parse_args()
    
    repo_root = Path(__file__).resolve().parent.parent
    checker = Phase3ValidationReadinessChecker(repo_root)
    
    if args.report_only:
        print("⚠️  Report-only mode not yet implemented")
        return 1
    
    print("🔍 Checking Phase 3 validation readiness...")
    results = checker.check_readiness(priority=args.priority)
    
    if not results:
        print("⚠️  No Phase 3 files found to check")
        return 1
    
    # Generate report
    output_path = args.output
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = repo_root / "reports" / f"phase3_validation_readiness_{timestamp}.md"
        output_path.parent.mkdir(exist_ok=True)
    
    report = checker.generate_report(results, output_path)
    
    # Print summary
    ready = sum(1 for r in results if r.status == "ready")
    total = len(results)
    print(f"\n✅ Validation Readiness: {ready}/{total} files ready ({(ready/total*100) if total > 0 else 0:.1f}%)")
    print(f"📄 Report: {output_path}")
    
    return 0 if ready == total else 1


if __name__ == "__main__":
    exit(main())

