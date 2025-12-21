#!/usr/bin/env python3
"""
Analyze Integration Tools for Function Size Violations
======================================================

Analyzes ~53 Integration SIGNAL tools for Phase 2 preparation.
Identifies functions >30 lines and common refactoring patterns.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-21
Task: Phase 2 Preparation - Function Refactoring Analysis
"""

import ast
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def is_integration_tool(file_path: str) -> bool:
    """Check if a tool is integration-related."""
    integration_patterns = [
        "integration",
        "integrate",
        "validator",
        "verify",
        "check",
        "coordination",
        "communication",
        "messaging",
        "orchestrator",
        "functionality",
    ]
    
    file_str = file_path.lower()
    name_str = Path(file_path).stem.lower()
    
    if "integration" in file_str or "communication" in file_str or "coordination" in file_str:
        return True
    
    for pattern in integration_patterns:
        if pattern in name_str:
            return True
    
    return False


def analyze_function_sizes(file_path: Path) -> Dict:
    """Analyze function sizes in a file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")
        
        tree = ast.parse(content, filename=str(file_path))
        
        violations = []
        all_functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Calculate function line count
                func_start = node.lineno - 1
                func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start + 1
                func_lines = func_end - func_start
                
                func_info = {
                    "name": node.name,
                    "lines": func_lines,
                    "start_line": node.lineno,
                    "end_line": func_end,
                    "args_count": len(node.args.args),
                }
                
                all_functions.append(func_info)
                
                if func_lines > 30:
                    violations.append(func_info)
        
        return {
            "file": str(file_path.relative_to(project_root)),
            "total_functions": len(all_functions),
            "violations": violations,
            "violation_count": len(violations),
            "total_lines": len(lines),
        }
    
    except SyntaxError as e:
        return {
            "file": str(file_path.relative_to(project_root)),
            "error": f"Syntax error: {e.msg} at line {e.lineno}",
            "violations": [],
            "violation_count": 0,
        }
    except Exception as e:
        return {
            "file": str(file_path.relative_to(project_root)),
            "error": str(e),
            "violations": [],
            "violation_count": 0,
        }


def identify_patterns(analysis_results: List[Dict]) -> Dict:
    """Identify common refactoring patterns."""
    patterns = defaultdict(list)
    
    for result in analysis_results:
        if "violations" not in result:
            continue
        
        for violation in result.get("violations", []):
            lines = violation.get("lines", 0)
            args = violation.get("args_count", 0)
            
            # Pattern classification
            if lines > 100:
                patterns["very_large_functions"].append({
                    "file": result["file"],
                    "function": violation["name"],
                    "lines": lines,
                })
            elif lines > 60:
                patterns["large_functions"].append({
                    "file": result["file"],
                    "function": violation["name"],
                    "lines": lines,
                })
            elif args > 5:
                patterns["many_parameters"].append({
                    "file": result["file"],
                    "function": violation["name"],
                    "args": args,
                    "lines": lines,
                })
            else:
                patterns["medium_violations"].append({
                    "file": result["file"],
                    "function": violation["name"],
                    "lines": lines,
                })
    
    return dict(patterns)


def main():
    """Analyze integration tools for function violations."""
    # Load classification
    classification_file = project_root / "tools" / "TOOL_CLASSIFICATION.json"
    
    if not classification_file.exists():
        print("❌ ERROR: TOOL_CLASSIFICATION.json not found!")
        return 1

    with open(classification_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get SIGNAL integration tools
    signal_tools = data.get("signal", [])
    integration_tools = [
        t for t in signal_tools
        if is_integration_tool(t.get("file", ""))
    ]
    
    print("🔍 Analyzing Integration SIGNAL tools for function size violations...")
    print(f"📊 Found {len(integration_tools)} integration SIGNAL tools")
    print()
    
    # Analyze each tool
    analysis_results = []
    total_violations = 0
    
    for tool in integration_tools:
        file_path = project_root / tool["file"].replace("\\", "/")
        if file_path.exists():
            result = analyze_function_sizes(file_path)
            analysis_results.append(result)
            total_violations += result.get("violation_count", 0)
    
    # Identify patterns
    patterns = identify_patterns(analysis_results)
    
    # Generate report
    print("=" * 60)
    print("📊 Analysis Results")
    print("=" * 60)
    print(f"   Tools analyzed: {len(analysis_results)}")
    print(f"   Total function violations (>30 lines): {total_violations}")
    print()
    
    # Pattern breakdown
    print("🔍 Refactoring Patterns Identified:")
    print()
    
    if patterns.get("very_large_functions"):
        print(f"   🔴 Very Large Functions (>100 lines): {len(patterns['very_large_functions'])}")
        for item in patterns["very_large_functions"][:5]:
            print(f"      - {item['file']}::{item['function']} ({item['lines']} lines)")
        if len(patterns["very_large_functions"]) > 5:
            print(f"      ... and {len(patterns['very_large_functions']) - 5} more")
        print()
    
    if patterns.get("large_functions"):
        print(f"   🟡 Large Functions (60-100 lines): {len(patterns['large_functions'])}")
        for item in patterns["large_functions"][:5]:
            print(f"      - {item['file']}::{item['function']} ({item['lines']} lines)")
        if len(patterns["large_functions"]) > 5:
            print(f"      ... and {len(patterns['large_functions']) - 5} more")
        print()
    
    if patterns.get("many_parameters"):
        print(f"   🟠 Many Parameters (>5 args): {len(patterns['many_parameters'])}")
        for item in patterns["many_parameters"][:5]:
            print(f"      - {item['file']}::{item['function']} ({item['args']} args, {item['lines']} lines)")
        if len(patterns["many_parameters"]) > 5:
            print(f"      ... and {len(patterns['many_parameters']) - 5} more")
        print()
    
    if patterns.get("medium_violations"):
        print(f"   🟢 Medium Violations (31-60 lines): {len(patterns['medium_violations'])}")
        print(f"      (Easiest to refactor - quick wins)")
        print()
    
    # Save detailed results
    output_file = project_root / "agent_workspaces" / "Agent-1" / "phase2_integration_analysis.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "timestamp": "2025-12-21",
        "tools_analyzed": len(analysis_results),
        "total_violations": total_violations,
        "patterns": patterns,
        "detailed_results": analysis_results,
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"💾 Detailed analysis saved to: {output_file.relative_to(project_root)}")
    print()
    print("📋 Next Steps:")
    print("   1. Review pattern breakdown")
    print("   2. Create refactoring utilities for common patterns")
    print("   3. Plan extraction strategy for Phase 2")
    print("   4. Prepare helper modules")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

