#!/usr/bin/env python3
"""
Phase 0: Syntax Error Finder - SIGNAL Tools Only
==================================================

Finds all syntax errors in SIGNAL tools only (Phase 0 of V2 Compliance Refactoring Plan).

Reference: docs/V2_COMPLIANCE_REFACTORING_PLAN.md - Phase 0

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-21
Priority: CRITICAL - Phase 0 execution
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class SyntaxErrorFinder:
    """
    Find syntax errors in SIGNAL tools only.
    
    Filters to SIGNAL tools using Phase -1 classification results.
    """

    def __init__(self, tools_dir: Path = None):
        """Initialize syntax error finder."""
        self.tools_dir = tools_dir or Path(__file__).parent
        self.project_root = self.tools_dir.parent
        
        # Load SIGNAL tool classification
        self.signal_files = self.load_signal_classification()

    def load_signal_classification(self) -> set:
        """Load SIGNAL tool file paths from Phase -1 classification."""
        classification_file = self.tools_dir / "TOOL_CLASSIFICATION.json"
        
        if not classification_file.exists():
            print(f"⚠️  Warning: Classification file not found: {classification_file}")
            print("   Proceeding without filtering (will check all tools)")
            return set()
        
        try:
            with open(classification_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get all SIGNAL tool file paths
            signal_files = set()
            for tool in data.get('signal', []):
                file_path = tool.get('file', '')
                # Normalize path separators
                file_path = file_path.replace('\\', '/')
                signal_files.add(file_path)
            
            print(f"✅ Loaded {len(signal_files)} SIGNAL tools from classification")
            return signal_files
        
        except Exception as e:
            print(f"⚠️  Error loading classification: {e}")
            print("   Proceeding without filtering (will check all tools)")
            return set()

    def is_signal_tool(self, file_path: Path) -> bool:
        """Check if a file is a SIGNAL tool."""
        if not self.signal_files:
            # No classification loaded, check all files
            return True
        
        # Normalize path for comparison
        relative_path = str(file_path.relative_to(self.project_root)).replace('\\', '/')
        return relative_path in self.signal_files

    def check_syntax_error(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Check a Python file for syntax errors.
        
        Returns error dict if syntax error found, None otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse the file
            ast.parse(content, filename=str(file_path))
            
            # No syntax error
            return None
        
        except SyntaxError as e:
            return {
                "file": str(file_path.relative_to(self.project_root)),
                "error_type": "SyntaxError",
                "message": str(e),
                "line": e.lineno,
                "offset": e.offset,
                "text": e.text,
            }
        
        except Exception as e:
            # Other errors (encoding, etc.)
            return {
                "file": str(file_path.relative_to(self.project_root)),
                "error_type": type(e).__name__,
                "message": str(e),
                "line": None,
                "offset": None,
                "text": None,
            }

    def find_all_syntax_errors(self) -> Dict[str, Any]:
        """
        Find all syntax errors in SIGNAL tools.
        
        Returns results dictionary with syntax errors found.
        """
        print("🔍 Scanning SIGNAL tools for syntax errors...")
        
        # Find all Python files
        tool_files = list(self.tools_dir.rglob("*.py"))
        
        # Filter out special files
        tool_files = [
            f for f in tool_files 
            if f.name not in ['__init__.py', '__main__.py', 'setup.py']
            and '__pycache__' not in str(f)
            and '.pyc' not in str(f)
        ]
        
        print(f"📊 Found {len(tool_files)} Python files to check")
        
        syntax_errors = []
        checked_count = 0
        signal_count = 0
        
        for tool_file in tool_files:
            # Filter to SIGNAL tools only
            if not self.is_signal_tool(tool_file):
                continue
            
            signal_count += 1
            checked_count += 1
            
            if checked_count % 100 == 0:
                print(f"   Progress: {checked_count} SIGNAL tools checked...")
            
            error = self.check_syntax_error(tool_file)
            if error:
                syntax_errors.append(error)
        
        print(f"✅ Checked {signal_count} SIGNAL tools")
        print(f"❌ Found {len(syntax_errors)} syntax errors")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_signal_tools_checked": signal_count,
            "syntax_errors_found": len(syntax_errors),
            "syntax_errors": syntax_errors,
        }
        
        return results

    def generate_report(self, results: Dict[str, Any], output_path: Path = None) -> str:
        """Generate syntax error report."""
        output_path = output_path or self.tools_dir / "PHASE0_SYNTAX_ERRORS_REPORT.md"
        
        doc = f"""# Phase 0: Syntax Errors Report - SIGNAL Tools Only

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Phase**: Phase 0 of V2 Compliance Refactoring Plan  
**Scope**: SIGNAL tools only (after Phase -1 classification)

---

## 📊 Summary

- **SIGNAL Tools Checked**: {results['total_signal_tools_checked']}
- **Syntax Errors Found**: {results['syntax_errors_found']}
- **Status**: {'✅ No syntax errors!' if results['syntax_errors_found'] == 0 else '❌ Syntax errors need fixing'}

---

## ❌ Syntax Errors Found ({results['syntax_errors_found']})

**Action Required**: Fix all syntax errors before proceeding with refactoring.

"""
        
        if results['syntax_errors']:
            for i, error in enumerate(results['syntax_errors'], 1):
                doc += f"""### {i}. {error['file']}

- **Error Type**: `{error['error_type']}`
- **Line**: {error.get('line', 'Unknown')}
- **Offset**: {error.get('offset', 'Unknown')}
- **Message**: `{error['message']}`
"""
                if error.get('text'):
                    doc += f"- **Code**: `{error['text'].strip()}`\n"
                doc += "\n"
        else:
            doc += "✅ **No syntax errors found in SIGNAL tools!**\n\n"
            doc += "Phase 0 is complete - all SIGNAL tools parse successfully.\n\n"
        
        doc += """
---

## 📋 Next Steps

1. **Fix Syntax Errors**: Fix all syntax errors listed above
2. **Verify Fixes**: Re-run this tool to verify all errors are resolved
3. **Proceed to Phase 1**: Once all syntax errors are fixed, proceed to Phase 1 (SSOT Tags)

---

## 🔗 References

- **V2 Compliance Refactoring Plan**: `docs/V2_COMPLIANCE_REFACTORING_PLAN.md`
- **Phase -1 Classification**: `tools/TOOL_CLASSIFICATION.md`
- **Syntax Error Finder**: `tools/phase0_syntax_error_finder.py`

---

*Generated by Phase 0 Syntax Error Finder*
*Part of V2 Compliance Refactoring Plan - Phase 0*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        return str(output_path)

    def save_json_results(self, results: Dict[str, Any], output_path: Path = None) -> str:
        """Save results as JSON for programmatic use."""
        output_path = output_path or self.tools_dir / "PHASE0_SYNTAX_ERRORS.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return str(output_path)


def main():
    """Main entry point for Phase 0 syntax error finding."""
    print("🚀 Phase 0: Syntax Error Finder - SIGNAL Tools Only")
    print("=" * 60)
    print("Reference: docs/V2_COMPLIANCE_REFACTORING_PLAN.md - Phase 0")
    print()
    
    finder = SyntaxErrorFinder()
    results = finder.find_all_syntax_errors()
    
    print()
    print("📊 Results:")
    print(f"   ✅ SIGNAL Tools Checked: {results['total_signal_tools_checked']}")
    print(f"   {'✅' if results['syntax_errors_found'] == 0 else '❌'} Syntax Errors Found: {results['syntax_errors_found']}")
    print()
    
    if results['syntax_errors_found'] > 0:
        print("❌ Syntax errors found! Details:")
        for error in results['syntax_errors'][:10]:  # Show first 10
            print(f"   - {error['file']}: Line {error.get('line', '?')} - {error['message'][:60]}")
        if len(results['syntax_errors']) > 10:
            print(f"   ... and {len(results['syntax_errors']) - 10} more")
    else:
        print("✅ No syntax errors found! Phase 0 complete!")
    
    print()
    
    # Generate report
    doc_path = finder.generate_report(results)
    print(f"📄 Report generated: {doc_path}")
    
    # Save JSON results
    json_path = finder.save_json_results(results)
    print(f"💾 JSON results: {json_path}")
    
    print()
    if results['syntax_errors_found'] > 0:
        print("📋 Next Steps:")
        print("   1. Fix syntax errors listed in report")
        print("   2. Re-run this tool to verify fixes")
        print("   3. Proceed to Phase 1 after all errors are fixed")
    else:
        print("✅ Phase 0 complete - ready for Phase 1!")
    
    print()
    print("🐝 WE. ARE. SWARM. PHASE 0 SYNTAX ERROR FINDING COMPLETE. ⚡🔥")


if __name__ == "__main__":
    main()

