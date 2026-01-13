#!/usr/bin/env python3
"""
Comprehensive Tool Registry Audit
=================================

Scans the codebase for potential tools and updates the tool registry.
This script performs the "1444+ tool audit" by identifying:
1. Registered tools in `tool_registry.lock.json`
2. Unregistered potential tools (scripts with main(), classes with execute())
3. Validating all discovered tools

Author: Agent-8 (SSOT & System Integration)
"""

import os
import sys
import json
import ast
import logging
from pathlib import Path
from typing import Dict, List, Set, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.audit.audit_toolbelt import ToolbeltHealthAuditor
except ImportError:
    try:
        from audit.audit_toolbelt import ToolbeltHealthAuditor
    except ImportError:
        sys.path.append(str(project_root / "tools"))
        from audit.audit_toolbelt import ToolbeltHealthAuditor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ToolDiscoveryAuditor:
    def __init__(self):
        self.root = project_root
        self.registry_path = self.root / "tools" / "tool_registry.lock.json"
        self.discovered_tools: List[Dict[str, Any]] = []
        self.potential_scripts: List[str] = []
        
    def scan_for_tools(self):
        """Scan codebase for tools."""
        logger.info("🔍 Scanning codebase for tools...")
        
        # 1. Scan tools/categories for Tool classes
        self._scan_categories()
        
        # 2. Scan tools/ root for scripts
        self._scan_scripts(self.root / "tools")
        
        # 3. Scan scripts/ directory
        self._scan_scripts(self.root / "scripts")
        
        logger.info(f"✅ Found {len(self.discovered_tools)} tool classes")
        logger.info(f"✅ Found {len(self.potential_scripts)} standalone scripts")

    def _scan_categories(self):
        """Scan tools/categories for IToolAdapter implementations."""
        categories_dir = self.root / "tools" / "categories"
        if not categories_dir.exists():
            return
            
        for file in categories_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
                
            try:
                with open(file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # Simple heuristic: Check if class name ends with 'Tool' or 'Adapter'
                        if node.name.endswith("Tool") or node.name.endswith("Adapter"):
                            # Check if it has 'execute' method
                            has_execute = any(
                                isinstance(n, ast.FunctionDef) and n.name == "execute" 
                                for n in node.body
                            )
                            if has_execute:
                                module_path = f"tools.categories.{file.stem}"
                                self.discovered_tools.append({
                                    "name": node.name,
                                    "module": module_path,
                                    "class": node.name,
                                    "category": file.stem.replace("_tools", "")
                                })
            except Exception as e:
                logger.warning(f"Failed to parse {file}: {e}")

    def _scan_scripts(self, directory: Path):
        """Scan directory for standalone scripts with main()."""
        if not directory.exists():
            return
            
        for file in directory.glob("*.py"):
            if file.name == "__init__.py":
                continue
                
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                if 'if __name__ == "__main__":' in content or "if __name__ == '__main__':" in content:
                    rel_path = file.relative_to(self.root)
                    self.potential_scripts.append(str(rel_path))
            except Exception:
                pass

    def generate_report(self):
        """Generate audit report."""
        report = {
            "summary": {
                "discovered_tool_classes": len(self.discovered_tools),
                "potential_scripts": len(self.potential_scripts),
                "total_assets": len(self.discovered_tools) + len(self.potential_scripts)
            },
            "tool_classes": self.discovered_tools,
            "scripts": self.potential_scripts
        }
        
        output_path = self.root / "reports" / "comprehensive_tool_audit.json"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"✅ Audit report saved to {output_path}")
        
        # Also generate markdown
        md_path = self.root / "docs" / "toolbelt" / "COMPREHENSIVE_TOOL_AUDIT.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Comprehensive Tool Audit Report\n\n")
            f.write(f"**Total Assets Found:** {report['summary']['total_assets']}\n\n")
            
            f.write("## 🛠️ Tool Classes\n")
            f.write(f"Found {len(self.discovered_tools)} tool classes in `tools/categories/`.\n\n")
            f.write("| Tool Class | Module | Category |\n")
            f.write("|------------|--------|----------|\n")
            for tool in self.discovered_tools:
                f.write(f"| `{tool['name']}` | `{tool['module']}` | `{tool['category']}` |\n")
            
            f.write("\n## 📜 Standalone Scripts\n")
            f.write(f"Found {len(self.potential_scripts)} scripts with `main()` entry points.\n\n")
            for script in sorted(self.potential_scripts):
                f.write(f"- `{script}`\n")
                
        logger.info(f"✅ Markdown report saved to {md_path}")

def main():
    auditor = ToolDiscoveryAuditor()
    auditor.scan_for_tools()
    auditor.generate_report()
    
    # Run health check on existing registry
    print("\nRunning existing registry health check...")
    registry_path = project_root / "tools" / "tool_registry.lock.json"
    health_auditor = ToolbeltHealthAuditor(registry_path=str(registry_path))
    health_auditor.run_audit()

if __name__ == "__main__":
    main()
