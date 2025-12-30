#!/usr/bin/env python3
"""
Toolbelt Health Audit
=====================

Comprehensive audit of toolbelt functionality and health status.
Validates tool functionality, identifies broken tools, and generates health reports.

Author: Agent-5 (Business Intelligence Specialist)
Domain: tools
"""

import importlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ToolbeltHealthAuditor:
    """Audits toolbelt health and generates comprehensive reports."""

    def __init__(self, registry_path: str = "tools_v2/tool_registry.lock.json"):
        """Initialize auditor with registry path."""
        self.registry_path = Path(registry_path)
        self.registry_data: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {
            "audit_date": datetime.now().isoformat(),
            "total_tools": 0,
            "working_tools": [],
            "broken_tools": [],
            "by_category": {},
            "error_types": {},
            "health_metrics": {},
        }

    def load_registry(self) -> bool:
        """Load tool registry from JSON file."""
        try:
            if not self.registry_path.exists():
                logger.error(f"Registry file not found: {self.registry_path}")
                return False

            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.registry_data = data.get("tools", {})
                self.results["total_tools"] = len(self.registry_data)
                logger.info(f"✅ Loaded {len(self.registry_data)} tools from registry")
                return True

        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
            return False

    def audit_tool(self, tool_name: str, module_path: str, class_name: str) -> Tuple[bool, str, str]:
        """
        Audit a single tool for functionality.
        
        Returns:
            (is_working, error_type, error_message)
        """
        try:
            # Test 1: Module import
            try:
                module = importlib.import_module(module_path)
            except ImportError as e:
                return False, "ImportError", str(e)
            except ModuleNotFoundError as e:
                return False, "ModuleNotFoundError", str(e)

            # Test 2: Class resolution
            try:
                tool_class = getattr(module, class_name)
            except AttributeError as e:
                return False, "AttributeError", f"Class '{class_name}' not found: {e}"

            # Test 3: Basic instantiation check (try to get class, don't fully instantiate)
            if not callable(tool_class):
                return False, "TypeError", f"'{class_name}' is not callable"

            # Tool is working
            return True, "", ""

        except SyntaxError as e:
            return False, "SyntaxError", str(e)
        except Exception as e:
            return False, "RuntimeError", str(e)

    def audit_all_tools(self) -> None:
        """Audit all tools in the registry."""
        if not self.registry_data:
            logger.error("Registry not loaded. Call load_registry() first.")
            return

        logger.info(f"🔍 Auditing {len(self.registry_data)} tools...")
        print(f"\n🔍 Toolbelt Health Audit - Auditing {len(self.registry_data)} tools")
        print("=" * 70)

        working_count = 0
        broken_count = 0

        for i, (tool_name, tool_info) in enumerate(
            sorted(self.registry_data.items()), 1
        ):
            if not isinstance(tool_info, list) or len(tool_info) < 2:
                logger.warning(f"Invalid tool info for {tool_name}: {tool_info}")
                continue

            module_path, class_name = tool_info[0], tool_info[1]
            category = tool_name.split(".")[0] if "." in tool_name else "unknown"

            # Audit tool
            is_working, error_type, error_msg = self.audit_tool(
                tool_name, module_path, class_name
            )

            # Track results
            tool_result = {
                "tool_name": tool_name,
                "module_path": module_path,
                "class_name": class_name,
                "category": category,
                "status": "working" if is_working else "broken",
                "error_type": error_type if not is_working else None,
                "error_message": error_msg if not is_working else None,
            }

            if is_working:
                working_count += 1
                self.results["working_tools"].append(tool_result)
                status_symbol = "✅"
            else:
                broken_count += 1
                self.results["broken_tools"].append(tool_result)
                status_symbol = "❌"

                # Track error types
                if error_type not in self.results["error_types"]:
                    self.results["error_types"][error_type] = []
                self.results["error_types"][error_type].append(tool_name)

            # Track by category
            if category not in self.results["by_category"]:
                self.results["by_category"][category] = {
                    "total": 0,
                    "working": 0,
                    "broken": 0,
                    "tools": [],
                }

            self.results["by_category"][category]["total"] += 1
            if is_working:
                self.results["by_category"][category]["working"] += 1
            else:
                self.results["by_category"][category]["broken"] += 1

            self.results["by_category"][category]["tools"].append(tool_result)

            # Print progress
            print(
                f"{i:3d}/{len(self.registry_data):3d} {status_symbol} {tool_name:<40} "
                f"[{category}]"
            )
            if not is_working:
                print(f"      └─ {error_type}: {error_msg[:60]}")

        # Calculate health metrics
        self.results["health_metrics"] = {
            "total_tools": len(self.registry_data),
            "working_tools": working_count,
            "broken_tools": broken_count,
            "health_percentage": (
                (working_count / len(self.registry_data) * 100)
                if self.registry_data
                else 0
            ),
            "categories_total": len(self.results["by_category"]),
            "error_types_total": len(self.results["error_types"]),
        }

        print("\n" + "=" * 70)
        print(f"📊 AUDIT COMPLETE")
        print(f"✅ Working tools: {working_count}/{len(self.registry_data)}")
        print(f"❌ Broken tools: {broken_count}/{len(self.registry_data)}")
        print(
            f"📈 Health: {self.results['health_metrics']['health_percentage']:.1f}%"
        )

    def generate_json_report(self, output_path: str = "toolbelt_health_audit.json") -> None:
        """Generate JSON report with audit results."""
        output_file = Path(output_path)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ JSON report saved to {output_file}")
        print(f"\n💾 JSON report saved to {output_file}")

    def generate_markdown_report(
        self, output_path: str = "docs/toolbelt/TOOLBELT_HEALTH_AUDIT_REPORT.md"
    ) -> None:
        """Generate comprehensive Markdown health report."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        metrics = self.results["health_metrics"]
        health_pct = metrics["health_percentage"]

        # Determine health status
        if health_pct >= 95:
            health_status = "🟢 EXCELLENT"
        elif health_pct >= 80:
            health_status = "🟡 GOOD"
        elif health_pct >= 60:
            health_status = "🟠 NEEDS ATTENTION"
        else:
            health_status = "🔴 CRITICAL"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Toolbelt Health Audit Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Agent:** Agent-5 (Business Intelligence Specialist)  \n")
            f.write(f"**Status:** {'✅ AUDIT COMPLETE' if self.results else '⚠️ IN PROGRESS'}\n\n")
            f.write("---\n\n")

            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"**Total Tools Audited:** {metrics['total_tools']}  \n")
            f.write(f"**Working Tools:** {metrics['working_tools']} ({health_pct:.1f}%)  \n")
            f.write(f"**Broken Tools:** {metrics['broken_tools']} ({100-health_pct:.1f}%)  \n")
            f.write(f"**Health Status:** {health_status}  \n")
            f.write(f"**Categories:** {metrics['categories_total']}  \n")
            f.write(f"**Error Types:** {metrics['error_types_total']}  \n\n")
            f.write("---\n\n")

            # Health by Category
            f.write("## 📋 Health by Category\n\n")
            f.write("| Category | Total | Working | Broken | Health % |\n")
            f.write("|----------|-------|---------|--------|----------|\n")

            for category in sorted(self.results["by_category"].keys()):
                cat_data = self.results["by_category"][category]
                cat_health = (
                    (cat_data["working"] / cat_data["total"] * 100)
                    if cat_data["total"] > 0
                    else 0
                )
                f.write(
                    f"| `{category}` | {cat_data['total']} | {cat_data['working']} | "
                    f"{cat_data['broken']} | {cat_health:.1f}% |\n"
                )

            f.write("\n---\n\n")

            # Error Analysis
            if self.results["error_types"]:
                f.write("## ❌ Error Analysis\n\n")
                f.write("### Error Types Distribution\n\n")
                f.write("| Error Type | Count | Tools |\n")
                f.write("|------------|-------|-------|\n")

                for error_type, tools in sorted(
                    self.results["error_types"].items(),
                    key=lambda x: len(x[1]),
                    reverse=True,
                ):
                    f.write(f"| `{error_type}` | {len(tools)} | ")
                    f.write(", ".join([f"`{t}`" for t in tools[:5]]))
                    if len(tools) > 5:
                        f.write(f" ... ({len(tools)-5} more)")
                    f.write(" |\n")

                f.write("\n---\n\n")

            # Broken Tools Details
            if self.results["broken_tools"]:
                f.write("## 🔧 Broken Tools Details\n\n")
                for tool in sorted(
                    self.results["broken_tools"], key=lambda x: x["category"]
                ):
                    f.write(f"### `{tool['tool_name']}`\n\n")
                    f.write(f"- **Category:** `{tool['category']}`  \n")
                    f.write(f"- **Module:** `{tool['module_path']}`  \n")
                    f.write(f"- **Class:** `{tool['class_name']}`  \n")
                    f.write(f"- **Error Type:** `{tool['error_type']}`  \n")
                    f.write(f"- **Error Message:** `{tool['error_message']}`  \n\n")

                f.write("---\n\n")

            # Recommendations
            f.write("## 💡 Recommendations\n\n")
            if metrics["broken_tools"] > 0:
                f.write(f"1. **Immediate Action:** Fix {metrics['broken_tools']} broken tools\n")
                f.write("2. **Priority:** Address tools with ImportError first (module resolution)\n")
                f.write("3. **Categories:** Focus on categories with <80% health\n")
                f.write("4. **Testing:** Add automated tests for tool imports\n")
            else:
                f.write("✅ **All tools are working!** Maintain this health status.\n")

            f.write("\n---\n\n")
            f.write("*Report generated by Agent-5 (Business Intelligence Specialist)*\n")

        logger.info(f"✅ Markdown report saved to {output_file}")
        print(f"📄 Markdown report saved to {output_file}")

    def run_audit(self) -> bool:
        """Run complete audit workflow."""
        logger.info("🚀 Starting toolbelt health audit...")

        if not self.load_registry():
            return False

        self.audit_all_tools()

        # Generate reports
        self.generate_json_report()
        self.generate_markdown_report()

        logger.info("✅ Toolbelt health audit complete!")
        return True


def main():
    """Main entry point."""
    auditor = ToolbeltHealthAuditor()
    success = auditor.run_audit()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())


