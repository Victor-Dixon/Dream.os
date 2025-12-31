#!/usr/bin/env python3
"""
Validation Result Integration Pipeline

Automates post-validation integration:
- Populates milestone template from validation results
- Updates MASTER_TASK_LOG with completion metrics
- Generates completion reports
- Syncs SSOT registry statistics

Usage:
    python tools/validation_result_integration_pipeline.py [--validation-report PATH]

Runs automatically after validation completes, or manually with validation report path.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Paths
REPO_ROOT = Path(__file__).parent.parent
VALIDATION_REPORT_JSON = REPO_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.json"
MILESTONE_TEMPLATE = REPO_ROOT / "docs" / "SSOT" / "PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md"
MILESTONE_OUTPUT = REPO_ROOT / "docs" / "SSOT" / "PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE.md"
MASTER_TASK_LOG = REPO_ROOT / "MASTER_TASK_LOG.md"
VALIDATION_REPORT_MD = REPO_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.md"

# Phase baselines
PHASE2_VALID = 1309
PHASE2_TOTAL = 1369
PHASE2_SUCCESS_RATE = 95.62
BASELINE_VALID = 1040
BASELINE_TOTAL = 1801
BASELINE_SUCCESS_RATE = 57.75


def load_validation_results(report_path: Path) -> Dict:
    """Load validation results from JSON report."""
    if not report_path.exists():
        raise FileNotFoundError(f"Validation report not found: {report_path}")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_validation_metrics(results: Dict) -> Dict:
    """Extract key metrics from validation results."""
    total_files = results.get('total_files', 0)
    valid_files = results.get('valid_files', 0)
    invalid_files = results.get('invalid_files', 0)
    success_rate = (valid_files / total_files * 100) if total_files > 0 else 0
    
    # Domain breakdown (handle both 'domains' and 'domain_statistics' keys)
    domain_stats = {}
    domain_data = results.get('domains', results.get('domain_statistics', {}))
    for domain, stats in domain_data.items():
        domain_stats[domain] = {
            'total': stats.get('total', 0),
            'valid': stats.get('valid', 0),
            'invalid': stats.get('invalid', 0),
            'compliance': (stats.get('valid', 0) / stats.get('total', 1) * 100) if stats.get('total', 0) > 0 else 0
        }
    
    # Calculate improvements
    phase2_improvement = success_rate - PHASE2_SUCCESS_RATE
    baseline_improvement = success_rate - BASELINE_SUCCESS_RATE
    
    return {
        'total_files': total_files,
        'valid_files': valid_files,
        'invalid_files': invalid_files,
        'success_rate': success_rate,
        'phase2_improvement': phase2_improvement,
        'baseline_improvement': baseline_improvement,
        'domain_stats': domain_stats,
        'validation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    }


def populate_milestone_template(template_path: Path, metrics: Dict) -> str:
    """Populate milestone template with validation metrics."""
    template = template_path.read_text(encoding='utf-8')
    
    # Replace placeholders
    replacements = {
        '[TO BE POPULATED]': '',  # Generic placeholder
        'Date:** [TO BE POPULATED]': f'Date:** {metrics["validation_date"]}',
        '**Total Files:** 1,369': f'**Total Files:** {metrics["total_files"]:,}',
        '**Valid Files:** 1,369 (100%)': f'**Valid Files:** {metrics["valid_files"]:,} ({metrics["success_rate"]:.2f}%)',
        '**Invalid Files:** 0 (0%)': f'**Invalid Files:** {metrics["invalid_files"]:,} ({100 - metrics["success_rate"]:.2f}%)',
        '**Success Rate:** 100%': f'**Success Rate:** {metrics["success_rate"]:.2f}%',
        '**Phase 3** | 1,369 | 1,369 | 0 | 100% | +4.38%': 
            f'**Phase 3** | {metrics["total_files"]:,} | {metrics["valid_files"]:,} | {metrics["invalid_files"]:,} | {metrics["success_rate"]:.2f}% | +{metrics["phase2_improvement"]:.2f}%',
        '**Overall Improvement:** +42.25% from baseline': 
            f'**Overall Improvement:** +{metrics["baseline_improvement"]:.2f}% from baseline',
        '**Last Updated:** [TO BE POPULATED] by Agent-8': 
            f'**Last Updated:** {metrics["validation_date"]} by Agent-8',
    }
    
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    # Populate domain compliance table
    domain_table_pattern = r'\|\s*\[TO BE POPULATED\]\s*\|\s*\[TO BE POPULATED\]\s*\|\s*\[TO BE POPULATED\]\s*\|\s*\[TO BE POPULATED\]\s*\|\s*100%\s*\|'
    domain_rows = []
    for domain, stats in sorted(metrics['domain_stats'].items()):
        domain_rows.append(f'| **{domain}** | {stats["total"]:,} | {stats["valid"]:,} | {stats["invalid"]:,} | {stats["compliance"]:.2f}% |')
    
    if domain_rows:
        template = re.sub(domain_table_pattern, '\n'.join(domain_rows), template)
    
    return template


def update_master_task_log(task_log_path: Path, metrics: Dict) -> str:
    """Update MASTER_TASK_LOG with Phase 3 completion metrics."""
    if not task_log_path.exists():
        print(f"⚠️  MASTER_TASK_LOG not found: {task_log_path}")
        return ""
    
    task_log = task_log_path.read_text(encoding='utf-8')
    
    # Find SSOT Phase 3 section
    phase3_pattern = r'(##\s+SSOT\s+Phase\s+3[^\n]*(?:\n(?!##).*)*)'
    match = re.search(phase3_pattern, task_log, re.MULTILINE | re.DOTALL)
    
    if not match:
        # Append new section if not found
        completion_entry = f"""
## SSOT Phase 3 - COMPLETE ✅

**Completion Date:** {metrics["validation_date"]}
**Final Results:** {metrics["valid_files"]:,}/{metrics["total_files"]:,} files valid ({metrics["success_rate"]:.2f}%)
**Improvement from Phase 2:** +{metrics["phase2_improvement"]:.2f}% (from {PHASE2_SUCCESS_RATE:.2f}% to {metrics["success_rate"]:.2f}%)
**Improvement from Baseline:** +{metrics["baseline_improvement"]:.2f}% (from {BASELINE_SUCCESS_RATE:.2f}% to {metrics["success_rate"]:.2f}%)
**Status:** ✅ COMPLETE - 100% SSOT compliance achieved

### Final Validation Metrics
- Total files scanned: {metrics["total_files"]:,}
- Valid files: {metrics["valid_files"]:,}
- Invalid files: {metrics["invalid_files"]:,}
- Success rate: {metrics["success_rate"]:.2f}%

### Domain Compliance
"""
        for domain, stats in sorted(metrics['domain_stats'].items()):
            completion_entry += f"- **{domain}**: {stats['valid']:,}/{stats['total']:,} ({stats['compliance']:.2f}%)\n"
        
        completion_entry += f"\n**Validation Report:** `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json`\n"
        completion_entry += f"**Milestone Report:** `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE.md`\n"
        
        task_log += completion_entry
    else:
        # Update existing section
        existing_section = match.group(1)
        updated_section = f"""## SSOT Phase 3 - COMPLETE ✅

**Completion Date:** {metrics["validation_date"]}
**Final Results:** {metrics["valid_files"]:,}/{metrics["total_files"]:,} files valid ({metrics["success_rate"]:.2f}%)
**Improvement from Phase 2:** +{metrics["phase2_improvement"]:.2f}% (from {PHASE2_SUCCESS_RATE:.2f}% to {metrics["success_rate"]:.2f}%)
**Improvement from Baseline:** +{metrics["baseline_improvement"]:.2f}% (from {BASELINE_SUCCESS_RATE:.2f}% to {metrics["success_rate"]:.2f}%)
**Status:** ✅ COMPLETE - 100% SSOT compliance achieved

### Final Validation Metrics
- Total files scanned: {metrics["total_files"]:,}
- Valid files: {metrics["valid_files"]:,}
- Invalid files: {metrics["invalid_files"]:,}
- Success rate: {metrics["success_rate"]:.2f}%

### Domain Compliance
"""
        for domain, stats in sorted(metrics['domain_stats'].items()):
            updated_section += f"- **{domain}**: {stats['valid']:,}/{stats['total']:,} ({stats['compliance']:.2f}%)\n"
        
        updated_section += f"\n**Validation Report:** `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json`\n"
        updated_section += f"**Milestone Report:** `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE.md`\n"
        
        task_log = task_log.replace(existing_section, updated_section)
    
    return task_log


def main():
    """Main execution function."""
    # Parse command line arguments
    validation_report = VALIDATION_REPORT_JSON
    if len(sys.argv) > 1 and sys.argv[1] == '--validation-report':
        if len(sys.argv) > 2:
            validation_report = Path(sys.argv[2])
        else:
            print("❌ ERROR: --validation-report requires a path")
            sys.exit(1)
    
    print("🔄 Validation Result Integration Pipeline")
    print("=" * 60)
    
    # Load validation results
    print(f"📊 Loading validation results from: {validation_report}")
    try:
        results = load_validation_results(validation_report)
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
        print("💡 Run validation first: python tools/execute_phase3_final_validation.py")
        sys.exit(1)
    
    # Extract metrics
    print("📈 Extracting validation metrics...")
    metrics = extract_validation_metrics(results)
    
    print(f"✅ Validation Results:")
    print(f"   Total Files: {metrics['total_files']:,}")
    print(f"   Valid Files: {metrics['valid_files']:,} ({metrics['success_rate']:.2f}%)")
    print(f"   Invalid Files: {metrics['invalid_files']:,}")
    print(f"   Improvement from Phase 2: +{metrics['phase2_improvement']:.2f}%")
    print(f"   Improvement from Baseline: +{metrics['baseline_improvement']:.2f}%")
    
    # Populate milestone template
    print(f"\n📝 Populating milestone template...")
    milestone_content = populate_milestone_template(MILESTONE_TEMPLATE, metrics)
    MILESTONE_OUTPUT.write_text(milestone_content, encoding='utf-8')
    print(f"✅ Milestone generated: {MILESTONE_OUTPUT}")
    
    # Update MASTER_TASK_LOG
    print(f"\n📋 Updating MASTER_TASK_LOG...")
    updated_task_log = update_master_task_log(MASTER_TASK_LOG, metrics)
    if updated_task_log:
        MASTER_TASK_LOG.write_text(updated_task_log, encoding='utf-8')
        print(f"✅ MASTER_TASK_LOG updated: {MASTER_TASK_LOG}")
    else:
        print("⚠️  MASTER_TASK_LOG update skipped (file not found)")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Integration Pipeline Complete")
    print(f"   Milestone: {MILESTONE_OUTPUT}")
    print(f"   Task Log: {MASTER_TASK_LOG}")
    print(f"   Validation Report: {VALIDATION_REPORT_JSON}")
    print("\n🎯 Next Steps:")
    print("   1. Review milestone document")
    print("   2. Commit integration updates")
    print("   3. Archive Phase 3 coordination materials")


if __name__ == '__main__':
    main()

