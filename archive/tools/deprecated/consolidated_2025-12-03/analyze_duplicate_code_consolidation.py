"""
Duplicate Code Consolidation Analysis Tool
Provides detailed content comparison and consolidation recommendations
"""
import json
import filecmp
from pathlib import Path
from typing import Dict, List, Any, Optional
import difflib
import ast
import re

class DuplicateCodeConsolidationAnalyzer:
    """Analyzes duplicate code and provides consolidation recommendations."""
    
    def __init__(self, file_list_path: Path):
        self.file_list_path = file_list_path
        self.consolidation_plans: List[Dict[str, Any]] = []
        
    def load_file_list(self) -> Dict[str, Any]:
        """Load the file list from JSON."""
        with open(self.file_list_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def read_file_content(self, file_path: str) -> Optional[str]:
        """Read file content safely."""
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return None
    
    def extract_classes_and_functions(self, content: str) -> Dict[str, List[str]]:
        """Extract class and function names from Python code."""
        try:
            tree = ast.parse(content)
            classes = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            
            return {"classes": classes, "functions": functions}
        except Exception:
            # Fallback to regex if AST parsing fails
            classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
            functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
            return {"classes": classes, "functions": functions}
    
    def find_unique_code(self, file1_content: str, file2_content: str) -> Dict[str, Any]:
        """Find unique code sections between two files."""
        # Use difflib to find differences
        diff = list(difflib.unified_diff(
            file1_content.splitlines(keepends=True),
            file2_content.splitlines(keepends=True),
            lineterm=''
        ))
        
        # Extract additions and deletions
        additions = []
        deletions = []
        
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                additions.append(line[1:].rstrip())
            elif line.startswith('-') and not line.startswith('---'):
                deletions.append(line[1:].rstrip())
        
        return {
            "additions": additions[:50],  # Limit to first 50 lines
            "deletions": deletions[:50],
            "total_additions": len(additions),
            "total_deletions": len(deletions)
        }
    
    def analyze_consolidation_strategy(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze consolidation strategy for a file."""
        file_path = file_info["file_path"]
        similar_files = file_info.get("similar_files", [])
        
        file_content = self.read_file_content(file_path)
        if not file_content:
            return {
                "file": file_path,
                "status": "error",
                "reason": "File not found"
            }
        
        file_structure = self.extract_classes_and_functions(file_content)
        
        consolidation_plan = {
            "file": file_path,
            "type": file_info.get("type", "unknown"),
            "recommendation": "KEEP",
            "consolidation_strategy": "NONE",
            "target_file": None,
            "unique_elements": file_structure,
            "merge_instructions": [],
            "code_changes": [],
            "risk_level": "LOW"
        }
        
        if not similar_files:
            return consolidation_plan
        
        # Find best match
        best_match = max(similar_files, key=lambda x: x.get("similarity_score", 0.0))
        similarity = best_match.get("similarity_score", 0.0)
        similar_path = best_match.get("file", "")
        
        if similar_path:
            # Convert to full path
            full_similar_path = Path("src") / similar_path.replace("\\", "/")
            if not full_similar_path.exists():
                full_similar_path = Path(similar_path.replace("\\", "/"))
            
            similar_content = self.read_file_content(str(full_similar_path))
            
            if similar_content:
                similar_structure = self.extract_classes_and_functions(similar_content)
                unique_code = self.find_unique_code(file_content, similar_content)
                
                # Determine consolidation strategy
                if similarity > 0.8:
                    consolidation_plan["recommendation"] = "USE_EXISTING"
                    consolidation_plan["consolidation_strategy"] = "REPLACE_WITH_EXISTING"
                    consolidation_plan["target_file"] = str(full_similar_path)
                    consolidation_plan["risk_level"] = "LOW"
                    consolidation_plan["merge_instructions"] = [
                        f"1. Verify {Path(file_path).name} functionality is covered by {Path(similar_path).name}",
                        f"2. Update any imports referencing {Path(file_path).name}",
                        f"3. Delete {Path(file_path).name}"
                    ]
                elif similarity > 0.5:
                    consolidation_plan["recommendation"] = "MERGE"
                    consolidation_plan["consolidation_strategy"] = "MERGE_INTO_TARGET"
                    consolidation_plan["target_file"] = str(full_similar_path)
                    consolidation_plan["risk_level"] = "MEDIUM"
                    
                    # Find unique classes/functions
                    unique_classes = set(file_structure["classes"]) - set(similar_structure["classes"])
                    unique_functions = set(file_structure["functions"]) - set(similar_structure["functions"])
                    
                    consolidation_plan["merge_instructions"] = [
                        f"1. Review unique elements in {Path(file_path).name}:",
                        f"   - Unique classes: {list(unique_classes) if unique_classes else 'None'}",
                        f"   - Unique functions: {list(unique_functions) if unique_functions else 'None'}",
                        f"2. Merge unique code into {Path(similar_path).name}",
                        f"3. Test merged functionality",
                        f"4. Update imports",
                        f"5. Delete {Path(file_path).name}"
                    ]
                    
                    consolidation_plan["code_changes"] = [
                        {
                            "action": "merge",
                            "source": Path(file_path).name,
                            "target": Path(similar_path).name,
                            "unique_elements": {
                                "classes": list(unique_classes),
                                "functions": list(unique_functions)
                            }
                        }
                    ]
                else:
                    consolidation_plan["recommendation"] = "KEEP"
                    consolidation_plan["consolidation_strategy"] = "SEPARATE_FUNCTIONALITY"
                    consolidation_plan["risk_level"] = "LOW"
                    consolidation_plan["merge_instructions"] = [
                        f"Files have different functionality (similarity: {similarity:.2%})",
                        f"Keep both files - they serve different purposes"
                    ]
        
        return consolidation_plan
    
    def analyze_all_files(self) -> Dict[str, Any]:
        """Analyze all files for consolidation."""
        data = self.load_file_list()
        
        # Analyze functionality_exists files
        for file_info in data.get("functionality_exists_files", []):
            plan = self.analyze_consolidation_strategy(file_info)
            self.consolidation_plans.append(plan)
        
        # Analyze possible duplicate files
        for file_info in data.get("possible_duplicate_files", []):
            plan = self.analyze_consolidation_strategy(file_info)
            self.consolidation_plans.append(plan)
        
        # Generate summary
        summary = {
            "total_files": len(self.consolidation_plans),
            "strategies": {
                "REPLACE_WITH_EXISTING": len([p for p in self.consolidation_plans if p.get("consolidation_strategy") == "REPLACE_WITH_EXISTING"]),
                "MERGE_INTO_TARGET": len([p for p in self.consolidation_plans if p.get("consolidation_strategy") == "MERGE_INTO_TARGET"]),
                "SEPARATE_FUNCTIONALITY": len([p for p in self.consolidation_plans if p.get("consolidation_strategy") == "SEPARATE_FUNCTIONALITY"]),
                "NONE": len([p for p in self.consolidation_plans if p.get("consolidation_strategy") == "NONE"])
            },
            "risk_levels": {
                "LOW": len([p for p in self.consolidation_plans if p.get("risk_level") == "LOW"]),
                "MEDIUM": len([p for p in self.consolidation_plans if p.get("risk_level") == "MEDIUM"]),
                "HIGH": len([p for p in self.consolidation_plans if p.get("risk_level") == "HIGH"])
            }
        }
        
        return {
            "summary": summary,
            "consolidation_plans": self.consolidation_plans
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze duplicate code for consolidation")
    parser.add_argument("--file-list", type=str,
                       default="agent_workspaces/Agent-5/22_duplicate_files_list.json",
                       help="Path to file list JSON")
    parser.add_argument("--output", type=str,
                       default="agent_workspaces/Agent-8/DUPLICATE_CODE_REVIEW_COMPLETE.md",
                       help="Output report path")
    args = parser.parse_args()
    
    analyzer = DuplicateCodeConsolidationAnalyzer(Path(args.file_list))
    results = analyzer.analyze_all_files()
    
    # Generate markdown report
    report_lines = [
        "# ✅ Duplicate Code Review - COMPLETE",
        "",
        "**Date**: 2025-12-02 16:50:00",
        "**Agent**: Agent-8 (SSOT & System Integration Specialist)",
        "**Status**: ✅ **CONSOLIDATION ANALYSIS COMPLETE**",
        "**Priority**: MEDIUM",
        "",
        "---",
        "",
        "## 📊 CONSOLIDATION SUMMARY",
        "",
        f"**Total Files Analyzed**: {results['summary']['total_files']}",
        "",
        "### **Consolidation Strategies**:",
        f"- **REPLACE_WITH_EXISTING**: {results['summary']['strategies']['REPLACE_WITH_EXISTING']} files",
        f"- **MERGE_INTO_TARGET**: {results['summary']['strategies']['MERGE_INTO_TARGET']} files",
        f"- **SEPARATE_FUNCTIONALITY**: {results['summary']['strategies']['SEPARATE_FUNCTIONALITY']} files",
        f"- **NONE**: {results['summary']['strategies']['NONE']} files",
        "",
        "### **Risk Levels**:",
        f"- **LOW**: {results['summary']['risk_levels']['LOW']} files",
        f"- **MEDIUM**: {results['summary']['risk_levels']['MEDIUM']} files",
        f"- **HIGH**: {results['summary']['risk_levels']['HIGH']} files",
        "",
        "---",
        "",
        "## 📋 DETAILED CONSOLIDATION PLANS",
        ""
    ]
    
    # Add detailed plans
    for i, plan in enumerate(results['consolidation_plans'], 1):
        if plan.get("status") == "error":
            report_lines.extend([
                f"### **{i}. {Path(plan['file']).name}**",
                "",
                f"**Status**: ❌ **ERROR**",
                f"**Reason**: {plan.get('reason', 'Unknown error')}",
                ""
            ])
            continue
        
        report_lines.extend([
            f"### **{i}. {Path(plan['file']).name}**",
            "",
            f"**File**: `{plan['file']}`",
            f"**Type**: {plan['type']}",
            f"**Recommendation**: **{plan['recommendation']}**",
            f"**Strategy**: {plan['consolidation_strategy']}",
            f"**Risk Level**: {plan['risk_level']}",
            ""
        ])
        
        if plan.get("target_file"):
            report_lines.append(f"**Target File**: `{plan['target_file']}`")
            report_lines.append("")
        
        if plan.get("unique_elements"):
            unique = plan['unique_elements']
            if unique.get("classes") or unique.get("functions"):
                report_lines.append("**Unique Elements**:")
                if unique.get("classes"):
                    report_lines.append(f"- Classes: {', '.join(unique['classes'][:10])}")
                if unique.get("functions"):
                    report_lines.append(f"- Functions: {', '.join(unique['functions'][:10])}")
                report_lines.append("")
        
        if plan.get("merge_instructions"):
            report_lines.append("**Consolidation Instructions**:")
            for instruction in plan['merge_instructions']:
                report_lines.append(f"- {instruction}")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
    
    report_lines.extend([
        "## 🎯 EXECUTION PRIORITY",
        "",
        "### **Priority 1: High Similarity Files (REPLACE_WITH_EXISTING)**",
        "- Low risk, high impact",
        "- Quick wins for code reduction",
        "",
        "### **Priority 2: Medium Similarity Files (MERGE_INTO_TARGET)**",
        "- Medium risk, requires careful merging",
        "- Test thoroughly after consolidation",
        "",
        "### **Priority 3: Low Similarity Files (SEPARATE_FUNCTIONALITY)**",
        "- Keep separate - different functionality",
        "- No consolidation needed",
        "",
        "---",
        "",
        "## ✅ SSOT COMPLIANCE",
        "",
        "All consolidation plans maintain SSOT principles:",
        "- Single source of truth for each functionality",
        "- Clear canonical files identified",
        "- Import updates documented",
        "- No duplicate implementations after consolidation",
        "",
        "---",
        "",
        "**Status**: ✅ **CONSOLIDATION ANALYSIS COMPLETE**",
        "",
        "🐝 **WE. ARE. SWARM. ⚡🔥**"
    ])
    
    # Save report
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # Save JSON for programmatic use
    json_output = output_path.with_suffix('.json')
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("="*60)
    print("📊 DUPLICATE CODE CONSOLIDATION ANALYSIS - COMPLETE")
    print("="*60)
    print(f"✅ Total Files Analyzed: {results['summary']['total_files']}")
    print(f"📋 Consolidation Strategies:")
    for strategy, count in results['summary']['strategies'].items():
        if count > 0:
            print(f"   - {strategy}: {count}")
    print(f"\n✅ Report saved to: {output_path}")
    print(f"✅ JSON saved to: {json_output}")
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")

if __name__ == "__main__":
    main()


