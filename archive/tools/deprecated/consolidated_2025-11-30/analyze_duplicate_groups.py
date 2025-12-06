#!/usr/bin/env python3
"""
Analyze Duplicate Groups - Agent-3
====================================

Categorizes duplicate groups from integration_issues_report.json
and identifies critical duplicates for resolution.

Usage:
    python tools/analyze_duplicate_groups.py [report_file]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

def load_report(report_file: str = "integration_issues_report.json") -> Dict:
    """Load integration issues report."""
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Report file not found: {report_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)

def categorize_duplicates(duplicates: Dict[str, List[str]]) -> Dict[str, List]:
    """Categorize duplicate groups by type."""
    categories = {
        'content_duplicates': [],  # Same hash (identical content)
        'name_duplicates': [],     # Same filename, different content
        'critical': [],            # Blocking integration
        'non_critical': []         # Can be deferred (e.g., __init__.py)
    }
    
    for hash_val, paths in duplicates.items():
        # Check if same filename
        filenames = [Path(p).name for p in paths]
        unique_filenames = set(filenames)
        
        # Content duplicates (same hash = identical content)
        if len(unique_filenames) == 1:
            # Same filename and same content = exact duplicate
            filename = filenames[0]
            if filename == '__init__.py':
                categories['non_critical'].append({
                    'hash': hash_val,
                    'paths': paths,
                    'type': 'content_duplicate',
                    'filename': filename
                })
            else:
                categories['content_duplicates'].append({
                    'hash': hash_val,
                    'paths': paths,
                    'type': 'content_duplicate',
                    'filename': filename
                })
        else:
            # Different filenames with same content = name duplicates
            categories['name_duplicates'].append({
                'hash': hash_val,
                'paths': paths,
                'type': 'name_duplicate',
                'filenames': list(unique_filenames)
            })
    
    return categories

def identify_critical_duplicates(categories: Dict) -> List:
    """Identify critical duplicates blocking integration."""
    critical = []
    
    # Check for duplicates in critical paths
    critical_paths = [
        'src/',
        'core/',
        'services/',
        'tools/',
        'config',
        'main',
        'setup',
        'requirements'
    ]
    
    for category_name, items in categories.items():
        if category_name == 'non_critical':
            continue
            
        for item in items:
            paths = item['paths']
            # Check if any path is in critical location
            for path in paths:
                path_lower = path.lower()
                if any(critical_path in path_lower for critical_path in critical_paths):
                    # Check if not __init__.py (those are usually non-critical)
                    if not path.endswith('__init__.py'):
                        critical.append(item)
                        break
    
    return critical

def generate_analysis_report(report_data: Dict, output_file: str = "duplicate_analysis_report.md") -> str:
    """Generate analysis report."""
    if not report_data:
        return "No data to analyze"
    
    result = report_data[0] if isinstance(report_data, list) else report_data
    duplicate_analysis = result.get('duplicate_analysis', {})
    duplicates = duplicate_analysis.get('duplicates', {})
    
    if not duplicates:
        return "No duplicates found"
    
    # Categorize duplicates
    categories = categorize_duplicates(duplicates)
    critical = identify_critical_duplicates(categories)
    
    # Generate report
    report = f"""# Duplicate Groups Analysis Report

**Date**: 2025-11-27  
**Agent**: Agent-3 (Infrastructure & DevOps Specialist)  
**Repository**: {result.get('repo', 'Unknown')}

---

## 📊 **SUMMARY**

- **Total Duplicate Groups**: {duplicate_analysis.get('duplicate_groups', 0)}
- **Total Duplicate Files**: {duplicate_analysis.get('duplicate_files', 0)}
- **Content Duplicates**: {len(categories['content_duplicates'])}
- **Name Duplicates**: {len(categories['name_duplicates'])}
- **Critical Duplicates**: {len(critical)}
- **Non-Critical Duplicates**: {len(categories['non_critical'])}

---

## 🚨 **CRITICAL DUPLICATES** (Blocking Integration)

**Count**: {len(critical)}

### **Top 20 Critical Duplicates**:

"""
    
    for i, item in enumerate(critical[:20], 1):
        paths = item['paths']
        report += f"\n{i}. **{Path(paths[0]).name}** ({len(paths)} copies)\n"
        for path in paths[:5]:  # Show first 5 paths
            report += f"   - `{path}`\n"
        if len(paths) > 5:
            report += f"   - ... and {len(paths) - 5} more\n"
    
    if len(critical) > 20:
        report += f"\n... and {len(critical) - 20} more critical duplicates\n"
    
    report += f"""

---

## 📋 **CONTENT DUPLICATES** (Safe to Remove)

**Count**: {len(categories['content_duplicates'])}

These are identical files (same hash). Safe to remove duplicates, keeping one copy.

### **Top 20 Content Duplicates**:

"""
    
    for i, item in enumerate(categories['content_duplicates'][:20], 1):
        paths = item['paths']
        filename = item['filename']
        report += f"\n{i}. **{filename}** ({len(paths)} copies)\n"
        report += f"   - Keep: `{paths[0]}`\n"
        report += f"   - Remove: {', '.join([f'`{p}`' for p in paths[1:]])}\n"
    
    if len(categories['content_duplicates']) > 20:
        report += f"\n... and {len(categories['content_duplicates']) - 20} more content duplicates\n"
    
    report += f"""

---

## 🔍 **NAME DUPLICATES** (Need Merge Analysis)

**Count**: {len(categories['name_duplicates'])}

These have same content but different filenames. Need merge analysis using `merge_duplicate_file_functionality.py`.

### **Top 20 Name Duplicates**:

"""
    
    for i, item in enumerate(categories['name_duplicates'][:20], 1):
        paths = item['paths']
        filenames = item['filenames']
        report += f"\n{i}. **Same content, different names** ({len(paths)} files)\n"
        report += f"   - Filenames: {', '.join(filenames)}\n"
        for path in paths[:3]:  # Show first 3 paths
            report += f"   - `{path}`\n"
        if len(paths) > 3:
            report += f"   - ... and {len(paths) - 3} more\n"
    
    if len(categories['name_duplicates']) > 20:
        report += f"\n... and {len(categories['name_duplicates']) - 20} more name duplicates\n"
    
    report += f"""

---

## ✅ **NON-CRITICAL DUPLICATES** (Can Be Deferred)

**Count**: {len(categories['non_critical'])}

These are typically `__init__.py` files or other non-critical duplicates.

---

## 🎯 **RESOLUTION PRIORITY**

1. **HIGH**: Resolve {len(critical)} critical duplicates (blocking integration)
2. **MEDIUM**: Remove {len(categories['content_duplicates'])} content duplicates (safe removal)
3. **LOW**: Analyze {len(categories['name_duplicates'])} name duplicates (merge analysis needed)
4. **DEFER**: {len(categories['non_critical'])} non-critical duplicates

---

## 🛠️ **NEXT STEPS**

1. Use `merge_duplicate_file_functionality.py` to analyze critical name duplicates
2. Remove content duplicates (keep one copy, remove others)
3. Verify resolution with `check_integration_issues.py`
4. **Goal**: 0 issues (Agent-3 standard)

---

**Status**: ⚡ **ANALYSIS COMPLETE - READY FOR RESOLUTION**
"""
    
    return report

def main():
    """Main execution."""
    report_file = sys.argv[1] if len(sys.argv) > 1 else "integration_issues_report.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "duplicate_analysis_report.md"
    
    print("=" * 60)
    print("Duplicate Groups Analyzer - Agent-3")
    print("=" * 60)
    print(f"\nLoading report: {report_file}...")
    
    report_data = load_report(report_file)
    
    print("Analyzing duplicate groups...")
    report = generate_analysis_report(report_data, output_file)
    
    # Save report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete!")
    print(f"📄 Report saved to: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

