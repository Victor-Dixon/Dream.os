#!/usr/bin/env python3
"""
Consolidate tools_v2 into tools
================================

Moves all files from tools_v2/ into tools/ and updates imports.

Author: Agent-3
Date: 2025-12-22
"""

import shutil
from pathlib import Path
import re


def consolidate_tools_v2():
    """Consolidate tools_v2 directory into tools."""
    print("=" * 70)
    print("🔄 CONSOLIDATING tools_v2 INTO tools")
    print("=" * 70)
    print()
    
    repo_root = Path(__file__).parent.parent
    tools_v2_dir = repo_root / "tools_v2"
    tools_dir = repo_root / "tools"
    
    if not tools_v2_dir.exists():
        print("❌ tools_v2 directory not found")
        return 1
    
    print(f"📁 Source: {tools_v2_dir}")
    print(f"📁 Destination: {tools_dir}")
    print()
    
    # Step 1: Move files from tools_v2 to tools
    print("📦 Step 1: Moving files...")
    
    moved_count = 0
    skipped_count = 0
    
    # Move all files and directories
    for item in tools_v2_dir.iterdir():
        if item.name in ['.git', '__pycache__', '.pytest_cache']:
            continue
        
        dest = tools_dir / item.name
        
        if dest.exists():
            print(f"   ⚠️  Skipping {item.name} (already exists in tools/)")
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
    
    print(f"\n   ✅ Moved {moved_count} items")
    if skipped_count > 0:
        print(f"   ⚠️  Skipped {skipped_count} items (already exist)")
    
    # Step 2: Update imports in moved files
    print(f"\n🔧 Step 2: Updating imports...")
    
    import_patterns = [
        (r'from tools_v2\.', 'from tools.'),
        (r'import tools\.', 'import tools.'),
        (r'from tools import', 'from tools import'),
        (r'import tools', 'import tools'),
    ]
    
    updated_files = 0
    for file_path in tools_dir.rglob("*.py"):
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            for pattern, replacement in import_patterns:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                print(f"   ✅ Updated imports in: {file_path.relative_to(repo_root)}")
                updated_files += 1
        except Exception as e:
            print(f"   ⚠️  Error updating {file_path}: {e}")
    
    print(f"\n   ✅ Updated {updated_files} files")
    
    # Step 3: Update imports in other files that reference tools_v2
    print(f"\n🔧 Step 3: Updating imports in codebase...")
    
    codebase_files = [
        repo_root / "src",
        repo_root / "scripts",
        repo_root / "tests",
    ]
    
    codebase_updated = 0
    for base_dir in codebase_files:
        if not base_dir.exists():
            continue
        
        for file_path in base_dir.rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                for pattern, replacement in import_patterns:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    print(f"   ✅ Updated: {file_path.relative_to(repo_root)}")
                    codebase_updated += 1
            except Exception:
                pass
    
    print(f"\n   ✅ Updated {codebase_updated} files in codebase")
    
    print(f"\n✅ Consolidation complete!")
    print(f"   📝 Next: Review changes and commit")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(consolidate_tools_v2())

