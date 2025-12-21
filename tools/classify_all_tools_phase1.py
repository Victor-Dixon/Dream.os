#!/usr/bin/env python3
"""
Phase -1: Signal vs Noise Classification Tool
==============================================

Systematically classifies all tools as SIGNAL (infrastructure) or NOISE (wrappers).

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-21
Task: Phase -1 of V2 Compliance Refactoring Plan
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class ToolClassifier:
    """Classifies tools as SIGNAL or NOISE based on analysis."""

    # NOISE patterns (indicators of wrappers)
    NOISE_PATTERNS = [
        "sys.argv",
        "argparse",
        "wrapper",
        "convenience",
        "cli",
        "main()",
        "if __name__",
    ]

    # SIGNAL patterns (indicators of real logic)
    SIGNAL_PATTERNS = [
        "class ",
        "def ",
        "import ",
        "from ",
        "business logic",
        "algorithm",
        "process",
        "analyze",
        "validate",
        "generate",
        "extract",
        "transform",
    ]

    def __init__(self, tools_dir: Path):
        """Initialize classifier."""
        self.tools_dir = tools_dir
        self.classifications: Dict[str, Dict] = {}

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single tool file."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")
                line_count = len(lines)

            # Basic metrics
            has_classes = "class " in content
            has_functions = "def " in content
            has_imports = "import " in content or "from " in content
            has_main = 'if __name__ == "__main__"' in content
            has_argparse = "argparse" in content
            has_sys_argv = "sys.argv" in content

            # Count functions and classes
            try:
                tree = ast.parse(content, filename=str(file_path))
                function_count = len(
                    [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                )
                class_count = len(
                    [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                )
            except SyntaxError:
                function_count = content.count("def ")
                class_count = content.count("class ")

            # Calculate complexity score
            complexity_score = (
                (function_count * 2)
                + (class_count * 3)
                + (1 if has_classes else 0)
                + (1 if has_functions else 0)
                + (1 if has_imports else 0)
            )

            # Wrapper detection
            is_wrapper = (
                (has_argparse and has_sys_argv and function_count < 3)
                or (has_main and function_count < 2 and class_count == 0)
                or (line_count < 100 and has_argparse and class_count == 0)
            )

            # Business logic detection
            has_business_logic = (
                function_count > 3
                or class_count > 0
                or complexity_score > 10
                or (has_classes and has_functions)
            )

            # Classification decision
            if is_wrapper and not has_business_logic:
                classification = "NOISE"
                reason = "Thin wrapper - minimal logic, primarily CLI interface"
            elif has_business_logic and not is_wrapper:
                classification = "SIGNAL"
                reason = "Real infrastructure - contains business logic"
            elif line_count > 200 and has_business_logic:
                classification = "SIGNAL"
                reason = "Large file with business logic - infrastructure tool"
            elif line_count < 50 and has_argparse:
                classification = "NOISE"
                reason = "Small wrapper script - convenience utility"
            else:
                # Default to SIGNAL if uncertain (better to keep than remove)
                classification = "SIGNAL"
                reason = "Uncertain - defaulting to SIGNAL (contains some logic)"

            return {
                "file": str(file_path.relative_to(project_root)),
                "classification": classification,
                "reason": reason,
                "metrics": {
                    "lines": line_count,
                    "functions": function_count,
                    "classes": class_count,
                    "complexity_score": complexity_score,
                    "has_argparse": has_argparse,
                    "has_main": has_main,
                    "has_classes": has_classes,
                    "has_functions": has_functions,
                },
            }

        except Exception as e:
            return {
                "file": str(file_path.relative_to(project_root)),
                "classification": "UNKNOWN",
                "reason": f"Error analyzing: {str(e)}",
                "metrics": {},
            }

    def classify_all_tools(self) -> Dict[str, List[Dict]]:
        """Classify all tools in tools directory."""
        tools = list(self.tools_dir.rglob("*.py"))
        tools = [
            t
            for t in tools
            if "__pycache__" not in str(t)
            and not t.name.startswith("test_")
            and not t.name.endswith("_test.py")
        ]

        print(f"🔍 Analyzing {len(tools)} tools...")

        classifications = {"SIGNAL": [], "NOISE": [], "UNKNOWN": []}

        for tool_path in tools:
            result = self.analyze_file(tool_path)
            classification = result["classification"]
            classifications[classification].append(result)
            self.classifications[result["file"]] = result

            # Progress indicator
            if len(self.classifications) % 50 == 0:
                print(f"   Analyzed {len(self.classifications)} tools...")

        return classifications

    def generate_classification_document(self, classifications: Dict[str, List[Dict]]) -> str:
        """Generate markdown classification document."""
        doc = []
        doc.append("# Tool Classification: Signal vs Noise")
        doc.append("")
        doc.append("**Date**: 2025-12-21")
        doc.append("**Phase**: Phase -1 of V2 Compliance Refactoring Plan")
        doc.append("**Analyst**: Agent-1 (Integration & Core Systems Specialist)")
        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append("## Executive Summary")
        doc.append("")
        doc.append(f"- **Total Tools Analyzed**: {sum(len(v) for v in classifications.values())}")
        doc.append(f"- **SIGNAL Tools**: {len(classifications['SIGNAL'])} (real infrastructure)")
        doc.append(f"- **NOISE Tools**: {len(classifications['NOISE'])} (thin wrappers)")
        doc.append(f"- **UNKNOWN**: {len(classifications['UNKNOWN'])} (needs manual review)")
        doc.append("")
        doc.append("## Classification Criteria")
        doc.append("")
        doc.append("### ✅ SIGNAL Tools (Real Infrastructure)")
        doc.append("- Contains **real business logic** (not just wrappers)")
        doc.append("- **Reusable infrastructure** (used across codebase/projects)")
        doc.append("- Has **modular architecture** (classes, multiple functions)")
        doc.append("- Provides **core functionality** (not convenience wrappers)")
        doc.append("")
        doc.append("### ❌ NOISE Tools (Thin Wrappers)")
        doc.append("- Just **CLI wrappers** around existing functionality")
        doc.append("- No real business logic (calls other tools/functions)")
        doc.append("- **One-off convenience scripts** (not reusable infrastructure)")
        doc.append("- Can be replaced by direct usage of underlying tool")
        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append("## SIGNAL Tools")
        doc.append("")
        doc.append(f"**Count**: {len(classifications['SIGNAL'])}")
        doc.append("")
        doc.append("| File | Lines | Functions | Classes | Reason |")
        doc.append("|------|-------|-----------|---------|--------|")

        for tool in sorted(classifications["SIGNAL"], key=lambda x: x["file"]):
            metrics = tool.get("metrics", {})
            doc.append(
                f"| `{tool['file']}` | {metrics.get('lines', 'N/A')} | "
                f"{metrics.get('functions', 'N/A')} | {metrics.get('classes', 'N/A')} | "
                f"{tool['reason']} |"
            )

        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append("## NOISE Tools")
        doc.append("")
        doc.append(f"**Count**: {len(classifications['NOISE'])}")
        doc.append("")
        doc.append("| File | Lines | Functions | Classes | Reason |")
        doc.append("|------|-------|-----------|---------|--------|")

        for tool in sorted(classifications["NOISE"], key=lambda x: x["file"]):
            metrics = tool.get("metrics", {})
            doc.append(
                f"| `{tool['file']}` | {metrics.get('lines', 'N/A')} | "
                f"{metrics.get('functions', 'N/A')} | {metrics.get('classes', 'N/A')} | "
                f"{tool['reason']} |"
            )

        if classifications["UNKNOWN"]:
            doc.append("")
            doc.append("---")
            doc.append("")
            doc.append("## UNKNOWN Tools (Needs Manual Review)")
            doc.append("")
            doc.append(f"**Count**: {len(classifications['UNKNOWN'])}")
            doc.append("")
            for tool in classifications["UNKNOWN"]:
                doc.append(f"- `{tool['file']}`: {tool['reason']}")

        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append("## Next Steps")
        doc.append("")
        doc.append("1. **Review UNKNOWN tools** - Manual classification needed")
        doc.append("2. **Move NOISE tools** - Move to `scripts/` directory")
        doc.append("3. **Update toolbelt registry** - Remove NOISE tools")
        doc.append("4. **Update compliance baseline** - Remove NOISE from denominator")
        doc.append("5. **Begin Phase 0** - Fix syntax errors in SIGNAL tools only")
        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append("*Classification complete. Ready for Phase 0.*")

        return "\n".join(doc)

    def save_classification_json(self, classifications: Dict[str, List[Dict]], output_path: Path):
        """Save classification as JSON for programmatic access."""
        output = {
            "metadata": {
                "date": "2025-12-21",
                "phase": "Phase -1",
                "total_tools": sum(len(v) for v in classifications.values()),
                "signal_count": len(classifications["SIGNAL"]),
                "noise_count": len(classifications["NOISE"]),
                "unknown_count": len(classifications["UNKNOWN"]),
            },
            "classifications": self.classifications,
            "by_classification": classifications,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)


def main():
    """Main execution."""
    tools_dir = project_root / "tools"
    output_dir = project_root / "tools"
    classifier = ToolClassifier(tools_dir)

    print("🚀 Phase -1: Signal vs Noise Classification")
    print("=" * 60)
    print()

    # Classify all tools
    classifications = classifier.classify_all_tools()

    # Generate documents
    print()
    print("📝 Generating classification documents...")

    # Markdown document
    md_content = classifier.generate_classification_document(classifications)
    md_path = output_dir / "TOOL_CLASSIFICATION.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"   ✅ Created: {md_path.relative_to(project_root)}")

    # JSON document
    json_path = output_dir / "TOOL_CLASSIFICATION.json"
    classifier.save_classification_json(classifications, json_path)
    print(f"   ✅ Created: {json_path.relative_to(project_root)}")

    # Summary
    print()
    print("=" * 60)
    print("📊 Classification Summary")
    print("=" * 60)
    print(f"   ✅ SIGNAL Tools: {len(classifications['SIGNAL'])}")
    print(f"   ❌ NOISE Tools: {len(classifications['NOISE'])}")
    print(f"   ⚠️  UNKNOWN: {len(classifications['UNKNOWN'])}")
    print()
    print("📋 Next Steps:")
    print("   1. Review TOOL_CLASSIFICATION.md")
    print("   2. Manually review UNKNOWN tools")
    print("   3. Move NOISE tools to scripts/")
    print("   4. Update toolbelt registry")
    print("   5. Update compliance baseline")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
