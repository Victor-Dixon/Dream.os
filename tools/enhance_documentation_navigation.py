#!/usr/bin/env python3
"""
Documentation Navigation Enhancement Tool
========================================

Scans documentation files and enhances them with proper tagging, cross-references, and navigation links.

<!-- SSOT Domain: tools -->
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict


class DocumentationEnhancer:
    """Enhance documentation files with navigation and tagging."""
    
    def __init__(self, root_dir: Path = None):
        if root_dir is None:
            root_dir = Path(__file__).parent.parent
        self.root_dir = root_dir
        self.docs_dir = root_dir / 'docs'
        self.websites_docs_dir = root_dir.parent / 'websites' / 'docs' if (root_dir.parent / 'websites').exists() else None
        
    def scan_documentation(self) -> Dict:
        """Scan all documentation files."""
        docs = {
            'files': [],
            'domains': defaultdict(list),
            'tags': defaultdict(list),
            'references': defaultdict(list),
            'missing_tags': [],
            'missing_metadata': [],
        }
        
        # Scan main docs directory
        if self.docs_dir.exists():
            for md_file in self.docs_dir.rglob('*.md'):
                doc_info = self._analyze_file(md_file, self.root_dir)
                if doc_info:
                    docs['files'].append(doc_info)
                    if doc_info.get('domain'):
                        docs['domains'][doc_info['domain']].append(doc_info)
                    if doc_info.get('tags'):
                        for tag in doc_info['tags']:
                            docs['tags'][tag].append(doc_info)
                    if doc_info.get('references'):
                        docs['references'][md_file.relative_to(self.root_dir)] = doc_info['references']
                    if not doc_info.get('has_ssot_tag'):
                        docs['missing_tags'].append(doc_info)
                    if not doc_info.get('has_metadata'):
                        docs['missing_metadata'].append(doc_info)
        
        # Scan websites docs directory
        if self.websites_docs_dir and self.websites_docs_dir.exists():
            for md_file in self.websites_docs_dir.rglob('*.md'):
                doc_info = self._analyze_file(md_file, self.root_dir.parent / 'websites')
                if doc_info:
                    docs['files'].append(doc_info)
                    if doc_info.get('domain'):
                        docs['domains'][doc_info['domain']].append(doc_info)
                    if doc_info.get('tags'):
                        for tag in doc_info['tags']:
                            docs['tags'][tag].append(doc_info)
        
        return docs
    
    def _analyze_file(self, file_path: Path, base_dir: Path) -> Optional[Dict]:
        """Analyze a single documentation file."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            rel_path = file_path.relative_to(base_dir)
            
            info = {
                'path': str(rel_path),
                'full_path': str(file_path),
                'name': file_path.name,
                'has_ssot_tag': False,
                'has_metadata': False,
                'domain': None,
                'tags': [],
                'references': [],
                'title': None,
            }
            
            # Check for SSOT domain tag
            ssot_pattern = r'<!--\s*SSOT\s+Domain:\s*([\w_]+)\s*-->'
            ssot_match = re.search(ssot_pattern, content, re.IGNORECASE)
            if ssot_match:
                info['has_ssot_tag'] = True
                info['domain'] = ssot_match.group(1).lower()
            
            # Check for metadata header
            metadata_pattern = r'\*\*Author:\*\*|\*\*Date:\*\*|\*\*Status:\*\*'
            if re.search(metadata_pattern, content):
                info['has_metadata'] = True
            
            # Extract title
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                info['title'] = title_match.group(1).strip()
            
            # Extract tags (YAML frontmatter or comment)
            yaml_tags = re.search(r'^tags:\s*\n(?:\s+-\s+(.+)\n)+', content, re.MULTILINE)
            if yaml_tags:
                tag_lines = re.findall(r'^\s+-\s+(.+)$', content, re.MULTILINE)
                info['tags'] = [tag.strip() for tag in tag_lines]
            
            comment_tags = re.search(r'<!--\s*Tags?:\s*([^>]+)\s*-->', content, re.IGNORECASE)
            if comment_tags:
                tags_str = comment_tags.group(1)
                info['tags'] = [tag.strip() for tag in tags_str.split(',')]
            
            # Extract references
            ref_pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
            references = re.findall(ref_pattern, content)
            info['references'] = [{'text': ref[0], 'path': ref[1]} for ref in references]
            
            return info
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def generate_enhancement_report(self, docs: Dict) -> str:
        """Generate enhancement report."""
        report = []
        report.append("# Documentation Navigation Enhancement Report\n")
        report.append(f"**Generated:** {Path(__file__).stat().st_mtime}\n")
        report.append(f"**Total Files:** {len(docs['files'])}\n\n")
        
        # Missing tags
        report.append("## Missing SSOT Domain Tags\n")
        if docs['missing_tags']:
            report.append(f"**Count:** {len(docs['missing_tags'])}\n\n")
            for doc in docs['missing_tags'][:20]:  # Limit to 20
                report.append(f"- `{doc['path']}`\n")
            if len(docs['missing_tags']) > 20:
                report.append(f"\n... and {len(docs['missing_tags']) - 20} more\n")
        else:
            report.append("✅ All files have SSOT domain tags\n")
        
        report.append("\n## Missing Metadata Headers\n")
        if docs['missing_metadata']:
            report.append(f"**Count:** {len(docs['missing_metadata'])}\n\n")
            for doc in docs['missing_metadata'][:20]:
                report.append(f"- `{doc['path']}`\n")
            if len(docs['missing_metadata']) > 20:
                report.append(f"\n... and {len(docs['missing_metadata']) - 20} more\n")
        else:
            report.append("✅ All files have metadata headers\n")
        
        # Domain distribution
        report.append("\n## Documentation by SSOT Domain\n")
        for domain, files in sorted(docs['domains'].items()):
            report.append(f"- **{domain}**: {len(files)} files\n")
        
        # Tag distribution
        report.append("\n## Documentation by Topic Tags\n")
        for tag, files in sorted(docs['tags'].items()):
            report.append(f"- **{tag}**: {len(files)} files\n")
        
        return '\n'.join(report)
    
    def save_report(self, docs: Dict, output_file: Path = None):
        """Save enhancement report."""
        if output_file is None:
            output_file = self.docs_dir / 'DOCUMENTATION_NAVIGATION_ENHANCEMENT_REPORT.md'
        
        report = self.generate_enhancement_report(docs)
        output_file.write_text(report, encoding='utf-8')
        print(f"✅ Report saved to: {output_file.relative_to(self.root_dir)}")
        
        # Also save JSON data
        json_file = output_file.with_suffix('.json')
        json_data = {
            'total_files': len(docs['files']),
            'domains': {k: len(v) for k, v in docs['domains'].items()},
            'tags': {k: len(v) for k, v in docs['tags'].items()},
            'missing_tags_count': len(docs['missing_tags']),
            'missing_metadata_count': len(docs['missing_metadata']),
        }
        json_file.write_text(json.dumps(json_data, indent=2), encoding='utf-8')
        print(f"✅ JSON data saved to: {json_file.relative_to(self.root_dir)}")


def main():
    """Main function."""
    enhancer = DocumentationEnhancer()
    
    print("🔍 Scanning documentation files...")
    docs = enhancer.scan_documentation()
    
    print(f"📊 Found {len(docs['files'])} documentation files")
    print(f"   Domains: {len(docs['domains'])}")
    print(f"   Tags: {len(docs['tags'])}")
    print(f"   Missing SSOT tags: {len(docs['missing_tags'])}")
    print(f"   Missing metadata: {len(docs['missing_metadata'])}")
    
    print("\n💾 Generating enhancement report...")
    enhancer.save_report(docs)
    
    print("\n✅ Documentation navigation enhancement scan complete!")


if __name__ == '__main__':
    main()

