#!/usr/bin/env python3
"""
Agent-8 SSOT Verification Script
Verifies SSOT compliance for 25 assigned files (core/services/infrastructure domains)
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

REPO_ROOT = Path(__file__).parent.parent

# 25 files assigned to Agent-8 for SSOT verification
AGENT8_SSOT_FILES = [
    # Base Classes (7 files)
    "src/core/base/__init__.py",
    "src/core/base/base_manager.py",
    "src/core/base/base_handler.py",
    "src/core/base/base_service.py",
    "src/core/base/initialization_mixin.py",
    "src/core/base/error_handling_mixin.py",
    "src/core/base/availability_mixin.py",

    # Config Files (5 files)
    "src/core/config/__init__.py",
    "src/core/config/config_manager.py",
    "src/core/config/config_dataclasses.py",
    "src/core/config/config_accessors.py",
    "src/core/config/config_enums.py",

    # Messaging Core (5 files)
    "src/core/messaging_core.py",
    "src/core/messaging_models.py",
    "src/core/messaging_templates.py",
    "src/core/messaging_pyautogui.py",
    "src/core/message_queue.py",

    # Error Handling (4 files)
    "src/core/error_handling/__init__.py",
    "src/core/error_handling/error_response_models.py",
    "src/core/error_handling/error_response_models_core.py",
    "src/core/error_handling/error_response_models_specialized.py",

    # Coordination (2 files)
    "src/core/coordination/__init__.py",
    "src/core/coordinator_interfaces.py",

    # Infrastructure/System Integration (2 files)
    "src/core/config_ssot.py",
    "src/core/pydantic_config.py",
]

SSOT_PATTERNS = [
    r'<!--\s*SSOT\s+Domain:\s*(\w+)\s*-->',
    r'#\s*SSOT\s+Domain:\s*(\w+)',
    r'"""\s*SSOT\s+Domain:\s*(\w+)',
    r"'''\s*SSOT\s+Domain:\s*(\w+)",
]


def check_ssot_tag(file_path: Path) -> Tuple[bool, str, str]:
    """Check if file has SSOT tag and return (has_tag, domain, reason)"""
    if not file_path.exists():
        return False, "", f"File not found: {file_path}"

    try:
        content = file_path.read_text(encoding='utf-8')

        # Check first 50 lines for SSOT tag
        lines = content.split('\n')[:50]
        header_content = '\n'.join(lines)

        for pattern in SSOT_PATTERNS:
            match = re.search(pattern, header_content, re.IGNORECASE)
            if match:
                domain = match.group(1).strip()
                return True, domain, f"SSOT tag found: {domain}"

        return False, "", "No SSOT tag found in first 50 lines"
    except Exception as e:
        return False, "", f"Error reading file: {str(e)}"


def verify_all_files() -> List[Dict]:
    """Verify all 25 files and return results"""
    results = []

    for file_rel_path in AGENT8_SSOT_FILES:
        file_path = REPO_ROOT / file_rel_path
        has_tag, domain, reason = check_ssot_tag(file_path)

        status = "PASS" if has_tag else "FAIL"

        results.append({
            "file": file_rel_path,
            "status": status,
            "domain": domain if has_tag else "N/A",
            "reason": reason,
            "exists": file_path.exists()
        })

    return results


def generate_report(results: List[Dict]) -> str:
    """Generate markdown report"""
    report = []
    report.append("# Agent-8 SSOT Verification Report")
    report.append("")
    report.append("**Date**: 2025-12-13")
    report.append("**Agent**: Agent-8 (SSOT & System Integration Specialist)")
    report.append(
        "**Task**: SSOT Verification - 25 Core/Services/Infrastructure Files")
    report.append("")
    report.append("---")
    report.append("")
    report.append("## Summary")
    report.append("")

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    report.append(f"- **Total Files**: {total}")
    report.append(f"- **PASS**: {passed} ({passed*100//total}%)")
    report.append(f"- **FAIL**: {failed} ({failed*100//total}%)")
    report.append("")
    report.append("---")
    report.append("")
    report.append("## Detailed Results")
    report.append("")
    report.append("| File | Status | Domain | Reason |")
    report.append("|------|--------|--------|--------|")

    for r in results:
        file_name = r["file"].split("/")[-1]
        status_emoji = "✅" if r["status"] == "PASS" else "❌"
        report.append(
            f"| `{file_name}` | {status_emoji} {r['status']} | {r['domain']} | {r['reason']} |")

    report.append("")
    report.append("---")
    report.append("")
    report.append("## Files by Category")
    report.append("")

    categories = {
        "Base Classes": [f for f in AGENT8_SSOT_FILES if "base" in f],
        "Config Files": [f for f in AGENT8_SSOT_FILES if "config" in f],
        "Messaging": [f for f in AGENT8_SSOT_FILES if "messaging" in f or "message_queue" in f],
        "Error Handling": [f for f in AGENT8_SSOT_FILES if "error_handling" in f],
        "Coordination": [f for f in AGENT8_SSOT_FILES if "coordination" in f or "coordinator" in f],
        "Infrastructure": [f for f in AGENT8_SSOT_FILES if "ssot" in f or "pydantic" in f],
    }

    for category, files in categories.items():
        if files:
            report.append(f"### {category} ({len(files)} files)")
            report.append("")
            for file_rel_path in files:
                result = next(
                    (r for r in results if r["file"] == file_rel_path), None)
                if result:
                    status_emoji = "✅" if result["status"] == "PASS" else "❌"
                    report.append(
                        f"- {status_emoji} `{file_rel_path}` - {result['status']} ({result['domain']})")
            report.append("")

    report.append("---")
    report.append("")
    report.append("## Next Steps")
    report.append("")

    if failed > 0:
        report.append("### Files Requiring SSOT Tags:")
        report.append("")
        for r in results:
            if r["status"] == "FAIL":
                report.append(f"- `{r['file']}` - {r['reason']}")
        report.append("")

    report.append(
        "**Status**: Report complete, ready for coordination with Agent-5")
    report.append("")
    report.append("🐝 **WE. ARE. SWARM. ⚡🔥**")

    return "\n".join(report)


if __name__ == "__main__":
    print("Agent-8 SSOT Verification - Checking 25 files...")
    results = verify_all_files()
    report = generate_report(results)

    # Save report
    report_path = REPO_ROOT / "docs" / "agent-8" / \
        "AGENT8_SSOT_VERIFICATION_REPORT_2025-12-13.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding='utf-8')

    print(f"\nReport generated: {report_path}")
    print(
        f"\nSummary: {sum(1 for r in results if r['status'] == 'PASS')}/{len(results)} files PASS")

    # Print summary
    print("\n" + "="*60)
    print(report)
    print("="*60)



