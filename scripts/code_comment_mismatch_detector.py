#!/usr/bin/env python3
"""
Code-Comment Mismatch Detector
==============================

Analyzes Python files to identify cases where code doesn't match comments.
Flags potential discrepancies for manual review.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-12
V2 Compliant: Yes
"""

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("❌ ERROR: pyyaml not installed. Install with: pip install pyyaml")
    sys.exit(1)


class CodeCommentAnalyzer:
    """Analyzes code-comment mismatches in Python files."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the analyzer."""
        if project_root is None:
            # Try to find project root by looking for common markers
            script_path = Path(__file__).resolve()
            current = script_path.parent
            # Look for project root (contains .git, agent_workspaces, or src/)
            while current != current.parent:
                if (current / "src").exists() or (current / "agent_workspaces").exists() or (current / ".git").exists():
                    self.project_root = current
                    break
                current = current.parent
            else:
                # Fallback to script's parent's parent's parent
                self.project_root = script_path.parent.parent.parent
        else:
            self.project_root = Path(project_root).resolve()
        self.src_dir = self.project_root / "src"
        self.issues = []

    def analyze_file(self, file_path: Path) -> List[Dict]:
        """Analyze a single Python file for code-comment mismatches."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return [{"type": "error", "message": f"Could not read file: {e}"}]

        # Parse AST for structural analysis
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError:
            return [{"type": "error", "message": "Syntax error in file"}]

        # Check 1: Function docstrings vs implementation
        issues.extend(self._check_function_docstrings(tree, lines, file_path))
        
        # Check 2: Class docstrings vs implementation
        issues.extend(self._check_class_docstrings(tree, lines, file_path))
        
        # Check 3: Inline comments vs adjacent code
        issues.extend(self._check_inline_comments(lines, file_path))
        
        # Check 4: TODO/FIXME comments without corresponding code
        issues.extend(self._check_todo_comments(lines, file_path))
        
        # Check 5: Parameter documentation vs actual parameters
        issues.extend(self._check_parameter_docs(tree, lines, file_path))
        
        # Check 6: Return type documentation vs actual returns
        issues.extend(self._check_return_docs(tree, lines, file_path))
        
        # Check 7: Deprecated comments vs actual usage
        issues.extend(self._check_deprecated_comments(lines, file_path))

        return issues

    def _check_function_docstrings(self, tree: ast.AST, lines: List[str], file_path: Path) -> List[Dict]:
        """Check if function docstrings match implementation."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Check if docstring mentions parameters that don't exist
                    func_params = [arg.arg for arg in node.args.args]
                    if 'self' in func_params:
                        func_params.remove('self')
                    if 'cls' in func_params:
                        func_params.remove('cls')
                    
                    # Look for parameter mentions in docstring
                    # Exclude docstring section headers (Args:, Returns:, Raises:, etc.)
                    docstring_sections = ['Args', 'Returns', 'Raises', 'Yields', 'Note', 'Example', 'Warning']
                    param_pattern = r'(\w+)\s*:.*?(\w+)'
                    doc_params = re.findall(r':param\s+(\w+)', docstring, re.IGNORECASE)
                    doc_params.extend(re.findall(r':type\s+(\w+)', docstring, re.IGNORECASE))
                    # Only extract from Args section, not Returns section
                    args_section = re.search(r'Args?:.*?(?=Returns?:|Raises?:|Yields?:|$)', docstring, re.IGNORECASE | re.DOTALL)
                    if args_section:
                        doc_params.extend(re.findall(r'(\w+)\s*:', args_section.group(0), re.IGNORECASE))
                    # Filter out docstring section headers
                    doc_params = [p for p in doc_params if p not in docstring_sections]
                    
                    # Check for documented params that don't exist
                    for doc_param in set(doc_params):
                        if doc_param not in func_params:
                            issues.append({
                                "type": "parameter_mismatch",
                                "severity": "medium",
                                "line": node.lineno,
                                "function": node.name,
                                "message": f"Docstring documents parameter '{doc_param}' but function doesn't have it",
                                "file": str(file_path.relative_to(self.project_root))
                            })
                    
                    # Check for params without documentation
                    for param in func_params:
                        if param not in doc_params and len(func_params) > 0:
                            # Only flag if docstring has Args section
                            if ':param' in docstring or 'Args:' in docstring:
                                issues.append({
                                    "type": "missing_documentation",
                                    "severity": "low",
                                    "line": node.lineno,
                                    "function": node.name,
                                    "message": f"Parameter '{param}' not documented in docstring",
                                    "file": str(file_path.relative_to(self.project_root))
                                })

        return issues

    def _check_class_docstrings(self, tree: ast.AST, lines: List[str], file_path: Path) -> List[Dict]:
        """Check if class docstrings match implementation."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Check if docstring mentions methods that don't exist
                    class_methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    
                    # Look for method mentions in docstring
                    method_pattern = r'(\w+)\(\)'
                    doc_methods = re.findall(method_pattern, docstring)
                    
                    # Check for documented methods that don't exist
                    for doc_method in set(doc_methods):
                        if doc_method not in class_methods and doc_method not in ['__init__', '__str__', '__repr__']:
                            issues.append({
                                "type": "method_mismatch",
                                "severity": "medium",
                                "line": node.lineno,
                                "class": node.name,
                                "message": f"Docstring mentions method '{doc_method}()' but class doesn't have it",
                                "file": str(file_path.relative_to(self.project_root))
                            })

        return issues

    def _check_inline_comments(self, lines: List[str], file_path: Path) -> List[Dict]:
        """Check if inline comments match adjacent code."""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Look for comments that describe specific behavior
            comment_match = re.search(r'#\s*(.+)$', line)
            if comment_match:
                comment = comment_match.group(1).strip()
                
                # Check for common mismatch patterns
                # Look ahead up to 5 lines for return statements (not just next line)
                if i < len(lines):
                    next_lines = lines[i:min(i+5, len(lines))]
                    next_lines_text = '\n'.join(next_lines)
                    next_line = lines[i].strip() if i < len(lines) else ""
                    
                    # Pattern: Comment says "returns X" but code doesn't return
                    if re.search(r'returns?\s+(\w+)', comment, re.IGNORECASE):
                        # Check if return appears in next 5 lines (not just next line)
                        if 'return' not in next_lines_text and not next_line.startswith('def'):
                            # Only flag if we're in a function context and no return found
                            issues.append({
                                "type": "return_mismatch",
                                "severity": "medium",
                                "line": i,
                                "message": f"Comment says 'returns' but no return found in next 5 lines: {comment[:50]}",
                                "file": str(file_path.relative_to(self.project_root))
                            })
                    
                    # Pattern: Comment says "sets X" but code doesn't assign
                    if re.search(r'sets?\s+(\w+)', comment, re.IGNORECASE):
                        if '=' not in next_line and not next_line.startswith('def'):
                            issues.append({
                                "type": "assignment_mismatch",
                                "severity": "low",
                                "line": i,
                                "message": f"Comment says 'sets' but next line doesn't assign: {comment[:50]}",
                                "file": str(file_path.relative_to(self.project_root))
                            })
                    
                    # Pattern: Comment says "calls X" but code doesn't call
                    if re.search(r'calls?\s+(\w+)', comment, re.IGNORECASE):
                        if '(' not in next_line or ')' not in next_line:
                            issues.append({
                                "type": "call_mismatch",
                                "severity": "low",
                                "line": i,
                                "message": f"Comment says 'calls' but next line doesn't appear to call: {comment[:50]}",
                                "file": str(file_path.relative_to(self.project_root))
                            })

        return issues

    def _check_todo_comments(self, lines: List[str], file_path: Path) -> List[Dict]:
        """Check for TODO/FIXME comments that might be outdated."""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Look for TODO/FIXME comments
            todo_match = re.search(r'#\s*(TODO|FIXME|XXX|HACK|NOTE):\s*(.+)', line, re.IGNORECASE)
            if todo_match:
                todo_type = todo_match.group(1).upper()
                todo_text = todo_match.group(2).strip()
                
                # Check if TODO might be completed (code after it)
                if i < len(lines):
                    next_lines = '\n'.join(lines[i:min(i+10, len(lines))])
                    # If TODO says "implement X" and X appears to be implemented
                    if 'implement' in todo_text.lower() or 'add' in todo_text.lower():
                        # Check if the thing mentioned is actually implemented
                        mentioned_item = re.search(r'(implement|add)\s+(\w+)', todo_text, re.IGNORECASE)
                        if mentioned_item:
                            item_name = mentioned_item.group(2)
                            if f'def {item_name}' in next_lines or f'class {item_name}' in next_lines:
                                issues.append({
                                    "type": "completed_todo",
                                    "severity": "low",
                                    "line": i,
                                    "message": f"{todo_type} comment might be completed: {todo_text[:50]}",
                                    "file": str(file_path.relative_to(self.project_root))
                                })

        return issues

    def _check_parameter_docs(self, tree: ast.AST, lines: List[str], file_path: Path) -> List[Dict]:
        """Check if parameter documentation matches actual parameters."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    func_params = [arg.arg for arg in node.args.args]
                    if 'self' in func_params:
                        func_params.remove('self')
                    if 'cls' in func_params:
                        func_params.remove('cls')
                    
                    # Check for type hints in function signature
                    type_hints = {}
                    for arg in node.args.args:
                        if arg.annotation:
                            type_hints[arg.arg] = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else str(arg.annotation)
                    
                    # Check docstring for type information
                    for param in func_params:
                        param_doc = re.search(rf':type\s+{param}:\s*(.+)', docstring, re.IGNORECASE)
                        if param_doc:
                            doc_type = param_doc.group(1).strip()
                            # If function has type hint, check if it matches
                            if param in type_hints:
                                # Simple check - could be improved
                                if doc_type.lower() not in type_hints[param].lower() and type_hints[param].lower() not in doc_type.lower():
                                    issues.append({
                                        "type": "type_mismatch",
                                        "severity": "medium",
                                        "line": node.lineno,
                                        "function": node.name,
                                        "message": f"Type documentation for '{param}' doesn't match type hint",
                                        "file": str(file_path.relative_to(self.project_root))
                                    })

        return issues

    def _check_return_docs(self, tree: ast.AST, lines: List[str], file_path: Path) -> List[Dict]:
        """Check if return documentation matches actual returns."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Check if function has return type hint
                    return_type = None
                    if node.returns:
                        return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
                    
                    # Check if docstring mentions return type
                    return_doc = re.search(r':rtype:\s*(.+)', docstring, re.IGNORECASE)
                    if return_doc:
                        doc_return_type = return_doc.group(1).strip()
                        if return_type:
                            # Simple check - could be improved
                            if doc_return_type.lower() not in return_type.lower() and return_type.lower() not in doc_return_type.lower():
                                issues.append({
                                    "type": "return_type_mismatch",
                                    "severity": "medium",
                                    "line": node.lineno,
                                    "function": node.name,
                                    "message": f"Return type documentation doesn't match type hint",
                                    "file": str(file_path.relative_to(self.project_root))
                                })
                    
                    # Check if function actually returns something
                    has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                    if ':returns:' in docstring or ':return:' in docstring:
                        if not has_return and return_type != 'None':
                            issues.append({
                                "type": "return_mismatch",
                                "severity": "high",
                                "line": node.lineno,
                                "function": node.name,
                                "message": f"Docstring says function returns something but no return statement found",
                                "file": str(file_path.relative_to(self.project_root))
                            })

        return issues

    def _check_deprecated_comments(self, lines: List[str], file_path: Path) -> List[Dict]:
        """Check for deprecated comments that might be outdated."""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Look for deprecated markers
            if re.search(r'deprecated|deprecat', line, re.IGNORECASE):
                # Check if deprecated code is still being used elsewhere
                # This is a simple check - could be improved with cross-file analysis
                if 'def ' in line or 'class ' in line:
                    # Check if it's actually marked as deprecated in docstring
                    if i < len(lines):
                        next_lines = '\n'.join(lines[i:min(i+5, len(lines))])
                        if '@deprecated' not in next_lines and '.. deprecated::' not in next_lines:
                            issues.append({
                                "type": "deprecated_marker",
                                "severity": "low",
                                "line": i,
                                "message": f"Comment mentions 'deprecated' but not properly marked: {line[:50]}",
                                "file": str(file_path.relative_to(self.project_root))
                            })

        return issues

    def scan_codebase(self) -> Dict:
        """Scan the entire codebase for code-comment mismatches."""
        all_issues = []
        files_scanned = 0
        
        if not self.src_dir.exists():
            return {
                "error": f"Source directory not found: {self.src_dir}",
                "issues": [],
                "files_scanned": 0
            }
        
        print(f"🔍 Scanning {self.src_dir} for code-comment mismatches...")
        
        for py_file in self.src_dir.rglob("*.py"):
            files_scanned += 1
            file_issues = self.analyze_file(py_file)
            all_issues.extend(file_issues)
            
            if file_issues:
                print(f"  ⚠️  {py_file.relative_to(self.project_root)}: {len(file_issues)} potential issues")
        
        # Categorize issues
        categorized = {
            "high": [i for i in all_issues if i.get("severity") == "high"],
            "medium": [i for i in all_issues if i.get("severity") == "medium"],
            "low": [i for i in all_issues if i.get("severity") == "low"],
            "error": [i for i in all_issues if i.get("type") == "error"]
        }
        
        return {
            "total_issues": len(all_issues),
            "files_scanned": files_scanned,
            "categorized": categorized,
            "issues": all_issues
        }

    def generate_report(self, results: Dict, output_path: Optional[Path] = None) -> str:
        """Generate a markdown report from analysis results."""
        report_lines = [
            "# Code-Comment Mismatch Analysis Report",
            "",
            f"**Date**: 2025-12-12",
            f"**Agent**: Agent-2 (Architecture & Design Specialist)",
            f"**Status**: ✅ **ANALYSIS COMPLETE**",
            "",
            "---",
            "",
            "## Summary",
            "",
            f"- **Files Scanned**: {results['files_scanned']}",
            f"- **Total Issues Found**: {results['total_issues']}",
            f"- **High Severity**: {len(results['categorized']['high'])}",
            f"- **Medium Severity**: {len(results['categorized']['medium'])}",
            f"- **Low Severity**: {len(results['categorized']['low'])}",
            "",
            "---",
            ""
        ]
        
        # High severity issues
        if results['categorized']['high']:
            report_lines.extend([
                "## 🔴 High Severity Issues",
                ""
            ])
            for issue in results['categorized']['high'][:20]:  # Top 20
                report_lines.extend([
                    f"### {issue.get('file', 'unknown')}:{issue.get('line', '?')}",
                    f"- **Type**: {issue.get('type', 'unknown')}",
                    f"- **Function/Class**: {issue.get('function', issue.get('class', 'N/A'))}",
                    f"- **Message**: {issue.get('message', 'No message')}",
                    ""
                ])
        
        # Medium severity issues
        if results['categorized']['medium']:
            report_lines.extend([
                "## 🟡 Medium Severity Issues",
                ""
            ])
            for issue in results['categorized']['medium'][:30]:  # Top 30
                report_lines.extend([
                    f"### {issue.get('file', 'unknown')}:{issue.get('line', '?')}",
                    f"- **Type**: {issue.get('type', 'unknown')}",
                    f"- **Function/Class**: {issue.get('function', issue.get('class', 'N/A'))}",
                    f"- **Message**: {issue.get('message', 'No message')}",
                    ""
                ])
        
        # Issue types summary
        issue_types = {}
        for issue in results['issues']:
            issue_type = issue.get('type', 'unknown')
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
        report_lines.extend([
            "## Issue Types Summary",
            ""
        ])
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"- **{issue_type}**: {count}")
        
        report_lines.extend([
            "",
            "---",
            "",
            "*Analysis generated by code-comment mismatch detector*"
        ])
        
        report = '\n'.join(report_lines)
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"💾 Report saved to: {output_path}")
        
        return report


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze codebase for code-comment mismatches"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to save the markdown report",
        default=None
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Path to save JSON results",
        default=None
    )

    args = parser.parse_args()

    analyzer = CodeCommentAnalyzer()
    results = analyzer.scan_codebase()
    
    # Generate report
    if args.output:
        report = analyzer.generate_report(results, args.output)
    else:
        report = analyzer.generate_report(results)
        print("\n" + "="*60)
        print(report)
    
    # Save JSON if requested
    if args.json:
        import json
        args.json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"💾 JSON results saved to: {args.json}")


if __name__ == "__main__":
    main()

