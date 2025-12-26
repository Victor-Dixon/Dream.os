#!/usr/bin/env python3
"""
Consolidate Duplicate Documentation
Identifies and consolidates duplicate documentation files
"""

import json
from pathlib import Path
from datetime import datetime

AUDIT_REPORT = Path("reports/documentation_sprawl_audit.json")

def load_audit_report():
    """Load the documentation audit report."""
    if not AUDIT_REPORT.exists():
        print(f"❌ Audit report not found: {AUDIT_REPORT}")
        print("   Run documentation_sprawl_audit.py first")
        return None
    
    return json.loads(AUDIT_REPORT.read_text())

def consolidate_duplicates():
    """Consolidate duplicate documentation files."""
    print("🔄 Starting duplicate documentation consolidation...")
    
    audit_data = load_audit_report()
    if not audit_data:
        return
    
    duplicates = audit_data.get("duplicate_files", {}).get("pairs", [])
    
    if not duplicates:
        print("✅ No duplicates found to consolidate")
        return
    
    print(f"📊 Found {len(duplicates)} duplicate pairs")
    
    consolidation_plan = []
    consolidated_count = 0
    
    for pair in duplicates[:20]:  # Process top 20 pairs
        file1 = Path(pair["file1"])
        file2 = Path(pair["file2"])
        
        if not file1.exists() or not file2.exists():
            continue
        
        # Determine which file to keep (prefer shorter path, then smaller file)
        if len(str(file1)) < len(str(file2)):
            keep_file = file1
            remove_file = file2
        elif len(str(file2)) < len(str(file1)):
            keep_file = file2
            remove_file = file1
        else:
            # Same path length, prefer smaller file
            if file1.stat().st_size <= file2.stat().st_size:
                keep_file = file1
                remove_file = file2
            else:
                keep_file = file2
                remove_file = file1
        
        consolidation_plan.append({
            "keep": str(keep_file),
            "remove": str(remove_file),
            "reason": "Duplicate content detected",
        })
    
    # Save consolidation plan
    plan_path = Path("reports/duplicate_documentation_consolidation_plan.json")
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps({
        "consolidation_date": datetime.now().isoformat(),
        "total_pairs": len(duplicates),
        "planned_consolidations": len(consolidation_plan),
        "plan": consolidation_plan,
    }, indent=2))
    
    # Generate markdown report
    report_path = Path("reports/duplicate_documentation_consolidation_report.md")
    with report_path.open("w", encoding="utf-8") as f:
        f.write("# Duplicate Documentation Consolidation Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Duplicate Pairs:** {len(duplicates)}\n\n")
        f.write(f"**Planned Consolidations:** {len(consolidation_plan)}\n\n")
        f.write("## Consolidation Plan\n\n")
        f.write("| Keep File | Remove File | Reason |\n")
        f.write("|-----------|-------------|--------|\n")
        for item in consolidation_plan:
            f.write(f"| `{item['keep']}` | `{item['remove']}` | {item['reason']} |\n")
        f.write("\n## Next Steps\n\n")
        f.write("1. Review consolidation plan\n")
        f.write("2. Execute consolidation (manual or automated)\n")
        f.write("3. Update all references to removed files\n")
        f.write("4. Verify no broken links\n")
    
    print(f"\n✅ Consolidation plan created!")
    print(f"   📄 Plan: {plan_path}")
    print(f"   📋 Report: {report_path}")
    print(f"   📊 Planned consolidations: {len(consolidation_plan)}")
    print(f"\n⚠️  Review plan before executing consolidations")

if __name__ == "__main__":
    consolidate_duplicates()

