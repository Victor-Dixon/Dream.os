#!/usr/bin/env python3
"""
Identify SSOT Batches Needing Work
===================================

Scans Priority 1 SSOT batches to identify which batches actually need tagging work,
skipping batches where files are already tagged.

Author: Agent-4 (Captain)
Date: 2025-12-30
V2 Compliant: Yes (<300 lines)

<!-- SSOT Domain: tools -->
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple

SSOT_TAG_PATTERN = re.compile(r'<!--\s*SSOT\s+Domain:\s*(\w+)\s*-->', re.IGNORECASE)


def file_has_ssot_tag(file_path: Path) -> Tuple[bool, str | None]:
    """Check if file has SSOT tag and return domain if found."""
    try:
        content = file_path.read_text(encoding='utf-8')
        match = SSOT_TAG_PATTERN.search(content)
        if match:
            return True, match.group(1)
        return False, None
    except Exception:
        return False, None


def scan_batch_for_work(batch_info: Dict[str, Any], workspace_root: Path) -> Dict[str, Any]:
    """Scan a batch to identify files needing work."""
    batch_id = batch_info.get('batch_id', 'unknown')
    files = batch_info.get('files', [])
    domain = batch_info.get('domain', 'unknown')
    
    needs_work = []
    already_tagged = []
    missing_files = []
    
    for file_info in files:
        # Handle both string paths and dict with file_path key
        if isinstance(file_info, str):
            file_path_str = file_info
        else:
            file_path_str = file_info.get('file_path', '')
        
        # Normalize path separators
        file_path_str = file_path_str.replace('\\', '/')
        file_path = workspace_root / file_path_str if not Path(file_path_str).is_absolute() else Path(file_path_str)
        
        if not file_path.exists():
            missing_files.append(file_path_str)
            continue
        
        has_tag, tag_domain = file_has_ssot_tag(file_path)
        if has_tag:
            already_tagged.append({
                'file': file_path_str,
                'domain': tag_domain
            })
        else:
            needs_work.append(file_path_str)
    
    return {
        'batch_id': batch_id,
        'domain': domain,
        'total_files': len(files),
        'needs_work': needs_work,
        'already_tagged': already_tagged,
        'missing_files': missing_files,
        'work_count': len(needs_work),
        'tagged_count': len(already_tagged),
        'needs_work': len(needs_work) > 0
    }


def identify_batches_needing_work(batch_assignments_file: str = "reports/ssot/ssot_batch_assignments_latest.json") -> Dict[str, Any]:
    """Identify which Priority 1 batches actually need work."""
    workspace_root = Path("agent_workspaces").parent if Path("agent_workspaces").exists() else Path(".")
    
    try:
        with open(batch_assignments_file, 'r', encoding='utf-8') as f:
            assignments = json.load(f)
    except FileNotFoundError:
        return {
            'error': f'Batch assignments file not found: {batch_assignments_file}',
            'batches_needing_work': [],
            'batches_complete': []
        }
    
    priority_1_batches = assignments.get('batches', {}).get('priority_1', [])
    
    batches_needing_work = []
    batches_complete = []
    
    for batch in priority_1_batches:
        scan_result = scan_batch_for_work(batch, workspace_root)
        
        if scan_result['work_count'] > 0:
            batches_needing_work.append(scan_result)
        else:
            batches_complete.append(scan_result)
    
    # Sort by work count (most work first)
    batches_needing_work.sort(key=lambda x: x['work_count'], reverse=True)
    
    total_work_files = sum(b['work_count'] for b in batches_needing_work)
    total_tagged_files = sum(b['tagged_count'] for b in batches_complete + batches_needing_work)
    
    return {
        'batches_needing_work': batches_needing_work,
        'batches_complete': batches_complete,
        'summary': {
            'total_batches_scanned': len(priority_1_batches),
            'batches_needing_work': len(batches_needing_work),
            'batches_complete': len(batches_complete),
            'total_files_needing_work': total_work_files,
            'total_files_already_tagged': total_tagged_files,
            'completion_rate': (total_tagged_files / (total_work_files + total_tagged_files) * 100) if (total_work_files + total_tagged_files) > 0 else 0
        }
    }


def main():
    """Main execution."""
    print("🔍 Identifying Priority 1 SSOT batches needing work...\n")
    
    result = identify_batches_needing_work()
    
    if 'error' in result:
        print(f"❌ {result['error']}")
        return
    
    summary = result['summary']
    print(f"📊 Summary:")
    print(f"   Total batches scanned: {summary['total_batches_scanned']}")
    print(f"   Batches needing work: {summary['batches_needing_work']}")
    print(f"   Batches complete: {summary['batches_complete']}")
    print(f"   Files needing work: {summary['total_files_needing_work']}")
    print(f"   Files already tagged: {summary['total_files_already_tagged']}")
    print(f"   Completion rate: {summary['completion_rate']:.1f}%\n")
    
    if result['batches_needing_work']:
        print("✅ Batches needing work (sorted by work count):")
        for batch in result['batches_needing_work'][:10]:  # Show top 10
            print(f"   {batch['batch_id']}: {batch['work_count']} files need work ({batch['domain']} domain)")
    else:
        print("✅ All batches complete!")
    
    # Save results
    output_file = "ssot_batches_needing_work.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()

