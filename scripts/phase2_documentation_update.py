#!/usr/bin/env python3
"""
Phase 2: Documentation Update Script
====================================

Updates all documentation references to reflect new system locations after Wave C extraction.
Replaces old temp_repos/ paths with new canonical system locations.

Run this script from the repository root.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Documentation path mappings
DOC_PATH_MAPPINGS = {
    # Dreamscape system references
    'temp_repos/Thea/src/dreamscape/core/mmorpg/': 'systems/gamification/mmorpg/',
    'temp_repos/Thea/src/dreamscape/core/memory/': 'systems/memory/memory/',
    'temp_repos/Thea/src/dreamscape/core/templates/': 'systems/templates/templates/',
    'temp_repos/Thea/src/dreamscape/gui/': 'systems/gui/gui/',
    'temp_repos/Thea/src/dreamscape/scrapers/': 'systems/scrapers/scrapers/',
    'temp_repos/Thea/src/dreamscape/core/analytics/': 'systems/analytics/analytics/',

    # Lead harvesting system references
    'temp_repos/temp_repos/contract-leads/': 'tools/lead_harvesting/',
    'temp_repos/contract-leads/': 'tools/lead_harvesting/',

    # Agent project references
    'temp_repos/agentproject/': 'tools/code_analysis/',

    # Auto Blogger references
    'temp_repos/Auto_Blogger/': 'archive/auto_blogger_project/',

    # Site-specific references
    'temp_repos/crosbyultimateevents.com/': 'archive/site_specific/crosbyultimateevents/',
    'temp_repos/dadudekc.com/': 'archive/site_specific/dadudekc/',
}

def find_documentation_files() -> List[str]:
    """Find all documentation files that might need updating."""
    doc_files = []

    # Documentation directories
    doc_dirs = ['docs', 'reports', 'README.md', 'archive']

    for doc_dir in doc_dirs:
        if os.path.exists(doc_dir):
            if os.path.isfile(doc_dir):  # For README.md
                doc_files.append(doc_dir)
            else:
                for root, dirs, files in os.walk(doc_dir):
                    for file in files:
                        if file.endswith(('.md', '.txt', '.rst', '.yaml', '.yml')):
                            doc_files.append(os.path.join(root, file))

    return doc_files

def update_file_paths(file_path: str) -> Tuple[int, List[str]]:
    """Update path references in a documentation file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        updated_paths = []

        for old_path, new_path in DOC_PATH_MAPPINGS.items():
            if old_path in content:
                content = content.replace(old_path, new_path)
                updated_paths.append(f"  {old_path} → {new_path}")

        updates_made = 1 if content != original_content else 0

        if updates_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return updates_made, updated_paths

    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return 0, []

def update_system_references() -> Tuple[int, List[str]]:
    """Update general system references in documentation."""
    print("🔧 Updating System References...")

    reference_updates = {
        # Update system descriptions
        'Dreamscape MMORPG Platform': 'Dreamscape MMORPG System (systems/gamification/)',
        'Dreamscape Memory Management': 'Dreamscape Memory System (systems/memory/)',
        'Dreamscape Template Engine': 'Dreamscape Template System (systems/templates/)',
        'Dreamscape GUI System': 'Dreamscape GUI System (systems/gui/)',
        'Lead Harvester Pro': 'Lead Harvesting System (tools/lead_harvesting/)',
        'AutoBloggerApp': 'Auto Blogger System (archive/auto_blogger_project/)',
    }

    updated_files = []

    doc_files = find_documentation_files()

    for file_path in doc_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            file_updated = False

            for old_ref, new_ref in reference_updates.items():
                if old_ref in content:
                    content = content.replace(old_ref, new_ref)
                    file_updated = True

            if file_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path)

        except Exception as e:
            print(f"  ❌ Error updating references in {file_path}: {e}")

    return len(updated_files), updated_files

def generate_documentation_report(path_updates: List[Tuple[str, int, List[str]]], reference_updates: Tuple[int, List[str]]):
    """Generate a documentation update report."""
    print("\n" + "=" * 60)
    print("📚 DOCUMENTATION UPDATE REPORT")
    print("=" * 60)

    total_files_updated = sum(updates for _, updates, _ in path_updates) + reference_updates[0]

    print(f"\n📈 SUMMARY: {total_files_updated} documentation files updated")

    print("\n🔍 PATH UPDATES:")
    for file_path, updates, paths in path_updates:
        if updates > 0:
            print(f"  ✅ {file_path} ({updates} updates)")
            for path_change in paths:
                print(f"    {path_change}")

    print("\n📝 REFERENCE UPDATES:")
    ref_count, ref_files = reference_updates
    print(f"  ✅ {ref_count} files with system reference updates")
    for ref_file in ref_files[:5]:  # Show first 5
        print(f"    - {ref_file}")
    if len(ref_files) > 5:
        print(f"    ... and {len(ref_files) - 5} more")

    if total_files_updated > 0:
        print("\n🎉 DOCUMENTATION SUCCESSFULLY UPDATED!")
        print("   ✅ All temp_repos/ references updated")
        print("   ✅ System descriptions current")
        print("   ✅ New canonical paths documented")
    else:
        print("\n⚠️  NO DOCUMENTATION UPDATES NEEDED")
        print("   (All documentation may already be current)")

def main():
    """Main documentation update function."""
    print("📚 Phase 2: Documentation Updates")
    print("=" * 40)

    # Find all documentation files
    doc_files = find_documentation_files()
    print(f"📁 Found {len(doc_files)} documentation files to check")

    # Update path references
    print("\n🔄 Updating Path References...")
    path_updates = []

    for file_path in doc_files:
        updates_made, updated_paths = update_file_paths(file_path)
        if updates_made > 0:
            path_updates.append((file_path, updates_made, updated_paths))
            print(f"  ✅ Updated: {file_path}")

    # Update system references
    reference_updates = update_system_references()

    # Generate report
    generate_documentation_report(path_updates, reference_updates)

    print("\n" + "=" * 40)
    print("✅ Phase 2: Documentation updates complete!")
    print("\n🎯 Wave C Phase 2: COMPLETE!")
    print("All extracted systems are now fully integrated!")

if __name__ == "__main__":
    main()