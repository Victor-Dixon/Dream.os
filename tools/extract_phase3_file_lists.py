#!/usr/bin/env python3
"""
Extract Phase 3 file lists by domain from Phase 2 validation report.

Generates domain-specific file lists for Phase 3 remediation coordination.

<!-- SSOT Domain: tools -->
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

def load_validation_report(report_path: str = "docs/SSOT/FINAL_VALIDATION_CHECKPOINT_20251230_175053.json") -> Dict:
    """Load Phase 2 validation report."""
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_invalid_files_by_domain(report: Dict) -> Dict[str, List[Dict]]:
    """Extract invalid files grouped by domain."""
    invalid_by_domain = defaultdict(list)
    
    # Find the list of file results - it's the last value in the dict
    all_files = None
    for key, value in report.items():
        if isinstance(value, list) and len(value) > 0:
            if isinstance(value[0], dict) and 'file' in value[0]:
                all_files = value
                break
    
    if not all_files:
        # Fallback: check if report itself is a list
        if isinstance(report, list):
            all_files = report
    
    if all_files:
        for file_result in all_files:
            if isinstance(file_result, dict) and file_result.get('valid') is False:
                domain = file_result.get('domain', 'unknown')
                invalid_by_domain[domain].append(file_result)
    
    return dict(invalid_by_domain)

def generate_domain_file_lists(invalid_by_domain: Dict[str, List[Dict]], output_dir: Path = Path("docs/SSOT/PHASE3_FILE_LISTS")):
    """Generate domain-specific file lists for Phase 3 coordination."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Domain owner mapping
    domain_owners = {
        'core': 'Agent-2',
        'integration': 'Agent-1',
        'infrastructure': 'Agent-3',
        'safety': 'Agent-3',
        'data': 'Agent-5',
        'domain': 'Agent-2',
        'trading_robot': 'Agent-5',
        'logging': 'TBD',
        'discord': 'TBD',
    }
    
    # Priority mapping
    high_priority_domains = {'core', 'integration', 'infrastructure'}
    medium_priority_domains = {'safety', 'data', 'domain', 'trading_robot', 'logging', 'discord'}
    
    for domain, files in invalid_by_domain.items():
        owner = domain_owners.get(domain, 'TBD')
        priority = 'HIGH' if domain in high_priority_domains else 'MEDIUM' if domain in medium_priority_domains else 'LOW'
        
        # Generate markdown file list
        output_file = output_dir / f"{domain}_files.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Phase 3 Remediation - {domain.upper()} Domain\n\n")
            f.write(f"**Owner:** {owner}\n")
            f.write(f"**Priority:** {priority}\n")
            f.write(f"**Total Files:** {len(files)}\n\n")
            f.write("<!-- SSOT Domain: documentation -->\n\n")
            f.write("---\n\n")
            f.write("## Files Requiring Remediation\n\n")
            
            for i, file_result in enumerate(files, 1):
                file_path = file_result.get('file', '')
                issues = []
                
                if not file_result.get('tag_format', [True])[0]:
                    issues.append("Tag format")
                if not file_result.get('domain_registry', [True])[0]:
                    issues.append("Domain registry")
                if not file_result.get('tag_placement', [True])[0]:
                    issues.append("Tag placement")
                if not file_result.get('compilation', [True])[0]:
                    issues.append("Compilation")
                
                f.write(f"### {i}. {Path(file_path).name}\n\n")
                f.write(f"**Path:** `{file_path}`\n\n")
                f.write(f"**Issues:** {', '.join(issues) if issues else 'Unknown'}\n\n")
                f.write(f"**Details:**\n")
                for check, result in [
                    ('tag_format', 'Tag Format'),
                    ('domain_registry', 'Domain Registry'),
                    ('tag_placement', 'Tag Placement'),
                    ('compilation', 'Compilation')
                ]:
                    check_result = file_result.get(check, [True, ''])
                    status = '✅' if check_result[0] else '❌'
                    message = check_result[1] if isinstance(check_result, list) else str(check_result)
                    f.write(f"- {status} **{result}:** {message}\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write("## Remediation Guidelines\n\n")
            f.write("1. Review each file's issues\n")
            f.write("2. Fix SSOT tag format if needed: `<!-- SSOT Domain: <domain> -->`\n")
            f.write("3. Verify domain is in SSOT registry\n")
            f.write("4. Ensure tag is in first 50 lines\n")
            f.write("5. Verify Python files compile successfully\n")
            f.write("6. Run validation: `python tools/validate_all_ssot_files.py`\n")
    
    # Generate summary
    summary_file = output_dir / "SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Phase 3 File Lists Summary\n\n")
        f.write("<!-- SSOT Domain: documentation -->\n\n")
        f.write("---\n\n")
        f.write("## Domain File Counts\n\n")
        f.write("| Domain | Files | Owner | Priority |\n")
        f.write("|--------|-------|-------|----------|\n")
        
        for domain in sorted(invalid_by_domain.keys()):
            owner = domain_owners.get(domain, 'TBD')
            priority = 'HIGH' if domain in high_priority_domains else 'MEDIUM' if domain in medium_priority_domains else 'LOW'
            count = len(invalid_by_domain[domain])
            f.write(f"| {domain} | {count} | {owner} | {priority} |\n")
        
        f.write("\n---\n\n")
        f.write("## File Lists\n\n")
        for domain in sorted(invalid_by_domain.keys()):
            f.write(f"- [{domain.upper()} Domain]({domain}_files.md) - {len(invalid_by_domain[domain])} files\n")

if __name__ == "__main__":
    report = load_validation_report()
    invalid_by_domain = extract_invalid_files_by_domain(report)
    generate_domain_file_lists(invalid_by_domain)
    
    total_files = sum(len(files) for files in invalid_by_domain.values())
    print(f"✅ Extracted {total_files} invalid files across {len(invalid_by_domain)} domains")
    print(f"✅ Generated file lists in docs/SSOT/PHASE3_FILE_LISTS/")
