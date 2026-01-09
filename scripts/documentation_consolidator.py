#!/usr/bin/env python3
"""
Documentation Consolidator

This script updates all references to consolidated files throughout the repository.
It handles:

1. Updating file paths in documentation
2. Fixing broken links after consolidation
3. Updating configuration files
4. Maintaining reference integrity

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@dataclass
class ReferenceUpdate:
    """Tracks a reference update operation"""
    file_path: str
    old_reference: str
    new_reference: str
    line_number: int
    context: str
    updated: bool
    timestamp: str

@dataclass
class DocumentationConsolidationReport:
    """Report for documentation consolidation operations"""
    timestamp: str
    files_scanned: int
    references_found: int
    references_updated: int
    broken_links_fixed: int
    errors: List[str]
    updates: List[ReferenceUpdate]

class DocumentationConsolidator:
    """Handles updating references to consolidated files"""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.consolidated_archives = self.base_path / "agent_workspaces" / "consolidated_archives"

        # Define consolidation mappings
        self.consolidation_mappings = {
            # QUICK_START.md consolidation
            r"agent_workspaces/Agent-[2-8]/QUICK_START\.md": "agent_workspaces/Agent-7/QUICK_START.md",

            # Archive consolidation mappings
            r"agent_workspaces/(Agent-\d+)/archive/": r"agent_workspaces/consolidated_archives/\1/",
        }

        # File extensions to scan for references
        self.scan_extensions = {'.md', '.txt', '.json', '.yaml', '.yml', '.py', '.js', '.ts', '.html', '.css'}

        # Files to exclude from scanning
        self.exclude_patterns = {
            '__pycache__',
            '.git',
            'node_modules',
            'backups',
            'archives'
        }

    def should_scan_file(self, file_path: Path) -> bool:
        """Determine if a file should be scanned for references"""
        if file_path.suffix.lower() not in self.scan_extensions:
            return False

        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if pattern in str(file_path):
                return False

        return True

    def find_file_references(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """Find all file references in a file"""
        references = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    # Look for file paths in the line
                    # Match patterns like: agent_workspaces/Agent-X/file.md
                    # or relative paths, or absolute paths within the repo

                    # Find potential file references
                    path_patterns = [
                        r'agent_workspaces/[^\'"\s)]+',  # Direct paths
                        r'\.\./[^\'"\s)]+',             # Relative paths
                        r'\./[^\'"\s)]+',               # Current dir paths
                    ]

                    for pattern in path_patterns:
                        matches = re.findall(pattern, line)
                        for match in matches:
                            # Clean up the match
                            match = match.rstrip('.,!?')
                            if len(match) > 10:  # Minimum length for a meaningful path
                                references.append((match, line_num, line.strip()))

        except Exception as e:
            print(f"Error scanning {file_path}: {e}")

        return references

    def apply_consolidation_mapping(self, reference: str) -> Optional[str]:
        """Apply consolidation mapping to a reference"""
        for pattern, replacement in self.consolidation_mappings.items():
            if re.search(pattern, reference):
                # Apply the mapping
                new_reference = re.sub(pattern, replacement, reference)
                if new_reference != reference:
                    return new_reference

        return None

    def update_file_references(self, file_path: Path) -> List[ReferenceUpdate]:
        """Update file references in a single file"""
        updates = []
        content_lines = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content_lines = f.readlines()

            modified = False

            for i, line in enumerate(content_lines):
                original_line = line
                line_num = i + 1

                # Find references in this line
                references = self.find_file_references_in_line(line, line_num)
                for old_ref, context in references:
                    new_ref = self.apply_consolidation_mapping(old_ref)
                    if new_ref and new_ref != old_ref:
                        # Replace the reference in the line
                        line = line.replace(old_ref, new_ref)

                        update = ReferenceUpdate(
                            file_path=str(file_path),
                            old_reference=old_ref,
                            new_reference=new_ref,
                            line_number=line_num,
                            context=context,
                            updated=True,
                            timestamp=datetime.now().isoformat()
                        )
                        updates.append(update)

                if line != original_line:
                    content_lines[i] = line
                    modified = True

            # Write back if modified
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(content_lines)

        except Exception as e:
            print(f"Error updating {file_path}: {e}")

        return updates

    def find_file_references_in_line(self, line: str, line_num: int) -> List[Tuple[str, str]]:
        """Find file references in a single line"""
        references = []

        # Look for various file reference patterns
        patterns = [
            r'agent_workspaces/Agent-\d+/[^\'"\s\)]+',  # Agent workspace files
            r'agent_workspaces/consolidated_archives/[^\'"\s\)]+',  # Consolidated archives
            r'\[([^\]]+)\]\(([^)]+)\)',  # Markdown links: [text](path)
            r'href=["\']([^"\']+)["\']',  # HTML href attributes
            r'src=["\']([^"\']+)["\']',   # HTML src attributes
        ]

        for pattern in patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                if isinstance(match, tuple):  # For markdown links
                    ref = match[1] if len(match) > 1 else match[0]
                else:
                    ref = match

                # Check if it looks like a file path
                if any(keyword in ref for keyword in ['agent_workspaces', 'QUICK_START', 'archive']):
                    references.append((ref, line.strip()))

        return references

    def scan_repository_for_references(self) -> Dict[str, List[Tuple[str, int, str]]]:
        """Scan the entire repository for file references"""
        print("🔍 Scanning repository for file references...")

        all_references = {}

        # Walk through all files in the repository
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)

            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]

            for file in files:
                file_path = root_path / file

                if self.should_scan_file(file_path):
                    references = self.find_file_references(file_path)
                    if references:
                        all_references[str(file_path)] = references

        print(f"📊 Found references in {len(all_references)} files")
        return all_references

    def update_all_references(self) -> DocumentationConsolidationReport:
        """Update all references throughout the repository"""
        print("🔄 Starting documentation consolidation...")

        # Scan for references
        all_references = self.scan_repository_for_references()

        updates = []
        errors = []

        # Process each file with references
        for file_path_str, references in all_references.items():
            file_path = Path(file_path_str)

            try:
                file_updates = self.update_file_references(file_path)
                updates.extend(file_updates)

                if file_updates:
                    print(f"✅ Updated {len(file_updates)} references in {file_path.name}")

            except Exception as e:
                error_msg = f"Error updating {file_path}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")

        # Generate report
        report = DocumentationConsolidationReport(
            timestamp=datetime.now().isoformat(),
            files_scanned=len(all_references),
            references_found=sum(len(refs) for refs in all_references.values()),
            references_updated=len(updates),
            broken_links_fixed=0,  # Would need additional logic to verify
            errors=errors,
            updates=updates
        )

        # Save detailed report
        self.save_report(report)

        print("
✅ Documentation consolidation complete!"        print(f"📁 Files scanned: {report.files_scanned}")
        print(f"🔗 References updated: {report.references_updated}")
        print(f"❌ Errors: {len(report.errors)}")

        return report

    def save_report(self, report: DocumentationConsolidationReport):
        """Save the consolidation report"""
        reports_dir = self.base_path / "reports" / "consolidation"
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_file = reports_dir / f"documentation_consolidation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(report_file, 'w', indent=2) as f:
                json.dump(asdict(report), f, indent=2)
            print(f"📄 Report saved to {report_file}")
        except Exception as e:
            print(f"Error saving report: {e}")

    def verify_consolidation(self) -> Dict[str, List[str]]:
        """Verify that consolidation was successful"""
        print("🔍 Verifying consolidation integrity...")

        issues = {
            "broken_references": [],
            "missing_files": [],
            "inconsistent_mappings": []
        }

        # Check that consolidated files exist
        if not (self.base_path / "agent_workspaces" / "Agent-7" / "QUICK_START.md").exists():
            issues["missing_files"].append("Consolidated QUICK_START.md not found")

        if not self.consolidated_archives.exists():
            issues["missing_files"].append("Consolidated archives directory not found")

        # Check for any remaining old references
        all_references = self.scan_repository_for_references()
        for file_path, references in all_references.items():
            for ref, line_num, context in references:
                # Check if this reference points to an old location
                if "Agent-[2-8]/QUICK_START.md" in ref:
                    issues["broken_references"].append(
                        f"{file_path}:{line_num} - Old QUICK_START.md reference: {ref}"
                    )

        return issues

    def generate_reference_map(self) -> Dict[str, str]:
        """Generate a mapping of old to new references for documentation"""
        reference_map = {}

        # QUICK_START.md mappings
        for i in range(2, 9):
            old_path = f"agent_workspaces/Agent-{i}/QUICK_START.md"
            new_path = "agent_workspaces/Agent-7/QUICK_START.md"
            reference_map[old_path] = new_path

        # Archive mappings
        for i in range(1, 9):
            old_pattern = f"agent_workspaces/Agent-{i}/archive/"
            new_pattern = f"agent_workspaces/consolidated_archives/Agent-{i}/"
            reference_map[old_pattern] = new_pattern

        return reference_map


def main():
    """Main entry point for documentation consolidation"""
    print("Documentation Consolidator")
    print("This script updates all references to consolidated files.")
    print()

    consolidator = DocumentationConsolidator()

    # Run consolidation
    report = consolidator.update_all_references()

    # Verify results
    issues = consolidator.verify_consolidation()

    print("\n🔍 Verification Results:")
    for issue_type, issue_list in issues.items():
        if issue_list:
            print(f"⚠️  {issue_type.upper()}: {len(issue_list)} issues")
            for issue in issue_list[:5]:  # Show first 5
                print(f"  - {issue}")
            if len(issue_list) > 5:
                print(f"  ... and {len(issue_list) - 5} more")
        else:
            print(f"✅ {issue_type.upper()}: No issues found")

    # Generate reference map
    reference_map = consolidator.generate_reference_map()
    print("
📋 Reference Mapping:"    for old, new in reference_map.items():
        print(f"  {old} → {new}")

    print("
✅ Documentation consolidation complete!"    print(f"🔄 References updated: {report.references_updated}")
    print(f"📄 Files processed: {report.files_scanned}")


if __name__ == "__main__":
    main()