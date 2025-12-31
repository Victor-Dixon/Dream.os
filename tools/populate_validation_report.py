#!/usr/bin/env python3
"""
Populate Final Phase 3 Validation Report from JSON Results

Automatically populates FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md
with results from FINAL_PHASE3_VALIDATION_REPORT.json.

Usage:
    python tools/populate_validation_report.py \
        --json docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json \
        --template docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md \
        --output docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md
"""

#!/usr/bin/env python3
"""
Populate Final Phase 3 Validation Report from JSON Results

Automatically populates FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md
with results from FINAL_PHASE3_VALIDATION_REPORT.json.

Usage:
    python tools/populate_validation_report.py \
        --json docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json \
        --template docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md \
        --output docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# SSOT Domain: tools

def load_json_report(json_path):
    """Load validation report JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template(template_path):
    """Load validation report template."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def calculate_metrics(report):
    """Calculate validation metrics from report."""
    total_files = len(report.get('validation_results', []))
    valid_files = sum(1 for r in report.get('validation_results', []) if r.get('valid', False))
    invalid_files = total_files - valid_files
    success_rate = (valid_files / total_files * 100) if total_files > 0 else 0
    
    # Phase 2 baseline
    phase2_valid = 1309
    phase2_total = 1369
    phase2_rate = 95.62
    
    # Baseline
    baseline_valid = 1040
    baseline_total = 1801
    baseline_rate = 57.75
    
    improvement_from_phase2 = success_rate - phase2_rate
    improvement_from_baseline = success_rate - baseline_rate
    
    return {
        'total_files': total_files,
        'valid_files': valid_files,
        'invalid_files': invalid_files,
        'success_rate': round(success_rate, 2),
        'phase2_valid': phase2_valid,
        'phase2_total': phase2_total,
        'phase2_rate': phase2_rate,
        'improvement_from_phase2': round(improvement_from_phase2, 2),
        'baseline_valid': baseline_valid,
        'baseline_total': baseline_total,
        'baseline_rate': baseline_rate,
        'improvement_from_baseline': round(improvement_from_baseline, 2)
    }

def calculate_domain_compliance(report):
    """Calculate domain-by-domain compliance."""
    domain_stats = defaultdict(lambda: {'total': 0, 'valid': 0})
    
    for result in report.get('validation_results', []):
        domain = result.get('domain', 'unknown')
        domain_stats[domain]['total'] += 1
        if result.get('valid', False):
            domain_stats[domain]['valid'] += 1
    
    compliance = {}
    for domain, stats in sorted(domain_stats.items()):
        total = stats['total']
        valid = stats['valid']
        rate = (valid / total * 100) if total > 0 else 0
        compliance[domain] = {
            'total': total,
            'valid': valid,
            'invalid': total - valid,
            'rate': round(rate, 2)
        }
    
    return compliance

def populate_template(template, metrics, domain_compliance, validation_date):
    """Populate template with calculated metrics."""
    content = template
    
    # Overall statistics
    content = content.replace('[TO BE POPULATED]', str(metrics['total_files']), 1)
    content = content.replace('[TO BE POPULATED]', str(metrics['valid_files']), 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['valid_files']}/{metrics['total_files']}", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['success_rate']}%", 1)
    content = content.replace('[TO BE POPULATED]', str(metrics['invalid_files']), 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['invalid_files']}/{metrics['total_files']}", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['success_rate']}%", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['improvement_from_phase2']}%", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['improvement_from_baseline']}%", 1)
    
    # Validation date
    content = content.replace('[TO BE POPULATED]', validation_date, 1)
    
    # Phase comparison
    content = content.replace('[TO BE POPULATED]', str(metrics['total_files']), 1)
    content = content.replace('[TO BE POPULATED]', str(metrics['valid_files']), 1)
    content = content.replace('[TO BE POPULATED]', str(metrics['invalid_files']), 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['success_rate']}%", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['improvement_from_phase2']}%", 1)
    
    # Domain compliance table
    domain_table_rows = []
    for domain, stats in sorted(domain_compliance.items()):
        domain_table_rows.append(
            f"| **{domain}** | {stats['total']} | {stats['valid']} | "
            f"{stats['invalid']} | {stats['rate']}% |"
        )
    
    # Replace domain table placeholder
    domain_table_placeholder = "| **[Other Domains]** | [TO BE POPULATED] | [TO BE POPULATED] | [TO BE POPULATED] | [TO BE POPULATED]% |"
    if domain_table_placeholder in content:
        content = content.replace(domain_table_placeholder, '\n'.join(domain_table_rows))
    
    # Final metrics
    content = content.replace('[TO BE POPULATED]', f"{metrics['success_rate']}%", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['valid_files']}/{metrics['total_files']}", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['improvement_from_baseline']}%", 1)
    content = content.replace('[TO BE POPULATED]', f"{metrics['success_rate']}%", 1)
    
    return content

def main():
    parser = argparse.ArgumentParser(description='Populate validation report from JSON results')
    parser.add_argument('--json', required=True, help='Path to validation JSON report')
    parser.add_argument('--template', required=True, help='Path to validation report template')
    parser.add_argument('--output', required=True, help='Path to output populated report')
    
    args = parser.parse_args()
    
    # Load data
    report = load_json_report(args.json)
    template = load_template(args.template)
    
    # Calculate metrics
    metrics = calculate_metrics(report)
    domain_compliance = calculate_domain_compliance(report)
    validation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Populate template
    populated = populate_template(template, metrics, domain_compliance, validation_date)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(populated)
    
    print(f"✅ Validation report populated: {args.output}")
    print(f"   Total files: {metrics['total_files']}")
    print(f"   Valid files: {metrics['valid_files']} ({metrics['success_rate']}%)")
    print(f"   Invalid files: {metrics['invalid_files']}")
    print(f"   Improvement from Phase 2: +{metrics['improvement_from_phase2']}%")
    print(f"   Improvement from baseline: +{metrics['improvement_from_baseline']}%")

if __name__ == '__main__':
    main()

