#!/usr/bin/env python3
"""
Verify Infrastructure SSOT Tags
===============================

Verifies SSOT domain tags in infrastructure files and generates report.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Task: SSOT Remediation Priority 1

<!-- SSOT Domain: infrastructure -->
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


# Infrastructure domain patterns
INFRASTRUCTURE_PATTERNS = [
    r"monitor",
    r"health",
    r"queue",
    r"deploy",
    r"ci.*cd",
    r"workflow",
    r"infrastructure",
    r"devops",
    r"status",
    r"activity.*detector",
    r"workspace.*health",
    r"agent.*fuel",
    r"message.*queue",
    r"integration.*health",
    r"system.*health",
    r"wordpress",
    r"sftp",
    r"diagnose",
    r"validate.*ci",
    r"diagnose.*github",
    r"diagnose.*wordpress",
    r"fix.*wordpress",
    r"disable.*wordpress",
    r"enable.*wordpress",
    r"check.*wordpress",
    r"reinitialize",
]

SSOT_TAG = "<!-- SSOT Domain: infrastructure -->"
SSOT_TAG_VARIANTS = [
    "<!-- SSOT Domain: infrastructure -->",
    "<!--SSOT Domain: infrastructure-->",
    "# SSOT Domain: infrastructure",
    "SSOT Domain: infrastructure",
]


def is_infrastructure_file(file_path: Path) -> bool:
    """Check if file is in infrastructure domain."""
    name_lower = file_path.name.lower()
    path_lower = str(file_path).lower()
    
    # Check patterns
    for pattern in INFRASTRUCTURE_PATTERNS:
        if re.search(pattern, name_lower) or re.search(pattern, path_lower):
            return True
    
    # Check directory
    if "infrastructure" in path_lower:
        return True
    
    return False


def has_ssot_tag(content: str) -> Tuple[bool, str]:
    """Check if file has SSOT tag."""
    content_lower = content.lower()
    
    for variant in SSOT_TAG_VARIANTS:
        if variant.lower() in content_lower:
            # Find exact match
            if variant in content:
                return True, variant
            # Find case-insensitive match
            pattern = re.escape(variant).replace(r'\ ', r'\s*')
            if re.search(pattern, content, re.IGNORECASE):
                return True, variant
    
    return False, ""


def find_ssot_tag_position(content: str) -> int:
    """Find line number where SSOT tag should be placed."""
    lines = content.split('\n')
    
    # Look for docstring end or header section
    for i, line in enumerate(lines[:50]):  # Check first 50 lines
        if '"""' in line and i > 0:
            # After docstring
            return i + 1
        if 'author' in line.lower() or 'date' in line.lower():
            # After author/date
            return i + 1
        if line.strip().startswith('import ') and i > 5:
            # After imports start
            return i
    
    return 5  # Default: after line 5


def scan_infrastructure_files() -> Dict:
    """Scan infrastructure files for SSOT tags."""
    print("=" * 60)
    print("🔍 Scanning Infrastructure Files for SSOT Tags")
    print("=" * 60)
    
    results = {
        "scanned": 0,
        "infrastructure_files": [],
        "with_tags": [],
        "without_tags": [],
        "needs_verification": []
    }
    
    # Scan tools directory
    tools_dir = Path("tools")
    if not tools_dir.exists():
        print("❌ tools/ directory not found")
        return results
    
    python_files = list(tools_dir.rglob("*.py"))
    results["scanned"] = len(python_files)
    
    print(f"\n📁 Found {len(python_files)} Python files in tools/")
    
    for file_path in python_files:
        if is_infrastructure_file(file_path):
            results["infrastructure_files"].append(str(file_path))
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_tag, tag_variant = has_ssot_tag(content)
                
                file_info = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "has_tag": has_tag,
                    "tag_variant": tag_variant if has_tag else "",
                    "insert_position": find_ssot_tag_position(content)
                }
                
                if has_tag:
                    results["with_tags"].append(file_info)
                    print(f"  ✅ {file_path.name}")
                else:
                    results["without_tags"].append(file_info)
                    print(f"  ❌ {file_path.name} - Missing SSOT tag")
                    
            except Exception as e:
                print(f"  ⚠️  {file_path.name} - Error: {e}")
                results["needs_verification"].append({
                    "path": str(file_path),
                    "error": str(e)
                })
    
    return results


def generate_report(results: Dict) -> str:
    """Generate SSOT tagging verification report."""
    report = []
    report.append("# Infrastructure SSOT Tagging Verification Report\n\n")
    report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Task**: SSOT Remediation Priority 1\n")
    report.append(f"**Agent**: Agent-3 (Infrastructure & DevOps)\n\n")
    
    report.append("## Summary\n\n")
    report.append(f"- **Files Scanned**: {results['scanned']}\n")
    report.append(f"- **Infrastructure Files Found**: {len(results['infrastructure_files'])}\n")
    report.append(f"- **With SSOT Tags**: {len(results['with_tags'])} ✅\n")
    report.append(f"- **Without SSOT Tags**: {len(results['without_tags'])} ❌\n")
    report.append(f"- **Needs Verification**: {len(results['needs_verification'])}\n\n")
    
    # Files with tags
    if results['with_tags']:
        report.append("## ✅ Files With SSOT Tags\n\n")
        for file_info in results['with_tags']:
            report.append(f"- `{file_info['name']}`\n")
        report.append("\n")
    
    # Files without tags
    if results['without_tags']:
        report.append("## ❌ Files Missing SSOT Tags\n\n")
        for file_info in results['without_tags']:
            report.append(f"- `{file_info['name']}` (insert at line {file_info['insert_position']})\n")
        report.append("\n")
        
        report.append("### Recommended Action\n\n")
        report.append("Add the following tag to each file:\n\n")
        report.append("```markdown\n")
        report.append("<!-- SSOT Domain: infrastructure -->\n")
        report.append("```\n\n")
        report.append("Place it in the file header, after author/date information.\n\n")
    
    # Verification needed
    if results['needs_verification']:
        report.append("## ⚠️  Files Needing Verification\n\n")
        for file_info in results['needs_verification']:
            report.append(f"- `{file_info['path']}` - {file_info['error']}\n")
        report.append("\n")
    
    # Statistics
    if results['infrastructure_files']:
        coverage = (len(results['with_tags']) / len(results['infrastructure_files'])) * 100
        report.append("## 📊 Coverage Statistics\n\n")
        report.append(f"- **SSOT Tag Coverage**: {coverage:.1f}%\n")
        report.append(f"- **Remaining**: {len(results['without_tags'])} files need tags\n\n")
    
    return "".join(report)


def main():
    """Main verification function."""
    print("\n" + "=" * 60)
    print("🔍 Infrastructure SSOT Tag Verification")
    print("=" * 60)
    print("Task: SSOT Remediation Priority 1\n")
    
    results = scan_infrastructure_files()
    
    # Generate report
    report = generate_report(results)
    
    # Save report
    report_file = Path("agent_workspaces/Agent-3/infrastructure_ssot_tagging_report_2025-12-12.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print("📊 Verification Complete")
    print("=" * 60)
    
    total = len(results['infrastructure_files'])
    with_tags = len(results['with_tags'])
    without_tags = len(results['without_tags'])
    
    if total > 0:
        coverage = (with_tags / total) * 100
        print(f"\n✅ Files with tags: {with_tags}/{total} ({coverage:.1f}%)")
        print(f"❌ Files missing tags: {without_tags}")
    else:
        print("\n⚠️  No infrastructure files found")
    
    print(f"\n📄 Report saved: {report_file}")
    print()


if __name__ == "__main__":
    main()

