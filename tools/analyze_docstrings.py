#!/usr/bin/env python3
"""
Docstring Coverage Analysis
===========================

Analyzes docstring coverage across the codebase and identifies methods missing documentation.

V2 Compliant: Automated documentation quality assurance
Author: Agent-8 (SSOT & System Integration)
Date: 2026-01-12
"""

import os
import ast
from pathlib import Path
from typing import List, Dict


def analyze_docstring_coverage(root_path: Path) -> Dict:
    """Analyze docstring coverage across the codebase."""
    coverage_data = {
        'files_analyzed': 0,
        'total_methods': 0,
        'methods_with_docstrings': 0,
        'missing_docstrings': [],
        'coverage_percentage': 0.0
    }

    for py_file in root_path.rglob('*.py'):
        if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'test', 'example']):
            continue

        try:
            coverage_data['files_analyzed'] += 1
            source = py_file.read_text(encoding='utf-8')
            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_'):
                    coverage_data['total_methods'] += 1

                    # Check if method has docstring
                    has_docstring = (
                        len(node.body) > 0 and
                        isinstance(node.body[0], ast.Expr) and
                        isinstance(node.body[0].value, ast.Str)
                    ) or (
                        len(node.body) > 0 and
                        isinstance(node.body[0], ast.Expr) and
                        isinstance(node.body[0].value, ast.Constant) and
                        isinstance(node.body[0].value.value, str)
                    )

                    if has_docstring:
                        coverage_data['methods_with_docstrings'] += 1
                    else:
                        coverage_data['missing_docstrings'].append({
                            'file': str(py_file),
                            'method': node.name,
                            'line': node.lineno
                        })

        except Exception as e:
            continue

    if coverage_data['total_methods'] > 0:
        coverage_data['coverage_percentage'] = (
            coverage_data['methods_with_docstrings'] / coverage_data['total_methods'] * 100
        )

    return coverage_data


def main():
    """Main entry point."""
    print('🔍 Analyzing docstring coverage...')
    coverage = analyze_docstring_coverage(Path('src'))

    print(f'Files analyzed: {coverage["files_analyzed"]}')
    print(f'Total public methods: {coverage["total_methods"]}')
    print(f'Methods with docstrings: {coverage["methods_with_docstrings"]}')
    print(f'Docstring coverage: {coverage["coverage_percentage"]:.1f}%')

    print(f'Missing docstrings: {len(coverage["missing_docstrings"])}')

    if len(coverage['missing_docstrings']) > 0:
        print('\nTop 20 missing docstrings:')
        for i, missing in enumerate(coverage['missing_docstrings'][:20]):
            file_path = missing['file'].replace('src\\', '').replace('src/', '')
            print(f'  {i+1}. {file_path}:{missing["line"]} - {missing["method"]}')

        # Save detailed report
        with open('docstring_coverage_report.txt', 'w') as f:
            f.write('Docstring Coverage Analysis Report\n')
            f.write('=' * 40 + '\n\n')
            f.write(f'Files analyzed: {coverage["files_analyzed"]}\n')
            f.write(f'Total public methods: {coverage["total_methods"]}\n')
            f.write(f'Methods with docstrings: {coverage["methods_with_docstrings"]}\n')
            f.write(f'Docstring coverage: {coverage["coverage_percentage"]:.1f}%\n\n')

            f.write('Missing Docstrings:\n')
            f.write('-' * 20 + '\n')
            for missing in coverage['missing_docstrings']:
                file_path = missing['file'].replace('src\\', '').replace('src/', '')
                f.write(f'{file_path}:{missing["line"]} - {missing["method"]}\n')

        print(f'\n📋 Detailed report saved to: docstring_coverage_report.txt')


if __name__ == "__main__":
    main()