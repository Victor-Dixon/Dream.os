#!/usr/bin/env python3
"""
Comprehensive Duplicate File Analyzer - Technical Debt Reduction
=================================================================

Analyzes duplicate files across the repository and generates resolution recommendations.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-02
"""

import hashlib
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class DuplicateAnalyzer:
    """Comprehensive duplicate file analyzer."""
    
    def __init__(self, repo_root: Path = None):
        """Initialize analyzer."""
        self.repo_root = repo_root or Path.cwd()
        self.excluded_patterns = {
            '.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env',
            '.env', 'data', 'archive', 'agent_workspaces', '.pytest_cache',
            'dist', 'build', '.mypy_cache', '.ruff_cache'
        }
        self.files_by_hash: Dict[str, List[Path]] = defaultdict(list)
        self.files_by_name: Dict[str, List[Path]] = defaultdict(list)
        
    def is_excluded(self, file_path: Path) -> bool:
        """Check if file should be excluded from analysis."""
        path_str = str(file_path)
        return any(pattern in path_str for pattern in self.excluded_patterns)
    
    def calculate_hash(self, file_path: Path) -> Optional[str]:
        """Calculate SHA256 hash of file."""
        try:
            return hashlib.sha256(file_path.read_bytes()).hexdigest()
        except Exception:
            return None
    
    def scan_repository(self) -> Tuple[Dict[str, List[Path]], Dict[str, List[Path]]]:
        """Scan repository for duplicates."""
        print("🔍 Scanning repository for duplicates...")
        
        count = 0
        for file_path in self.repo_root.rglob("*"):
            if not file_path.is_file():
                continue
            
            if self.is_excluded(file_path):
                continue
            
            count += 1
            if count % 1000 == 0:
                print(f"   Scanned {count} files...")
            
            # Hash-based duplicates (identical content)
            file_hash = self.calculate_hash(file_path)
            if file_hash:
                self.files_by_hash[file_hash].append(file_path)
            
            # Name-based duplicates (same filename)
            if file_path.suffix in ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md']:
                self.files_by_name[file_path.name].append(file_path)
        
        print(f"✅ Scanned {count} files")
        
        # Filter to only duplicates
        exact_duplicates = {
            h: paths for h, paths in self.files_by_hash.items() 
            if len(paths) > 1
        }
        name_duplicates = {
            n: paths for n, paths in self.files_by_name.items()
            if len(paths) > 1
        }
        
        return exact_duplicates, name_duplicates
    
    def determine_ssot(self, paths: List[Path]) -> Path:
        """Determine single source of truth file."""
        # Priority 1: src/core/ or src/services/
        for path in paths:
            rel = path.relative_to(self.repo_root)
            if str(rel).startswith('src/core/') or str(rel).startswith('src/services/'):
                return path
        
        # Priority 2: Shortest path
        return min(paths, key=lambda p: len(p.relative_to(self.repo_root).parts))
    
    def categorize_duplicates(
        self, 
        exact_duplicates: Dict[str, List[Path]],
        name_duplicates: Dict[str, List[Path]]
    ) -> Dict:
        """Categorize duplicates for resolution."""
        categories = {
            'identical_safe_delete': [],  # Category A
            'same_name_different': [],     # Category C
            'needs_analysis': []           # Category B
        }
        
        # Category A: Identical files (safe to delete)
        for hash_val, paths in exact_duplicates.items():
            ssot = self.determine_ssot(paths)
            duplicates = [p for p in paths if p != ssot]
            categories['identical_safe_delete'].append({
                'ssot': str(ssot.relative_to(self.repo_root)),
                'duplicates': [str(p.relative_to(self.repo_root)) for p in duplicates],
                'count': len(paths)
            })
        
        # Category C: Same name, need content comparison
        for name, paths in name_duplicates.items():
            if name == '__init__.py':
                continue  # Skip __init__.py (expected)
            
            # Check if any are identical
            hashes = {}
            for path in paths:
                h = self.calculate_hash(path)
                if h:
                    hashes.setdefault(h, []).append(path)
            
            # If all different hashes, they're different content
            if len(hashes) == len(paths):
                categories['same_name_different'].append({
                    'filename': name,
                    'paths': [str(p.relative_to(self.repo_root)) for p in paths],
                    'count': len(paths)
                })
            else:
                # Some might be identical, needs deeper analysis
                categories['needs_analysis'].append({
                    'filename': name,
                    'paths': [str(p.relative_to(self.repo_root)) for p in paths],
                    'count': len(paths)
                })
        
        return categories
    
    def generate_report(self, categories: Dict) -> str:
        """Generate analysis report."""
        report = []
        report.append("# Duplicate File Analysis Report")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Analyzer**: Agent-2 (Architecture & Design Specialist)")
        report.append("")
        
        # Summary
        report.append("## 📊 Summary")
        report.append("")
        report.append(f"- **Identical Files (Safe Delete)**: {len(categories['identical_safe_delete'])} groups")
        report.append(f"- **Same Name, Different Content**: {len(categories['same_name_different'])} groups")
        report.append(f"- **Needs Analysis**: {len(categories['needs_analysis'])} groups")
        report.append("")
        
        # Category A: Identical files
        if categories['identical_safe_delete']:
            report.append("## ✅ Category A: Identical Files (Safe to Delete)")
            report.append("")
            total_deletable = sum(len(g['duplicates']) for g in categories['identical_safe_delete'])
            report.append(f"**Total files safe to delete**: {total_deletable}")
            report.append("")
            
            for i, group in enumerate(categories['identical_safe_delete'][:20], 1):
                report.append(f"### Group {i}: {group['count']} identical files")
                report.append(f"- **Keep**: `{group['ssot']}`")
                report.append(f"- **Delete**:")
                for dup in group['duplicates']:
                    report.append(f"  - `{dup}`")
                report.append("")
        
        # Category C: Same name, different content
        if categories['same_name_different']:
            report.append("## ⚠️ Category C: Same Name, Different Content")
            report.append("")
            report.append("These files have the same name but different content. Consider renaming for clarity.")
            report.append("")
            
            for i, group in enumerate(categories['same_name_different'][:10], 1):
                report.append(f"### {group['filename']} ({group['count']} files)")
                for path in group['paths']:
                    report.append(f"- `{path}`")
                report.append("")
        
        return "\n".join(report)


def main():
    """Main execution."""
    analyzer = DuplicateAnalyzer()
    
    print("🚀 Starting comprehensive duplicate analysis...")
    print("")
    
    # Scan repository
    exact_duplicates, name_duplicates = analyzer.scan_repository()
    
    print("")
    print(f"📊 Found {len(exact_duplicates)} identical content groups")
    print(f"📊 Found {len(name_duplicates)} same-name groups")
    print("")
    
    # Categorize
    print("🔍 Categorizing duplicates...")
    categories = analyzer.categorize_duplicates(exact_duplicates, name_duplicates)
    
    # Generate report
    report = analyzer.generate_report(categories)
    
    # Save report
    report_path = Path("docs/technical_debt/DUPLICATE_ANALYSIS_REPORT.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    
    # Save JSON data
    json_path = Path("docs/technical_debt/DUPLICATE_ANALYSIS_DATA.json")
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'identical_groups': len(categories['identical_safe_delete']),
            'same_name_groups': len(categories['same_name_different']),
            'needs_analysis_groups': len(categories['needs_analysis'])
        },
        'categories': {
            'identical_safe_delete': categories['identical_safe_delete'],
            'same_name_different': categories['same_name_different'],
            'needs_analysis': categories['needs_analysis']
        }
    }
    json_path.write_text(json.dumps(json_data, indent=2))
    
    print("✅ Analysis complete!")
    print(f"📄 Report: {report_path}")
    print(f"📄 Data: {json_path}")
    print("")
    
    # Print quick summary
    total_deletable = sum(len(g['duplicates']) for g in categories['identical_safe_delete'])
    print(f"🎯 Quick Wins: {total_deletable} files safe to delete immediately")
    print(f"⚠️  Needs Review: {len(categories['same_name_different'])} same-name groups")


if __name__ == '__main__':
    main()

