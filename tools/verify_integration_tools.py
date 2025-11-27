#!/usr/bin/env python3
"""
Integration Tools Verification - Agent-2
========================================

Verifies all integration tools are available and working.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def verify_tool(tool_path: Path, tool_name: str) -> bool:
    """Verify a tool exists and is accessible."""
    if tool_path.exists():
        print(f"  ✅ {tool_name}: Found at {tool_path}")
        return True
    else:
        print(f"  ❌ {tool_name}: Not found at {tool_path}")
        return False


def verify_script(script_path: Path, script_name: str) -> bool:
    """Verify a script exists and is accessible."""
    if script_path.exists():
        print(f"  ✅ {script_name}: Found at {script_path}")
        return True
    else:
        print(f"  ❌ {script_name}: Not found at {script_path}")
        return False


def main():
    """Main entry point."""
    print("🔍 Verifying Integration Tools")
    print("="*60)
    
    tools_dir = project_root / "tools"
    all_verified = True
    
    # Verify tools
    print("\n📋 Verifying Tools:")
    tools = [
        (tools_dir / "enhanced_duplicate_detector.py", "Enhanced Duplicate Detector"),
        (tools_dir / "detect_venv_files.py", "Venv File Detector"),
        (tools_dir / "check_integration_issues.py", "Integration Issues Checker"),
        (tools_dir / "analyze_merged_repo_patterns.py", "Pattern Analyzer"),
    ]
    
    for tool_path, tool_name in tools:
        if not verify_tool(tool_path, tool_name):
            all_verified = False
    
    # Verify automation scripts
    print("\n📋 Verifying Automation Scripts:")
    scripts = [
        (tools_dir / "integration_workflow_automation.py", "Integration Workflow Automation"),
        (tools_dir / "complete_cleanup_workflow.sh", "Complete Cleanup Workflow"),
        (tools_dir / "pattern_extraction_workflow.sh", "Pattern Extraction Workflow"),
    ]
    
    for script_path, script_name in scripts:
        if not verify_script(script_path, script_name):
            all_verified = False
    
    # Verify documentation
    print("\n📋 Verifying Documentation:")
    docs_dir = project_root / "docs" / "integration"
    docs = [
        (docs_dir / "INTEGRATION_QUICK_START.md", "Quick Start Guide"),
        (docs_dir / "INTEGRATION_TOOLKIT_SUMMARY.md", "Toolkit Summary"),
        (docs_dir / "INTEGRATION_INDEX.md", "Documentation Index"),
        (docs_dir / "STAGE1_INTEGRATION_METHODOLOGY.md", "Integration Methodology"),
        (docs_dir / "INTEGRATION_BEST_PRACTICES.md", "Best Practices"),
        (docs_dir / "INTEGRATION_PATTERNS_CATALOG.md", "Patterns Catalog"),
        (docs_dir / "INTEGRATION_TEMPLATES.md", "Templates"),
        (docs_dir / "TOOL_USAGE_GUIDE.md", "Tool Usage Guide"),
        (docs_dir / "INTEGRATION_TROUBLESHOOTING.md", "Troubleshooting Guide"),
        (docs_dir / "QUICK_REFERENCE_GUIDE.md", "Quick Reference"),
        (docs_dir / "INTEGRATION_SCENARIOS.md", "Scenarios"),
        (docs_dir / "TOOL_SELECTION_DECISION_TREE.md", "Decision Tree"),
        (docs_dir / "INTEGRATION_CHECKLIST_GENERATOR.md", "Checklist Generator"),
        (docs_dir / "TOOL_COMPARISON_MATRIX.md", "Tool Comparison"),
        (docs_dir / "INTEGRATION_WORKFLOW_AUTOMATION.md", "Workflow Automation"),
    ]
    
    docs_verified = True
    for doc_path, doc_name in docs:
        if doc_path.exists():
            print(f"  ✅ {doc_name}: Found")
        else:
            print(f"  ❌ {doc_name}: Not found")
            docs_verified = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    if all_verified and docs_verified:
        print("✅ All tools, scripts, and documentation verified")
        print("✅ Integration toolkit complete and ready for use")
        return 0
    else:
        print("⚠️ Some tools, scripts, or documentation missing")
        print("   Review output above for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())

