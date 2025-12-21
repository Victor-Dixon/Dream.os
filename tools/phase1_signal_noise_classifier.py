#!/usr/bin/env python3
"""
Phase -1: Signal vs Noise Classification Tool
==============================================

Classifies all 791 tools as SIGNAL (real infrastructure) or NOISE (thin wrappers/scripts)
based on Agent-1's Signal vs Noise analysis criteria.

This is the CRITICAL first step before any V2 refactoring begins.

Reference: docs/V2_COMPLIANCE_REFACTORING_PLAN.md - Phase -1
Reference: agent_workspaces/Agent-1/TOOLBELT_SIGNAL_VS_NOISE_ANALYSIS.md

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-21
Priority: CRITICAL - Phase -1 execution
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class SignalNoiseClassifier:
    """
    Classify tools as SIGNAL (real infrastructure) or NOISE (thin wrappers).
    
    Classification Criteria (from Agent-1 analysis):
    
    SIGNAL Tools (Real Infrastructure - REFACTOR THESE):
    - Contains real business logic (not just wrappers)
    - Reusable infrastructure (used across codebase/projects)
    - Has modular architecture (extractable components)
    - Provides core functionality (not convenience wrappers)
    
    NOISE Tools (Thin Wrappers - DEPRECATE/MOVE THESE):
    - Just CLI wrappers around existing functionality
    - No real business logic (calls other tools/functions)
    - One-off convenience scripts (not reusable infrastructure)
    - Can be replaced by direct usage of underlying tool
    """

    def __init__(self, tools_dir: Path = None):
        """Initialize classifier."""
        self.tools_dir = tools_dir or Path(__file__).parent
        self.project_root = self.tools_dir.parent
        
        # Known NOISE patterns (from Agent-1 analysis)
        self.noise_patterns = {
            'wrapper': ['wrapper', 'cli_wrapper', 'cli'],
            'validation': ['validate_imports'],  # Known NOISE from Agent-1
            'task_cli': ['task_cli'],  # Known NOISE from Agent-1
        }
        
        # Known SIGNAL patterns (core infrastructure)
        self.signal_patterns = {
            'verification': ['functionality_verification', 'integration_validator'],
            'orchestration': ['swarm_orchestrator', 'orchestrator'],
            'analysis': ['test_usage_analyzer'],
        }

    def analyze_tool_file(self, tool_path: Path) -> Dict[str, Any]:
        """
        Analyze a tool file to determine if it's SIGNAL or NOISE.
        
        Returns analysis dictionary with classification metadata.
        """
        analysis = {
            "file": str(tool_path.relative_to(self.project_root)),
            "name": tool_path.stem,
            "size_bytes": tool_path.stat().st_size,
            "lines": 0,
            "has_business_logic": False,
            "is_cli_wrapper": False,
            "imports_other_tools": False,
            "function_count": 0,
            "class_count": 0,
            "has_main": False,
            "calls_other_tools": False,
            "error": None,
            "classification": "UNKNOWN",
            "confidence": "LOW",
            "rationale": []
        }

        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
                analysis["lines"] = len(content.splitlines())
                tree = ast.parse(content, filename=str(tool_path))

            # Analyze AST structure
            functions = []
            classes = []
            imports = []
            tool_calls = []
            
            for node in ast.walk(tree):
                # Collect functions
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    if node.name == "main":
                        analysis["has_main"] = True
                
                # Collect classes
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                
                # Collect imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                        # Check if importing tools (potential wrapper indicator)
                        if 'tools.' in alias.name or alias.name.startswith('tools'):
                            analysis["imports_other_tools"] = True
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                        # Check if importing from tools (potential wrapper)
                        if 'tools.' in node.module or node.module.startswith('tools'):
                            analysis["imports_other_tools"] = True
                        # Check for calls to other tools
                        for alias in (node.names or []):
                            if alias.name:
                                tool_calls.append(f"{node.module}.{alias.name}")

            analysis["function_count"] = len(functions)
            analysis["class_count"] = len(classes)
            
            # Check for CLI wrapper patterns
            content_lower = content.lower()
            
            # Pattern 1: Just calls another tool/function with argparse
            if 'argparse' in content_lower and analysis["function_count"] <= 2:
                # Check if main function just calls another tool
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == "main":
                        # Count meaningful statements (not just calls)
                        meaningful_statements = 0
                        for stmt in ast.walk(node):
                            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.Try)):
                                meaningful_statements += 1
                            elif isinstance(stmt, ast.Call):
                                # Check if it's just calling another tool
                                if isinstance(stmt.func, ast.Attribute):
                                    if 'tools.' in ast.unparse(stmt.func) if hasattr(ast, 'unparse') else str(stmt.func):
                                        analysis["calls_other_tools"] = True
                        if meaningful_statements < 3 and analysis["calls_other_tools"]:
                            analysis["is_cli_wrapper"] = True
                            analysis["rationale"].append("Thin CLI wrapper - just calls other tools")

            # Pattern 2: Very small file that just imports and calls
            if analysis["lines"] < 100 and analysis["function_count"] <= 1:
                if analysis["imports_other_tools"]:
                    analysis["is_cli_wrapper"] = True
                    analysis["rationale"].append("Small file that just imports and calls other tools")

            # Pattern 3: Check name patterns
            name_lower = analysis["name"].lower()
            for pattern_type, patterns in self.noise_patterns.items():
                for pattern in patterns:
                    if pattern in name_lower:
                        analysis["rationale"].append(f"Name matches NOISE pattern: {pattern}")
                        break

            # Check for business logic indicators (SIGNAL)
            if analysis["function_count"] > 3:
                analysis["has_business_logic"] = True
                analysis["rationale"].append(f"Multiple functions ({analysis['function_count']}) indicate business logic")
            
            if analysis["class_count"] > 0:
                analysis["has_business_logic"] = True
                analysis["rationale"].append(f"Contains classes ({analysis['class_count']}) indicate modular architecture")
            
            # Check for complex control flow (indicates business logic)
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    if analysis["function_count"] > 0:
                        analysis["has_business_logic"] = True
                        analysis["rationale"].append("Contains complex control flow structures")
                        break

            # Check known SIGNAL patterns
            for pattern_type, patterns in self.signal_patterns.items():
                for pattern in patterns:
                    if pattern in name_lower:
                        analysis["rationale"].append(f"Known SIGNAL pattern: {pattern}")
                        break

        except SyntaxError as e:
            analysis["error"] = f"Syntax error: {e}"
            analysis["classification"] = "NOISE"  # Syntax errors = likely NOISE
            analysis["rationale"].append(f"Syntax error indicates broken/unmaintained code")
        except Exception as e:
            analysis["error"] = f"Error analyzing: {e}"
            analysis["classification"] = "UNKNOWN"
            analysis["rationale"].append(f"Error during analysis: {e}")

        return analysis

    def classify_tool(self, analysis: Dict[str, Any]) -> str:
        """
        Classify tool as SIGNAL or NOISE based on analysis.
        
        Returns: "SIGNAL", "NOISE", or "UNKNOWN"
        """
        # If already classified with high confidence
        if analysis.get("classification") in ["SIGNAL", "NOISE"] and analysis.get("error"):
            return analysis["classification"]

        # Strong NOISE indicators
        if analysis["is_cli_wrapper"]:
            analysis["classification"] = "NOISE"
            analysis["confidence"] = "HIGH"
            return "NOISE"
        
        # Very small files that just call other tools
        if analysis["lines"] < 50 and analysis["imports_other_tools"] and analysis["function_count"] <= 1:
            analysis["classification"] = "NOISE"
            analysis["confidence"] = "MEDIUM"
            analysis["rationale"].append("Very small file with minimal logic, likely wrapper")
            return "NOISE"

        # Strong SIGNAL indicators
        if analysis["has_business_logic"]:
            # Check if it's a real implementation (not just a wrapper)
            if not analysis["is_cli_wrapper"]:
                analysis["classification"] = "SIGNAL"
                analysis["confidence"] = "HIGH"
                return "SIGNAL"
        
        # Medium-sized files with multiple functions (likely SIGNAL)
        if analysis["lines"] > 150 and analysis["function_count"] > 2:
            analysis["classification"] = "SIGNAL"
            analysis["confidence"] = "MEDIUM"
            analysis["rationale"].append("Medium-large file with multiple functions indicates real implementation")
            return "SIGNAL"

        # Large files are almost certainly SIGNAL (have substantial logic)
        if analysis["lines"] > 300:
            analysis["classification"] = "SIGNAL"
            analysis["confidence"] = "HIGH"
            analysis["rationale"].append("Large file size indicates substantial business logic")
            return "SIGNAL"

        # Default: UNKNOWN (needs manual review)
        analysis["classification"] = "UNKNOWN"
        analysis["confidence"] = "LOW"
        analysis["rationale"].append("Does not match clear SIGNAL/NOISE patterns - needs manual review")
        return "UNKNOWN"

    def classify_all_tools(self) -> Dict[str, Any]:
        """
        Classify all Python files in tools/ directory.
        
        Returns classification results dictionary.
        """
        print("🔍 Scanning tools directory...")
        
        # Find all Python files
        tool_files = []
        for ext in ['*.py']:
            tool_files.extend(self.tools_dir.rglob(ext))
        
        # Filter out special files
        tool_files = [
            f for f in tool_files 
            if f.name not in ['__init__.py', '__main__.py', 'setup.py']
            and '__pycache__' not in str(f)
            and '.pyc' not in str(f)
        ]
        
        print(f"📊 Found {len(tool_files)} Python files to classify")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_tools": len(tool_files),
            "signal": [],
            "noise": [],
            "unknown": [],
            "errors": []
        }
        
        # Classify each tool
        for i, tool_file in enumerate(tool_files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(tool_files)} tools analyzed...")
            
            try:
                analysis = self.analyze_tool_file(tool_file)
                classification = self.classify_tool(analysis)
                analysis["classification"] = classification
                
                if classification == "SIGNAL":
                    results["signal"].append(analysis)
                elif classification == "NOISE":
                    results["noise"].append(analysis)
                else:
                    results["unknown"].append(analysis)
                    
            except Exception as e:
                error_analysis = {
                    "file": str(tool_file.relative_to(self.project_root)),
                    "error": str(e),
                    "classification": "ERROR"
                }
                results["errors"].append(error_analysis)
        
        # Sort results by filename
        results["signal"].sort(key=lambda x: x["file"])
        results["noise"].sort(key=lambda x: x["file"])
        results["unknown"].sort(key=lambda x: x["file"])
        
        return results

    def generate_classification_document(self, results: Dict[str, Any], output_path: Path = None) -> str:
        """
        Generate TOOL_CLASSIFICATION.md document as specified in Phase -1.
        
        Reference: docs/V2_COMPLIANCE_REFACTORING_PLAN.md
        """
        output_path = output_path or self.tools_dir / "TOOL_CLASSIFICATION.md"
        
        doc = f"""# Tool Classification - Phase -1 Results

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Classification**: Signal vs Noise Analysis  
**Purpose**: Filter V2 refactoring to SIGNAL tools only (Phase -1 of V2 Compliance Refactoring Plan)

---

## 📊 Classification Summary

- **Total Tools Analyzed**: {results['total_tools']}
- **SIGNAL Tools** (Real Infrastructure - REFACTOR): {len(results['signal'])}
- **NOISE Tools** (Thin Wrappers - DEPRECATE/MOVE): {len(results['noise'])}
- **UNKNOWN Tools** (Needs Manual Review): {len(results['unknown'])}
- **Errors**: {len(results['errors'])}

---

## Classification Criteria

### ✅ SIGNAL Tools (Real Infrastructure - REFACTOR THESE)

**Criteria**:
- Contains **real business logic** (not just wrappers)
- **Reusable infrastructure** (used across codebase/projects)
- Has **modular architecture** (extractable components)
- Provides **core functionality** (not convenience wrappers)

**Action**: Include in V2 refactoring phases (these are worth fixing)

### ❌ NOISE Tools (Thin Wrappers - DEPRECATE/MOVE THESE)

**Criteria**:
- Just **CLI wrappers** around existing functionality
- No real business logic (calls other tools/functions)
- **One-off convenience scripts** (not reusable infrastructure)
- Can be replaced by direct usage of underlying tool

**Action**: Move to `scripts/`, deprecate, or remove (don't refactor wrappers)

---

## ✅ SIGNAL Tools ({len(results['signal'])})

**Status**: Real infrastructure - Include in V2 refactoring

"""
        
        # List SIGNAL tools
        for tool in results['signal']:
            doc += f"- **{tool['name']}** (`{tool['file']}`)\n"
            doc += f"  - Lines: {tool['lines']}, Functions: {tool['function_count']}, Classes: {tool['class_count']}\n"
            if tool['rationale']:
                doc += f"  - Rationale: {'; '.join(tool['rationale'][:2])}\n"
            doc += "\n"
        
        doc += f"""
---

## ❌ NOISE Tools ({len(results['noise'])})

**Status**: Thin wrappers - Move to scripts/, deprecate, or remove

"""
        
        # List NOISE tools
        for tool in results['noise']:
            doc += f"- **{tool['name']}** (`{tool['file']}`)\n"
            doc += f"  - Lines: {tool['lines']}, Functions: {tool['function_count']}\n"
            if tool['rationale']:
                doc += f"  - Rationale: {'; '.join(tool['rationale'][:2])}\n"
            doc += "\n"
        
        if results['unknown']:
            doc += f"""
---

## ❓ UNKNOWN Tools ({len(results['unknown'])})

**Status**: Needs manual review before classification

"""
            for tool in results['unknown']:
                doc += f"- **{tool['name']}** (`{tool['file']}`)\n"
                doc += f"  - Lines: {tool['lines']}, Functions: {tool['function_count']}\n"
                if tool['rationale']:
                    doc += f"  - Rationale: {'; '.join(tool['rationale'][:2])}\n"
                doc += "\n"
        
        doc += """
---

## 📋 Next Steps (Phase -1 Actions)

1. **Review UNKNOWN Tools**: Manually classify tools that couldn't be auto-classified
2. **Move NOISE Tools**: Move NOISE tools to `scripts/` directory
3. **Update Toolbelt Registry**: Remove NOISE tools from toolbelt registry
4. **Update Refactoring Scope**: Filter all V2 refactoring phases to SIGNAL tools only
5. **Update Compliance Baseline**: Recalculate compliance percentages (remove NOISE from denominator)

---

## 🔗 References

- **V2 Compliance Refactoring Plan**: `docs/V2_COMPLIANCE_REFACTORING_PLAN.md`
- **Signal vs Noise Analysis**: `agent_workspaces/Agent-1/TOOLBELT_SIGNAL_VS_NOISE_ANALYSIS.md`
- **Classification Tool**: `tools/phase1_signal_noise_classifier.py`

---

*Generated by Phase -1 Signal vs Noise Classification Tool*
*Part of V2 Compliance Refactoring Plan - Phase -1*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        return str(output_path)

    def save_json_results(self, results: Dict[str, Any], output_path: Path = None) -> str:
        """Save classification results as JSON for programmatic use."""
        output_path = output_path or self.tools_dir / "TOOL_CLASSIFICATION.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return str(output_path)


def main():
    """Main entry point for Phase -1 classification."""
    print("🚀 Phase -1: Signal vs Noise Classification")
    print("=" * 60)
    print("Reference: docs/V2_COMPLIANCE_REFACTORING_PLAN.md")
    print()
    
    classifier = SignalNoiseClassifier()
    results = classifier.classify_all_tools()
    
    print()
    print("📊 Classification Results:")
    print(f"   ✅ SIGNAL (Real Infrastructure): {len(results['signal'])}")
    print(f"   ❌ NOISE (Thin Wrappers): {len(results['noise'])}")
    print(f"   ❓ UNKNOWN (Needs Review): {len(results['unknown'])}")
    print(f"   ⚠️  ERRORS: {len(results['errors'])}")
    print()
    
    # Generate classification document
    doc_path = classifier.generate_classification_document(results)
    print(f"📄 Classification document: {doc_path}")
    
    # Save JSON results
    json_path = classifier.save_json_results(results)
    print(f"💾 JSON results: {json_path}")
    
    print()
    print("✅ Phase -1 classification complete!")
    print()
    print("📋 Next Steps:")
    print("   1. Review UNKNOWN tools for manual classification")
    print("   2. Move NOISE tools to scripts/ directory")
    print("   3. Update toolbelt registry (remove NOISE tools)")
    print("   4. Update V2 refactoring scope (SIGNAL tools only)")
    print()
    print("🐝 WE. ARE. SWARM. PHASE -1 CLASSIFICATION COMPLETE. ⚡🔥")


if __name__ == "__main__":
    main()

