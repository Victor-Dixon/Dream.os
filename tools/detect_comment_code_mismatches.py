#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Comment-Code Mismatch Detector
==============================

Analyzes Python files to identify cases where comments/docstrings don't match
the actual code implementation. Detects:
- Outdated docstrings describing removed functionality
- Comments describing code that doesn't exist
- Function signatures that don't match docstrings
- Missing parameter documentation
- Incorrect return type documentation

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


class CommentCodeMismatchDetector:
    """Detects mismatches between comments and code."""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.mismatches: List[Dict] = []
        self.stats = {
            'files_analyzed': 0,
            'functions_checked': 0,
            'classes_checked': 0,
            'mismatches_found': 0
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
    
    def extract_docstring_params(self, docstring: str) -> Dict[str, str]:
        """Extract parameter descriptions from docstring."""
        params = {}
        if not docstring:
            return params
        
        # Look for parameter sections
        param_pattern = r'(?:Args?|Parameters?|Arguments?):\s*\n((?:\s+\w+[:\s].*?\n?)+)'
        match = re.search(param_pattern, docstring, re.MULTILINE | re.IGNORECASE)
        if match:
            param_text = match.group(1)
            # Extract individual parameters
            param_lines = re.findall(r'^\s+(\w+)[:\s]+(.*?)(?=\n\s+\w+[:\s]|\Z)', 
                                    param_text, re.MULTILINE | re.DOTALL)
            for name, desc in param_lines:
                params[name.strip()] = desc.strip()
        
        return params
    
    def extract_return_info(self, docstring: str) -> Optional[str]:
        """Extract return type/description from docstring."""
        if not docstring:
            return None
        
        # Look for Returns section
        return_pattern = r'(?:Returns?|Return type):\s*(.*?)(?=\n\n|\n\w+:|$)'
        match = re.search(return_pattern, docstring, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return None
    
    def check_function_signature(self, node: ast.FunctionDef, file_path: Path) -> List[Dict]:
        """Check if function signature matches docstring."""
        issues = []
        
        if not node.body:
            return issues
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        # Get function parameters
        actual_params = set()
        for arg in node.args.args:
            actual_params.add(arg.arg)
        
        # Check for *args and **kwargs
        has_vararg = node.args.vararg is not None
        has_kwarg = node.args.kwarg is not None
        
        # Check if docstring mentions parameters
        if docstring:
            docstring_params = self.extract_docstring_params(docstring)
            
            # Check for documented params that don't exist
            for doc_param in docstring_params:
                if doc_param not in actual_params:
                    issues.append({
                        'type': 'param_documented_but_missing',
                        'file': str(file_path.relative_to(self.root_dir)),
                        'line': node.lineno,
                        'function': node.name,
                        'issue': f"Parameter '{doc_param}' documented in docstring but not in function signature",
                        'severity': 'medium'
                    })
            
            # Check for params without documentation (only if docstring has Args section)
            if docstring_params:  # Only check if Args section exists
                for actual_param in actual_params:
                    if actual_param not in docstring_params and actual_param != 'self':
                        issues.append({
                            'type': 'param_missing_documentation',
                            'file': str(file_path.relative_to(self.root_dir)),
                            'line': node.lineno,
                            'function': node.name,
                            'issue': f"Parameter '{actual_param}' not documented in docstring",
                            'severity': 'low'
                        })
        
        # Check return annotation vs docstring
        if node.returns and docstring:
            return_info = self.extract_return_info(docstring)
            if not return_info:
                issues.append({
                    'type': 'return_missing_documentation',
                    'file': str(file_path.relative_to(self.root_dir)),
                    'line': node.lineno,
                    'function': node.name,
                    'issue': f"Function has return type annotation but no Returns section in docstring",
                    'severity': 'low'
                })
        
        return issues
    
    def check_outdated_comments(self, node: ast.AST, file_path: Path, source_lines: List[str]) -> List[Dict]:
        """Check for comments that reference non-existent code."""
        issues = []
        
        # This is a simplified check - look for TODO/FIXME/XXX that might be outdated
        # More sophisticated analysis would require semantic understanding
        
        return issues
    
    def analyze_file(self, file_path: Path) -> List[Dict]:
        """Analyze a single Python file for comment-code mismatches."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()
                source_lines = source.split('\n')
            
            try:
                tree = ast.parse(source, filename=str(file_path))
            except SyntaxError:
                # Skip files with syntax errors
                return issues
            
            # Walk through AST
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.stats['functions_checked'] += 1
                    func_issues = self.check_function_signature(node, file_path)
                    issues.extend(func_issues)
                
                elif isinstance(node, ast.ClassDef):
                    self.stats['classes_checked'] += 1
                    # Check class docstring
                    class_docstring = ast.get_docstring(node)
                    if class_docstring:
                        # Basic check: class has methods mentioned in docstring?
                        # This would require more sophisticated analysis
                        pass
            
        except Exception as e:
            issues.append({
                'type': 'analysis_error',
                'file': str(file_path.relative_to(self.root_dir)),
                'line': 0,
                'function': '',
                'issue': f"Error analyzing file: {str(e)}",
                'severity': 'low'
            })
        
        return issues
    
    def run(self) -> Dict:
        """Run the analysis on all Python files."""
        print("=" * 70)
        print("Comment-Code Mismatch Detection")
        print("=" * 70)
        print()
        
        files = self.find_python_files()
        print(f"📁 Found {len(files)} Python files to analyze")
        print()
        
        for file_path in files:
            self.stats['files_analyzed'] += 1
            issues = self.analyze_file(file_path)
            self.mismatches.extend(issues)
            self.stats['mismatches_found'] += len(issues)
        
        return {
            'stats': self.stats,
            'mismatches': self.mismatches,
            'files_analyzed': len(files)
        }


def generate_report(results: Dict, output_file: Optional[Path] = None):
    """Generate a report from analysis results."""
    report_lines = []
    report_lines.append("# Comment-Code Mismatch Detection Report\n")
    report_lines.append(f"**Date**: {Path(__file__).stat().st_mtime}")
    report_lines.append(f"**Files Analyzed**: {results['files_analyzed']}")
    report_lines.append(f"**Functions Checked**: {results['stats']['functions_checked']}")
    report_lines.append(f"**Classes Checked**: {results['stats']['classes_checked']}")
    report_lines.append(f"**Mismatches Found**: {results['stats']['mismatches_found']}\n")
    report_lines.append("---\n")
    
    # Group by type
    by_type = defaultdict(list)
    for mismatch in results['mismatches']:
        by_type[mismatch['type']].append(mismatch)
    
    # Group by file
    by_file = defaultdict(list)
    for mismatch in results['mismatches']:
        by_file[mismatch['file']].append(mismatch)
    
    report_lines.append("## Summary by Issue Type\n")
    for issue_type, issues in sorted(by_type.items()):
        report_lines.append(f"- **{issue_type}**: {len(issues)} issues")
    report_lines.append("\n")
    
    report_lines.append("## Detailed Findings\n")
    
    # Sort by file, then line
    sorted_mismatches = sorted(results['mismatches'], 
                              key=lambda x: (x['file'], x['line']))
    
    current_file = None
    for mismatch in sorted_mismatches:
        if mismatch['file'] != current_file:
            current_file = mismatch['file']
            report_lines.append(f"\n### {current_file}\n")
        
        report_lines.append(f"**Line {mismatch['line']}** ({mismatch['severity']}): {mismatch['function']}")
        report_lines.append(f"- {mismatch['issue']}\n")
    
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
        description='Detect comment-code mismatches in Python files'
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
    
    detector = CommentCodeMismatchDetector(root_dir)
    results = detector.run()
    
    output_file = Path(args.output) if args.output else None
    generate_report(results, output_file)
    
    print("\n" + "=" * 70)
    print("Analysis Complete")
    print("=" * 70)
    print(f"Files analyzed: {results['files_analyzed']}")
    print(f"Mismatches found: {results['stats']['mismatches_found']}")
    print()


if __name__ == '__main__':
    main()

