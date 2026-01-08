#!/usr/bin/env python3
"""
A2A Coordination Analyzer
Automated analysis tool for A2A coordination requests

Usage:
    python tools/a2a_coordination_analyzer.py --analyze-file src/services/unified_command_handlers.py --v2-compliance
    python tools/a2a_coordination_analyzer.py --analyze-request "V2 compliance modularization"
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, List, Optional


class A2ACoordinationAnalyzer:
    """Analyzes files and coordination requests for A2A response preparation"""

    def __init__(self):
        self.v2_target_lines = 600
        self.findings = {}

    def analyze_file_compliance(self, file_path: str) -> Dict:
        """Analyze file for V2 compliance and modularization opportunities"""
        result = {
            "file_path": file_path,
            "exists": False,
            "line_count": 0,
            "compliance_status": "UNKNOWN",
            "over_limit": 0,
            "structure_analysis": {},
            "modularization_candidates": [],
            "recommendations": []
        }

        if not os.path.exists(file_path):
            result["error"] = f"File not found: {file_path}"
            return result

        result["exists"] = True

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                result["line_count"] = len(lines)

                # Check V2 compliance
                if result["line_count"] < self.v2_target_lines:
                    result["compliance_status"] = "COMPLIANT"
                else:
                    result["over_limit"] = result["line_count"] - self.v2_target_lines
                    result["compliance_status"] = f"NON_COMPLIANT (+{result['over_limit']} lines)"

                # Analyze structure
                result["structure_analysis"] = self._analyze_file_structure(lines)

                # Identify modularization candidates
                result["modularization_candidates"] = self._identify_modularization_candidates(lines)

                # Generate recommendations
                result["recommendations"] = self._generate_modularization_recommendations(result)

        except Exception as e:
            result["error"] = f"Analysis failed: {str(e)}"

        return result

    def _analyze_file_structure(self, lines: List[str]) -> Dict:
        """Analyze the structural composition of the file"""
        structure = {
            "classes": [],
            "functions": [],
            "imports": 0,
            "comments": 0,
            "blank_lines": 0,
            "code_lines": 0
        }

        for i, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                structure["blank_lines"] += 1
            elif stripped.startswith("#"):
                structure["comments"] += 1
            elif stripped.startswith("import ") or stripped.startswith("from "):
                structure["imports"] += 1
            elif stripped.startswith("class "):
                class_match = re.match(r'class\s+(\w+)', stripped)
                if class_match:
                    structure["classes"].append({
                        "name": class_match.group(1),
                        "line": i + 1
                    })
            elif stripped.startswith("def ") or stripped.startswith("async def "):
                func_match = re.match(r'(?:async\s+)?def\s+(\w+)', stripped)
                if func_match:
                    structure["functions"].append({
                        "name": func_match.group(1),
                        "line": i + 1
                    })
            else:
                structure["code_lines"] += 1

        return structure

    def _identify_modularization_candidates(self, lines: List[str]) -> List[Dict]:
        """Identify potential modularization opportunities"""
        candidates = []

        # Look for class-based modularization
        current_class = None
        class_start = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith("class "):
                # Save previous class if it exists
                if current_class and class_start is not None:
                    class_end = i - 1
                    class_lines = class_end - class_start + 1
                    candidates.append({
                        "type": "class",
                        "name": current_class,
                        "lines": class_lines,
                        "line_range": f"{class_start + 1}-{class_end + 1}",
                        "reason": f"Class with {class_lines} lines could be extracted"
                    })

                # Start new class
                class_match = re.match(r'class\s+(\w+)', stripped)
                current_class = class_match.group(1) if class_match else None
                class_start = i

        # Handle the last class
        if current_class and class_start is not None:
            class_lines = len(lines) - class_start
            candidates.append({
                "type": "class",
                "name": current_class,
                "lines": class_lines,
                "line_range": f"{class_start + 1}-{len(lines)}",
                "reason": f"Class with {class_lines} lines could be extracted"
            })

        return candidates

    def _generate_modularization_recommendations(self, analysis_result: Dict) -> List[str]:
        """Generate specific modularization recommendations"""
        recommendations = []

        if analysis_result["compliance_status"].startswith("NON_COMPLIANT"):
            over_limit = analysis_result["over_limit"]
            recommendations.append(f"Reduce file size by {over_limit} lines to meet V2 compliance (<{self.v2_target_lines} lines)")

        candidates = analysis_result["modularization_candidates"]
        if candidates:
            total_candidate_lines = sum(c["lines"] for c in candidates)
            recommendations.append(f"Extract {len(candidates)} classes ({total_candidate_lines} lines) into separate modules")

            # Suggest specific extraction strategy
            if len(candidates) >= 3:
                recommendations.append("Consider service layer pattern: extract classes into focused service modules")
            elif len(candidates) == 2:
                recommendations.append("Split into 2 focused modules following single responsibility principle")

        structure = analysis_result["structure_analysis"]
        if structure["classes"] and structure["functions"]:
            recommendations.append("Separate business logic classes from utility functions for better organization")

        return recommendations

    def prepare_coordination_response(self, analysis_result: Dict, request_context: str = "") -> Dict:
        """Prepare A2A coordination response based on analysis"""
        response = {
            "acceptance": "✅ ACCEPT",
            "approach": "Service layer modularization extracting consolidated command handlers",
            "technical_details": f"File: {analysis_result['line_count']} lines ({analysis_result['compliance_status']})",
            "synergy": "Integration expertise complements modularization requirements for V2 compliance",
            "timeline": "Immediate execution with phased rollout within coordination window"
        }

        if analysis_result["modularization_candidates"]:
            candidates = analysis_result["modularization_candidates"]
            response["approach"] = f"Extract {len(candidates)} command handler classes into focused service modules"

        return response

    def generate_report(self, analysis_result: Dict) -> str:
        """Generate human-readable analysis report"""
        report = f"""# A2A Coordination Analysis Report
**File:** {analysis_result['file_path']}
**Lines:** {analysis_result['line_count']}
**V2 Compliance:** {analysis_result['compliance_status']}

## File Structure Analysis
"""

        if "error" in analysis_result:
            report += f"**Error:** {analysis_result['error']}\n"
            return report

        structure = analysis_result["structure_analysis"]
        report += f"- **Classes:** {len(structure['classes'])}\n"
        report += f"- **Functions:** {len(structure['functions'])}\n"
        report += f"- **Imports:** {structure['imports']}\n"
        report += f"- **Comments:** {structure['comments']}\n"
        report += f"- **Code Lines:** {structure['code_lines']}\n"
        report += f"- **Blank Lines:** {structure['blank_lines']}\n"

        if analysis_result["modularization_candidates"]:
            report += "\n## Modularization Candidates\n"
            for candidate in analysis_result["modularization_candidates"]:
                report += f"- **{candidate['name']}** ({candidate['type']}): {candidate['lines']} lines ({candidate['line_range']})\n"
                report += f"  *{candidate['reason']}*\n"

        if analysis_result["recommendations"]:
            report += "\n## Recommendations\n"
            for rec in analysis_result["recommendations"]:
                report += f"- {rec}\n"

        return report


def main():
    parser = argparse.ArgumentParser(description="A2A Coordination Analyzer")
    parser.add_argument("--analyze-file", help="Analyze specific file for V2 compliance")
    parser.add_argument("--v2-compliance", action="store_true", help="Focus on V2 compliance analysis")
    parser.add_argument("--prepare-response", action="store_true", help="Prepare A2A coordination response")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    analyzer = A2ACoordinationAnalyzer()

    if args.analyze_file:
        result = analyzer.analyze_file_compliance(args.analyze_file)
        report = analyzer.generate_report(result)

        if args.prepare_response:
            response = analyzer.prepare_coordination_response(result)
            report += f"\n## A2A Coordination Response\n"
            report += f"- **Acceptance:** {response['acceptance']}\n"
            report += f"- **Approach:** {response['approach']}\n"
            report += f"- **Technical Details:** {response['technical_details']}\n"
            report += f"- **Synergy:** {response['synergy']}\n"
            report += f"- **Timeline:** {response['timeline']}\n"

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Analysis saved to {args.output}")
        else:
            print(report)

    else:
        print("Use --analyze-file to specify a file to analyze")


if __name__ == "__main__":
    main()