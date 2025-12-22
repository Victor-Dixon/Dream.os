#!/usr/bin/env python3
"""
Merge tools_v2 subdirectories into tools
========================================

Merges contents of categories/, adapters/, and core/ from tools_v2 into tools.

Author: Agent-3
Date: 2025-12-22
"""

import shutil
from pathlib import Path
import re


def merge_subdirectories():
    """Merge subdirectories from tools_v2 into tools."""
    print("=" * 70)
    print("🔄 MERGING tools_v2 SUBDIRECTORIES INTO tools")
    print("=" * 70)
    print()
    
    repo_root = Path(__file__).parent.parent
    tools_v2_dir = repo_root / "tools_v2"
    tools_dir = repo_root / "tools"
    
    subdirs = ["categories", "adapters", "core"]
    
    for subdir_name in subdirs:
        source_dir = tools_v2_dir / subdir_name
        dest_dir = tools_dir / subdir_name
        
        if not source_dir.exists():
            print(f"⚠️  {subdir_name}/ not found in tools_v2")
            continue
        
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📦 Merging {subdir_name}/...")
        
        moved_count = 0
        skipped_count = 0
        
        for item in source_dir.iterdir():
            if item.name in ['__pycache__', '.pytest_cache']:
                continue
            
            dest = dest_dir / item.name
            
            if dest.exists():
                print(f"   ⚠️  Skipping {item.name} (already exists)")
                skipped_count += 1
                continue
            
            try:
                if item.is_dir():
                    shutil.copytree(item, dest)
                    print(f"   ✅ Moved directory: {item.name}")
                else:
                    shutil.copy2(item, dest)
                    print(f"   ✅ Moved file: {item.name}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {item.name}: {e}")
        
        print(f"   ✅ Moved {moved_count} items, skipped {skipped_count}")
        print()
    
    # Update imports in merged files
    print("🔧 Updating imports in merged files...")
    
    import_patterns = [
        (r'from tools_v2\.', 'from tools.'),
        (r'import tools_v2\.', 'import tools.'),
        (r'from tools_v2 import', 'from tools import'),
        (r'import tools_v2', 'import tools'),
    ]
    
    updated_count = 0
    for subdir_name in subdirs:
        dest_dir = tools_dir / subdir_name
        if not dest_dir.exists():
            continue
        
        for file_path in dest_dir.rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                for pattern, replacement in import_patterns:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    updated_count += 1
            except Exception:
                pass
    
    print(f"   ✅ Updated {updated_count} files")
    print()
    print("✅ Directory merge complete!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(merge_subdirectories())

