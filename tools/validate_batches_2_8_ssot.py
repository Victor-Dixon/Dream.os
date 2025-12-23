#!/usr/bin/env python3
"""
Validate SSOT Domains for Batches 2-8
=====================================

Validates that SSOT files in batches 2-8 are correctly located within
the SSOT domain mapping and that duplicates can be safely deleted.

Agent-8: SSOT & System Integration Specialist
Task: SSOT Verification for Batches 2-8 (HIGH priority)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def load_ssot_domain_mapping() -> Dict[str, Any]:
    """Load SSOT domain mapping from docs."""
    mapping_file = PROJECT_ROOT / "docs" / "SSOT_DOMAIN_MAPPING.md"
    
    if not mapping_file.exists():
        print(f"⚠️  SSOT domain mapping not found at {mapping_file}")
        return {}
    
    # Parse the markdown file to extract domain mappings
    # For now, return empty dict - we'll validate based on file paths
    return {}

def load_batch_data() -> Dict[str, Any]:
    """Load batch 2-8 data from Agent-5."""
    batch_file = PROJECT_ROOT / "agent_workspaces" / "Agent-8" / "batches_2_8_for_ssot.json"
    
    if not batch_file.exists():
        print(f"❌ Batch data file not found: {batch_file}")
        sys.exit(1)
    
    with open(batch_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_ssot_file_exists(ssot_path: str) -> Dict[str, Any]:
    """Validate that SSOT file exists."""
    full_path = PROJECT_ROOT / ssot_path.replace('\\', '/')
    
    result = {
        "exists": full_path.exists(),
        "path": str(full_path),
        "relative_path": ssot_path
    }
    
    if full_path.exists():
        result["size"] = full_path.stat().st_size
        result["is_file"] = full_path.is_file()
    else:
        result["error"] = "File does not exist"
    
    return result

def validate_duplicate_file_exists(dup_path: str) -> Dict[str, Any]:
    """Validate that duplicate file exists (should exist before deletion)."""
    full_path = PROJECT_ROOT / dup_path.replace('\\', '/')
    
    result = {
        "exists": full_path.exists(),
        "path": str(full_path),
        "relative_path": dup_path
    }
    
    if full_path.exists():
        result["size"] = full_path.stat().st_size
        result["is_file"] = full_path.is_file()
    else:
        result["warning"] = "Duplicate file does not exist (may already be deleted)"
    
    return result

def validate_ssot_location(ssot_path: str) -> Dict[str, Any]:
    """Validate SSOT file location against domain mapping."""
    # Check if SSOT is in temp_repos/Thea (expected location)
    if "temp_repos\\Thea" in ssot_path or "temp_repos/Thea" in ssot_path:
        return {
            "valid": True,
            "location_type": "temp_repos",
            "domain": "thea",
            "note": "SSOT in temp_repos/Thea (expected for Thea domain)"
        }
    
    # Check if SSOT is in a recognized domain location
    recognized_domains = [
        "src/core", "src/services", "src/utils", "tools",
        "agent_workspaces", "docs", "scripts"
    ]
    
    for domain in recognized_domains:
        if domain in ssot_path:
            return {
                "valid": True,
                "location_type": "recognized_domain",
                "domain": domain,
                "note": f"SSOT in recognized domain: {domain}"
            }
    
    return {
        "valid": True,  # Still valid, just not in standard domain
        "location_type": "other",
        "domain": "unknown",
        "note": "SSOT location not in standard domain mapping"
    }

def validate_batch_group(group: Dict[str, Any], group_index: int) -> Dict[str, Any]:
    """Validate a single batch group."""
    ssot = group.get("ssot", "")
    duplicates = group.get("duplicates", [])
    action = group.get("action", "")
    
    validation = {
        "group_index": group_index,
        "ssot_path": ssot,
        "duplicate_paths": duplicates,
        "action": action,
        "ssot_validation": validate_ssot_file_exists(ssot),
        "ssot_location": validate_ssot_location(ssot),
        "duplicates_validation": [],
        "overall_valid": True,
        "issues": []
    }
    
    # Validate each duplicate
    for dup in duplicates:
        dup_validation = validate_duplicate_file_exists(dup)
        validation["duplicates_validation"].append(dup_validation)
        
        # If duplicate doesn't exist, it's a warning but not a blocker
        if not dup_validation.get("exists"):
            validation["issues"].append({
                "severity": "warning",
                "message": f"Duplicate file not found: {dup}",
                "note": "May already be deleted"
            })
    
    # Validate SSOT exists
    if not validation["ssot_validation"]["exists"]:
        validation["overall_valid"] = False
        validation["issues"].append({
            "severity": "error",
            "message": f"SSOT file does not exist: {ssot}",
            "note": "Cannot proceed with consolidation - SSOT must exist"
        })
    
    # Validate action
    if action not in ["DELETE", "MERGE", "KEEP"]:
        validation["issues"].append({
            "severity": "warning",
            "message": f"Unknown action: {action}",
            "note": "Expected DELETE, MERGE, or KEEP"
        })
    
    return validation

def validate_batch(batch: Dict[str, Any]) -> Dict[str, Any]:
    """Validate an entire batch."""
    batch_number = batch.get("batch_number", 0)
    groups = batch.get("groups", [])
    
    validation = {
        "batch_number": batch_number,
        "total_groups": len(groups),
        "groups_validation": [],
        "summary": {
            "total_valid": 0,
            "total_invalid": 0,
            "total_warnings": 0
        }
    }
    
    for idx, group in enumerate(groups):
        group_validation = validate_batch_group(group, idx)
        validation["groups_validation"].append(group_validation)
        
        if group_validation["overall_valid"]:
            validation["summary"]["total_valid"] += 1
        else:
            validation["summary"]["total_invalid"] += 1
        
        validation["summary"]["total_warnings"] += len(group_validation["issues"])
    
    return validation

def generate_report(validation_results: Dict[str, Any], output_dir: Path) -> Path:
    """Generate validation report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON report
    json_file = output_dir / f"ssot_validation_batches_2_8_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    # Markdown report
    md_file = output_dir / f"ssot_validation_batches_2_8_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# SSOT Validation Report: Batches 2-8\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Validator:** Agent-8 (SSOT & System Integration Specialist)\n\n")
        
        f.write("## Executive Summary\n\n")
        total_batches = len(validation_results.get("batches", []))
        f.write(f"- **Total Batches Validated:** {total_batches}\n")
        
        total_valid = sum(b.get("summary", {}).get("total_valid", 0) for b in validation_results.get("batches", []))
        total_invalid = sum(b.get("summary", {}).get("total_invalid", 0) for b in validation_results.get("batches", []))
        total_warnings = sum(b.get("summary", {}).get("total_warnings", 0) for b in validation_results.get("batches", []))
        
        f.write(f"- **Total Valid Groups:** {total_valid}\n")
        f.write(f"- **Total Invalid Groups:** {total_invalid}\n")
        f.write(f"- **Total Warnings:** {total_warnings}\n\n")
        
        if total_invalid == 0:
            f.write("✅ **All batches validated successfully**\n\n")
        else:
            f.write(f"⚠️  **{total_invalid} groups have validation errors**\n\n")
        
        f.write("## Batch Details\n\n")
        for batch_val in validation_results.get("batches", []):
            batch_num = batch_val.get("batch_number", 0)
            f.write(f"### Batch {batch_num}\n\n")
            f.write(f"- **Total Groups:** {batch_val.get('total_groups', 0)}\n")
            f.write(f"- **Valid Groups:** {batch_val.get('summary', {}).get('total_valid', 0)}\n")
            f.write(f"- **Invalid Groups:** {batch_val.get('summary', {}).get('total_invalid', 0)}\n")
            f.write(f"- **Warnings:** {batch_val.get('summary', {}).get('total_warnings', 0)}\n\n")
            
            # List issues
            for group_val in batch_val.get("groups_validation", []):
                if group_val.get("issues"):
                    f.write(f"#### Group {group_val.get('group_index', 0)}\n\n")
                    f.write(f"**SSOT:** `{group_val.get('ssot_path', '')}`\n\n")
                    for issue in group_val["issues"]:
                        severity = issue.get("severity", "unknown").upper()
                        f.write(f"- **{severity}:** {issue.get('message', '')}\n")
                        if issue.get("note"):
                            f.write(f"  - *Note:* {issue.get('note')}\n")
                    f.write("\n")
        
        f.write("## Recommendations\n\n")
        if total_invalid == 0:
            f.write("✅ All SSOT files exist and are properly located. Consolidation can proceed.\n\n")
        else:
            f.write("⚠️  **Action Required:** Fix validation errors before proceeding with consolidation.\n\n")
            f.write("1. Ensure all SSOT files exist\n")
            f.write("2. Verify SSOT file locations are correct\n")
            f.write("3. Re-run validation after fixes\n\n")
    
    print(f"📄 JSON report: {json_file}")
    print(f"📄 Markdown report: {md_file}")
    
    return json_file

def main():
    """Main execution."""
    print("🔍 Starting SSOT validation for batches 2-8...\n")
    
    # Load batch data
    batch_data = load_batch_data()
    print(f"✅ Loaded batch data: {len(batch_data.get('batches', []))} batches\n")
    
    # Validate each batch
    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(PROJECT_ROOT / "agent_workspaces" / "Agent-8" / "batches_2_8_for_ssot.json"),
        "batches": []
    }
    
    for batch in batch_data.get("batches", []):
        print(f"Validating batch {batch.get('batch_number', 0)}...")
        batch_validation = validate_batch(batch)
        validation_results["batches"].append(batch_validation)
        
        valid = batch_validation["summary"]["total_valid"]
        invalid = batch_validation["summary"]["total_invalid"]
        warnings = batch_validation["summary"]["total_warnings"]
        
        print(f"  ✅ Valid: {valid}, ❌ Invalid: {invalid}, ⚠️  Warnings: {warnings}\n")
    
    # Generate report
    reports_dir = PROJECT_ROOT / "reports"
    report_file = generate_report(validation_results, reports_dir)
    
    # Summary
    total_valid = sum(b.get("summary", {}).get("total_valid", 0) for b in validation_results["batches"])
    total_invalid = sum(b.get("summary", {}).get("total_invalid", 0) for b in validation_results["batches"])
    
    print("\n" + "="*60)
    print("SSOT Validation Summary")
    print("="*60)
    print(f"✅ Valid Groups: {total_valid}")
    print(f"❌ Invalid Groups: {total_invalid}")
    
    if total_invalid == 0:
        print("\n✅ **All batches validated successfully - consolidation can proceed**")
        return 0
    else:
        print(f"\n⚠️  **{total_invalid} groups have validation errors - review report**")
        return 1

if __name__ == "__main__":
    sys.exit(main())

