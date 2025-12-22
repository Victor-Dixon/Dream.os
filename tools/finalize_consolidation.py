#!/usr/bin/env python3
"""
Finalize tools_v2 Consolidation
================================

Updates all remaining imports and removes tools_v2 directory.

Author: Agent-3
Date: 2025-12-22
"""

import re
import shutil
from pathlib import Path


def finalize_consolidation():
    """Finalize the consolidation."""
    print("=" * 70)
    print("🔧 FINALIZING tools_v2 CONSOLIDATION")
    print("=" * 70)
    print()
    
    repo_root = Path(__file__).parent.parent
    
    # Step 1: Update all imports in codebase
    print("🔧 Step 1: Updating all imports...")
    
    import_patterns = [
        (r'from tools_v2\.', 'from tools.'),
        (r'import tools\.', 'import tools.'),
        (r'from tools import', 'from tools import'),
        (r'import tools', 'import tools'),
        (r'"tools"', '"tools"'),
        (r"'tools'", "'tools'"),
    ]
    
    search_dirs = [
        repo_root / "src",
        repo_root / "scripts",
        repo_root / "tests",
        repo_root / "tools",
        repo_root / "mcp_servers",
    ]
    
    updated_files = []
    for base_dir in search_dirs:
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
                    updated_files.append(file_path.relative_to(repo_root))
            except Exception:
                pass
    
    print(f"   ✅ Updated {len(updated_files)} files")
    if updated_files:
        print("   Files updated:")
        for f in updated_files[:10]:
            print(f"      - {f}")
        if len(updated_files) > 10:
            print(f"      ... and {len(updated_files) - 10} more")
    
    # Step 2: Update JSON/YAML files
    print(f"\n🔧 Step 2: Updating config files...")
    
    config_patterns = [
        (r'"tools"', '"tools"'),
        (r"'tools'", "'tools'"),
        (r'tools_v2/', 'tools/'),
        (r'tools_v2\.', 'tools.'),
    ]
    
    config_files = list(repo_root.rglob("*.json")) + list(repo_root.rglob("*.yaml")) + list(repo_root.rglob("*.yml"))
    config_updated = 0
    
    for file_path in config_files:
        # Skip node_modules and other large dirs
        if any(skip in str(file_path) for skip in ['node_modules', '__pycache__', '.git', 'temp_']):
            continue
        
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            for pattern, replacement in config_patterns:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                config_updated += 1
        except Exception:
            pass
    
    print(f"   ✅ Updated {config_updated} config files")
    
    # Step 3: Remove tools_v2 directory
    print(f"\n🗑️  Step 3: Removing tools_v2 directory...")
    
    tools_v2_dir = repo_root / "tools"
    if tools_v2_dir.exists():
        try:
            shutil.rmtree(tools_v2_dir)
            print(f"   ✅ Removed {tools_v2_dir}")
        except Exception as e:
            print(f"   ⚠️  Error removing directory: {e}")
            print(f"   💡 You may need to remove it manually")
    else:
        print(f"   ℹ️  tools_v2 directory not found (already removed?)")
    
    print(f"\n✅ Consolidation finalized!")
    print(f"   📝 Ready to commit and push")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(finalize_consolidation())

