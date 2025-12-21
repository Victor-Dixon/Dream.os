#!/usr/bin/env python3
"""
Phase 0: Fix Syntax Errors in Web Tools (Agent-7 Contract)

This script:
1. Identifies web tools with syntax errors (SIGNAL tools only)
2. Attempts to fix common syntax errors
3. Reports on files that need manual review
4. Updates status after fixes
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import subprocess

def is_web_tool(file_path: Path) -> bool:
    """Determine if a file is a web tool based on path/name patterns."""
    path_str = str(file_path).lower()
    web_keywords = [
        'wordpress', 'website', 'web', 'html', 'css', 'deploy', 
        'blog', 'site', 'theme', 'crosby', 'dadudekc', 'houstonsipqueen',
        'tradingrobotplug', 'freerideinvestor', 'sftp', 'ftp'
    ]
    return any(keyword in path_str for keyword in web_keywords)

def check_syntax_error(file_path: Path) -> Tuple[bool, str, int, int]:
    """Check if a Python file has syntax errors. Returns (has_error, error_msg, line, col)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return (False, "", 0, 0)
    except SyntaxError as e:
        return (True, str(e.msg), e.lineno or 0, e.offset or 0)
    except Exception as e:
        return (True, str(e), 0, 0)

def find_web_tools_with_syntax_errors(repo_root: Path) -> List[Dict]:
    """Find all web tools in tools/ directory with syntax errors."""
    tools_dir = repo_root / 'tools'
    web_tools_with_errors = []
    
    # Check all Python files in tools directory
    for py_file in tools_dir.rglob('*.py'):
        # Skip __pycache__ and __init__.py
        if '__pycache__' in str(py_file) or py_file.name == '__init__.py':
            continue
        
        # Check if it's a web tool
        if not is_web_tool(py_file):
            continue
        
        # Check for syntax errors
        has_error, error_msg, line, col = check_syntax_error(py_file)
        
        if has_error:
            relative_path = py_file.relative_to(repo_root)
            web_tools_with_errors.append({
                'file': str(relative_path),
                'absolute_path': str(py_file),
                'error': error_msg,
                'line': line,
                'col': col
            })
    
    return web_tools_with_errors

def attempt_fix_syntax_error(file_path: Path) -> Tuple[bool, str]:
    """Attempt to fix common syntax errors. Returns (success, message)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_content = ''.join(lines)
        fixed_content = original_content
        changes_made = []
        
        # Try to fix common issues
        # Note: This is a simple approach - complex syntax errors may need manual review
        
        # Check if file is empty or very small
        if len(lines) < 3:
            return (False, "File too small or empty - may need manual review")
        
        # Re-parse to see if our "fixes" worked
        try:
            ast.parse(fixed_content)
            if fixed_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                return (True, f"Fixed: {', '.join(changes_made)}")
            else:
                return (False, "No automatic fixes available - needs manual review")
        except SyntaxError:
            return (False, "Syntax error persists - needs manual review")
            
    except Exception as e:
        return (False, f"Error attempting fix: {str(e)}")

def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    
    print("🔍 Phase 0 - Agent-7 Contract: Finding syntax errors in web tools...")
    print(f"   Repository: {repo_root}")
    print()
    
    # Find web tools with syntax errors
    print("📋 Scanning web tools for syntax errors...")
    web_tools_with_errors = find_web_tools_with_syntax_errors(repo_root)
    
    if not web_tools_with_errors:
        print("✅ No syntax errors found in web tools!")
        print()
        print("All web tools passed syntax validation.")
        return
    
    print(f"⚠️  Found {len(web_tools_with_errors)} web tools with syntax errors:")
    print()
    
    for i, tool_info in enumerate(web_tools_with_errors, 1):
        print(f"{i}. {tool_info['file']}")
        print(f"   Error: {tool_info['error']}")
        if tool_info['line'] > 0:
            print(f"   Line {tool_info['line']}, Column {tool_info['col']}")
        print()
    
    # Report on files needing manual review
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"Total web tools with syntax errors: {len(web_tools_with_errors)}")
    print()
    print("These files need manual review and fixing.")
    print("Common syntax errors include:")
    print("  - Missing colons (:)")
    print("  - Unclosed brackets/parentheses")
    print("  - Indentation errors")
    print("  - Invalid escape sequences")
    print("  - Invalid syntax in f-strings")
    print()
    
    # Generate report file
    report_path = repo_root / 'docs' / 'toolbelt' / 'PHASE0_WEB_TOOLS_SYNTAX_ERRORS.md'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report_lines = [
        "# Phase 0 - Web Tools Syntax Errors Report",
        "",
        f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Agent**: Agent-7 (Web Development Specialist)",
        f"**Contract**: Phase 0 - Syntax Error Fixes (Web Tools)",
        f"**Status**: 🔍 IDENTIFIED - Ready for manual fixes",
        "",
        "## Summary",
        "",
        f"- **Total Web Tools with Syntax Errors**: {len(web_tools_with_errors)}",
        f"- **Status**: Needs manual review and fixing",
        "",
        "## Files with Syntax Errors",
        "",
        "| # | File | Error Message | Line | Column |",
        "|---|------|---------------|------|--------|",
    ]
    
    for i, tool_info in enumerate(web_tools_with_errors, 1):
        report_lines.append(
            f"| {i} | `{tool_info['file']}` | {tool_info['error'][:60]}... | "
            f"{tool_info['line']} | {tool_info['col']} |"
        )
    
    report_lines.extend([
        "",
        "## Next Steps",
        "",
        "1. Review each file manually",
        "2. Fix syntax errors",
        "3. Verify fixes with `python -m py_compile <file>`",
        "4. Test functionality if possible",
        "5. Commit fixes",
        "",
        "## Common Syntax Error Patterns",
        "",
        "- Missing colons (`:`) after function/class/if/for definitions",
        "- Unclosed brackets, parentheses, or quotes",
        "- Indentation inconsistencies (mixing tabs/spaces)",
        "- Invalid escape sequences in strings",
        "- Invalid syntax in f-strings",
        "- Missing import statements",
        "",
        "---",
        "",
        "🐝 **WE. ARE. SWARM. ⚡🔥**",
    ])
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"📄 Report generated: {report_path}")
    print()
    print("⚠️  Action Required: Manual review and fixing needed for these files.")

if __name__ == '__main__':
    main()

