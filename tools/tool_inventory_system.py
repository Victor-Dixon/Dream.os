#!/usr/bin/env python3
"""
Tool Inventory System for Tools Consolidation
Comprehensive catalog and analysis of all repository tools
"""

import json
import os
import ast
import inspect
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
import re

class ToolInventorySystem:
    """Comprehensive tool inventory and analysis system"""

    def __init__(self):
        self.repo_root = Path(__file__).resolve().parents[1]
        self.tools_dir = self.repo_root / "tools"
        self.inventory = {}
        self.dependencies = {}
        self.usage_patterns = {}

    def scan_tools_directory(self) -> Dict[str, Any]:
        """Scan the tools directory for all Python tools"""
        tools_inventory = {}

        if not self.tools_dir.exists():
            return tools_inventory

        # Scan for Python files
        for py_file in self.tools_dir.rglob("*.py"):
            if py_file.name.startswith("__"):
                continue

            tool_info = self.analyze_tool_file(py_file)
            if tool_info:
                tool_key = py_file.relative_to(self.repo_root).as_posix()
                tools_inventory[tool_key] = tool_info

        return tools_inventory

    def analyze_tool_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single tool file for metadata and characteristics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return None

        # Parse AST for analysis
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return None

        # Extract tool metadata
        tool_info = {
            "file_path": str(file_path.relative_to(self.repo_root)),
            "file_size": len(content),
            "line_count": len(content.split('\n')),
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "functions": [],
            "classes": [],
            "imports": [],
            "dependencies": [],
            "capabilities": [],
            "complexity_score": 0,
            "duplication_risk": "low"
        }

        # Extract functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                tool_info["functions"].append({
                    "name": node.name,
                    "args": len(node.args.args),
                    "line_start": node.lineno,
                    "complexity": self._calculate_complexity(node)
                })
            elif isinstance(node, ast.ClassDef):
                tool_info["classes"].append({
                    "name": node.name,
                    "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    "line_start": node.lineno
                })
            elif isinstance(node, ast.Import):
                tool_info["imports"].extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                tool_info["imports"].extend([f"{module}.{alias.name}" for alias in node.names])

        # Analyze capabilities based on function names and content
        tool_info["capabilities"] = self._analyze_capabilities(content, tool_info["functions"])

        # Calculate complexity score
        tool_info["complexity_score"] = self._calculate_file_complexity(tool_info)

        # Assess duplication risk
        tool_info["duplication_risk"] = self._assess_duplication_risk(content)

        # Extract dependencies
        tool_info["dependencies"] = self._extract_dependencies(content)

        return tool_info

    def _analyze_capabilities(self, content: str, functions: List[Dict]) -> List[str]:
        """Analyze what capabilities a tool provides"""
        capabilities = []
        content_lower = content.lower()
        function_names = [f["name"].lower() for f in functions]

        # WordPress capabilities
        if any(word in content_lower for word in ["wordpress", "wp_cli", "post create"]):
            capabilities.append("wordpress_management")
        if any(word in content_lower for word in ["page", "post", "content"]):
            capabilities.append("content_management")

        # Validation capabilities
        if any(word in content_lower for word in ["validate", "check", "test", "verify"]):
            capabilities.append("validation")
        if any(word in content_lower for word in ["http", "requests", "url"]):
            capabilities.append("http_validation")

        # SSH/Remote capabilities
        if any(word in content_lower for word in ["ssh", "paramiko", "remote", "server"]):
            capabilities.append("remote_operations")

        # Reporting capabilities
        if any(word in content_lower for word in ["report", "summary", "analytics"]):
            capabilities.append("reporting")

        # System management
        if any(word in content_lower for word in ["agent", "onboard", "workspace"]):
            capabilities.append("system_management")

        # Function-based capabilities
        if any(name in function_names for name in ["create_page", "update_post", "validate_url"]):
            capabilities.append("wordpress_operations")
        if any(name in function_names for name in ["run_validation", "check_status"]):
            capabilities.append("validation_operations")

        return list(set(capabilities))

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _calculate_file_complexity(self, tool_info: Dict) -> int:
        """Calculate overall file complexity score"""
        score = 0

        # Size factors
        score += tool_info["line_count"] // 50
        score += len(tool_info["functions"]) * 2
        score += len(tool_info["classes"]) * 5

        # Complexity factors
        for func in tool_info["functions"]:
            score += func["complexity"]

        return score

    def _assess_duplication_risk(self, content: str) -> str:
        """Assess the risk of code duplication in this tool"""
        risk_score = 0

        # Check for common duplication patterns
        patterns = [
            r"paramiko\.SSHClient\(\)",  # SSH connection
            r"requests\.get\(",          # HTTP requests
            r"subprocess\.run\(",        # System calls
            r"json\.load\(",             # JSON parsing
            r"BeautifulSoup\(.*\)",      # HTML parsing
        ]

        for pattern in patterns:
            matches = len(re.findall(pattern, content))
            if matches > 1:
                risk_score += matches

        # Size-based risk
        if len(content.split('\n')) > 200:
            risk_score += 2

        # Function count risk
        functions = len(re.findall(r"def \w+\(", content))
        if functions > 10:
            risk_score += 1

        if risk_score >= 5:
            return "high"
        elif risk_score >= 3:
            return "medium"
        else:
            return "low"

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract external dependencies from imports"""
        dependencies = set()

        # Standard library (exclude)
        stdlib = {
            "os", "sys", "json", "datetime", "pathlib", "typing", "re",
            "subprocess", "argparse", "logging", "functools", "itertools"
        }

        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                # Extract module names
                if " import " in line:
                    module_part = line.split(" import ")[0].replace("from ", "").replace("import ", "")
                    modules = [m.strip() for m in module_part.split(",")]
                    for module in modules:
                        base_module = module.split(".")[0]
                        if base_module and base_module not in stdlib:
                            dependencies.add(base_module)
                else:
                    module = line.replace("import ", "").split(".")[0].strip()
                    if module and module not in stdlib:
                        dependencies.add(module)

        return sorted(list(dependencies))

    def analyze_dependencies(self, inventory: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dependencies across all tools"""
        dependency_analysis = {
            "shared_dependencies": {},
            "tool_clusters": {},
            "dependency_graph": {},
            "consolidation_opportunities": []
        }

        # Count dependency usage
        dep_usage = {}
        tool_deps = {}

        for tool_path, tool_info in inventory.items():
            tool_name = Path(tool_path).stem
            tool_deps[tool_name] = tool_info["dependencies"]

            for dep in tool_info["dependencies"]:
                if dep not in dep_usage:
                    dep_usage[dep] = []
                dep_usage[dep].append(tool_name)

        # Identify shared dependencies
        dependency_analysis["shared_dependencies"] = {
            dep: tools for dep, tools in dep_usage.items() if len(tools) > 1
        }

        # Identify tool clusters based on shared capabilities
        capabilities_clusters = {}
        for tool_path, tool_info in inventory.items():
            tool_name = Path(tool_path).stem
            for cap in tool_info["capabilities"]:
                if cap not in capabilities_clusters:
                    capabilities_clusters[cap] = []
                capabilities_clusters[cap].append(tool_name)

        dependency_analysis["capability_clusters"] = capabilities_clusters

        # Find consolidation opportunities
        opportunities = []

        # Tools with similar capabilities
        for cap, tools in capabilities_clusters.items():
            if len(tools) > 2:
                opportunities.append({
                    "type": "capability_consolidation",
                    "capability": cap,
                    "tools": tools,
                    "recommendation": f"Consolidate {len(tools)} tools with {cap} capability"
                })

        # Tools sharing dependencies
        for dep, tools in dep_usage.items():
            if len(tools) > 2:
                opportunities.append({
                    "type": "dependency_sharing",
                    "dependency": dep,
                    "tools": tools,
                    "recommendation": f"Extract shared {dep} logic to utility module"
                })

        dependency_analysis["consolidation_opportunities"] = opportunities

        return dependency_analysis

    def generate_inventory_report(self) -> Dict[str, Any]:
        """Generate complete inventory report"""
        print("🔍 Scanning tools directory...")
        inventory = self.scan_tools_directory()

        print(f"📊 Found {len(inventory)} tools")
        dependency_analysis = self.analyze_dependencies(inventory)

        report = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_tools": len(inventory),
            "inventory": inventory,
            "dependency_analysis": dependency_analysis,
            "consolidation_metrics": {
                "high_duplication_risk": len([t for t in inventory.values() if t["duplication_risk"] == "high"]),
                "shared_dependencies_count": len(dependency_analysis["shared_dependencies"]),
                "consolidation_opportunities": len(dependency_analysis["consolidation_opportunities"]),
                "total_capabilities": len(set(cap for t in inventory.values() for cap in t["capabilities"]))
            },
            "recommendations": self._generate_recommendations(inventory, dependency_analysis)
        }

        return report

    def _generate_recommendations(self, inventory: Dict, dependency_analysis: Dict) -> List[str]:
        """Generate consolidation recommendations"""
        recommendations = []

        # High duplication risk tools
        high_risk_tools = [path for path, info in inventory.items() if info["duplication_risk"] == "high"]
        if high_risk_tools:
            recommendations.append(f"🔴 PRIORITY: Address {len(high_risk_tools)} high-duplication-risk tools: {', '.join(high_risk_tools[:3])}")

        # Shared dependencies
        shared_deps = dependency_analysis["shared_dependencies"]
        if len(shared_deps) > 0:
            recommendations.append(f"🔵 EXTRACT: {len(shared_deps)} shared dependencies can be moved to utilities")

        # Capability consolidation
        cap_clusters = dependency_analysis["capability_clusters"]
        large_clusters = {cap: tools for cap, tools in cap_clusters.items() if len(tools) > 2}
        if large_clusters:
            recommendations.append(f"🟡 CONSOLIDATE: {len(large_clusters)} capability areas need consolidation")

        # Complexity analysis
        complex_tools = sorted(
            [(path, info["complexity_score"]) for path, info in inventory.items()],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        if complex_tools:
            recommendations.append(f"🟠 REFACTOR: Top complex tools: {', '.join([t[0] for t in complex_tools])}")

        return recommendations

    def save_inventory_report(self, filename: Optional[str] = None) -> str:
        """Save inventory report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tool_inventory_{timestamp}.json"

        report_path = self.repo_root / filename
        report = self.generate_inventory_report()

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        return str(report_path)

def main():
    """Generate and display tool inventory"""
    print("🏗️ TOOL INVENTORY SYSTEM")
    print("=" * 50)

    inventory_system = ToolInventorySystem()
    report = inventory_system.generate_inventory_report()

    # Save report
    report_path = inventory_system.save_inventory_report()
    print(f"✅ Inventory saved to: {report_path}")
    print()

    # Display summary
    print("📊 INVENTORY SUMMARY")
    print("-" * 30)
    print(f"Total Tools: {report['total_tools']}")
    print(f"High Duplication Risk: {report['consolidation_metrics']['high_duplication_risk']}")
    print(f"Shared Dependencies: {report['consolidation_metrics']['shared_dependencies_count']}")
    print(f"Consolidation Opportunities: {report['consolidation_metrics']['consolidation_opportunities']}")
    print(f"Total Capabilities: {report['consolidation_metrics']['total_capabilities']}")
    print()

    print("🎯 KEY RECOMMENDATIONS")
    print("-" * 30)
    for rec in report["recommendations"]:
        print(f"• {rec}")
    print()

    print("📋 CONSOLIDATION OPPORTUNITIES")
    print("-" * 30)
    for opp in report["dependency_analysis"]["consolidation_opportunities"][:5]:  # Show top 5
        print(f"• {opp['recommendation']}")
        print(f"  Tools: {', '.join(opp['tools'][:3])}...")
    print()

    if report["consolidation_metrics"]["consolidation_opportunities"] > 5:
        print(f"... and {report['consolidation_metrics']['consolidation_opportunities'] - 5} more opportunities")
    print()

    print("✅ TOOL INVENTORY COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()