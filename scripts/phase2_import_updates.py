#!/usr/bin/env python3
"""
Phase 2: Import Updates Script
==============================

Updates all import statements to use new canonical locations for extracted components.
This script systematically finds and updates imports from the old temp_repos locations
to the new system locations.

Run this script from the repository root.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Import mapping from old paths to new paths
IMPORT_MAPPINGS = {
    # Dreamscape/GUI system
    'from dreamscape.core.memory_system': 'from systems.memory.memory',
    'from dreamscape.gui.components.shared_components': 'from systems.gui.gui.components.shared_components',
    'from dreamscape.core.intelligent_agent_system': 'from systems.ai.intelligent_agent_system',
    'from dreamscape.core.memory_system': 'from systems.memory.memory',

    # Template system
    'from dreamscape.core.templates.prompt_orchestrator': 'from systems.templates.templates.runners.template_runner',
    'from dreamscape.core.templates.template_engine': 'from systems.templates.templates.engine.template_engine',
    'from dreamscape.core.consolidate_template_analyzers': 'from systems.templates.templates.analytics.template_analyzer',

    # Lead scoring system
    'from scrapers': 'from tools.lead_harvesting.scrapers',
}

def find_python_files(directory: str) -> List[str]:
    """Find all Python files in directory recursively."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.venv']]

        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def update_imports_in_file(file_path: str) -> Tuple[int, List[str]]:
    """Update imports in a single file. Returns (updates_made, changed_lines)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changed_lines = []

    for old_import, new_import in IMPORT_MAPPINGS.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(old_import) + r'\b'

        if re.search(pattern, content):
            content = re.sub(pattern, new_import, content)
            changed_lines.append(f"  {old_import} → {new_import}")

    updates_made = 1 if content != original_content else 0

    if updates_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return updates_made, changed_lines

def main():
    """Main update function."""
    print("🔄 Phase 2: Import Updates")
    print("=" * 40)

    # Directories to scan for import updates
    scan_dirs = [
        'systems/gui',
        'systems/memory',
        'systems/templates',
        'tools/lead_scoring',
        'tools/lead_harvesting',
        'tools/code_analysis'
    ]

    total_files_processed = 0
    total_updates_made = 0
    files_updated = []

    for scan_dir in scan_dirs:
        if not os.path.exists(scan_dir):
            print(f"⚠️  Directory not found: {scan_dir}")
            continue

        print(f"\n📁 Scanning {scan_dir}...")

        python_files = find_python_files(scan_dir)

        for file_path in python_files:
            relative_path = os.path.relpath(file_path)
            updates_made, changed_lines = update_imports_in_file(file_path)

            total_files_processed += 1

            if updates_made:
                total_updates_made += 1
                files_updated.append(relative_path)
                print(f"  ✅ Updated: {relative_path}")
                for line in changed_lines:
                    print(f"    {line}")

    # Summary
    print("\n" + "=" * 40)
    print("📊 UPDATE SUMMARY")
    print(f"Files processed: {total_files_processed}")
    print(f"Files updated: {total_updates_made}")
    print(f"Import mappings applied: {len(IMPORT_MAPPINGS)}")

    if files_updated:
        print("\n📝 Updated Files:")
        for file in files_updated:
            print(f"  - {file}")

    print("\n✅ Phase 2: Import updates complete!")
    print("\nNext: Run dependency resolution script")

if __name__ == "__main__":
    main()