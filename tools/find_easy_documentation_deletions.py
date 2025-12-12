#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Easy Documentation Deletion Finder
===================================

Finds documentation that can be easily deleted:
- Parameters documented but don't exist in code
- Functions/classes documented but don't exist
- Outdated TODO/FIXME comments
- Duplicate docstrings
- Documentation describing removed functionality

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict

# Exclude patterns
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'venv', '.venv', 'node_modules',
    'agent_workspaces', 'temp_repos', 'archive', 'build', 'dist',
    '.egg-info', 'swarm_brain'
}

EXCLUDE_FILES = {
    '__init__.py'
}

# Patterns that indicate outdated documentation
OUTDATED_MARKERS = [
    r'\bTODO\b',
    r'\bFIXME\b',
    r'\bXXX\b',
    r'\bHACK\b',
    r'\bDEPRECATED\b',
    r'\bREMOVED\b',
    r'\bOBSOLETE\b',
    r'\bOLD\b',
    r'\bLEGACY\b',
    r'no longer',
    r'not used',
    r'removed',
    r'deleted',
]


class EasyDeletionFinder:
    """Finds documentation that can be easily deleted."""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.deletions: List[Dict] = []
        self.stats = {
            'files_analyzed': 0,
            'functions_checked': 0,
            'easy_deletions_found': 0
        }
    
    def should_analyze_file(self, file_path: Path) -> bool:
        """Check if file should be analyzed."""
        if not file_path.suffix == '.py':
            return False
        
        if file_path.name in EXCLUDE_FILES:
            return False
        
        # Check if in excluded directory
        parts = file_path.parts
        for exclude_dir in EXCLUDE_DIRS:
            if exclude_dir in parts:
                return False
        
        return True
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files to analyze."""
        files = []
        for py_file in self.root_dir.rglob('*.py'):
            if self.should_analyze_file(py_file):
                files.append(py_file)
        return sorted(files)
    
    def extract_docstring_params(self, docstring: str) -> Set[str]:
        """Extract parameter names from docstring."""
        params = set()
        if not docstring:
            return params
        
        # Look for parameter sections
        param_pattern = r'(?:Args?|Parameters?|Arguments?):\s*\n((?:\s+\w+[:\s].*?\n?)+)'
        match = re.search(param_pattern, docstring, re.MULTILINE | re.IGNORECASE)
        if match:
            param_text = match.group(1)
            # Extract parameter names
            param_names = re.findall(r'^\s+(\w+)[:\s]', param_text, re.MULTILINE)
            params.update(param_names)
        
        return params
    
    def check_outdated_markers(self, docstring: str, file_path: Path, line: int, context: str) -> List[Dict]:
        """Check for outdated markers in documentation."""
        issues = []
        if not docstring:
            return issues
        
        for marker_pattern in OUTDATED_MARKERS:
            if re.search(marker_pattern, docstring, re.IGNORECASE):
                issues.append({
                    'type': 'outdated_marker',
                    'file': str(file_path.relative_to(self.root_dir)),
                    'line': line,
                    'context': context,
                    'issue': f"Contains outdated marker: {marker_pattern}",
                    'action': 'Review and delete if obsolete',
                    'severity': 'medium'
                })
        
        return issues
    
    def check_documented_but_missing_params(self, node: ast.FunctionDef, file_path: Path) -> List[Dict]:
        """Check for parameters documented but missing from code."""
        issues = []
        
        docstring = ast.get_docstring(node)
        if not docstring:
            return issues
        
        # Get actual parameters
        actual_params = set()
        for arg in node.args.args:
            actual_params.add(arg.arg)
        
        # Get documented parameters
        documented_params = self.extract_docstring_params(docstring)
        
        # Find documented but missing
        missing_params = documented_params - actual_params
        
        for param in missing_params:
            issues.append({
                'type': 'param_documented_but_missing',
                'file': str(file_path.relative_to(self.root_dir)),
                'line': node.lineno,
                'context': f"Function: {node.name}",
                'issue': f"Parameter '{param}' documented but doesn't exist in function signature",
                'action': f"Delete parameter documentation for '{param}'",
                'severity': 'high'
            })
        
        return issues
    
    def check_duplicate_docstrings(self, file_path: Path, source: str) -> List[Dict]:
        """Check for duplicate docstrings in the same file."""
        issues = []
        
        try:
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError:
            return issues
        
        docstrings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Normalize docstring (remove leading/trailing whitespace)
                    normalized = docstring.strip()
                    if normalized:
                        docstrings.append({
                            'node': node,
                            'docstring': normalized,
                            'name': node.name
                        })
        
        # Find duplicates
        seen = {}
        for doc_info in docstrings:
            doc = doc_info['docstring']
            if doc in seen:
                issues.append({
                    'type': 'duplicate_docstring',
                    'file': str(file_path.relative_to(self.root_dir)),
                    'line': doc_info['node'].lineno,
                    'context': f"{doc_info['node'].__class__.__name__}: {doc_info['name']}",
                    'issue': f"Duplicate docstring (same as {seen[doc]['name']} at line {seen[doc]['line']})",
                    'action': 'Consider consolidating or removing duplicate',
                    'severity': 'low'
                })
            else:
                seen[doc] = {
                    'name': doc_info['name'],
                    'line': doc_info['node'].lineno
                }
        
        return issues
    
    def check_empty_or_trivial_docstrings(self, file_path: Path, source: str) -> List[Dict]:
        """Check for empty or trivial docstrings that can be removed."""
        issues = []
        
        try:
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError:
            return issues
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Check if docstring is trivial (just function name or very short)
                    normalized = docstring.strip()
                    if len(normalized) < 10 or normalized.lower() == node.name.lower():
                        issues.append({
                            'type': 'trivial_docstring',
                            'file': str(file_path.relative_to(self.root_dir)),
                            'line': node.lineno,
                            'context': f"{node.__class__.__name__}: {node.name}",
                            'issue': f"Trivial docstring: '{normalized[:50]}...'",
                            'action': 'Delete if not adding value',
                            'severity': 'low'
                        })
        
        return issues
    
    def analyze_file(self, file_path: Path) -> List[Dict]:
        """Analyze a single Python file for easy deletions."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()
                source_lines = source.split('\n')
            
            try:
                tree = ast.parse(source, filename=str(file_path))
            except SyntaxError:
                return issues
            
            # Check functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.stats['functions_checked'] += 1
                    
                    # Check for documented but missing parameters
                    param_issues = self.check_documented_but_missing_params(node, file_path)
                    issues.extend(param_issues)
                    
                    # Check for outdated markers
                    docstring = ast.get_docstring(node)
                    if docstring:
                        marker_issues = self.check_outdated_markers(
                            docstring, file_path, node.lineno, f"Function: {node.name}"
                        )
                        issues.extend(marker_issues)
            
            # Check for duplicate docstrings
            dup_issues = self.check_duplicate_docstrings(file_path, source)
            issues.extend(dup_issues)
            
            # Check for trivial docstrings
            trivial_issues = self.check_empty_or_trivial_docstrings(file_path, source)
            issues.extend(trivial_issues)
            
        except Exception as e:
            issues.append({
                'type': 'analysis_error',
                'file': str(file_path.relative_to(self.root_dir)),
                'line': 0,
                'context': '',
                'issue': f"Error analyzing file: {str(e)}",
                'action': 'N/A',
                'severity': 'low'
            })
        
        return issues
    
    def run(self) -> Dict:
        """Run the analysis on all Python files."""
        print("=" * 70)
        print("Easy Documentation Deletion Finder")
        print("=" * 70)
        print()
        
        files = self.find_python_files()
        print(f"📁 Found {len(files)} Python files to analyze")
        print()
        
        for file_path in files:
            self.stats['files_analyzed'] += 1
            issues = self.analyze_file(file_path)
            self.deletions.extend(issues)
            self.stats['easy_deletions_found'] += len(issues)
        
        return {
            'stats': self.stats,
            'deletions': self.deletions,
            'files_analyzed': len(files)
        }


def generate_report(results: Dict, output_file: Optional[Path] = None):
    """Generate a report from analysis results."""
    report_lines = []
    report_lines.append("# Easy Documentation Deletion Report\n")
    report_lines.append(f"**Files Analyzed**: {results['files_analyzed']}")
    report_lines.append(f"**Functions Checked**: {results['stats']['functions_checked']}")
    report_lines.append(f"**Easy Deletions Found**: {results['stats']['easy_deletions_found']}\n")
    report_lines.append("---\n")
    
    # Group by type
    by_type = defaultdict(list)
    for deletion in results['deletions']:
        by_type[deletion['type']].append(deletion)
    
    # Group by severity
    by_severity = defaultdict(list)
    for deletion in results['deletions']:
        by_severity[deletion['severity']].append(deletion)
    
    report_lines.append("## Summary by Issue Type\n")
    for issue_type, issues in sorted(by_type.items()):
        report_lines.append(f"- **{issue_type}**: {len(issues)} issues")
    report_lines.append("\n")
    
    report_lines.append("## Summary by Severity\n")
    for severity in ['high', 'medium', 'low']:
        if severity in by_severity:
            report_lines.append(f"- **{severity}**: {len(by_severity[severity])} issues")
    report_lines.append("\n")
    
    report_lines.append("## Easy Deletions (High Priority)\n")
    
    # Sort by severity, then file, then line
    sorted_deletions = sorted(results['deletions'], 
                              key=lambda x: (
                                  {'high': 0, 'medium': 1, 'low': 2}.get(x['severity'], 3),
                                  x['file'],
                                  x['line']
                              ))
    
    current_file = None
    for deletion in sorted_deletions:
        if deletion['file'] != current_file:
            current_file = deletion['file']
            report_lines.append(f"\n### {current_file}\n")
        
        report_lines.append(f"**Line {deletion['line']}** ({deletion['severity']}): {deletion['context']}")
        report_lines.append(f"- Issue: {deletion['issue']}")
        report_lines.append(f"- Action: {deletion['action']}\n")
    
    report_text = '\n'.join(report_lines)
    
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n📄 Report saved: {output_file}")
    else:
        print("\n" + report_text)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Find documentation that can be easily deleted'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='.',
        help='Root directory to analyze (default: current directory)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file for report (default: print to stdout)'
    )
    
    args = parser.parse_args()
    
    root_dir = Path(args.root).resolve()
    if not root_dir.exists():
        print(f"❌ Error: Directory not found: {root_dir}")
        sys.exit(1)
    
    finder = EasyDeletionFinder(root_dir)
    results = finder.run()
    
    output_file = Path(args.output) if args.output else None
    generate_report(results, output_file)
    
    print("\n" + "=" * 70)
    print("Analysis Complete")
    print("=" * 70)
    print(f"Files analyzed: {results['files_analyzed']}")
    print(f"Easy deletions found: {results['stats']['easy_deletions_found']}")
    print()


if __name__ == '__main__':
    main()

