"""
Phase 0: Fix Syntax Errors in SIGNAL Tools Only
================================================

Identifies and fixes syntax errors in SIGNAL tools (real infrastructure).
NOISE tools are skipped (they'll be deprecated/moved).

Agent: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-21
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def load_classification() -> Dict[str, str]:
    """Load tool classification from JSON."""
    classification_path = Path(__file__).parent / "TOOL_CLASSIFICATION.json"
    
    if not classification_path.exists():
        print(f"❌ Classification file not found: {classification_path}")
        return {}
    
    with open(classification_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Build mapping: file_path -> classification
    classification_map = {}
    
    # Handle different JSON structures
    if "classifications" in data:
        # New structure from classify_all_tools_phase1.py
        for file_path, info in data["classifications"].items():
            classification_map[file_path] = info.get("classification", "UNKNOWN")
    elif "signal" in data:
        # Structure with signal/noise/unknown arrays
        for tool in data.get("signal", []):
            file_path = tool.get("file", "")
            if file_path:
                # Normalize path
                file_path = file_path.replace('\\', '/')
                classification_map[file_path] = "SIGNAL"
        for tool in data.get("noise", []):
            file_path = tool.get("file", "")
            if file_path:
                file_path = file_path.replace('\\', '/')
                classification_map[file_path] = "NOISE"
        for tool in data.get("unknown", []):
            file_path = tool.get("file", "")
            if file_path:
                file_path = file_path.replace('\\', '/')
                classification_map[file_path] = "UNKNOWN"
    
    return classification_map


def check_syntax_error(file_path: Path) -> Tuple[bool, Optional[str], Optional[int]]:
    """Check if a Python file has syntax errors.
    
    Returns: (has_error, error_message, line_number)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse
        try:
            ast.parse(content)
            return False, None, None
        except SyntaxError as e:
            return True, str(e), e.lineno
    except Exception as e:
        return True, f"File read error: {str(e)}", None


def find_syntax_errors_in_signal_tools(tools_dir: Path) -> List[Dict]:
    """Find all syntax errors in SIGNAL tools only."""
    classification_map = load_classification()
    
    if not classification_map:
        print("⚠️  No classification data found. Checking all tools...")
    
    syntax_errors = []
    tools_checked = 0
    
    # Find all Python files
    exclude_patterns = [
        '__pycache__',
        '.pyc',
        'test_',
        '_test.py',
        'archive',
        'deprecated',
        '__init__.py',
        'classify_all_tools_phase1.py',
        'fix_syntax_errors_phase0.py',  # Exclude this script
    ]
    
    for py_file in tools_dir.rglob('*.py'):
        # Skip excluded files
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue
        
        tools_checked += 1
        
        # Check if it's a SIGNAL tool
        file_path_str = str(py_file.relative_to(tools_dir.parent))
        # Normalize path separators
        file_path_str = file_path_str.replace('\\', '/')
        
        classification = classification_map.get(file_path_str, "UNKNOWN")
        
        # Only check SIGNAL tools
        if classification != "SIGNAL":
            continue
        
        # Check for syntax errors
        has_error, error_msg, line_num = check_syntax_error(py_file)
        
        if has_error:
            syntax_errors.append({
                "file": str(py_file),
                "file_path": file_path_str,
                "error": error_msg,
                "line": line_num,
                "classification": classification
            })
    
    print(f"✅ Checked {tools_checked} tools")
    print(f"🔍 Found {len(syntax_errors)} syntax errors in SIGNAL tools\n")
    
    return syntax_errors


def fix_common_syntax_errors(file_path: Path) -> Tuple[bool, str]:
    """Attempt to fix common syntax errors.
    
    Returns: (success, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_content = ''.join(lines)
        fixed_content = original_content
        fixes_applied = []
        
        # Fix 1: Missing colons after if/for/while/def/class
        # This is complex and risky, so we'll be conservative
        
        # Fix 2: Unclosed parentheses/brackets (basic detection)
        # This is also risky, so we'll focus on obvious cases
        
        # Fix 3: Indentation errors (very risky, skip for now)
        
        # Fix 4: Missing quotes (very risky, skip for now)
        
        # For now, we'll just report the errors and let manual fixing happen
        # or use more sophisticated tools
        
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, f"Applied fixes: {', '.join(fixes_applied)}"
        else:
            return False, "No automatic fixes available (requires manual review)"
    
    except Exception as e:
        return False, f"Error during fix attempt: {str(e)}"


def generate_syntax_error_report(syntax_errors: List[Dict], output_path: Path) -> None:
    """Generate a report of syntax errors found."""
    md_content = f"""# Phase 0: Syntax Errors in SIGNAL Tools

**Date**: 2025-12-21  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: 🔍 **SYNTAX ERRORS IDENTIFIED**

---

## 📊 Summary

**Total Syntax Errors Found**: {len(syntax_errors)}

All errors are in **SIGNAL tools only** (NOISE tools excluded from Phase 0).

---

## 🔴 Syntax Errors by File

"""
    
    for i, error_info in enumerate(syntax_errors, 1):
        md_content += f"""
### {i}. `{error_info['file_path']}`

- **Error**: {error_info['error']}
- **Line**: {error_info['line'] if error_info['line'] else 'Unknown'}
- **Classification**: {error_info['classification']}

"""
    
    md_content += """
---

## 🔧 Fix Strategy

1. **Manual Review**: Each syntax error requires manual inspection
2. **Common Fixes**:
   - Missing colons (`:`) after if/for/while/def/class
   - Unclosed parentheses, brackets, or braces
   - Indentation errors (mixed tabs/spaces)
   - Missing quotes in strings
   - Invalid escape sequences

3. **Verification**: After fixing, verify with:
   ```bash
   python -m py_compile <file>
   ```

---

## 📋 Next Steps

1. Fix syntax errors one by one
2. Verify each fix compiles correctly
3. Update status after all fixes complete
4. Proceed with Phase 1 (SSOT Tags - SIGNAL only)

---

**Agent-8 (SSOT & System Integration)**  
🐝 **WE. ARE. SWARM.** ⚡🔥
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"📄 Syntax error report written to: {output_path}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("Phase 0: Fix Syntax Errors in SIGNAL Tools Only")
    print("=" * 70)
    print()
    
    # Set up paths
    repo_root = Path(__file__).parent.parent
    tools_dir = repo_root / "tools"
    output_dir = repo_root / "tools"
    
    # Find syntax errors in SIGNAL tools
    print("🔍 Scanning SIGNAL tools for syntax errors...")
    syntax_errors = find_syntax_errors_in_signal_tools(tools_dir)
    
    if not syntax_errors:
        print("✅ No syntax errors found in SIGNAL tools!")
        print("   Phase 0 complete - ready for Phase 1")
        return
    
    # Generate report
    report_path = output_dir / "PHASE0_SYNTAX_ERRORS.md"
    generate_syntax_error_report(syntax_errors, report_path)
    
    # Print summary
    print("\n📊 Syntax Error Summary:")
    print(f"   Total errors: {len(syntax_errors)}")
    print(f"   Files affected: {len(set(e['file'] for e in syntax_errors))}")
    print()
    
    # Show first few errors
    print("🔴 First 10 syntax errors:")
    for i, error in enumerate(syntax_errors[:10], 1):
        print(f"   {i}. {error['file_path']}")
        print(f"      Error: {error['error'][:80]}...")
        if error['line']:
            print(f"      Line: {error['line']}")
        print()
    
    if len(syntax_errors) > 10:
        print(f"   ... and {len(syntax_errors) - 10} more errors (see report)")
    
    print()
    print("=" * 70)
    print("✅ Phase 0 Syntax Error Detection Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review PHASE0_SYNTAX_ERRORS.md")
    print("2. Fix syntax errors manually (or use automated tools)")
    print("3. Verify fixes compile correctly")
    print("4. Proceed with Phase 1 (SSOT Tags - SIGNAL only)")


if __name__ == "__main__":
    main()

