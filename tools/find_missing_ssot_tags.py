#!/usr/bin/env python3
"""
Find files missing SSOT tags (<!-- SSOT Domain: domain_name -->).
Focuses on .py and .md files in src, tools, and scripts.

<!-- SSOT Domain: tools -->
"""

import os
from pathlib import Path

def find_missing_tags(root_dir, search_dirs):
    missing_files = []
    tag_pattern = "SSOT Domain:"
    
    # Exclude cache directories and generated files
    excluded_dirs = {'__pycache__', '.git', 'node_modules', '.next', '.venv', 'venv', 'env', '.pytest_cache'}
    excluded_patterns = {'.pyc', '.pyo', '.pyd'}
    
    for search_dir in search_dirs:
        dir_path = Path(root_dir) / search_dir
        if not dir_path.exists():
            continue
            
        for file_path in dir_path.rglob("*"):
            # Skip excluded directories
            if any(excluded_dir in file_path.parts for excluded_dir in excluded_dirs):
                continue
            
            # Skip excluded file patterns
            if file_path.suffix in excluded_patterns:
                continue
            
            if file_path.suffix in [".py", ".md"]:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if tag_pattern not in content:
                        missing_files.append(str(file_path.relative_to(root_dir)))
                except Exception:
                    # Skip files that can't be read
                    continue
                    
    return missing_files

if __name__ == "__main__":
    workspaces = [
        ("D:\\Agent_Cellphone_V2_Repository", ["src", "tools", "scripts"]),
        ("D:\\websites", ["tools", "sites", "ops"])
    ]
    
    all_missing = []
    for root, search_dirs in workspaces:
        missing = find_missing_tags(root, search_dirs)
        # Add root prefix to make paths absolute or distinguishable
        all_missing.extend([f"{root}\\{m}" for m in missing])
    
    print(f"Total files missing SSOT tags: {len(all_missing)}")
    
    # Save the list
    output_path = Path("agent_workspaces/Agent-6/MISSING_SSOT_TAGS_LIST.txt")
    output_path.write_text("\n".join(all_missing), encoding='utf-8')
    print(f"Saved list to {output_path}")

