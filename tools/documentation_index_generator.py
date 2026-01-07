#!/usr/bin/env python3
"""
Documentation Index Generator - Phase 4 Block 8
===============================================

Generates comprehensive documentation index with SSOT domain tagging validation.
Creates cross-referenced navigation for all documentation files.

V2 Compliance: <300 lines
Author: Agent-2 (Architecture & Design Specialist)
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime
from collections import defaultdict

class DocumentationIndexGenerator:
    """Generates comprehensive documentation index with SSOT validation."""

    def __init__(self, docs_root: Path):
        self.docs_root = docs_root
        self.index_data = {
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categories": defaultdict(list),
            "cross_references": defaultdict(list),
            "ssot_validation": {
                "total_files": 0,
                "tagged_files": 0,
                "missing_tags": []
            }
        }

    def extract_ssot_domain(self, content: str) -> str:
        """Extract SSOT domain from file content."""
        pattern = r'<!--\s*SSOT\s+Domain:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*-->'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).lower() if match else ""

    def extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata from file headers."""
        metadata = {}
        lines = content.split('\n')[:20]  # Check first 20 lines

        # Extract common metadata patterns
        patterns = {
            'version': r'\*\*Version:\*\*\s*([^\n]+)',
            'author': r'\*\*Author:\*\*\s*([^\n]+)',
            'status': r'\*\*Status:\*\*\s*([^\n]+)',
            'updated': r'\*\*Last Updated:\*\*\s*([^\n]+)'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content[:1000])  # Check first 1000 chars
            if match:
                metadata[key] = match.group(1).strip()

        return metadata

    def categorize_file(self, file_path: Path, content: str) -> str:
        """Categorize documentation file based on path and content."""
        path_str = str(file_path).lower()

        # Path-based categorization
        if 'architecture' in path_str:
            return 'Architecture'
        elif 'protocols' in path_str or 'protocol' in path_str:
            return 'Protocols'
        elif 'messaging' in path_str:
            return 'Messaging'
        elif 'website' in path_str or 'seo' in path_str:
            return 'Websites'
        elif 'onboarding' in path_str:
            return 'Onboarding'
        elif 'reports' in path_str or 'audit' in path_str:
            return 'Reports'
        elif 'standards' in path_str or 'compliance' in path_str:
            return 'Standards'
        elif 'trading' in path_str:
            return 'Trading'
        elif 'ssot' in path_str:
            return 'SSOT'
        elif 'deployment' in path_str:
            return 'Deployment'

        # Content-based categorization fallback
        if 'architecture' in content[:500].lower():
            return 'Architecture'
        elif 'protocol' in content[:500].lower():
            return 'Protocols'
        elif 'messaging' in content[:500].lower():
            return 'Messaging'
        elif 'website' in content[:500].lower() or 'seo' in content[:500].lower():
            return 'Websites'
        elif 'onboard' in content[:500].lower():
            return 'Onboarding'
        elif 'report' in content[:500].lower():
            return 'Reports'

        return 'General'

    def extract_title_and_description(self, content: str) -> Tuple[str, str]:
        """Extract title and description from file content."""
        lines = content.split('\n')

        # Find title (first # heading)
        title = ""
        for line in lines[:10]:
            if line.strip().startswith('# ') and not line.strip().startswith('<!--'):
                title = line.strip()[2:].strip()
                break

        # Extract description (text after title, before next heading or within first few paragraphs)
        description = ""
        in_description = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('##') and description:
                break
            if line.startswith('#') and title:
                in_description = True
                continue
            if in_description or (title and not description):
                if not line.startswith('**') and not line.startswith('*') and not line.startswith('-'):
                    description += line + " "
                    if len(description) > 200:  # Limit description length
                        break

        return title, description.strip()

    def scan_documentation(self) -> None:
        """Scan all documentation files and build index."""
        for root, dirs, files in os.walk(self.docs_root):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]

            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Extract SSOT domain
                        ssot_domain = self.extract_ssot_domain(content)
                        self.index_data['ssot_validation']['total_files'] += 1

                        if ssot_domain:
                            self.index_data['ssot_validation']['tagged_files'] += 1
                        else:
                            self.index_data['ssot_validation']['missing_tags'].append(str(file_path))

                        # Extract metadata
                        metadata = self.extract_metadata(content)
                        title, description = self.extract_title_and_description(content)

                        # Categorize file
                        category = self.categorize_file(file_path, content)

                        # Create entry
                        entry = {
                            'path': str(file_path.relative_to(self.docs_root.parent)),
                            'title': title or file,
                            'description': description,
                            'ssot_domain': ssot_domain,
                            'metadata': metadata,
                            'category': category
                        }

                        self.index_data['categories'][category].append(entry)

                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

    def generate_cross_references(self) -> None:
        """Generate cross-reference data between documentation files."""
        # Build reference mapping
        for category, files in self.index_data['categories'].items():
            for file_entry in files:
                # Find files that reference this one
                for other_category, other_files in self.index_data['categories'].items():
                    for other_entry in other_files:
                        if file_entry['path'] != other_entry['path']:
                            # Check if other file references this file
                            if file_entry['title'] in other_entry.get('description', '') or \
                               file_entry['path'].split('/')[-1] in other_entry.get('description', ''):
                                self.index_data['cross_references'][file_entry['path']].append({
                                    'referenced_by': other_entry['path'],
                                    'category': other_category
                                })

    def generate_markdown_index(self) -> str:
        """Generate markdown documentation index."""
        output = ["# Documentation Index", ""]
        output.append(f"**Generated:** {self.index_data['generated']}")
        output.append("")

        # SSOT Validation Summary
        ssot = self.index_data['ssot_validation']
        output.append("## SSOT Validation Summary")
        output.append("")
        output.append(f"- **Total Files:** {ssot['total_files']}")
        output.append(f"- **Tagged Files:** {ssot['tagged_files']}")
        output.append(f"- **Missing Tags:** {len(ssot['missing_tags'])}")
        output.append("")

        if ssot['missing_tags']:
            output.append("### Files Missing SSOT Tags")
            for file_path in ssot['missing_tags'][:10]:  # Show first 10
                output.append(f"- `{file_path}`")
            if len(ssot['missing_tags']) > 10:
                output.append(f"- ... and {len(ssot['missing_tags']) - 10} more")
            output.append("")

        # Categories
        for category, files in sorted(self.index_data['categories'].items()):
            if files:
                output.append(f"## {category}")
                output.append("")
                output.append(f"_{self.get_category_description(category)}_")
                output.append("")

                # Sort files by title
                sorted_files = sorted(files, key=lambda x: x['title'])

                for file_entry in sorted_files[:20]:  # Limit to 20 per category for readability
                    title = file_entry['title']
                    path = file_entry['path']
                    description = file_entry['description'][:100] + "..." if len(file_entry['description']) > 100 else file_entry['description']
                    ssot_tag = f" ({file_entry['ssot_domain']})" if file_entry['ssot_domain'] else " ⚠️ *Missing SSOT tag*"

                    output.append(f"- [{title}]({path}){ssot_tag}")
                    if description:
                        output.append(f"  - {description}")

                if len(sorted_files) > 20:
                    output.append(f"- ... and {len(sorted_files) - 20} more files")
                output.append("")

        return "\n".join(output)

    def get_category_description(self, category: str) -> str:
        """Get description for category."""
        descriptions = {
            'Architecture': 'System architecture, design patterns, technical decisions',
            'Protocols': 'Operational protocols, workflows, procedures',
            'Messaging': 'Communication systems, A2A/C2A protocols',
            'Websites': 'Website audits, SEO, optimization guides',
            'Onboarding': 'Agent onboarding guides and procedures',
            'Reports': 'Audit reports, analysis, and assessments',
            'Standards': 'Code quality standards, compliance guidelines',
            'Trading': 'Trading robot documentation and guides',
            'SSOT': 'Single Source of Truth validation and coordination',
            'Deployment': 'Deployment protocols and procedures',
            'General': 'General documentation and guides'
        }
        return descriptions.get(category, 'Documentation files')

    def save_index(self, output_path: Path) -> None:
        """Save generated index to file."""
        markdown_content = self.generate_markdown_index()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Also save JSON data for programmatic access
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.index_data, f, indent=2, default=str)

        print(f"📄 Documentation index generated: {output_path}")
        print(f"📊 JSON data saved: {json_path}")

def main():
    """Main execution."""
    docs_root = Path(__file__).parent.parent / "docs"

    generator = DocumentationIndexGenerator(docs_root)
    generator.scan_documentation()
    generator.generate_cross_references()

    output_path = docs_root / "DOCUMENTATION_INDEX_GENERATED.md"
    generator.save_index(output_path)

    # Print summary
    ssot = generator.index_data['ssot_validation']
    print(f"\n📊 Documentation Index Generation Complete")
    print(f"   Total files: {ssot['total_files']}")
    print(f"   Tagged files: {ssot['tagged_files']}")
    print(f"   Missing tags: {len(ssot['missing_tags'])}")

if __name__ == "__main__":
    main()